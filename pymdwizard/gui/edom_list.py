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

# Standard python libraries.
import math

# Non-standard python libraries.
try:
    import pandas as pd
    from PyQt5.QtWidgets import (QListWidgetItem, QAbstractItemView)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_edom_list
    from pymdwizard.gui import edom
except ImportError as err:
    raise ImportError(err, __file__)


class EdomList(WizardWidget):  #
    """
    Description:
        A widget for managing a list of FGDC "enumerated domain"
        ("edom") elements. This list typically forms the domain values
        for a specific attribute. Inherits from WizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages a QListWidget where each item contains an instance of
        the "Edom" widget. Provides functionality to add, remove, and
        populate the list from a sequence of attribute values.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Enumerated Domain <edom>"

    # This widget handles <attrdomv> which is nested under <attr>.
    acceptable_tags = ["attr"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, sets up the list for Edom widgets, sets
            up drag-and-drop, and connects the add/delete buttons.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_edom_list.Ui_edom_contents()
        self.ui.setupUi(self)

        # List to hold references (though the QListWidget stores them).
        self.edoms = []

        # Initialize drag-and-drop features.
        self.setup_dragdrop(self)

        # Enable internal movement for drag-and-drop reordering.
        self.ui.listWidget.setDragDropMode(QAbstractItemView.InternalMove)

        # Connect button signals to methods.
        self.ui.btn_addone.clicked.connect(self.add_clicked)
        self.ui.btn_delete.clicked.connect(self.remove_selected)

    def populate_from_list(self, items):
        """
        Description:
            Populates the list widget with domain values derived from a
            list of unique items (e.g., a DataFrame column).

        Passed arguments:
            items (list): List of unique values from a data source.

        Returned objects:
            None

        Workflow:
            Clears the existing list, then iterates through the input
            items. Handles empty/null/NaN values by creating a special
            "<< empty cell >>" entry (if configured).

        Notes:
            None
        """

        # Reset the internal list and the UI list.
        self.edoms = []
        self.ui.listWidget.clear()

        # Iterate over unique values to create an Edom for each.
        for item_label in items:
            is_empty = (
                    pd.isnull(item_label)
                    or str(item_label) == ""
                    or (type(item_label) != str and math.isnan(item_label))
            )

            # Handle empty/null values
            if is_empty:
                # Check if the parent attribute has a custom nodata value.
                if not self.parent().nodata == "<< empty cell >>":
                    self.add_edom("<< empty cell >>")
            else:
                # Add the actual value as an enumerated domain.
                self.add_edom(str(item_label))

    def add_clicked(self):
        """
        Description:
            Wrapper method to add a new, empty enumerated domain.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls "add_edom" with default empty strings.

        Notes:
            None
        """

        self.add_edom()

    def remove_selected(self):
        """
        Description:
            Removes all selected items (Edom widgets) from the list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Iterates over the selected list items and removes them from
            the QListWidget.

        Notes:
            None
        """

        # Iterate over a copy of the selected items list.
        for item in self.ui.listWidget.selectedItems():
            # Remove the item from the QListWidget.
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def add_edom(self, edomv="", edomvd="", edomvds=""):
        """
        Description:
            Creates a new "Edom" widget, sets its initial values, and
            adds it to the QListWidget.

        Passed arguments:
            edomv (str): Enumerated domain value.
            edomvd (str): Enumerated domain definition.
            edomvds (str): Enumerated domain definition source.

        Returned objects:
            None

        Workflow:
            1. Creates a "QListWidgetItem" and an "Edom" widget.
            2. Sets the text content for the "Edom" widget.
            3. Sets the item's size hint based on the widget.
            4. Adds the item and then sets the "Edom" widget as the
               custom item widget.

        Notes:
            None
        """

        # Create a new list item container.
        item = QListWidgetItem()

        # Create an Edom widget instance, passing the item reference.
        e = edom.Edom(item=item)

        # Set initial values.
        e.ui.fgdc_edomv.setText(edomv)
        if edomvd:
            e.ui.fgdc_edomvd.setPlainText(edomvd)
        if edomvds:
            e.ui.fgdc_edomvds.setText(edomvds)

        # Ensure the list item is sized correctly for the widget.
        item.setSizeHint(e.sizeHint())

        # Add the item to the list.
        self.ui.listWidget.addItem(item)

        # Set the custom widget for the item.
        self.ui.listWidget.setItemWidget(item, e)

    def to_xml(self):
        """
        Description:
            Encapsulates the list of enumerated domains into a single
            'attr' element tag.

        Passed arguments:
            None

        Returned objects:
            attr (xml.etree.ElementTree.Element): The attribute element
                containing the enumerated domain list.

        Workflow:
            1. Creates the <attr> parent node.
            2. Iterates through the list of "Edom" widgets.
            3. For each "Edom", creates an <attrdomv> wrapper node.
            4. Appends the <edom> XML (generated by the "Edom" widget)
               to the <attrdomv> node.

        Notes:
            Assumes "xml_utils.xml_node" and "Edom.to_xml()" are
            available.
        """

        # Create the parent "attr" XML node.
        attr = xml_utils.xml_node("attr")

        # Iterate through every item in the QListWidget.
        for i in range(self.ui.listWidget.count()):
            e = self.ui.listWidget.item(i)

            # Get the actual Edom widget instance.
            e2 = self.ui.listWidget.itemWidget(e)

            # Create the <attrdomv> wrapper node.
            attrdomv = xml_utils.xml_node("attrdomv", parent_node=attr)

            # Get the <edom> node from the widget.
            e_node = e2.to_xml()

            # Append the <edom> node to <attrdomv>.
            attrdomv.append(e_node)

        return attr

    def from_xml(self, attr):
        """
        Description:
            Parses the XML code into the list of enumerated domain
            widgets.

        Passed arguments:
            attr (xml.etree.ElementTree.Element): The XML element
                containing the attribute information.

        Returned objects:
            None

        Workflow:
            1. Checks for the "attr" tag.
            2. Clears the existing list.
            3. Finds all <edom> nodes nested under <attrdomv>.
            4. Converts each <edom> node to a dictionary and calls
               "add_edom" to populate a new widget with the data.

        Notes:
            Assumes "xml_utils.node_to_dict" is available.
        """

        try:
            if attr.tag == "attr":
                # Clear existing content.
                self.edoms = []
                self.ui.listWidget.clear()

                # Find all <edom> elements.
                for edom in attr.xpath("attrdomv/edom"):
                    # Convert XML node content to a dictionary.
                    edom_dict = xml_utils.node_to_dict(edom, False)

                    # Add a new Edom widget using the parsed data.
                    self.add_edom(**edom_dict)
            else:
                # Print a message if the tag is incorrect.
                print("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(EdomList, "udom testing")
