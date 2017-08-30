#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Distribution Information <distinfo> section


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

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_distinfo
from pymdwizard.gui.ContactInfo import ContactInfo
from pymdwizard.gui.metainfo import MetaInfo

class DistInfo(WizardWidget):

    drag_label = "Distribution Information <distinfo>"
    acceptable_tags = ['abstract']

    ui_class = UI_distinfo.Ui_fgdc_distinfo

    def __init__(self, root_widget=None):
        super(self.__class__, self).__init__()
        self.root_widget = root_widget

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
        sb_info = utils.get_usgs_contact_info('sciencebase',
                                              as_dictionary=False)
        self.contactinfo._from_xml(sb_info)


    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        print("distinfo drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'distinfo':
                e.accept()
        else:
            e.ignore()

    def has_content(self):
        return self.ui.radio_distyes.isChecked()

    def _to_xml(self):
        distinfo_node = xml_utils.xml_node('distinfo')

        dist = xml_utils.xml_node('distrib', parent_node=distinfo_node)
        cntinfo = self.contactinfo._to_xml()
        dist.append(cntinfo)

        if self.ui.radio_online.isChecked():
            liab = xml_utils.xml_node('distliab', text=self.ui.fgdc_distliab.toPlainText(),
                                      parent_node=distinfo_node)
            stdorder = xml_utils.xml_node('stdorder', parent_node=distinfo_node)
            digform = xml_utils.xml_node('digform', parent_node=stdorder)
            digtinfo = xml_utils.xml_node('digtinfo', parent_node=digform)
            formname = xml_utils.xml_node('formname', parent_node=digtinfo, text='Digital Data')
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
            # other = xml_utils.xml_node('custom', text=self.ui.fgdc_custom.toPlainText(),
            #                            parent_node=distinfo_node)

        return distinfo_node

    def _from_xml(self, xml_distinfo):

        self.clear_widget()

        if xml_distinfo.tag == 'distinfo':
            self.ui.radio_distyes.setChecked(True)
            if xml_distinfo.xpath('distrib/cntinfo'):
                self.contactinfo._from_xml(xml_distinfo.xpath('distrib/cntinfo')[0])
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