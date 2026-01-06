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
    from pymdwizard.gui.ui_files import UI_native
except ImportError as err:
    raise ImportError(err, __file__)

class Native(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <native> tag, which describes
        the native data set environment of the digital data.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        Manages a single QPlainTextEdit field for the native environment
        description, allowing for XML serialization and deserialization
        of this content.

    Notes:
        Inherits from "WizardWidget".
    """

    # Class attributes.
    drag_label = "Native data set environment <native>"
    acceptable_tags = ["native"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI class, calls "setupUi", and sets up
            drag-and-drop functionality.

        Notes:
            None
        """

        self.ui = UI_native.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def has_content(self):
        """
        Description:
            Checks if the widget contains any user-entered text.

        Passed arguments:
            None

        Returned objects:
            bool: True if the text field is not empty, False otherwise.

        Workflow:
            Compares the content of the QPlainTextEdit to an empty string.

        Notes:
            None
        """

        # Return True if the text content is not empty.
        return self.ui.fgdc_native.toPlainText() != ""

    def to_xml(self):
        """
        Description:
            Encapsulates the text content of the widget into an FGDC
            <native> XML element.

        Passed arguments:
            None

        Returned objects:
            native (lxml.etree._Element): The <native> element tag
                in the XML tree.

        Workflow:
            Creates an XML node with the tag "native" and the
            QPlainTextEdit's content as its text.

        Notes:
            None
        """

        # Create the <native> XML node with the widget's text content.
        native = xml_utils.xml_node("native",
                                    text=self.ui.fgdc_native.toPlainText())

        return native

    def from_xml(self, native):
        """
        Description:
            Parses an XML element and populates the widget's text field
            with the content of the <native> tag.

        Passed arguments:
            native (lxml.etree._Element): The XML element, expected to
                be <native>.

        Returned objects:
            None

        Workflow:
            1. Checks if the tag is <native>.
            2. Sets the QPlainTextEdit content to the element's text.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected tag.
            if native.tag == "native":
                # Set the text content of the QPlainTextEdit.
                self.ui.fgdc_native.setPlainText(native.text)
            else:
                # Output a message if the tag is incorrect.
                print("The tag is not native")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Native, "Access Constraints testing")
