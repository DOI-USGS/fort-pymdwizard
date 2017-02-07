from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit

from pymdwizard.gui import Citation

# def test_citation__from_xml(qtbot):
#     widget = Citation.Citation()
#     qtbot.addWidget(widget)
#
#     test_record_fname = "tests/data/USGS_ASC_PolarBears_FGDC.xml"
#     test_record = etree.parse(test_record_fname)
#     citation = test_record.xpath("idinfo/citation/citeinfo")[0]
#
#     widget._from_xml(citation)
#     #assert widget.findChild(QComboBox, 'fgdc_geoform').currentText() == 'Tabular Digital Data'
#     assert widget.findChild(QLineEdit, 'fgdc_pubdate').text() == '20101231'


def test_citation__to_xml(qtbot):
    widget = Citation.Citation()
    qtbot.addWidget(widget)


    widget._to_xml#(status)
    #assert type(progress) == 'lxml.etree._Element'
    widget.findChild(QComboBox, 'fgdc_geoform').setCurrentText('Book')# == 'Complete'
    widget.findChild(QLineEdit, 'fgdc_pubdate').setText('20001013')# == 'Continually'

    cit = widget._to_xml()

    assert etree.tostring(cit, pretty_print=True).decode() \
    == """<citation>
  <citeinfo>
    <origin></origin>
    <pubdate>20001013</pubdate>
    <title></title>
    <edition></edition>
    <geoform>Book</geoform>
    <onlink></onlink>
  </citeinfo>
</citation>
"""