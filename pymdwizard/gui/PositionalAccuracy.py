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
    from pymdwizard.gui.ui_files import UI_posacc
except ImportError as err:
    raise ImportError(err, __file__)


class PositionalAccuracy(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <posacc> tag, which describes
        the positional accuracy of a spatial data set. It includes fields
        for horizontal and vertical positional accuracy reports.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        Manages two QPlainTextEdit fields ("fgdc_horizpa" and
        "fgdc_vertacc") and handles their translation to the nested
        <horizpa>/<horizpar> and <vertacc>/<vertaccr> XML structure.

    Notes:
        Inherits from "WizardWidget".
    """

    # Class attributes.
    drag_label = "Positional Accuracy <possacc>"
    acceptable_tags = ["posacc"]

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

        self.ui = UI_posacc.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)


    def has_content(self):
        """
        Description:
            Checks for valid content in this widget by determining if
            either the horizontal or vertical accuracy fields contain text.

        Passed arguments:
            None

        Returned objects:
            bool: True if either field has content, False otherwise.

        Workflow:
            Checks the text content of "fgdc_horizpa" and "fgdc_vertacc".

        Notes:
            None
        """

        # Assume no content initially.
        has_content = False

        # Check for text in horizontal accuracy field.
        if self.ui.fgdc_horizpa.toPlainText():
            has_content = True

        # Check for text in vertical accuracy field.
        if self.ui.fgdc_vertacc.toPlainText():
            has_content = True

        return has_content

    def to_xml(self):
        """
        Description:
            Encapsulates the text content into the nested FGDC
            <posacc> XML element structure.

        Passed arguments:
            None

        Returned objects:
            possacc (lxml.etree._Element): The <posacc> element tag
                in the XML tree.

        Workflow:
            1. Creates the root <posacc> node.
            2. For horizontal accuracy, if text exists, creates
               <horizpa> and <horizpar> and appends them.
            3. For vertical accuracy, if text exists, creates
               <vertacc> and <vertaccr> and appends them.

        Notes:
            Uses "findChild" to access the QPlainTextEdit widgets.
        """

        # Create the root <posacc> node.
        possacc = xml_utils.xml_node(tag="posacc")

        # --- Horizontal Positional Accuracy (<horizpa>) ---
        horizpa = xml_utils.xml_node(tag="horizpa")
        horizpar = xml_utils.xml_node(tag="horizpar")

        # Access the horizontal text field using its object name.
        horizpar_text = self.findChild(QPlainTextEdit,
                                       "fgdc_horizpa").toPlainText()

        # Append nodes if content exists.
        if len(horizpar_text) > 0:
            horizpar.text = horizpar_text
            horizpa.append(horizpar)
            possacc.append(horizpa)

        # --- Vertical Positional Accuracy (<vertacc>) ---
        vertacc = xml_utils.xml_node(tag="vertacc")
        vertaccr = xml_utils.xml_node(tag="vertaccr")

        # Access the vertical text field using its object name.
        vertaccr_text = self.findChild(QPlainTextEdit,
                                       "fgdc_vertacc").toPlainText()

        # Append nodes if content exists.
        if len(vertaccr_text) > 0:
            vertaccr.text = vertaccr_text
            vertacc.append(vertaccr)
            possacc.append(vertacc)

        return possacc

    def from_xml(self, positional_accuracy):
        """
        Description:
            Parses an XML element and populates the widget's text fields
            with the horizontal and vertical positional accuracy reports.

        Passed arguments:
            positional_accuracy (lxml.etree._Element): The XML element,
                expected to be <posacc>.

        Returned objects:
            None

        Workflow:
            1. Checks if the tag is <posacc>.
            2. Uses `findtext` to extract the text from the nested
               <horizpa>/<horizpar> and <vertacc>/<vertaccr> paths.
            3. Sets the text content of the corresponding QPlainTextEdit
               widgets.

        Notes:
            Fails silently on "KeyError".
        """

        try:
            # Check if the element tag matches the expected tag.
            if positional_accuracy.tag == "posacc":
                # Extract horizontal accuracy text.
                horizpa_text = positional_accuracy.findtext("horizpa/horizpar")
                horizpa_box = self.findChild(QPlainTextEdit,
                                             "fgdc_horizpa")
                horizpa_box.setPlainText(horizpa_text)

                # Extract vertical accuracy text.
                vertacc_text = positional_accuracy.findtext("vertacc/vertaccr")
                vertacc_box = self.findChild(QPlainTextEdit,
                                             "fgdc_vertacc")
                vertacc_box.setPlainText(vertacc_text)
            else:
                # Output a message if the tag is incorrect.
                print("The tag is not possacc")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(PositionalAccuracy, "Positional Accuracy testing")
