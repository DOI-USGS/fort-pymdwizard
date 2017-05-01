from __future__ import print_function

# import sys
# sys.path.append(r"../..")

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QLineEdit, QComboBox, QTabWidget, QStackedWidget
from PyQt5.QtCore import QDate

from pymdwizard.gui import fgdc_date

# def test_metadatadate__from_xml(qtbot):
#     widget = MetadataDate.MetadataDate()
#     qtbot.addWidget(widget)
#
#     test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
#     test_record = etree.parse(test_record_fname)
#     metadatadate = test_record.xpath("idinfo/timeperd")[0]
#
#     widget._from_xml(metadatadate)
#     assert widget.findChild(QDateEdit, "dateEdit_2").date() == '1981'
#     assert widget.findChild(QDateEdit, "dateEdit_3").date() == '2013'

def test_metadata_date__to_xml(qtbot):
    widget = fgdc_date.FGDCDate()
    qtbot.addWidget(widget)

#     widget.ui.radioButton_2.setChecked(True)
#     timeWidget = widget.findChild(QStackedWidget, "fgdc_timeinfo")
#     timeWidget.setCurrentIndex(1)
#     begdate = "20131219"
#     enddate = "20140904"
#     date_edit2 = widget.range_date1.findChild(QLineEdit, "lineEdit")
#     date_edit2.setText(begdate)
#     date_edit3 = widget.range_date2.findChild(QLineEdit, "lineEdit")
#     date_edit3.setText(enddate)
#
#     mdDate = widget._to_xml()
#
#     assert etree.tostring(mdDate, pretty_print=True).decode()\
#     == """<timeperd>
#   <timeinfo>
#     <rngdates>
#       <begdate>20131219</begdate>
#       <enddate>20140904</enddate>
#     </rngdates>
#   </timeinfo>
#   <current></current>
# </timeperd>
# """