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

from PyQt5.QtWidgets import QComboBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_timeperd
from pymdwizard.gui import timeinfo

class Timeperd(WizardWidget):  #

    drag_label = "Time Period of Content <timeperd>"
    acceptable_tags = ['timeperd']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_timeperd.Ui_Form()
        self.ui.setupUi(self)

        self.timeinfo = timeinfo.Timeinfo(parent=self)
        self.ui.fgdc_timeperd.layout().insertWidget(0, self.timeinfo)

        self.setup_dragdrop(self)


    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        timeperd = xml_utils.xml_node('timeperd')
        timeinfo = self.timeinfo.to_xml()

        timeperd.append(timeinfo)

        current = xml_utils.xml_node('current', parent_node=timeperd,
                                     text= self.ui.fgdc_current.currentText())

        return timeperd

    def from_xml(self, timeperd):
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
            if timeperd.tag == 'timeperd':

                if timeperd.findall("current"):
                    current_text = timeperd.findtext("current")
                    current_box = self.findChild(QComboBox, 'fgdc_current')
                    current_box.setCurrentText(current_text)
                else:
                    pass

                if timeperd.findall("timeinfo"):
                    self.timeinfo.from_xml(timeperd.xpath('timeinfo')[0])
                else:
                    pass



            else:
                print ("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Timeperd,
                        "Metadata Date testing")

