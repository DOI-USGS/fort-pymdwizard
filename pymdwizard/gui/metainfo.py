#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

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

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QMessageBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_metainfo
    from pymdwizard.gui.ContactInfo import ContactInfo
    from pymdwizard.gui.fgdc_date import FGDCDate
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

        # Connect signals for Metadata Standard Name/Version choices. The
        # "activated" signal is emitted only when the user picks a value,
        # not when the code sets one.
        self.ui.fgdc_metstdn.activated.connect(self.name_chosen)
        self.ui.fgdc_metstdv.activated.connect(self.version_chosen)

        # Connect button to pull contact from IdInfo section.
        self.ui.button_use_dataset.clicked.connect(self.pull_datasetcontact)

    @staticmethod
    def schema_from_name(name):
        """
        Description:
            Returns the schema that a Metadata Standard Name belongs to.

        Passed arguments:
            name (str): The Metadata Standard Name text.

        Returned objects:
            str: "bdp" if the name is the Biological Data Profile,
                otherwise "fgdc".

        Workflow:
            Looks for "biological" or "bdp" in the lower-cased name.

        Notes:
            None
        """

        name = name.lower()
        if "biological" in name or "bdp" in name:
            return "bdp"
        return "fgdc"

    def name_chosen(self, index=None):
        """
        Description:
            Applies the schema for a Metadata Standard Name picked by
            the user.

        Passed arguments:
            index (int): Index of the chosen item (unused).

        Returned objects:
            None

        Workflow:
            Works out the schema from the name text and passes it to
            "apply_chosen_schema".

        Notes:
            None
        """

        self.apply_chosen_schema(
            self.schema_from_name(self.ui.fgdc_metstdn.currentText())
        )

    def version_chosen(self, index=None):
        """
        Description:
            Applies the schema for a Metadata Standard Version picked by
            the user.

        Passed arguments:
            index (int): Index of the chosen item (unused).

        Returned objects:
            None

        Workflow:
            Maps "FGDC-STD-001-1998" to FGDC and "FGDC-STD-001.1-1999"
            to BDP and passes it to "apply_chosen_schema". Any other
            (typed) version leaves the schema unchanged.

        Notes:
            None
        """

        version = self.ui.fgdc_metstdv.currentText()
        if version == "FGDC-STD-001-1998":
            self.apply_chosen_schema("fgdc")
        elif version == "FGDC-STD-001.1-1999":
            self.apply_chosen_schema("bdp")

    def apply_chosen_schema(self, schema):
        """
        Description:
            Switches the record to the schema the user picked in the
            Metadata Standard Name or Version box.

        Passed arguments:
            schema (str): "fgdc" or "bdp".

        Returned objects:
            None

        Workflow:
            1. If switching to plain FGDC while Taxonomy is "Yes" or the
               Geographic Description has text, asks for confirmation
               because plain FGDC cannot store them. If declined, the
               boxes go back to the current standard.
            2. Switches the schema (an explicit choice) and syncs the
               Name and Version boxes.
            3. After a confirmed switch to FGDC, sets Taxonomy to "No".

        Notes:
            None
        """

        root = self.root_widget
        if schema == "fgdc" and root.has_bdp_only_content():
            msg = (
                "The plain FGDC standard does not include Taxonomy or a "
                "Geographic Description. If you switch to it, they will be "
                "left out of the saved file.\n\nSwitch anyway?"
            )
            answer = QMessageBox.question(
                self,
                "Switch metadata standard?",
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                self.show_schema(root.schema)
                return

        root.set_schema(schema, explicit=True)

        if schema == "fgdc":
            # Taxonomy is not saved under plain FGDC, so don't leave it
            # set to "Yes". Its entries are kept if it is set back to "Yes".
            root.idinfo.taxonomy.ui.rbtn_no.setChecked(True)

    def show_schema(self, schema):
        """
        Description:
            Sets the Metadata Standard Name and Version boxes to the
            standard for a schema, without triggering a schema switch.

        Passed arguments:
            schema (str): "fgdc" or "bdp".

        Returned objects:
            None

        Workflow:
            Selects item 1 (BDP) or item 0 (FGDC) in both boxes with
            their signals blocked.

        Notes:
            None
        """

        index = 1 if schema == "bdp" else 0
        for combo in (self.ui.fgdc_metstdn, self.ui.fgdc_metstdv):
            combo.blockSignals(True)
            combo.setCurrentIndex(index)
            combo.blockSignals(False)

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
        xml_utils.xml_node(
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
        xml_utils.xml_node(
            "metstdn",
            text=self.ui.fgdc_metstdn.currentText(),
            parent_node=metainfo_node,
        )
        xml_utils.xml_node(
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
                # Switch wizard content to reflect the standard. A record
                # that declares BDP keeps it even without taxonomy.
                schema = self.schema_from_name(standard)
                self.root_widget.bdp_by_choice = schema == "bdp"
                self.root_widget.switch_schema(schema)

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
