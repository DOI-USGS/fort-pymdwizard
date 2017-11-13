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

from PyQt5.QtCore import QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_place_list
from pymdwizard.gui import ThesaurusSearch
from pymdwizard.gui.theme import Theme


class PlaceList(WizardWidget): #

    drag_label = "Place Keywords <keywords>"
    acceptable_tags = ['keywords', 'place']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_place_list.Ui_place_keywords()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)


        self.ui.theme_tabs.setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        self.thesauri = []

        self.contact_include_place_change(False)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions
        Returns
        -------
        None
        """
        self.ui.btn_add_thesaurus.clicked.connect(self.add_another)
        self.ui.btn_remove_selected.clicked.connect(self.remove_selected)
        self.ui.btn_search_controlled.clicked.connect(self.search_controlled)
        self.ui.rbtn_yes.toggled.connect(self.contact_include_place_change)

    def contact_include_place_change(self, b):
        if b:
            self.ui.place_contents.show()
            if len(self.thesauri) == 0:
                theme_widget = self.add_keyword(keyword='', thesaurus='None',
                                            locked=False)
                self.thesauri.append(theme_widget)
        else:
            self.ui.place_contents.hide()

    def add_another(self, click=False, tab_label='', locked=False):

        if 'None' not in [t.get_thesaurus_name() for t in self.thesauri] and \
                        tab_label == '':
            theme_widget = self.add_keyword(keyword='', thesaurus='None',
                                            locked=False)
        else:
            theme_widget = Theme(which='place')
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
        self.remove_tab(current_index)

    def remove_tab(self, index):
        self.ui.theme_tabs.removeTab(index)
        del self.thesauri[index]

    def get_children(self, widget):
        children = []

        if self.ui.rbtn_yes.isChecked():
            for place in self.thesauri:
                children.append(place)

        return children

    def clear_widget(self):
        for i in range(len(self.thesauri)-1, -1, -1):
            self.remove_tab(i)
        self.thesauri = []

    def search_controlled(self):
        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(add_term_function=self.add_keyword, place=True, parent=self)

        self.thesaurus_search.setWindowTitle('Place Keyword Thesaurus Search')

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

        theme_widget.add_keyword(keyword)
        return theme_widget
                
    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        procstep element tag in xml tree
        """
        keywords = xml_utils.xml_node('keywords')

        if self.ui.rbtn_yes.isChecked():
            for place in self.thesauri:
                place_xml = place.to_xml()
                keywords.append(place_xml)

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
        self.clear_widget()

        self.original_xml = keywords_xml
        if keywords_xml.tag == 'keywords':
            place_kws = keywords_xml.xpath('place')


            for place_xml in place_kws:
                place = self.add_another(tab_label='x')
                place.from_xml(place_xml)

            if place_kws:
                self.ui.rbtn_yes.setChecked(True)
            else:
                self.ui.rbtn_no.setChecked(True)


if __name__ == "__main__":
    utils.launch_widget(PlaceList,
                        "ThemeList Step testing")







