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
import os

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton, QInputDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QStackedWidget, QTabWidget, QDateEdit, QListWidget
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QGridLayout, QScrollArea, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QDate, QSettings

from pymdwizard.core import utils
from pymdwizard.core import spatial_utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spatial_tab
from pymdwizard.gui import spref
from pymdwizard.gui import spdoinfo
from pymdwizard.gui import spdom


class SpatialTab(WizardWidget):

    drag_label = "Spatial org and Spatial Ref <...>"

    ui_class = UI_spatial_tab.Ui_spatial_tab

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.schema = 'bdp'
        self.root_widget = root_widget

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.spdom = spdom.Spdom()
        self.ui.spatial_main_widget.layout().insertWidget(0, self.spdom)

        self.spref = spref.SpRef()
        self.ui.two_column_left.layout().insertWidget(0, self.spref)

        self.spdoinfo = spdoinfo.SpdoInfo()
        self.ui.two_column_right.layout().insertWidget(0, self.spdoinfo)

        self.ui.btn_browse.clicked.connect(self.browse)

    def browse(self):
        settings = QSettings('USGS', 'pymdwizard')
        last_data_fname = settings.value('lastDataFname', '')
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(self, fname, dname)
        if fname[0]:
            settings.setValue('lastDataFname', fname[0])
            self.populate_from_fname(fname[0])

    def populate_from_fname(self, fname):

        layer = spatial_utils.get_layer(fname)
        params = spatial_utils.get_params(layer)
        geo = spatial_utils.geographic(params)
        self.spref._from_xml(geo)

        spdom = spatial_utils.get_bounding(fname)
        self.spdom._from_xml(spdom)

        spdoinfo = spatial_utils.get_spdoinfo(fname)
        self.spdoinfo._from_xml(spdoinfo)




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
        self.spdom.switch_schema(schema)

    def _to_xml(self):
        pass

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

        try:
            citation = xml_idinfo.xpath('citation')[0]
            self.citation._from_xml(citation)
        except IndexError:
            pass

        try:
            timeperd = xml_idinfo.xpath('timeperd')[0]
            self.timeperd._from_xml(timeperd)
        except IndexError:
            pass

        try:
            descript = xml_idinfo.xpath('descript')[0]
            self.descript._from_xml(descript)
        except IndexError:
            pass

if __name__ == "__main__":
    utils.launch_widget(SpatialTab, "IdInfo testing")