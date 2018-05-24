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

from PyQt5.QtWidgets import QMessageBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_distinfo
from pymdwizard.gui.ContactInfo import ContactInfo
from pymdwizard.gui.metainfo import MetaInfo


class DistInfo(WizardWidget):

    drag_label = "Distribution Information <distinfo>"
    acceptable_tags = ['distinfo']

    ui_class = UI_distinfo.Ui_fgdc_distinfo

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.root_widget = root_widget
        self.scroll_area = self.ui.scrollArea

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.contactinfo = ContactInfo(parent=self)
        self.metainfo = MetaInfo()

        self.ui.fgdc_distrib.layout().addWidget(self.contactinfo)

        self.ui.widget_distinfo.hide()

    def connect_events(self):
        self.ui.radio_distyes.toggled.connect(self.include_dist_contacts)
        self.ui.radio_online.toggled.connect(self.online_toggle)
        self.ui.radio_otherdist.toggled.connect(self.other_dist_toggle)
        self.ui.radio_dist.toggled.connect(self.dist_toggle)
        self.ui.button_use_sb.clicked.connect(self.pull_datasetcontact)

    def online_toggle(self, b):
        if b:
            self.ui.fgdc_networkr.setEnabled(True)
            self.ui.fgdc_distliab.setEnabled(True)
            self.ui.fgdc_fees.setEnabled(True)
        else:
            self.ui.fgdc_networkr.setEnabled(False)

    def other_dist_toggle(self, b):
        if b:
            self.ui.fgdc_custom.setEnabled(True)
            self.ui.fgdc_fees.setEnabled(False)
            self.ui.fgdc_distliab.setEnabled(True)
        else:
            self.ui.fgdc_custom.setEnabled(False)

    def dist_toggle(self, b):
        if b:
            self.ui.fgdc_distliab.setEnabled(True)
            self.ui.fgdc_fees.setEnabled(False)
        else:
            self.ui.fgdc_distliab.setEnabled(False)

    def include_dist_contacts(self, b):
        if b:
            self.ui.widget_distinfo.show()
        else:
            self.ui.widget_distinfo.hide()

    def pull_datasetcontact(self):
        try:
            sb_info = utils.get_usgs_contact_info('sciencebase',
                                                  as_dictionary=False)
            self.contactinfo.from_xml(sb_info)
        except:
            msg = "Having trouble getting sciencebase contact info now.\n"
            msg += "Check internet connection or try again latter."
            QMessageBox.warning(self, "Problem encountered", msg)

    def has_content(self):
        return self.ui.radio_distyes.isChecked()

    def to_xml(self):
        distinfo_node = xml_utils.xml_node('distinfo')

        dist = xml_utils.xml_node('distrib', parent_node=distinfo_node)
        cntinfo = self.contactinfo.to_xml()
        dist.append(cntinfo)

        if self.original_xml is not None:
            resdesc = xml_utils.search_xpath(self.original_xml, 'resdesc')
            if resdesc is not None:
                resdesc.tail = None
                distinfo_node.append(deepcopy(resdesc))

        if self.ui.radio_online.isChecked():
            liab = xml_utils.xml_node('distliab', text=self.ui.fgdc_distliab.toPlainText(),
                                      parent_node=distinfo_node)
            stdorder = xml_utils.xml_node('stdorder', parent_node=distinfo_node)
            digform = xml_utils.xml_node('digform', parent_node=stdorder)

            if self.original_xml is not None and \
               self.original_xml.xpath('stdorder/digform/digtinfo/formname'):
                digtinfo = self.original_xml.xpath('stdorder/digform/digtinfo')
                digform.append(deepcopy(digtinfo[0]))
            else:
                digtinfo = xml_utils.xml_node('digtinfo', parent_node=digform)
                formname = xml_utils.xml_node('formname', parent_node=digtinfo,
                                              text='Digital Data')

            digtopt = xml_utils.xml_node('digtopt', parent_node=digform)
            onlinopt = xml_utils.xml_node('onlinopt', parent_node=digtopt)
            computer = xml_utils.xml_node('computer', parent_node=onlinopt)
            networka = xml_utils.xml_node('networka', parent_node=computer)
            networkr = xml_utils.xml_node('networkr', text=self.ui.fgdc_networkr.text(), parent_node=networka)
            fees = xml_utils.xml_node('fees', text=self.ui.fgdc_fees.toPlainText(), parent_node=stdorder)

        if self.ui.radio_otherdist.isChecked():
            liab = xml_utils.xml_node('distliab', text=self.ui.fgdc_distliab.toPlainText(),
                                      parent_node=distinfo_node)
            other = xml_utils.xml_node('custom', text=self.ui.fgdc_custom.toPlainText(),
                                       parent_node=distinfo_node)

        if self.ui.radio_dist.isChecked():
            liab = xml_utils.xml_node('distliab', text=self.ui.fgdc_distliab.toPlainText(),
                                      parent_node=distinfo_node)

        if self.original_xml is not None:
            techpreq = xml_utils.search_xpath(self.original_xml, 'techpreq')
            if techpreq is not None:
                techpreq.tail = None
                distinfo_node.append(deepcopy(techpreq))

        return distinfo_node

    def from_xml(self, xml_distinfo):

        self.original_xml = xml_distinfo
        self.clear_widget()

        if xml_distinfo.tag == 'distinfo':
            self.original_xml = xml_distinfo
            self.ui.radio_distyes.setChecked(True)
            if xml_distinfo.xpath('distrib/cntinfo'):
                self.contactinfo.from_xml(xml_distinfo.xpath('distrib/cntinfo')[0])
            if xml_distinfo.xpath('distliab'):
                self.ui.radio_dist.setChecked(True)
                utils.populate_widget_element(widget=self.ui.fgdc_distliab,
                                              element=xml_distinfo,
                                              xpath='distliab')
                self.ui.fgdc_distliab.sizeChange()
            if xml_distinfo.xpath('custom'):
                self.ui.radio_otherdist.setChecked(True)
                utils.populate_widget_element(widget=self.ui.fgdc_custom,
                                              element=xml_distinfo,
                                              xpath='custom')
            if xml_distinfo.xpath('stdorder'):
                self.ui.radio_online.setChecked(True)
                utils.populate_widget_element(widget=self.ui.fgdc_networkr,
                                              element=xml_distinfo,
                                              xpath='stdorder/digform/digtopt/onlinopt/computer/networka/networkr')
                utils.populate_widget_element(widget=self.ui.fgdc_fees,
                                              element=xml_distinfo,
                                              xpath='stdorder/fees')


if __name__ == "__main__":
    utils.launch_widget(DistInfo, "DistInfo testing")