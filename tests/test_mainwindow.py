from __future__ import print_function

import sys
sys.path.append(r"../..")

import os
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import pytest
from pytestqt import qtbot
from pytestqt.qt_compat import qt_api


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

    # For some reason this part of the test is causing it to hang on TravisCI
    mock.patch.object(QMessageBox, 'question',
                      return_value=QMessageBox.No)
    mock.patch.object(QMessageBox, 'information',
                      return_value=QMessageBox.Ok)
    widget.last_updated = time.time()
    widget.generate_review_doc()
    assert os.path.exists("tests/data/USGS_ASC_PolarBears_FGDC_REVIEW.docx")
    os.remove("tests/data/USGS_ASC_PolarBears_FGDC_REVIEW.docx")


def test_splash(qtbot):

    MainWindow.show_splash()
    MainWindow.show_splash('2.1.9')


def test_misc(qtbot, mock):
    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    mock.patch.object(QMessageBox, 'about', return_value=QMessageBox.Ok)
    widget.about()


def test_settings(qtbot, mock):

    settings = qt_api.QtCore.QSettings('USGS', 'pymdwizard')
    settings.setValue('template_fname', 'tests/data/USGS_ASC_PolarBears_FGDC.xml')

    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    widget.get_save_name = lambda : 'test_output.xml'

    mock.patch.object(QMessageBox, 'question',
                      return_value=QMessageBox.No)
    widget.new_record()

    md = widget.metadata_root.to_xml()
    os.remove('test_output.xml')

    assert md.xpath('idinfo/spdom/bounding/westbc')[0].text == '178.2167'
