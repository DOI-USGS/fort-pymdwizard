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
    from pymdwizard.gui.ui_files import UI_abstract
except ImportError as err:
    raise ImportError(err, __file__)


class Abstract(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "abstract" metadata element.
        Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the user interface for the abstract text, handles
        data extraction to XML, and parsing from XML.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Abstract <abstract>"
    acceptable_tags = ["abstract"]

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
            Assumes UI_abstract and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_abstract.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)


    def get_children(self, widget):
        """
        Description:
            Return a list of widget's children, including related
            FGDC metadata widgets (supplinf and purpose).

        Passed arguments:
            widget (QWidget): The widget whose children are to be returned.

        Returned objects:
            children (list): List of child widgets and related widgets.

        Workflow:
            1. Find the main abstract text box.
            2. Traverse up the parent chain to find the 'fgdc_idinfo'
               container.
            3. Append related widgets (supplinf, purpose) from the
               'fgdc_idinfo' container.

        Notes:
            None
        """

        # Initialize the list of children.
        children = []

        # Add the primary abstract text field.
        children.append(self.ui.fgdc_abstract)

        # Traverse the parent hierarchy to find the 'fgdc_idinfo' parent
        parent = self.parent()
        while parent.objectName() != "fgdc_idinfo":
            parent = parent.parent()

        # Add related information widgets from the parent (fgdc_idinfo).
        children.append(parent.supplinf.ui.fgdc_supplinf)
        children.append(parent.purpose.ui.fgdc_purpose)

        return children


    def to_xml(self):
        """
        Description:
            Encapsulate the QPlainTextEdit text in an 'abstract' element tag.

        Passed arguments:
            None

        Returned objects:
            abstract (xml.etree.ElementTree.Element): Abstract element tag
                in XML tree.

        Workflow:
            Extracts text from the UI box and wraps it in an XML element.

        Notes:
            Assumes xml_utils.xml_node is a function to create an
            ElementTree.Element with text content.
        """

        # Create the 'abstract' XML node with the text content.
        abstract = xml_utils.xml_node(
            "abstract", text=self.ui.fgdc_abstract.toPlainText()
        )

        return abstract


    def from_xml(self, abstract):
        """
        Description:
            Parse the XML code into the relevant abstract element.

        Passed arguments:
            abstract (xml.etree.ElementTree.Element): The XML element
                containing the abstract text.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is 'abstract'.
            2. Extract the text content.
            3. Find the corresponding UI text box.
            4. Set the text box content.
            5. Handles potential XML parsing and UI errors gracefully.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected "abstract".
            if abstract.tag == "abstract":
                try:
                    # Retrieve text.
                    abstract_text = abstract.text

                    # Locate the specific QPlainTextEdit widget by name.
                    abstract_box = self.findChild(
                        QPlainTextEdit, "fgdc_abstract"
                    )

                    # Set the extracted text to the UI widget
                    abstract_box.setPlainText(abstract_text)
                except:
                    # Handle if the element is not found.
                    pass
            else:
                # Print a message if the tag is incorrect
                print("The tag is not abstract.")
        except KeyError:
            # Handle if the element is not found.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Abstract, "Abstract testing")
