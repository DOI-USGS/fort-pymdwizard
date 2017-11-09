#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a date widget


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

import sys

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_fgdc_date


class FGDCDate(QWidget):

    def __init__(self, parent=None, show_format=True, label='',
                 required=False, fgdc_name=None, parent_fgdc_name=None):
        QWidget.__init__(self, parent=parent)

        self.build_ui()

        if not show_format:
            self.ui.widget_format.hide()

        if label:
            self.ui.label.setText(label)
        else:
            self.ui.label.visible = False

        if not required:
            self.ui.lbl_required.hide()

        self.date_widget = self.ui.fgdc_caldate
        if fgdc_name is not None:
            self.ui.fgdc_caldate.setObjectName(fgdc_name)

        if parent_fgdc_name is not None:
            self.ui.parent_fgdc.setObjectName(parent_fgdc_name)

        self.last_checked_contents = ''
        self.connect_events()

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_fgdc_date.Ui_parent_widget()
        self.ui.setupUi(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.date_widget.editingFinished.connect(self.check_format)

    def check_format(self):

        cur_contents = self.date_widget.text()
        if cur_contents == self.last_checked_contents:
            return
        else:
            self.last_checked_contents = cur_contents

        msg = ''
        if len(cur_contents) not in (0, 4, 6, 8):
            msg = "An FGDC date needs to be 4, 6, or 8 numbers long, or be 'Unknown'"
        if not cur_contents.isdigit():
            msg = "An FGDC date can only consist of numbers"

        if cur_contents == 'Unknown':
            msg = ''

        if msg:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(msg)
            msgbox.setInformativeText("YYYY or YYYYMM or YYYYMMDD or 'Unknown'")
            msgbox.setWindowTitle("Problem with FGDC date format")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def get_date(self):
        return self.date_widget.text()

    def set_date(self, date_str):
        self.date_widget.setText(date_str)

if __name__ == "__main__":
    utils.launch_widget(FGDCDate, label='testing', show_format=False, parent_fgdc_name='fgdc_sngdate')

