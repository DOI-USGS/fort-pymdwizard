#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


NOTES
------------------------------------------------------------------------------
None
"""

from PyQt5.QtWidgets import QComboBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_timeperd
from pymdwizard.gui import timeinfo


class Timeperd(WizardWidget):  #

    drag_label = "Time Period of Content <timeperd>"
    acceptable_tags = ["timeperd"]

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
        timeperd = xml_utils.xml_node("timeperd")
        timeinfo = self.timeinfo.to_xml()

        timeperd.append(timeinfo)

        current = xml_utils.xml_node(
            "current", parent_node=timeperd, text=self.ui.fgdc_current.currentText()
        )

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
            if timeperd.tag == "timeperd":

                if timeperd.findall("current"):
                    current_text = timeperd.findtext("current")
                    current_box = self.findChild(QComboBox, "fgdc_current")
                    current_box.setCurrentText(current_text)
                else:
                    pass

                if timeperd.findall("timeinfo"):
                    self.timeinfo.from_xml(timeperd.xpath("timeinfo")[0])
                else:
                    pass

            else:
                print("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Timeperd, "Metadata Date testing")
