#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Process Step <procstep> section


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

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint



from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_theme_list
from pymdwizard.gui import ThesaurusSearch
from pymdwizard.gui.theme import Theme
from pymdwizard.gui.iso_keyword import IsoKeyword
from pymdwizard.gui.repeating_element import RepeatingElement


class ThemeList(WizardWidget): #

    drag_label = "Theme Keywords <keywords>"


    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_theme_list.Ui_theme_list()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)


        self.ui.theme_tabs.setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        self.iso_kws = RepeatingElement(which='vertical',
                                        add_text='Add additonal',
                                        widget=IsoKeyword,
                                        remove_text='Remove Keyword',
                                        italic_text='ISO Topic Category Keywords')
        self.iso_kws.add_another()
        self.ui.iso_keywords_layout.addWidget(self.iso_kws)
        self.thesauri = []

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions
        Returns
        -------
        None
        """
        self.ui.btn_add_thesaurus.clicked.connect(self.add_another)
        self.ui.btn_remove_selected.clicked.connect(self.remove_selected)
        self.ui.btn_add_iso.clicked.connect(self.add_iso)
        self.ui.btn_search_controlled.clicked.connect(self.search_controlled)

    def add_another(self, click=False, tab_label='', locked=False):

        if 'None' not in [t.get_thesaurus_name() for t in self.thesauri] and \
                tab_label == '':
            theme_widget = self.add_keyword(keyword='', thesaurus='None',
                                            locked=False)
        else:
            theme_widget = Theme()
            theme_widget.ui.fgdc_themekt.textChanged.connect(self.changed_thesaurus)

            self.ui.theme_tabs.addTab(theme_widget, tab_label)
            self.ui.theme_tabs.setCurrentIndex(self.ui.theme_tabs.count()-1)

            self.thesauri.append(theme_widget)

        return theme_widget

    def changed_thesaurus(self, s):
            current_index = self.ui.theme_tabs.currentIndex()
            current_tab = self.ui.theme_tabs.setTabText(current_index, 'Thesaurus: ' + s)

    def remove_selected(self):
        current_index = self.ui.theme_tabs.currentIndex()
        if current_index == 0:
            self.ui.theme_tabs.setTabEnabled(0, False)
            self.ui.iso_tab.hide()
        else:
            self.ui.theme_tabs.removeTab(current_index)
            del self.thesauri[current_index-1]

    def add_iso(self):
        self.ui.theme_tabs.setTabEnabled(0, True)
        self.ui.iso_tab.show()

    def clear_widget(self):
        self.iso_kws.clear_widgets()

        for i in range(len(self.thesauri), 0, -1):
            self.ui.theme_tabs.setCurrentIndex(i)
            self.remove_selected()

    def search_controlled(self):
        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword)

        self.thesaurus_search.setWindowTitle('Theme Keyword Thesaurus Search')

        fg = self.frameGeometry()
        self.thesaurus_search.move(fg.topRight() - QPoint(150, -25))

        self.thesaurus_search.show()

    def add_keyword(self, keyword=None, thesaurus=None, locked=True):
        theme_widget = None
        for theme in self.thesauri:
            if theme.ui.fgdc_themekt.text() == thesaurus:
                theme_widget = theme

        if theme_widget is None:
            shortname = thesaurus.split(' ')[0]
            theme_widget = self.add_another(tab_label=shortname, locked=locked)
            theme_widget.ui.fgdc_themekt.setText(thesaurus)
            if locked:
                theme_widget.lock()
            self.changed_thesaurus(shortname)

        theme_widget.add_keyword(keyword, locked=locked)
        return theme_widget

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'procstep'
        Parameters
        ----------
        e : qt event

        Returns
        -------
        None

        """
        print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'keywords':
                e.accept()
        else:
            e.ignore()


         
                
    def _to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        procstep element tag in xml tree
        """
        keywords = xml_utils.xml_node('keywords')
        for theme in self.thesauri:
            theme_xml = theme._to_xml()
            keywords.append(theme_xml)

        return keywords

    def _from_xml(self, keywords_xml):
        """
        parses the xml code into the relevant procstep elements

        Parameters
        ----------
        process_step - the xml element status and its contents

        Returns
        -------
        None
        """
        self.clear_widget()

        self.original_xml = keywords_xml
        if keywords_xml.tag == 'keywords':
            for theme_xml in keywords_xml.xpath('theme'):
                if theme_xml.xpath('themekt'):
                    themekt = theme_xml.xpath('themekt')[0]
                    if 'iso 19115' in themekt.text.lower():
                        self.iso_kws.clear_widgets(add_another=False)
                        for themekey in theme_xml.xpath('themekey'):
                            iso = self.iso_kws.add_another()
                            iso.ui.comboBox.setCurrentText(themekey.text)

                    else:
                        theme = self.add_another()
                        theme._from_xml(theme_xml)


if __name__ == "__main__":
    utils.launch_widget(ThemeList,
                        "ThemeList Step testing")

