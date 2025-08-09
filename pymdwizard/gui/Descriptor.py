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
from pymdwizard.gui.ui_files import UI_Descriptor


class Descriptor(WizardWidget):

    drag_label = "Descriptor <descript>"
    acceptable_tags = ["descript"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_Descriptor.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        descript element tag in xml tree
        """
        descript = xml_utils.xml_node(tag="descript")

        abstract = xml_utils.xml_node(tag="abstract")
        abstract.text = self.findChild(QPlainTextEdit, "fgdc_abstract").toPlainText()
        descript.append(abstract)

        purpose = xml_utils.xml_node(tag="purpose")
        purpose.text = self.findChild(QPlainTextEdit, "fgdc_purpose").toPlainText()
        descript.append(purpose)

        supplinf_str = self.ui.fgdc_supplinf.toPlainText()
        if supplinf_str:
            upplinf = xml_utils.xml_node(
                "supplinf", text=supplinf_str, parent_node=descript
            )

        return descript

    def from_xml(self, descriptors):
        """
        parses the xml code into the relevant descript elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if descriptors.tag == "descript":
                try:

                    abstract = descriptors[0]
                    abstract_text = abstract.text
                    abstract_box = self.findChild(QPlainTextEdit, "fgdc_abstract")
                    abstract_box.setPlainText(abstract.text)

                    purpose = descriptors[1]
                    purpose_text = purpose.text
                    purpose_box = self.findChild(QPlainTextEdit, "fgdc_purpose")
                    purpose_box.setPlainText(purpose.text)

                    supplinf = descriptors[2]
                    supplinf_text = supplinf.text
                    supplinf_box = self.findChild(QPlainTextEdit, "fgdc_supplinf")
                    supplinf_box.setPlainText(supplinf.text)
                except:
                    abstract = descriptors[0]
                    abstract_text = abstract.text
                    abstract_box = self.findChild(QPlainTextEdit, "fgdc_abstract")
                    abstract_box.setPlainText(abstract.text)

                    purpose = descriptors[1]
                    purpose_text = purpose.text
                    purpose_box = self.findChild(QPlainTextEdit, "fgdc_purpose")
                    purpose_box.setPlainText(purpose.text)
            else:
                print("The tag is not descript")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Descriptor, "Descriptor testing")
