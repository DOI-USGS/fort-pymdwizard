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

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QMessageBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_distinfo
    from pymdwizard.gui.ContactInfo import ContactInfo
    from pymdwizard.gui.metainfo import MetaInfo
    from pymdwizard.gui.repeating_element import RepeatingElement
except ImportError as err:
    raise ImportError(err, __file__)


class DistInfo(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "distribution information"
        ("distinfo") metadata element. This includes distributor
        contact, online links, fees, and liability.
        Inherits from WizardWidget.

    Passed arguments:
        root_widget (QWidget, optional): The root metadata widget.

    Returned objects:
        None

    Workflow:
        1. Manages distributor contact using a "ContactInfo" child widget.
        2. Manages multiple distribution URLs using "RepeatingElement".
        3. Toggles visibility and content based on radio button choices
           (online, direct, or other distribution).

    Notes:
        The "pull_datasetcontact" method fetches a ScienceBase contact
        template for the distributor.
    """

    # Class attributes.
    drag_label = "Distribution Information <distinfo>"
    acceptable_tags = ["distinfo"]

    # Assumed UI class for instantiation.
    ui_class = UI_distinfo.Ui_fgdc_distinfo

    def __init__(self, root_widget=None):
        # Initialize the parent class.
        super(self.__class__, self).__init__()
        self.root_widget = root_widget
        self.scroll_area = self.ui.scrollArea

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, creates child widgets ("ContactInfo",
            "MetaInfo"), embeds the "ContactInfo" widget, creates the
            "RepeatingElement" for URLs, and adds an initial URL field.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Setup drag-and-drop functionality.
        self.setup_dragdrop(self)

        # Initialize child widgets.
        self.contactinfo = ContactInfo(parent=self)
        self.metainfo = MetaInfo()

        # Embed the contact information widget.
        self.ui.fgdc_distrib.layout().addWidget(self.contactinfo)

        # Hide the main distribution section by default.
        self.ui.widget_distinfo.hide()

        # Initialize the RepeatingElement for distribution URLs (networkr).
        self.networkr_list = RepeatingElement(
            add_text="Add URL",
            remove_text="Remove last",
            italic_text="URL(s) of website or GIS service",
            widget_kwargs={"label": "URL", "line_name": "fgdc_networkr"},
        )
        self.networkr_list.add_another()

        # Add the repeating element to the layout.
        self.ui.horizontalLayout_6.addWidget(self.networkr_list)

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
            Connects radio button toggles to visibility and state
            handling functions, and the "Use SB Contact" button to the
            "pull_datasetcontact" function.

        Notes:
            None
        """

        self.ui.radio_distyes.toggled.connect(self.include_dist_contacts)
        self.ui.radio_online.toggled.connect(self.online_toggle)
        self.ui.radio_otherdist.toggled.connect(self.other_dist_toggle)
        self.ui.radio_dist.toggled.connect(self.dist_toggle)
        self.ui.button_use_sb.clicked.connect(self.pull_datasetcontact)

    def online_toggle(self, b):
        """
        Description:
            Enables/disables elements related to online distribution.

        Passed arguments:
            b (bool): True if the radio button is checked.

        Returned objects:
            None

        Workflow:
            If checked, enables/shows URL list, liability, and fees.
            If unchecked, disables/hides URL list.

        Notes:
            None
        """

        if b:
            # Enable/show online specific fields.
            self.networkr_list.setEnabled(True)
            self.networkr_list.show()
            self.ui.fgdc_distliab.setEnabled(True)
            self.ui.fgdc_fees.setEnabled(True)
            self.networkr_list.setEnabled(True)
        else:
            # Disable/hide URL list.
            self.networkr_list.setEnabled(False)
            self.networkr_list.hide()

    def other_dist_toggle(self, b):
        """
        Description:
            Enables/disables elements related to custom distribution.

        Passed arguments:
            b (bool): True if the radio button is checked.

        Returned objects:
            None

        Workflow:
            If checked, enables the custom text box and liability, and
            disables the fees box (as custom terms often replace fees).

        Notes:
            None
        """

        if b:
            self.ui.fgdc_custom.setEnabled(True)
            self.ui.fgdc_fees.setEnabled(False)
            self.ui.fgdc_distliab.setEnabled(True)
        else:
            self.ui.fgdc_custom.setEnabled(False)

    def dist_toggle(self, b):
        """
        Description:
            Enables/disables elements related to direct distribution.

        Passed arguments:
            b (bool): True if the radio button is checked.

        Returned objects:
            None

        Workflow:
            If checked, enables the liability field and disables fees.

        Notes:
            None
        """

        if b:
            self.ui.fgdc_distliab.setEnabled(True)
            self.ui.fgdc_fees.setEnabled(False)
        else:
            self.ui.fgdc_distliab.setEnabled(False)

    def include_dist_contacts(self, b):
        """
        Description:
            Toggles the visibility of the distribution information
            container based on the radio button state.

        Passed arguments:
            b (bool): True to show the container, False to hide it.

        Returned objects:
            None

        Workflow:
            Shows or hides the "widget_distinfo".

        Notes:
            None
        """

        if b:
            self.ui.widget_distinfo.show()
        else:
            self.ui.widget_distinfo.hide()

    def pull_datasetcontact(self):
        """
        Description:
            Loads the ScienceBase contact information from a template
            file and populates the "ContactInfo" widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Locates the template XML file.
            2. Reads the file and extracts the ScienceBase contact info.
            3. Populates the "contactinfo" child widget.
            4. Displays a warning on error (e.g., file read failure).

        Notes:
            None
        """

        try:
            # Pull this contact info from our starter template file.
            template_fname = utils.get_resource_path("CSDGM_Template.xml")
            template_record = xml_utils.fname_to_node(template_fname)

            # Search for the ScienceBase contact information.
            sb_info = xml_utils.search_xpath(
                template_record, "distinfo/distrib/cntinfo"
            )

            # Populate the child widget
            self.contactinfo.from_xml(sb_info)
        except:
            msg = "Having trouble getting ScienceBase contact info now.\n"
            msg += "Check internet connection or try again later."
            QMessageBox.warning(self, "Problem encountered", msg)

    def has_content(self):
        """
        Description:
            Checks if the distribution information section is marked as
            being used.

        Passed arguments:
            None

        Returned objects:
            bool: True if the "Yes" radio button is checked, False
                otherwise.

        Workflow:
            Returns the checked state of the 'Yes' radio button.

        Notes:
            None
        """

        return self.ui.radio_distyes.isChecked()

    def to_xml(self):
        """
        Description:
            Encapsulates the distribution information content into a
            single "distinfo" XML element tag.

        Passed arguments:
            None

        Returned objects:
            distinfo_node (xml.etree.ElementTree.Element): Distribution
                information element tag in XML tree.

        Workflow:
            1. Creates <distinfo> node and appends <distrib>
               (with contact info).
            2. Re-inserts legacy tags like <resdesc> and <techpreq>.
            3. Conditionally builds <stdorder> (online), <custom>
               (other), or just <distliab> based on radio button state.

        Notes:
            None
        """

        # Create the parent "distinfo" XML node.
        distinfo_node = xml_utils.xml_node("distinfo")

        # Create the <distrib> node and append the contact info.
        dist = xml_utils.xml_node("distrib", parent_node=distinfo_node)
        cntinfo = self.contactinfo.to_xml()
        dist.append(cntinfo)

        # Re-insert original <resdesc> if it exists.
        if self.original_xml is not None:
            resdesc = xml_utils.search_xpath(self.original_xml, "resdesc")
            if resdesc is not None:
                resdesc.tail = None
                distinfo_node.append(deepcopy(resdesc))

        # --- Online Distribution (<stdorder>) ---
        if self.ui.radio_online.isChecked():
            # <distliab>
            liab = xml_utils.xml_node(
                "distliab",
                text=self.ui.fgdc_distliab.toPlainText(),
                parent_node=distinfo_node,
            )

            # <stdorder> container
            stdorder = xml_utils.xml_node("stdorder",
                                          parent_node=distinfo_node)
            digform = xml_utils.xml_node("digform",
                                         parent_node=stdorder)

            # Re-insert original <digtinfo> or create default.
            digtinfo = None
            if self.original_xml is not None and self.original_xml.xpath(
                    "stdorder/digform/digtinfo/formname"
            ):
                digtinfo = self.original_xml.xpath(
                    "stdorder/digform/digtinfo"
                )[0]
                digform.append(deepcopy(digtinfo))
            else:
                digtinfo = xml_utils.xml_node("digtinfo",
                                              parent_node=digform)
                xml_utils.xml_node(
                    "formname", parent_node=digtinfo, text="Digital Data"
                )

            # <digtopt> -> <onlinopt> -> <computer> -> <networka>.
            digtopt = xml_utils.xml_node("digtopt", parent_node=digform)
            onlinopt = xml_utils.xml_node("onlinopt", parent_node=digtopt)
            computer = xml_utils.xml_node("computer", parent_node=onlinopt)
            networka = xml_utils.xml_node("networka", parent_node=computer)

            # Insert all <networkr> nodes from the repeating element.
            for networkr in self.networkr_list.get_widgets():
                if networkr.text() != "":
                    networkr_node = xml_utils.xml_node(
                        "networkr", parent_node=networka,
                        text=networkr.text()
                    )

            # Fees
            fees = xml_utils.xml_node(
                "fees", text=self.ui.fgdc_fees.toPlainText(),
                parent_node=stdorder
            )

            # Re-insert optional online attributes (<accinstr>, <oncomp>).
            if self.original_xml is not None:
                accinstr = xml_utils.search_xpath(
                    self.original_xml,
                    "stdorder/digform/digtopt/onlinopt/accinstr",
                )
                if accinstr is not None:
                    accinstr.tail = None
                    onlinopt.append(deepcopy(accinstr))
            if self.original_xml is not None:
                oncomp = xml_utils.search_xpath(
                    self.original_xml,
                    "stdorder/digform/digtopt/onlinopt/oncomp",
                )
                if oncomp is not None:
                    oncomp.tail = None
                    onlinopt.append(deepcopy(oncomp))

        # --- Other Distribution (<custom>) ---
        if self.ui.radio_otherdist.isChecked():
            liab = xml_utils.xml_node(
                "distliab",
                text=self.ui.fgdc_distliab.toPlainText(),
                parent_node=distinfo_node,
            )
            other = xml_utils.xml_node(
                "custom",
                text=self.ui.fgdc_custom.toPlainText(),
                parent_node=distinfo_node,
            )

        # --- Direct Distribution (Just <distliab>) ---
        if self.ui.radio_dist.isChecked():
            liab = xml_utils.xml_node(
                "distliab",
                text=self.ui.fgdc_distliab.toPlainText(),
                parent_node=distinfo_node,
            )

        # Re-insert original <techpreq> if it exists.
        if self.original_xml is not None:
            techpreq = xml_utils.search_xpath(self.original_xml,
                                              "techpreq")
            if techpreq is not None:
                techpreq.tail = None
                distinfo_node.append(deepcopy(techpreq))

        return distinfo_node

    def from_xml(self, xml_distinfo):
        """
        Description:
            Parse the XML code into the relevant distribution elements.

        Passed arguments:
            xml_distinfo (xml.etree.ElementTree.Element): The XML
                element containing the distribution information.

        Returned objects:
            None

        Workflow:
            1. Checks for "distinfo" tag and sets the "Yes" radio button.
            2. Populates "contactinfo".
            3. Checks for distribution type ("distliab", "custom",
               "stdorder") to set the appropriate radio button.
            4. Populates fields like liability, fees, and the list of
               "networkr" URLs.

        Notes:
            None
        """

        self.original_xml = xml_distinfo
        self.clear_widget()

        if xml_distinfo.tag == "distinfo":
            self.original_xml = xml_distinfo
            self.ui.radio_distyes.setChecked(True)

            # Populate Contact Info.
            if xml_distinfo.xpath("distrib/cntinfo"):
                self.contactinfo.from_xml(xml_distinfo.xpath(
                    "distrib/cntinfo")[0])

            # Check for Distliab (default for direct distribution).
            if xml_distinfo.xpath("distliab"):
                self.ui.radio_dist.setChecked(True)
                utils.populate_widget_element(
                    widget=self.ui.fgdc_distliab, element=xml_distinfo,
                    xpath="distliab"
                )
                self.ui.fgdc_distliab.sizeChange()

            # Check for Custom (other distribution).
            if xml_distinfo.xpath("custom"):
                self.ui.radio_otherdist.setChecked(True)
                utils.populate_widget_element(
                    widget=self.ui.fgdc_custom, element=xml_distinfo,
                    xpath="custom"
                )

            # Check for Stdorder (online distribution).
            if xml_distinfo.xpath("stdorder"):
                self.ui.radio_online.setChecked(True)

                # Find all <networkr> URLs.
                networkrs = xml_distinfo.findall(
                    "stdorder/digform/digtopt/"
                    "onlinopt/computer/networka/networkr"
                )

                if networkrs:
                    # Clear default and add widgets for each URL found.
                    self.networkr_list.clear_widgets(add_another=False)

                    for networkr in networkrs:
                        networkr_widget = self.networkr_list.add_another()
                        networkr_widget.setText(networkr.text)
                else:
                    # If none found, keep the default single empty widget.
                    self.networkr_list.add_another()

                # Populate Fees.
                utils.populate_widget_element(
                    widget=self.ui.fgdc_fees,
                    element=xml_distinfo,
                    xpath="stdorder/fees",
                )


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(DistInfo, "DistInfo testing")
