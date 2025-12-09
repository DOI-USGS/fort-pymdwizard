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
import webbrowser

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QMessageBox, QDialog, QProgressDialog)
    from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QFont)
    from PyQt5.QtCore import (Qt, QThread, pyqtSignal)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_ThesaurusSearch
except ImportError as err:
    raise ImportError(err, __file__)


class SearchThread(QThread):
    """
    Description:
        A worker thread used to perform thesaurus search queries
        asynchronously, preventing the main GUI thread from freezing.

    Passed arguments:
        dialog_instance (ThesaurusSearch): Reference to the main dialog.
        populate_lookup_function (callable): Method to ensure thesauri
            lookup is populated.
        search_term (str): The term to search for.
        selected_thesaurus_name (str): Name of the thesaurus to search,
            or "All".
        parent (QObject): Parent Qt object.

    Returned objects:
        finished (pyqtSignal(list)): Signal emitted upon completion,
            containing a list of search results.

    Workflow:
        1. Calls "populate_lookup_function" to initialize thesaurus data.
        2. Calls "dialog_instance.search_all_thesauri" to execute the
           network request and search logic.
        3. Emits results via the "finished" signal.

    Notes:
        Inherits from "QThread".
    """

    finished = pyqtSignal(list)

    def __init__(
            self,
            dialog_instance,
            populate_lookup_function,
            search_term,
            selected_thesaurus_name,
            parent=None
    ):

        # Initialize the parent QThread.
        super(SearchThread, self).__init__(parent)
        self.dialog_instance = dialog_instance
        self.populate_lookup_function = populate_lookup_function
        self.search_term = search_term

        # Store the selected thesaurus name for filtering.
        self.selected_thesaurus_name = selected_thesaurus_name

    def run(self):
        """
        Description:
            Execute the search and emit the results.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Executes the search logic in the background.

        Notes:
            None
        """

        # Ensure the thesaurus lookup data is loaded.
        if not self.populate_lookup_function():
            self.finished.emit([])
            return

        # Call the main dialog's search method.
        all_results = self.dialog_instance.search_all_thesauri(
            self.search_term, self.selected_thesaurus_name
        )

        # Emit the results to the main thread.
        self.finished.emit(all_results)

