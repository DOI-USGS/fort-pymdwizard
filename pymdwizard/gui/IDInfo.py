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
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, Qt

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_IdInfo
from pymdwizard.gui.PointOfContact import ContactInfoPointOfContact
from pymdwizard.gui.Taxonomy import Taxonomy
from pymdwizard.gui.Keywords import Keywords
from pymdwizard.gui.AccessConstraints import AccessConstraints
from pymdwizard.gui.UseConstraints import UseConstraints
from pymdwizard.gui.Status import Status


class IdInfo(WizardWidget):

    drag_label = "Identification Information <idinfo>"

    # This dictionary provides a mechanism for crosswalking between
    # gui elements (pyqt widgets) and the xml document
    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
                        'cntorg': 'cntinfo/cntperp/cntorg',
                        'cntpos': 'cntinfo/cntpos',}

    ui_class = UI_IdInfo.Ui_fgdc_idinfo

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.ptcontac = ContactInfoPointOfContact(parent=self)
        self.taxonomy = Taxonomy(parent=self)
        self.keywords = Keywords(parent=self)
        self.access = AccessConstraints(parent=self)
        self.use = UseConstraints(parent=self)
        self.status = Status(parent=self)

        self.ui.two_column_left.layout().addWidget(self.ptcontac, 0)
        self.ui.two_column_right.layout().addWidget(self.keywords, 1)
        self.ui.two_column_left.layout().addWidget(self.taxonomy)
        self.ui.two_column_left.layout().addWidget(self.access)
        self.ui.two_column_left.layout().addWidget(self.use)
        self.ui.two_column_left.layout().addWidget(self.status)



    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        print("idinfo drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'idinfo':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        # add code here to translate the form into xml representation
        idinfo_node = etree.Element('idinfo')

        citation_node = etree.Element('citation')
        idinfo_node.append(citation_node)

        descript_node = etree.Element('descript')
        idinfo_node.append(descript_node)

        timeperd_node = etree.Element('timeperd')
        idinfo_node.append(timeperd_node)

        status_node = etree.Element('status')
        idinfo_node.append(status_node)

        keywords = self.keywords._to_xml()
        idinfo_node.append(keywords)

        accconst_node = etree.Element('accconst')
        idinfo_node.append(accconst_node)

        useconst_node = etree.Element('useconst')
        idinfo_node.append(useconst_node)

        ptcontac = self.ptcontac._to_xml()
        idinfo_node.append(ptcontac)



        if self.taxonomy.ui.rbtn_yes.isChecked():
            taxonomy = self.taxonomy._to_xml()
            idinfo_node.append(taxonomy)



        return idinfo_node

    def _from_xml(self, xml_idinfo):
        try:
            ptcontac = xml_idinfo.xpath('ptcontac')[0]
            self.ptcontac._from_xml(ptcontac)
        except IndexError:
            pass

        try:
            keywords = xml_idinfo.xpath('keywords')[0]
            self.keywords._from_xml(keywords)
        except IndexError:
            pass


if __name__ == "__main__":
    utils.launch_widget(IdInfo, "IdInfo testing")