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
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QDialog
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui import ThesaurusSearch
from pymdwizard.gui.ui_files import UI_ThemeKeywords

class ThemeKeywords(WizardWidget):

    drag_label = "Theme Keywords <theme>"
    acceptable_tags = ['abstract']
    ui_class = UI_ThemeKeywords.Ui_theme_keywords

    def build_ui(self):
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # self.setup_dragdrop(self)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Thesaurus', 'Keyword'])
        rootNode = model.invisibleRootItem()

        self.ui.theme.setModel(model)
        self.ui.theme.setColumnWidth(0, 250)
        self.ui.theme.expandAll()


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_search_controlled.clicked.connect(self.search_controlled)
        self.ui.btn_add_custom.clicked.connect(self.add_custom)
        self.ui.themekey.returnPressed.connect(self.add_custom)
        self.ui.btn_browse_iso.clicked.connect(self.browse_iso)
        self.ui.btn_remove_keywords.clicked.connect(self.remove_selected)
        # self.ui.btn_import_contact.clicked.connect(self.find_usgs_contact)
        # self.ui.rbtn_perp.toggled.connect(self.switch_primary)

    def search_controlled(self):
        """
        Open a USGS controlled vocabulary search widget to find keywords.

        Returns
        -------
        None
        """
        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword, parent=self)
        #
        # self.thesaurus_search.setWindowTitle('Theme Keyword Thesaurus Search')
        #
        # fg = self.frameGeometry()
        # self.thesaurus_search.move(fg.topRight() - QPoint(150, -25))
        #
        # self.thesaurus_search.show()

        self.search_dialog = QDialog(self)
        self.search_dialog.setWindowTitle('Theme Keyword Thesaurus Search')
        self.search_dialog.setLayout(self.thesaurus_search.layout())

        self.search_dialog.exec_()

    def browse_iso(self):
        self.iso_browse = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword)
        self.iso_browse.load_iso()

        fg = self.frameGeometry()
        self.iso_browse.move(fg.topRight() - QPoint(150, -25))
        self.iso_browse.show()

    def add_custom(self):

        themekey = self.ui.themekey.text()
        themekt = self.ui.themekt.text()

        self.add_keyword(themekey, themekt)

    def add_keyword(self=None, keyword=None, thesaurus=None):

        contents = self._to_xml()

        existing_themekts = {item.xpath('themekt')[0].text: item for item in \
                             contents.xpath('theme')}

        if thesaurus in existing_themekts:
            theme = existing_themekts[thesaurus]
        else:
            theme = etree.Element("theme")
            themekt_node = etree.Element("themekt")
            themekt_node.text = thesaurus
            theme.append(themekt_node)
            contents.append(theme)


        existing_keys = [key.text for key in theme.xpath('themekey')]
        if keyword not in existing_keys:
            themekey_node = etree.Element('themekey')
            themekey_node.text = keyword
            theme.append(themekey_node)

        self._from_xml(contents)

    def remove_themekt(self, themekt):
        contents = self._to_xml()

        existing_themekts = {item.xpath('themekt')[0].text: item for item in \
                             contents.xpath('theme')}
        themekt_node = existing_themekts[themekt]
        themekt_node.getparent().remove(themekt_node)
        self._from_xml(contents)

    def remove_keyword(self, themekey, themekt):
        contents = self._to_xml()
        existing_themekts = {item.xpath('themekt')[0].text: item for item in \
                             contents.xpath('theme')}
        themekt_node = existing_themekts[themekt]

        for themekey_node in themekt_node.xpath('theme'):
            if themekey_node.text() == themekey:
                themekt_node.getparent().remove(themekey_node)

        self._from_xml(contents)

    def remove_selected(self):
        starting_data = self._to_xml()
        model = self.ui.theme.model()
        for i in self.ui.theme.selectedIndexes():
            try:
                clicked_item = model.itemFromIndex(i)
                if clicked_item.hasChildren():
                    self.remove_themekt(clicked_item.text())
                else:
                    themekt = clicked_item.parent().text()
                    self.remove_keyword(clicked_item.text(), themekt)
            except:
                pass



    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        print("cinfo drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'keywords' or element.tag == 'theme':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):


        keywords = etree.Element("keywords")

        root = self.ui.theme.model().invisibleRootItem()
        for i in range(root.rowCount()):
            item = root.child(i)

            theme = etree.Element("theme")
            themekt = etree.Element("themekt")
            themekt.text = item.text()
            theme.append(themekt)
            for j in range(item.rowCount()):
                kw = item.child(j, 1)
                themekey = etree.Element('themekey')
                themekey.text = kw.text()
                theme.append(themekey)
            keywords.append(theme)

        return keywords

    def _from_xml(self, keywords):

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Thesaurus', 'Keyword'])

        rootNode = model.invisibleRootItem()

        for theme in keywords.xpath('theme'):
            thesaurus_name = theme.xpath('themekt')[0].text
            branch = QStandardItem(thesaurus_name)
            branch.setFont(QFont('Arial', 9))

            for kw in theme.xpath('themekey'):
                childnode = QStandardItem(kw.text)
                childnode.setFont(QFont('Arial', 10))
                branch.appendRow([None, childnode])

            rootNode.appendRow([branch, None])

        self.ui.theme.setModel(model)
        # self.ui.theme.setColumnWidth(250, 150)
        self.ui.theme.expandAll()


if __name__ == "__main__":
    utils.launch_widget(ThemeKeywords)
