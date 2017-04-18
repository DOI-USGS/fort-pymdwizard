from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QLineEdit

from pymdwizard.gui import single_date

def test_single_date__check_format(qtbot):
    widget = single_date.SingleDate(label='testing', show_format=False)
    qtbot.addWidget(widget)

    widget.ui.fgdc_caldate.setText('1234')
    assert widget.get_date() == '1234'

# def test_single_date__to_xml(qtbot):
#     widget = single_date.single_date()
#     qtbot.addWidget(widget)
#
# 
#     widget._to_xml#(single_date)
#     #assert type(progress) == 'lxml.etree._Element'
#     widget.findChild(QLineEdit, 'fgdc_progress').currentText()# == 'Complete'
#     widget.findChild(QLineEdit, 'fgdc_update').currentText()# == 'Continually'
#
#     stat = widget._to_xml()
#
#     assert etree.tostring(stat, pretty_print=True).decode() \
#     == """<single_date>
#   <progress>Complete</progress>
#   <update>None planned</update>
# </single_date>
# """