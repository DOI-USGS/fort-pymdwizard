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
    from pymdwizard.gui.ui_files import UI_supplinf
except ImportError as err:
    raise ImportError(err, __file__)


class SupplInf(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <supplinf> tag, which
        contains any supplementary information about the metadata
        record not included elsewhere.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Manages a single "QPlainTextEdit" field for multi-line
           supplementary text.
        2. Handles XML serialization/deserialization for the <supplinf> tag.

    Notes:
        Inherits from "WizardWidget". The "get_children" method is
        redundant because this widget is a leaf node.
    """

    # Class attributes.
    drag_label = "SupplInf <supplinf>"
    acceptable_tags = ["supplinf"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI and sets up drag-and-drop.

        Notes:
            None
        """

        self.ui = UI_supplinf.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def get_children(self, widget):
        """
        Description:
            Returns a list of this widget's children, which are empty
            since this is typically a leaf node.

        Passed arguments:
            widget (object): Reference to the current widget instance.

        Returned objects:
            list: An empty list.

        Workflow:
            Directly returns an empty list.

        Notes:
            This method is generally handled by the abstract base widget
            but is included here for completeness.
        """

        # This is a leaf node, so it has no relevant children to return.
        return []

    def to_xml(self):
        """
        Description:
            Encapsulates the text content of the "QPlainTextEdit" into a
            <supplinf> element tag.

        Passed arguments:
            None

        Returned objects:
            supplinf (lxml.etree._Element): The <supplinf> element
                tag in the XML tree.

        Workflow:
            1. Retrieves text from "fgdc_supplinf".
            2. Creates and returns the <supplinf> node with text.

        Notes:
            None
        """

        # Get text content from the plain text editor.
        supplinf_text = self.ui.fgdc_supplinf.toPlainText()

        # Create the <supplinf> node with the extracted text.
        supplinf = xml_utils.xml_node("supplinf", text=supplinf_text)

        return supplinf

    def from_xml(self, supplinf):
        """
        Description:
            Parses an XML element and populates the supplementary
            information text area.

        Passed arguments:
            supplinf (lxml.etree._Element): The XML element, expected
                to be <supplinf>.

        Returned objects:
            None

        Workflow:
            1. Checks for the <supplinf> tag.
            2. Extracts the element's text content.
            3. Sets the extracted text into the "QPlainTextEdit".

        Notes:
            Fails silently on errors during text extraction/setting.
        """

        try:
            if supplinf.tag == "supplinf":
                try:
                    # Get the text directly from the XML element.
                    supplinf_text = supplinf.text

                    # Find the QPlainTextEdit widget by object name.
                    supplinf_box = self.findChild(
                        QPlainTextEdit, "fgdc_supplinf"
                    )

                    # Set the text into the widget.
                    supplinf_box.setPlainText(supplinf.text)
                except:
                    # Silently ignore errors during text population.
                    pass
            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not supplinf")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SupplInf, "SupplInf testing")
