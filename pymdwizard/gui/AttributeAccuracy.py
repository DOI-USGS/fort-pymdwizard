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

from copy import deepcopy

from PyQt5.QtWidgets import QPlainTextEdit
from pymdwizard.core import xml_utils
from pymdwizard.core import utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_attracc


class AttributeAccuracy(WizardWidget):

    drag_label = "Attribute Accuracy <attracc>"
    acceptable_tags = ["attracc"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_attracc.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)
        self.ui.fgdc_attraccr.setFixedHeight(55)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        attraccr element tag in xml tree
        """
        attracc = xml_utils.xml_node(tag="attracc")
        attraccr_str = self.findChild(QPlainTextEdit, "fgdc_attraccr").toPlainText()
        attraccr = xml_utils.xml_node(
            tag="attraccr", text=attraccr_str, parent_node=attracc
        )

        if self.original_xml is not None:
            qattracc = xml_utils.search_xpath(self.original_xml, "qattracc")
            if qattracc is not None:
                qattracc.tail = None
                attracc.append(deepcopy(qattracc))

        return attracc

    def from_xml(self, attribute_accuracy):
        """
        parses the xml code into the relevant attraccr elements

        Parameters
        ----------
        attribute_accuracy - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if attribute_accuracy.tag == "attracc":
                self.original_xml = attribute_accuracy
                attraccr_text = attribute_accuracy.findtext("attraccr")
                accost_box = self.findChild(QPlainTextEdit, "fgdc_attraccr")
                accost_box.setPlainText(attraccr_text)
            else:
                print("The tag is not attracc")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(AttributeAccuracy, "Attribute Accuracy testing")
