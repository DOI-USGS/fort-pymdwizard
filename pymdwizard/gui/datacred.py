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
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_datacred
except ImportError as err:
    raise ImportError(err, __file__)


class Datacred(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "data credit" ("datacred")
        metadata element. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the user interface for the data credit text, handles
        data extraction to XML, parsing from XML, and drag-and-drop
        acceptance for "datacred" tags.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Data Credit <datacred>"
    acceptable_tags = ["datacred"]

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
            Assumes UI_datacred and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_datacred.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

    def dragEnterEvent(self, e):
        """
        Description:
            Handles incoming drag events, only accepting items that can
            be converted to an XML object with a root tag called
            "datacred".

        Passed arguments:
            e (QEvent): The drag event object.

        Returned objects:
            None

        Workflow:
            1. Check if the mime data contains plain text.
            2. Attempt to convert the text to an XML node.
            3. Accept the event only if the root tag is "datacred".

        Notes:
            None
        """

        mime_data = e.mimeData()

        # Check if the dropped data is plain text.
        if e.mimeData().hasFormat("text/plain"):

            # Attempt to convert the text to an XML node.
            element = xml_utils.string_to_node(mime_data.text())

            # Accept if the node exists and its tag is "datacred".
            if element is not None and element.tag == "datacred":
                e.accept()
        else:
            # Ignore all other formats.
            e.ignore()

    def to_xml(self):
        """
        Description:
            Encapsulates the QPlainTextEdit text in a "datacred" element
            tag.

        Passed arguments:
            None

        Returned objects:
            datacred (xml.etree.ElementTree.Element): Data credit
                element tag in XML tree.

        Workflow:
            Extracts text from the UI box and wraps it in an XML element.

        Notes:
            Assumes "xml_utils.xml_node" is available.
        """

        # Create the XML node using text from the QPlainTextEdit.
        datacred = xml_utils.xml_node(
            "datacred", text=self.ui.fgdc_datacred.toPlainText()
        )

        return datacred

    def from_xml(self, data_credit):
        """
        Description:
            Parse the XML code into the relevant data credit elements.

        Passed arguments:
            data_credit (xml.etree.ElementTree.Element): The XML
                element containing the data credit.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is "datacred".
            2. Set the UI text box content using the XML element's text.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected "datacred".
            if data_credit.tag == "datacred":
                # Set the extracted text to the UI widget.
                self.ui.fgdc_datacred.setPlainText(data_credit.text)
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not datacred")
        except KeyError:
            # Handle if the element text is missing.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Datacred, "Data Credit testing")
