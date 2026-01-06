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
    from pymdwizard.gui.ui_files import UI_Descriptor
except ImportError as err:
    raise ImportError(err, __file__)


class Descriptor(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "description" ("descript")
        metadata element, including abstract, purpose, and
        supplemental information. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages UI elements for the descriptive text fields, handles
        data extraction to XML, parsing from XML, and drag-and-drop
        functionality.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Descriptor <descript>"
    acceptable_tags = ["descript"]

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
            Assumes UI_Descriptor and setup_dragdrop are available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_Descriptor.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Encapsulates the QPlainTextEdit text fields into a single
            "descript" element tag.

        Passed arguments:
            None

        Returned objects:
            descript (xml.etree.ElementTree.Element): Description
                element tag in XML tree.

        Workflow:
            Creates the <descript> parent node, then extracts text for
            <abstract>, <purpose>, and <supplinf> (if present)
            to create child nodes.

        Notes:
            Assumes "xml_utils.xml_node" and "findChild" are available.
        """

        # Create the parent "descript" XML node.
        descript = xml_utils.xml_node(tag="descript")

        # Create and append the "abstract" node.
        abstract = xml_utils.xml_node(tag="abstract")
        abstract.text = self.findChild(QPlainTextEdit,
                                       "fgdc_abstract").toPlainText()
        descript.append(abstract)

        # Create and append the "purpose" node.
        purpose = xml_utils.xml_node(tag="purpose")
        purpose.text = self.findChild(QPlainTextEdit,
                                      "fgdc_purpose").toPlainText()
        descript.append(purpose)

        # Get the "supplinf" text.
        supplinf_str = self.ui.fgdc_supplinf.toPlainText()
        if supplinf_str:
            upplinf = xml_utils.xml_node(
                "supplinf", text=supplinf_str, parent_node=descript
            )

        return descript

    def from_xml(self, descriptors):
        """
        Description:
            Parse the XML code into the relevant descriptive elements.

        Passed arguments:
            descriptors (xml.etree.ElementTree.Element): The XML
                element containing the description details.

        Returned objects:
            None

        Workflow:
            1. Check if the element tag is "descript".
            2. Attempt to parse <abstract>, <purpose>, and <supplinf> by index.
            3. Uses a nested "except" to handle cases where <supplinf>
               is missing.

        Notes:
            The original docstring mentioned "access_constraints" which
            was replaced with "descriptors" for relevance.
        """

        try:
            # Check if the element tag matches the expected "descript".
            if descriptors.tag == "descript":
                # Attempt to parse abstract, purpose, and supplinf.
                try:
                    # Abstract
                    abstract = descriptors[0]
                    abstract_text = abstract.text
                    abstract_box = self.findChild(QPlainTextEdit,
                                                  "fgdc_abstract")
                    abstract_box.setPlainText(abstract.text)
                except KeyError:
                    pass

                try:
                    # Purpose
                    purpose = descriptors[1]
                    purpose_text = purpose.text
                    purpose_box = self.findChild(QPlainTextEdit,
                                                 "fgdc_purpose")
                    purpose_box.setPlainText(purpose.text)
                except KeyError:
                    pass

                try:
                    # Supplemental info (optional).
                    supplinf = descriptors[2]
                    supplinf_text = supplinf.text
                    supplinf_box = self.findChild(QPlainTextEdit,
                                                  "fgdc_supplinf")
                    supplinf_box.setPlainText(supplinf.text)
                except KeyError:
                    pass
            else:
                print("The tag is not descript")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Descriptor, "Descriptor testing")
