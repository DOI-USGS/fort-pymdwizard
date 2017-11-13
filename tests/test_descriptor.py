# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
sys.path.append(r"../..")

from lxml import etree

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.gui import Descriptor

def test_descriptor_from_xml(qtbot):
    widget = Descriptor.Descriptor()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    test_record = etree.parse(test_record_fname)
    descript = test_record.xpath("idinfo/descript")[0]

    widget.from_xml(descript)
    assert widget.findChild(QPlainTextEdit, "fgdc_abstract").toPlainText() == 'Abstract MH'
    assert widget.findChild(QPlainTextEdit, "fgdc_purpose").toPlainText() ==  'Purpose MH'
    assert widget.findChild(QPlainTextEdit, "fgdc_supplinf").toPlainText() == 'Supplemental Information MH'

def test_descriptor_to_xml(qtbot):
    widget = Descriptor.Descriptor()
    qtbot.addWidget(widget)

    widget.findChild(QPlainTextEdit, "fgdc_abstract").setPlainText("This is the description portion")
    widget.findChild(QPlainTextEdit, "fgdc_purpose").setPlainText("The purpose and appropriate use of the data is to...")
    widget.findChild(QPlainTextEdit, "fgdc_supplinf").setPlainText("Any additional supplemental info is this,")

    mdDescript = widget.to_xml()

    assert etree.tostring(mdDescript, pretty_print=True).decode() \
    == """<descript>
  <abstract>This is the description portion</abstract>
  <purpose>The purpose and appropriate use of the data is to...</purpose>
  <supplinf>Any additional supplemental info is this,</supplinf>
</descript>
"""