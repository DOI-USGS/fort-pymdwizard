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
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_complete
except ImportError as err:
    raise ImportError(err, __file__)


class Completeness(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "completeness" metadata element.
        Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the user interface for the completeness text, handles
        data extraction to XML, and parsing from XML.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Completeness <complete>"
    acceptable_tags = ["complete"]

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
            Assumes UI_complete and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_complete.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Encapsulates the QPlainTextEdit text in a "complete" element
            tag.

        Passed arguments:
            None

        Returned objects:
            complete (xml.etree.ElementTree.Element): Completeness
                element tag in XML tree.

        Workflow:
            Extracts text from the UI box and wraps it in an XML element.

        Notes:
            Assumes "xml_utils.xml_node" is available.
        """

        # Find the text from the UI widget and create the XML node.
        complete = xml_utils.xml_node(
            tag="complete",
            text=self.findChild(QPlainTextEdit,
                                "fgdc_complete").toPlainText(),
        )

        return complete

    def from_xml(self, complete_ness):
        """
        Description:
            Parse the XML code into the relevant completeness elements.

        Passed arguments:
            completeness (xml.etree.ElementTree.Element): The XML
                element containing the completeness report.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is "complete".
            2. Find the corresponding UI text box.
            3. Set the text box content using the XML element's text.

        Notes:
            The parameter name was updated from "complete_ness" to
            "completeness" for PEP 8 compliance.
        """

        try:
            # Check if the element tag matches the expected "complete".
            if complete_ness.tag == "complete":
                # Locate the specific QPlainTextEdit widget by name.
                accost_box = self.findChild(
                    QPlainTextEdit, "fgdc_complete"
                )
                # Set the extracted text to the UI widget.
                accost_box.setPlainText(complete_ness.text)
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not complete")
        except KeyError:
            # Handle if the element text is missing.
            pass

if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Completeness, "Completeness testing")
