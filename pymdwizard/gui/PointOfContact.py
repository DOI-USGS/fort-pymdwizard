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
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_PointOfContact
from pymdwizard.gui import ContactInfo


class ContactInfoPointOfContact(WizardWidget):

    WIDGET_WIDTH = 500
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Point of Contact <pntcontac>"

    # This dictionary provides a mechanism for crosswalking between
    # gui elements (pyqt widgets) and the xml document
    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
                    'cntorg': 'cntinfo/cntperp/cntorg',
                    'cntpos': 'cntinfo/cntpos',
                    'address': 'cntinfo/cntaddr/address',
                    'address2': 'cntinfo/cntaddr/address[2]',
                    'address3': 'cntinfo/cntaddr/address[3]',
                    'city': 'cntinfo/cntaddr/city',
                    'state': 'cntinfo/cntaddr/state',
                    'postal': 'cntinfo/cntaddr/postal',
                    'state': 'cntinfo/cntaddr/state',
                    'country': 'cntinfo/cntaddr/country',
                    'addrtype': 'cntinfo/cntaddr/addrtype',
                    'cntvoice': 'cntinfo/cntvoice',
                    'cntfax': 'cntinfo/cntfax',
                    'cntemail': 'cntinfo/cntemail'}

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_PointOfContact.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.contact_info_widget = ContactInfo.ContactInfo()
        self.ui.main_layout.addWidget(self.contact_info_widget)

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
            self.contact_info_widget.show()
        else:
            self.contact_info_widget.hide()

    def _to_xml(self):
        pntcontact = etree.Element('ptcontac')

        cntinfo = self.contact_info_widget._to_xml()
        pntcontact.append(cntinfo)

        return pntcontact

    def _from_xml(self, contact_information):

        continfo = contact_information.xpath('cntinfo')[0]
        self.contact_info_widget._from_xml(continfo)


if __name__ == "__main__":
    utils.launch_widget(ContactInfoPointOfContact,
                        "ContactInfoPointOfContact testing")

