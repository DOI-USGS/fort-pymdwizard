from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QLineEdit, QComboBox, QTabWidget, QStackedWidget
from PyQt5.QtCore import QDate

from pymdwizard.gui import MetadataDate

# def test_metadatadate__from_xml(qtbot):
#     widget = MetadataDate.MetadataDate()
#     qtbot.addWidget(widget)
#
#     test_record_fname = "C:/Users/mhannon/dev_mdwizard/pymdwizard/tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
#     test_record = etree.parse(test_record_fname)
#     metadatadate = test_record.xpath("idinfo/timeperd")[0]
#
#     widget._from_xml(metadatadate)
#     assert widget.findChild(QDateEdit, "dateEdit_2").date() == '1981'
#     assert widget.findChild(QDateEdit, "dateEdit_3").date() == '2013'

def test_metadata_date__to_xml(qtbot):
    widget = MetadataDate.MetadataDate()
    qtbot.addWidget(widget)

    widget._to_xml
    widget.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(1)
    #begdateQ = QDate.fromString("20131219", 'yyyyMMdd')
    #enddateQ = QDate.fromString("20140904", 'yyyyMMdd')
    widget.findChild(QLineEdit, "dateEdit_2").setText("20131219")
    widget.findChild(QLineEdit, "dateEdit_3").setText("20140904")
    #widget.findChild(QComboBox, 'fgdc_current').setCurrentText("up to date")

    mdDate = widget._to_xml()

    assert etree.tostring(mdDate, pretty_print=True).decode()\
    == """<timeperd>
  <timeinfo>
    <rngdates>
      <begdate>20131219</begdate>
      <enddate>20140904</enddate>
    </rngdates>
  </timeinfo>
  <current></current>
</timeperd>
"""