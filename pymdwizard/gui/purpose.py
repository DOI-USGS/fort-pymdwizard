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
    from pymdwizard.gui.ui_files import UI_purpose
except ImportError as err:
    raise ImportError(err, __file__)


class Purpose(WizardWidget):

    drag_label = "Purpose <purpose>"
    acceptable_tags = ["purpose"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_purpose.Ui_Form()
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
        purpose element tag in xml tree
        """

        purpose = xml_utils.xml_node("purpose", text=self.ui.fgdc_purpose.toPlainText())

        return purpose

    def from_xml(self, purpose):
        """
        parses the xml code into the relevant purpose elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if purpose.tag == "purpose":
                try:

                    purpose_text = purpose.text
                    purpose_box = self.findChild(QPlainTextEdit, "fgdc_purpose")
                    purpose_box.setPlainText(purpose_text)
                except:
                    pass
            else:
                print("The tag is not purpose")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Purpose, "Purpose testing")
