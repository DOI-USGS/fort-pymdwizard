from __future__ import print_function

import sys

sys.path.append(r"../..")

import sys
from lxml import etree

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.gui import useconst


def test_useconstraints_from_xml(qtbot):
    widget = useconst.Useconst()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    use_const = test_record.xpath("idinfo/useconst")[0]

    widget.from_xml(use_const)
    assert widget.findChild(QPlainTextEdit, "fgdc_useconst").toPlainText() == "none"


def test_useconstraints_to_xml(qtbot):
    widget = useconst.Useconst()
    qtbot.addWidget(widget)

    expected_text = "These data are marked with a Creative Commons Zero v1.0 Universal (CC0-1.0) public domain dedication and do not have any use constraints. Users are advised to read the dataset's metadata thoroughly to understand appropriate use and data limitations."

    assert (
        widget.findChild(QPlainTextEdit, "fgdc_useconst").toPlainText()
        == expected_text
    )

    uc = widget.to_xml()
    assert (
        etree.tostring(uc, pretty_print=True).decode()
        == f"<useconst>{expected_text}</useconst>\n"
    )
