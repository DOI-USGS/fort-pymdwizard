from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit

from pymdwizard.gui import UseConstraints

def test_useconstraints__from_xml(qtbot):
    widget = UseConstraints.UseConstraints()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    use_const = test_record.xpath("idinfo/useconst")[0]

    widget._from_xml(use_const)
    assert widget.findChild(QPlainTextEdit, "fgdc_useconst").toPlainText() == 'none'

def test_useconstraints__to_xml(qtbot):
    widget = UseConstraints.UseConstraints()
    qtbot.addWidget(widget)


    widget._to_xml#(use_const)
    assert widget.findChild(QPlainTextEdit, "fgdc_useconst").toPlainText() == "None.  Users are advised to read the dataset's metadata thoroughly to understand appropriate use and data limitations."

    uc = widget._to_xml()
    assert etree.tostring(uc, pretty_print=True).decode() \
    == "<useconst>None.  Users are advised to read the dataset's metadata thoroughly to understand appropriate use and data limitations.</useconst>\n"