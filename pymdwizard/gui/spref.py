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
    This script is part of the pymdwizard package and is not intended to be
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

from copy import deepcopy

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core.xml_utils import xml_node
from pymdwizard.core import spatial_utils
from pymdwizard.core import fgdc_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spref
from pymdwizard.gui.mapproj import MapProj


class SpRef(WizardWidget):

    drag_label = "Spatial Reference <spref>"
    acceptable_tags = ['spref']

    ui_class = UI_spref.Ui_fgdc_spref

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

        self.mapproj = MapProj()
        self.ui.fgdc_mapproj.layout().addWidget(self.mapproj)

        self.grid_mapproj = MapProj()
        self.ui.fgdc_gridsys.layout().addWidget(self.grid_mapproj)

        self.ui.fgdc_gridsysn.addItems(spatial_utils.GRIDSYS_LOOKUP.keys())

        self.clear_widget()
        self.ui.fgdc_mapprojn.setCurrentText('Transverse Mercator')

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

        self.ui.fgdc_gridsysn.currentIndexChanged.connect(self.load_gridsys)
        self.load_gridsys()

        self.ui.fgdc_horizdn.currentIndexChanged.connect(self.load_datum)
        self.load_datum()

    def clear_widget(self):
        WizardWidget.clear_widget(self)
        self.ui.btn_geographic.setChecked(True)
        self.ui.rbtn_no.setChecked(True)
        self.spref_used_change(False)

    def spref_used_change(self, b):
        if b:
            self.ui.horiz_layout.show()
        else:
            self.ui.horiz_layout.hide()

    def has_content(self):
        return self.ui.rbtn_yes.isChecked()

    def system_def_changed(self):

        self.sender().objectName()

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
        try:
            projection = spatial_utils.PROJECTION_LOOKUP[projection_name]
            self.mapproj.load_projection(projection['shortname'])
        except:
            pass

    def load_gridsys(self):

        gridsys_name = self.ui.fgdc_gridsysn.currentText()
        projection = spatial_utils.GRIDSYS_LOOKUP[gridsys_name]

        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        layout = self.ui.gridsys_contents.layout()
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

        gridsys_proj = spatial_utils.PROJECTION_LOOKUP[projection['projection']]
        self.grid_mapproj.load_projection(gridsys_proj['shortname'])



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

    def to_xml(self):

        spref_node = xml_node('spref')

        horizsys = xml_node('horizsys',   parent_node=spref_node)

        if self.ui.btn_geographic.isChecked():
            geograph = xml_node('geograph', parent_node=horizsys)
            latres_str = self.findChild(QLineEdit, "fgdc_latres").text()
            xml_node('latres', latres_str, geograph)
            longres_str = self.findChild(QLineEdit, "fgdc_longres").text()
            xml_node('longres', longres_str, geograph)
            geogunit_str = self.findChild(QComboBox, 
                                          "fgdc_geogunit").currentText()
            xml_node('geogunit', geogunit_str, geograph)
        elif self.ui.btn_planar.isChecked():
            planar = xml_node('planar', parent_node=horizsys)

            if self.ui.btn_projection.isChecked():
                mapproj = xml_node('mapproj', parent_node=planar)
                projection_name = self.ui.fgdc_mapprojn.currentText()
                xml_node('mapprojn', text=projection_name, parent_node=mapproj)
                proj = self.mapproj.to_xml()
                mapproj.append(proj)
            elif self.ui.btn_grid.isChecked():
                gridsys = xml_node('gridsys', parent_node=planar)
                gridsys_name = self.ui.fgdc_gridsysn.currentText()
                gridsys_info = spatial_utils.GRIDSYS_LOOKUP[gridsys_name]

                xml_node('gridsysn', text=gridsys_name, parent_node=gridsys)

                root_node = xml_node(gridsys_info['shortname'],
                                               parent_node=gridsys)

                for item in gridsys_info['elements']:
                    widget = self.findChild(QLineEdit, "fgdc_"+item).text()
                    xml_node(item, text=widget, parent_node=root_node)

                proj = self.grid_mapproj.to_xml()
                root_node.append(proj)
            else:
                localp = xml_node('localp', parent_node=planar)
                localpd_str = self.ui.fgdc_localpd.text()
                xml_node('localpd', localpd_str, parent_node=localp)
                localpgi_str = self.ui.fgdc_localpgi.text()
                xml_node('localpgi', localpgi_str,
                                              parent_node=localp)

            planci = xml_node('planci', parent_node=planar)
            xml_node('plance', text=self.ui.fgdc_plance.currentText(),
                     parent_node=planci)
            coordrep = xml_node('coordrep', parent_node=planci)
            xml_node('absres', text=self.ui.fgdc_absres.text(),
                     parent_node=coordrep)
            xml_node('ordres', text=self.ui.fgdc_ordres.text(),
                     parent_node=coordrep)
            xml_node('plandu', text=self.ui.fgdc_plandu.currentText(),
                     parent_node=planci)
        else:
            local = xml_node('local', parent_node=horizsys)
            xml_node('localdes', text=self.ui.fgdc_localdes.text(),
                     parent_node=local)
            xml_node('localgeo', text=self.ui.fgdc_localgeo.text(),
                     parent_node=local)

        if self.findChild(QComboBox, "fgdc_horizdn").currentText():
            geodetic = xml_node('geodetic', parent_node=horizsys)
            horizdn_str = self.findChild(QComboBox,
                                         "fgdc_horizdn").currentText()
            xml_node('horizdn', horizdn_str, geodetic)
            ellips_str = self.findChild(QComboBox, "fgdc_ellips").currentText()
            xml_node('ellips', ellips_str, geodetic)
            semiaxis_str = self.findChild(QLineEdit, "fgdc_semiaxis").text()
            xml_node('semiaxis', semiaxis_str, geodetic)
            denflat_str = self.findChild(QLineEdit, "fgdc_denflat").text()
            xml_node('denflat', denflat_str, geodetic)

            if self.original_xml is not None:
                vertdef = xml_utils.search_xpath(self.original_xml, 'vertdef')
                if vertdef is not None:
                    vertdef.tail = None
                    spref_node.append(deepcopy(vertdef))

        return spref_node

    def from_xml(self, spref_node):
        self.clear_widget()
        if spref_node.tag == 'spref':
            self.original_xml = spref_node

            self.ui.rbtn_yes.setChecked(True)

            geograph = xml_utils.search_xpath(spref_node, 'horizsys/geograph')
            if geograph is not None:
                self.ui.btn_planar.setChecked(True)
                self.ui.btn_geographic.setChecked(True)

                utils.populate_widget_element(self.ui.fgdc_latres, 
                                              geograph, 'latres')
                utils.populate_widget_element(self.ui.fgdc_longres, 
                                              geograph, 'longres')
                utils.populate_widget_element(self.ui.fgdc_geogunit, 
                                              geograph, 'geogunit')

            local = xml_utils.search_xpath(spref_node, 'horizsys/local')
            if local is not None:
                self.ui.btn_planar.setChecked(True)
                self.ui.btn_local.setChecked(True)

                utils.populate_widget_element(self.ui.fgdc_localdes, local, 
                                              'localdes')
                utils.populate_widget_element(self.ui.fgdc_localgeo, local, 
                                              'localgeo')

            planar = xml_utils.search_xpath(spref_node, 'horizsys/planar')
            if planar is not None:
                self.ui.btn_grid.setChecked(True)
                self.ui.btn_planar.setChecked(True)

                mapproj = xml_utils.search_xpath(planar, 'mapproj')
                if mapproj is not None:
                    self.ui.btn_projection.setChecked(True)

                    utils.populate_widget_element(self.ui.fgdc_mapprojn, 
                                                  mapproj, 'mapprojn')
                    if mapproj.getchildren():
                        mapproj_contents = mapproj.getchildren()[1]
                        self.mapproj.from_xml(mapproj_contents)

                gridsys = xml_utils.search_xpath(planar, 'gridsys')
                if gridsys is not None:
                    self.ui.btn_grid.setChecked(True)
                    xml_utils.search_xpath(gridsys, 'gridsysn')
                    utils.populate_widget_element(self.ui.fgdc_gridsysn,
                                                  gridsys, 'gridsysn')

                    if gridsys.getchildren():
                        gridsys_contents = gridsys.getchildren()[1]
                        for item in gridsys_contents.getchildren():
                            tag = item.tag
                            if spatial_utils.lookup_shortname(tag) is not None:
                                self.grid_mapproj.from_xml(item)
                            elif tag == 'mapproj':
                                mapprojn = xml_utils.search_xpath(item, 
                                                                  'mapprojn')
                                if mapprojn.text in \
                                        spatial_utils.PROJECTION_LOOKUP:
                                    self.grid_mapproj.from_xml(item.getchildren()[1])
                            else:
                                item_widget = self.findChild(QLineEdit, 
                                                             "fgdc_"+tag)
                                utils.set_text(item_widget, item.text)

                    grid_proj = gridsys.xpath('proj')

                localp = xml_utils.search_xpath(planar, 'localp')
                if localp:
                    self.ui.btn_localp.setChecked(True)
                    utils.populate_widget_element(self.ui.fgdc_localpd, 
                                                  localp, 'localpd')
                    utils.populate_widget_element(self.ui.fgdc_localpgi, 
                                                  localp, 'localpgi')

                utils.populate_widget_element(self.ui.fgdc_plance, planar, 
                                              'planci/plance')
                utils.populate_widget_element(self.ui.fgdc_plandu, planar, 
                                              'planci/plandu')
                utils.populate_widget_element(self.ui.fgdc_absres, planar, 
                                              'planci/coordrep/absres')
                utils.populate_widget_element(self.ui.fgdc_ordres, planar, 
                                              'planci/coordrep/ordres')

                self.planar_changed()

            geodetic = xml_utils.search_xpath(spref_node, 'horizsys/geodetic')
            if geodetic is not None:
                utils.populate_widget_element(self.ui.fgdc_horizdn, geodetic, 
                                              'horizdn')
                utils.populate_widget_element(self.ui.fgdc_ellips, geodetic, 
                                              'ellips')
                utils.populate_widget_element(self.ui.fgdc_semiaxis, geodetic,
                                              'semiaxis')
                utils.populate_widget_element(self.ui.fgdc_denflat, geodetic, 
                                              'denflat')

if __name__ == "__main__":
    utils.launch_widget(SpRef, "spref testing")