from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QComboBox

from pymdwizard.gui import Status

def test_status__from_xml(qtbot):
    widget = Status.Status()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    status = test_record.xpath("idinfo/status")[0]

    widget._from_xml(status)
    assert widget.findChild(QComboBox, 'fgdc_progress').currentText() == 'complete'
    assert widget.findChild(QComboBox, 'fgdc_update').currentText() == 'none planned'

def test_status__to_xml(qtbot):
    widget = Status.Status()
    qtbot.addWidget(widget)


    widget._to_xml#(status)
    #assert type(progress) == 'lxml.etree._Element'
    widget.findChild(QComboBox, 'fgdc_progress').currentText()# == 'Complete'
    widget.findChild(QComboBox, 'fgdc_update').currentText()# == 'Continually'

    stat = widget._to_xml()

    assert etree.tostring(stat, pretty_print=True).decode() \
    == """<status>
  <progress>Complete</progress>
  <update>None planned</update>
</status>
"""