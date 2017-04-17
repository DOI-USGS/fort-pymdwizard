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
from pymdwizard.gui.ui_files import UI_mapproj


class MapProj(WizardWidget):

    drag_label = "Map Projection <mapproj>"

    ui_class = UI_mapproj.Ui_Form

    def build_ui(self):
        self.shortname = ''

        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def clear_widget(self):
        layout = self.ui.mapproj_contents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_projection(self, shortname):

        self.clear_widget()
        self.shortname = shortname
        self.projection = spatial_utils.lookup_shortname(shortname)

        annotation_lookup_fname = utils.get_resource_path('fgdc/bdp_lookup')
        try:
            with open(annotation_lookup_fname, encoding='utf-8') as data_file:
                annotation_lookup = json.loads(data_file.read())
        except TypeError:
            with open(annotation_lookup_fname) as data_file:
                annotation_lookup = json.loads(data_file.read())

        annotation_lookup['stdparl_2'] = {'long_name':'Standard Parallel',
                                      'annotation':annotation_lookup['stdparll']['annotation']}

        self.clear_widget()
        layout = self.ui.mapproj_contents.layout()

        for param in self.projection['elements']:
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
            layout.insertRow(layout.count()-1, label, lineedit)

    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        # e.ignore()
        e.accept()

    def _to_xml(self):

        if self.shortname:
            proj_root = xml_utils.xml_node(self.shortname)

            for param in self.projection['elements']:
                widget = self.findChild(QLineEdit, "fgdc_"+param)
                xml_utils.xml_node(param, text=widget.text(), parent_node=proj_root)

            return proj_root
        else:
            return None


    def _from_xml(self, mapproj_node):
        self.clear_widget()

        shortname = mapproj_node.tag
        self.load_projection(shortname)

        for item in mapproj_node.getchildren():
            tag = item.tag
            item_widget = self.findChild(QLineEdit, "fgdc_"+tag)
            utils.set_text(item_widget, item.text)

        #
        # for param in self.projection['elements']:
        #
        # if spref_node.tag == 'spref':
        #     self.ui.rbtn_yes.setChecked(True)
        #
        #     geograph = xml_utils.search_xpath(spref_node, 'horizsys/geograph')
        #     if geograph is not None:
        #         self.ui.btn_geographic.setChecked(True)
        #
        #         utils.populate_widget_element(self.ui.fgdc_latres, geograph, 'latres')
        #         utils.populate_widget_element(self.ui.fgdc_longres, geograph, 'longres')
        #         utils.populate_widget_element(self.ui.fgdc_geogunit, geograph, 'geogunit')
        #
        #     local = xml_utils.search_xpath(spref_node, 'horizsys/local')
        #     if local is not None:
        #         self.ui.btn_local.setChecked(True)
        #
        #         utils.populate_widget_element(self.ui.fgdc_localdes, local, 'localdes')
        #         utils.populate_widget_element(self.ui.fgdc_localgeo, local, 'localgeo')
        #
        #     planar = xml_utils.search_xpath(spref_node, 'horizsys/planar')
        #     if planar is not None:
        #         self.ui.btn_planar.setChecked(True)
        #
        #         mapproj = xml_utils.search_xpath(planar, 'mapproj')
        #         if mapproj is not None:
        #             self.ui.btn_projection.setChecked(True)
        #
        #             utils.populate_widget_element(self.ui.fgdc_mapprojn, mapproj, 'mapprojn')
        #             mapproj_contents = mapproj.getchildren()[1]
        #             for item in mapproj_contents.getchildren():
        #                 tag = item.tag
        #                 item_widget = self.findChild(QLineEdit, "fgdc_"+tag)
        #                 utils.set_text(item_widget, item.text)
        #
        #             stdparll = mapproj_contents.xpath('stdparll')
        #             try:
        #                 stdparll_widget = self.findChildren(QLineEdit, "fgdc_stdparll")[0]
        #                 utils.set_text(stdparll_widget, stdparll[0].text)
        #                 stdparl_2_widget = self.findChildren(QLineEdit, "fgdc_stdparl_2")[0]
        #                 utils.set_text(stdparl_2_widget, stdparll[1].text)
        #             except:
        #                 pass
        #
        #         gridsys = xml_utils.search_xpath(planar, 'gridsys')
        #         if gridsys is not None:
        #             self.ui.btn_grid.setChecked(True)
        #
        #             utils.populate_widget_element(self.ui.fgdc_gridsysn, gridsys, 'gridsysn')
        #             gridsys_contents = gridsys.getchildren()[1]
        #             for item in gridsys_contents.getchildren():
        #                 tag = item.tag
        #                 if spatial_utils.lookup_shortname(tag) is not None:
        #
        #                 else
        #                     item_widget = self.findChild(QLineEdit, "fgdc_"+tag)
        #                     utils.set_text(item_widget, item.text)
        #
        #             grid_proj = gridsys.xpath('proj')
        #
        #
        #         localp = xml_utils.search_xpath(planar, 'localp')
        #         if localp:
        #             self.ui.btn_localp.setChecked(True)
        #             utils.populate_widget_element(self.ui.fgdc_localpd, localp, 'localpd')
        #             utils.populate_widget_element(self.ui.fgdc_localpgi, localp, 'localpgi')
        #
        #         utils.populate_widget_element(self.ui.fgdc_plance, planar, 'planci/plance')
        #         utils.populate_widget_element(self.ui.fgdc_plandu, planar, 'planci/plandu')
        #         utils.populate_widget_element(self.ui.fgdc_absres, planar, 'planci/coordrep/absres')
        #         utils.populate_widget_element(self.ui.fgdc_ordres, planar, 'planci/coordrep/ordres')
        #
        #         self.planar_changed()
        #
        #     geodetic = xml_utils.search_xpath(spref_node, 'horizsys/geodetic')
        #     if geodetic is not None:
        #         utils.populate_widget_element(self.ui.fgdc_horizdn, geodetic, 'horizdn')
        #         utils.populate_widget_element(self.ui.fgdc_ellips, geodetic, 'ellips')
        #         utils.populate_widget_element(self.ui.fgdc_semiaxis, geodetic, 'semiaxis')
        #         utils.populate_widget_element(self.ui.fgdc_denflat, geodetic, 'denflat')

if __name__ == "__main__":
    utils.launch_widget(MapProj, "spref testing")