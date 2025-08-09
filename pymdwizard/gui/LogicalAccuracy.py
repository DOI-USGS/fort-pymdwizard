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
from pymdwizard.gui.ui_files import UI_logic


class LogicalAccuracy(WizardWidget):

    drag_label = "Logical Accuracy <logic>"
    acceptable_tags = ["logic"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_logic.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        logic element tag in xml tree
        """
        logic = xml_utils.xml_node(tag="logic")
        logic.text = self.findChild(QPlainTextEdit, "fgdc_logic").toPlainText()

        return logic

    def from_xml(self, logical_accuracy):
        """
        parses the xml code into the relevant logic elements

        Parameters
        ----------
        logical_accuracy - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if logical_accuracy.tag == "logic":
                accost_box = self.findChild(QPlainTextEdit, "fgdc_logic")
                accost_box.setPlainText(logical_accuracy.text)
            else:
                print("The tag is not logic")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(LogicalAccuracy, "Logical Accuracy testing")
