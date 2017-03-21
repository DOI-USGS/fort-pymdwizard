#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Contact Info <cntinfo> widget


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
import tempfile

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QUrl
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebKitWidgets import QWebView

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core.xml_utils import xml_node

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spdom

class Spdom(WizardWidget):
    xpath_root = "spdom"
    drag_label = "Spatial Domain <spdom>"

    ui_class = UI_spdom.Ui_Form

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.schema = 'bdp'
        self.root_widget = root_widget

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)


        self.ui.map_viewer.hide()

        view = self.view = QWebView()
        view.page().mainFrame().addToJavaScriptWindowObject("Spdom", self)
        map_fname = utils.get_resource_path('leaflet/map.html')
        view.setUrl(QUrl.fromLocalFile(map_fname))
        self.ui.verticalLayout_3.addWidget(view)

        # this is where more complex build information would go such as
        # instantiating child widgets, inserting them into the layout,
        # tweaking the layout or individual widget properties, etc.
        # If you are using this base class as intended this should not
        # include extensive widget building from scratch.

        # setup drag-drop functionality for this widget and all it's children.
        self.setup_dragdrop(self)

        self.in_update = False
        self.raise_()

    def draw_js_map(self):
        js_fname = utils.get_resource_path('leaflet/map.js')
        with open(js_fname, 'r') as f:
            js_str = f.read()
        js_str = js_str.replace('east_var', str(self.east))
        js_str = js_str.replace('west_var', str(self.west))
        js_str = js_str.replace('north_var', str(self.north))
        js_str = js_str.replace('south_var', str(self.south))

        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript(js_str)


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """

        self.ui.fgdc_eastbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_westbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_northbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_southbc.editingFinished.connect(self.coord_updated)

    def coord_updated(self):
        self.update_rect()
        self.in_update = True
        self.update_markers()
        self.in_update = False

    def update_coords(self):
        try:
            self.east = float(self.ui.fgdc_eastbc.text())
        except ValueError:
            self.east = None

        try:
            self.west = float(self.ui.fgdc_westbc.text())
        except ValueError:
            self.west = None

        try:
            self.north = float(self.ui.fgdc_northbc.text())
        except ValueError:
            self.north = None

        try:
            self.south = float(self.ui.fgdc_southbc.text())
        except ValueError:
            self.south = None

        if self.west is not None and \
           self.east is not None and \
           self.south is not None and \
           self.north is not None:
                self.width = (self.west + self.east)
                self.center_long =  self.width / 2.0
                self.center_lat = (self.north + self.south) / 2.0
                self.valid = True
        else:
            self.width = None
            self.valid = False

        self.zoom = 3
        if self.width is not None:
            if self.width < 20:
                self.zoom = 5



    def draw_map(self):
        self.update_coords()
        if self.valid:
            self.draw_js_map()

    def update_rect(self):
        try:
            if not self.in_update:
                self.update_coords()
                jstr = "rect.setBounds(L.latLngBounds(L.latLng({s}, {w}), L.latLng({n}, {e})));".format(e=self.east, w=self.west, n=self.north, s=self.south)
                frame = self.view.page().mainFrame()
                frame.evaluateJavaScript(jstr)
        except:
            # no matter what this error is not critical
            pass

    def update_markers(self):
        try:
            self.update_coords()
            h_center = (self.east + self.west) / 2.0
            v_center = (self.north + self.south) / 2.0

            frame = self.view.page().mainFrame()
            jstr = "s_marker.setLatLng(new L.latLng({s}, {h}));".format(s=self.south, h=h_center)
            frame.evaluateJavaScript(jstr)
            jstr = "e_marker.setLatLng(new L.latLng({v}, {e}));".format(e=self.east, v=v_center)
            frame.evaluateJavaScript(jstr)

            jstr = "n_marker.setLatLng(new L.latLng({n}, {h}));".format(n=self.north, h=h_center)
            frame.evaluateJavaScript(jstr)
            jstr = "w_marker.setLatLng(new L.latLng({v}, {w}));".format(w=self.west, v=v_center)
            frame.evaluateJavaScript(jstr)
        except:
            # no matter what this error is not critical
            pass

    @pyqtSlot(float, float)
    def on_e_move(self, lat, lng):
        self.ui.fgdc_eastbc.setText(str(lng))
        self.update_rect()

    @pyqtSlot(float, float)
    def on_w_move(self, lat, lng):
        self.ui.fgdc_westbc.setText(str(lng))
        self.update_rect()

    @pyqtSlot(float, float)
    def on_n_move(self, lat, lng):
        self.ui.fgdc_northbc.setText(str(lat))
        self.update_rect()

    @pyqtSlot(float, float)
    def on_s_move(self, lat, lng):
        self.ui.fgdc_southbc.setText(str(lat))
        self.update_rect()

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
            if element.tag == 'spdom':
                e.accept()
        else:
            e.ignore()

    def switch_schema(self, schema):
        self.schema = schema
        if schema == 'bdp':
            self.ui.fgdc_descgeog.show()
            self.ui.descgeog_label.show()
            self.ui.descgeog_star.show()
        else:
            self.ui.fgdc_descgeog.hide()
            self.ui.descgeog_label.hide()
            self.ui.descgeog_star.hide()

    def _to_xml(self):
        spdom = xml_node('spdom')

        if self.schema == 'bdp':
            descgeog = xml_node('descgeog', text=self.ui.fgdc_descgeog.text(), parent_node=spdom)

        bounding = xml_node('bounding', parent_node=spdom)
        westbc = xml_node('westbc', text=self.ui.fgdc_westbc.text(), parent_node=bounding)
        eastbc = xml_node('eastbc', text=self.ui.fgdc_eastbc.text(), parent_node=bounding)
        northbc = xml_node('northbc', text=self.ui.fgdc_northbc.text(), parent_node=bounding)
        southbc = xml_node('southbc', text=self.ui.fgdc_southbc.text(), parent_node=bounding)
        return spdom

    def _from_xml(self, spdom):
        utils.populate_widget(self, spdom)
        self.draw_map()
        self.update_rect()
        self.update_markers()

        jstr = "map.fitBounds(L.latLngBounds(L.latLng({s}, {w}), L.latLng({n}, {e})));".format(e=self.east, w=self.west, n=self.north, s=self.south)
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript(jstr)


if __name__ == "__main__":
    utils.launch_widget(Spdom)
