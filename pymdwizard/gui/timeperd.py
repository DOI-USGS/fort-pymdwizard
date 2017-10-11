#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Metadata Date <timeperd> section
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

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QStackedWidget


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


    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        timeperd = xml_utils.xml_node('timeperd')
        timeinfo = self.timeinfo._to_xml()

        timeperd.append(timeinfo)

        current = xml_utils.xml_node('current', parent_node=timeperd,
                                     text= self.ui.fgdc_current.currentText())

        return timeperd

    def _from_xml(self, timeperd):
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
                    self.timeinfo._from_xml(timeperd.xpath('timeinfo')[0])
                else:
                    pass



            else:
                print ("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Timeperd,
                        "Metadata Date testing")
