from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit

from pymdwizard.gui import datacred

def test_datacredit__from_xml(qtbot):
    widget = datacred.Datacred()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    test_record = etree.parse(test_record_fname)
    data_credit = test_record.xpath("idinfo/datacred")[0]

    widget._from_xml(data_credit)
    assert widget.findChild(QPlainTextEdit, "fgdc_datacred").toPlainText() == 'Data set Credits MH'

def test_datacredit__to_xml(qtbot):
    widget = datacred.Datacred()
    qtbot.addWidget(widget)

    #test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    #test_record = etree.parse(test_record_fname)
    #use_const = test_record.xpath("idinfo/useconst")[0]

    widget._to_xml#(use_const)
    widget.findChild(QPlainTextEdit, "fgdc_datacred").setPlainText("This is who should be credited.")

    dc = widget._to_xml()

    assert etree.tostring(dc, pretty_print=True).decode() \
    == """<datacred>This is who should be credited.</datacred>
"""