#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.

    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""
import platform
from copy import deepcopy

import pandas as pd

from PyQt5.QtWidgets import QMessageBox, QCompleter
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore

try:
    from PyQt5.QtWebKitWidgets import QWebView
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
    from PyQt5.QtWebEngineWidgets import QWebEnginePage
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import pyqtSlot, QStringListModel

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import spatial_utils
from pymdwizard.core.xml_utils import xml_node

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spdom


class Spdom(WizardWidget):
    drag_label = "Spatial Domain <spdom>"
    acceptable_tags = ['spdom', 'bounding']
    ui_class = UI_spdom.Ui_fgdc_spdom

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
        self.in_xml_load = False
        self.has_rect = True

        self.completer = QCompleter()
        self.ui.fgdc_descgeog.setCompleter(self.completer)

        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(0)

        fname = utils.get_resource_path("spatial/BNDCoords.csv")
        self.bnds_df = pd.read_csv(fname)
        self.model.setStringList(self.bnds_df['Name'])

        self.completer.popup().clicked.connect(self.on_completer_activated)
        self.completer.popup().selectionModel().selectionChanged.connect(self.on_completer_activated)
        # self.completer.popup().activated.connect(self.on_completer_activated)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)


        if platform.system() == 'Darwin':
            map_fname = utils.get_resource_path('leaflet/map_mac.html')
        else:
            map_fname = utils.get_resource_path('leaflet/map.html')

        try:
            self.view = QWebView()
            self.view.page().mainFrame().addToJavaScriptWindowObject("Spdom", self)
            self.view.setUrl(QUrl.fromLocalFile(map_fname))
            self.frame = self.view.page().mainFrame()
            self.view.load(QUrl.fromLocalFile(QtCore.QDir.current().filePath(map_fname)))
        except AttributeError:
            self.view = QWebView()
            self.view.load(QUrl.fromLocalFile(QtCore.QDir.current().filePath(map_fname)))
            channel = QWebChannel(self.view.page())

            jstr="""
            var spdom;

            new QWebChannel(qt.webChannelTransport, function (channel) {
                spdom = channel.objects.spdom;
            });"""

            self.view.page().setWebChannel(channel)
            self.evaluate_js(jstr)
            channel.registerObject("spdom", self)



        self.ui.verticalLayout_3.addWidget(self.view)

        # setup drag-drop functionality for this widget and all it's children.
        self.setup_dragdrop(self)
        self.add_rect()
        self.raise_()

    def connect_events(self):
        self.ui.fgdc_eastbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_westbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_northbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_southbc.editingFinished.connect(self.coord_updated)

    def on_completer_activated(self, model_index):

        try:
            cur_descgeog = model_index.data()
        except AttributeError:
            try:
                cur_descgeog = model_index.indexes()[0].data()
            except:
                return

        try:
            if self.bnds_df['Name'].str.contains(cur_descgeog).any():
                self.ui.fgdc_eastbc.setText(str(float(self.bnds_df[self.bnds_df['Name']==cur_descgeog]['east'])))
                self.ui.fgdc_westbc.setText(str(float(self.bnds_df[self.bnds_df['Name']==cur_descgeog]['west'])))
                self.ui.fgdc_northbc.setText(str(float(self.bnds_df[self.bnds_df['Name']==cur_descgeog]['north'])))
                self.ui.fgdc_southbc.setText(str(float(self.bnds_df[self.bnds_df['Name']==cur_descgeog]['south'])))
                self.add_rect()
                self.update_map()
        except:
            pass
            # this is a convenience function.
            # If anything at all happens pass silently

    def complete_name(self):
        self.view.page().runJavaScript('addRect();', js_callback)

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
        self.evaluate_js(jstr)

    def add_rect(self):
        jstr = """addRect();"""
        self.evaluate_js(jstr)

    def remove_rect(self):
        if self.has_rect:
            self.has_rect = False
            jstr = """removeRect()"""
            self.evaluate_js(jstr)

    def evaluate_js(self, jstr):
        """

        :param jstr:
        :return:
        """
        try:
            self.frame.evaluateJavaScript(jstr)
        except:
            self.view.page().runJavaScript(jstr, js_callback)

    @pyqtSlot(float, float)
    def on_ne_move(self, lat, lng):
        if self.in_xml_load:
            n, e = lat, lng
            try:
                s = float(self.ui.fgdc_southbc.text())
                w = float(self.ui.fgdc_westbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_eastbc.setText(bounds[1])
                self.ui.fgdc_northbc.setText(bounds[2])
            except:
                pass

    @pyqtSlot(float, float)
    def on_nw_move(self, lat, lng):
        if self.in_xml_load:
            n, w = lat, lng
            try:
                s = float(self.ui.fgdc_southbc.text())
                e = float(self.ui.fgdc_eastbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_westbc.setText(bounds[0])
                self.ui.fgdc_northbc.setText(bounds[2])
            except:
                pass

    @pyqtSlot(float, float)
    def on_se_move(self, lat, lng):
        if self.in_xml_load:
            s, e = lat, lng
            try:
                n = float(self.ui.fgdc_northbc.text())
                w = float(self.ui.fgdc_westbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_eastbc.setText(bounds[1])
                self.ui.fgdc_southbc.setText(bounds[3])
            except:
                pass

    @pyqtSlot(float, float)
    def on_sw_move(self, lat, lng):
        if self.in_xml_load:
            s, w = lat, lng
            try:
                n = float(self.ui.fgdc_northbc.text())
                e = float(self.ui.fgdc_eastbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_westbc.setText(bounds[0])
                self.ui.fgdc_southbc.setText(bounds[3])
            except:
                pass

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
            self.evaluate_js(jstr)
            self.after_load = True

    def to_xml(self):
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

    def from_xml(self, spdom):
        self.in_xml_load = False
        self.original_xml = spdom
        self.clear_widget()
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
        self.in_xml_load = True


def js_callback(result):
    print(result)


if __name__ == "__main__":
    w = utils.launch_widget(Spdom)

