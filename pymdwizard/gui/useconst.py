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
    from pymdwizard.gui.ui_files import UI_useconst
except ImportError as err:
    raise ImportError(err, __file__)


class Useconst(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <useconst> tag (Use
        Constraints), used to describe the restrictions and legal
        prerequisites for using the data set.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Provides a multiline text field ("QPlainTextEdit") for the
           user to enter use constraints.
        2. Handles serialization to and deserialization from the
           <useconst> XML tag.

    Notes:
        Inherits from "WizardWidget". The constraints description is
        free-form text.
    """

    # Class attributes.
    drag_label = "Use Constraints <useconst>"
    acceptable_tags = ["useconst"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI and enables drag-and-drop.

        Notes:
            None
        """

        self.ui = UI_useconst.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Converts the text content into an FGDC <useconst> XML
            element.

        Passed arguments:
            None

        Returned objects:
            useconst (lxml.etree._Element): The <useconst> element
                tag in the XML tree.

        Workflow:
            Creates a single XML node with the element name "useconst"
            and the text content from the widget.

        Notes:
            None
        """

        # Create the <useconst> node with the text content.
        useconst = xml_utils.xml_node(
            "useconst", text=self.ui.fgdc_useconst.toPlainText()
        )

        return useconst

    def from_xml(self, useconst):
        """
        Description:
            Parses an XML element and populates the widget fields.

        Passed arguments:
            useconst (lxml.etree._Element): The XML element, expected
                to be <useconst>.

        Returned objects:
            None

        Workflow:
            Checks for the correct tag and sets the text content of the
            widget using the XML node's text.

        Notes:
            None
        """

        try:
            if useconst.tag == "useconst":
                # Populate the widget's text field with XML content.
                self.ui.fgdc_useconst.setPlainText(useconst.text)
            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not useconst")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Useconst, "Use Constraints testing")
