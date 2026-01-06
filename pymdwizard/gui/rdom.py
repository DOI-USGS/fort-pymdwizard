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
    from pymdwizard.core import (utils, xml_utils)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_rdom
except ImportError as err:
    raise ImportError(err, __file__)

class Rdom(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <rdom> tag, which is part
        of <attrdomv> (Attribute Domain Values) and specifies a range
        of attribute values.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        Manages fields for minimum value ("rdommin"), maximum value
        ("rdommax"), attribute unit ("attrunit"), and attribute resolution
        ("attrmres"), handling their XML serialization and
        deserialization.

    Notes:
        Inherits from "WizardWidget". The class name "Rdom" is a short
        form for Range Domain.
    """

    # Class attributes.
    drag_label = "Range Domain <rdom>"
    acceptable_tags = ["rdom"]

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

        self.ui = UI_rdom.Ui_fgdc_attrdomv()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <rdom> XML
            element, including its nested components.

        Passed arguments:
            None

        Returned objects:
            rdom (lxml.etree._Element): The <rdom> element tag
                in the XML tree.

        Workflow:
            1. Creates the root <rdom> node.
            2. Appends <rdommin> and <rdommax> (required).
            3. Appends <attrunit> and <attrmres> only if they contain text.

        Notes:
            None
        """

        # Create the root <rdom> node.
        rdom = xml_utils.xml_node("rdom")

        # Range Domain Minimum (<rdommin>).
        xml_utils.xml_node(
            "rdommin",
            text=self.ui.fgdc_rdommin.text(),
            parent_node=rdom,
        )

        # Range Domain Maximum (<rdommax>).
        xml_utils.xml_node(
            "rdommax",
            text=self.ui.fgdc_rdommax.text(),
            parent_node=rdom,
        )

        # Attribute Unit (<attrunit>) - optional.
        if self.ui.fgdc_attrunit.text():
            xml_utils.xml_node(
                "attrunit",
                text=self.ui.fgdc_attrunit.text(),
                parent_node=rdom,
            )

        # Attribute Measurement Resolution (<attrmres>) - optional.
        if self.ui.fgdc_attrmres.text():
            xml_utils.xml_node(
                "attrmres",
                text=self.ui.fgdc_attrmres.text(),
                parent_node=rdom,
            )

        return rdom

    def from_xml(self, rdom):
        """
        Description:
            Parses an XML element and populates the widget's fields.

        Passed arguments:
            rdom (lxml.etree._Element): The XML element, expected to
                be <rdom>.

        Returned objects:
            None

        Workflow:
            1. Checks if the tag is <rdom>.
            2. Uses a utility function to populate the fields based on
               matching object names.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected tag.
            if rdom.tag == "rdom":
                # Populate fields based on matching XML tags and widget names.
                utils.populate_widget(self, rdom)
            else:
                # Output a message if the tag is incorrect.
                print("The tag is not rdom")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Rdom, "udom testing")
