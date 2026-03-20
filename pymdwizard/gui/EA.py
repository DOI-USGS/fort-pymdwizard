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
    from pymdwizard.gui.ui_files import UI_EA
    from pymdwizard.gui.detailed import Detailed
    from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
except ImportError as err:
    raise ImportError(err, __file__)


class EA(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "Entity and Attribute Information"
        ("eainfo") metadata section. It handles both overview fields
        and a repeating list of "Detailed" description widgets.
        Inherits from WizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages UI for Entity/Attribute Overview ("eaover") and
        Detailed Citation ("eadetcit"). Uses a tab widget to contain a
        list of dynamically added "Detailed" description widgets.

    Notes:
        The tab widget structure requires special handling for adding/
        removing the "Detailed" tabs.
    """

    # Class attributes.
    drag_label = "Entity and Attributes <eainfo>"
    acceptable_tags = ["eainfo", "detailed"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, sets up the list for "Detailed" widgets,
            adds the initial "Detailed" tab, sets up drag-and-drop, and
            applies syntax highlighting to text areas.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_EA.Ui_Form()
        self.ui.setupUi(self)

        # List to hold references to Detailed widgets.
        self.detaileds = []

        # Add the first required Detailed tab.
        detailed = self.add_detailed()

        # Initialize drag-and-drop features.
        self.setup_dragdrop(self)

        # Setup syntax highlighting for overview fields.
        self.highlighter = Highlighter(self.ui.fgdc_eaover.document())
        self.highlighter2 = Highlighter(self.ui.fgdc_eadetcit.document())

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
            Connects the "Add Detailed" button to the "add_detailed"
            method.

        Notes:
            None
        """

        # Connect the button to add a new Detailed tab.
        self.ui.btn_add_detailed.clicked.connect(self.add_detailed)

    def remove_detailed(self):
        """
        Description:
            Removes the currently selected "Detailed" tab from the UI
            and the internal list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the current tab index, removes the tab from the UI
            widget, and deletes the corresponding object from the
            "detaileds" list.

        Notes:
            The first "Detailed" widget cannot be removed.
        """

        # Get the index of the current tab.
        cur_index = self.ui.fgdc_eainfo.currentIndex()

        # Remove the tab from the QTabWidget.
        self.ui.fgdc_eainfo.removeTab(cur_index)

        # Remove the widget instance from the internal list.
        # Note: Index is -1 because the first tab (index 0) is reserved.
        del self.detaileds[cur_index - 1]

    def add_detailed(self):
        """
        Description:
            Adds another "Detailed" tab to the form.

        Passed arguments:
            None

        Returned objects:
            new_detailed (Detailed): The newly created Detailed widget.

        Workflow:
            Creates a new "Detailed" widget, passes the "remove_detailed"
            function, inserts the new widget before the last tab (which
            is the Add button), and appends it to the internal list.

        Notes:
            None
        """

        # Instantiate a new Detailed widget.
        new_detailed = Detailed(remove_function=self.remove_detailed,
                                parent=self)
        # Insert the new tab before the last tab (the Add button).
        self.ui.fgdc_eainfo.insertTab(
            self.ui.fgdc_eainfo.count() - 1, new_detailed, "Detailed"
        )

        # Store the new widget instance.
        self.detaileds.append(new_detailed)

        return new_detailed

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears the content of the first "Detailed" tab, removes all
            subsequent "Detailed" tabs, and clears the overview text
            fields.

        Notes:
            None
        """

        # Clear the content of the first Detailed widget.
        self.detaileds[0].clear_widget()

        # Remove all extra Detailed tabs (from end to 1).
        for i in range(len(self.detaileds), 1, -1):
            self.ui.fgdc_eainfo.removeTab(i)

            # Remove from the internal list.
            del self.detaileds[i - 1]

        # Clear the overview text fields.
        utils.set_text(self.ui.fgdc_eaover, "")
        utils.set_text(self.ui.fgdc_eadetcit, "")

    def has_content(self):
        """
        Description:
            Checks for valid content in this widget.

        Passed arguments:
            None

        Returned objects:
            bool: True if any text fields are populated or if any
                "Detailed" widget has content.

        Workflow:
            Checks the overview texts and iterates through all "Detailed"
            widgets to see if any have content.

        Notes:
            None
        """

        # Initiate default value.
        has_content = False

        # Check overview text fields.
        if self.ui.fgdc_eadetcit.toPlainText():
            has_content = True
        if self.ui.fgdc_eaover.toPlainText():
            has_content = True

        # Check if the first Detailed widget has content.
        if self.detaileds and self.detaileds[0].has_content():
            has_content = True

        # Check all other Detailed widgets.
        for detailed in self.detaileds:
            if detailed.has_content():
                has_content = True

        return has_content

    def to_xml(self):
        """
        Description:
            Encapsulates the Entity and Attribute information into a
            single "eainfo" XML element tag.

        Passed arguments:
            None

        Returned objects:
            eainfo (xml.etree.ElementTree.Element): Entity and Attribute
                element tag in XML tree.

        Workflow:
            1. Creates the <eainfo> parent node.
            2. Appends the XML for all "Detailed" widgets.
            3. If overview text exists, creates the <overview> node
               with <eaover> and <eadetcit> children.

        Notes:
            The first "Detailed" node is only output if it has content,
            but subsequent nodes are output regardless.
        """

        # Create the parent "eainfo" XML node.
        eainfo = xml_utils.xml_node("eainfo")

        # Only output the first detailed if it has content
        if self.detaileds and self.detaileds[0].has_content():
            detailed_xml = self.detaileds[0].to_xml()
            eainfo.append(detailed_xml)

        # The remaining detaileds will get output regardless.
        for detailed in self.detaileds[1:]:
            detailed_xml = detailed.to_xml()
            eainfo.append(detailed_xml)

        # Get the overview text fields.
        eaover_str = self.ui.fgdc_eaover.toPlainText()
        eadetcit_str = self.ui.fgdc_eadetcit.toPlainText()

        # Create and append <overview> if either text field is populated.
        if eaover_str or eadetcit_str:
            overview = xml_utils.xml_node("overview", parent_node=eainfo)
            # <eaover>
            xml_utils.xml_node("eaover", text=eaover_str,
                               parent_node=overview)
            # <eadetcit>
            xml_utils.xml_node(
                "eadetcit", text=eadetcit_str, parent_node=overview
            )

        return eainfo

    def from_xml(self, eainfo):
        """
        Description:
            Parse the XML code into the relevant E&A elements.

        Passed arguments:
            eainfo (xml.etree.ElementTree.Element): The XML element
                containing the entity and attribute information.

        Returned objects:
            None

        Workflow:
            1. Clears existing widgets.
            2. Parses <overview> and populates text fields.
            3. Parses the first <detailed> node into the initial tab.
            4. Iterates over remaining <detailed> nodes, adding a new
               tab for each, and populating its content.

        Notes:
            None
        """

        try:
            # Clear all existing content first.
            self.ui.fgdc_eainfo.setCurrentIndex(0)
            self.clear_widget()

            if eainfo.tag == "eainfo":
                self.original_xml = eainfo
                overview = eainfo.xpath("overview")

                # Parse and populate overview text fields.
                if overview:
                    eaover = eainfo.xpath("overview/eaover")
                    if eaover:
                        utils.set_text(self.ui.fgdc_eaover, eaover[0].text)

                    eadetcit = eainfo.xpath("overview/eadetcit")
                    if eadetcit:
                        utils.set_text(self.ui.fgdc_eadetcit, eadetcit[0].text)

                    # Switch to the overview tab after populating.
                    self.ui.fgdc_eainfo.setCurrentIndex(2)

                # Parse and populate detailed sections.
                detailed = eainfo.xpath("detailed")
                if detailed:
                    # Populate the first required Detailed tab.
                    self.ui.fgdc_eainfo.setCurrentIndex(1)
                    self.detaileds[0].from_xml(detailed[0])

                    # Loop through all remaining Detailed nodes.
                    for i, additional_detailed in enumerate(detailed[1:]):
                        # Add a new tab for each.
                        new_detailed = self.add_detailed()

                        # Set current tab to the new one.
                        self.ui.fgdc_eainfo.setCurrentIndex(i + 2)

                        # Populate the new tab.
                        new_detailed.from_xml(additional_detailed)
            else:
                print("The tag is not EA")
        except KeyError:
            return None


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(EA, "detailed testing")
