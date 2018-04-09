"""Unittests for core.data_io"""


import pytest

from lxml import etree

from pymdwizard.core import xml_utils

xml_str = """<cntinfo>
  <cntperp>
    <cntper>Colin Talbert</cntper>
    <cntorg>U.S. Geological Survey, Southwest Region</cntorg>
  </cntperp>
  <cntpos>Ecologist</cntpos>
  <cntaddr>
    <addrtype>Mailing</addrtype>
    <address>2150 Centre Avenue Bldg C</address>
    <city>Fort Collins</city>
    <state>CO</state>
    <postal>80526</postal>
  </cntaddr>
</cntinfo>
"""

parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
element = etree.fromstring(xml_str, parser=parser)


def test_node_to_dict():
    result = xml_utils.node_to_dict(element)
    assert result['fgdc_cntperp']['fgdc_cntper'] == 'Colin Talbert'


def test_url_read():
    url = "https://www2.usgs.gov/datamanagement/documents/USGS_ASC_PolarBears_FGDC.xml"
    md = xml_utils.XMLRecord(url)
    assert md.metadata.idinfo.citation.citeinfo.geoform.text == 'Tabular Digital Data'


def test_open_save():
    fname = "tests/data/USGS_ASC_PolarBears_FGDC.xml"
    md = xml_utils.XMLRecord(fname)
    assert md.metadata.idinfo.citation.citeinfo.geoform.text == 'Tabular Digital Data'
    md.metadata.idinfo.citation.citeinfo.geoform.text = 'testing'
    md.save()
    md = xml_utils.XMLRecord(fname)
    new_geoform = md.metadata.idinfo.citation.citeinfo.geoform.text
    md.metadata.idinfo.citation.citeinfo.geoform.text = 'Tabular Digital Data'
    md.save()

    assert new_geoform == 'testing'





