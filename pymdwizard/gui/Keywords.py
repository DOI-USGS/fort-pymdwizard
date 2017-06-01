#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Point of Contact <pntcontac> section


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
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QSpacerItem
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_Keywords
from pymdwizard.gui.theme_list import ThemeList
from pymdwizard.gui.place_list import PlaceList


class Keywords(WizardWidget):

    drag_label = "Keywords <keywords>"
    acceptable_tags = ['keywords', 'theme']

    ui_class = UI_Keywords.Ui_keyword_widget

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.theme_list = ThemeList(parent=self)
        self.ui.fgdc_keywords.layout().addWidget(self.theme_list)

        self.place_list = PlaceList(parent=self)
        self.ui.fgdc_keywords.layout().addWidget(self.place_list)

        spacerItem = QSpacerItem(24, 10, QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.ui.fgdc_keywords.layout().addItem(spacerItem)
        self.setup_dragdrop(self)

    def _to_xml(self):
        keywords = self.theme_list._to_xml()
        place_keywords = self.place_list._to_xml()
        for child_node in place_keywords.xpath('place'):
            keywords.append(child_node)

        return keywords

    def _from_xml(self, keywords):

        self.theme_list._from_xml(keywords)
        self.place_list._from_xml(keywords)


if __name__ == "__main__":
    utils.launch_widget(Keywords,
                        "keywords testing")

