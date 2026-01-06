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
    from pymdwizard.gui.ui_files import UI_udom
    from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
except ImportError as err:
    raise ImportError(err, __file__)


class Udom(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <udom> tag (Unrepresentable
        Domain), used to describe the domain of an attribute when the
        domain cannot be expressed using a code, enumerated list, or
        range of values.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Provides a multiline text field ("QPlainTextEdit") for the
           user to describe the attribute domain.
        2. Applies syntax highlighting (if "Highlighter" is available).
        3. Handles serialization to and deserialization from the <udom>
           XML tag.

    Notes:
        Inherits from "WizardWidget". The domain description is free-form
        text.
    """

    # Class attributes.
    drag_label = "Unrepresentable Domain <udom>"
    acceptable_tags = ["udom"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, enables drag-and-drop, and applies a syntax
            highlighter to the text input field.

        Notes:
            None
        """

        self.ui = UI_udom.Ui_fgdc_attrdomv()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Apply syntax highlighting to the multiline text box.
        self.highlighter = Highlighter(self.ui.fgdc_udom.document())

    def to_xml(self):
        """
        Description:
            Converts the text content into an FGDC <udom> XML element.

        Passed arguments:
            None

        Returned objects:
            udom (lxml.etree._Element): The <udom> element tag in
                the XML tree.

        Workflow:
            Creates a single XML node with the element name "udom" and
            the text content from the widget.

        Notes:
            None
        """

        # Create the <udom> node with the text content.
        udom = xml_utils.xml_node(
            "udom", self.ui.fgdc_udom.toPlainText()
        )

        return udom

    def from_xml(self, udom):
        """
        Description:
            Parses an XML element and populates the widget fields.

        Passed arguments:
            udom (lxml.etree._Element): The XML element, expected to be
                <udom>.

        Returned objects:
            None

        Workflow:
            Checks for the correct tag and uses "utils.populate_widget"
            to set the text content.

        Notes:
            None
        """

        try:
            if udom.tag == "udom":
                # Populate the widget's text field with XML content.
                utils.populate_widget(self, udom)
            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Udom, "udom testing")
