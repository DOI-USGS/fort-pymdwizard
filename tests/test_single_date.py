from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QLineEdit

from pymdwizard.gui import fgdc_date

def test_single_date_setgetdate(qtbot):
    widget = fgdc_date.FGDCDate()
    qtbot.addWidget(widget)

    widget.ui.fgdc_caldate.setText('1234')
    assert widget.get_date() == '1234'

    widget.set_date('4567')
    assert widget.ui.fgdc_caldate.text() == '4567'


def test_single_date_itit(qtbot):
    widget = fgdc_date.FGDCDate(label='testing', show_format=False)
    qtbot.addWidget(widget)

    assert widget.ui.label.text() == 'testing'
    assert widget.ui.widget_format.isHidden()


    widget = fgdc_date.FGDCDate(label='testing', show_format=True)
    qtbot.addWidget(widget)

    assert not widget.ui.widget_format.isHidden()


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