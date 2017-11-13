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

import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSettings

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import spatial_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spatial_tab
from pymdwizard.gui import spref
from pymdwizard.gui import spdoinfo
from pymdwizard.gui import spdom


class SpatialTab(WizardWidget):

    drag_label = "Spatial org and Spatial Ref <...>"
    acceptable_tags = ['idinfo']

    ui_class = UI_spatial_tab.Ui_spatial_tab

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.schema = 'bdp'
        self.root_widget = root_widget
        self.scroll_area = self.ui.spatial_scroll_area

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.spdom = spdom.Spdom()
        self.ui.spatial_main_widget.layout().insertWidget(0, self.spdom)

        self.spref = spref.SpRef()
        self.ui.two_column_left.layout().insertWidget(0, self.spref)

        self.spdoinfo = spdoinfo.SpdoInfo()
        self.ui.two_column_right.layout().insertWidget(0, self.spdoinfo)

        self.ui.btn_browse.clicked.connect(self.browse)
        self.clear_widget()

    def browse(self):
        settings = QSettings('USGS', 'pymdwizard')
        last_data_fname = settings.value('lastDataFname', '')
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(self, fname, dname,
                                            # Image Files (*.png *.jpg *.bmp)
                                            filter="Spatial files (*.shp *.tif *.jpg *.bmp *.img *.jp2 *.png *.grd)")
        if fname[0]:
            settings.setValue('lastDataFname', fname[0])
            self.populate_from_fname(fname[0])

    def populate_from_fname(self, fname):
        msg = ''
        try:
            spdom = spatial_utils.get_bounding(fname)
            self.spdom.from_xml(spdom)
        except:
            msg = "Problem encountered extracting bounding coordinates"
            self.spdom.clear_widget()

        try:
            spdoinfo = spatial_utils.get_spdoinfo(fname)
            self.spdoinfo.from_xml(spdoinfo)
        except:
            msg += "\nProblem encountered extracting spatial data organization"
            self.spdoinfo.clear_widget()

        try:
            spref = spatial_utils.get_spref(fname)
            self.spref.from_xml(spref)
        except:
            msg += "\nProblem encountered extracting spatial reference"
            self.spref.clear_widget()

        if msg:
            QMessageBox.warning(self, "Problem encountered", msg)

    def switch_schema(self, schema):
        self.spdom.switch_schema(schema)

    def clear_widget(self):
        self.spdoinfo.clear_widget()
        self.spdom.clear_widget()
        self.spref.clear_widget()

    def to_xml(self):
        # since this tab is composed of content from three disparate sections
        # the to and from xml functions are being handled
        # by the parent widget (MetadataRoot)
        return self.spdom.to_xml()

    def from_xml(self, xml_unknown):
        # since this tab is composed of content from three disparate sections
        # the to and from xml functions are being handled
        # by the parent widget (MetadataRoot)
        if xml_unknown.tag == 'spdoinfo':
            self.spdoinfo.from_xml(xml_unknown)
        elif xml_unknown.tag == 'spref':
            self.spref.from_xml(xml_unknown)
        elif xml_unknown.tag == 'spdom':
            self.spdom.from_xml(xml_unknown)

if __name__ == "__main__":
    utils.launch_widget(SpatialTab, "IdInfo testing")
