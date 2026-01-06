#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
The widget for the main metadata root item.
This is the container for an FGDC record without the application wrapper,
menu bar, etc.


NOTES
------------------------------------------------------------------------------
None
"""

# Non-standard python libraries.
try:
    from lxml import etree
    from PyQt5.QtGui import (QPainter, QPixmap)
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtCore import QTimeLine
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_MetadataRoot
    from pymdwizard.gui.IDInfo import IdInfo
    from pymdwizard.gui.spatial_tab import SpatialTab
    from pymdwizard.gui.EA import EA
    from pymdwizard.gui.DataQuality import DataQuality
    from pymdwizard.gui.metainfo import MetaInfo
    from pymdwizard.gui.distinfo import DistInfo
except ImportError as err:
    raise ImportError(err, __file__)


class MetadataRoot(WizardWidget):
    """
    Description:
        The root widget for the entire metadata document, corresponding
        to the FGDC <metadata> tag. It manages the top-level sections
        and handles schema switching.

    Passed arguments:
        parent (QWidget, optional): The parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes top-level section widgets (idinfo, dataqual, etc.).
        2. Manages which section is currently visible based on button clicks.
        3. Provides XML serialization/deserialization for the entire
           metadata structure.

    Notes:
        Inherits from "WizardWidget". Uses the "FaderWidget" for
        smooth section transitions.
    """

    # Class attributes.
    drag_label = "Metadata <metadata>"
    acceptable_tags = ["abstract"]

    ui_class = UI_MetadataRoot.Ui_metadata_root

    def __init__(self, parent=None):
        # Default to BDP (Biological Data Profile) schema.
        self.schema = "bdp"

        # Call the constructor of the base class (QWidget/WizardWidget).
        super(self.__class__, self).__init__(parent=parent)

        # Flags to track which optional sections are in use.
        self.use_dataqual = True
        self.use_spatial = True
        self.use_eainfo = True
        self.use_distinfo = True

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's GUI, initializing all
            top-level section widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Initializes the UI.
            2. Creates instances of all section widgets (IdInfo, etc.).
            3. Adds each section widget to its corresponding page in the
               stacked widget.

        Notes:
            None
        """

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self, enable=True)

        # Initialize and place the top-level section widgets.
        self.idinfo = IdInfo(root_widget=self, parent=self)
        self.ui.page_idinfo.layout().addWidget(self.idinfo)

        self.dataqual = DataQuality()
        self.ui.page_dataqual.layout().addWidget(self.dataqual)

        self.spatial_tab = SpatialTab(root_widget=self)
        self.ui.page_spatial.layout().addWidget(self.spatial_tab)

        self.eainfo = EA()
        self.ui.page_eainfo.layout().addWidget(self.eainfo)

        self.metainfo = MetaInfo(root_widget=self)
        self.ui.page_metainfo.layout().addWidget(self.metainfo)

        self.distinfo = DistInfo(root_widget=self)
        self.ui.page_distinfo.layout().addWidget(self.distinfo)

    def connect_events(self):
        """
        Description:
            Connects the top-level section header buttons to the
            "section_changed" handler.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the "pressed" signal of each section button to
            "self.section_changed".

        Notes:
            None
        """

        # Connect section buttons to the handler function.
        self.ui.idinfo_button.pressed.connect(self.section_changed)
        self.ui.dataquality_button.pressed.connect(self.section_changed)
        self.ui.spatial_button.pressed.connect(self.section_changed)
        self.ui.eainfo_button.pressed.connect(self.section_changed)
        self.ui.distinfo_button.pressed.connect(self.section_changed)
        self.ui.metainfo_button.pressed.connect(self.section_changed)

    def section_changed(self):
        """
        Description:
            Handles the event when a user clicks a top-level section
            header button, determining the new section index.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Gets the object name of the button that triggered the event.
            2. Looks up the corresponding index.
            3. Calls `switch_section` with the new index.

        Notes:
            Uses "self.sender()" to identify the calling object.
        """

        # Get the name of the button that was pressed.
        button_name = self.sender().objectName()

        index_lookup = {
            "idinfo_button": 0,
            "dataquality_button": 1,
            "spatial_button": 2,
            "eainfo_button": 3,
            "distinfo_button": 4,
            "metainfo_button": 5,
        }

        # Determine the index of the new section.
        new_index = index_lookup[button_name]
        self.switch_section(which_index=new_index)

    def switch_section(self, which_index):
        """
        Description:
            Performs the actual switching of the displayed section in
            the stacked widget, including applying a fade effect.

        Passed arguments:
            which_index (int): The index of the section to display.

        Returned objects:
            new_widget (QWidget): The newly displayed section widget.

        Workflow:
            1. Updates the checked state of the section buttons.
            2. Creates a "FaderWidget" for a smooth transition effect.
            3. Sets the new current index on the stacked widget.

        Notes:
            None
        """

        # Update button checked state (exclusive check).
        if which_index == 0:
            self.ui.idinfo_button.setChecked(True)
        elif which_index == 1:
            self.ui.dataquality_button.setChecked(True)
        elif which_index == 2:
            self.ui.spatial_button.setChecked(True)
        elif which_index == 3:
            self.ui.eainfo_button.setChecked(True)
        elif which_index == 4:
            self.ui.distinfo_button.setChecked(True)
        elif which_index == 5:
            self.ui.metainfo_button.setChecked(True)

        # Get the old and new widgets for the transition.
        old_widget = self.ui.fgdc_metadata.currentWidget()
        new_widget = self.ui.fgdc_metadata.widget(which_index)

        # Create fader for visual effect.
        FaderWidget(old_widget, new_widget)

        # Set the new current section.
        self.ui.fgdc_metadata.setCurrentIndex(which_index)

        return new_widget

    def switch_schema(self, schema):
        """
        Description:
            Switches the metadata schema between straight FGDC and BDP
            (Biological Data Profile) by updating child widgets.

        Passed arguments:
            schema (str): The name of the schema to switch to.

        Returned objects:
            None

        Workflow:
            1. Updates the internal self.schema flag.
            2. Calls switch_schema on relevant child widgets.

        Notes:
            Not all sections require schema-specific changes.
        """

        self.schema = schema

        # Propagate the schema change to child widgets.
        self.idinfo.switch_schema(schema)
        self.spatial_tab.switch_schema(schema)

    def use_section(self, which, value):
        """
        Description:
            Enables or disables (shows or hides) top-level optional
            sections.

        Passed arguments:
            which (str): Which section to change:
                ["dataqual", "spatial", "eainfo", "distinfo"].
            value (bool): Whether to enable (True) or disable (False).

        Returned objects:
            None

        Workflow:
            Updates the internal flag and calls "setVisible" on the
            corresponding widget.

        Notes:
            None
        """

        if which == "dataqual":
            self.use_dataqual = value
            self.dataqual.setVisible(value)
        if which == "spatial":
            self.use_spatial = value
            self.spatial_tab.setVisible(value)
        if which == "eainfo":
            self.use_eainfo = value
            self.eainfo.setVisible(value)
        if which == "distinfo":
            self.use_distinfo = value
            self.distinfo.setVisible(value)

    def to_xml(self):
        """
        Description:
            Converts the entire widget's contents into a single FGDC
            <metadata> XML element structure.

        Passed arguments:
            None

        Returned objects:
            metadata_node (lxml.etree._Element): The root XML node.

        Workflow:
            1. Creates the <metadata> root node.
            2. Calls to_xml() on each child widget.
            3. Appends the resulting XML nodes to the root, skipping
               optional sections if disabled or empty.

        Notes:
            Checks for has_content() for optional spatial sections.
        """

        # Create the root <metadata> node.
        metadata_node = xml_utils.xml_node(tag="metadata")

        # Append required and enabled sections.
        idinfo = self.idinfo.to_xml()
        metadata_node.append(idinfo)

        if self.use_dataqual:
            dataqual = self.dataqual.to_xml()
            metadata_node.append(dataqual)

        # Check for content before appending spatial sections.
        if self.spatial_tab.spdoinfo.has_content() and self.use_spatial:
            spdoinfo = self.spatial_tab.spdoinfo.to_xml()
            metadata_node.append(spdoinfo)

        if self.spatial_tab.spref.has_content() and self.use_spatial:
            spref = self.spatial_tab.spref.to_xml()
            metadata_node.append(spref)

        if self.eainfo.has_content() and self.use_eainfo:
            eainfo = self.eainfo.to_xml()
            metadata_node.append(eainfo)

        if self.use_distinfo:
            distinfo = self.distinfo.to_xml()
            metadata_node.append(distinfo)

        # Append the required <metainfo> section.
        metainfo = self.metainfo.to_xml()
        metadata_node.append(metainfo)

        return metadata_node

    def from_xml(self, metadata_element):
        """
        Description:
            Populates the entire widget structure from an FGDC
            <metadata> XML element.

        Passed arguments:
            metadata_element (lxml.etree._Element): The XML node to load.

        Returned objects:
            None

        Workflow:
            Calls "populate_section" for each top-level section widget.

        Notes:
            None
        """

        # Load content into all top-level sections.
        self.populate_section(
            metadata_element, "spdoinfo", self.spatial_tab.spdoinfo
        )

        self.populate_section(
            metadata_element, "spref", self.spatial_tab.spref
        )

        self.populate_section(metadata_element, "idinfo",
                              self.idinfo)

        self.populate_section(
            metadata_element, "dataqual", self.dataqual
        )

        self.populate_section(metadata_element, "eainfo",
                              self.eainfo)

        self.populate_section(
            metadata_element, "distinfo", self.distinfo
        )

        self.populate_section(
            metadata_element, "metainfo", self.metainfo
        )

    def populate_section(self, metadata_element, section_name, widget):
        """
        Description:
            Locates a section's XML and populates the corresponding widget.
            Handles cases where the passed element IS the section itself.

        Passed arguments:
            metadata_element (XML Element): The parent XML node or the
                section node itself.
            section_name (str): The tag name of the section (e.g., "idinfo").
            widget (WizardWidget): The widget corresponding to the section.

        Returned objects:
            bool: Returns True if the element passed was the section
                itself (used internally for recursion, not directly useful).

        Workflow:
            1. Determines if "metadata_element" is the section node itself.
            2. If not, searches for the section via XPath.
            3. Calls widget.from_xml(section) if found, or
               widget.clear_widget() if not found (and not the single
               section case).

        Notes:
            The "just_this_one" logic is to support loading from a single
            section's XML rather than the full <metadata> file.
        """

        # Check if the passed element is the section itself.
        just_this_one = type(metadata_element) == etree._Element

        if just_this_one and metadata_element.tag == section_name:
            section = metadata_element
        elif just_this_one:
            return True
        else:
            # Search for the section within the parent element.
            section = xml_utils.search_xpath(metadata_element, section_name)

        if section is not None:
            # Populate the widget with the found XML section.
            widget.from_xml(section)
        elif not just_this_one:
            # Clear the widget if the section is not found.
            widget.clear_widget()


