from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox

from pymdwizard.gui import MetadataRoot

def test_datacredit_from_xml(qtbot):
    widget = MetadataRoot.MetadataRoot()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    test_record = etree.parse(test_record_fname)

    widget.from_xml(test_record)
    assert widget.findChild(QPlainTextEdit, "fgdc_logic").toPlainText() == 'No formal logical accuracy tests were conducted. testing'

def test_datacredit_to_xml(qtbot):
    widget = MetadataRoot.MetadataRoot()
    qtbot.addWidget(widget)

    widget.findChild(QPlainTextEdit, "fgdc_logic").setPlainText("this is a test")

    dc = widget.to_xml()

    assert dc.xpath('dataqual/logic')[0].text == 'this is a test'
