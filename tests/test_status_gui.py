from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit

from pymdwizard.gui import Status

def test_status__from_xml(qtbot):
    widget = Status.Status()
    qtbot.addWidget(widget)

    test_record_fname = "C:/Users/mhannon/dev_mdwizard/pymdwizard/tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    status = test_record.xpath("idinfo/status")[0]

    widget._from_xml(status)
    assert widget.findChild(QPlainTextEdit, "fgdc_progress").text() == 'complete'
    assert widget.findChild(QPlainTextEdit, "fgdc_update").text() == 'none planned'