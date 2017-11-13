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

from copy import deepcopy

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_metainfo
from pymdwizard.gui.ContactInfo import ContactInfo
from pymdwizard.gui.fgdc_date import FGDCDate


class MetaInfo(WizardWidget):

    drag_label = "Metadata Information <metainfo>"
    acceptable_tags = ['metainfo', 'cntinfo', 'ptcontact']

    ui_class = UI_metainfo.Ui_fgdc_metainfo

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.root_widget = root_widget

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.contactinfo = ContactInfo(parent=self)
        self.metd = FGDCDate(parent=self, fgdc_name='fgdc_metd')

        self.ui.help_metd.layout().addWidget(self.metd)

        self.ui.fgdc_metc.layout().addWidget(self.contactinfo)

    def connect_events(self):
        self.ui.fgdc_metstdn.currentTextChanged.connect(self.update_metstdv)
        self.ui.fgdc_metstdv.currentIndexChanged.connect(self.update_metstdn)
        self.ui.button_use_dataset.clicked.connect(self.pull_datasetcontact)

    def update_metstdn(self):
        if self.ui.fgdc_metstdv.currentText() == 'FGDC-STD-001-1998':
            self.ui.fgdc_metstdn.setCurrentIndex(0)
            self.root_widget.switch_schema('fgdc')
        elif self.ui.fgdc_metstdv.currentText() == 'FGDC-STD-001.1-1999':
            self.ui.fgdc_metstdn.setCurrentIndex(1)
            self.root_widget.switch_schema('bdp')

    def update_metstdv(self):
        if 'biological' in self.ui.fgdc_metstdn.currentText().lower() or \
           'bdp' in self.ui.fgdc_metstdn.currentText().lower():
            self.ui.fgdc_metstdv.setCurrentIndex(1)
            self.root_widget.switch_schema('bdp')
        else:
            self.ui.fgdc_metstdv.setCurrentIndex(0)
            self.root_widget.switch_schema('fgdc')

    def pull_datasetcontact(self):
        self.contactinfo.from_xml(self.root_widget.idinfo.ptcontac.to_xml())

    def to_xml(self):
        # add code here to translate the form into xml representation
        metainfo_node = xml_utils.xml_node('metainfo')
        metd = xml_utils.xml_node('metd', text=self.metd.get_date(),
                                  parent_node=metainfo_node)

        if self.original_xml is not None:
            metrd = xml_utils.search_xpath(self.original_xml, 'metrd')
            if metrd is not None:
                metrd.tail = None
                metainfo_node.append(deepcopy(metrd))
        if self.original_xml is not None:
            metfrd = xml_utils.search_xpath(self.original_xml, 'metfrd')
            if metfrd is not None:
                metfrd.tail = None
                metainfo_node.append(deepcopy(metfrd))

        metc = xml_utils.xml_node('metc', parent_node=metainfo_node)
        cntinfo = self.contactinfo.to_xml()
        metc.append(cntinfo)

        metstdn = xml_utils.xml_node('metstdn',
                                     text=self.ui.fgdc_metstdn.currentText(),
                                     parent_node=metainfo_node)
        metstdv = xml_utils.xml_node('metstdv',
                                     text=self.ui.fgdc_metstdv.currentText(),
                                     parent_node=metainfo_node)

        if self.original_xml is not None:
            mettc = xml_utils.search_xpath(self.original_xml, 'mettc')
            if mettc is not None:
                mettc.tail = None
                metainfo_node.append(deepcopy(mettc))
        if self.original_xml is not None:
            metac = xml_utils.search_xpath(self.original_xml, 'metac')
            if metac is not None:
                metac.tail = None
                metainfo_node.append(deepcopy(metac))

        metuc_str = "Record created using USGS Metadata Wizard tool. (https://github.com/usgs/fort-pymdwizard)"
        if self.original_xml is not None:
            metuc = xml_utils.search_xpath(self.original_xml, 'metuc')
            if metuc is not None:
                metuc_str = xml_utils.get_text_content(self.original_xml, 'metuc')
        metuc = xml_utils.xml_node('metuc',
                                   text=metuc_str,
                                   parent_node=metainfo_node)

        if self.original_xml is not None:
            metextns = xml_utils.search_xpath(self.original_xml, 'metextns')
            if metextns is not None:
                metextns.tail = None
                metainfo_node.append(deepcopy(metextns))

        return metainfo_node

    def from_xml(self, xml_metainfo):

        if xml_metainfo.tag == 'metainfo':
            self.original_xml = xml_metainfo

            if xml_metainfo.xpath('metc/cntinfo'):
                self.contactinfo.from_xml(xml_metainfo.xpath('metc/cntinfo')[0])

            if xml_metainfo.xpath('metstdn'):
                standard = xml_utils.get_text_content(xml_metainfo, 'metstdn')
                self.ui.fgdc_metstdn.setCurrentText(standard)
                # switch wizard content to reflect the standard in this record
                if "biological" in standard.lower() \
                        or 'bdp' in standard.lower():
                    self.root_widget.switch_schema('bdp')
                else:
                    self.root_widget.switch_schema('fgdc')

            metstdv = xml_utils.get_text_content(xml_metainfo, 'metstdv')
            self.ui.fgdc_metstdv.setCurrentText(metstdv)

            metd = xml_utils.get_text_content(xml_metainfo, 'metd')
            self.metd.set_date(metd)
        elif xml_metainfo.tag in ['ptcontac', 'cntinfo']:
            if xml_metainfo.tag == 'ptcontac':
                xml_metainfo = xml_utils.search_xpath(xml_metainfo, 'cntinfo')
            self.contactinfo.from_xml(xml_metainfo)

if __name__ == "__main__":
    utils.launch_widget(MetaInfo, "MetaInfo testing")