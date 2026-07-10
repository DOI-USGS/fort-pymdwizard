"""Unittests for core.org_cert_setup"""

import os
import sys
import tempfile
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pymdwizard.core import org_cert_setup


class TestRetrieveCertsSsl:
    """Tests for retrieve_certs_ssl() function."""

    def test_retrieve_certs_with_ctx_attribute(self):
        """Test certificate retrieval using ctx._ctx (cryptography < 49)."""
        mock_certs = [b"cert1", b"cert2"]

        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl:
            mock_ctx = Mock()
            mock_ctx._ctx = Mock()
            mock_ctx._ctx.get_ca_certs = Mock(return_value=mock_certs)
            mock_ssl.create_default_context.return_value = mock_ctx

            result = org_cert_setup.retrieve_certs_ssl()

            assert result == mock_certs
            mock_ctx.load_default_certs.assert_called_once()
            mock_ctx._ctx.get_ca_certs.assert_called_once_with(binary_form=True)

    def test_retrieve_certs_with_direct_method(self):
        """Test certificate retrieval using ctx.get_ca_certs (some versions)."""
        mock_certs = [b"cert1", b"cert2"]

        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl:
            mock_ctx = Mock()
            # Simulate ctx without _ctx attribute but with get_ca_certs
            del mock_ctx._ctx
            mock_ctx.get_ca_certs = Mock(return_value=mock_certs)
            mock_ssl.create_default_context.return_value = mock_ctx

            result = org_cert_setup.retrieve_certs_ssl()

            assert result == mock_certs
            mock_ctx.get_ca_certs.assert_called_once_with(binary_form=True)

    def test_retrieve_certs_fallback_to_direct_method(self):
        """Test fallback from ctx._ctx to ctx.get_ca_certs."""
        mock_certs = [b"cert1", b"cert2"]

        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl:
            mock_ctx = Mock()
            # First method raises AttributeError
            mock_ctx._ctx.get_ca_certs.side_effect = AttributeError()
            # Second method works
            mock_ctx.get_ca_certs = Mock(return_value=mock_certs)
            mock_ssl.create_default_context.return_value = mock_ctx

            result = org_cert_setup.retrieve_certs_ssl()

            assert result == mock_certs
            mock_ctx.get_ca_certs.assert_called_once_with(binary_form=True)

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_retrieve_certs_windows_fallback(self):
        """Test Windows wincertstore fallback when SSL methods fail."""
        mock_cert_data = b"windows_cert"

        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl, \
             patch("pymdwizard.core.org_cert_setup.sys.platform", "win32"):

            # SSL methods fail
            mock_ctx = Mock()
            mock_ctx._ctx.get_ca_certs.side_effect = AttributeError()
            del mock_ctx.get_ca_certs
            mock_ssl.create_default_context.return_value = mock_ctx

            # Mock wincertstore
            with patch.dict('sys.modules', {'wincertstore': MagicMock()}):
                import wincertstore
                mock_cert = Mock()
                mock_cert.get_encoded.return_value = mock_cert_data

                mock_store = MagicMock()
                mock_store.__enter__.return_value.itercerts.return_value = [mock_cert]
                wincertstore.CertSystemStore.return_value = mock_store

                result = org_cert_setup.retrieve_certs_ssl()

                # Should return certs from both CA and ROOT stores (2 stores × 1 cert each)
                assert result == [mock_cert_data, mock_cert_data]

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS-specific test")
    def test_retrieve_certs_macos_fallback(self):
        """Test macOS Keychain fallback when SSL methods fail."""
        # Sample PEM certificate
        pem_cert = (
            b"-----BEGIN CERTIFICATE-----\n"
            b"MIIBkTCB+wIJAKHHCgVZU4oAMA0GCSqGSIb3DQEBCwUAMBExDzANBgNVBAMMBnRl\n"
            b"c3RDQTAeFw0yMDA1MjcxNjQ5MjVaFw0yMTA1MjcxNjQ5MjVaMBExDzANBgNVBAMM\n"
            b"BnRlc3RDQTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAwXZqNqG3r3H9QJYH\n"
            b"CfKVVvJLpg0fvLXkEcgS6P3cZj9F5LsqVfL8P6qLkDJpC4Xa8m2J6HqF8qMPZqMR\n"
            b"Z9l4hA7HZvF4xN8P2LmLJ3qF9P6qLkDJpC4Xa8m2J6HqF8qMPZqMRZ9l4hA7HZvF\n"
            b"4xN8P2LmLJ3qF9P6qLkDJpC4Xa8m2J6HqF8qMPZqMRZ9l4hA7HZvF4xN8P2LmLJ3\n"
            b"qCAwEAATANBgkqhkiG9w0BAQsFAAOBgQBT8P6qLkDJpC4Xa8m2J6HqF8qMPZqMR\n"
            b"Z9l4hA7HZvF4xN8P2LmLJ3qF9P6qLkDJpC4Xa8m2J6HqF8qMPZqMRZ9l4hA7HZvF\n"
            b"4xN8P2LmLJ3qF9P6qLkDJpC4Xa8m2J6HqF8qMPZqMRZ9l4hA7HZvF4xN8P2LmLJ3\n"
            b"qF9P6qLkDJpC4Xa8m2J6HqF8qMPZqMRZ9l4hA7HZvF4xN8P2LmLJ3qF9P6qLkDJp\n"
            b"-----END CERTIFICATE-----\n"
        )

        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl, \
             patch("pymdwizard.core.org_cert_setup.sys.platform", "darwin"), \
             patch("pymdwizard.core.org_cert_setup.subprocess") as mock_subprocess:

            # SSL methods fail
            mock_ctx = Mock()
            mock_ctx._ctx.get_ca_certs.side_effect = AttributeError()
            del mock_ctx.get_ca_certs
            mock_ssl.create_default_context.return_value = mock_ctx

            # Mock subprocess returning PEM certificate
            mock_result = Mock()
            mock_result.stdout = pem_cert
            mock_subprocess.run.return_value = mock_result

            result = org_cert_setup.retrieve_certs_ssl()

            # Should return list with at least one certificate in DER format
            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], bytes)

            # Verify subprocess was called with correct command
            mock_subprocess.run.assert_called_once()
            call_args = mock_subprocess.run.call_args[0][0]
            assert call_args[0] == "security"
            assert "find-certificate" in call_args

    def test_retrieve_certs_returns_none_on_error(self):
        """Test that function returns None when all methods fail."""
        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl:
            mock_ssl.create_default_context.side_effect = Exception("SSL error")

            result = org_cert_setup.retrieve_certs_ssl()

            assert result is None

    def test_retrieve_certs_handles_notimplementederror(self):
        """Test handling of NotImplementedError from SSL methods."""
        with patch("pymdwizard.core.org_cert_setup.ssl") as mock_ssl:
            mock_ctx = Mock()
            mock_ctx._ctx.get_ca_certs.side_effect = NotImplementedError()
            mock_ctx.get_ca_certs.side_effect = NotImplementedError()
            mock_ssl.create_default_context.return_value = mock_ctx

            result = org_cert_setup.retrieve_certs_ssl()

            # Should return None when all SSL methods raise NotImplementedError
            assert result is None


