"""Unittests for core.data_io"""


import pytest

from lxml import etree

from pymdwizard.core import utils


def test_url_validator():
    bad_urls = ["not a url", r"c:\temp\test.xml"]
    good_urls = ["https://www.sciencebase.gov/catalog/", "https://github.com/"]

    for url in bad_urls:
        assert utils.url_validator(url) is False

    for url in good_urls:
        assert utils.url_validator(url) is True


def test_get_usgs_contact_info():

    fgdc_cntinfo = utils.get_usgs_contact_info('talbertc')
    if not 'fgdc_error' in fgdc_cntinfo:
        assert 'fgdc_cntperp' in utils.get_usgs_contact_info('talbertc')

        bad = utils.get_usgs_contact_info('bad')
        assert bad['fgdc_cntperp']['fgdc_cntper'].strip() == ''

        cnt_info = utils.get_usgs_contact_info('talbertc', as_dictionary=False)
        assert cnt_info.getchildren()[0].getchildren()[0].text == 'Colin Talbert'
