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
    from pymdwizard.gui.ui_files import UI_logic
except ImportError as err:
    raise ImportError(err, __file__)


class LogicalAccuracy(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "Logical Consistency Report"
        ("logic") metadata element, which describes the integrity and
        consistency of the data. Inherits from WizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Initializes the UI and sets up drag-and-drop. Provides methods
        to convert the widget's text content to a <logic> XML node and
        to populate the widget from an existing XML node.

    Notes:
        Uses "QPlainTextEdit" for multiline text input.
    """

    # Class attributes.
    drag_label = "Logical Accuracy <logic>"
    acceptable_tags = ["logic"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates the UI, sets up the components, and initializes
            drag-and-drop.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_logic.Ui_Form()
        self.ui.setupUi(self)

        # Setup drag-and-drop functionality.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Encapsulates the QPlainTextEdit text into a single "logic"
            XML element tag.

        Passed arguments:
            None

        Returned objects:
            logic (xml.etree.ElementTree.Element): Logical accuracy
                element tag in XML tree.

        Workflow:
            1. Creates the <logic> parent node.
            2. Finds the "fgdc_logic" text box.
            3. Sets the node's text to the content of the text box.

        Notes:
            None
        """

        # Create the parent "logic" XML node.
        logic = xml_utils.xml_node(tag="logic")

        # Find the QPlainTextEdit widget by object name and get its text.
        logic.text = self.findChild(
            QPlainTextEdit, "fgdc_logic"
        ).toPlainText()

        return logic

    def from_xml(self, logical_accuracy):
        """
        Description:
            Parses the XML code into the relevant logical consistency
            report text box.

        Passed arguments:
            logical_accuracy (ElementTree.Element): The XML element
                containing the logical consistency information.

        Returned objects:
            None

        Workflow:
            1. Checks for the correct <logic> tag.
            2. Finds the target "QPlainTextEdit" widget.
            3. Sets the widget's content to the text of the XML node.

        Notes:
            None
        """

        try:
            if logical_accuracy.tag == "logic":
                # Find the target text box by object name.
                accost_box = self.findChild(QPlainTextEdit,
                                            "fgdc_logic")

                # Set the text box content from the XML node's text.
                accost_box.setPlainText(logical_accuracy.text)
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not logic")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(LogicalAccuracy, "Logical Accuracy testing")
