#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Identification Information <idinfo> section


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
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_idinfo
from pymdwizard.gui.PointOfContact import ContactInfoPointOfContact


class IdInfo(WizardWidget):

    drag_label = "Identification Information <idinfo>"

    # This dictionary provides a mechanism for crosswalking between
    # gui elements (pyqt widgets) and the xml document
    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
                        'cntorg': 'cntinfo/cntperp/cntorg',
                        'cntpos': 'cntinfo/cntpos',}

    ui_class = UI_idinfo.Ui_idinfo

    def build_ui(self):

        self.ui = UI_idinfo.Ui_idinfo()
        self.ui.setupUi(self)

        self.main_layout = self.ui.main_layout
        self.setup_dragdrop(self)

        self.ptcontac = ContactInfoPointOfContact(parent=self)


        section1 = QHBoxLayout()
        section1.setObjectName("ContactInfoHBox")
        section1.addWidget(self.ptcontac)
        self.main_layout.addLayout(section1)

    def _to_xml(self):
        # add code here to translate the form into xml representation
        idinfo_node = etree.Element('idinfo')

        ptcontac = self.ptcontac._to_xml()
        idinfo_node.append(ptcontac)

        return idinfo_node

    def _from_xml(self, xml_idinfo):
        idinfo_dict = xml_utils.node_to_dict(xml_idinfo)
        utils.populate_widget(self, idinfo_dict)

if __name__ == "__main__":
    utils.launch_widget(IdInfo, "IdInfo testing")