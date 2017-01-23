# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QPlainTextEdit

from pymdwizard.gui import Descriptor

def test_descriptor__from_xml(qtbot):
    widget = Descriptor.Descriptor()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    test_record = etree.parse(test_record_fname)
    descript = test_record.xpath("idinfo/descript")[0]

    widget._from_xml(descript)
    assert widget.findChild(QPlainTextEdit, "fgdc_abstract").toPlainText() == 'Abstract MH'
    assert widget.findChild(QPlainTextEdit, "fgdc_purpose").toPlainText() ==  'Purpose MH'
    assert widget.findChild(QPlainTextEdit, "fgdc_supplinf").toPlainText() == 'Supplemental Information MH'

def test_descriptor__to_xml(qtbot):
    widget = Descriptor.Descriptor()
    qtbot.addWidget(widget)

    #test_record_fname = "C:/Users/mhannon/dev_mdwizard/pymdwizard/tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    #test_record = etree.parse(test_record_fname)
    #use_const = test_record.xpath("idinfo/useconst")[0]

    widget._to_xml#(use_const)
    assert widget.findChild(QPlainTextEdit, "fgdc_abstract").toPlainText() == ""
    assert widget.findChild(QPlainTextEdit, "fgdc_purpose").toPlainText() == ""
    assert widget.findChild(QPlainTextEdit, "fgdc_supplinf").toPlainText() == ""