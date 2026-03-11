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
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_accconst
except ImportError as err:
    raise ImportError(err, __file__)


class Accconst(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "access constraints" metadata
        element. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the user interface for the access constraints text,
        handles data extraction to XML, and parsing from XML.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Access Constraints <accconst>"
    acceptable_tags = ["accconst"]

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
            Assumes UI_accconst and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_accconst.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Encapsulate the QPlainTextEdit text in an 'accconst' element
            tag.

        Passed arguments:
            None

        Returned objects:
            accconst (xml.etree.ElementTree.Element): Access constraints
                element tag in XML tree.

        Workflow:
            Extracts text from the UI box and wraps it in an XML element.

        Notes:
            Assumes xml_utils.xml_node is a function to create an
            ElementTree.Element with text content.
        """

        # Create the "accconst" XML node with the text content.
        accconst = xml_utils.xml_node(
            "accconst", text=self.ui.fgdc_accconst.toPlainText()
        )

        return accconst

    def from_xml(self, acconst):
        """
        Description:
            Parse the XML code into the relevant accconst elements.

        Passed arguments:
            accconst (xml.etree.ElementTree.Element): The XML element
                containing the access constraints.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is 'accconst'.
            2. Extract the text content.
            3. Set the UI text box content.
            4. Handles potential XML parsing errors gracefully.

        Notes:
            Error handling uses bare `except` to silently pass on
            KeyError, consistent with the original code.
        """

        try:
            # Check if the element tag matches the expected "accconst".
            if acconst.tag == "accconst":
                # Set the extracted text to the UI widget.
                self.ui.fgdc_accconst.setPlainText(acconst.text)
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not accconst")
        except KeyError:
            # Handle if the element is not found/accessible.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Accconst, "Access Constraints testing")