class ThesaurusSearch(QDialog):
    """
    Description:
        A dialog for searching USGS controlled vocabularies and selecting
        terms to add to the metadata.

    Passed arguments:
        add_term_function (callable): Function in the parent widget to
            call when a term is selected/added.
        parent (QWidget): Parent widget.
        place (bool): If True, prioritize "Place" keywords; otherwise,
            prioritize "Theme" keywords.

    Returned objects:
        None

    Workflow:
        1. Initializes UI, loads thesaurus lookup data via API.
        2. Manages search execution via "SearchThread".
        3. Displays search results in a tree view and term details in
           a text browser.
        4. Calls "add_term_function" when a term is selected.

    Notes:
        Inherits from "QDialog". Uses "requests_pem_get" for network calls.
    """

    def __init__(self, add_term_function=None, parent=None, place=False):

        # Initialize the parent QDialog.
        super(self.__class__, self).__init__(parent=parent)

        self.build_ui()

        self.thesauri_lookup = {}
        self.thesauri_lookup_r = {}

        # Load thesaurus codes and names.
        self.populate_thesauri_lookup()
        self.connect_events()

        self.add_term_function = add_term_function

        self.place = place

        # Set the window icon using a utility function.
        utils.set_window_icon(self)

    def load_iso(self):
        """
        Description:
            Configures the dialog specifically for loading and displaying
            ISO 19115 Topic Categories without an active search.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Hides search controls, makes an API call for ISO terms, and
            populates the tree view.

        Notes:
            This function is typically used when the dialog is invoked
            to manage the ISO keywords tab.
        """

        # Hide search components.
        self.ui.label_search_term.hide()
        self.ui.search_term.hide()
        self.ui.button_search.hide()

        # Update results label.
        self.ui.label_search_results.text = "ISO 19115 Topic Categories"

        self.populate_thesauri_lookup()

        # API URL for ISO 19115 Topic Category terms.
        iso_url = (
            "https://apps.usgs.gov/thesaurus/term.php?thcode=15&"
            "text=ISO 19115 Topic Category"
        )
        results = utils.requests_pem_get(iso_url).json()

        # Create the top-level branch for the thesaurus.
        thesaurus_name = "ISO 19115 Topic Category"
        branch = QStandardItem(thesaurus_name)
        branch.setFont(QFont("Arial", 11))

        # Populate with narrower terms (nt).
        for item in results["nt"]:
            childnode = QStandardItem(item["name"])
            childnode.setFont(QFont("Arial", 9))
            branch.appendRow([childnode])

        model = QStandardItemModel(0, 0)

        # Append the branch to the root of the model.
        rootNode = model.invisibleRootItem()
        rootNode.appendRow(branch)

        self.ui.treeview_results.setModel(model)

        # Display all results.
        self.ui.treeview_results.expandAll()

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI and configures the "QTextBrowser" to handle
            links internally.

        Notes:
            None
        """

        self.ui = UI_ThesaurusSearch.Ui_ThesaurusSearch()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Prevent automatic opening of external links.
        self.ui.textBrowser.setOpenLinks(False)
        self.ui.textBrowser.setOpenExternalLinks(False)

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects search button, tree view clicks/double clicks, add
            term button, close button, and details anchor clicks.

        Notes:
            None
        """

        # Connect search button to search method.
        self.ui.button_search.clicked.connect(self.search_thesaurus)

        # Connect double-click in results to add term.
        self.ui.treeview_results.doubleClicked.connect(self.add_term)

        # Connect single-click in results to show details.
        self.ui.treeview_results.clicked.connect(self.show_details)

        # Connect buttons.
        self.ui.btn_add_term.clicked.connect(self.add_term)
        self.ui.btn_close.clicked.connect(self.close_form)

        # Connect anchor clicks in the details pane to custom handler.
        self.ui.textBrowser.anchorClicked.connect(self.text_clicked)

    def show_details(self, index):
        """
        Description:
            Fetches and displays detailed information for the clicked
            thesaurus or term in the "QTextBrowser".

        Passed arguments:
            index (QModelIndex): The index of the item clicked in the
                tree view.

        Returned objects:
            None

        Workflow:
            1. Determines if the click is on a thesaurus branch or a term.
            2. Fetches details using the appropriate API URL (thesaurus
               details or term details).
            3. Formats and displays the HTML-based details, including
               related terms (BT, NT, RT).

        Notes:
            Uses HTML for rich text formatting.
        """

        clicked_item = self.ui.treeview_results.model().itemFromIndex(index)
        parent = clicked_item.parent()
        details_msg = ""

        # --- Clicked on a Thesaurus Branch ---
        if clicked_item.hasChildren():
            thcode = self.thesauri_lookup_r[clicked_item.text()]
            thname = clicked_item.text()

            THESAURUS_DETAILS_URL = (
                "https://apps.usgs.gov/thesaurus/thesaurus.php?"
                "format=json&thcode={}"
            )
            thesaurus_details_url = THESAURUS_DETAILS_URL.format(thcode)
            details = utils.requests_pem_get(thesaurus_details_url).json()

            # Format thesaurus details message.
            details_msg += (
                f'<b><font size="5" face="arial">{thname}</font></b><br>'
            )
            uri = (
                "https://apps.usgs.gov/thesaurus/about/thesaurus-full.php?"
                f"thcode={thcode}"
            )
            if uri:
                details_msg += (
                    f'<a href="{uri}"><u><i><font size="4" '
                    'face="arial" style="color:#386EC4">'
                    f"{uri}</font></i></u></a><br><br>"
                )

            details_msg += details["vocabulary"]["scope"]

        # --- Clicked on a Term/Keyword ---
        else:
            thcode = self.thesauri_lookup_r[parent.text()]
            # Strip '(use: ...)' part for search
            item_text = clicked_item.text().split(" (use: ")[0]
            details_url = (
                "https://apps.usgs.gov/thesaurus/term.php?"
                f"thcode={thcode}&text={quote(item_text)}"
            )

            try:
                details = utils.requests_pem_get(details_url).json()
                if isinstance(details, dict):
                    details = [details]

                search_term = self.ui.search_term.text()
                prefered_shown = False

                for detail in details:
                    term = detail["term"]
                    uf = detail["uf"]
                    bt = detail["bt"]
                    nt = detail["nt"]
                    rt = detail["rt"]

                    # Display if the user searched for a non-preferred term.
                    if (
                            term["name"].lower() != search_term
                            and not prefered_shown
                    ):
                        term_count = 0
                        prefered_shown = True
                        for alt_term in uf:
                            if alt_term["name"].lower() in search_term.lower():
                                term_count += 1
                                if term_count == 1:
                                    details_msg += (
                                        "The query matches the following "
                                        "non-preferred terms: "
                                    )
                                else:
                                    details_msg += ", "
                                details_msg += (
                                    f"<u>{alt_term['name']}</u>"
                                )

                        if term_count > 0:
                            details_msg += "<br><br>"

                    # Display the preferred term details.
                    details_msg += (
                        f'<b><font size="5" face="arial">{term["name"]}'
                        f'</font></b><br>'
                    )
                    details_msg += (
                        f'<font size="4" face="arial">{term["scope"]}'
                        f'<br><br>'
                    )

                    # Display Broader Terms (BT).
                    if bt:
                        details_msg += "Broader terms: "
                        details_msg += " > ".join(
                            [
                                f'<a href="{item["name"]}"><u>'
                                f'{item["name"]}</u></a>'
                                for item in bt[::-1]
                            ]
                        )
                        details_msg += "<br>"

                    # Display Narrower Terms (NT).
                    if nt:
                        details_msg += " Narrower terms: "
                        details_msg += ", ".join(
                            [
                                f'<a href="{item["name"]}"><u>'
                                f'{item["name"]}</u></a>'
                                for item in nt
                            ]
                        )
                        details_msg += "<br>"

                    # Display Related Terms (RT).
                    if rt:
                        details_msg += " Related terms: "
                        details_msg += ", ".join(
                            [
                                f'<a href="{item["name"]}"><u>'
                                f'{item["name"]}</u></a>'
                                for item in rt
                            ]
                        )
                        details_msg += "<br>"
            except Exception:
                details_msg = "Error getting details."

        self.ui.textBrowser.setText(details_msg)

    def populate_thesauri_lookup(self):
        """
        Description:
            Fetches the list of all available thesauri from the USGS API
            and populates the internal lookup dictionaries.

        Passed arguments:
            None

        Returned objects:
            bool: True if lookup was successfully populated or already
                exists, False otherwise (e.g., connection error).

        Workflow:
            1. Checks if "thesauri_lookup" is empty.
            2. Fetches data from the API.
            3. Populates forward ("thcode" -> "name") and reverse
               ("name" -> "thcode") lookups.
            4. Calls "populate_thesaurus_dropdown".

        Notes:
            None
        """

        if not self.thesauri_lookup:
            url = (
                "https://apps.usgs.gov/thesaurus/thesaurus.php?"
                "format=json"
            )
            result = self.get_result(url)

            if result is not None:
                # Populate forward lookup (thcode -> name).
                self.thesauri_lookup = {
                    i["thcode"]: i["name"] for i in result["vocabulary"]
                }
                # Populate reverse lookup (name -> thcode).
                self.thesauri_lookup_r = {
                    i["name"]: i["thcode"] for i in result["vocabulary"]
                }
                self.populate_thesaurus_dropdown()
                return True
            else:
                return False
        return True

    def populate_thesaurus_dropdown(self):
        """
        Description:
            Populates the thesaurus selection dropdown with all
            available thesauri names plus the "All" option.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears dropdown, adds "All", adds thesaurus names from
            lookup, and sets the default selection (code "2")..

        Notes:
            None
        """

        # Clear existing items.
        self.ui.thesaurus_dropdown.clear()

        # Add the option to search all thesauri.
        self.ui.thesaurus_dropdown.addItem("All")

        # Add each thesaurus name from the lookup.
        for name in self.thesauri_lookup.values():
            self.ui.thesaurus_dropdown.addItem(name)

        # Set default value to thesaurus code "2" (often "USGS GeoData").
        if "2" in self.thesauri_lookup:
            thesaurus_name = self.thesauri_lookup["2"]
            index = self.ui.thesaurus_dropdown.findText(thesaurus_name)
            if index != -1:
                self.ui.thesaurus_dropdown.setCurrentIndex(index)

    def get_result(self, url):
        """
        Description:
            A wrapper for making API GET requests, handling connection
            errors and returning JSON content.

        Passed arguments:
            url (str): The API endpoint URL to query.

        Returned objects:
            dict or None: The parsed JSON response, or None if an
                error occurred.

        Workflow:
            Uses "utils.requests_pem_get" (assuming it handles SSL/PEM
            certificates) and catches connection errors, showing a warning.

        Notes:
            None
        """

        try:
            return utils.requests_pem_get(url).json()
        except requests.exceptions.ConnectionError:
            msg = (
                "We're having trouble connecting to the controlled "
                "vocabularies service"
            )
            msg += "\n Check that you have an internet connect, or "
            msg += "try again later"
            QMessageBox.warning(self, "Connection error", msg)
            self.close_form()

            return None

    def search_thesaurus(self):
        """
        Description:
            Initiates the asynchronous thesaurus search via "SearchThread".

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Gets the search term and selected thesaurus name.
            2. Creates and configures a modal "QProgressDialog".
            3. Initializes and starts "SearchThread" with search parameters.
            4. Connects the thread's "finished" signal to
               "on_search_finished".
            5. Shows the progress dialog.

        Notes:
            None
        """

        term = self.ui.search_term.text()

        # Get the selected thesaurus from the dropdown.
        selected_thesaurus_name = self.ui.thesaurus_dropdown.currentText()

        # Create a non-cancelable progress dialog
        progress = QProgressDialog(
            "Searching thesaurus...", "Cancel", 0, 0, self
        )

        # Configure progress dialog flags (no help/close button, stays on top)
        flags = progress.windowFlags()

        # Remove context help button and close button.
        flags &= ~Qt.WindowContextHelpButtonHint
        flags &= ~Qt.WindowCloseButtonHint

        # Set the modified flags.
        progress.setWindowFlags(flags | Qt.WindowStaysOnTopHint)

        progress.setWindowTitle(" ")
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)  # Disable the cancel button
        progress.setValue(0)

        # Start the worker thread.
        self.thread = SearchThread(
            self,
            self.populate_thesauri_lookup,
            term,
            selected_thesaurus_name,
            self,
        )

        # Connect finished signal to handler.
        self.thread.finished.connect(
            lambda all_results: self.on_search_finished(
                all_results, progress, selected_thesaurus_name
            )
        )
        self.thread.start()

        # Show the progress dialog while the search is processing.
        progress.exec_()

    def on_search_finished(self, all_results, progress,
                           selected_thesaurus_name):
        """
        Description:
            Handles the results returned by "SearchThread".

        Passed arguments:
            all_results (list): List of search results.
            progress (QProgressDialog): The progress dialog instance.
            selected_thesaurus_name (str): The name of the thesaurus
                that was searched.

        Returned objects:
            None

        Workflow:
            Closes the progress dialog, checks for empty results, and
            calls "process_thesaurus_results" if results are found.

        Notes:
            None
        """

        # Close the progress dialog.
        progress.close()

        if not all_results:
            msg = (
                "The Metadata Wizard was unable to locate the provided "
                "search term in the controlled vocabulary search\n\n'"
                f"{self.ui.search_term.text()}' Not Found"
            )
            QMessageBox.information(
                self, "Search Term Not Found", msg, QMessageBox.Ok
            )
            return

        # Process and display the results.
        self.process_thesaurus_results(all_results)

    def search_all_thesauri(self, term, selected_thesaurus_name):
        """
        Description:
            Searches the specified thesaurus(i) for the term using API calls.

        Passed arguments:
            term (str): The term to be searched.
            selected_thesaurus_name (str): The selected thesaurus name,
                or 'All'.

        Returned objects:
            list: A list of results from the thesaurus search(es).

        Workflow:
            Iterates through relevant thesauri (all or just the
            selected one), constructs the API URL, and aggregates results.

        Notes:
            This method runs in the "SearchThread".
        """

        all_results = []

        # Determine which thesaurus(i) to search.
        if selected_thesaurus_name == "All":
            thesauri_to_search = self.thesauri_lookup.items()
        else:
            thesauri_to_search = [
                (thcode, name)
                for thcode, name in self.thesauri_lookup.items()
                if name == selected_thesaurus_name
            ]

        for thcode, name in thesauri_to_search:
            # Construct the search URL.
            search_url = (
                f"https://apps.usgs.gov/thesaurus/term-search.php?"
                f"thcode={thcode}&term={term}&rel=contains"
            )

            # Get results from the current thesaurus.
            try:
                results = self.get_result(search_url)
            except Exception:
                results = []

            if results is None:
                # Connection error handled in get_result, but return here.
                return []

            if results:
                all_results.extend(results)

        return all_results

    def process_thesaurus_results(self, results):
        """
        Description:
            Processes the API search results, structuring them into a
            tree model for display in the UI.

        Passed arguments:
            results (list): A list of results obtained from the API.

        Returned objects:
            None

        Workflow:
            1. Groups results by thesaurus name.
            2. Creates "QStandardItem" nodes for each thesaurus and term.
            3. Sets the new "QStandardItemModel" on the tree view.

        Notes:
            "self.branch_lookup" stores the top-level QStandardItem
            for each thesaurus.
        """

        self.branch_lookup = {}
        unique_children = []

        try:
            for item in results:
                thesaurus_name = self.thesauri_lookup[item["thcode"]]
                thcode = item["thcode"]

                # Filter out Theme/Place keywords based on self.place flag.
                is_valid = (
                        thcode != "1" and not self.place
                        or thcode == "1" and self.place
                )

                if is_valid:
                    # Get or create the thesaurus branch node.
                    branch = self.branch_lookup.get(
                        thesaurus_name, QStandardItem(thesaurus_name)
                    )
                    branch.setFont(QFont("Arial", 11))

                    # Create the term child node, adding '(use: ...)' if needed.
                    if item["label"] != item["value"]:
                        childnode = QStandardItem(
                            f"{item['label']} (use: {item['value']})"
                        )
                    else:
                        childnode = QStandardItem(item["label"])

                    branch.appendRow([childnode, None])

                    childnode.setFont(QFont("Arial", 9))
                    # Track unique children to avoid repetition.
                    if (thesaurus_name, item["value"]) not in unique_children:
                        unique_children.append(
                            (thesaurus_name, item["value"])
                        )

                    self.branch_lookup[thesaurus_name] = branch

            # Setup the final model.
            model = QStandardItemModel(0, 0)
            rootNode = model.invisibleRootItem()

            # Append all thesaurus branches to the root.
            for thesaurus_node in self.branch_lookup.values():
                rootNode.appendRow(thesaurus_node)

            self.ui.treeview_results.setModel(model)
            self.ui.treeview_results.expandAll()

        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                "An error occurred retrieving values from the "
                f"controlled vocabulary search: {str(e)}",
            )

    def get_thesaurus(self):
        """
        Description:
            Retrieves the thesaurus name associated with the currently
            selected term in the tree view.

        Passed arguments:
            None

        Returned objects:
            str or None: The thesaurus name (parent node text) or None
                if a thesaurus branch is selected.

        Workflow:
            Gets the parent of the selected item.

        Notes:
            None
        """

        model = self.ui.treeview_results.model()
        for i in self.ui.treeview_results.selectedIndexes():
            clicked_item = model.itemFromIndex(i)
            parent = clicked_item.parent()
            keyword = clicked_item.text()

            # If the clicked item has children, it is a branch (thesaurus).
            if clicked_item.hasChildren():
                return None
            else:
                thesaurus = parent.text()

                # Return the parent's text (thesaurus name).
                return thesaurus

    def add_term(self, index):
        """
        Description:
            Adds the accepted keyword(s) from the selected term to the
            parent widget's keyword list via the callback function.

        Passed arguments:
            index (QModelIndex): The index of the item selected.

        Returned objects:
            None

        Workflow:
            1. Identifies the selected term and its thesaurus.
            2. Extracts the preferred term, handling (use: ...) syntax.
            3. Calls self.add_term_function for each accepted term.

        Notes:
            None
        """

        model = self.ui.treeview_results.model()
        for i in self.ui.treeview_results.selectedIndexes():
            clicked_item = model.itemFromIndex(i)
            parent = clicked_item.parent()
            keyword = clicked_item.text()

            if clicked_item.hasChildren():
                pass
            else:
                thesaurus = parent.text()

                # Check for "use" syntax for non-preferred terms.
                if " (use: " in keyword:
                    to_use = keyword.split(" (use: ")[1][:-1]
                    accepted_terms = to_use.split(" AND ")
                else:
                    accepted_terms = [keyword]

                # Call the parent function for each accepted term.
                for keyword in accepted_terms:
                    if keyword:
                        self.add_term_function(keyword=keyword,
                                               thesaurus=thesaurus)

    def text_clicked(self, link):
        """
        Description:
            Handles clicks within the details "QTextBrowser".
            If a standard URL is clicked, opens it externally. If a
            term link is clicked, it initiates a new search for that term.

        Passed arguments:
            link (QUrl): The URL associated with the clicked anchor.

        Returned objects:
            None

        Workflow:
            1. Checks if the link is an external URL; if so, opens browser.
            2. Otherwise, treats the link text as a new search term.
            3. Initiates a new search and attempts to select the term.

        Notes:
            None
        """

        parent = self.get_thesaurus()

        # Check if the link is an external URL (starts with "http").
        if link.url().startswith("http"):
            # Open the URL in the system's web browser.
            webbrowser.open(link.url(), new=0, autoraise=True)
            return
        else:
            self.ui.search_term.setText(link.url())

        # Execute the search for the new term.
        self.search_thesaurus()

        if parent is None:
            return

        # Try to select the item in the tree view.
        parent_item = self.branch_lookup[parent]

        model = self.ui.treeview_results.model()
        for irow in range(parent_item.rowCount()):
            child = parent_item.child(irow)
            if child.text() == link.url():
                # Select the item and show its details.
                self.ui.treeview_results.setCurrentIndex(child.index())
                self.show_details(child.index())

    def close_form(self):
        """
        Description:
            Closes the dialog and cleans up references.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets parent to None, uses "deleteLater", and calls close().

        Notes:
            None
        """

        self.parent = None
        self.deleteLater()
        self.close()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ThesaurusSearch, "Thesaurus Search testing")
