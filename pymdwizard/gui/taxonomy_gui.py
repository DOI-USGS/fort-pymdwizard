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
import requests

# Non-standard python libraries.
try:
    import pandas as pd
    from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)
    from PyQt5.QtCore import Qt
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (taxonomy, utils)
    from pymdwizard.gui.ui_files import UI_ITISSearch
except ImportError as err:
    raise ImportError(err, __file__)


class ItisMainForm(QWidget):
    """
    Description:
        A dedicated GUI form for searching the Integrated Taxonomic
        Information System (ITIS). This form allows users to search
        for taxa, select results, and generate the corresponding
        FGDC <taxonomy> XML section.

    Passed arguments:
        xml (lxml.etree._Element): Existing <taxonomy> XML to load.
        fgdc_function (callable): Function to call when XML is
            generated, typically "Taxonomy.from_xml".
        parent (QWidget): Parent widget.

    Returned objects:
        None (The primary output is the call to "fgdc_function")

    Workflow:
        1. Initializes UI and sets up models for search results and
           included taxa.
        2. Connects search, add, remove, and generate buttons to
           their handlers.
        3. Executes ITIS searches via "taxonomy" module functions.
        4. Closes itself after generating and passing the XML.

    Notes:
        Inherits from "QWidget". Uses pandas DataFrames for
        handling table data and requests for network operations.
    """

    # Class attributes.
    drag_label = "Taxonomy"
    acceptable_tags = ["abstract"]

    def __init__(self, xml=None, fgdc_function=None, parent=None):
        """
        Description:
            Initializes the ITIS search form.

        Passed arguments:
            xml (lxml.etree._Element): Existing <taxonomy> XML.
            fgdc_function (callable): Function to receive generated XML.
            parent (QWidget): Parent widget.

        Returned objects:
            None

        Workflow:
            Sets up UI, connects events, initializes table models,
            and loads existing XML data.

        Notes:
            None
        """

        QWidget.__init__(self, parent=parent)
        self.build_ui()
        self.connect_events()

        # Setup DataFrame and Model for selected items (to include).
        self.selected_items_df = pd.DataFrame(columns=["item", "tsn"])
        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)

        # Load existing taxonomy XML.
        self.from_xml(xml)

        # Store the callback function.
        self.fgdc_function = fgdc_function

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets splitter sizes, and sets window icon.

        Notes:
            None
        """

        self.ui = UI_ITISSearch.Ui_ItisSearchWidget()
        self.ui.setupUi(self)

        # Set the relative size of the two splitter panels.
        self.ui.splitter.setSizes([300, 100])

        # Set application icon (utility function assumed).
        utils.set_window_icon(self)

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects search term input, buttons, and table double-clicks
            to their respective methods.

        Notes:
            None
        """

        # Connect search button and Enter key press.
        self.ui.button_search.clicked.connect(self.search_itis)
        self.ui.search_term.returnPressed.connect(self.search_itis)

        # Connect double-click/button to add search results to selection.
        self.ui.table_results.doubleClicked.connect(self.add_tsn)
        self.ui.button_add_taxon.clicked.connect(self.add_tsn)

        # Connect button to generate XML.
        self.ui.button_gen_fgdc.clicked.connect(self.generate_fgdc)

        # Connect double-click/button to remove selected items.
        self.ui.button_remove_selected.clicked.connect(self.remove_selected)
        self.ui.table_include.doubleClicked.connect(self.remove_selected)

    def search_itis(self):
        """
        Description:
            Executes a search against the ITIS database based on the
            term and search type selected in the GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Sets a wait cursor.
            2. Calls either "search_by_scientific_name"`" or
               `search_by_common_name`.
            3. Updates the results table model.
            4. Restores the cursor or displays an error if connection fails.

        Notes:
            None
        """

        # Set cursor to wait state while searching.
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            search_type = str(self.ui.combo_search_type.currentText())
            search_term = str(self.ui.search_term.text())

            # Call appropriate search function based on selection.
            if search_type == "Scientific name":
                results = taxonomy.search_by_scientific_name(
                    search_term
                )
            else:
                results = taxonomy.search_by_common_name(
                    str(self.ui.search_term.text())
                )

            # Update results table model.
            model = utils.PandasModel(results)
            self.ui.table_results.setModel(model)
            QApplication.restoreOverrideCursor()
        except requests.exceptions.ConnectionError:
            QApplication.restoreOverrideCursor()
            msg = "This functionality requires an internet connection."
            msg += "\n Please retry later."
            QMessageBox.information(None,
                                    "No internet connection", msg)
            self.close()

    def add_tsn(self, index):
        """
        Description:
            Adds the currently selected Taxon(s) from the search results
            table to the inclusion table.

        Passed arguments:
            index (QModelIndex): The index double-clicked (ignored).

        Returned objects:
            None

        Workflow:
            1. Identifies the selected row(s) in the results table.
            2. Extracts the "tsn" and item name.
            3. Appends the new item to "selected_items_df".
            4. Updates the model for "table_include".

        Notes:
            Handles both double-click and button press.
        """

        try:
            # Get selected row indexes.
            indexes = self.ui.table_results.selectionModel().selectedRows()
            selected_indices = [int(index.row()) for index in list(indexes)]
            df = self.ui.table_results.model().dataframe()
            indexes = df.index[selected_indices]

            if df.shape[0] == 1:
                index = 0
            elif selected_indices:
                index = selected_indices[0]
            else:
                return

            if "combinedName" in df.columns:
                item_name = df.iloc[index]["combinedName"]
            else:
                try:
                    item_name = str(df.iloc[index]["commonName"])
                except KeyError:
                    msg = "Error, No taxon was selected in the Search "
                    msg += "Results table!"
                    msg += "\nMake sure the ITIS search returned results "
                    msg += "and select one before clicking Add Selection."
                    QMessageBox.information(
                        None, "Problem adding taxon", msg,
                        parent=self
                    )
                    return None

            # Extract TSN and add to the selected items DataFrame.
            tsn = df.iloc[index]["tsn"]
            i = self.selected_items_df.index.max() + 1

            # Get the next index for the selected items DataFrame.
            if pd.isnull(i):
                i = 0

            # Add the new row.
            self.selected_items_df.loc[i] = [str(item_name), tsn]

            # Re-set the model to force refresh and show new item.
            self.selected_model = utils.PandasModel(self.selected_items_df)
            self.ui.table_include.setModel(self.selected_model)
        except AttributeError:
            pass

    def remove_selected(self, index):
        """
        Description:
            Removes the currently selected Taxon(s) from the inclusion
            table.

        Passed arguments:
            index (QModelIndex): The index double-clicked (ignored).

        Returned objects:
            None

        Workflow:
            1. Finds selected rows in the inclusion table.
            2. Drops corresponding indices from "selected_items_df".
            3. Emits a layout change signal for the table model.

        Notes:
            None
        """

        # Get selected row indexes from the inclusion table.
        indexes = self.ui.table_include.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]

        # Get the DataFrame index labels corresponding to selected rows.
        index = self.selected_items_df.index[selected_indices]

        # Drop the selected rows.
        self.selected_items_df.drop(index, inplace=True)

        # Notify the model of the change to refresh the table view.
        self.ui.table_include.model().layoutChanged.emit()

    def generate_fgdc(self):
        """
        Description:
            Generates the FGDC <taxonomy> XML section from the items
            in the inclusion table and calls the provided callback
            function with the resulting XML.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Sets a wait cursor.
            2. Calls "to_xml" to generate the XML.
            3. Calls "self.fgdc_function" with the XML.
            4. Restores the cursor and closes the form.

        Notes:
            None
        """

        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Generate the XML content.
        fgdc_taxonomy = self.to_xml()

        # Call the external function (e.g., Taxonomy.from_xml).
        self.fgdc_function(fgdc_taxonomy)

        QApplication.restoreOverrideCursor()

        msg = "A taxonomy section has been created and added below"
        QMessageBox.information(self, "Taxonomy created", msg)

        self.close()

    def to_xml(self):
        """
        Description:
            Generates the FGDC <taxonomy> XML element based on the
            selected items in the inclusion table.

        Passed arguments:
            None

        Returned objects:
            fgdc_taxonomy (lxml.etree._Element): The complete
                <taxonomy> XML element.

        Workflow:
            1. Extracts the list of names and TSNs from the DataFrame.
            2. Calls "taxonomy.gen_taxonomy_section" to create the XML.

        Notes:
            None
        """

        # Get the current data from the inclusion table model.
        df = self.ui.table_include.model().dataframe()

        # Check if common names should be included in the output.
        include_common = self.ui.check_include_common.isChecked()

        # Generate the taxonomy XML using the utility function.
        fgdc_taxonomy = taxonomy.gen_taxonomy_section(
            keywords=list(df.item),
            tsns=list(df.tsn),
            include_common_names=include_common,
        )

        return fgdc_taxonomy

    def from_xml(self, taxonomy_element):
        """
        Description:
            Parses an existing FGDC <taxonomy> element and populates
            the inclusion table with the taxonomy items (TSNs).

        Passed arguments:
            taxonomy_element (lxml.etree._Element): The existing
                <taxonomy> XML to load.

        Returned objects:
            None

        Workflow:
            1. Finds all <common> tags that start with "TSN: ".
            2. Extracts the TSN and fetches the scientific name using
               "get_full_record_from_tsn".
            3. Populates "selected_items_df" and updates the table model.

        Notes:
            None
        """

        if taxonomy_element is not None:
            i = 0

            # Find common nodes that store the TSN.
            for common_node in taxonomy_element.findall(".//common"):
                if common_node.text.startswith("TSN: "):
                    tsn = common_node.text[5:]

                    # Get the scientific name from the full record.
                    scientific_name = taxonomy.get_full_record_from_tsn(tsn)[
                        "scientificName"
                    ]["combinedName"]

                    # Add to the selected items DataFrame.
                    self.selected_items_df.loc[i] = [scientific_name, tsn]
                    i += 1

            # Update the table model to display the loaded data.
            self.selected_model = utils.PandasModel(self.selected_items_df)
            self.ui.table_include.setModel(self.selected_model)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ItisMainForm, "Itis testing")
