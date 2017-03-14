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


class MetadataRoot(WizardWidget):

    drag_label = "Metadata <metadata>"

    ui_class = UI_MetadataRoot.Ui_metadata_root

    def __init__(self):
        self.schema = 'bdp'
        super(self.__class__, self).__init__()

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

        self.idinfo = IdInfo(root_widget=self)
        self.ui.page_idinfo.layout().addWidget(self.idinfo)

        self.dataqual =DataQuality()
        self.ui.page_dataqual.setLayout(self.dataqual.layout())

        self.spatial_tab = SpatialTab(root_widget=self)
        self.ui.page_spatial.setLayout(self.spatial_tab.layout())

        self.eainfo = EA()
        self.ui.page_eainfo.setLayout(self.eainfo.layout())

        self.metainfo = MetaInfo(root_widget=self)
        self.ui.page_metainfo.layout().addWidget(self.metainfo)

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
        old_widget = self.ui.fgdc_metadata.currentWidget()


        index_lookup = {'idinfo_button': 0,
                        'dataquality_button': 1,
                        'spatial_button': 2,
                        'eainfo_button': 3,
                        'distinfo_button': 4,
                        'metainfo_button': 5,
                        'validation_button': 6}

        new_index = index_lookup[button_name]

        new_widget = self.ui.fgdc_metadata.widget(new_index)

        fader_widget = FaderWidget(old_widget, new_widget)
        self.ui.fgdc_metadata.setCurrentIndex(new_index)

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

        if self.spatial_tab.spdoinfo.ui.rbtn_yes.isChecked():
            spdoinfo = self.spatial_tab.spdoinfo._to_xml()
            metadata_node.append(spdoinfo)

        spref = self.spatial_tab.spref._to_xml()
        metadata_node.append(spref)

        if self.eainfo.has_content():
            eainfo = self.eainfo._to_xml()
            metadata_node.append(eainfo)

        metainfo = self.metainfo._to_xml()
        metadata_node.append(metainfo)
        return metadata_node


    def _from_xml(self, metadata_element):
        self.idinfo._from_xml(metadata_element.xpath('idinfo')[0])

        dataqual = metadata_element.xpath('dataqual')
        if dataqual:
            self.dataqual._from_xml(dataqual[0])

        spdom = metadata_element.xpath('idinfo/spdom')
        if spdom:
            self.spatial_tab.spdom._from_xml(spdom[0])

        spdoinfo = metadata_element.xpath('spdoinfo')
        if spdoinfo:
            self.spatial_tab.spdoinfo._from_xml(spdoinfo[0])

        spref = metadata_element.xpath('spref')
        if spref:
            self.spatial_tab.spref._from_xml(spref[0])

        eainfo = metadata_element.xpath('eainfo')
        if eainfo:
            self.eainfo._from_xml(eainfo[0])
        else:
            self.eainfo.clear_widget()

        self.metainfo._from_xml(metadata_element.xpath('metainfo')[0])


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
