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
    from pymdwizard.gui.ui_files import UI_taxoncl
    from pymdwizard.gui.repeating_element import RepeatingElement
except ImportError as err:
    raise ImportError(err, __file__)


class Taxoncl(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <taxoncl> tag, representing
        a taxonomic classification, which is a key component of the
        Taxonomy section (<taxonomy>). This widget supports nested
        classifications.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Manages fields for Taxonomic Rank Name (<taxonrn>) and
           Taxonomic Rank Value (<taxonrv>).
        2. Manages a repeating list of Common Names (<common>).
        3. Recursively manages a list of child <taxoncl> widgets for
           nested classifications.

    Notes:
        Inherits from "WizardWidget". The class contains a list,
        "child_taxoncl", to hold instances of itself for nesting.
    """

    # Class attributes.
    drag_label = "taxon class <taxoncl>"
    acceptable_tags = ["taxoncl"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding repeating element widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, creates a "RepeatingElement" for Common Names,
            and prepares the list for child "Taxoncl" widgets.

        Notes:
            None
        """

        self.ui = UI_taxoncl.Ui_fgdc_taxoncl()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        widget_kwargs = {"line_name": "common", "required": False}

        # Setup RepeatingElement for Common Names.
        self.commons = RepeatingElement(
            add_text="Add Common",
            remove_text="Remove last",
            widget_kwargs=widget_kwargs,
            show_buttons=False,
        )

        # Add the first common name field.
        self.commons.add_another()

        # Add the repeating element widget to the UI layout.
        self.ui.horizontalLayout_4.addWidget(self.commons)

        # List to hold nested Taxoncl widgets.
        self.child_taxoncl = []

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget, including both local
            fields and all nested child widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears Rank Name/Value, clears Common Names, and deletes
            all instances in "child_taxoncl".

        Notes:
            None
        """

        # Clear Taxon Rank Name and Value fields.
        self.ui.fgdc_taxonrn.clear()
        self.ui.fgdc_taxonrv.clear()

        # Clear all Common Name widgets.
        self.commons.clear_widgets()

        # Delete all nested child Taxoncl widgets.
        for taxoncl in self.child_taxoncl:
            taxoncl.deleteLater()

        # Reset the list of child widgets.
        self.child_taxoncl = []

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <taxoncl> XML
            element, including rank, common names, and recursively,
            child classifications.

        Passed arguments:
            None

        Returned objects:
            taxoncl (lxml.etree._Element): The <taxoncl> element
                tag in the XML tree.

        Workflow:
            1. Creates <taxoncl> node.
            2. Appends <taxonrn> and <taxonrv>.
            3. Appends all populated <common> names.
            4. Recursively calls "to_xml" for all child "Taxoncl".

        Notes:
            None
        """

        # Create the root <taxoncl> node.
        taxoncl = xml_utils.xml_node("taxoncl")

        # Add Taxon Rank Name.
        xml_utils.xml_node(
            "taxonrn",
            text=self.ui.fgdc_taxonrn.text(),
            parent_node=taxoncl,
        )

        # Add Taxon Rank Value.
        xml_utils.xml_node(
            "taxonrv",
            text=self.ui.fgdc_taxonrv.text(),
            parent_node=taxoncl,
        )

        # Get and add Common Names.
        common_names = [c.text() for c in self.commons.get_widgets()]
        for common_name in common_names:
            if common_name:
                xml_utils.xml_node(
                    "common", text=common_name, parent_node=taxoncl
                )

        # Recursively add child Taxoncl elements.
        for child_taxoncl in self.child_taxoncl:
            taxoncl.append(child_taxoncl.to_xml())

        return taxoncl

    def from_xml(self, taxoncl):
        """
        Description:
            Parses an XML element and populates the widget fields and
            creates nested child "Taxoncl" widgets.

        Passed arguments:
            taxoncl (lxml.etree._Element): The XML element, expected
                to be <taxoncl>.

        Returned objects:
            None

        Workflow:
            1. Populates Rank Name and Value.
            2. Populates Common Names using the "RepeatingElement".
            3. Recursively creates new "Taxoncl" widgets for each
               child <taxoncl> element found in the XML.

        Notes:
            None
        """

        try:
            if taxoncl.tag == "taxoncl":
                # Populate Rank Name and Value.
                self.ui.fgdc_taxonrn.setText(
                    taxoncl.xpath("taxonrn")[0].text
                )
                self.ui.fgdc_taxonrv.setText(
                    taxoncl.xpath("taxonrv")[0].text
                )

                # Populate Common Names (Repeating Element).
                commons = xml_utils.search_xpath(
                    taxoncl, "common", only_first=False
                )
                if commons:
                    # Clear existing widgets, don't add default.
                    self.commons.clear_widgets(add_another=False)
                    for common in commons:
                        # Add a new common name widget and set its text.
                        this_common = self.commons.add_another()
                        this_common.setText(common.text)

                # Recursively populate child Taxoncl widgets.
                children_taxoncl = taxoncl.xpath("taxoncl")
                for child_taxoncl in children_taxoncl:
                    # Create a new child widget instance.
                    child_widget = Taxoncl()

                    # Recursively populate the new widget.
                    child_widget.from_xml(child_taxoncl)

                    # Add to the child widget layout.
                    self.ui.child_taxoncl.layout().addWidget(child_widget)

                    # Store reference to the child widget.
                    self.child_taxoncl.append(child_widget)
            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not a detailed")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Taxoncl, "detailed testing")
