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

# Standard python libraries.
from copy import deepcopy

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QPlainTextEdit
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (xml_utils, utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_attracc
except ImportError as err:
    raise ImportError(err, __file__)


class AttributeAccuracy(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "attribute accuracy" metadata
        element. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the user interface for attribute accuracy text,
        handles data extraction to XML, and parsing from XML.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Attribute Accuracy <attracc>"
    acceptable_tags = ["attracc"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI elements, sets up drag-and-drop, and
            adjusts the height of the primary text box.

        Notes:
            Assumes UI_attracc and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_attracc.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

        # Adjust the height of the attribute accuracy report text box.
        self.ui.fgdc_attraccr.setFixedHeight(55)

    def to_xml(self):
        """
        Description:
            Encapsulates the QPlainTextEdit text in an "attracc'"element
            tag and potentially includes a "qattracc" element.

        Passed arguments:
            None

        Returned objects:
            attracc (xml.etree.ElementTree.Element): Attribute accuracy
                element tag in XML tree.

        Workflow:
            1. Create the parent "attracc" node.
            2. Get text from "fgdc_attraccr" and create its node as a
               child.
            3. If "self.original_xml" exists, find the "qattracc" node
               in it, deepcopy it, and append it to "attracc".

        Notes:
            Assumes xml_utils.xml_node and xml_utils.search_xpath are
            available. Uses `deepcopy` to prevent modifying the original
            XML structure.
        """

        # Create the parent "attracc" XML node.
        attracc = xml_utils.xml_node(tag="attracc")

        # Find the text from the UI widget.
        attraccr_str = self.findChild(
            QPlainTextEdit, "fgdc_attraccr"
        ).toPlainText()

        # Create and append the "attraccr" child node.
        attraccr = xml_utils.xml_node(
            tag="attraccr", text=attraccr_str, parent_node=attracc
        )

        # Check if original XML exists to search for "qattracc".
        if self.original_xml is not None:
            # Search for the optional "qattracc" (quantitative accuracy).
            qattracc = xml_utils.search_xpath(
                self.original_xml, "qattracc"
            )
            if qattracc is not None:
                # Remove the element tail if it exists.
                qattracc.tail = None

                # Deep copy and append the element to the new "attracc".
                attracc.append(deepcopy(qattracc))

        return attracc

    def from_xml(self, attribute_accuracy):
        """
        Description:
            Parse the XML code into the relevant "attraccr" elements.

        Passed arguments:
            attribute_accuracy (xml.etree.ElementTree.Element): The XML
                element containing the attribute accuracy.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is "attracc".
            2. Store the original XML element.
            3. Extract the text content of the "attraccr" child node.
            4. Find the corresponding UI text box.
            5. Set the text box content.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected "attracc".
            if attribute_accuracy.tag == "attracc":
                # Store the original element for use in to_xml().
                self.original_xml = attribute_accuracy

                # Find the text of the "attraccr" child element.
                attraccr_text = attribute_accuracy.findtext("attraccr")

                # Locate the specific QPlainTextEdit widget by name.
                accost_box = self.findChild(
                    QPlainTextEdit, "fgdc_attraccr"
                )

                # Set the extracted text to the UI widget.
                accost_box.setPlainText(attraccr_text)
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not attracc")
        except KeyError:
            # Handle if the element is not found/accessible.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(AttributeAccuracy, "Attribute Accuracy testing")
