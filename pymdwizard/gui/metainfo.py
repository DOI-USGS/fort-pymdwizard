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
    from pymdwizard.gui.ui_files import UI_metainfo
    from pymdwizard.gui.ContactInfo import ContactInfo
    from pymdwizard.gui.fgdc_date import FGDCDate
    from pymdwizard import __version__
except ImportError as err:
    raise ImportError(err, __file__)


class MetaInfo(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <metainfo> (Metadata
        Reference Information) tag. It manages metadata date, contact,
        and standard information.

    Passed arguments:
        root_widget (MetadataRoot, optional): The root widget of the
            metadata document.

    Returned objects:
        None

    Workflow:
        1. Initializes sub-widgets for Contact Info and Metadata Date.
        2. Handles logic for syncing the Metadata Standard Name and Version.
        3. Allows pulling contact info from the dataset contact.
        4. Serializes/deserializes all content, including preservation
           of optional tags not displayed in the UI.

    Notes:
        Inherits from "WizardWidget". Preserves non-editable XML tags
        from self.original_xml during serialization.
    """

    # Class attributes.
    drag_label = "Metadata Information <metainfo>"
    acceptable_tags = ["metainfo", "cntinfo", "ptcontact"]

    ui_class = UI_metainfo.Ui_fgdc_metainfo

    def __init__(self, root_widget=None):
        # Initialize base class.
        super(self.__class__, self).__init__()

        # Store the root widget reference.
        self.root_widget = root_widget

        # Will store the original XML to preserve non-editable tags.
        self.original_xml = None

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's GUI, initializing child
            widgets and placing them in the layout.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Initializes the UI and drag-and-drop setup.
            2. Creates "ContactInfo" and "FGDCDate" child widgets.
            3. Places the children in the appropriate layouts.

        Notes:
            None
        """

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        # Initialize child widgets.
        self.contactinfo = ContactInfo(parent=self)
        self.metd = FGDCDate(parent=self, fgdc_name="fgdc_metd")

        # Add child widgets to the layout containers.
        self.ui.help_metd.layout().addWidget(self.metd)
        self.ui.fgdc_metc.layout().addWidget(self.contactinfo)

    def connect_events(self):
        """
        Description:
            Connects GUI component signals to the corresponding handler
            functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects signals for standard name/version syncing and the
            "Use Dataset Contact" button.

        Notes:
            None
        """

        # Connect signals for Metadata Standard Name/Version sync.
        self.ui.fgdc_metstdn.currentTextChanged.connect(self.update_metstdv)
        self.ui.fgdc_metstdv.currentIndexChanged.connect(self.update_metstdn)

        # Connect button to pull contact from IdInfo section.
        self.ui.button_use_dataset.clicked.connect(self.pull_datasetcontact)

    def update_metstdn(self):
        """
        Description:
            Updates the Metadata Standard Name combobox index and triggers
            a schema switch in the root widget based on the selected
            **Metadata Standard Version**.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Checks the current version text and sets the corresponding
            name and schema.

        Notes:
            None
        """

        if self.ui.fgdc_metstdv.currentText() == "FGDC-STD-001-1998":
            # FGDC Content Standard for Digital Geospatial Metadata.
            self.ui.fgdc_metstdn.setCurrentIndex(0)
            self.root_widget.switch_schema("fgdc")
        elif self.ui.fgdc_metstdv.currentText() == "FGDC-STD-001.1-1999":
            # Biological Data Profile.
            self.ui.fgdc_metstdn.setCurrentIndex(1)
            self.root_widget.switch_schema("bdp")

    def update_metstdv(self):
        """
        Description:
            Updates the Metadata Standard Version combobox index and
            triggers a schema switch in the root widget based on the
            selected Metadata Standard Name.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Checks the current name text for biological or "bdp" and
            sets the corresponding version and schema.

        Notes:
            None
        """

        current_name = self.ui.fgdc_metstdn.currentText().lower()
        if "biological" in current_name or "bdp" in current_name:
            # Set to Biological Data Profile version.
            self.ui.fgdc_metstdv.setCurrentIndex(1)
            self.root_widget.switch_schema("bdp")
        else:
            # Set to FGDC CSDGM version.
            self.ui.fgdc_metstdv.setCurrentIndex(0)
            self.root_widget.switch_schema("fgdc")

    def pull_datasetcontact(self):
        """
        Description:
            Copies the contact information from the dataset contact
            (in the IdInfo section) to the metadata contact.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Gets the XML representation of the IdInfo point of
               contact ("ptcontac").
            2. Passes that XML to the metadata contact widget
               (self.contactinfo.from_xml).

        Notes:
            None
        """

        # Get the XML of the dataset's point of contact.
        ptcontac_xml = self.root_widget.idinfo.ptcontac.to_xml()

        # Populate the metadata contact from that XML.
        self.contactinfo.from_xml(ptcontac_xml)

    def to_xml(self):
        """
        Description:
            Converts the form's contents into an FGDC <metainfo> XML
            element. Preserves optional elements not displayed in the UI.

        Passed arguments:
            None

        Returned objects:
            metainfo_node (lxml.etree._Element): The XML node
                representing the metadata reference information.

        Workflow:
            1. Creates <metainfo>, <metd>, and <metc> nodes.
            2. Appends the XML from the "contactinfo" child widget.
            3. Appends <metstdn> and <metstdv>.
            4. Searches for and appends preserved optional tags
               ("metrd", "metfrd", "mettc", "metac", "metuc", "metsi",
               "metextns") from self.original_xml.

        Notes:
            None
        """

        # Create the root <metainfo> node.
        metainfo_node = xml_utils.xml_node("metainfo")

        # Metadata Date (<metd>)
        metd = xml_utils.xml_node(
            "metd",
            text=self.metd.get_date(),
            parent_node=metainfo_node,
        )

        # Preserve optional tags from original XML (metrd, metfrd).
        if self.original_xml is not None:
            for tag in ["metrd", "metfrd"]:
                node = xml_utils.search_xpath(self.original_xml, tag)
                if node is not None:
                    node.tail = None
                    metainfo_node.append(deepcopy(node))

        # Metadata Contact (<metc>).
        metc = xml_utils.xml_node("metc", parent_node=metainfo_node)
        cntinfo = self.contactinfo.to_xml()
        metc.append(cntinfo)

        # Metadata Standard Name and Version.
        metstdn = xml_utils.xml_node(
            "metstdn",
            text=self.ui.fgdc_metstdn.currentText(),
            parent_node=metainfo_node,
        )
        metstdv = xml_utils.xml_node(
            "metstdv",
            text=self.ui.fgdc_metstdv.currentText(),
            parent_node=metainfo_node,
        )

        # Preserve optional tags from original XML (mettc, metac).
        if self.original_xml is not None:
            for tag in ["mettc", "metac"]:
                node = xml_utils.search_xpath(self.original_xml, tag)
                if node is not None:
                    node.tail = None
                    metainfo_node.append(deepcopy(node))

        # Preserve optional tag <metuc> (Metadata User Comments).
        if self.original_xml is not None:
            metuc_node = xml_utils.search_xpath(self.original_xml, "metuc")
            if metuc_node is not None:
                # Re-create metuc using text content.
                metuc_str = xml_utils.get_text_content(
                    self.original_xml, "metuc"
                )
                xml_utils.xml_node(
                    "metuc", text=metuc_str, parent_node=metainfo_node
                )

        # Preserve optional tags from original XML (metsi, metextns).
        if self.original_xml is not None:
            for tag in ["metsi", "metextns"]:
                node = xml_utils.search_xpath(self.original_xml, tag)
                if node is not None:
                    node.tail = None
                    metainfo_node.append(deepcopy(node))

        return metainfo_node

    def from_xml(self, xml_metainfo):
        """
        Description:
            Populates the widget's fields from an XML element.

        Passed arguments:
            xml_metainfo (lxml.etree._Element): The XML node to load.
                Can be <metainfo>, <ptcontac>, or <cntinfo>.

        Returned objects:
            None

        Workflow:
            1. If loading <metainfo>, populates all fields and stores
               the element in self.original_xml.
            2. Switches the root widget's schema based on <metstdn>.
            3. If loading contact info, delegates to
               self.contactinfo.from_xml().

        Notes:
            None
        """

        if xml_metainfo.tag == "metainfo":
            # Store original XML for preservation on to_xml.
            self.original_xml = xml_metainfo

            # Load Metadata Contact.
            contact_path = xml_metainfo.xpath("metc/cntinfo")
            if contact_path:
                self.contactinfo.from_xml(contact_path[0])

            # Load Metadata Standard Name and switch schema
            standard = xml_utils.get_text_content(
                xml_metainfo, "metstdn"
            )
            if standard:
                self.ui.fgdc_metstdn.setCurrentText(standard)
                # Switch wizard content to reflect the standard
                if ("biological" in standard.lower() or
                        "bdp" in standard.lower()):
                    self.root_widget.switch_schema("bdp")
                else:
                    self.root_widget.switch_schema("fgdc")

            # Load Metadata Standard Version.
            metstdv = xml_utils.get_text_content(xml_metainfo, "metstdv")
            self.ui.fgdc_metstdv.setCurrentText(metstdv)

            # Load Metadata.
            metd = xml_utils.get_text_content(xml_metainfo, "metd")
            self.metd.set_date(metd)

        elif xml_metainfo.tag in ["ptcontac", "cntinfo"]:
            # If the XML is just contact information, load it directly.
            if xml_metainfo.tag == "ptcontac":
                xml_metainfo = xml_utils.search_xpath(xml_metainfo,
                                                      "cntinfo")
            self.contactinfo.from_xml(xml_metainfo)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(MetaInfo, "MetaInfo testing")
