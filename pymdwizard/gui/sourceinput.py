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
    from pymdwizard.gui.ui_files import UI_sourceinput
    from pymdwizard.gui.srcinfo import SRCInfo
    from pymdwizard.gui.repeating_element import RepeatingElement
except ImportError as err:
    raise ImportError(err, __file__)


class SourceInput(WizardWidget):
    """
    Description:
        A container widget corresponding to the FGDC <lineage> tag,
        specifically managing a repeating list of <srcinfo> (Source
        Information) elements.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds the "RepeatingElement" widget configured to contain
           "SRCInfo" instances in a tabbed layout.
        2. Uses a radio button to conditionally show/hide the source
           information frame.
        3. Handles XML serialization/deserialization for the <lineage>
           structure containing multiple <srcinfo> elements.

    Notes:
        Inherits from "WizardWidget". The "acceptable_tags" is set to
        "lineage" because this widget manages the source input part
        of the overall lineage section.
    """

    # Class attributes.
    drag_label = "Source Information <srcinfo>"
    acceptable_tags = ["lineage"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            initializing the repeating element container for sources.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up drag-and-drop, creates the tabbed
            "RepeatingElement" for "SRCInfo" widgets, adds a default
            source, and hides the container initially.

        Notes:
            None
        """

        self.ui = UI_sourceinput.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Initialize the RepeatingElement container for source info.
        self.src_info = RepeatingElement(
            which="tab",
            tab_label="Source",
            add_text="Add Source",
            widget=SRCInfo,
            remove_text="Remove Source",
            italic_text="Source",
        )

        # Add an initial source tab.
        self.src_info.add_another()

        # Place the repeating element container in the frame layout.
        self.ui.frame_sourceinfo.layout().addWidget(self.src_info)

        # Hide the source info frame by default.
        self.ui.frame_sourceinfo.hide()

    def connect_events(self):
        """
        Description:
            Connects the 'Yes' radio button signal to the handler that
            controls source visibility.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects "radio_sourceyes.toggled" to "include_sources_change".

        Notes:
            None
        """

        # Connect the radio button signal to the visibility handler.
        self.ui.radio_sourceyes.toggled.connect(self.include_sources_change)

    def include_sources_change(self, b):
        """
        Description:
            Shows or hides the frame containing the repeating source
            information widgets based on the radio button state.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Calls frame_sourceinfo.show() if True, or hide() if False.

        Notes:
            None
        """

        if b:
            # Show the source information section.
            self.ui.frame_sourceinfo.show()
        else:
            # Hide the source information section.
            self.ui.frame_sourceinfo.hide()

    def clear_widget(self):
        """
        Description:
            Clears the widget's content by setting the "No" radio
            button and calling the parent clear method.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets "No" radio button and calls base class "clear_widget".

        Notes:
            None
        """

        # Set the "No" radio button to hide the sources.
        self.ui.radio_sourceno_2.setChecked(True)

        # Call the base class clear method.
        WizardWidget.clear_widget(self)

    def to_xml(self):
        """
        Description:
            Converts the content of all child "SRCInfo" widgets into a
            series of <srcinfo> elements wrapped in a <lineage> tag.

        Passed arguments:
            None

        Returned objects:
            lineage (lxml.etree._Element): The <lineage> element tag
                in the XML tree containing all <srcinfo> children.

        Workflow:
            1. Creates the root <lineage> node.
            2. If "Yes" is checked, iterates through all "SRCInfo"
               widgets and appends their XML output to <lineage>.

        Notes:
            None
        """

        # Create the root <lineage> node.
        lineage = xml_utils.xml_node(tag="lineage")
        if self.ui.radio_sourceyes.isChecked():
            cnt = 0
            srcinfo_list = self.src_info.get_widgets()

            # Append the XML output of each source widget.
            for srcinfo in srcinfo_list:
                lineage.append(srcinfo.to_xml())

        return lineage

    def from_xml(self, xml_srcinput):
        """
        Description:
            Parses an FGDC <lineage> XML element and populates the
            widget by creating corresponding "SRCInfo" tabs.

        Passed arguments:
            xml_srcinput (lxml.etree._Element): The XML node to load,
                expected to be <lineage>.

        Returned objects:
            None

        Workflow:
            1. Checks the tag.
            2. Clears existing tabs and sets "Yes" to show the frame.
            3. Finds all <srcinfo> children and populates new tabs.
            4. If no <srcinfo> elements are found, sets "No" and adds
               a single empty tab.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected tag.
            if xml_srcinput.tag == "lineage":
                # Clear all existing source tabs.
                self.src_info.clear_widgets(add_another=False)
                self.ui.frame_sourceinfo.show()
                self.ui.radio_sourceyes.setChecked(True)

                # Find all <srcinfo> children.
                xml_srcinput = xml_srcinput.findall("srcinfo")

                if xml_srcinput:
                    for srcinput in xml_srcinput:
                        try:
                            # Add a new source tab and populate it from XML.
                            srcinfo_widget = self.src_info.add_another()
                            srcinfo_widget.from_xml(srcinput)
                        except:
                            pass
                else:
                    # If no sources found, set 'No' and add one empty tab.
                    self.ui.radio_sourceno_2.setChecked(True)
                    self.src_info.add_another()
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SourceInput, "Source Input testing")
