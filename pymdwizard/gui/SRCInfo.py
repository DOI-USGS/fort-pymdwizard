#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a SRCInfo <srcinfo> section


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

from lxml import etree

from PyQt5.QtWidgets import QComboBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_SRCInfo
from pymdwizard.gui.citeinfo import Citeinfo
from pymdwizard.gui.timeperd import Timeperd



class SRCInfo(WizardWidget): #

    drag_label = "SRCInfo <srcinfo>"
    acceptable_tags = ['srcinfo']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_SRCInfo.Ui_Form()
        self.ui.setupUi(self)
        self.timeperd = Timeperd()
        self.citation = Citeinfo(parent=self, include_lwork=False)

        self.ui.widget_citation.layout().addWidget(self.citation)
        self.ui.widget_timeperd.layout().addWidget(self.timeperd)

        self.setup_dragdrop(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.fgdc_srccitea.editingFinished.connect(self.update_tab_label)
        self.ui.fgdc_srcscale.editingFinished.connect(self.format_scale)

    def update_tab_label(self):
        new_label = "Source: {}".format(self.ui.fgdc_srccitea.text())
        tab_widget = self.ui.fgdc_srccitea.parent().parent().parent().parent()
        current_index = tab_widget.currentIndex()
        tab_widget.setTabText(current_index, new_label)

    def format_scale(self):
        cur_text = self.ui.fgdc_srcscale.text().replace(',', '')
        try:
            if '.' in cur_text:
                formatted_text = '{:,}'.format(float(cur_text))
            else:
                formatted_text = '{:,}'.format(int(cur_text))
            self.ui.fgdc_srcscale.setText(formatted_text)
        except:
            pass

    def _to_xml(self):
        """
        encapsulates the QLineEdit text in an element tag

        Returns
        -------
        srcinfo element tag in xml tree
        """
        srcinfo = xml_utils.xml_node('srcinfo')
        srccite = xml_utils.xml_node('srccite', parent_node=srcinfo)

        cite = self.citation._to_xml()
        srccite.append(cite)

        if self.ui.fgdc_srcscale.text():
            srcscale = xml_utils.xml_node('srcscale',
                                          text=self.ui.fgdc_srcscale.text().replace(',', ''),
                                          parent_node=srcinfo)

        typesrc = xml_utils.xml_node('typesrc',
                                      text=self.ui.fgdc_typesrc.currentText(),
                                      parent_node=srcinfo)

        srctime = xml_utils.xml_node('srctime', parent_node=srcinfo)
        time = self.timeperd._to_xml()
        timeinfo = time.xpath('/timeperd/timeinfo')[0]
        srctime.append(timeinfo)

        cur = time.xpath('/timeperd/current')[0]
        cur.tag = 'srccurr'
        srctime.append(cur)

        srccitea = xml_utils.xml_node('srccitea',
                                      text=self.ui.fgdc_srccitea.text(),
                                      parent_node=srcinfo)

        srccontr = xml_utils.xml_node('srccontr',
                                      text=self.ui.fgdc_srccontr.toPlainText(),
                                      parent_node=srcinfo)

        return srcinfo

    def _from_xml(self, srcinfo):
        """
        parses the xml code into the relevant srcinfo elements

        Parameters
        ----------
        srcinfo - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if srcinfo.tag == "srcinfo":
                utils.populate_widget(self, srcinfo)
                srccite = srcinfo.xpath('srccite')[0]
                citeinfo = srccite.xpath('citeinfo')[0]
            elif srcinfo.tag != 'srcinfo':
                print("The tag is not 'srcinfo'")
                return

            self.citation._from_xml(citeinfo)

            utils.populate_widget_element(self.ui.fgdc_srcscale, srcinfo, 'srcscale')
            self.format_scale()

            typesrc = srcinfo.xpath('typesrc/text()')
            typesrc_text = str(typesrc[0])
            self.findChild(QComboBox, "fgdc_typesrc").setCurrentText(typesrc_text)

            utils.populate_widget_element(self.ui.fgdc_srccitea, srcinfo, 'srccitea')

            utils.populate_widget_element(self.ui.fgdc_srccontr, srcinfo, 'srccontr')


            if srcinfo.xpath('srctime'):
                timeperd = etree.Element('timeperd')
                timeinfo = srcinfo.xpath('srctime/timeinfo')[0]
                srccurr = srcinfo.xpath('srctime/srccurr')[0]
                srccurr.tag = 'current'
                timeperd.append(timeinfo)
                timeperd.append(srccurr)
                self.timeperd._from_xml(timeperd)



        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(SRCInfo,
                        "SRCInfo testing")

