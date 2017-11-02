from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit

from pymdwizard.gui import datacred

def test_datacredit_from_xml(qtbot):
    widget = datacred.Datacred()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    test_record = etree.parse(test_record_fname)
    data_credit = test_record.xpath("idinfo/datacred")[0]

    widget.from_xml(data_credit)
    assert widget.findChild(QPlainTextEdit, "fgdc_datacred").toPlainText() == 'Data set Credits MH'

def test_datacredit_to_xml(qtbot):
    widget = datacred.Datacred()
    qtbot.addWidget(widget)

    widget.findChild(QPlainTextEdit, "fgdc_datacred").setPlainText("This is who should be credited.")

    dc = widget.to_xml()

    assert etree.tostring(dc, pretty_print=True).decode() \
    == """<datacred>This is who should be credited.</datacred>
"""