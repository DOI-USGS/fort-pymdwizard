#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Contact Info <cntinfo> widget


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

import sys

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtGui import QMouseEvent, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui import ThesaurusSearch
from pymdwizard.gui.ui_files import UI_PlaceKeywords

class PlaceKeywords(WizardWidget):
    drag_label = "Place Keywords <place>"
    acceptable_tags = ['keywords', 'place']
    ui_class = UI_PlaceKeywords.Ui_place_keywords

    def build_ui(self):
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # self.setup_dragdrop(self)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Thesaurus', 'Keyword'])
        rootNode = model.invisibleRootItem()

        self.ui.place.setModel(model)
        self.ui.place.setColumnWidth(0, 250)
        self.ui.place.expandAll()

        self.contact_include_place_change(self.ui.rbtn_yes.isChecked())

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_search_controlled.clicked.connect(self.search_controlled)
        self.ui.btn_add_custom.clicked.connect(self.add_custom)
        self.ui.placekey.returnPressed.connect(self.add_custom)
        self.ui.btn_remove_keywords.clicked.connect(self.remove_selected)
        self.ui.rbtn_yes.toggled.connect(self.contact_include_place_change)

    def contact_include_place_change(self, b):
            if b:
                self.ui.place_contents.show()
            else:
                self.ui.place_contents.hide()

    def search_controlled(self):
        """
        Open a USGS controlled vocabulary search widget to find keywords.

        Returns
        -------
        None
        """

        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword, place=True)

        self.thesaurus_search.setWindowTitle('Place Keyword Thesaurus Search')

        fg = self.frameGeometry()
        self.thesaurus_search.move(fg.topRight() - QPoint(150, -25))

        self.thesaurus_search.show()

    def browse_iso(self):
        self.iso_browse = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword)
        self.iso_browse.load_iso()

        fg = self.frameGeometry()
        self.iso_browse.move(fg.topRight() - QPoint(150, -25))
        self.iso_browse.show()

    def add_custom(self):

        placekey = self.ui.placekey.text()
        placekt = self.ui.placekt.text()

        self.add_keyword(placekey, placekt)

    def add_keyword(self=None, keyword=None, thesaurus=None):

        contents = self._to_xml()

        existing_placekts = {item.xpath('placekt')[0].text: item for item in \
                             contents.xpath('place')}

        if thesaurus in existing_placekts:
            place = existing_placekts[thesaurus]
        else:
            place = etree.Element("place")
            placekt_node = etree.Element("placekt")
            placekt_node.text = thesaurus
            place.append(placekt_node)
            contents.append(place)


        existing_keys = [key.text for key in place.xpath('placekey')]
        if keyword not in existing_keys:
            placekey_node = etree.Element('placekey')
            placekey_node.text = keyword
            place.append(placekey_node)

        self._from_xml(contents)

    def remove_placekt(self, placekt):
        contents = self._to_xml()

        existing_placekts = {item.xpath('placekt')[0].text: item for item in \
                             contents.xpath('place')}
        placekt_node = existing_placekts[placekt]
        placekt_node.getparent().remove(placekt_node)
        self._from_xml(contents)

    def remove_keyword(self, placekey, placekt):
        contents = self._to_xml()
        existing_placekts = {item.xpath('placekt')[0].text: item for item in \
                             contents.xpath('place')}
        placekt_node = existing_placekts[placekt]

        for placekey_node in placekt_node.xpath('place'):
            if placekey_node.text() == placekey:
                placekt_node.getparent().remove(placekey_node)

        self._from_xml(contents)

    def remove_selected(self):
        starting_data = self._to_xml()
        model = self.ui.place.model()
        for i in self.ui.place.selectedIndexes():
            try:
                clicked_item = model.itemFromIndex(i)
                if clicked_item.hasChildren():
                    self.remove_placekt(clicked_item.text())
                else:
                    placekt = clicked_item.parent().text()
                    self.remove_keyword(clicked_item.text(), placekt)
            except:
                pass


    def _to_xml(self):


        keywords = etree.Element("keywords")

        if self.ui.rbtn_yes.isChecked():
            root = self.ui.place.model().invisibleRootItem()
            for i in range(root.rowCount()):
                item = root.child(i)

                place = etree.Element("place")
                placekt = etree.Element("placekt")
                placekt.text = item.text()
                place.append(placekt)
                for j in range(item.rowCount()):
                    kw = item.child(j, 1)
                    placekey = etree.Element('placekey')
                    placekey.text = kw.text()
                    place.append(placekey)
                keywords.append(place)

        return keywords

    def _from_xml(self, keywords):

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Thesaurus', 'Keyword'])

        rootNode = model.invisibleRootItem()

        if keywords.xpath('place'):
            self.ui.rbtn_yes.setChecked(True)
        else:
            self.ui.rbtn_yes.setChecked(False)

        for place in keywords.xpath('place'):
            thesaurus_name = place.xpath('placekt')[0].text
            branch = QStandardItem(thesaurus_name)
            branch.setFont(QFont('Arial', 9))

            for kw in place.xpath('placekey'):
                childnode = QStandardItem(kw.text)
                childnode.setFont(QFont('Arial', 10))
                branch.appendRow([None, childnode])

            rootNode.appendRow([branch, None])

        self.ui.place.setModel(model)
        # self.ui.place.setColumnWidth(250, 150)
        self.ui.place.expandAll()


if __name__ == "__main__":
    utils.launch_widget(PlaceKeywords)
