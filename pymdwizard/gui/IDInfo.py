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
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QSpacerItem
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
from pymdwizard.gui.timeperd import Timeperd
from pymdwizard.gui.Citation import Citation
from pymdwizard.gui.DataCredit import DataCredit
from pymdwizard.gui.Descriptor import Descriptor


class IdInfo(WizardWidget):

    drag_label = "Identification Information <idinfo>"

    # This dictionary provides a mechanism for crosswalking between
    # gui elements (pyqt widgets) and the xml document
    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
                        'cntorg': 'cntinfo/cntperp/cntorg',
                        'cntpos': 'cntinfo/cntpos',}

    ui_class = UI_IdInfo.Ui_fgdc_idinfo

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.schema = 'bdp'
        self.root_widget = root_widget

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.ptcontac = ContactInfoPointOfContact(parent=self)
        self.taxonomy = Taxonomy(parent=self)
        self.keywords = Keywords(parent=self)
        self.accconst = AccessConstraints(parent=self)
        self.useconst = UseConstraints(parent=self)
        self.status = Status(parent=self)
        self.timeperd = Timeperd(parent=self)
        self.citation = Citation(parent=self)
        self.datacredit = DataCredit(parent=self)
        self.descript = Descriptor(parent=self)

        self.ui.fgdc_citation.layout().addWidget(self.citation)

        self.ui.two_column_left.layout().addWidget(self.ptcontac, 0)
        self.ui.two_column_left.layout().addWidget(self.taxonomy, 1)
        self.ui.two_column_left.layout().addWidget(self.status, 2)
        self.ui.two_column_left.layout().addWidget(self.accconst, 3)
        self.ui.two_column_left.layout().addWidget(self.useconst, 4)
        self.ui.two_column_left.layout().addWidget(self.datacredit, 5)

        self.ui.two_column_right.layout().addWidget(self.keywords, 0)
        self.ui.two_column_right.layout().addWidget(self.timeperd, 1)
        self.ui.two_column_right.layout().addWidget(self.descript, 2)


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

    def switch_schema(self, schema):
        self.schema = schema
        if schema == 'bdp':
            self.taxonomy.show()
        else:
            self.taxonomy.hide()

    def _to_xml(self):
        # add code here to translate the form into xml representation
        idinfo_node = xml_utils.xml_node('idinfo')

        citation_node = xml_utils.xml_node('citation', parent_node=idinfo_node)
        citeinfo_node = self.citation._to_xml()
        citation_node.append(citeinfo_node)
        idinfo_node.append(citation_node)

        descript_node = self.descript._to_xml()
        idinfo_node.append(descript_node)

        timeperd_node = self.timeperd._to_xml()
        idinfo_node.append(timeperd_node)

        status_node = self.status._to_xml()
        idinfo_node.append(status_node)

        spdom_node = self.root_widget.spatial_tab.spdom._to_xml()
        idinfo_node.append(spdom_node)

        keywords = self.keywords._to_xml()
        idinfo_node.append(keywords)

        if self.schema == 'bdp' and self.taxonomy.ui.rbtn_yes.isChecked():
            taxonomy = self.taxonomy._to_xml()
            idinfo_node.append(taxonomy)

        accconst_node = self.accconst._to_xml()
        idinfo_node.append(accconst_node)

        useconst_node = self.useconst._to_xml()
        idinfo_node.append(useconst_node)

        ptcontac = self.ptcontac._to_xml()
        if ptcontac:
            idinfo_node.append(ptcontac)

        datacredit_node = self.datacredit._to_xml()
        if datacredit_node.text:
            idinfo_node.append(datacredit_node)

        return idinfo_node

    def _from_xml(self, xml_idinfo):

        try:
            citation = xml_idinfo.xpath('citation')[0]
            self.citation._from_xml(citation)
        except IndexError:
            pass

        try:
            descript = xml_idinfo.xpath('descript')[0]
            self.descript._from_xml(descript)
        except IndexError:
            pass

        try:
            timeperd = xml_idinfo.xpath('timeperd')[0]
            self.timeperd._from_xml(timeperd)
        except IndexError:
            pass

        try:
            status = xml_idinfo.xpath('status')[0]
            self.status._from_xml(status)
        except IndexError:
            pass

        try:
            spdom = xml_idinfo.xpath('spdom')[0]
            self.root_widget.spatial_tab.spdom._from_xml(spdom)
        except IndexError:
            pass

        try:
            keywords = xml_idinfo.xpath('keywords')[0]
            self.keywords._from_xml(keywords)
        except IndexError:
            pass

        try:
            taxonomy = xml_idinfo.xpath('taxonomy')[0]
            self.taxonomy._from_xml(taxonomy)
        except IndexError:
            pass

        try:
            accconst = xml_idinfo.xpath('accconst')[0]
            self.accconst._from_xml(accconst)
        except IndexError:
            pass

        try:
            useconst = xml_idinfo.xpath('useconst')[0]
            self.useconst._from_xml(useconst)
        except IndexError:
            pass

        try:
            ptcontac = xml_idinfo.xpath('ptcontac')[0]
            self.ptcontac._from_xml(ptcontac)
        except IndexError:
            pass






if __name__ == "__main__":
    utils.launch_widget(IdInfo, "IdInfo testing")