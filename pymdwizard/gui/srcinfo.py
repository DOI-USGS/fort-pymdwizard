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
    from PyQt5.QtWidgets import QComboBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_srcinfo
    from pymdwizard.gui.citeinfo import Citeinfo
    from pymdwizard.gui.timeinfo import Timeinfo
except ImportError as err:
    raise ImportError(err, __file__)


class SRCInfo(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <srcinfo> tag, which
        provides detailed information about the source material for
        a geospatial dataset.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds child widgets for Source Citation ("Citeinfo") and
           Source Time Period ("Timeinfo").
        2. Handles user input for map scale, source type, and contribution
           statement.
        3. Updates its containing tab's label based on the citation title for
           better navigation.

    Notes:
        Inherits from "WizardWidget". Used as a repeating element
        within the Lineage (<lineage>) section.
    """

    # Class attributes.
    drag_label = "SRCInfo <srcinfo>"
    acceptable_tags = ["srcinfo"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding child widgets for citation and time.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, creates "Timeinfo" and "Citeinfo" instances,
            and inserts them into the respective layouts.

        Notes:
            None
        """

        self.ui = UI_srcinfo.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Initialize child widgets.
        self.timeinfo = Timeinfo()
        self.citation = Citeinfo(parent=self, include_lwork=False)

        # Place citation widget in its frame.
        self.ui.fgdc_srccite.layout().addWidget(self.citation)

        # Place timeinfo widget in its frame.
        self.ui.fgdc_srctime.layout().insertWidget(0, self.timeinfo)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects editing finished events for citation title to
            update the tab label, and source scale to format its text.

        Notes:
            None
        """

        # Connect to update the tab label when citation title changes.
        self.ui.fgdc_srccitea.editingFinished.connect(self.update_tab_label)

        # Connect to format the map scale input (e.g., 1:100000).
        self.ui.fgdc_srcscale.editingFinished.connect(self.format_scale)

    def update_tab_label(self):
        """
        Description:
            Updates the label of the tab containing this widget using
            the current value of the Source Citation Abbreviation.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Finds the parent tab widget and sets the tab's text using
            the citation abbreviation, truncated to 15 characters.

        Notes:
            None
        """

        # Get the first 15 characters of the citation abbreviation.
        new_label = "Source: {}".format(self.ui.fgdc_srccitea.text()[:15])

        # Traverse up the parent hierarchy to find the QTabWidget.
        tab_widget = self.ui.fgdc_srccitea.parent().parent().parent().parent()
        current_index = tab_widget.currentIndex()

        # Set the tab text for the current index.
        tab_widget.setTabText(current_index, new_label)

    def format_scale(self):
        """
        Description:
            Formats the source scale input to include thousands separators
            (e.g., 100000 becomes 100,000).

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Removes commas, converts to int/float, applies formatting,
            and updates the line edit text.

        Notes:
            Fails silently if the input cannot be converted to a number.
        """

        # Remove existing commas.
        cur_text = self.ui.fgdc_srcscale.text().replace(",", "")
        try:
            # Format as float if decimal is present, otherwise integer.
            if "." in cur_text:
                formatted_text = "{:,}".format(float(cur_text))
            else:
                formatted_text = "{:,}".format(int(cur_text))
            self.ui.fgdc_srcscale.setText(formatted_text)
        except:
            pass

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <srcinfo> XML
            element, including nested citation and time information.

        Passed arguments:
            None

        Returned objects:
            srcinfo (lxml.etree._Element): The <srcinfo> element
                tag in the XML tree.

        Workflow:
            1. Creates <srcinfo>.
            2. Appends XML output from "Citeinfo" and "Timeinfo".
            3. Appends fields for source scale, type, abbreviation,
               and contribution.

        Notes:
            Removes commas from the source scale before serialization.
        """

        # Create the root <srcinfo> node.
        srcinfo = xml_utils.xml_node("srcinfo")

        # --- Source Citation (<srccite>) ---
        srccite = xml_utils.xml_node("srccite", parent_node=srcinfo)
        cite = self.citation.to_xml()
        srccite.append(cite)

        # --- Source Scale Denominator (<srcscale>) ---
        if self.ui.fgdc_srcscale.text():
            srcscale = xml_utils.xml_node(
                "srcscale",
                text=self.ui.fgdc_srcscale.text().replace(",", ""),
                parent_node=srcinfo,
            )

        # --- Type of Source Media (<typesrc>) ---
        typesrc = xml_utils.xml_node(
            "typesrc", text=self.ui.fgdc_typesrc.currentText(),
            parent_node=srcinfo
        )

        # --- Source Time Period (<srctime>) ---
        srctime = xml_utils.xml_node("srctime", parent_node=srcinfo)
        timeinfo = self.timeinfo.to_xml()
        srctime.append(timeinfo)

        # Append Source Currentness Reference to srctime.
        xml_utils.xml_node(
            "srccurr",
            text=self.ui.fgdc_srccurr.currentText(),
            parent_node=srctime,
        )

        # --- Source Citation Abbreviation (<srccitea>) ---
        xml_utils.xml_node(
            "srccitea",
            text=self.ui.fgdc_srccitea.text(),
            parent_node=srcinfo,
        )

        # --- Source Contribution (<srccontr>) ---
        xml_utils.xml_node(
            "srccontr",
            text=self.ui.fgdc_srccontr.toPlainText(),
            parent_node=srcinfo,
        )

        return srcinfo

    def from_xml(self, srcinfo):
        """
        Description:
            Parses an FGDC <srcinfo> XML element and populates the
            widget's fields and nested child widgets.

        Passed arguments:
            srcinfo (lxml.etree._Element): The <srcinfo> XML element.

        Returned objects:
            None

        Workflow:
            1. Checks for the correct tag.
            2. Passes <citeinfo> to self.citation.
            3. Populates scale, type, abbreviation, and contribution.
            4. Passes time info to self.timeinfo.
            5. Updates the tab label.

        Notes:
            None
        """

        try:
            # Check for the correct tag name.
            if srcinfo.tag == "srcinfo":
                utils.populate_widget(self, srcinfo)

                # Find and isolate the nested citeinfo.
                srccite = srcinfo.xpath("srccite")[0]
                citeinfo = srccite.xpath("citeinfo")[0]
            elif srcinfo.tag != "srcinfo":
                # Exit if the wrong tag is passed.
                print("The tag is not 'srcinfo'")
                return

            # Populate Citation child widget.
            self.citation.from_xml(citeinfo)

            # Populate Source Scale and format it.
            utils.populate_widget_element(self.ui.fgdc_srcscale, srcinfo,
                                          "srcscale")
            self.format_scale()

            # Populate Type of Source Media.
            typesrc = srcinfo.xpath("typesrc/text()")
            if typesrc:
                typesrc_text = str(typesrc[0])
                self.findChild(QComboBox,
                               "fgdc_typesrc").setCurrentText(typesrc_text)

                # Populate Source Citation Abbreviation and Contribution.
                utils.populate_widget_element(
                    self.ui.fgdc_srccitea, srcinfo, "srccitea"
                )
                utils.populate_widget_element(
                    self.ui.fgdc_srccontr, srcinfo, "srccontr"
                )

            # Populate Source Time Period (<srctime>).
            if srcinfo.xpath("srctime"):
                timeinfo = srcinfo.xpath("srctime/timeinfo")[0]
                srccurr = srcinfo.xpath("srctime/srccurr")[0]
                self.timeinfo.from_xml(timeinfo)
                self.ui.fgdc_srccurr.setCurrentText(srccurr.text)

            # Update tab label after populating abbreviation.
            self.update_tab_label()

        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SRCInfo, "SRCInfo testing")
