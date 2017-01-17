from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit

from pymdwizard.gui import AccessConstraints

def test_accessconstraints__from_xml(qtbot):
    widget = AccessConstraints.AccessConstraints()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    acc_const = test_record.xpath("idinfo/accconst")[0]

    widget._from_xml(acc_const)
    assert widget.findChild(QPlainTextEdit, "accconst").text() == 'none.'