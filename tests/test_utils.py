"""Unittests for core.data_io"""




from pymdwizard.core import utils


def test_url_validator():
    bad_urls = ["not a url", r"c:\temp\test.xml"]
    good_urls = ["https://www.sciencebase.gov/catalog/", "https://github.com/"]

    for url in bad_urls:
        assert utils.url_validator(url) is False

    for url in good_urls:
        assert utils.url_validator(url) is True


def test_get_usgs_contact_info():
    # Test with a valid USGS username
    fgdc_cntinfo = utils.get_usgs_contact_info("mlangseth")

    # Check that the function returns the expected FGDC structure
    assert "fgdc_cntperp" in fgdc_cntinfo
    assert "fgdc_cntper" in fgdc_cntinfo["fgdc_cntperp"]
    assert "fgdc_cntorg" in fgdc_cntinfo["fgdc_cntperp"]

    # Verify the name is populated (People Picker returns "name" field)
    assert len(fgdc_cntinfo["fgdc_cntperp"]["fgdc_cntper"]) > 0

    # Test with an invalid username - should return empty contact person
    bad = utils.get_usgs_contact_info("invalidusernamethatdoesnotexist")
    assert bad["fgdc_cntperp"]["fgdc_cntper"].strip() == ""

    # Test as_dictionary=False (returns XML element)
    cnt_info = utils.get_usgs_contact_info("mlangseth", as_dictionary=False)
    assert cnt_info.tag == "cntinfo"
    # Check that cntperp exists and has cntper child with text
    cntper_elem = cnt_info.xpath("cntperp/cntper")[0]
    assert len(cntper_elem.text) > 0


def test_url_is_alive():

    bad_url = 'https://www.go_thisdoesnotesist_ogle.com/'
    good_url = 'https://www.google.com/'

    assert utils.url_is_alive(good_url)
    assert not utils.url_is_alive(bad_url)
