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
from pymdwizard.gui.ui_files import UI_rdom


class Rdom(WizardWidget):  #

    drag_label = "Range Domain <rdom>"
    acceptable_tags = ['rdom']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_rdom.Ui_fgdc_attrdomv()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        rdom = xml_utils.xml_node('rdom')
        rdommin = xml_utils.xml_node('rdommin', text=self.ui.fgdc_rdommin.text(), parent_node=rdom)
        rdommax = xml_utils.xml_node('rdommax', text=self.ui.fgdc_rdommax.text(), parent_node=rdom)

        if self.ui.fgdc_attrunit.text():
            attrunit= xml_utils.xml_node('attrunit',
                                         text=self.ui.fgdc_attrunit.text(),
                                         parent_node=rdom)

        if self.ui.fgdc_attrmres.text():
            attrmres= xml_utils.xml_node('attrmres',
                                         text=self.ui.fgdc_attrmres.text(),
                                         parent_node=rdom)

        return rdom

    def _from_xml(self, rdom):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if rdom.tag == 'rdom':
                utils.populate_widget(self, rdom)
            else:
                print ("The tag is not rdom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Rdom,
                        "udom testing")