class FaderWidget(QWidget):
    """
    Description:
        A utility widget used to create a visual fade-out transition
        when switching between two widgets in a layout.

    Passed arguments:
        old_widget (QWidget): The widget currently being displayed.
        new_widget (QWidget): The widget about to be displayed.

    Returned objects:
        None

    Workflow:
        1. Captures the "old_widget" content as a "QPixmap".
        2. Initializes a "QTimeLine" to manage the animation duration.
        3. Fades the "QPixmap"'s opacity from 1.0 to 0.0, redrawing
           in "paintEvent".
        4. Closes itself when the fade animation finishes.

    Notes:
        This is a temporary overlay widget.
    """

    def __init__(self, old_widget, new_widget):

        QWidget.__init__(self, new_widget)

        # Capture the content of the old widget as a pixmap.
        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        # Setup the animation timeline.
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(450)  # milliseconds
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        """
        Overridden Qt paint event to draw the fading pixmap.
        """

        painter = QPainter()
        painter.begin(self)

        # Apply the current opacity to the old widget's pixmap.
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        """
        Slot connected to the QTimeLine's valueChanged signal.
        Updates the opacity based on the timeline value.
        """

        # Value goes from 0.0 to 1.0; opacity goes from 1.0 to 0.0.
        self.pixmap_opacity = 1.0 - value

        # Trigger a redraw.
        self.repaint()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(MetadataRoot, "MetadataRoot testing")
