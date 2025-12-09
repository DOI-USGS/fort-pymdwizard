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
    from pymdwizard.gui.ui_files import UI_purpose
except ImportError as err:
    raise ImportError(err, __file__)


class Purpose(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <purpose> tag, which
        describes the rationale or goal for which the data set was
        developed.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        Manages a single QPlainTextEdit field for the purpose
        description, handling its XML serialization and
        deserialization.

    Notes:
        Inherits from "WizardWidget". The "get_children" method is
        intentionally minimal as content handling is simple.
    """

    # Class attributes.
    drag_label = "Purpose <purpose>"
    acceptable_tags = ["purpose"]

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

        self.ui = UI_purpose.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def get_children(self, widget):
        """
        Description:
            Returns a list of child widgets for traversal.

        Passed arguments:
            widget: Ignored; typically the parent widget.

        Returned objects:
            list: An empty list, as this widget holds no complex
                  children relevant for standard XML traversal.

        Workflow:
            Returns an empty list.

        Notes:
            This function is primarily handled in the Abstract widget.
        """

        return []

    def to_xml(self):
        """
        Description:
            Encapsulates the text content of the widget into an FGDC
            <purpose> XML element.

        Passed arguments:
            None

        Returned objects:
            purpose (lxml.etree._Element): The <purpose> element tag
                in the XML tree.

        Workflow:
            Creates an XML node with the tag "purpose" and the
            QPlainTextEdit's content as its text.

        Notes:
            None
        """

        # Create the <purpose> XML node with the widget's text content.
        purpose = xml_utils.xml_node(
            "purpose", text=self.ui.fgdc_purpose.toPlainText()
        )

        return purpose

    def from_xml(self, purpose):
        """
        Description:
            Parses an XML element and populates the widget's text field
            with the content of the <purpose> tag.

        Passed arguments:
            purpose (lxml.etree._Element): The XML element, expected to
                be <purpose>.

        Returned objects:
            None

        Workflow:
            1. Checks if the tag is <purpose>.
            2. Extracts the text content and sets it in the
               "fgdc_purpose" QPlainTextEdit.

        Notes:
            Uses a nested try/except block to handle missing elements.
        """

        try:
            # Check if the element tag matches the expected tag.
            if purpose.tag == "purpose":
                try:
                    # Extract the text content from the element.
                    purpose_text = purpose.text

                    # Find the QPlainTextEdit widget by object name.
                    purpose_box = self.findChild(QPlainTextEdit,
                                                 "fgdc_purpose")

                    # Set the extracted text into the widget.
                    purpose_box.setPlainText(purpose_text)
                except:
                    pass
            else:
                # Output a message if the tag is incorrect.
                print("The tag is not purpose")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Purpose, "Purpose testing")
