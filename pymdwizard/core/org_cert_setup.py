# coding=utf-8
"""
Author:             Michael O'Donnell
Created:            8/7/2025
License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

Citation:


PURPOSE
------------------------------------------------------------------------------
Setup for Department of Interior Organizational certificates, which is required
when access HTTPS. These methods aim to support Windows, Mac, and Linux
operating systems, but verification is provided in case changes occur or
methods not supported on all platforms.


NOTES
------------------------------------------------------------------------------
Info on libraries that can help with SSL issues:
# ----------------
pip_system_certs (not perfect support across all platforms):
    This will automatically configure pip, requests,
    urllib3, and other Python libraries that use the standard SSL
    context to utilize your system's certificate store for SSL
    verification. This method loads certs but prevents us from
    exporting to PEM and therefore not desired.

    NOTE: conda virtual environments on Linux may install a separate
    SSL certificate store which takes precedence over the system
    store, potentially preventing this package from accessing
    system-installed certificates.

    IMPORTANT: Currently, pip-system-certs versions above 4.0 cause
    issues with truststore and causing ssl get_ca_certs() to result
    in NotImplementedError()).

    Windows: Works well because it uses the Windows certificate store.
    Mac: Works well; accesses Keychain directly when needed.
    Linux: Works if your system CA certificates are in standard locations.

python-certifi-win32 (Windows only):
    This makes requests using the Windows certificate store (which commonly
    contains your org CA), fixing many corporate SSL errors without custom
    bundles. Only works on Windows.


UPDATE (2026-07): Added robust certificate retrieval with fallback methods:
# ----------------
    Windows: Works reliably using Python SSL library. Falls back to
      wincertstore if needed.
    Mac: Works by querying Keychain directly via the 'security' command when
      Python SSL library cannot access certificates. No additional packages
      required.
    Linux: Works if system CA certificates are in standard locations
      accessible to Python's SSL library.
"""

# Standard python libraries.
import os
import time
import warnings
import sys
import subprocess
import requests
import certifi

# Non-standard python libraries.
try:
    # Retrieve DOI organizational cert from OS, if applicable.
    import ssl
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    from cryptography.utils import CryptographyDeprecationWarning

    # Suppress CryptographyDeprecationWarning. Not required.
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore",
                            category=CryptographyDeprecationWarning)
except ImportError as err:
    raise ImportError(err, __file__)


def retrieve_certs_ssl():
    """
    Description:
        Method to obtain CA/ROOT system certs, so we can locate the
        USGS organizational certificate (if one exists).

    Passed arguments:
        None

    Returned objects:
        certs (list): List of system certificates in binary format (DER-encoded).

    Workflow:
        Tries multiple methods to retrieve system certificates with automatic
        fallback for maximum compatibility:
        1. Python SSL library via ctx._ctx (cryptography < 49)
        2. Python SSL library via ctx.get_ca_certs (some versions)
        3. Windows: Direct access via wincertstore library
        4. macOS: Direct Keychain access via 'security' command
        5. Linux: Relies on methods 1-2 with standard cert locations

    Notes:
        Compatible with cryptography 46.x through 49.x+.
        Handles API changes across Python and cryptography versions.
    """

    # Initiate default.
    certs = None

    try:
        # Create a default SSL context.
        ctx = ssl.create_default_context()

        # Load the operating system's certificate store.
        ctx.load_default_certs()

        # Method 1: Try private _ctx attribute (works in cryptography < 49).
        try:
            if hasattr(ctx, '_ctx') and hasattr(ctx._ctx, 'get_ca_certs'):
                certs = ctx._ctx.get_ca_certs(binary_form=True)
        except (AttributeError, NotImplementedError):
            pass

        # Method 2: Try direct get_ca_certs on context (some versions).
        if certs is None:
            try:
                if hasattr(ctx, 'get_ca_certs'):
                    certs = ctx.get_ca_certs(binary_form=True)
            except (AttributeError, NotImplementedError):
                pass

        # Method 3: Windows-specific fallback using wincertstore.
        if certs is None and sys.platform == "win32":
            try:
                import wincertstore
                certs = []
                for storename in ("CA", "ROOT"):
                    with wincertstore.CertSystemStore(storename) as store:
                        for cert in store.itercerts():
                            certs.append(cert.get_encoded())
                if not certs:
                    certs = None
            except (ImportError, Exception):
                pass

        # Method 4: macOS-specific fallback using Keychain via 'security' command.
        if certs is None and sys.platform == "darwin":
            try:
                result = subprocess.run(
                    ["security", "find-certificate", "-a", "-p"],
                    capture_output=True,
                    check=True
                )
                # Parse PEM certificates from output and convert to DER.
                cert_data = result.stdout
                pem_certs = []
                current_cert = b""
                for line in cert_data.split(b'\n'):
                    current_cert += line + b'\n'
                    if b"-----END CERTIFICATE-----" in line:
                        try:
                            cert_obj = x509.load_pem_x509_certificate(
                                current_cert, default_backend())
                            pem_certs.append(
                                cert_obj.public_bytes(serialization.Encoding.DER))
                        except Exception:
                            pass
                        current_cert = b""
                if pem_certs:
                    certs = pem_certs
            except (FileNotFoundError, subprocess.CalledProcessError, Exception):
                pass

    except Exception as e:
        print(f"An unexpected error occurred using Python's SSL library when "
              f"attempting to retrieve system certificates: {e}")
        certs = None

    return certs


