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
    from pymdwizard.gui.ui_files import UI_spdoinfo
except ImportError as err:
    raise ImportError(err, __file__)


class SpdoInfo(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <spdoinfo> tag, which
        describes the approach used to encode spatial coordinates,
        including data structure type (e.g., raster or vector) and
        related metrics (e.g., row/column count).

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Manages UI fields for data type ("direct"), vector type
           ("sdtstype"), and raster properties ("rasttype", "rowcount",
           "colcount", "vrtcount").
        2. Uses radio buttons to conditionally show/hide the content.
        3. Dynamically switches the input fields shown based on the
           selected spatial data organization type.

    Notes:
        Inherits from "WizardWidget". The class name "SpdoInfo" is a
        short form for Spatial Data Organization Information.
    """

    # Class attributes.
    drag_label = "Spatial Domain Info <spdoinfo>"
    acceptable_tags = ["spdoinfo"]

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.original_xml = None

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up drag-and-drop, and clears the widget.

        Notes:
            None
        """

        self.ui = UI_spdoinfo.Ui_spatial_domain_widget()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Clear fields and reset state.
        self.clear_widget()

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the "Yes" radio button to content visibility
            and the data type dropdown to the form change handler.

        Notes:
            None
        """

        # Connect "Yes" radio button to show/hide content.
        self.ui.rbtn_yes.toggled.connect(self.spdoinfo_used_change)

        # Connect data type selector to switch between raster/vector forms.
        self.ui.fgdc_direct.currentIndexChanged.connect(self.change_type)

    def spdoinfo_used_change(self, b):
        """
        Description:
            Shows or hides the content widget based on the "Yes"
            radio button state.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Calls content_widget.show() or content_widget.hide().

        Notes:
            None
        """

        if b:
            # Show the content fields.
            self.ui.content_widget.show()
        else:
            # Hide the content fields.
            self.ui.content_widget.hide()

    def change_type(self):
        """
        Description:
            Switches the stacked widget index to display either raster
            or vector specific fields based on the selected "fgdc_direct"
            type.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            If "Raster" is selected, sets stacked widget index to 1;
            otherwise, sets it to 0 (vector).

        Notes:
            None
        """

        # Check the current text of the data type combobox.
        if self.ui.fgdc_direct.currentText() == "Raster":
            # Show the Raster input fields (index 1).
            self.ui.vector_or_raster.setCurrentIndex(1)
        else:
            # Show the Vector input fields (index 0).
            self.ui.vector_or_raster.setCurrentIndex(0)

    def has_content(self):
        """
        Description:
            Checks if the widget contains content that should be written to
            XML.

        Passed arguments:
            None

        Returned objects:
            bool: True if the "Yes" radio button is checked, False otherwise.

        Workflow:
            Returns the state of the "Yes" radio button.

        Notes:
            This is the widget's content check.
        """

        # Content exists if the user has indicated they will provide info.
        return self.ui.rbtn_yes.isChecked()

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget and resets UI state.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears text fields, resets dropdown indices, sets the "No"
            radio button, and hides content.

        Notes:
            None
        """

        # Clear raster counts.
        self.ui.fgdc_rowcount.setText("")
        self.ui.fgdc_colcount.setText("")
        self.ui.fgdc_vrtcount.setText("")

        # Clear vector count.
        self.ui.fgdc_ptvctcnt.setText("")

        # Reset dropdowns to the first item (typically empty/default).
        self.ui.fgdc_sdtstype.setCurrentIndex(0)
        self.ui.fgdc_rasttype.setCurrentIndex(0)
        self.ui.fgdc_direct.setCurrentIndex(2)

        # Set the "No" radio button and hide the content fields.
        self.ui.rbtn_no.setChecked(True)
        self.spdoinfo_used_change(False)

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <spdoinfo> XML
            element, including nested raster or vector information.

        Passed arguments:
            None

        Returned objects:
            spdoinfo (lxml.etree._Element or None): The <spdoinfo>
                element or None if content is not included.

        Workflow:
            1. Creates <spdoinfo> if "Yes" is checked.
            2. Appends optional <indspref> if present in original XML.
            3. Appends <direct>.
            4. Builds either the <rastinfo> (for Raster) or <ptvctinf>
               (for Vector/Point) structure.

        Notes:
            None
        """

        if self.ui.rbtn_yes.isChecked():
            # Create the root <spdoinfo> node.
            spdoinfo = xml_utils.xml_node("spdoinfo")

            # Preserve <indspref> if it existed in the original XML.
            if self.original_xml is not None:
                indspref = xml_utils.search_xpath(self.original_xml,
                                                  "indspref")
                if indspref is not None:
                    indspref.tail = None
                    spdoinfo.append(deepcopy(indspref))

            # Add <direct> (Spatial object type).
            direct = xml_utils.xml_node(
                "direct", text=self.ui.fgdc_direct.currentText(),
                parent_node=spdoinfo
            )

            # --- Handle RASTER specific information ---
            if self.ui.fgdc_direct.currentText() == "Raster":
                rasttype = self.ui.fgdc_rasttype.currentText()
                if rasttype:
                    rastinfo = xml_utils.xml_node("rastinfo",
                                                  parent_node=spdoinfo)
                    xml_utils.xml_node(
                        "rasttype", text=rasttype, parent_node=rastinfo
                    )

                    # Get count strings.
                    rowcount_str = self.ui.fgdc_rowcount.text()
                    colcount_str = self.ui.fgdc_colcount.text()
                    vrtcount_str = self.ui.fgdc_vrtcount.text()

                    if rowcount_str or colcount_str:
                        # Add required counts.
                        xml_utils.xml_node(
                            "rowcount",
                            text=rowcount_str,
                            parent_node=rastinfo,
                        )
                        xml_utils.xml_node(
                            "colcount",
                            text=colcount_str,
                            parent_node=rastinfo,
                        )
                        if vrtcount_str:
                            # Add optional vertical count.
                            xml_utils.xml_node(
                                "vrtcount",
                                text=vrtcount_str,
                                parent_node=rastinfo,
                            )

            # --- Handle VECTOR specific information ---
            else:
                sdtstype = self.ui.fgdc_sdtstype.currentText()
                ptvctcnt = self.ui.fgdc_ptvctcnt.text()

                if sdtstype or ptvctcnt:
                    ptvctinf = xml_utils.xml_node("ptvctinf",
                                                  parent_node=spdoinfo)
                    sdtsterm = xml_utils.xml_node("sdtsterm",
                                                  parent_node=ptvctinf)
                    sdtstype = xml_utils.xml_node(
                        "sdtstype", text=sdtstype, parent_node=sdtsterm
                    )

                    ptvctcnt_str = self.ui.fgdc_ptvctcnt.text()
                    if ptvctcnt_str:
                        sdtsterm = xml_utils.xml_node(
                            "ptvctcnt", text=ptvctcnt_str,
                            parent_node=sdtsterm
                        )
        else:
            spdoinfo = None

        return spdoinfo

    def from_xml(self, spdoinfo):
        """
        Description:
            Parses an XML element and populates the widget's fields.

        Passed arguments:
            spdoinfo (lxml.etree._Element): The XML element, expected to
                be <spdoinfo>.

        Returned objects:
            None

        Workflow:
            1. Clears existing content.
            2. Checks for <spdoinfo> tag and sets "Yes" radio button.
            3. Extracts and sets values for <direct>, vector types
               ("sdtstype", "ptvctcnt"), and raster counts/type.
            4. Handles combobox index switching to match the data type.

        Notes:
            Relies on xml_utils.get_text_content for extraction.
        """

        self.clear_widget()
        if spdoinfo.tag == "spdoinfo":
            self.original_xml = spdoinfo

            self.ui.rbtn_yes.setChecked(True)

            direct = xml_utils.get_text_content(spdoinfo, "direct")
            if direct is not None:
                # Set fgdc_direct and trigger change_type() via index.
                if "raster" in direct.lower():
                    # Set the index twice to force signal emission.
                    self.ui.fgdc_direct.setCurrentIndex(0)
                    self.ui.fgdc_direct.setCurrentIndex(2)
                elif "point" in direct.lower():
                    self.ui.fgdc_direct.setCurrentIndex(2)
                    self.ui.fgdc_direct.setCurrentIndex(0)
                elif "vector" in direct.lower():
                    self.ui.fgdc_direct.setCurrentIndex(0)
                    self.ui.fgdc_direct.setCurrentIndex(1)

            # --- Extract Raster Info ---
            rasttype = xml_utils.get_text_content(
                spdoinfo, "rastinfo/rasttype"
            )
            if rasttype is not None:
                self.ui.fgdc_rasttype.setCurrentText(rasttype)

            rowcount = xml_utils.get_text_content(spdoinfo,
                                                 "rastinfo/rowcount")
            if rowcount is not None:
                self.ui.fgdc_rowcount.setText(rowcount)

            colcount = xml_utils.get_text_content(spdoinfo,
                                                 "rastinfo/colcount")
            if colcount is not None:
                self.ui.fgdc_colcount.setText(colcount)

            vrtcount = xml_utils.get_text_content(spdoinfo,
                                                 "rastinfo/vrtcount")
            if vrtcount is not None:
                self.ui.fgdc_vrtcount.setText(vrtcount)

            # --- Extract Vector Info ---
            sdtstype = xml_utils.get_text_content(
                spdoinfo, "ptvctinf/sdtsterm/sdtstype"
            )
            if sdtstype is not None:
                self.ui.fgdc_sdtstype.setCurrentText(sdtstype)

            ptvctcnt = xml_utils.get_text_content(
                spdoinfo, "ptvctinf/sdtsterm/ptvctcnt"
            )
            if ptvctcnt is not None:
                self.ui.fgdc_ptvctcnt.setText(ptvctcnt)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SpdoInfo, "Spatial Domain Information")
