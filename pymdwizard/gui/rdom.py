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

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_rdom


class Rdom(WizardWidget):  #

    drag_label = "Range Domain <rdom>"
    acceptable_tags = ["rdom"]

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_rdom.Ui_fgdc_attrdomv()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        rdom = xml_utils.xml_node("rdom")
        rdommin = xml_utils.xml_node(
            "rdommin", text=self.ui.fgdc_rdommin.text(), parent_node=rdom
        )
        rdommax = xml_utils.xml_node(
            "rdommax", text=self.ui.fgdc_rdommax.text(), parent_node=rdom
        )

        if self.ui.fgdc_attrunit.text():
            attrunit = xml_utils.xml_node(
                "attrunit", text=self.ui.fgdc_attrunit.text(), parent_node=rdom
            )

        if self.ui.fgdc_attrmres.text():
            attrmres = xml_utils.xml_node(
                "attrmres", text=self.ui.fgdc_attrmres.text(), parent_node=rdom
            )

        return rdom

    def from_xml(self, rdom):
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
            if rdom.tag == "rdom":
                utils.populate_widget(self, rdom)
            else:
                print("The tag is not rdom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Rdom, "udom testing")
