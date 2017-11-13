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
The widget for the main metadata root item.
This is the container for an FGDC record without the application wrapper,
menu bar, etc.


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
from lxml import etree

from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimeLine

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
        self.use_dataqual = True
        self.use_spatial = True
        self.use_eainfo = True
        self.use_distinfo = True


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

        self.dataqual = DataQuality()
        self.ui.page_dataqual.layout().addWidget(self.dataqual)

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
        """
        The event which switches the currently displayed main section
        when a user clicks on one of the top level section header buttons.

        Returns
        -------
        None
        """

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
        """
        sub funtion that does the actual switching, creating a fader widget,
        etc.

        Parameters
        ----------
        which_index : int
            The index of the section to display

        Returns
        -------
        None
        """
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

        FaderWidget(old_widget, new_widget)
        self.ui.fgdc_metadata.setCurrentIndex(which_index)

        return new_widget

    def switch_schema(self, schema):
        """
        Switch the displayed schema between straight FGDC and BDP

        Parameters
        ----------
        schema : str

        Returns
        -------

        """
        self.schema = schema
        self.idinfo.switch_schema(schema)
        self.spatial_tab.switch_schema(schema)

    def use_section(self, which, value):
        """
        enable or disable top optional top level sections

        Parameters
        ----------
        which : str
                Which section to change: ['dataqual', 'spatial', 'ea',
                                          'distinfo']
        value : bool
                Whether to enable (True) or disable (False)

        Returns
        -------
        None
        """
        if which == 'dataqual':
            self.use_dataqual = value
            self.dataqual.setVisible(value)
        if which == 'spatial':
            self.use_spatial = value
            self.spatial_tab.setVisible(value)
        if which == 'eainfo':
            self.use_eainfo = value
            self.eainfo.setVisible(value)
        if which == 'distinfo':
            self.use_distinfo = value
            self.distinfo.setVisible(value)

    def to_xml(self):
        metadata_node = xml_utils.xml_node(tag='metadata')
        idinfo = self.idinfo.to_xml()
        metadata_node.append(idinfo)

        if self.use_dataqual:
            dataqual = self.dataqual.to_xml()
            metadata_node.append(dataqual)

        if self.spatial_tab.spdoinfo.has_content() and self.use_spatial:
            spdoinfo = self.spatial_tab.spdoinfo.to_xml()
            metadata_node.append(spdoinfo)

        if self.spatial_tab.spref.has_content() and self.use_spatial:
            spref = self.spatial_tab.spref.to_xml()
            metadata_node.append(spref)

        if self.eainfo.has_content() and self.use_eainfo:
            eainfo = self.eainfo.to_xml()
            metadata_node.append(eainfo)

        if self.use_distinfo:
            distinfo = self.distinfo.to_xml()
            metadata_node.append(distinfo)

        metainfo = self.metainfo.to_xml()
        metadata_node.append(metainfo)
        return metadata_node

    def from_xml(self, metadata_element):

        self.populate_section(metadata_element, 'spdoinfo',
                              self.spatial_tab.spdoinfo)

        self.populate_section(metadata_element, 'spref',
                              self.spatial_tab.spref)

        self.populate_section(metadata_element, 'idinfo', self.idinfo)

        self.populate_section(metadata_element, 'dataqual', self.dataqual)

        self.populate_section(metadata_element, 'eainfo', self.eainfo)

        self.populate_section(metadata_element, 'distinfo', self.distinfo)

        self.populate_section(metadata_element, 'metainfo', self.metainfo)

    def populate_section(self, metadata_element, section_name, widget):
        """
        Since the content of top level sections might contain items that
        need to go to separate top level items, this function handles the
        divvying up of sub-content.

        Parameters
        ----------
        metadata_element : XML Element
        section_name : Section tag to populate
        widget :  The section widget

        Returns
        -------

        """
        just_this_one = type(metadata_element) == etree._Element

        if just_this_one and metadata_element.tag == section_name:
            section = metadata_element
        elif just_this_one:
            return True
        else:
            section = xml_utils.search_xpath(metadata_element, section_name)

        if section is not None:
            widget.from_xml(section)
        elif not just_this_one:
            widget.clear_widget()


class FaderWidget(QWidget):
    """
    A QWidget that allows for fading in and out on display.
    """
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

