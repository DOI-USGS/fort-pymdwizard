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
from pymdwizard.gui.ui_files import UI_native


class Native(WizardWidget):  #

    drag_label = "Native data set environment <native>"
    acceptable_tags = ["native"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_native.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def has_content(self):
        return self.ui.fgdc_native.toPlainText() != ""

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        native element tag in xml tree
        """
        native = xml_utils.xml_node("native", text=self.ui.fgdc_native.toPlainText())
        return native

    def from_xml(self, native):
        """
        parses the xml code into the relevant native elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if native.tag == "native":
                self.ui.fgdc_native.setPlainText(native.text)
            else:
                print("The tag is not native")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Native, "Access Constraints testing")
