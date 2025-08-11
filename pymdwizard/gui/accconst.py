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
files name.


NOTES
------------------------------------------------------------------------------
None
"""

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_accconst
except ImportError as err:
    raise ImportError(err, __file__)


class Accconst(WizardWidget):

    drag_label = "Access Constraints <accconst>"
    acceptable_tags = ["accconst"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_accconst.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        accconst element tag in xml tree
        """
        accconst = xml_utils.xml_node(
            "accconst", text=self.ui.fgdc_accconst.toPlainText()
        )
        return accconst

    def from_xml(self, acconst):
        """
        parses the xml code into the relevant accconst elements

        Parameters
        ----------
        acconst - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if acconst.tag == "accconst":
                self.ui.fgdc_accconst.setPlainText(acconst.text)
            else:
                print("The tag is not accconst")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Accconst, "Access Constraints testing")
