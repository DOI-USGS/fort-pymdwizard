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

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_descript
from pymdwizard.gui.abstract import Abstract


class Descript(WizardWidget):

    drag_label = "Abstract <abstract>"
    acceptable_tags = ["abstract"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_descript.Ui_fgdc_descript()
        self.ui.setupUi(self)

        self.setObjectName("fgdc_descript")
        self.abstract = Abstract()
        self.ui.verticalLayout.addWidget(self.abstract)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        abstract element tag in xml tree
        """

        return self.abstract.to_xml()

    def from_xml(self, abstract):
        """
        parses the xml code into the relevant abstract elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        self.abstract.from_xml(abstract)


if __name__ == "__main__":
    utils.launch_widget(Descript, "Abstract testing")
