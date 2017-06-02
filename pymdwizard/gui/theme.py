#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Metadata Date <timeperd> section
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
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QStackedWidget, QTabWidget, QDateEdit, QListWidget
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QGridLayout, QScrollArea
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QDate

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.keywords_repeater import KeywordsRepeater

class Theme(KeywordsRepeater):  #

    drag_label = "Theme Keywords <theme>"
    acceptable_tags = ['theme']

    def __init__(self, which='theme', parent=None):
        self.which = which
        KeywordsRepeater.__init__(self, keywords_label='Keyword   ',
                                  parent=parent, line_name='fgdc_{}key'.format(self.which))

        self.kt = self.ui.fgdc_themekt
        if which == 'place':
            self.setObjectName('fgdc_place')
            self.drag_label = "Place Keywords <place>"
            self.ui.fgdc_themekt.setObjectName('fgdc_placekt')
            self.acceptable_tags = ['place']
        else:
            self.setObjectName('fgdc_theme')

    def changed_thesaurus(self, s):
        self.change_tab_label(s)

    def add_keyword(self, keyword, locked=False):
        existing_kws = self.get_keywords()
        if existing_kws[0] == '':
            kw = self.keywords.get_widgets()[0]
            kw.added_line.setText(keyword)
            kw.added_line.setReadOnly(locked)
        elif keyword not in existing_kws:
            kw = self.keywords.add_another()
            kw.added_line.setText(keyword)
            kw.added_line.setReadOnly(locked)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'timeperd'
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == self.which:
                e.accept()
        else:
            e.ignore()

    def get_thesaurus_name(self):
        return self.kt.text()

    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        keywtax = xml_utils.xml_node(self.which)
        taxonkt = xml_utils.xml_node("{}kt".format(self.which),
                                     text=self.ui.fgdc_themekt.text(),
                                     parent_node=keywtax)
        for keyword in self.get_keywords():
            taxonkey = xml_utils.xml_node("{}key".format(self.which),
                                          text=keyword,
                                          parent_node=keywtax)

        return keywtax

    def _from_xml(self, keywtax):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if keywtax.tag == self.which:
                thesaurus = keywtax.xpath("{}kt".format(self.which))
                if thesaurus:
                    self.ui.fgdc_themekt.setText(thesaurus[0].text)

                keywords = keywtax.xpath("{}key".format(self.which))
                for kw in keywords:
                    if self.keywords.get_widgets()[0].added_line.text() == '':
                        kw_widget = self.get_widgets()[0]
                    else:
                        kw_widget = self.keywords.add_another()

                    kw_widget.added_line.setText(kw.text)

            else:
                print ("The tag is not theme")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Theme,
                        " testing", which='place')
