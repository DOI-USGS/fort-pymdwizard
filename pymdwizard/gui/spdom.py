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

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QUrl

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core.xml_utils import xml_node

import folium

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spdom

class Spdom(WizardWidget):
    xpath_root = "spdom"
    drag_label = "Spatial Domain <spdom>"

    ui_class = UI_spdom.Ui_Form

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # this is where more complex build information would go such as
        # instantiating child widgets, inserting them into the layout,
        # tweaking the layout or individual widget properties, etc.
        # If you are using this base class as intended this should not
        # include extensive widget building from scratch.

        # setup drag-drop functionality for this widget and all it's children.
        self.setup_dragdrop(self)

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
        self.draw_map()

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
            map = folium.Map(location=[self.center_lat, self.center_long],
                                 zoom_start=self.zoom)

            folium.Marker([self.north, self.east], popup='Northeast bounding').add_to(map)
            folium.Marker([self.south, self.east], popup='Southeast bounding').add_to(map)
            folium.Marker([self.north, self.west], popup='Northwest bounding').add_to(map)
            folium.Marker([self.south, self.west], popup='Southeast bounding').add_to(map)

            folium.features.RectangleMarker(bounds=[[self.south, self.west],
                                           [self.north, self.east]],
                        color='blue',
                        fill_color='red',
                        popup='Bounding rectangle').add_to(map)

            map.fit_bounds([[self.south, self.west], [self.north, self.east]])

            fname = r"c:\temp\osm.html"
            map.save(fname)

            self.ui.map_viewer.setUrl(QUrl.fromLocalFile(fname))
        # self.ui.btn_import_contact.clicked.connect(self.find_usgs_contact)
        # self.ui.rbtn_perp.toggled.connect(self.switch_primary)

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

    def _to_xml(self):
        spdom = xml_node('spdom')

        if True: #TODO replace this with global check for BDP
            descgeog = xml_node('descgeog', text=self.ui.fgdc_descgeog, parent_node=spdom)

        bounding = xml_node('bounding', parent_node=spdom)
        westbc = xml_node('westbc', text=self.ui.fgdc_westbc.text(), parent_node=bounding)
        eastbc = xml_node('eastbc', text=self.ui.fgdc_eastbc.text(), parent_node=bounding)
        northbc = xml_node('northtbc', text=self.ui.fgdc_northbc.text(), parent_node=bounding)
        southbc = xml_node('southbc', text=self.ui.fgdc_southbc.text(), parent_node=bounding)
        return spdom

    def _from_xml(self, spdom):
        utils.populate_widget(self, spdom)
        self.draw_map()


if __name__ == "__main__":
    utils.launch_widget(Spdom)
