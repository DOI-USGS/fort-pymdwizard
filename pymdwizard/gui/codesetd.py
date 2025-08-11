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

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_codesetd
except ImportError as err:
    raise ImportError(err, __file__)


class Codesetd(WizardWidget):  #

    drag_label = "Codeset Domain <codesetd>"
    acceptable_tags = ["codesetd"]

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_codesetd.Ui_fgdc_attrdomv()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        codesetd = xml_utils.xml_node("codesetd")
        codesetn = xml_utils.xml_node(
            "codesetn", text=self.ui.fgdc_codesetn.currentText(), parent_node=codesetd
        )
        codesetn = xml_utils.xml_node(
            "codesets", text=self.ui.fgdc_codesets.text(), parent_node=codesetd
        )
        return codesetd

    def from_xml(self, codesetd):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if codesetd.tag == "codesetd":
                self.ui.fgdc_codesetn.setCurrentText(codesetd.xpath("codesetn")[0].text)
                self.ui.fgdc_codesets.setText(codesetd.xpath("codesets")[0].text)
            else:
                print("The tag is not codesetd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Codesetd, "udom testing")
