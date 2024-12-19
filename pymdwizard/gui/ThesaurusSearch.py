#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

import requests


from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_ThesaurusSearch

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

class SearchThread(QThread):
    """Thread for searching the thesaurus."""
    finished = pyqtSignal(list)

    def __init__(self, dialog_instance, populate_lookup_function, search_term, selected_thesaurus_name, parent=None):
        super(SearchThread, self).__init__(parent)
        self.dialog_instance = dialog_instance
        self.populate_lookup_function = populate_lookup_function
        self.search_term = search_term
        self.selected_thesaurus_name = selected_thesaurus_name  # Add this line

    def run(self):
        """Execute the search and emit the results."""
        if not self.populate_lookup_function():
            self.finished.emit([])
            return
        
        # Call the search_all_thesauri method from the dialog instance
        all_results = self.dialog_instance.search_all_thesauri(self.search_term, self.selected_thesaurus_name)  # Update this line
        self.finished.emit(all_results)

class ThesaurusSearch(QDialog):
    def __init__(self, add_term_function=None, parent=None, place=False):
        super(self.__class__, self).__init__(parent=parent)

        self.build_ui()

        self.thesauri_lookup = {}
        self.thesauri_lookup_r = {}
        self.populate_thesauri_lookup()
        self.connect_events()

        self.add_term_function = add_term_function

        self.place = place

        utils.set_window_icon(self)

    def load_iso(self):
        self.ui.label_search_term.hide()
        self.ui.search_term.hide()
        self.ui.button_search.hide()
        self.ui.label_search_results.text = "ISO 19115 Topic Categories"

        self.populate_thesauri_lookup()

        iso_url = "https://apps.usgs.gov/thesaurus/term.php?thcode=15&text=ISO 19115 Topic Category"
        results = utils.requests_pem_get(iso_url).json()

        thesaurus_name = "ISO 19115 Topic Category"
        branch = QStandardItem(thesaurus_name)
        branch.setFont(QFont("Arial", 11))
        for item in results["nt"]:
            childnode = QStandardItem(item["name"])
            childnode.setFont(QFont("Arial", 9))
            branch.appendRow([childnode])

        model = QStandardItemModel(0, 0)

        rootNode = model.invisibleRootItem()
        rootNode.appendRow(branch)

        self.ui.treeview_results.setModel(model)
        self.ui.treeview_results.expandAll()

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_ThesaurusSearch.Ui_ThesaurusSearch()
        self.ui.setupUi(self)
        self.ui.textBrowser.setOpenLinks(False)
        self.ui.textBrowser.setOpenExternalLinks(False)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.button_search.clicked.connect(self.search_thesaurus)
        # self.ui.search_term.returnPressed.connect(self.search_thesaurus)
        self.ui.treeview_results.doubleClicked.connect(self.add_term)
        self.ui.treeview_results.clicked.connect(self.show_details)
        self.ui.btn_add_term.clicked.connect(self.add_term)
        self.ui.btn_close.clicked.connect(self.close_form)
        self.ui.textBrowser.anchorClicked.connect(self.text_clicked)

    def show_details(self, index):
        clicked_item = self.ui.treeview_results.model().itemFromIndex(index)
        parent = clicked_item.parent()

        if clicked_item.hasChildren():
            thcode = self.thesauri_lookup_r[clicked_item.text()]
            thname = clicked_item.text()

            THESAURUS_DETAILS_URL = (
                "https://apps.usgs.gov/thesaurus/thesaurus.php?format=json&thcode={}"
            )
            thesaurus_details_url = THESAURUS_DETAILS_URL.format(thcode)
            details = utils.requests_pem_get(thesaurus_details_url).json()

            details_msg = ""
            details_msg += '<b><font size="5" face="arial">{}</font></b><br>'.format(
                thname
            )
            # uri = details['vocabulary']['uri']
            uri = "https://apps.usgs.gov/thesaurus/about/thesaurus-full.php?thcode={}".format(
                thcode
            )
            if uri:
                details_msg += '<a href="{}"><u><i><font size="4" face="arial" style="color:#386EC4">{}</font></i></u></a><br><br>'.format(
                    uri, uri
                )

            details_msg += details["vocabulary"]["scope"]
        else:
            thcode = self.thesauri_lookup_r[parent.text()]
            item_text = clicked_item.text().split(" (use: ")[0]
            details_url = "https://apps.usgs.gov/thesaurus/term.php?thcode={}&text={}".format(
                thcode, quote(item_text)
            )

            try:
                details = utils.requests_pem_get(details_url).json()
                if type(details) == dict:
                    details = [details]

                details_msg = ""
                search_term = self.ui.search_term.text()
                prefered_shown = False
                for detail in details:

                    term = detail["term"]
                    uf = detail["uf"]
                    bt = detail["bt"]
                    nt = detail["nt"]
                    rt = detail["rt"]

                    if term["name"].lower() != search_term and not prefered_shown:
                        term_count = 0
                        prefered_shown = True
                        for alt_term in uf:
                            if alt_term["name"].lower() in search_term.lower():
                                term_count += 1
                                if term_count == 1:
                                    details_msg += "The query matches the following non-preferred terms: "
                                else:
                                    details_msg += ", "
                                details_msg += "<u>{}</u>".format(alt_term["name"])

                        if term_count > 0:
                            details_msg += "<br><br>"

                    details_msg += '<b><font size="5" face="arial">{}</font></b><br>'.format(
                        term["name"]
                    )
                    details_msg += '<font size="4" face="arial">{}<br><br>'.format(
                        term["scope"]
                    )

                    if bt:
                        details_msg += "Broader terms: "
                        details_msg += " > ".join(
                            [
                                '<a href="{0}"><u>{0}</u></a>'.format(item["name"])
                                for item in bt[::-1]
                            ]
                        )
                        details_msg += "<br>"

                    if nt:
                        details_msg += " Narrower terms: "
                        details_msg += ", ".join(
                            [
                                '<a href="{0}"><u>{0}</u></a>'.format(item["name"])
                                for item in nt
                            ]
                        )
                        details_msg += "<br>"

                    if rt:
                        details_msg += " Related terms: "
                        details_msg += ", ".join(
                            [
                                '<a href="{0}"><u>{0}</u></a>'.format(item["name"])
                                for item in rt
                            ]
                        )
                        details_msg += "<br>"
            except:
                details_msg = "error getting details"

        self.ui.textBrowser.setText(details_msg)

    def populate_thesauri_lookup(self):
        if not self.thesauri_lookup:
            url = "https://apps.usgs.gov/thesaurus/thesaurus.php?format=json"
            result = self.get_result(url)
            if result is not None:
                self.thesauri_lookup = {
                    i["thcode"]: i["name"] for i in result["vocabulary"]
                }
                self.thesauri_lookup_r = {
                    i["name"]: i["thcode"] for i in result["vocabulary"]
                }
                self.populate_thesaurus_dropdown()  # Populate the dropdown
                return True
            else:
                return False
        return True

    def populate_thesaurus_dropdown(self):
        """Populate the thesaurus dropdown with thesauri names."""
        self.ui.thesaurus_dropdown.clear()  # Clear existing items

        self.ui.thesaurus_dropdown.addItem('All')

        for name in self.thesauri_lookup.values():
            self.ui.thesaurus_dropdown.addItem(name)  # Add each thesaurus name to the dropdown

        # Set the current value to the thesaurus code 2 if it exists
        if '2' in self.thesauri_lookup:
            thesaurus_name = self.thesauri_lookup['2']
            index = self.ui.thesaurus_dropdown.findText(thesaurus_name)
            if index != -1:  # Check if the item is found
                self.ui.thesaurus_dropdown.setCurrentIndex(index)  # Set the current index

    def get_result(self, url):
        try:
            return utils.requests_pem_get(url).json()
        except requests.exceptions.ConnectionError:
            msg = (
                "We're having trouble connecting to the controlled vocabularies service"
            )
            msg += "\n Check that you have an internet connect, or try again later"
            QMessageBox.warning(self, "Connection error", msg)
            self.close_form()

    def search_thesaurus(self):
        """
        Searches the thesaurus for a term based on the selected thesaurus
        in the thesaurus_dropdown.
        
        Returns:
            bool: True if search completed successfully, False if an error occurred.
        """
        term = self.ui.search_term.text()

        # Retrieve the selected thesaurus from the dropdown
        selected_thesaurus_name = self.ui.thesaurus_dropdown.currentText()

        # Create a progress dialog
        progress = QProgressDialog("Searching thesaurus...", "Cancel", 0, 0, self)

        # Get current window flags
        flags = progress.windowFlags()
        # Remove context help button and close button
        flags &= ~Qt.WindowContextHelpButtonHint
        flags &= ~Qt.WindowCloseButtonHint
        # Set the modified flags
        progress.setWindowFlags(flags | Qt.WindowStaysOnTopHint)

        progress.setWindowTitle(" ")
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)  # Disable the cancel button
        progress.setValue(0)

        # Start the worker thread
        self.thread = SearchThread(self, self.populate_thesauri_lookup, term,  selected_thesaurus_name, self)
        
        # Connect finished signal with modified logic
        self.thread.finished.connect(lambda all_results: self.on_search_finished(all_results, progress, selected_thesaurus_name))
        self.thread.start()

        # Show the progress dialog while the search is processing
        progress.exec_()

    def on_search_finished(self, all_results, progress, selected_thesaurus_name):
        """Handle the search results after the thread has finished."""
        progress.close()  # Close the progress dialog

        if not all_results:
            msg = f"The Metadata Wizard was unable to locate the provided search term in the controlled vocabulary search\n\n'{self.ui.search_term.text()}' Not Found"
            QMessageBox.information(self, "Search Term Not Found", msg, QMessageBox.Ok)
            return

        self.process_thesaurus_results(all_results)

    def search_all_thesauri(self, term, selected_thesaurus_name):
        """
        Searches the selected thesaurus for the specified term.
        
        Args:
            term (str): The term to be searched in the thesaurus.
            selected_thesaurus_name (str): The selected thesaurus name.

        Returns:
            list: A list of results retrieved from the thesaurus; can be empty if no matches found.
        """
        all_results = []
        
        # If 'All' is selected, search all thesauri
        if selected_thesaurus_name == 'All':
            for thcode in self.thesauri_lookup.keys():
                search_url = f"https://apps.usgs.gov/thesaurus/term-search.php?thcode={thcode}&term={term}&rel=contains"
                
                # Get results from the current thesaurus search
                try:
                    results = self.get_result(search_url)
                except:
                    results = []

                if results is None:
                    return []  # Return empty list if there's an error
                
                if results:  # Append results if found
                    all_results.extend(results)
        else:
            # Only search in the specified thesaurus
            for thcode, name in self.thesauri_lookup.items():
                if name == selected_thesaurus_name:
                    search_url = f"https://apps.usgs.gov/thesaurus/term-search.php?thcode={thcode}&term={term}&rel=contains"
                    
                    # Get results from the current thesaurus search
                    try:
                        results = self.get_result(search_url)
                    except:
                        results = []

                    if results is None:
                        return []  # Return empty list if there's an error
                    
                    if results:  # Append results if found
                        all_results.extend(results)

        return all_results

    def process_thesaurus_results(self, results):
        """
        Processes the search results from the thesaurus and updates the UI.

        This function takes the results list, organizes the data, and updates the
        branch lookup to display results in the application's tree view.

        Args:
            results (list): A list of results obtained from searching the thesaurus.
        """
        self.branch_lookup = {}
        unique_children = []

        try:
            for item in results:
                thesaurus_name = self.thesauri_lookup[item["thcode"]]
                if (
                    item["thcode"] != "1"
                    and not self.place
                    or item["thcode"] == "1"
                    and self.place
                ):
                    branch = self.branch_lookup.get(
                        thesaurus_name, QStandardItem(thesaurus_name)
                    )
                    branch.setFont(QFont("Arial", 11))
                    
                    if item["label"] != item["value"]:
                        childnode = QStandardItem(
                            "{} (use: {})".format(item["label"], item["value"])
                        )
                    else:
                        childnode = QStandardItem(item["label"])

                    branch.appendRow([childnode, None])
                    
                    childnode.setFont(QFont("Arial", 9))
                    if (thesaurus_name, item["value"]) not in unique_children:
                        unique_children.append((thesaurus_name, item["value"]))

                    self.branch_lookup[thesaurus_name] = branch

            model = QStandardItemModel(0, 0)
            rootNode = model.invisibleRootItem()

            for thesaurus_node in self.branch_lookup.items():
                rootNode.appendRow(thesaurus_node[1])

            self.ui.treeview_results.setModel(model)
            self.ui.treeview_results.expandAll()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred retrieving values from the controlled vocabulary search: {str(e)}")

    def get_thesaurus(self):
        model = self.ui.treeview_results.model()
        for i in self.ui.treeview_results.selectedIndexes():
            clicked_item = model.itemFromIndex(i)
            parent = clicked_item.parent()
            keyword = clicked_item.text()

            if clicked_item.hasChildren():
                return None
            else:
                thesaurus = parent.text()
                return thesaurus

    def add_term(self, index):
        """
        Adds the accepted keyword associated with the
        selected item in this widget to the parent theme keywords list.

        Parameters
        ----------
        index : int

        Returns
        -------
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
                if " (use: " in keyword:
                    to_use = keyword.split(" (use: ")[1][:-1]
                    accepted_terms = to_use.split(" AND ")
                else:
                    accepted_terms = [keyword]

                for keyword in accepted_terms:
                    if keyword:
                        self.add_term_function(keyword=keyword, thesaurus=thesaurus)

    def text_clicked(self, link):
        """
        Update the form with the value clicked on in the details/definition

        Parameters
        ----------
        link : Qt url

        Returns
        -------
        None
        """
        parent = self.get_thesaurus()

        if link.url().startswith("http"):
            import webbrowser

            webbrowser.open(link.url(), new=0, autoraise=True)
            return
        else:
            self.ui.search_term.setText(link.url())

        self.search_thesaurus()

        if parent is None:
            return

        parent_item = self.branch_lookup[parent]

        model = self.ui.treeview_results.model()
        for irow in range(parent_item.rowCount()):
            child = parent_item.child(irow)
            if child.text() == link.url():
                self.ui.treeview_results.setCurrentIndex(child.index())
                self.show_details(child.index())

    def close_form(self):
        self.parent = None
        self.deleteLater()
        self.close()


if __name__ == "__main__":
    utils.launch_widget(ThesaurusSearch, "Thesaurus Search testing")
