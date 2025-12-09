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
    from PyQt5.QtWidgets import QWidget
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.ui_files import UI_edom
except ImportError as err:
    raise ImportError(err, __file__)


class Edom(QWidget):  #
    """
    Description:
        A widget for managing the FGDC "enumerated domain" ("edom")
        metadata element. This specifies a valid value, its definition,
        and the definition source. Inherits from QWidget.

    Passed arguments:
        xml (ElementTree.Element, optional): The XML element to parse.
        parent (QWidget, optional): Parent widget.
        item (object, optional): Reference to a related item (e.g.,
            the parent attribute).

    Returned objects:
        None

    Workflow:
        Initializes the UI, sets up size constraints for the definition
        text box, and sets the default definition source text.

    Notes:
        The "dragEnterEvent" is explicitly set to ignore all drag-and-
        drop input.
    """

    # Class attributes.
    drag_label = "Enumerated Domain <edom>"
    acceptable_tags = ["edom"]

    def __init__(self, xml=None, parent=None, item=None):
        # Initialize the parent QWidget class.
        QWidget.__init__(self, parent=parent)
        self.item = item
        self.build_ui()

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, links the item to the definition widget,
            sets min/max heights for the definition text box, triggers
            a size change, and sets the default definition source text.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_edom.Ui_fgdc_attrdomv()
        self.ui.setupUi(self)

        # Link the item to the definition text box.
        self.ui.fgdc_edomvd.item = self.item

        # Set size constraints for the definition text box.
        self.ui.fgdc_edomvd.heightMin = 25
        self.ui.fgdc_edomvd.heightMax = 150

        # Trigger size update.
        self.ui.fgdc_edomvd.sizeChange()

        # Get the default source text from settings.
        defsource = utils.get_setting("defsource",
                                      "Producer defined")

        # Set the default source text.
        self.ui.fgdc_edomvds.setText(defsource)

    def dragEnterEvent(self, e):
        """
        Description:
            Ignores all drag-and-drop events for this widget.

        Passed arguments:
            e (QDragEnterEvent): The drag event object.

        Returned objects:
            None

        Workflow:
            Calls "e.ignore()" to prevent any dropped data from being
            accepted.

        Notes:
            None
        """

        # Ignore all dragged items
        e.ignore()

    def to_xml(self):
        """
        Description:
            Encapsulates the text fields into a single "edom" XML
            element tag.

        Passed arguments:
            None

        Returned objects:
            edom (xml.etree.ElementTree.Element): Enumerated domain
                element tag in XML tree.

        Workflow:
            Creates the <edom> parent node, and appends <edomv>
            (value), <edomvd> (definition), and <edomvds> (source).

        Notes:
            Assumes "xml_utils.xml_node" is available.
        """

        # Create the parent "edom" XML node.
        edom = xml_utils.xml_node("edom")

        # Create <edomv> (Enumerated Domain Value).
        xml_utils.xml_node(
            "edomv", text=self.ui.fgdc_edomv.text(), parent_node=edom
        )

        # Create <edomvd> (Enumerated Domain Definition).
        xml_utils.xml_node(
            "edomvd", text=self.ui.fgdc_edomvd.toPlainText(),
            parent_node=edom
        )

        # Create <edomvds> (Enumerated Domain Definition Source).
        xml_utils.xml_node(
            "edomvds", text=self.ui.fgdc_edomvds.text(), parent_node=edom
        )

        return edom

    def from_xml(self, edom):
        """
        Description:
            Parse the XML code into the relevant enumerated domain
            elements.

        Passed arguments:
            edom (xml.etree.ElementTree.Element): The XML element
                containing the enumerated domain details.

        Returned objects:
            None

        Workflow:
            1. Check for the "edom" tag.
            2. Clears any existing definition source text.
            3. Populates the widget fields using the utility function.

        Notes:
            None
        """

        try:
            if edom.tag == "edom":
                # Clear the definition source text field before populating.
                self.ui.fgdc_edomvds.setText("")

                # Populate all simple fields from the XML node.
                utils.populate_widget(self, edom)
            else:
                print("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Edom, "edom testing")
