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
from pymdwizard.gui.ui_files import UI_metainfo
from pymdwizard.gui.ContactInfo import ContactInfo
from pymdwizard.gui.single_date import SingleDate


class MetaInfo(WizardWidget):

    drag_label = "Metadata Information <metainfo>"

    ui_class = UI_metainfo.Ui_fgdc_metainfo

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.root_widget = root_widget

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.contactinfo = ContactInfo(parent=self)
        self.fgdc_metd = SingleDate(parent=self)

        self.ui.group_metd.layout().addWidget(self.fgdc_metd)

        self.ui.fgdc_metc.layout().addWidget(self.contactinfo)

    def connect_events(self):
        self.ui.fgdc_metstdn.currentIndexChanged.connect(self.update_metstdv)
        self.ui.fgdc_metstdv.currentIndexChanged.connect(self.update_metstdn)
        self.ui.button_use_dataset.clicked.connect(self.pull_datasetcontact)

    def update_metstdn(self):
        if self.ui.fgdc_metstdv.currentText() == 'FGDC-STD-001-1998':
            self.ui.fgdc_metstdn.setCurrentIndex(0)
            self.root_widget.switch_schema('fgdc')
        elif self.ui.fgdc_metstdv.currentText() == 'FGDC-STD-001.1-1999':
            self.ui.fgdc_metstdn.setCurrentIndex(1)
            self.root_widget.switch_schema('bdp')

    def update_metstdv(self):
        if self.ui.fgdc_metstdn.currentText() == 'FGDC CSDGM':
            self.ui.fgdc_metstdv.setCurrentIndex(0)
            self.root_widget.switch_schema('fgdc')
        elif self.ui.fgdc_metstdn.currentText() == 'FGDC Biological Data Profile of the CDGSM':
            self.ui.fgdc_metstdv.setCurrentIndex(1)
            self.root_widget.switch_schema('bdp')

    def pull_datasetcontact(self):
        self.contactinfo._from_xml(self.root_widget.idinfo.ptcontac._to_xml())

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
            if element.tag == 'metainfo':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        # add code here to translate the form into xml representation
        metainfo_node = xml_utils.xml_node('metainfo')
        metd = xml_utils.xml_node('metd', text=self.fgdc_metd.get_date(),
                                  parent_node=metainfo_node)

        metc = xml_utils.xml_node('metc', parent_node=metainfo_node)
        cntinfo = self.contactinfo._to_xml()
        metc.append(cntinfo)

        metstdn = xml_utils.xml_node('metstdn',
                                     text=self.ui.fgdc_metstdn.currentText(),
                                     parent_node=metainfo_node)
        metstdv = xml_utils.xml_node('metstdv',
                                     text=self.ui.fgdc_metstdv.currentText(),
                                     parent_node=metainfo_node)

        return metainfo_node

    def _from_xml(self, xml_metainfo):

        if xml_metainfo.tag == 'metainfo':
            if xml_metainfo.xpath('metc/cntinfo'):
                self.contactinfo._from_xml(xml_metainfo.xpath('metc/cntinfo')[0])

            if xml_metainfo.xpath('metstdn'):
                standard = xml_metainfo.xpath('metstdn')[0].text
                self.ui.fgdc_metstdn.setCurrentText(standard)
                # switch wizard content to reflect the standard in this record
                if "biological" in standard.lower() \
                        or 'bdp' in standard.lower():
                    self.root_widget.switch_schema('bdp')
                else:
                    self.root_widget.switch_schema('fgdc')
                    
            if xml_metainfo.xpath('metstdv'):
                self.ui.fgdc_metstdv.setCurrentText(xml_metainfo.xpath('metstdv')[0].text)


            if xml_metainfo.xpath('metd'):
                self.fgdc_metd.set_date(xml_metainfo.xpath('metd')[0].text)

if __name__ == "__main__":
    utils.launch_widget(MetaInfo, "MetaInfo testing")