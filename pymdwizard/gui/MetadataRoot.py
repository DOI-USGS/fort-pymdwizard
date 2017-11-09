#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a completer FGDC record


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
import lxml
from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolButton
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint
from PyQt5.QtCore import Qt, QMimeData, QObject, QTimeLine

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QEvent, QCoreApplication
from PyQt5.QtGui import QMouseEvent

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_MetadataRoot
from pymdwizard.gui.IDInfo import IdInfo
from pymdwizard.gui.spatial_tab import SpatialTab
from pymdwizard.gui.EA import EA
from pymdwizard.gui.DataQuality import DataQuality
from pymdwizard.gui.metainfo import MetaInfo
from pymdwizard.gui.distinfo import DistInfo


class MetadataRoot(WizardWidget):

    drag_label = "Metadata <metadata>"
    acceptable_tags = ['abstract']

    ui_class = UI_MetadataRoot.Ui_metadata_root

    def __init__(self, parent=None):
        self.schema = 'bdp'
        super(self.__class__, self).__init__(parent=parent)

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

        self.idinfo = IdInfo(root_widget=self, parent=self)
        self.ui.page_idinfo.layout().addWidget(self.idinfo)

        self.dataqual =DataQuality()
        self.ui.page_dataqual.layout().addWidget(self.dataqual)
        # self.ui.page_dataqual.setLayout(self.dataqual.layout())

        self.spatial_tab = SpatialTab(root_widget=self)
        self.ui.page_spatial.layout().addWidget(self.spatial_tab)

        self.eainfo = EA()
        self.ui.page_eainfo.layout().addWidget(self.eainfo)

        self.metainfo = MetaInfo(root_widget=self)
        self.ui.page_metainfo.layout().addWidget(self.metainfo)

        self.distinfo = DistInfo(root_widget=self)
        self.ui.page_distinfo.layout().addWidget(self.distinfo)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.idinfo_button.pressed.connect(self.section_changed)
        self.ui.dataquality_button.pressed.connect(self.section_changed)
        self.ui.spatial_button.pressed.connect(self.section_changed)
        self.ui.eainfo_button.pressed.connect(self.section_changed)
        self.ui.distinfo_button.pressed.connect(self.section_changed)
        self.ui.metainfo_button.pressed.connect(self.section_changed)

    def section_changed(self):

        button_name = self.sender().objectName()

        index_lookup = {'idinfo_button': 0,
                        'dataquality_button': 1,
                        'spatial_button': 2,
                        'eainfo_button': 3,
                        'distinfo_button': 4,
                        'metainfo_button': 5}

        new_index = index_lookup[button_name]
        self.switch_section(which_index=new_index)

    def switch_section(self, which_index):
        if which_index == 0:
            self.ui.idinfo_button.setChecked(True)
        elif which_index == 1:
            self.ui.dataquality_button.setChecked(True)
        elif which_index == 2:
            self.ui.spatial_button.setChecked(True)
        elif which_index == 3:
            self.ui.eainfo_button.setChecked(True)
        elif which_index == 4:
            self.ui.distinfo_button.setChecked(True)
        elif which_index == 5:
            self.ui.metainfo_button.setChecked(True)

        old_widget = self.ui.fgdc_metadata.currentWidget()
        new_widget = self.ui.fgdc_metadata.widget(which_index)

        fader_widget = FaderWidget(old_widget, new_widget)
        self.ui.fgdc_metadata.setCurrentIndex(which_index)

    def switch_schema(self, schema):
        self.schema = schema
        self.idinfo.switch_schema(schema)
        self.spatial_tab.switch_schema(schema)

    def _to_xml(self):
        metadata_node = etree.Element('metadata')
        idinfo = self.idinfo._to_xml()
        metadata_node.append(idinfo)

        dataqual = self.dataqual._to_xml()
        metadata_node.append(dataqual)

        if self.spatial_tab.spdoinfo.has_content():
            spdoinfo = self.spatial_tab.spdoinfo._to_xml()
            metadata_node.append(spdoinfo)

        if self.spatial_tab.spref.has_content():
            spref = self.spatial_tab.spref._to_xml()
            metadata_node.append(spref)

        if self.eainfo.has_content():
            eainfo = self.eainfo._to_xml()
            metadata_node.append(eainfo)

        distinfo = self.distinfo._to_xml()
        metadata_node.append(distinfo)

        metainfo = self.metainfo._to_xml()
        metadata_node.append(metainfo)
        return metadata_node


    def _from_xml(self, metadata_element):

        self.populate_section(metadata_element, 'spdoinfo', self.spatial_tab.spdoinfo)
        #
        self.populate_section(metadata_element, 'spref', self.spatial_tab.spref)

        self.populate_section(metadata_element, 'idinfo', self.idinfo)

        self.populate_section(metadata_element, 'dataqual', self.dataqual)

        self.populate_section(metadata_element, 'eainfo', self.eainfo)

        self.populate_section(metadata_element, 'distinfo', self.distinfo)

        self.populate_section(metadata_element, 'metainfo', self.metainfo)

    def populate_section(self, metadata_element, section_name, widget):

        just_this_one = type(metadata_element) == etree._Element

        if just_this_one and metadata_element.tag == section_name:
            section = metadata_element
        elif just_this_one:
            return True
        else:
            section =  xml_utils.search_xpath(metadata_element, section_name)

        if section is not None:
            widget._from_xml(section)
        elif not just_this_one:
            widget.clear_widget()


class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):

        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(450)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()

if __name__ == "__main__":
    utils.launch_widget(MetadataRoot, "MetadataRoot testing")
