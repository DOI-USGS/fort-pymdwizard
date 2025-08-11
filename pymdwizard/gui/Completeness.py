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
    from pymdwizard.gui.ui_files import UI_complete
except ImportError as err:
    raise ImportError(err, __file__)


class Completeness(WizardWidget):  #

    drag_label = "Completeness <complete>"
    acceptable_tags = ["complete"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_complete.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        complete element tag in xml tree
        """
        complete = xml_utils.xml_node(
            tag="complete",
            text=self.findChild(QPlainTextEdit, "fgdc_complete").toPlainText(),
        )

        return complete

    def from_xml(self, complete_ness):
        """
        parses the xml code into the relevant complete elements

        Parameters
        ----------
        complete_ness - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if complete_ness.tag == "complete":
                accost_box = self.findChild(QPlainTextEdit, "fgdc_complete")
                accost_box.setPlainText(complete_ness.text)
            else:
                print("The tag is not complete")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Completeness, "Completeness testing")