def cert_setup(local_cert_file):
    """
    Description:
        Define organization certificate (PEM) to allow access to
        programmatically retrieve information for internet.

        IMPT: Works with pip_system_certs 4.0

    Passed arguments:
        local_cert_file (String): Path and file name of DOI PEM file.

    Returned objects:
        None

    Workflow:
        None

    Notes:
        None
    """

    # Hard codded name of organizational cert for DOI. Will likely change at
    # some point.
    alias_name = "DOIRootCA2"

    # Check if the DOI cert already exists in resources folder.
    # If not, extract it from the system certificate store.
    if not os.path.exists(local_cert_file):
        # Use the user's home directory for cross-platform compatibility.
        local_cert_file = os.path.join(os.path.expanduser("~"),
                                       "certificates", local_cert_file)
        cert_ws = os.path.dirname(local_cert_file)
        if not os.path.exists(cert_ws):
            os.makedirs(cert_ws)

        # Try using ssl installed with Python to obtain system certificates.
        certs = retrieve_certs_ssl()

        # If certs identified using ssl, try to export USGS organizational cert,
        # which will not exist or be required if user not on a USGS system.
        if certs is not None:
            # Initiate object.
            doi_cert = None

            # Iterate over each certificate in the list.
            for cert in certs:
                try:
                    # Load the certificate from DER format.
                    certificate = \
                        x509.load_der_x509_certificate(cert, default_backend())

                    # Extract the common names (CN) from the certificate's
                    # subject.
                    common_names = certificate.subject.get_attributes_for_oid(
                        x509.NameOID.COMMON_NAME)

                    # QAQC: Keep
                    # print(common_names)

                    # Check if the common names list is not empty and the first
                    # common name matches the alias name.
                    if common_names and common_names[0].value == alias_name:
                        # Assign the matching certificate to doi_cert.
                        doi_cert = certificate
                except ValueError as e:
                    print(f"Skipping invalid certificate: {e}")

            # Export the certificate to a PEM file if located.
            if doi_cert is not None:
                pem_data = doi_cert.public_bytes(
                    encoding=serialization.Encoding.PEM)
                with open(local_cert_file, "wb") as pem_file:
                    pem_file.write(pem_data)
            else:
                print("INVESTIGATE: Did not locate USGS organization "
                      "certificate (may not be on a USGS system or something "
                      "changed).")

    # Add organizational cert to certifi cert list installed with certifi
    # library.
    if os.path.exists(local_cert_file):
        # Obtain Python site-packages certs: site-packages\\certifi\\cacert.pem
        certifi_bundle = certifi.where()

        # New output.
        local_cert_file2 = os.path.join(
            os.path.splitext(local_cert_file)[0] +
            "_certifi" + os.path.splitext(local_cert_file)[1]
        )

        # Read both bundles and write the combined file (binary-safe).
        with (open(certifi_bundle, "rb") as f_certifi,
              open(local_cert_file, "rb") as f_org):
            combined_bytes = f_certifi.read() + f_org.read()

        with open(local_cert_file2, "wb") as f_out:
            f_out.write(combined_bytes)
    else:
        print("Certificate file NOT found...")

        # Obtain Python site-packages certs: site-packages\\certifi\\cacert.pem
        local_cert_file2 = certifi.where()

    # Rename variable.
    local_cert_file = local_cert_file2

    # Add to various SSL environments that tools may use.
    if os.path.exists(local_cert_file):
        os.environ["PIP_CERT"] = local_cert_file
        os.environ["SSL_CERT_FILE"] = local_cert_file
        os.environ["GIT_SSL_CAINFO"] = local_cert_file
        os.environ["REQUESTS_CA_BUNDLE"] = local_cert_file
        os.environ["CURL_CA_BUNDLE"] = local_cert_file

    # Test: should succeed
    resp = requests.get("https://google.com", verify=str(local_cert_file))
    if resp.status_code != 200:
        print("SSL error. Check PEM file or internet. Exiting...")
        sys.tracebacklimit = 1
        raise ValueError()

    return local_cert_file


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Start time of script
    tot_start_comp_time = time.time()
    print("Started...\n")

    # Set up Cert for accessing https.
    cert_file = "DOIRootCA2.pem"

    # Testing newer versions of pip_system_certs
    cert_file = cert_setup(cert_file)

    print("Output USGS PEM:", cert_file)

    print("\nCompleted...")
    tot_elapsed_comp_time = time.time() - tot_start_comp_time
    print("\tTotal Elapsed Time (min): " +
          str(float(tot_elapsed_comp_time / 60.0)))