class TestCertSetup:
    """Tests for cert_setup() function."""

    def test_cert_setup_uses_existing_cert_file(self, tmp_path):
        """Test that cert_setup uses existing certificate file if present."""
        # Create a temporary cert file
        cert_file = tmp_path / "DOIRootCA2.pem"
        cert_content = b"-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----\n"
        cert_file.write_bytes(cert_content)

        # Create mock certifi bundle
        certifi_bundle = tmp_path / "cacert.pem"
        certifi_content = b"certifi bundle"
        certifi_bundle.write_bytes(certifi_content)

        with patch("pymdwizard.core.org_cert_setup.certifi.where", return_value=str(certifi_bundle)), \
             patch("pymdwizard.core.org_cert_setup.requests.get") as mock_requests:

            mock_response = Mock()
            mock_response.status_code = 200
            mock_requests.return_value = mock_response

            result = org_cert_setup.cert_setup(str(cert_file))

            # Should create combined cert file
            assert result is not None
            assert os.path.exists(result)

            # Verify combined file contains both certifi bundle and org cert
            with open(result, "rb") as f:
                combined_content = f.read()
            assert certifi_content in combined_content
            assert cert_content in combined_content

    def test_cert_setup_extracts_doi_cert(self, tmp_path):
        """Test that cert_setup extracts DOI certificate from system certs."""
        # Use temporary directory for cert file
        cert_file = tmp_path / "DOIRootCA2.pem"
        certifi_bundle = tmp_path / "cacert.pem"
        certifi_bundle.write_bytes(b"certifi bundle")

        # Create a mock DOI certificate
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        from cryptography.x509.oid import NameOID
        import datetime

        # Generate a test certificate with CN=DOIRootCA2
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, "DOIRootCA2"),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        ).sign(private_key, hashes.SHA256(), default_backend())

        # Convert to DER format
        cert_der = cert.public_bytes(serialization.Encoding.DER)

        with patch("pymdwizard.core.org_cert_setup.retrieve_certs_ssl", return_value=[cert_der]), \
             patch("pymdwizard.core.org_cert_setup.certifi.where", return_value=str(certifi_bundle)), \
             patch("pymdwizard.core.org_cert_setup.requests.get") as mock_requests:

            mock_response = Mock()
            mock_response.status_code = 200
            mock_requests.return_value = mock_response

            result = org_cert_setup.cert_setup(str(cert_file))

            # Verify DOI cert was extracted
            assert cert_file.exists()

            # Verify environment variables were set
            assert os.environ.get("SSL_CERT_FILE") == result
            assert os.environ.get("REQUESTS_CA_BUNDLE") == result

    def test_cert_setup_handles_missing_doi_cert(self, tmp_path, capsys):
        """Test that cert_setup handles case where DOI cert is not found."""
        cert_file = tmp_path / "DOIRootCA2.pem"
        certifi_bundle = tmp_path / "cacert.pem"
        certifi_bundle.write_bytes(b"certifi bundle")

        # Create mock certificates without DOI cert
        mock_certs = [b"some_other_cert"]

        with patch("pymdwizard.core.org_cert_setup.retrieve_certs_ssl", return_value=mock_certs), \
             patch("pymdwizard.core.org_cert_setup.certifi.where", return_value=str(certifi_bundle)), \
             patch("pymdwizard.core.org_cert_setup.requests.get") as mock_requests:

            mock_response = Mock()
            mock_response.status_code = 200
            mock_requests.return_value = mock_response

            result = org_cert_setup.cert_setup(str(cert_file))

            # Should still return certifi bundle path
            assert result == str(certifi_bundle)

            # Should print warning message
            captured = capsys.readouterr()
            assert "Did not locate USGS organization certificate" in captured.out

    def test_cert_setup_handles_ssl_failure(self, tmp_path):
        """Test that cert_setup handles SSL verification failure."""
        cert_file = tmp_path / "DOIRootCA2.pem"
        certifi_bundle = tmp_path / "cacert.pem"
        certifi_bundle.write_bytes(b"certifi bundle")

        with patch("pymdwizard.core.org_cert_setup.retrieve_certs_ssl", return_value=None), \
             patch("pymdwizard.core.org_cert_setup.certifi.where", return_value=str(certifi_bundle)), \
             patch("pymdwizard.core.org_cert_setup.requests.get") as mock_requests:

            mock_response = Mock()
            mock_response.status_code = 403  # Not 200
            mock_requests.return_value = mock_response

            # Should raise ValueError on SSL verification failure
            with pytest.raises(ValueError):
                org_cert_setup.cert_setup(str(cert_file))

    def test_cert_setup_sets_environment_variables(self, tmp_path):
        """Test that cert_setup properly sets all environment variables."""
        cert_file = tmp_path / "DOIRootCA2.pem"
        cert_file.write_bytes(b"test cert")
        certifi_bundle = tmp_path / "cacert.pem"
        certifi_bundle.write_bytes(b"certifi bundle")

        with patch("pymdwizard.core.org_cert_setup.certifi.where", return_value=str(certifi_bundle)), \
             patch("pymdwizard.core.org_cert_setup.requests.get") as mock_requests:

            mock_response = Mock()
            mock_response.status_code = 200
            mock_requests.return_value = mock_response

            result = org_cert_setup.cert_setup(str(cert_file))

            # Verify all expected environment variables are set
            expected_vars = [
                "PIP_CERT",
                "SSL_CERT_FILE",
                "GIT_SSL_CAINFO",
                "REQUESTS_CA_BUNDLE",
                "CURL_CA_BUNDLE"
            ]

            for var in expected_vars:
                assert os.environ.get(var) == result


