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
from copy import deepcopy

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_DataQuality
    from pymdwizard.gui.AttributeAccuracy import AttributeAccuracy
    from pymdwizard.gui.LogicalAccuracy import LogicalAccuracy
    from pymdwizard.gui.Completeness import Completeness
    from pymdwizard.gui.PositionalAccuracy import PositionalAccuracy
    from pymdwizard.gui.sourceinput import SourceInput
    from pymdwizard.gui.procstep import ProcStep
except ImportError as err:
    raise ImportError(err, __file__)


class DataQuality(WizardWidget):
    """
    Description:
        A master widget for managing the FGDC "data quality"
        ("dataqual") metadata section. This widget aggregates several
        child widgets for sub-sections like accuracy, completeness,
        and lineage. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Initializes and arranges child widgets for all major data
        quality components. Handles collecting XML from children and
        reconstituting the full "dataqual" and "lineage" structure
        during XML conversion.

    Notes:
        The "to_xml" method handles complex re-assembly of the
        <lineage> and <dataqual> nodes, including merging source
        info and processing steps, and re-inserting legacy tags.
    """

    # Class attributes.
    drag_label = "Data Quality <dataqual>"
    acceptable_tags = ["dataqual"]

    # Assumed UI class for instantiation.
    ui_class = UI_DataQuality.Ui_fgdc_dataqual

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI, initializing all child
            widgets and adding them to the layouts.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, sets up drag-and-drop, creates instance
            of all required child widgets, and arranges them in the
            two-column layout.

        Notes:
            None
        """

        # Initialize the main UI.
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Setup drag-and-drop functionality.
        self.setup_dragdrop(self)

        # Initialize all child widgets.
        self.attraccr = AttributeAccuracy(parent=self)
        self.logic = LogicalAccuracy(parent=self)
        self.complete = Completeness(parent=self)
        self.posacc = PositionalAccuracy(parent=self)
        self.sourceinput = SourceInput(parent=self)
        self.procstep = ProcStep(parent=self)

        # Add accuracy/completeness widgets to the left column.
        self.ui.two_column_left.layout().addWidget(self.attraccr)
        self.ui.two_column_left.layout().addWidget(self.logic)
        self.ui.two_column_left.layout().addWidget(self.complete)
        self.ui.two_column_left.layout().addWidget(self.posacc)

        # Add source input to the bottom layout.
        self.ui.bottom_layout.layout().addWidget(self.sourceinput)

        # Add processing step to the lineage group box.
        self.ui.fgdc_lineage.layout().addWidget(self.procstep)
        self.scroll_area = self.ui.idinfo_scroll_area

    def clear_widget(self):
        """
        Description:
            Clears the content of this widget and its children.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the clear methods for child widgets and the parent
            class, and triggers a size update on the completeness widget.

        Notes:
            None
        """

        # Clear content of the SourceInput child widget.
        self.sourceinput.clear_widget()

        # Call the parent's clear method.
        WizardWidget.clear_widget(self)

        # Trigger size change on the completeness text box.
        self.complete.ui.fgdc_complete.sizeChange()

    def to_xml(self):
        """
        Description:
            Encapsulates the content of all child widgets into a single
            "dataqual" XML element tag, including complex lineage assembly.

        Passed arguments:
            None

        Returned objects:
            dataqual_node (xml.etree.ElementTree.Element): Data
                quality element tag in XML tree.

        Workflow:
            1. Creates the <dataqual> node.
            2. Appends accuracy and completeness nodes from children.
            3. Assembles the <lineage> node by merging <srcinfo>
               from "sourceinput" and <procstep> from "procstep".
            4. Re-inserts any legacy <method> or <cloud> tags
               from the "original_xml" if present.

        Notes:
            None
        """

        # Create the parent "dataqual" XML node.
        dataqual_node = xml_utils.xml_node(tag="dataqual")

        # Append Attribute Accuracy (<attracc>).
        attraccr_node = self.attraccr.to_xml()
        dataqual_node.append(attraccr_node)

        # Append Logical Accuracy (<logic>).
        logic_node = self.logic.to_xml()
        dataqual_node.append(logic_node)

        # Append Completeness (<complete>).
        complete_node = self.complete.to_xml()
        dataqual_node.append(complete_node)

        # Append Positional Accuracy (<posacc>) if content exists.
        if self.posacc.has_content():
            posacc_node = self.posacc.to_xml()
            dataqual_node.append(posacc_node)

        # Lineage Assembly ---------------------

        # Get the <lineage> node containing <srcinfo>.
        if self.sourceinput.has_content():
            srcinfo_node = self.sourceinput.to_xml()

        # Get the processing step nodes.
        procstep_node = self.procstep.to_xml()
        procstep_children = procstep_node.getchildren()

        # Append all procstep children to the lineage node.
        for child in procstep_children:
            srcinfo_node.append(child)

        # Re-insert any original <method> tags if loading from existing XML.
        if self.original_xml is not None:
            methods = xml_utils.search_xpath(
                self.original_xml, "lineage/method", only_first=False
            )
            for i, method in enumerate(methods):
                method.tail = None
                srcinfo_node.insert(i, deepcopy(method))

        # Append the fully assembled <lineage> node to <dataqual>.
        dataqual_node.append(srcinfo_node)

        # Re-insert any original <cloud> tags if loading from existing XML.
        if self.original_xml is not None:
            cloud = xml_utils.search_xpath(self.original_xml, "cloud")
            if cloud is not None:
                cloud.tail = None
                dataqual_node.append(deepcopy(cloud))

        return dataqual_node

    def from_xml(self, xml_dataqual):
        """
        Description:
            Parse the XML code into the relevant child widgets.

        Passed arguments:
            xml_dataqual (xml.etree.ElementTree.Element): The XML
                element containing the data quality details.

        Returned objects:
            None

        Workflow:
            Attempts to find and parse each data quality sub-element
            ("attracc", "logic", "complete", "posacc") and the shared
            "lineage" element, forwarding the XML node to the
            corresponding child widget's "from_xml" method.

        Notes:
            None
        """

        # Store the original XML for use in to_xml reassembly.
        self.original_xml = xml_dataqual

        # Parse Attribute Accuracy (<attracc>).
        try:
            attraccr = xml_dataqual.xpath("attracc")[0]
            self.attraccr.from_xml(attraccr)
        except IndexError:
            pass

        # Parse Logical Accuracy (<logic>).
        try:
            logic = xml_dataqual.xpath("logic")[0]
            self.logic.from_xml(logic)
        except IndexError:
            pass

        # Parse Completeness (<complete>).
        try:
            complete = xml_dataqual.xpath("complete")[0]
            self.complete.from_xml(complete)
        except IndexError:
            pass

        # Parse Positional Accuracy (<posacc>).
        try:
            posacc = xml_dataqual.xpath("posacc")[0]
            self.posacc.from_xml(posacc)
        except IndexError:
            pass

        # Parse Source Information (<lineage>).
        try:
            sourceinput = xml_dataqual.xpath("lineage")[0]
            self.sourceinput.from_xml(sourceinput)
        except IndexError:
            pass

        # Parse Processing Steps (<lineage>).
        try:
            procstep = xml_dataqual.xpath("lineage")[0]
            self.procstep.from_xml(procstep)
        except IndexError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(DataQuality, "DataQual testing")
