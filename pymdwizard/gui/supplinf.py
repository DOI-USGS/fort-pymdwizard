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

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QPlainTextEdit
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_supplinf
except ImportError as err:
    raise ImportError(err, __file__)


class SupplInf(WizardWidget):

    drag_label = "SupplInf <supplinf>"
    acceptable_tags = ["supplinf"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_supplinf.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def get_children(self, widget):
        """
        This is actually getting handled in the Abstract widget

        """
        return []

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        supplinf element tag in xml tree
        """
        supplinf_text = self.ui.fgdc_supplinf.toPlainText()
        supplinf = xml_utils.xml_node("supplinf", text=supplinf_text)
        return supplinf

    def from_xml(self, supplinf):
        """
        parses the xml code into the relevant supplinf elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if supplinf.tag == "supplinf":
                try:
                    supplinf_text = supplinf.text
                    supplinf_box = self.findChild(QPlainTextEdit, "fgdc_supplinf")
                    supplinf_box.setPlainText(supplinf.text)
                except:
                    pass
            else:
                print("The tag is not supplinf")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(SupplInf, "SupplInf testing")
