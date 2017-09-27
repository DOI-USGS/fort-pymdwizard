#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests


from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_ThesaurusSearch


class ThesaurusSearch(QDialog):

    def __init__(self, add_term_function=None, parent=None, place=False):
        super(self.__class__, self).__init__(parent=parent)

        self.build_ui()
        self.connect_events()

        self.thesauri_lookup = {}
        self.thesauri_lookup_r = {}

        self.add_term_function = add_term_function

        self.place = place

        utils.set_window_icon(self)

    def load_iso(self):
        self.ui.label_search_term.hide()
        self.ui.search_term.hide()
        self.ui.button_search.hide()
        self.ui.label_search_results.text = "ISO 19115 Topic Categories"

        self.populate_thesauri_lookup()

        iso_url = "https://www2.usgs.gov/science/term.php?thcode=15&text=ISO 19115 Topic Category"
        results = utils.requests_pem_get(iso_url).json()

        thesaurus_name = "ISO 19115 Topic Category"
        branch = QStandardItem(thesaurus_name)
        branch.setFont(QFont('Arial', 11))
        for item in results['nt']:
            childnode = QStandardItem(item['name'])
            childnode.setFont(QFont('Arial', 9))
            branch.appendRow([childnode])

        model = QStandardItemModel(0, 0)
        # model.setHorizontalHeaderLabels(['Theme Keywords (thesaurus/keywords)'])

        rootNode = model.invisibleRootItem()
        rootNode.appendRow(branch)

        self.ui.treeview_results.setModel(model)
        # self.ui.treeview_results.setColumnWidth(0, 150)
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

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.button_search.clicked.connect(self.search_thesaurus)
        self.ui.search_term.returnPressed.connect(self.search_thesaurus)
        self.ui.treeview_results.doubleClicked.connect(self.add_term)
        self.ui.treeview_results.clicked.connect(self.show_details)
        self.ui.btn_add_term.clicked.connect(self.add_term)
        self.ui.btn_close.clicked.connect(self.close_form)

    def show_details(self, index):
        clicked_item = self.ui.treeview_results.model().itemFromIndex(index)
        parent = clicked_item.parent()

        if clicked_item.hasChildren():
            thcode = self.thesauri_lookup_r[clicked_item.text()]
            thname = clicked_item.text()

            THESAURUS_DETAILS_URL = "https://www2.usgs.gov/science/thesaurus.php?format=json&thcode={}"
            thesaurus_details_url = THESAURUS_DETAILS_URL.format(thcode)
            details = utils.requests_pem_get(thesaurus_details_url).json()

            details_msg = ''
            details_msg += '<b><font size="5" face="arial">{}</font></b><br>'.format(thname)
            uri = details['vocabulary']['uri']
            if uri:
                details_msg += '<a href="{}"><u><i><font size="4" face="arial" style="color:#386EC4">{}</font></i></u></a><br><br>'.format(uri, uri)

            details_msg += details['vocabulary']['scope']
        else:
            thcode = self.thesauri_lookup_r[parent.text()]
            details_url = "https://www2.usgs.gov/science/term.php?thcode={}&text={}".format(thcode, clicked_item.text())
            details = utils.requests_pem_get(details_url).json()
            if type(details) == dict:
                details = [details]

            details_msg = ''
            search_term = self.ui.search_term.text()
            prefered_shown = False
            for detail in details:

                term = detail["term"]
                uf = detail["uf"]
                bt = detail["bt"]
                nt = detail["nt"]
                rt = detail["rt"]

                if term['name'].lower() != search_term and \
                        not prefered_shown:
                    term_count = 0
                    prefered_shown = True
                    for alt_term in uf:
                        if alt_term['name'].lower() in search_term.lower():
                            term_count += 1
                            if term_count == 1:
                                details_msg += "The query matches the following non-preferred terms: "
                            else:
                                details_msg += ', '
                            details_msg += "<u>{}</u>".format(alt_term['name'])

                    if term_count > 0:
                        details_msg += '<br><br>'

                details_msg += '<b><font size="5" face="arial">{}</font></b><br>'.format(term['name'])
                details_msg += '<font size="4" face="arial">{}<br><br>'.format(term['scope'])


                if bt:
                    details_msg += "Broader terms: "
                    details_msg += " > ".join(['<u>{}</u>'.format(item['name']) for item in bt[::-1]])
                    details_msg += '<br>'


                if nt:
                    details_msg += " Narrower terms: "
                    details_msg += ", ".join(['<u>{}</u>'.format(item['name']) for item in nt])
                    details_msg += '<br>'

                if rt:
                    details_msg += " Related terms: "
                    details_msg += ", ".join(['<u>{}</u>'.format(item['name']) for item in rt])
                    details_msg += '<br>'

        self.ui.textBrowser.setText(details_msg)

    def populate_thesauri_lookup(self):
        if not self.thesauri_lookup:
            url = "https://www2.usgs.gov/science/thesaurus.php?format=json"
            result = self.get_result(url)
            if result is not None:
                self.thesauri_lookup = {i['thcode']: i['name'] for i in result['vocabulary']}
                self.thesauri_lookup_r = {i['name']: i['thcode'] for i in result['vocabulary']}
                return True
            else:
                return False
        return True

    def get_result(self, url):
        try:
            return utils.requests_pem_get(url).json()
        except requests.exceptions.ConnectionError:
            msg = "We're having trouble connecting to the controlled vocabularies service"
            msg += "\n Check that you have an internet connect, or try again latter"
            QMessageBox.warning(self, "Connection error", msg)
            self.close_form()

    def search_thesaurus(self):

        if not self.populate_thesauri_lookup():
            return False

        search_url = "https://www2.usgs.gov/science/term-search.php?thcode=any&term={}".format(self.ui.search_term.text())


        results = self.get_result(search_url)
        if results is None:
            return False

        if not results:
            msg = "The Metadata Wizard was unable to locate the provided search term in the controlled vocabulary search"
            msg += "\n\n'{}' Not Found".format(self.ui.search_term.text())
            QMessageBox.information(self, "Search Term Not Found", msg, QMessageBox.Ok)
            return False

        branch_lookup = {}
        unique_children = []
        for item in results:
            thesaurus_name = self.thesauri_lookup[item['thcode']]
            if item['thcode'] != '1' and not self.place or \
               item['thcode'] == '1' and self.place:
                branch = branch_lookup.get(thesaurus_name, QStandardItem(thesaurus_name))
                branch.setFont(QFont('Arial', 11))
                childnode = QStandardItem(item['value'])
                childnode.setFont(QFont('Arial', 9))
                if (thesaurus_name, item['value']) not in unique_children:
                    branch.appendRow([childnode])
                    unique_children.append((thesaurus_name, item['value']))

                branch_lookup[thesaurus_name] = branch

        model = QStandardItemModel(0, 0)

        rootNode = model.invisibleRootItem()

        for thesaurus_node in branch_lookup.items():
            rootNode.appendRow(thesaurus_node[1])

        self.ui.treeview_results.setModel(model)
        self.ui.treeview_results.expandAll()

    def add_term(self, index):
        model = self.ui.treeview_results.model()
        for i in self.ui.treeview_results.selectedIndexes():
            clicked_item = model.itemFromIndex(i)
            parent = clicked_item.parent()
            keyword = clicked_item.text()

            if clicked_item.hasChildren():
                pass
            else:
                thesaurus = parent.text()
                self.add_term_function(keyword=keyword, thesaurus=thesaurus)

    def close_form(self):
        self.parent = None
        self.deleteLater()
        self.close()

if __name__ == '__main__':
    utils.launch_widget(ThesaurusSearch, "Thesaurus Search testing")
