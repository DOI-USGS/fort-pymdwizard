#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Status <status> section
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

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QAction, QListWidgetItem
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QUrl

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.ui_files import UI_error_list

class ErrorList(QWidget):

    def __init__(self, main_form, parent=None):
        QWidget.__init__(self, parent=parent)
        self.ui = UI_error_list.Ui_error_list() # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.main_form = main_form
        self.errors = []
        self.ui.listWidget.itemClicked.connect(self.main_form.goto_error)

    def add_error(self, error_msg, xpath):
        action = QListWidgetItem()
        action.setText(error_msg)
        action.setHidden(False)
        action.setData(1, xpath)

        self.ui.listWidget.addItem(action)

    def clear_errors(self):
        self.ui.listWidget.clear()

if __name__ == "__main__":
    utils.launch_widget(Preview,
                        "Preview", url=r"c:/temp/text.html")