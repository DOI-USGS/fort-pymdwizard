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
    from pymdwizard.gui.ui_files import UI_procstep
    from pymdwizard.gui.ProcessStep import ProcessStep
    from pymdwizard.gui.repeating_element import RepeatingElement
except ImportError as err:
    raise ImportError(err, __file__)


class ProcStep(WizardWidget):  #
    """
    Description:
        A container widget corresponding to the FGDC <lineage> tag.
        It manages a repeating list of <procstep> widgets, where each
        step describes a single operation in the data's history.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds the "RepeatingElement" widget configured to use tabs
           and contain "ProcessStep" instances.
        2. Handles the serialization and deserialization of the entire
           <lineage> structure, which contains multiple <procstep>
           elements.

    Notes:
        Inherits from "WizardWidget". The class name "ProcStep" is used
        here, but its purpose is to contain multiple <procstep>
        elements, thus handling the <lineage> tag.
    """

    # Class attributes.
    drag_label = "Process Step <procstep>"
    acceptable_tags = ["lineage"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            initializing the repeating element container.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up drag-and-drop, creates the
            "RepeatingElement" (tab-based) for "ProcessStep" widgets,
            adds a default step, and places the container in the layout.

        Notes:
            None
        """

        self.ui = UI_procstep.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Initialize the RepeatingElement container for steps.
        self.proc_step = RepeatingElement(
            which="tab",
            tab_label="Step",
            add_text="Additional Step",
            widget=ProcessStep,
            remove_text="Remove Step",
            # Descriptive text for the section
            italic_text=("Describe the methods performed to collect "
                         "or generate the data.\n Provide as much "
                         "detail as possible."),
        )

        # Add an initial process step tab.
        self.proc_step.add_another()

        # Place the repeating element container in the main widget's layout.
        self.ui.widget_procstep.layout().addWidget(self.proc_step)

    def to_xml(self):
        """
        Description:
            Converts the content of all child "ProcessStep" widgets into
            an FGDC <lineage> XML element.

        Passed arguments:
            None

        Returned objects:
            lineage (lxml.etree._Element): The <lineage> element tag
                in the XML tree containing all <procstep> children.

        Workflow:
            1. Creates the root <lineage> node.
            2. Iterates through all child "ProcessStep" widgets.
            3. Appends the XML output (<procstep>) of each child
               to the <lineage> node.

        Notes:
            None
        """

        # Create the root <lineage> node.
        lineage = xml_utils.xml_node(tag="lineage")
        procstep_list = self.proc_step.get_widgets()

        # Iterate through all ProcessStep widgets and append their XML.
        for procstep in procstep_list:
            lineage.append(procstep.to_xml())

        return lineage

    def from_xml(self, xml_procstep):
        """
        Description:
            Parses an FGDC <lineage> XML element and populates the
            widget by creating corresponding "ProcessStep" tabs.

        Passed arguments:
            xml_procstep (lxml.etree._Element): The XML node to load,
                expected to be <lineage>.

        Returned objects:
            None

        Workflow:
            1. Checks the tag.
            2. Clears existing steps.
            3. Finds all <procstep> children.
            4. For each <procstep>, a new tab is added and populated.
            5. If no steps are found, adds a single default empty step.

        Notes:
            None
        """

        try:
            # Check if the element tag matches the expected tag.
            if xml_procstep.tag == "lineage":
                # Clear all existing step tabs.
                self.proc_step.clear_widgets(add_another=False)

                # Find all <procstep> children.
                xml_procstep = xml_procstep.findall("procstep")

                if xml_procstep:
                    for procstep in xml_procstep:
                        # Add a new step widget and populate it from XML.
                        procdesc_widget = self.proc_step.add_another()
                        procdesc_widget.from_xml(procstep)
                else:
                    # If no steps found, add one default empty step
                    self.proc_step.add_another()
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ProcStep, "Source Input testing")
