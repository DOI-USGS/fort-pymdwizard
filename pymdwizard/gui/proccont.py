#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Point of Contact <proccont> section


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
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_proccont
from pymdwizard.gui import ContactInfo


class ProcessContact(WizardWidget):

    WIDGET_WIDTH = 500
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Process Contact <proccont>"


    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_proccont.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.cntinfo = ContactInfo.ContactInfo()
        self.ui.main_layout.addWidget(self.cntinfo)

        self.collaped_size = QSize(self.WIDGET_WIDTH,
                                          self.COLLAPSED_HEIGHT)
        self.expanded_size = QSize(self.WIDGET_WIDTH,
                                   self.EXPANDED_HEIGHT)
        self.resize(self.collaped_size)


        self.setObjectName("ptcontac")

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.rbtn_yes.toggled.connect(self.contact_used_change)

    def contact_used_change(self, b):
        if b:
            self.cntinfo.show()
        else:
            self.cntinfo.hide()

    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'proccont' or element.tag == 'cntinfo':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        if self.ui.rbtn_yes.isChecked():
            proccont = etree.Element('proccont')

            cntinfo = self.cntinfo._to_xml()
            proccont.append(cntinfo)
        else:
            self.ui.rbtn_no.setChecked(True)
            proccont = None

        return proccont

    def _from_xml(self, contact_information):

        if contact_information.tag == 'cntinfo':
            self.ui.rbtn_yes.setChecked(True)
            cntinfo_node = contact_information
        else:
            cntinfo_node = contact_information.xpath('cntinfo')[0]
        self.cntinfo._from_xml(cntinfo_node)


if __name__ == "__main__":
    utils.launch_widget(ProcessContact,
                        "ProcessContact testing")

