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
from pymdwizard.gui.ui_files import UI_udom
from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter


class Udom(WizardWidget):

    drag_label = "Unrepresentable Domain <udom>"
    acceptable_tags = ["udom"]

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_udom.Ui_fgdc_attrdomv()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)
        self.highlighter = Highlighter(self.ui.fgdc_udom.document())

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        udom = xml_utils.xml_node("udom", self.ui.fgdc_udom.toPlainText())

        return udom

    def from_xml(self, udom):
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
            if udom.tag == "udom":
                utils.populate_widget(self, udom)
            else:
                print("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Udom, "udom testing")
