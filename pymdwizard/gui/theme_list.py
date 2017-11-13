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
    acceptable_tags = ['keywords']

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
            self.remove_iso()
        else:
            self.ui.theme_tabs.removeTab(current_index)
            del self.thesauri[current_index-1]

    def remove_iso(self):
        self.ui.theme_tabs.setTabEnabled(0, False)
        self.ui.fgdc_theme.hide()

    def add_iso(self):
        self.ui.theme_tabs.setTabEnabled(0, True)
        self.ui.theme_tabs.setTabText(0, 'ISO 19115')
        self.ui.fgdc_theme.show()

        self.ui.theme_tabs.setCurrentIndex(0)
        self.resize(100, 100)

    def get_children(self, widget):

        children = []

        if self.ui.theme_tabs.isTabEnabled(0):
            children.append(self.ui.fgdc_theme)
        for theme in self.thesauri:
            children.append(theme)

        return children

    def clear_widget(self, remove_iso=False):

        self.iso_kws.clear_widgets()
        if remove_iso:
            self.remove_iso()

        for i in range(len(self.thesauri), -1, -1):
            self.ui.theme_tabs.setCurrentIndex(i)
            self.remove_selected()

        self.ui.fgdc_themekt.setText('ISO 19115 Topic Category')

    def search_controlled(self):

        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword, parent=self)
        self.thesaurus_search.setWindowTitle('Search USGS Controlled Vocabularies')
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
                
    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        procstep element tag in xml tree
        """
        keywords = xml_utils.xml_node('keywords')

        if self.ui.theme_tabs.isTabEnabled(0):
            theme = xml_utils.xml_node('theme', parent_node=keywords)
            themekt = xml_utils.xml_node('themekt',
                                         text=self.ui.fgdc_themekt.text(),
                                         parent_node=theme)
            for isokw in self.iso_kws.get_widgets():
                themekey = xml_utils.xml_node('themekey', text=isokw.ui.fgdc_themekey.currentText(),
                                           parent_node=theme)

        for theme in self.thesauri:
            theme_xml = theme.to_xml()
            keywords.append(theme_xml)

        return keywords

    def from_xml(self, keywords_xml):
        """
        parses the xml code into the relevant procstep elements

        Parameters
        ----------
        process_step - the xml element status and its contents

        Returns
        -------
        None
        """
        self.clear_widget(remove_iso=True)

        self.original_xml = keywords_xml
        if keywords_xml.tag == 'keywords':
            for theme_xml in xml_utils.search_xpath(keywords_xml, 'theme', False):
                themekt = xml_utils.get_text_content(theme_xml, 'themekt')
                if themekt is not None and 'iso 19115' in themekt.lower():
                    self.add_iso()
                    self.iso_kws.clear_widgets(add_another=False)
                    for themekey in xml_utils.search_xpath(theme_xml,
                                                           'themekey',
                                                           only_first=False):
                        iso = self.iso_kws.add_another()
                        iso.ui.fgdc_themekey.setCurrentText(themekey.text)


                else:
                    theme = self.add_another()
                    theme.from_xml(theme_xml)


if __name__ == "__main__":
    utils.launch_widget(ThemeList,
                        "ThemeList Step testing")







