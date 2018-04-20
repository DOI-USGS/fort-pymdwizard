from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit

from pymdwizard.gui import citeinfo

# def test_citation_from_xml(qtbot):
#     widget = Citation.Citation()
#     qtbot.addWidget(widget)
#
#     test_record_fname = "tests/data/USGS_ASC_PolarBears_FGDC.xml"
#     test_record = etree.parse(test_record_fname)
#     citation = test_record.xpath("idinfo/citation/citeinfo")[0]
#
#     widget.from_xml(citation)
#     #assert widget.findChild(QComboBox, 'fgdc_geoform').currentText() == 'Tabular Digital Data'
#     assert widget.findChild(QLineEdit, 'fgdc_pubdate').text() == '20101231'


def test_citation_to_xml(qtbot):
    widget = citeinfo.Citeinfo()
    qtbot.addWidget(widget)

    #assert type(progress) == 'lxml.etree._Element'
    widget.ui.fgdc_title.setPlainText("test title")
    widget.ui.pubdate_widget.set_date('1234')
    widget.ui.fgdc_geoform.setCurrentText('book')

    widget.ui.radio_seriesyes.setChecked(True)
    series = widget.findChild(QLineEdit, "fgdc_sername")
    series2 = widget.findChild(QLineEdit, "fgdc_issue")
    series.setText('Name 25')
    series2.setText('Issue 45')

    cit = widget.to_xml()

    assert etree.tostring(cit, pretty_print=True).decode() \
    == """<citeinfo>
  <origin/>
  <pubdate>1234</pubdate>
  <title>test title</title>
  <geoform>book</geoform>
  <serinfo>
    <sername>Name 25</sername>
    <issue>Issue 45</issue>
  </serinfo>
</citeinfo>
"""