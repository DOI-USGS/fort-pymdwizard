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
from copy import deepcopy

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
    drag_label = "Spatial Domain <spdom>"
    acceptable_tags = ['spdom', 'bounding']
    ui_class = UI_spdom.Ui_Form

    def __init__(self, root_widget=None):

        self.east = 180
        self.west = -180
        self.north = 90
        self.south = -90
        self.valid = True

        super(self.__class__, self).__init__()
        self.schema = 'bdp'
        self.root_widget = root_widget

        self.after_load = False
        self.has_rect = True

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.view = QWebView()
        self.view.page().mainFrame().addToJavaScriptWindowObject("Spdom", self)
        map_fname = utils.get_resource_path('leaflet/map.html')


        self.view.setUrl(QUrl.fromLocalFile(map_fname))

        self.frame = self.view.page().mainFrame()
        self.ui.verticalLayout_3.addWidget(self.view)

        # this is where more complex build information would go such as
        # instantiating child widgets, inserting them into the layout,
        # tweaking the layout or individual widget properties, etc.
        # If you are using this base class as intended this should not
        # include extensive widget building from scratch.

        # setup drag-drop functionality for this widget and all it's children.
        self.setup_dragdrop(self)
        self.add_rect()
        self.raise_()

    def connect_events(self):
        self.ui.fgdc_eastbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_westbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_northbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_southbc.editingFinished.connect(self.coord_updated)

    def coord_updated(self):

        good_coords = self.all_good_coords()

        try:
            cur_name = self.sender().objectName()
            if 'fgdc' not in cur_name:
                return
            cur_value = self.sender().text()
        except AttributeError:
            cur_name = ''
            cur_value = ''

        try:
            cur_value = float(cur_value)
        except ValueError:
            pass

        msg = ''
        if type(cur_value) != float and cur_value != '':
            msg = 'number entered must be numeric only'
        elif cur_value == '':
            msg = ''
        elif cur_name in ['fgdc_westbc', 'fgdc_eastbc'] \
            and -180 >= cur_value >= 180:
            msg = 'East or West coordinate must be within -180 and 180'
        elif cur_name in ['fgdc_southbc', 'fgdc_northbc'] \
                and -90 >= cur_value >= 90:
            msg = 'North and South coordinates must be within -90 and 90'
        elif cur_name == 'fgdc_southbc':
            try:
                north = float(self.ui.fgdc_northbc.text())
                if north <= cur_value:
                    msg = 'North coordinate must be greater than South coordinate'
            except ValueError:
                pass
        elif cur_name == 'fgdc_northbc':
            try:
                south = float(self.ui.fgdc_southbc.text())
                if south >= cur_value:
                    msg = 'North coordinate must be greater than South coordinate'
            except ValueError:
                pass

        if msg:
                QMessageBox.warning(self, "Problem bounding coordinates", msg)

        if good_coords:
            self.add_rect()
        else:
            self.remove_rect()
            return

        self.update_map()

    def update_map(self):
        jstr = """east = {eastbc};
        west = {westbc};
        south = {southbc};
        north = {northbc};
        updateMap();
        fitMap();
        """.format(**{'eastbc': self.ui.fgdc_eastbc.text(),
                      'westbc': self.ui.fgdc_westbc.text(),
                      'northbc': self.ui.fgdc_northbc.text(),
                      'southbc': self.ui.fgdc_southbc.text(),
                      })
        self.frame.evaluateJavaScript(jstr)

    def add_rect(self):
        jstr = """addRect();"""
        self.frame.evaluateJavaScript(jstr)

    def remove_rect(self):
        if self.has_rect:
            self.has_rect = False
            jstr = """removeRect()"""
            self.frame.evaluateJavaScript(jstr)

    @pyqtSlot(float, float)
    def on_ne_move(self, lat, lng):
        self.ui.fgdc_eastbc.setText(str(lng))
        self.ui.fgdc_northbc.setText(str(lat))

    @pyqtSlot(float, float)
    def on_nw_move(self, lat, lng):
        self.ui.fgdc_westbc.setText(str(lng))
        self.ui.fgdc_northbc.setText(str(lat))

    @pyqtSlot(float, float)
    def on_se_move(self, lat, lng):
        self.ui.fgdc_eastbc.setText(str(lng))
        self.ui.fgdc_southbc.setText(str(lat))

    @pyqtSlot(float, float)
    def on_sw_move(self, lat, lng):
        self.ui.fgdc_westbc.setText(str(lng))
        self.ui.fgdc_southbc.setText(str(lat))

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

    def all_good_coords(self):
        try:
            if -180 > float(self.ui.fgdc_westbc.text()) > 180:
                return False
            if -180 > float(self.ui.fgdc_eastbc.text()) > 180:
                return False
            if -90 > float(self.ui.fgdc_southbc.text()) > 90:
                return False
            if -90 > float(self.ui.fgdc_northbc.text()) > 90:
                return False
            if float(self.ui.fgdc_northbc.text()) <= float(self.ui.fgdc_southbc.text()):
                return False
            return True
        except:
            return False

    def clear_widget(self):
        super(self.__class__, self).clear_widget()

        # self.view.page().mainFrame().addToJavaScriptWindowObject("Spdom", self)
        # map_fname = utils.get_resource_path('leaflet/map.html')
        # self.view.setUrl(QUrl.fromLocalFile(map_fname))

    def showEvent(self, e):
        if not self.after_load:
           self.add_rect()
           self.update_map()
           jstr = "sw_marker.openPopup();"
           self.frame.evaluateJavaScript(jstr)
           self.after_load = True

    def _to_xml(self):
        spdom = xml_node('spdom')

        if self.schema == 'bdp':
            descgeog = xml_node('descgeog', text=self.ui.fgdc_descgeog.text(), parent_node=spdom)

        bounding = xml_node('bounding', parent_node=spdom)
        westbc = xml_node('westbc', text=self.ui.fgdc_westbc.text(), parent_node=bounding)
        eastbc = xml_node('eastbc', text=self.ui.fgdc_eastbc.text(), parent_node=bounding)
        northbc = xml_node('northbc', text=self.ui.fgdc_northbc.text(), parent_node=bounding)
        southbc = xml_node('southbc', text=self.ui.fgdc_southbc.text(), parent_node=bounding)

        if self.original_xml is not None:
            boundalt = xml_utils.search_xpath(self.original_xml, 'bounding/boundalt')
            if boundalt is not None:
                spdom.append(deepcopy(boundalt))

            dsgpoly_list = xml_utils.search_xpath(self.original_xml, 'dsgpoly',
                                                  only_first=False)
            for dsgpoly in dsgpoly_list:
                spdom.append(deepcopy(dsgpoly))

        return spdom

    def _from_xml(self, spdom):
        self.original_xml = spdom
        utils.populate_widget(self, spdom)

        contents = xml_utils.node_to_dict(spdom, add_fgdc=False)
        if 'bounding' in contents:
            contents = contents['bounding']

        try:
            if self.all_good_coords():
                self.add_rect()
                self.update_map()
            else:
                self.remove_rect()
        except KeyError:
            self.remove_rect()


if __name__ == "__main__":
    utils.launch_widget(Spdom)
