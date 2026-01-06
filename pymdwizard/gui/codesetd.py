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
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_codesetd
except ImportError as err:
    raise ImportError(err, __file__)


class Codesetd(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "codeset domain" ("codesetd")
        metadata element. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the user interface for codeset name and source, handles
        data extraction to XML, and parsing from XML.

    Notes:
        None
    """

    # Class attributes
    drag_label = "Codeset Domain <codesetd>"
    acceptable_tags = ["codesetd"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI elements and sets up drag-and-drop
            functionality.

        Notes:
            Assumes UI_codesetd and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_codesetd.Ui_fgdc_attrdomv()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Encapsulate the UI content into an XML "codesetd" element
            tag.

        Passed arguments:
            None

        Returned objects:
            codesetd (xml.etree.ElementTree.Element): Codeset domain
                element tag in XML tree.

        Workflow:
            Creates the "codesetd" parent node and appends the "codesetn"
            (name) and "codesets" (source) children.

        Notes:
            Assumes `xml_utils.xml_node` is available.
        """

        # Create the parent "codesetd" XML node.
        codesetd = xml_utils.xml_node("codesetd")

        # Create and append the "codesetn" (Code set name) node.
        xml_utils.xml_node(
            "codesetn",
            text=self.ui.fgdc_codesetn.currentText(),
            parent_node=codesetd,
        )
        # Create and append the 'codesets' (Code set source) node.
        xml_utils.xml_node(
            "codesets",
            text=self.ui.fgdc_codesets.text(),
            parent_node=codesetd,
        )

        return codesetd

    def from_xml(self, codesetd):
        """
        Description:
            Parse the XML code into the relevant codeset domain elements.

        Passed arguments:
            codesetd (xml.etree.ElementTree.Element): The XML element
                containing the codeset domain details.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is "codesetd".
            2. Extract and set the text for "codesetn" and "codesets"
               UI fields.
            3. Handles potential XML parsing errors gracefully.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected "codesetd".
            if codesetd.tag == "codesetd":
                # Set the combo box text from the "codesetn" child.
                self.ui.fgdc_codesetn.setCurrentText(
                    codesetd.xpath("codesetn")[0].text
                )
                # Set the line edit text from the "codesets" child.
                self.ui.fgdc_codesets.setText(
                    codesetd.xpath("codesets")[0].text
                )
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not codesetd")
        except KeyError:
            # Handle if child elements are missing.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Codesetd, "udom testing")
