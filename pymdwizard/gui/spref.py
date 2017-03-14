#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for an FGDC spatial reference element


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
import json

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolButton
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QLabel, QComboBox
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint
from PyQt5.QtCore import Qt, QMimeData, QObject, QTimeLine

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QEvent, QCoreApplication
from PyQt5.QtGui import QMouseEvent

from lxml import etree

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import spatial_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spref


class SpRef(WizardWidget):

    drag_label = "Spatial Refernce <spref>"

    ui_class = UI_spref.Ui_Form

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)
        self.setup_dragdrop(self, enable=True)

        self.ui.fgdc_mapprojn.addItems(spatial_utils.PROJECTION_LOOKUP.keys())


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.rbtn_yes.toggled.connect(self.spref_used_change)
        self.ui.btn_geographic.toggled.connect(self.system_def_changed)
        self.ui.btngrp_planar.buttonReleased.connect(self.planar_changed)

        self.ui.fgdc_mapprojn.currentIndexChanged.connect(self.load_projection)

        # self.ui.dataquality_button.pressed.connect(self.section_changed)
        # self.ui.spatial_button.pressed.connect(self.section_changed)
        # self.ui.eainfo_button.pressed.connect(self.section_changed)
        # self.ui.distinfo_button.pressed.connect(self.section_changed)
        # self.ui.metainfo_button.pressed.connect(self.section_changed)

    def spref_used_change(self, b):
        if b:
            self.ui.horiz_layout.show()
        else:
            self.ui.horiz_layout.hide()

    def system_def_changed(self):

        button_name = self.sender().objectName()

        is_geographic = self.ui.btn_geographic.isChecked()
        if is_geographic:
            self.ui.stack_definition.setCurrentIndex(0)
        else:
            self.ui.stack_definition.setCurrentIndex(1)

    def planar_changed(self):
        if self.ui.btn_local.isChecked():
            index = 2
        elif self.ui.btn_projection.isChecked():
            index = 0
        else:
            index = 1
        self.ui.stack_planar.setCurrentIndex(index)

    def load_projection(self):

        projection_name = self.ui.fgdc_mapprojn.currentText()
        projection = spatial_utils.PROJECTION_LOOKUP[projection_name]


        annotation_lookup_fname = utils.get_resource_path('fgdc/bdp_lookup')
        try:
            with open(annotation_lookup_fname, encoding='utf-8') as data_file:
                annotation_lookup = json.loads(data_file.read())
        except TypeError:
            with open(annotation_lookup_fname) as data_file:
                annotation_lookup = json.loads(data_file.read())

        annotation_lookup['stdparl_2'] = {'long_name':'Standard Parallel',
                                      'annotation':annotation_lookup['stdparll']['annotation']}
    # widgets = self.findChildren(QObject, QRegExp(r'.*'))
    # for widget in widgets:
    #     if widget.objectName().startswith('fgdc_'):
    #         shortname = widget.objectName().replace('fgdc_', '')
    #         if shortname[-1].isdigit():
    #             shortname = shortname[:-1]
    #         widget.setToolTip(annotation_lookup[shortname]['annotation'])


        layout = self.ui.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for param in projection['elements']:
            try:
                long_name = annotation_lookup[param]['long_name']
                annotation = annotation_lookup[param]['annotation']
            except:
                long_name = param
                annotation = 'Unknown'
            label = QLabel(long_name)
            label.setToolTip(annotation)
            lineedit = QLineEdit('...')
            lineedit.setObjectName('fgdc_' + param)
            lineedit.setToolTip(annotation)
            layout.addRow(label, lineedit)

    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'spref':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):

        spref_node = xml_utils.xml_node('spref')
        return spref_node
        horizsys = xml_utils.xml_node('horizsys',   parent_node=spref_node)

        if self.ui.btn_geographic.isChecked():
            geograph = xml_utils.xml_node('geograph', parent_node=horizsys)
            latres_str = self.findChild(QLineEdit, "fgdc_latres").text()
            latres = xml_utils.xml_node('latres', latres_str, geograph)
            longres_str = self.findChild(QLineEdit, "fgdc_longres").text()
            longres = xml_utils.xml_node('longres', latres_str, geograph)
            geogunit_str = self.findChild(QComboBox, "fgdc_geogunit").currentText()
            geogunit = xml_utils.xml_node('geogunit', geogunit_str, geograph)
        else:
            planar = xml_utils.xml_node('planar', parent_node=horizsys)

        if self.findChild(QComboBox, "fgdc_horizdn").currentText():
            geodetic = xml_utils.xml_node('geodetic', parent_node=horizsys)
            horizdn_str = self.findChild(QComboBox, "fgdc_horizdn").currentText()
            horizdn = xml_utils.xml_node('horizdn', horizdn_str, geodetic)
            ellips_str = self.findChild(QComboBox, "fgdc_ellips").currentText()
            ellips = xml_utils.xml_node('ellips', ellips_str, geodetic)
            semiaxis_str = self.findChild(QLineEdit, "fgdc_semiaxis").text()
            semiaxis = xml_utils.xml_node('horizdn', semiaxis_str, geodetic)
            denflat_str = self.findChild(QLineEdit, "fgdc_denflat").text()
            denflat = xml_utils.xml_node('denflat', denflat_str, geodetic)

        return spref_node


    def _from_xml(self, metadata_element):
        pass



if __name__ == "__main__":
    utils.launch_widget(SpRef, "spref testing")