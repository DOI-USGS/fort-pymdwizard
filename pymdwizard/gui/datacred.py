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
from pymdwizard.gui.ui_files import UI_datacred


class Datacred(WizardWidget):  #

    drag_label = "Data Credit <datacred>"
    acceptable_tags = ["datacred"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_datacred.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'datacred'
        Parameters
        ----------
        e : qt event

        Returns
        -------
        None

        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat("text/plain"):
            element = xml_utils.string_to_node(mime_data.text())
            if element is not None and element.tag == "datacred":
                e.accept()
        else:
            e.ignore()

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        datacred element tag in xml tree
        """
        datacred = xml_utils.xml_node(
            "datacred", text=self.ui.fgdc_datacred.toPlainText()
        )
        return datacred

    def from_xml(self, data_credit):
        """
        parses the xml code into the relevant datacred elements

        Parameters
        ----------
        data_credit - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if data_credit.tag == "datacred":
                self.ui.fgdc_datacred.setPlainText(data_credit.text)
            else:
                print("The tag is not datacred")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Datacred, "Data Credit testing")
