#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Data Quality <dataqual> section


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
from pymdwizard.gui.ui_files import UI_DataQuality
from pymdwizard.gui.AttributeAccuracy import AttributeAccuracy
from pymdwizard.gui.LogicalAccuracy import LogicalAccuracy
from pymdwizard.gui.Completeness import Completeness
from pymdwizard.gui.PositionalAccuracy import PositionalAccuracy
from pymdwizard.gui.sourceinput import SourceInput
from pymdwizard.gui.procstep import ProcStep



class DataQuality(WizardWidget):

    drag_label = "Data Quality <dataqual>"


    ui_class = UI_DataQuality.Ui_fgdc_dataqual

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.attraccr = AttributeAccuracy(parent=self)
        self.logic = LogicalAccuracy(parent=self)
        self.complete = Completeness(parent=self)
        self.posacc = PositionalAccuracy(parent=self)
        self.sourceinput = SourceInput(parent=self)
        self.procstep = ProcStep(parent=self)


        self.ui.two_column_left.layout().addWidget(self.attraccr)
        self.ui.two_column_left.layout().addWidget(self.logic)
        self.ui.two_column_left.layout().addWidget(self.complete)
        self.ui.two_column_left.layout().addWidget(self.posacc)

        self.ui.bottom_layout.layout().addWidget(self.sourceinput)
        self.ui.two_column_right.layout().addWidget(self.procstep)


    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        print("dataqual drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'dataqual':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        # add code here to translate the form into xml representation
        dataqual_node = etree.Element('dataqual')

        attraccr_node = self.attraccr._to_xml()
        dataqual_node.append(attraccr_node)

        logic_node = self.logic._to_xml()
        dataqual_node.append(logic_node)

        complete_node = self.complete._to_xml()
        dataqual_node.append(complete_node)

        posacc_node = self.posacc._to_xml()
        dataqual_node.append(posacc_node)

        srcinfo_node = self.sourceinput._to_xml()

        procstep_node = self.procstep._to_xml()
        procstep_children = procstep_node.getchildren()
        print type(procstep_children)

        for i in procstep_children:
            srcinfo_node.append(i)
        dataqual_node.append(srcinfo_node)

        dataqual_node.append(procstep_node)

        return dataqual_node

    def _from_xml(self, xml_dataqual):
        try:
            attraccr = xml_dataqual.xpath('attraccr')[0]
            self.attraccr._from_xml(attraccr)
        except IndexError:
            pass

        try:
            logic = xml_dataqual.xpath('logic')[0]
            self.logic._from_xml(logic)
        except IndexError:
            pass

        try:
            complete = xml_dataqual.xpath('complete')[0]
            self.complete._from_xml(complete)
        except IndexError:
            pass

        try:
            posacc = xml_dataqual.xpath('posacc')[0]
            self.posacc._from_xml(posacc)
        except IndexError:
            pass

        try:
            sourceinput = xml_dataqual.xpath('lineage')[0]
            self.sourceinput._from_xml(sourceinput)
        except IndexError:
            pass

        try:
            procstep = xml_dataqual.xpath('lineage')[0]
            self.procstep._from_xml(procstep)
        except IndexError:
            pass


if __name__ == "__main__":
    utils.launch_widget(DataQuality, "DataQual testing")