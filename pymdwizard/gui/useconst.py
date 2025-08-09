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
from pymdwizard.gui.ui_files import UI_useconst


class Useconst(WizardWidget):  #

    drag_label = "Use Constraints <useconst>"
    acceptable_tags = ["useconst"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_useconst.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        useconst element tag in xml tree
        """
        useconst = xml_utils.xml_node(
            "useconst", text=self.ui.fgdc_useconst.toPlainText()
        )
        return useconst

    def from_xml(self, useconst):
        """
        parses the xml code into the relevant useconst elements

        Parameters
        ----------
        use_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if useconst.tag == "useconst":
                self.ui.fgdc_useconst.setPlainText(useconst.text)
            else:
                print("The tag is not useconst")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Useconst, "Use Constraints testing")
