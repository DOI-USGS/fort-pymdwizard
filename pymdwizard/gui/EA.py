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

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_EA
from pymdwizard.gui.detailed import Detailed


class EA(WizardWidget):  #

    drag_label = "Entity and Attributes <eainfo>"
    acceptable_tags = ['eainfo', 'detailed']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_EA.Ui_Form()
        self.ui.setupUi(self)

        self.detaileds = []
        detailed = self.add_detailed()

        self.setup_dragdrop(self)
        return None

    def connect_events(self):
        self.ui.btn_add_detailed.clicked.connect(self.add_detailed)

    def remove_detailed(self):
        cur_index = self.ui.fgdc_eainfo.currentIndex()
        self.ui.fgdc_eainfo.removeTab(cur_index)
        del self.detaileds[cur_index-1]

    def add_detailed(self):
        """
        Adds another Detailed tab to the form
        Returns
        -------
        None
        """
        new_detailed = Detailed(remove_function=self.remove_detailed, parent=self)
        self.ui.fgdc_eainfo.insertTab(self.ui.fgdc_eainfo.count()-1,
                                      new_detailed, 'Detailed')
        self.detaileds.append(new_detailed)
        return new_detailed

    def clear_widget(self):
        """
        Clears all content from this widget

        Returns
        -------
        None
        """
        self.detaileds[0].clear_widget()
        for i in range(len(self.detaileds), 1, -1):
            self.ui.fgdc_eainfo.removeTab(i)
            del self.detaileds[i-1]

        utils.set_text(self.ui.fgdc_eaover, '')
        utils.set_text(self.ui.fgdc_eadetcit, '')

    def has_content(self):
        """
        Checks for valid content in this widget

        Returns
        -------
        Boolean
        """
        has_content = False

        if self.ui.fgdc_eadetcit.toPlainText():
            has_content = True
        if self.ui.fgdc_eaover.toPlainText():
            has_content = True
        if self.detaileds and self.detaileds[0].has_content():
            has_content = True
        for detailed in self.detaileds:
            if detailed.has_content():
                has_content = True

        return has_content

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        eainfo = xml_utils.xml_node('eainfo')

        #only output the first detailed if it has content
        if self.detaileds and self.detaileds[0].has_content():
            detailed_xml = self.detaileds[0].to_xml()
            eainfo.append(detailed_xml)

        #the remaining detaileds will get output regardless
        for detailed in self.detaileds[1:]:
            detailed_xml = detailed.to_xml()
            eainfo.append(detailed_xml)

        eaover_str = self.ui.fgdc_eaover.toPlainText()
        eadetcit_str = self.ui.fgdc_eadetcit.toPlainText()

        if eaover_str or eadetcit_str:
            overview = xml_utils.xml_node('overview', parent_node=eainfo)
            eaover = xml_utils.xml_node('eaover', text=eaover_str, parent_node=overview)
            eadetcit = xml_utils.xml_node('eadetcit', text=eadetcit_str, parent_node=overview)

        return eainfo

    def from_xml(self, eainfo):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            self.ui.fgdc_eainfo.setCurrentIndex(0)
            self.clear_widget()

            if eainfo.tag == 'eainfo':
                self.original_xml = eainfo
                overview = eainfo.xpath('overview')
                if overview:
                    eaover = eainfo.xpath('overview/eaover')
                    if eaover:
                        utils.set_text(self.ui.fgdc_eaover, eaover[0].text)

                    eadetcit = eainfo.xpath('overview/eadetcit')
                    if eadetcit:
                        utils.set_text(self.ui.fgdc_eadetcit, eadetcit[0].text)
                    self.ui.fgdc_eainfo.setCurrentIndex(2)

                detailed = eainfo.xpath('detailed')
                if detailed:
                    self.ui.fgdc_eainfo.setCurrentIndex(1)
                    self.detaileds[0].from_xml(detailed[0])

                    for i, additional_detailed in enumerate(detailed[1:]):
                        new_detailed = self.add_detailed()
                        self.ui.fgdc_eainfo.setCurrentIndex(i+2)
                        new_detailed.from_xml(additional_detailed)

            else:
                print("The tag is not EA")
        except KeyError:
            return None
        return None


if __name__ == "__main__":
    utils.launch_widget(EA,
                        "detailed testing")
