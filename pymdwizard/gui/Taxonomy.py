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
    from PyQt5.QtCore import QPoint
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_taxonomy
    from pymdwizard.gui import taxonomy_gui
    from pymdwizard.gui.taxoncl import Taxoncl
    from pymdwizard.gui.keywtax import Keywordtax
except ImportError as err:
    raise ImportError(err, __file__)


class Taxonomy(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <taxonomy> tag, which
        describes the biological classification information for the
        dataset's subject matter.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds child widgets for taxonomic keywords ("Keywordtax")
           and the classification tree ("Taxoncl").
        2. Provides functionality to search the ITIS database via a
           separate GUI ("taxonomy_gui.ItisMainForm").
        3. Manages the overall inclusion/exclusion of the taxonomy
           section.

    Notes:
        Inherits from "WizardWidget". Uses "QPoint" for GUI positioning
        when launching the search tool.
    """

    # Class attributes.
    drag_label = "Taxonomy"
    acceptable_tags = ["taxonomy"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding child widgets for keywords and classification.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, creates "Keywordtax" and "Taxoncl" instances,
            and embeds them into the layout. Sets initial state to hidden.

        Notes:
            None
        """

        self.ui = UI_taxonomy.Ui_Taxonomy()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Embed Keywordtax widget.
        self.keywtax = Keywordtax()
        self.ui.kws_layout.addWidget(self.keywtax)

        # Embed Taxoncl (Taxonomic Classification) widget.
        self.taxoncl = Taxoncl()
        self.ui.taxoncl_contents.layout().addWidget(self.taxoncl)

        # Hide contents by default.
        self.include_taxonomy_change(False)

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the "Search ITIS" button to the search function
            and the "Yes/No" radio button to content visibility.

        Notes:
            None
        """

        # Connect search button to the ITIS utility.
        self.ui.btn_search.clicked.connect(self.search_itis)

        # Connect "Yes" radio button to show/hide content.
        self.ui.rbtn_yes.toggled.connect(self.include_taxonomy_change)

    def include_taxonomy_change(self, b):
        """
        Description:
            Shows or hides the entire taxonomy content widget based on
            the "Yes" radio button state.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Calls widget_contents.show() or widget_contents.hide().

        Notes:
            None
        """

        if b:
            # Show the content fields.
            self.ui.widget_contents.show()
        else:
            # Hide the content fields.
            self.ui.widget_contents.hide()

    def search_itis(self):
        """
        Description:
            Launches a separate GUI for searching the Integrated
            Taxonomic Information System (ITIS).

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Creates an "ItisMainForm" instance, passing the current
               widget's XML content and "from_xml" method for callback.
            2. Positions and shows the new GUI window.

        Notes:
            The search tool uses the current XML content to initialize.
        """

        # Initialize the ITIS search GUI.
        self.tax_gui = taxonomy_gui.ItisMainForm(
            xml=self.to_xml(), fgdc_function=self.from_xml
        )

        # Get geometry of the current frame.
        fg = self.frameGeometry()

        # Move the new GUI window relative to the current one.
        self.tax_gui.move(fg.topRight() - QPoint(150, -25))

        # Display the new GUI.
        self.tax_gui.show()

    def remove_selected(self):
        """
        Description:
            Removes selected rows from the internal dataframe used by
            the keyword table model (currently unused, kept for context).

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Finds selected rows in "table_include".
            2. Drops corresponding indices from "selected_items_df".
            3. Emits a layout change signal for the table model.

        Notes:
            This method is likely a relic from a previous design or
            intended for a feature not fully integrated here.
        """

        # Get selected rows from the table view.
        indexes = self.ui.table_include.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]

        # Get the index labels from the internal DataFrame.
        index = self.selected_items_df.index[selected_indices]

        # Drop the selected rows.
        self.selected_items_df.drop(index, inplace=True)

        # Notify the model of the change.
        self.ui.table_include.model().layoutChanged.emit()

    def has_content(self):
        """
        Description:
            Checks if the widget contains content that should be written to XML.

        Passed arguments:
            None

        Returned objects:
            bool: True if the "Yes" radio button is checked, False otherwise.

        Workflow:
            Returns the state of the "Yes" radio button.

        Notes:
            None
        """

        return self.ui.rbtn_yes.isChecked()

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget by clearing child
            widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls "clear_widget" on the embedded "Keywordtax" and
            "Taxoncl" instances.

        Notes:
            None
        """

        # Clear the taxonomic keywords widget.
        self.keywtax.clear_widget()

        # Clear the taxonomic classification widget (including children).
        self.taxoncl.clear_widget()

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <taxonomy> XML
            element, merging content from child widgets and preserving
            some original XML elements.

        Passed arguments:
            None

        Returned objects:
            taxonomy (lxml.etree._Element): The <taxonomy> element
                tag in the XML tree.

        Workflow:
            1. Creates <taxonomy> node.
            2. Appends XML from "keywtax" and "taxoncl".
            3. Preserves original <taxonsys> and <taxongen> if they
               existed in self.original_xml.

        Notes:
            None
        """

        # Create the root <taxonomy> node.
        taxonomy = xml_utils.xml_node("taxonomy")

        # Append content from taxonomic keywords widget.
        taxonomy.append(self.keywtax.to_xml())

        # Preserve original <taxonsys> and <taxongen> if present.
        if self.original_xml is not None:
            # Preserve original <taxonsys>.
            taxonsys = xml_utils.search_xpath(self.original_xml,
                                              "taxonsys")
            if taxonsys is not None:
                taxonsys.tail = None
                taxonomy.append(deepcopy(taxonsys))

            # Preserve original <taxongen>.
            taxongen = xml_utils.search_xpath(self.original_xml,
                                              "taxongen")
            if taxongen is not None:
                taxongen.tail = None
                taxonomy.append(deepcopy(taxongen))

        # Append content from taxonomic classification widget.
        taxonomy.append(self.taxoncl.to_xml())
        return taxonomy

    def from_xml(self, taxonomy_element):
        """
        Description:
            Parses an XML element and populates the widget fields and
            child widgets.

        Passed arguments:
            taxonomy_element (lxml.etree._Element): The XML element,
                expected to be <taxonomy>.

        Returned objects:
            None

        Workflow:
            1. Stores the original XML.
            2. Clears the widget and sets the "Yes" radio button.
            3. Passes the relevant child elements to "keywtax.from_xml"
               and "taxoncl.from_xml".

        Notes:
            None
        """

        self.original_xml = taxonomy_element

        # Clear existing content.
        self.clear_widget()

        # Set the "Yes" radio button to show content.
        self.ui.rbtn_yes.setChecked(True)

        # Populate Keywordtax widget.
        keywtax = taxonomy_element.xpath("keywtax")
        if keywtax:
            self.keywtax.from_xml(taxonomy_element.xpath("keywtax")[0])

        # Populate Taxoncl widget.
        taxoncl = taxonomy_element.xpath("taxoncl")
        if taxoncl:
            self.taxoncl.from_xml(taxoncl[0])


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Taxonomy, "Taxonomy testing")
