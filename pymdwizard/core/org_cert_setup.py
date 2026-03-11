# coding=utf-8
"""
Author:             Michael O'Donnell
Created:            8/7/2025
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

Citation:


PURPOSE
------------------------------------------------------------------------------
Set up of organization certificates (USGS/DOI) to access HTTPS sites from
government hardware.

NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import os
import time
import warnings

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

    # Imported below to be used for a backup if SSL fails.
    # import pip_system_certs
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
        certs (list): List of system certificates in binary format.

    Workflow:
        None

    Notes:
        Cannot recognize NotImplementedError(), so not using with try/except.
    """

    # Initiate default.
    certs = None
    try:
        # Create a default SSL context.
        ctx = ssl.create_default_context()

        # Load the operating system's certificate store.
        ctx.load_default_certs()

        # Get the list of certificates.
        # Method suggested for Mac and Windows, which works.
        try:
            certs = ctx._ctx.get_ca_certs(binary_form=True)
        except:
            # Method should work on all platforms, but not working for Windows.
            certs = ctx.get_ca_certs(binary_form=True)
    except:
        print(f"An unexpected error occurred using Python's SSL library when "
              f"attempting to retrieve system certificates.")
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

    if os.path.exists(local_cert_file):
        os.environ["PIP_CERT"] = local_cert_file
        os.environ["SSL_CERT_FILE"] = local_cert_file
        os.environ["GIT_SSL_CAINFO"] = local_cert_file
        os.environ["REQUESTS_CA_BUNDLE"] = local_cert_file
        return local_cert_file
    else:
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
                print(f"INVESTIGATE: Did not locate USGS organization "
                      f"certificate (may not be on a USGS system or something "
                      f"changed).")
        else:
            # pip-system-certs will automatically configure pip, requests,
            # urllib3, and other Python libraries that use the standard SSL
            # context to utilize your system's certificate store for SSL
            # verification. This method loads certs but prevents us from
            # exporting to PEM and therefore not desired.
            #
            # NOTE: conda virtual environments on Linux may install a separate
            # SSL certificate store which takes precedence over the system
            # store, potentially preventing this package from accessing
            # system-installed certificates.
            #
            # IMPORTANT: Currently, pip-system-certs versions above 4.0 cause
            # issues with truststore and causing ssl get_ca_certs() to result
            # in NotImplementedError()).
            print(f"SSL certificate retrieval failed and using a different "
                  f"method (pip_system_certs).")
            import pip_system_certs.wrapt_requests
            pip_system_certs.wrapt_requests.inject_truststore()
            local_cert_file = ""

    if os.path.exists(local_cert_file):
        os.environ["PIP_CERT"] = local_cert_file
        os.environ["SSL_CERT_FILE"] = local_cert_file
        os.environ["GIT_SSL_CAINFO"] = local_cert_file
        os.environ["REQUESTS_CA_BUNDLE"] = local_cert_file

    return local_cert_file


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Start time of script
    tot_start_comp_time = time.time()
    print("Started...\n")

    # Set up Cert for accessing https. DOI cert name.
    cert_file = "DOIRootCA2.pem"

    # Testing methods
    cert_file = cert_setup(cert_file)

    print("Output USGS PEM:", cert_file)

    print("\nCompleted...")
    tot_elapsed_comp_time = time.time() - tot_start_comp_time
    print("\tTotal Elapsed Time (min): " +
          str(float(tot_elapsed_comp_time / 60.0)))
