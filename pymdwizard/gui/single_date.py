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

from pymdwizard.gui.ui_files import UI_single_date


class SingleDate(QWidget):

    def __init__(self, xml=None, parent=None, show_format=True, label=''):
        QWidget.__init__(self, parent=parent)

        self.build_ui()

        if not show_format:
            self.ui.widget_format.hide()

        if label:
            self.ui.label.setText(label)
        else:
            self.ui.label.visible = False

        self.changed = False
        self.connect_events()


    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_single_date.Ui_Form()
        self.ui.setupUi(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.lineEdit.editingFinished.connect(self.check_format)
        self.ui.lineEdit.textChanged.connect(self.changed_text)

    def changed_text(self):
        self.changed = True

    def check_format(self):
        if not self.changed:
            return None

        cur_contents = self.ui.lineEdit.text()

        msg = ""
        if len(cur_contents) not in (4, 6, 8):
            msg = "needs to be ..."
        if not cur_contents.isdigit():
            msg = "only numbers ..."

        if msg:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(msg)
            msgbox.setInformativeText("YYYY or YYYYMM or YYYYMMDD")
            msgbox.setWindowTitle("Problem with date format")
            msgbox.setStandardButtons(QMessageBox.Retry)
            msgbox.exec_()

        self.changed = False

    def get_date(self):
        return self.ui.lineEdit.text()

    def set_date(self, date_str):
        self.ui.lineEdit.setText(date_str)

if __name__ == "__main__":
    utils.launch_widget(SingleDate, label='testing', show_format=False)

