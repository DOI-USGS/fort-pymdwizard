"""Unittests for core.data_io"""


import pytest

from lxml import etree

import pymdwizard

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
    result = pymdwizard.core.xml_utils.node_to_dict(element)
    assert result['fgdc_cntperp']['fgdc_cntper'] == 'Colin Talbert'