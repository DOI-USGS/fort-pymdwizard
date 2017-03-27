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

class Keywordtax(KeywordsRepeater):  #

    drag_label = "Taxonomic keywords <keywtax>"

    def __init__(self, parent=None):
        KeywordsRepeater.__init__(self, keywords_label='Taxonomic keywords',
                                  parent=parent)

    # def build_ui(self):
    #     """
    #     Build and modify this widget's GUI
    #     Returns
    #     -------
    #     None
    #     """
    #     self.
    #
    #     self.repeater = KeywordsRepeater(keywords_label='Taxonomic keywords')
    #
    #     self.ui = self.repeater.ui
    #     self.repeater.add_another()
    #     self.setup_dragdrop(self)


    # def connect_events(self):
    #     """
    #     Connect the appropriate GUI components with the corresponding functions
    #     Returns
    #     -------
    #     None
    #     """
    #     self.ui.radio_single.toggled.connect(self.switch_primary)
    #     self.ui.radio_range.toggled.connect(self.switch_primary)
    #     self.ui.radio_multiple.toggled.connect(self.switch_primary)
    #
    # def switch_primary(self):
    #     """
    #     Switches form to reflect either organization or person primary
    #     Returns
    #     -------
    #     None
    #     """
    #     if self.ui.radio_single.isChecked():
    #         self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(0)
    #         self.ui.page_singledate.show()
    #         self.ui.page_daterange.hide()
    #         self.ui.page_multipledates.hide()
    #         self.ui.page_multipledates.layout().removeWidget(self.multi_dates)
    #     elif self.ui.radio_range.isChecked():
    #         self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(1)
    #         self.ui.page_singledate.hide()
    #         self.ui.page_daterange.show()
    #         self.ui.page_multipledates.hide()
    #         self.ui.page_multipledates.layout().removeWidget(self.multi_dates)
    #     elif self.ui.radio_multiple.isChecked():
    #         self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(2)
    #         self.ui.page_singledate.hide()
    #         self.ui.page_daterange.hide()
    #         self.ui.page_multipledates.layout().addWidget(self.multi_dates)
    #         self.ui.page_multipledates.show()
    #
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
            if element.tag == 'keywtax':
                e.accept()
        else:
            e.ignore()

    def clear_widget(self):
        self.ui.thesaurus_edit.clear()
        self.keywords.clear_widgets()

    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        keywtax = xml_utils.xml_node('keywtax')
        taxonkt = xml_utils.xml_node("taxonkt",
                                     text=self.ui.thesaurus_edit.text(),
                                     parent_node=keywtax)
        for keyword in self.get_keywords():
            taxonkey = xml_utils.xml_node('taxonkey', text=keyword,
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
            if keywtax.tag == 'keywtax':
                thesaurus = keywtax.xpath('taxonkt')
                if thesaurus:
                    self.ui.thesaurus_edit.setText(thesaurus[0].text)

                keywords = keywtax.xpath('taxonkey')
                for kw in keywords:
                    kw_widget = self.add_another()
                    kw_widget.added_line.setText(kw.text)

            else:
                print ("The tag is not keywtax")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Keywordtax,
                        " testing")
