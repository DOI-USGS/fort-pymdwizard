from __future__ import print_function

import sys

sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.gui import accconst


def test_accessconstraints_from_xml(qtbot):
    widget = accconst.Accconst()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    acc_const = test_record.xpath("idinfo/accconst")[0]

    widget.from_xml(acc_const)
    assert widget.findChild(QPlainTextEdit, "fgdc_accconst").toPlainText() == "none"


def test_accessconstraints_to_xml(qtbot):
    widget = accconst.Accconst()
    qtbot.addWidget(widget)

    assert (
        widget.findChild(QPlainTextEdit, "fgdc_accconst").toPlainText()
        == "No access constraints. Please see 'Distribution Information' for details."
    )
    ac = widget.to_xml()
    assert (
        str(etree.tostring(ac, pretty_print=True).decode())
        == """<accconst>No access constraints. Please see 'Distribution Information' for details.</accconst>
"""
    )
