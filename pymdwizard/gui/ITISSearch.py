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
    import pandas as pd
    from PyQt5.QtWidgets import QWidget
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (taxonomy, utils)
    from pymdwizard.gui.ui_files import UI_ITISSearchSimple
except ImportError as err:
    raise ImportError(err, __file__)


class ItisSearch(QWidget):
    """
    Description:
        A widget providing a search interface for the Integrated
        Taxonomic Information System (ITIS) to retrieve and select
        taxonomic serial numbers (TSNs). Inherits from QWidget.

    Passed arguments:
        table (QTableView, optional): The QTableView widget in the
            parent form where selected TSNs should be added.
        selected_items_df (pd.DataFrame, optional): The DataFrame
            holding currently selected items, which will be updated.
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes the UI and connects search/selection events.
        2. Allows searching ITIS by scientific or common name.
        3. Users select results, which are added to the
           "selected_items_df" and updated in the parent "table".

    Notes:
        None
    """

    def __init__(self, table=None, selected_items_df=None, parent=None):
        # Initialize the parent QWidget class (PEP8 prefers super()).
        super(self.__class__, self).__init__()

        # Setup UI and events.
        self.build_ui()
        self.connect_events()

        # Store references to external objects.
        self.table_include = table
        self.selected_items_df = selected_items_df

        # Set the window icon.
        utils.set_window_icon(self)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates and sets up the UI elements.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_ITISSearchSimple.Ui_ItisSearchWidget()
        self.ui.setupUi(self)

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
            Connects search button click/Enter press to "search_itis",
            double-click/Add button to "add_tsn", and Close button to
            "close".

        Notes:
            None
        """

        # Connect search trigger events.
        self.ui.button_search.clicked.connect(self.search_itis)
        self.ui.search_term.returnPressed.connect(self.search_itis)

        # Connect selection trigger events.
        self.ui.table_results.doubleClicked.connect(self.add_tsn)
        self.ui.btn_add_taxon.clicked.connect(self.add_tsn)

        # Connect window close event.
        self.ui.btn_close.clicked.connect(self.close)

    def search_itis(self):
        """
        Description:
            Executes a search against the ITIS database based on the
            selected search type and term, and displays results.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Reads the search type and term from the UI.
            2. Calls the appropriate "taxonomy" module function.
            3. Populates the results table using a "PandasModel".

        Notes:
            None
        """

        # Retrieve values from widgets.
        search_type = str(self.ui.combo_search_type.currentText())
        search_term = str(self.ui.search_term.text())

        # Determine which search function to call
        if search_type == "Scientific name":
            results = taxonomy.search_by_scientific_name(search_term)
        else:
            results = taxonomy.search_by_common_name(search_term)

        # Create and set the model for the results table.
        model = utils.PandasModel(results)
        self.ui.table_results.setModel(model)

    def add_tsn(self, index):
        """
        Description:
            Adds the currently selected taxonomic serial number (TSN)
            and name to the "selected_items_df" and updates the
            parent table display.

        Passed arguments:
            index (QModelIndex, optional): The index of the item that
                was double-clicked (unused in selection logic).

        Returned objects:
            None

        Workflow:
            1. Retrieves the indices of selected rows from the results
               table.
            2. Loops through selected items, extracts the combined
               name/common name and TSN.
            3. Appends the data to the "selected_items_df".
            4. Updates the model of the parent "table_include".

        Notes:
            None
        """

        # Get the row indices of selected items.
        indexes = self.ui.table_results.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]

        # Get the underlying DataFrame from the model.
        df = self.ui.table_results.model().dataframe()

        # Get the actual data indices from the selected row indices.
        data_indices = df.index[selected_indices]

        # Process each selected item.
        for index in data_indices:
            # Determine the item name (prioritize combinedName).
            if "combinedName" in df.columns:
                item_name = df.iloc[index]["combinedName"]
            else:
                item_name = str(df.iloc[index]["commonName"])

            # Get the Taxonomic Serial Number (TSN).
            tsn = df.iloc[index]["tsn"]

            # Determine the next available index for the target DataFrame.
            i = self.selected_items_df.index.max() + 1
            i = 0 if pd.isnull(i) else i + 1

            # Append the new row to the target DataFrame.
            self.selected_items_df.loc[i] = [str(item_name), tsn]

        # Update the model of the external table.
        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.table_include.setModel(self.selected_model)

    def close(self):
        """
        Description:
            Closes the widget, deleting it safely from the memory.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls deleteLater() to safely destroy the QWidget.

        Notes:
            None
        """

        self.deleteLater()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ItisSearch, "Itis testing")
