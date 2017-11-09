#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Metadata Date <timeperd> section
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
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QStackedWidget, QTabWidget, QDateEdit, QListWidget
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QGridLayout, QScrollArea
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QDate

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.ui_files import UI_keywords_repeater

class KeywordsRepeater(WizardWidget):  #

    drag_label = "NA <NA>"

    def __init__(self, thesaurus_label='Thesaurus', keywords_label='Keywords:',
                 line_name='kw', parent=None):
        self.thesaurus_label = thesaurus_label
        self.keywords_label = keywords_label
        self.line_name = line_name

        WizardWidget.__init__(self, parent=parent)

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_keywords_repeater.Ui_Form()

        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.ui.thesaurus_label = self.thesaurus_label

        widget_kwargs = {'label':self.keywords_label,
                         'line_name':self.line_name,
                         'required':True}

        self.keywords = RepeatingElement(add_text='Add keyword',
                                            remove_text='Remove last',
                                            widget_kwargs=widget_kwargs,
                                            )
        self.keywords.ui.italic_label.setStyleSheet('')

        self.keywords.add_another()

        self.ui.keywords_layout.insertWidget(0, self.keywords)

    def lock(self):
        self.ui.fgdc_themekt.setReadOnly(True)
        self.keywords.ui.addAnother.setEnabled(False)

    def get_keywords(self):
        return [kw.added_line.text() for kw in self.keywords.get_widgets()]

    def add_another(self, locked=False):
        widget = self.keywords.add_another()
        widget.setObjectName(self.line_name)
        widget.added_line.setReadOnly(locked)
        return widget

    def get_widgets(self):
        return self.keywords.get_widgets()



if __name__ == "__main__":
    utils.launch_widget(KeywordsRepeater,
                        " testing")
