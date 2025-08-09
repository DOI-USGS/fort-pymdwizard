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

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_posacc


class PositionalAccuracy(WizardWidget):  #

    drag_label = "Positional Accuracy <possacc>"
    acceptable_tags = ["posacc"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_posacc.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def has_content(self):
        """
        Checks for valid content in this widget

        Returns
        -------
        Boolean
        """
        has_content = False

        if self.ui.fgdc_horizpa.toPlainText():
            has_content = True
        if self.ui.fgdc_vertacc.toPlainText():
            has_content = True

        return has_content

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        possacc element tag in xml tree
        """
        possacc = xml_utils.xml_node(tag="posacc")
        horizpa = xml_utils.xml_node(tag="horizpa")
        horizpar = xml_utils.xml_node(tag="horizpar")
        horizpar_text = self.findChild(QPlainTextEdit, "fgdc_horizpa").toPlainText()
        if len(horizpar_text) > 0:
            horizpar.text = horizpar_text
            horizpa.append(horizpar)
            possacc.append(horizpa)

        vertacc = xml_utils.xml_node(tag="vertacc")
        vertaccr = xml_utils.xml_node(tag="vertaccr")
        vertaccr_text = self.findChild(QPlainTextEdit, "fgdc_vertacc").toPlainText()
        if len(vertaccr_text) > 0:
            vertaccr.text = vertaccr_text
            vertacc.append(vertaccr)
            possacc.append(vertacc)
        return possacc

    def from_xml(self, positional_accuracy):
        """
        parses the xml code into the relevant possacc elements

        Parameters
        ----------
        postional_accuracy - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if positional_accuracy.tag == "posacc":
                horizpa_text = positional_accuracy.findtext("horizpa/horizpar")
                horizpa_box = self.findChild(QPlainTextEdit, "fgdc_horizpa")
                horizpa_box.setPlainText(horizpa_text)

                vertacc_text = positional_accuracy.findtext("vertacc/vertaccr")
                vertacc_box = self.findChild(QPlainTextEdit, "fgdc_vertacc")
                vertacc_box.setPlainText(vertacc_text)
            else:
                print("The tag is not possacc")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(PositionalAccuracy, "Positional Accuracy testing")
