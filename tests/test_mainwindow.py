from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys

from PyQt5 import QtCore

import pytest
from pytestqt import qtbot
from PyQt5.QtWidgets import QMessageBox
from lxml import etree
try:
    from unittest.mock import Mock
    from unittest import mock
except ImportError:
    from mock import Mock # Python 2

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox

from pymdwizard.gui import MainWindow


def test_mainwindow_from_xml(qtbot, mock):

    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    mock.patch.object(QMessageBox, 'question',
                      return_value=QMessageBox.No)
    widget.open_file(test_record_fname)

    assert widget.metadata_root.findChild(QPlainTextEdit, "fgdc_logic").toPlainText() == 'No formal logical accuracy tests were conducted. testing'


def test_mainwindow_to_xml(qtbot):
    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    widget.metadata_root.findChild(QPlainTextEdit, "fgdc_logic").setPlainText("this is a test")

    dc = widget.metadata_root.to_xml()

    assert dc.xpath('dataqual/logic')[0].text == 'this is a test'

def test_validation(qtbot, mock):

    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/USGS_ASC_PolarBears_FGDC.xml"
    mock.patch.object(QMessageBox, 'question',
                      return_value=QMessageBox.No)
    mock.patch.object(QMessageBox, 'warning',
                      return_value=QMessageBox.Cancel)
    mock.patch.object(QMessageBox, 'information',
                      return_value=QMessageBox.Cancel)
    widget.open_file(test_record_fname)
    widget.validate()
    assert len(widget.error_list.errors) == 1
