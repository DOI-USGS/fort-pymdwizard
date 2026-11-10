"""Unittests for core.utils

Network-dependent checks are marked @pytest.mark.network and skipped offline.
The offline unit tests mock the network boundary (get_from_people_picker) or
exercise pure logic (url_validator, url_is_alive SSRF guards).
"""

import pytest

from pymdwizard.core import utils


# ---------------------------------------------------------------------------
# url_validator - pure logic, no network
# ---------------------------------------------------------------------------

def test_url_validator():
    bad_urls = ["not a url", r"c:\temp\test.xml"]
    good_urls = ["https://www.sciencebase.gov/catalog/", "https://github.com/"]

    for url in bad_urls:
        assert utils.url_validator(url) is False

    for url in good_urls:
        assert utils.url_validator(url) is True


# ---------------------------------------------------------------------------
# get_usgs_contact_info - mocked People Picker (offline)
# ---------------------------------------------------------------------------

# A representative People Picker person dict (shape per get_from_people_picker).
_FAKE_PERSON = {
    "email": "talbertc@usgs.gov",
    "name": "Colin Talbert",
    "active": True,
    "affiliation": "USGS",
    "department": "Fort Collins Science Center",
    "description": "",
    "orcid": "",
    "orcid_num": "",
    "title": "Ecologist",
    "street_address": "2150 Centre Ave, Bldg C",
    "city": "Fort Collins",
    "state": "CO",
    "postal_code": "80526",
    "telephone": "970-226-9100",
}


def test_get_usgs_contact_info_mocked(mocker):
    """get_usgs_contact_info transforms a People Picker dict into an FGDC
    contact structure. Mock the network call so this runs offline."""
    mocker.patch.object(
        utils, "get_from_people_picker", return_value=dict(_FAKE_PERSON)
    )

    fgdc_cntinfo = utils.get_usgs_contact_info("talbertc@usgs.gov")

    assert "fgdc_cntperp" in fgdc_cntinfo
    assert fgdc_cntinfo["fgdc_cntperp"]["fgdc_cntper"] == "Colin Talbert"
    assert "Fort Collins Science Center" in \
        fgdc_cntinfo["fgdc_cntperp"]["fgdc_cntorg"]

    # as_dictionary=False returns the lxml element.
    cnt_info = utils.get_usgs_contact_info(
        "talbertc@usgs.gov", as_dictionary=False
    )
    assert cnt_info.tag == "cntinfo"
    assert cnt_info.xpath("cntperp/cntper")[0].text == "Colin Talbert"


def test_get_usgs_contact_info_not_found_mocked(mocker):
    """An unknown user yields an empty People Picker result; the contact
    person comes back empty/None rather than raising."""
    mocker.patch.object(utils, "get_from_people_picker", return_value={})

    result = utils.get_usgs_contact_info("invaliduser@usgs.gov")
    cntper_value = result["fgdc_cntperp"]["fgdc_cntper"]
    assert cntper_value is None or cntper_value.strip() == ""


@pytest.mark.network
def test_get_usgs_contact_info_live():
    """Integration check against the live USGS People Picker service."""
    fgdc_cntinfo = utils.get_usgs_contact_info("talbertc@usgs.gov")
    assert "fgdc_cntperp" in fgdc_cntinfo
    assert len(fgdc_cntinfo["fgdc_cntperp"]["fgdc_cntper"]) > 0


# ---------------------------------------------------------------------------
# url_is_alive - SSRF guards (offline) + live reachability (network)
# ---------------------------------------------------------------------------

def test_url_is_alive_rejects_non_http_schemes():
    """Only http/https are permitted; file:// and friends are rejected
    before any network call (SSRF hardening, CHANGES 2.2.1)."""
    assert utils.url_is_alive("file:///etc/passwd") is False
    assert utils.url_is_alive("ftp://example.com/resource") is False
    assert utils.url_is_alive("gopher://example.com/") is False


def test_url_is_alive_rejects_loopback_and_private(mocker):
    """Loopback and private/link-local hosts are rejected without opening a
    connection. urlopen is patched to fail loudly if it were ever reached."""
    sentinel = mocker.patch(
        "pymdwizard.core.utils.urllib.request.urlopen",
        side_effect=AssertionError("urlopen must not be called for blocked host"),
    )

    assert utils.url_is_alive("http://127.0.0.1/") is False
    assert utils.url_is_alive("http://localhost/") is False
    assert utils.url_is_alive("http://10.0.0.5/") is False
    assert utils.url_is_alive("http://192.168.1.1/") is False
    assert utils.url_is_alive("http://169.254.1.1/") is False  # link-local

    sentinel.assert_not_called()


def test_url_is_alive_reachable_public_host_mocked(mocker):
    """A public host that responds is reported alive. The actual open is
    mocked so the test is deterministic and offline-safe."""
    mocker.patch(
        "pymdwizard.core.utils._is_private_host", return_value=False
    )
    mocker.patch(
        "pymdwizard.core.utils.urllib.request.urlopen", return_value=object()
    )
    assert utils.url_is_alive("https://www.example.com/") is True


def test_url_is_alive_unreachable_public_host_mocked(mocker):
    """A public host whose open raises is reported not alive."""
    mocker.patch(
        "pymdwizard.core.utils._is_private_host", return_value=False
    )
    mocker.patch(
        "pymdwizard.core.utils.urllib.request.urlopen",
        side_effect=OSError("unreachable"),
    )
    assert utils.url_is_alive("https://www.example.invalid/") is False


@pytest.mark.network
def test_url_is_alive_live():
    """Integration check against a real reachable and unreachable host."""
    assert utils.url_is_alive("https://www.google.com/")
    assert not utils.url_is_alive("https://www.go_thisdoesnotesist_ogle.com/")