class TestIntegration:
    """Integration tests for certificate handling."""

    def test_retrieve_certs_returns_valid_format(self):
        """Test that retrieve_certs_ssl returns properly formatted certificates."""
        result = org_cert_setup.retrieve_certs_ssl()

        # May return None on some systems, but if it returns data, validate it
        if result is not None:
            assert isinstance(result, list)
            assert all(isinstance(cert, bytes) for cert in result)
            # DER-encoded certs should be binary data
            assert all(len(cert) > 0 for cert in result)

    def test_cert_setup_creates_valid_pem_file(self, tmp_path):
        """Test that cert_setup creates a valid PEM file structure."""
        cert_file = tmp_path / "test_cert.pem"
        certifi_bundle = tmp_path / "cacert.pem"
        certifi_bundle.write_bytes(
            b"-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----\n"
        )

        with patch("pymdwizard.core.org_cert_setup.retrieve_certs_ssl", return_value=None), \
             patch("pymdwizard.core.org_cert_setup.certifi.where", return_value=str(certifi_bundle)), \
             patch("pymdwizard.core.org_cert_setup.requests.get") as mock_requests:

            mock_response = Mock()
            mock_response.status_code = 200
            mock_requests.return_value = mock_response

            result = org_cert_setup.cert_setup(str(cert_file))

            # Verify result is a valid file path
            assert os.path.exists(result)

            # Verify file contains PEM certificate markers
            with open(result, "rb") as f:
                content = f.read()
            assert b"-----BEGIN CERTIFICATE-----" in content
            assert b"-----END CERTIFICATE-----" in content
