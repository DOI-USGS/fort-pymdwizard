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
        self.ui.fgdc_gridsysn.addItems(spatial_utils.GRIDSYS_LOOKUP.keys())


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.rbtn_yes.toggled.connect(self.spref_used_change)

        self.ui.btn_geographic.toggled.connect(self.system_def_changed)
        self.ui.btn_local.toggled.connect(self.system_def_changed)

        self.ui.btngrp_planar.buttonClicked.connect(self.planar_changed)

        self.ui.fgdc_mapprojn.currentIndexChanged.connect(self.load_projection)
        self.load_projection()

        self.ui.fgdc_horizdn.currentIndexChanged.connect(self.load_datum)
        self.load_datum()

    def spref_used_change(self, b):
        if b:
            self.ui.horiz_layout.show()
        else:
            self.ui.horiz_layout.hide()

    def has_content(self):
        return self.ui.rbtn_yes.isChecked()

    def system_def_changed(self):

        button_name = self.sender().objectName()

        is_geographic = self.ui.btn_geographic.isChecked()
        if self.ui.btn_geographic.isChecked():
            self.ui.stack_definition.setCurrentIndex(0)
        elif self.ui.btn_planar.isChecked():
            self.ui.stack_definition.setCurrentIndex(1)
        else:
            self.ui.stack_definition.setCurrentIndex(2)

    def planar_changed(self):
        if self.ui.btn_localp.isChecked():
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


        layout = self.ui.mapproj_contents.layout()
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
            label.help_text = annotation
            lineedit = QLineEdit('...')
            lineedit.setObjectName('fgdc_' + param)
            lineedit.setToolTip(annotation)
            layout.addRow(label, lineedit)

    def load_datum(self):
        datum_names = spatial_utils.DATUM_LOOKUP.keys()
        datum_name = self.ui.fgdc_horizdn.currentText()
        if datum_name in datum_names:
            datum_params = spatial_utils.DATUM_LOOKUP[datum_name]
            self.ui.fgdc_ellips.setCurrentText(datum_params['ellips'])
            self.ui.fgdc_semiaxis.setText(datum_params['semiaxis'])
            self.ui.fgdc_denflat.setText(datum_params['denflat'])

    def has_content(self):
        return self.ui.rbtn_yes.isChecked()

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
            if element is not None and element.tag == 'spref':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):

        spref_node = xml_utils.xml_node('spref')

        horizsys = xml_utils.xml_node('horizsys',   parent_node=spref_node)

        if self.ui.btn_geographic.isChecked():
            geograph = xml_utils.xml_node('geograph', parent_node=horizsys)
            latres_str = self.findChild(QLineEdit, "fgdc_latres").text()
            latres = xml_utils.xml_node('latres', latres_str, geograph)
            longres_str = self.findChild(QLineEdit, "fgdc_longres").text()
            longres = xml_utils.xml_node('longres', latres_str, geograph)
            geogunit_str = self.findChild(QComboBox, "fgdc_geogunit").currentText()
            geogunit = xml_utils.xml_node('geogunit', geogunit_str, geograph)
        elif self.ui.btn_planar.isChecked():
            planar = xml_utils.xml_node('planar', parent_node=horizsys)

            projection_name = self.ui.fgdc_mapprojn.currentText()
            projection = spatial_utils.PROJECTION_LOOKUP[projection_name]
            for param in projection['elements']:
                widget = self.findChild(QLineEdit, "fgdc_"+param)
                xml_utils.xml_node(param, text=widget.text(), parent_node=planar)

            planci = xml_utils.xml_node('planci', parent_node=planar)
            plance = xml_utils.xml_node('plance', text=self.ui.fgdc_plance.currentText(), parent_node=planci)
            coordrep = xml_utils.xml_node('coordrep', parent_node=planci)
            absres = xml_utils.xml_node('absres', text=self.ui.fgdc_absres, parent_node=coordrep)
            absres = xml_utils.xml_node('ordres', text=self.ui.fgdc_ordres, parent_node=coordrep)
            plandu = xml_utils.xml_node('plandu', text=self.ui.fgdc_plandu, parent_node=planci)
        else:
            local = xml_utils.xml_node('local', parent_node=horizsys)
            fgdc_localdes = xml_utils.xml_node('localdes', text=self.ui.fgdc_localdes, parent_node=local)
            fgdc_localgeo = xml_utils.xml_node('localgeo', text=self.ui.fgdc_localgeo, parent_node=local)

        if self.findChild(QComboBox, "fgdc_horizdn").currentText():
            geodetic = xml_utils.xml_node('geodetic', parent_node=horizsys)
            horizdn_str = self.findChild(QComboBox, "fgdc_horizdn").currentText()
            horizdn = xml_utils.xml_node('horizdn', horizdn_str, geodetic)
            ellips_str = self.findChild(QComboBox, "fgdc_ellips").currentText()
            ellips = xml_utils.xml_node('ellips', ellips_str, geodetic)
            semiaxis_str = self.findChild(QLineEdit, "fgdc_semiaxis").text()
            semiaxis = xml_utils.xml_node('semiaxis', semiaxis_str, geodetic)
            denflat_str = self.findChild(QLineEdit, "fgdc_denflat").text()
            denflat = xml_utils.xml_node('denflat', denflat_str, geodetic)

        return spref_node


    def _from_xml(self, spref_node):
        self.clear_widget()
        if spref_node.tag == 'spref':
            self.ui.rbtn_yes.setChecked(True)

            geograph = xml_utils.search_xpath(spref_node, 'horizsys/geograph')
            if geograph:
                self.ui.btn_geographic.setChecked(True)

                utils.populate_widget_element(self.ui.fgdc_latres, geograph[0], 'latres')
                utils.populate_widget_element(self.ui.fgdc_longres, geograph[0], 'longres')
                utils.populate_widget_element(self.ui.fgdc_geogunit, geograph[0], 'geogunit')

            local = xml_utils.search_xpath(spref_node, 'horizsys/local')
            if local:
                self.ui.btn_local.setChecked(True)

                utils.populate_widget_element(self.ui.fgdc_localdes, local[0], 'localdes')
                utils.populate_widget_element(self.ui.fgdc_localgeo, local[0], 'localgeo')

            planar = xml_utils.search_xpath(spref_node, 'horizsys/planar')
            if planar:
                self.ui.btn_planar.setChecked(True)

                mapproj = xml_utils.search_xpath(planar[0], 'mapproj')
                if mapproj:
                    self.ui.btn_projection.setChecked(True)

                gridsys = xml_utils.search_xpath(planar[0], 'gridsys')
                if gridsys:
                    self.ui.btn_grid.setChecked(True)

                localp = xml_utils.search_xpath(planar[0], 'localp')
                if localp:
                    self.ui.btn_localp.setChecked(True)
                    utils.populate_widget_element(self.ui.fgdc_localpd, localp[0], 'localpd')
                    utils.populate_widget_element(self.ui.fgdc_localpgi, localp[0], 'localpgi')

                self.planar_changed()

            geodetic = xml_utils.search_xpath(spref_node, 'horizsys/geodetic')
            if geodetic:
                utils.populate_widget_element(self.ui.fgdc_horizdn, geodetic[0], 'horizdn')
                utils.populate_widget_element(self.ui.fgdc_ellips, geodetic[0], 'ellips')
                utils.populate_widget_element(self.ui.fgdc_semiaxis, geodetic[0], 'semiaxis')
                utils.populate_widget_element(self.ui.fgdc_denflat, geodetic[0], 'denflat')

if __name__ == "__main__":
    utils.launch_widget(SpRef, "spref testing")