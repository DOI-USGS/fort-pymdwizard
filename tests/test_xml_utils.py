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

def test_find_replace():
    fname = "tests/data/USGS_ASC_PolarBears_FGDC.xml"
    md = xml_utils.XMLRecord(fname)
    assert len(md.metadata.find_string('asc', ignorecase=True)) == 7
    assert len(md.metadata.find_string('asc', ignorecase=False)) == 0
    assert len(md.metadata.find_string('ASC')) == 7

    assert md.metadata.replace_string('Polar Bear', "Honey Badger", deep=False) == 0
    assert md.metadata.replace_string('Polar Bear', "Honey Badger") == 4
    assert 'Honey Badger' in md.metadata.idinfo.citation.citeinfo.title.text
    assert md.metadata.idinfo.descript.abstract.replace_string('polar', 'big white') == 4
    assert md.metadata.idinfo.descript.abstract.text.count('polar') == 0

    md = xml_utils.XMLRecord(fname)
    assert md.metadata.idinfo.descript.abstract.replace_string('polar', 'big white', maxreplace=2) == 2
    assert md.metadata.idinfo.descript.abstract.text.count('polar') == 2





