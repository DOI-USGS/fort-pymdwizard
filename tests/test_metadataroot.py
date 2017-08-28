from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox

from pymdwizard.gui import MetadataRoot

def test_datacredit__from_xml(qtbot):
    widget = MetadataRoot.MetadataRoot()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    test_record = etree.parse(test_record_fname)

    widget._from_xml(test_record)
    assert widget.findChild(QPlainTextEdit, "fgdc_logic").toPlainText() == 'No formal logical accuracy tests were conducted. testing'

def test_datacredit__to_xml(qtbot):
    widget = MetadataRoot.MetadataRoot()
    qtbot.addWidget(widget)

    #test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    #test_record = etree.parse(test_record_fname)
    #use_const = test_record.xpath("idinfo/useconst")[0]

    widget._to_xml#(use_const)
    widget.findChild(QPlainTextEdit, "fgdc_logic").setPlainText("this is a test")

    dc = widget._to_xml()

    assert dc.xpath('dataqual/logic')[0].text == 'this is a test'