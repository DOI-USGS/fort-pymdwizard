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
    from PyQt5.QtWidgets import (QDialog, QMessageBox, QLineEdit, QComboBox,
                                 QRadioButton)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.core.xml_utils import xml_node
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import (UI_ContactInfo,
                                         UI_USGSContactImporter)
except ImportError as err:
    raise ImportError(err, __file__)


class ContactInfo(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "contact information" ("cntinfo")
        metadata element. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages UI elements for contact details (person/org, address,
        phone, email), supports importing USGS contacts via a dialog,
        and performs XML conversion.

    Notes:
        Relies on PyQt's dynamic layout manipulation in
        "switch_primary".
    """

    # Class attributes.
    drag_label = "Contact Information <cntinfo>"
    acceptable_tags = ["ptcontac", "cntinfo"]

    ui_class = UI_ContactInfo.Ui_USGSContactInfoWidget

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
            Connects the 'Import USGS Contact' button to the lookup
            dialog and the person/organization radio button to the
            layout switch function.

        Notes:
            None
        """

        # Connect the import button to the lookup function.
        self.ui.btn_import_contact.clicked.connect(self.find_usgs_contact)

        # Store a reference to the layout that holds the person/org.
        self.per_or_org = self.ui.fgdc_cntperp

        # Connect the person radio button to the primary switch.
        self.ui.rbtn_perp.toggled.connect(self.switch_primary)

    def find_usgs_contact(self):
        """
        Description:
            Initializes and displays the USGS contact lookup dialog.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Creates the dialog, loads its UI, connects the OK/Cancel
            buttons, sets the window icon, and displays the dialog.

        Notes:
            None
        """

        # Create the dialog instance.
        self.usgs_contact = QDialog(parent=self)
        utils.set_window_icon(self.usgs_contact)

        # Load the dialog UI.
        self.usgs_contact_ui = UI_USGSContactImporter.Ui_ImportUsgsUser()
        self.usgs_contact_ui.setupUi(self.usgs_contact)

        # Connect dialog buttons to handlers.
        self.usgs_contact_ui.btn_OK.clicked.connect(self.add_contact)
        self.usgs_contact_ui.btn_cancel.clicked.connect(self.cancel)
        utils.set_window_icon(self.usgs_contact)

        # Show the dialog.
        self.usgs_contact.show()

    def add_contact(self):
        """
        Description:
            Fetches USGS contact information based on a provided
            username, loads it into the widget, or shows an error.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Gets username and appends "@usgs.gov" if missing.
            2. Fetches contact data as XML.
            3. If successful, loads data into the widget and closes
               the dialog.
            4. If unsuccessful, displays an appropriate error message.

        Notes:
            None
        """

        # Retrieve username.
        username = self.usgs_contact_ui.le_usgs_ad_name.text()

        # Add "@usgs.gov" if it is not present
        if not "@" in username:
            username = username + "@usgs.gov"
        if not username:
            return

        try:
            # Retrieve contact info from USGS directory as XML.
            cntperp = utils.get_usgs_contact_info(username, as_dictionary=False)

            # Check if contact content is actually present.
            if cntperp.getchildren()[0].getchildren()[0].text.strip():
                # Load the XML into the widget and close the dialog.
                self.from_xml(cntperp)
                self.usgs_contact.deleteLater()
            else:
                # Show error message if name not found.
                msg = QMessageBox(self)
                utils.set_window_icon(msg)
                msg.setIcon(QMessageBox.Information)
                msg.setText("'{}' Not Found".format(username))
                msg.setInformativeText(
                    "The Metadata Wizard was unable to locate the "
                    "provided user name in the USGS directory"
                )
                msg.setWindowTitle("Name Not Found")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        except:
            # Show error for connection/unexpected issues.
            msg_text = (
                "Make sure there is a working Internet connection or "
                "try again later."
            )
            msg = QMessageBox(self)
            utils.set_window_icon(msg)
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "Issue encountered while searching contact information."
            )
            msg.setInformativeText(msg_text)
            msg.setWindowTitle("Problem encountered")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def cancel(self):
        """
        Description:
            Closes and deletes the USGS contact lookup dialog.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Schedules the dialog for deletion.

        Notes:
            None
        """

        self.usgs_contact.deleteLater()

    def switch_primary(self):
        """
        Description:
            Switches the UI layout to designate either Person or
            Organization as the primary contact entity.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Dynamically moves QLabel and QLineEdit widgets within the
            required and optional layout containers to reflect the
            selected primary entity.

        Notes:
            Relies on PyQt's layout insertWidget method.
        """

        # If 'Person' radio button is checked, make person primary
        if self.ui.rbtn_perp.isChecked():
            # Move Person label and field to required layout.
            self.per_or_org.layout().insertWidget(0, self.ui.lbl_cntper)
            self.ui.required_horizontal_layout.insertWidget(
                0, self.ui.fgdc_cntper
            )

            # Move Organization label and field to optional layout.
            self.per_or_org.layout().insertWidget(2, self.ui.lbl_cntorg)
            self.ui.optional_horizontal_layout.insertWidget(
                0, self.ui.fgdc_cntorg
            )

        # If "Organization" radio button is checked, make organization primary.
        else:
            # Move Organization label and field to required layout.
            self.per_or_org.layout().insertWidget(0, self.ui.lbl_cntorg)
            self.ui.required_horizontal_layout.insertWidget(
                0, self.ui.fgdc_cntorg
            )
            # Move Person label and field to optional layout.
            self.per_or_org.layout().insertWidget(2, self.ui.lbl_cntper)
            self.ui.optional_horizontal_layout.insertWidget(
                0, self.ui.fgdc_cntper
            )

    def to_xml(self):
        """
        Description:
            Encapsulates the widget's content into an XML "cntinfo"
            element tag.

        Passed arguments:
            None

        Returned objects:
            cntinfo (xml.etree.ElementTree.Element): Contact
                information element tag in XML tree.

        Workflow:
            Constructs the "cntinfo" node, handling person/org details
            conditionally based on radio button state, then processes
            position, address (up to 3 lines), city/state/postal,
            country, and electronic contact info.

        Notes:
            Assumes "xml_node" is available. Uses "findChild" to
            retrieve values from various UI elements.
        """

        # Create the parent "cntinfo" XML node.
        cntinfo = xml_node("cntinfo")

        # Get values for person and organization.
        cntper_str = self.findChild(QLineEdit, "fgdc_cntper").text()
        cntorg_str = self.findChild(QLineEdit, "fgdc_cntorg").text()

        # Check which entity is primary (Person or Organization).
        rbtn_perp = self.findChild(QRadioButton, "rbtn_perp")
        if rbtn_perp.isChecked():
            # Person primary: <cntperp>.
            cntperp = xml_node("cntperp", parent_node=cntinfo)
            cntper = xml_node("cntper", cntper_str, cntperp)
            if cntorg_str:
                cntorg = xml_node("cntorg", cntorg_str, cntperp)
        else:
            # Organization primary: <cntorgp>.
            cntorgp = xml_node("cntorgp", parent_node=cntinfo)
            cntper = xml_node("cntorg", cntorg_str, cntorgp)
            if cntper_str:
                cntper = xml_node("cntper", cntper_str, cntorgp)

        # Add Contact Position (<cntpos>).
        cntpos_str = self.findChild(QLineEdit, "fgdc_cntpos").text()
        if cntpos_str:
            cntpos = xml_node("cntpos", cntpos_str, cntinfo)

        # Add Contact Address (<cntaddr>).
        cntaddr = xml_node("cntaddr", parent_node=cntinfo)

        # Add Address Type (<addrtype>).
        addrtype_str = self.findChild(QComboBox,
                                      "fgdc_addrtype").currentText()
        addrtype = xml_node("addrtype", addrtype_str, cntaddr)

        # Add Address Lines (up to 3).
        address_str = self.findChild(QLineEdit, "fgdc_address").text()
        node = xml_node("address", address_str, cntaddr)
        address2_str = self.findChild(QLineEdit, "fgdc_address2").text()

        if address2_str:
            node = xml_node("address", address2_str, cntaddr)
        address3_str = self.findChild(QLineEdit, "fgdc_address3").text()
        if address3_str:
            node = xml_node("address", address3_str, cntaddr)

        # Add City, State, Postal Code.
        for label in ["city", "state", "postal"]:
            widget_str = self.findChild(QLineEdit,
                                        "fgdc_" + label).text()
            try:
                # Create XML node if text is present.
                node = xml_node(label, widget_str, cntaddr)
            except:
                pass

        # Add Country.
        country_str = self.ui.fgdc_country.text()
        if country_str:
            node = xml_node("country", country_str, cntaddr)

        # Add Voice, Fax, Email.
        for label in ["cntvoice", "cntfax", "cntemail"]:
            widget_str = self.findChild(QLineEdit,
                                        "fgdc_" + label).text()
            try:
                # cntvoice is required, others only if text is present.
                if label == "cntvoice" or widget_str:
                    node = xml_node(label, widget_str, cntinfo)
            except:
                pass

        return cntinfo

    def from_xml(self, contact_information):
        """
        Description:
            Parse the XML code into the relevant contact information
            elements.

        Passed arguments:
            contact_information (xml.etree.ElementTree.Element): The
                XML element containing contact details ("cntinfo" or
                "ptcontac").

        Returned objects:
            None

        Workflow:
            1. Clears existing content.
            2. Uses "node_to_dict" and "populate_widget" to fill most
               fields.
            3. Manually handles multi-line addresses and complex
               person/organization grouping (<cntperp> or <cntorgp>).

        Notes:
            Uses "xml_utils.search_xpath" for address lines.
        """

        self.clear_widget()

        # Convert the XML node to a dictionary for easy field population.
        contact_dict = xml_utils.node_to_dict(contact_information)

        # Populate simple fields (e.g., position, voice, email).
        utils.populate_widget(self, contact_dict)

        # Manually handle multiple address lines.
        addresses = xml_utils.search_xpath(
            contact_information, "cntaddr/address", only_first=False
        )
        if len(addresses) >= 1:
            self.ui.fgdc_address.setText(addresses[0].text)
        if len(addresses) >= 2:
            self.ui.fgdc_address2.setText(addresses[1].text)
        if len(addresses) >= 3:
            self.ui.fgdc_address3.setText(addresses[2].text)

        addrtype_widget = self.findChild(QComboBox, "fgdc_addrtype")

        # Dig into the dictionary structure to find necessary details.
        if "cntinfo" in contact_dict:
            contact_dict = contact_dict["cntinfo"]
        if "fgdc_cntinfo" in contact_dict:
            contact_dict = contact_dict["fgdc_cntinfo"]

        # Set address type.
        try:
            addrtype = contact_dict["fgdc_cntaddr"]["fgdc_addrtype"]
            addrtype_widget.setEditText(addrtype)
        except KeyError:
            pass

        # Set the correct primary radio button.
        try:
            if "fgdc_cntorgp" in contact_dict:
                rbtn_orgp = self.findChild(QRadioButton, "rbtn_orgp")
                rbtn_orgp.setChecked(True)
            elif "fgdc_cntperp" in contact_dict:
                rbtn_perp = self.findChild(QRadioButton, "rbtn_perp")
                rbtn_perp.setChecked(True)
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ContactInfo)
