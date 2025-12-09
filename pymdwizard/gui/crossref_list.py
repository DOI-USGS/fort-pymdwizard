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
    from pymdwizard.gui.ui_files import UI_crossref
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.crossref import Crossref
except ImportError as err:
    raise ImportError(err, __file__)


class Crossref_list(WizardWidget):
    """
    Description:
        A widget for managing a list of FGDC "cross reference"
        ("crossref") elements, which are citation objects.
        Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the display and manipulation of multiple Crossref widgets
        using a RepeatingElement container. Controls visibility based on
        a radio button toggle.

    Notes:
        The "to_xml" method incorrectly wraps crossrefs in an
        "<idinfo>" tag instead of the expected parent.
    """

    # Class attributes.
    drag_label = "Cross Reference <crossref>"

    # This tag is typically "idinfo" in the context where the list appears.
    acceptable_tags = ["idinfo"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the main UI, sets up the RepeatingElement for
            Crossref widgets, adds an initial crossref, and hides the
            container by default.

        Notes:
            None
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_crossref.Ui_Form()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Initialize drag-and-drop features for the widget.
        self.setup_dragdrop(self)

        # Initialize the RepeatingElement container for Crossref widgets.
        self.crossrefs = RepeatingElement(
            which="tab",
            tab_label="Crossref",
            add_text="   Add Additional Crossref   ",
            widget=Crossref,
            remove_text="   Remove Selected Crossref   ",
            italic_text="",
        )

        # Add an initial Crossref widget.
        self.crossrefs.add_another()

        # Add the RepeatingElement to the main widget layout.
        self.ui.crossref_widget.layout().addWidget(self.crossrefs)

        # Hide the container widget by default.
        self.ui.crossref_widget.hide()

    def connect_events(self):
        """
        Description:
            Connect the appropriate GUI components with the corresponding
            functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the "Yes" radio button for cross-references to the
            visibility toggle function.

        Notes:
            None
        """

        # Connect the radio button to the visibility handler.
        self.ui.radio_crossrefyes.toggled.connect(self.crossref_used_change)

    def crossref_used_change(self, b):
        """
        Description:
            Toggles the visibility of the cross-reference list container.

        Passed arguments:
            b (bool): True to show the container, False to hide it.

        Returned objects:
            None

        Workflow:
            Shows or hides the "crossref_widget" based on the boolean
            state "b".

        Notes:
            None
        """

        if b:
            self.ui.crossref_widget.show()
        else:
            self.ui.crossref_widget.hide()

    def has_content(self):
        """
        Description:
            Checks if the cross-reference section is marked as being used.

        Passed arguments:
            None

        Returned objects:
            bool: True if the "Yes" radio button is checked, False
                otherwise.

        Workflow:
            Returns the checked state of the "Yes" radio button.

        Notes:
            None
        """

        return self.ui.radio_crossrefyes.isChecked()

    def get_children(self, widget=None):
        """
        Description:
            Returns a list of all active Crossref widgets managed by the
            RepeatingElement.

        Passed arguments:
            widget (QWidget, optional): Ignored parameter.

        Returned objects:
            children (list): List of Crossref widget instances.

        Workflow:
            Iterates through the RepeatingElement's widgets and collects
            them into a list.

        Notes:
            None
        """

        # Initiate list object.
        children = []

        # Iterate through the repeating widgets and collect them.
        for crossref in self.crossrefs.get_widgets():
            children.append(crossref)

        return children

    def clear_widget(self):
        """
        Description:
            Clears the widget content and resets the radio button.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the base class clear method and sets the radio button
            to "No" (hidden state).

        Notes:
            None
        """

        # Call the parent's clear method.
        super(Crossref_list, self).clear_widget()

        # Set the radio button to "No".
        self.ui.radio_crossrefno.setChecked(True)

    def to_xml(self):
        """
        Description:
            Encapsulates the multiple cross reference elements into a
            single XML node.

        Passed arguments:
            None

        Returned objects:
            idinfo (xml.etree.ElementTree.Element): The parent
                identification information element tag containing the
                cross references.

        Workflow:
            Creates an <idinfo> node and appends the XML from each
            active Crossref widget as a child.

        Notes:
            The parent tag <idinfo> is used here based on the original
            implementation, although <crossref> elements are typically
            direct children of <idinfo>.
        """

        # Create the parent "idinfo" XML node.
        idinfo = xml_utils.xml_node(tag="idinfo")

        # Iterate through each Crossref widget and append its XML to idinfo.
        for crossref in self.crossrefs.get_widgets():
            idinfo.append(crossref.to_xml())

        return idinfo

    def from_xml(self, xml_idinfo):
        """
        Description:
            Parse the XML code to populate the cross-reference list.

        Passed arguments:
            xml_idinfo (xml.etree.ElementTree.Element): The XML element
                containing the cross references (expected to be "idinfo").

        Returned objects:
            None

        Workflow:
            1. Check for the "idinfo" tag.
            2. Clear existing RepeatingElement widgets.
            3. Search for <crossref> children.
            4. Toggle the radio button based on whether crossrefs were
               found.
            5. For each <crossref> found, add a new widget and load
               the nested <citeinfo> XML into it.

        Notes:
            None
        """

        try:
            if xml_idinfo.tag == "idinfo":
                # Clear all existing crossref widgets.
                self.crossrefs.clear_widgets(add_another=False)

                # Search for all existing <crossref> nodes.
                crossrefs = xml_utils.search_xpath(
                    xml_idinfo, "crossref", only_first=False
                )

                # Check if any cross-references were found.
                if crossrefs:
                    self.ui.radio_crossrefyes.setChecked(True)
                else:
                    # If none found, add one empty widget and set to "No".
                    self.crossrefs.add_another()
                    self.ui.radio_crossrefno.setChecked(True)

                # Populate the widgets with the XML data.
                for crossref in crossrefs:
                    crossref_widget = self.crossrefs.add_another()

                    # Load the nested <citeinfo> into the widget.
                    crossref_widget.from_xml(
                        xml_utils.search_xpath(crossref, "citeinfo")
                    )
        except KeyError:
            # If any parsing error occurs, default to "No".
            self.ui.radio_crossrefno.setChecked(True)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Crossref_list, "Source Input testing")
