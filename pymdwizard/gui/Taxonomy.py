#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Taxonomy <taxonomy> section


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
import pandas as pd

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import taxonomy
from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_Taxonomy
from pymdwizard.gui import ITISSearch


class Taxonomy(WizardWidget):

    WIDGET_WIDTH = 500
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Taxonomy"
    acceptable_tags = ['abstract']


    def __init__(self, parent=None):

        WizardWidget.__init__(self, parent=parent)

        self.selected_items_df = pd.DataFrame(columns=['item', 'tsn'])
        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)

        self.ui.frame_included_species.hide()

        # This dictionary contains copies of each unique taxonomy xml created
        # so that we need not generate them more than once
        self.xml_lookup = {}

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_Taxonomy.Ui_Taxonomy()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_search.clicked.connect(self.search_itis)
        self.ui.rbtn_yes.toggled.connect(self.include_taxonomy_change)
        self.ui.btn_remove_selected.clicked.connect(self.remove_selected)

    def include_taxonomy_change(self, b):
        if b:
            self.ui.frame_included_species.show()
        else:
            self.ui.frame_included_species.hide()

    def search_itis(self):

        # self.ITIS_Search = QDialog(self)
        self.ITIS_Search = ITISSearch.ItisSearch(table=self.ui.table_include,
                                                 selected_items_df=self.selected_items_df,
                                                 parent=self)
        fg = self.frameGeometry()
        self.ITIS_Search.move(fg.topRight() - QPoint(150, -25))
        self.ITIS_Search.show()

        # self.ui.table_results.setModel(self.ITIS_Search.ui.table_results)

    def remove_selected(self):
        indexes = self.ui.table_include.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]
        index = self.selected_items_df.index[selected_indices]
        self.selected_items_df.drop(index, inplace=True)
        self.ui.table_include.model().layoutChanged.emit()

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'taxonomy'

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'taxonomy':
                e.accept()
        else:
            e.ignore()

    def has_content(self):
        """
        Returns if the widget contains legitimate content that should be
        written out to xml

        By default this is always true but should be implement in each
        subclass with logic to check based on contents

        Returns
        -------
        bool : True if there is content, False if no
        """
        return self.ui.rbtn_yes.isChecked()

    def _to_xml(self):
        df = self.ui.table_include.model().dataframe()
        include_common = self.ui.check_include_common.isChecked()
        unique_id = tuple([tuple(df.tsn), include_common])

        if unique_id not in self.xml_lookup:
            fgdc_taxonomy = taxonomy.gen_taxonomy_section(keywords=list(df.item),
                        tsns=list(df.tsn), include_common_names=include_common)
            self.xml_lookup[unique_id] = fgdc_taxonomy

        return self.xml_lookup[unique_id]

    def _from_xml(self, taxonomy_element):

        self.ui.rbtn_yes.setChecked(True)

        self.selected_items_df = pd.DataFrame(columns=['item', 'tsn'])
        i = 0
        for common_node in taxonomy_element.findall('.//common'):
            if common_node.text.startswith('TSN: '):
                tsn = common_node.text[5:]
                self.selected_items_df.loc[i] = ['...', tsn]
                # try:
                #     scientific_name = taxonomy.get_full_record_from_tsn(tsn)['scientificName']['combinedName']
                #     self.selected_items_df.loc[i] = [scientific_name, tsn]
                # except:
                #     self.selected_items_df.loc[i] = ['...', tsn]
                # i += 1

        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)


if __name__ == "__main__":
    utils.launch_widget(Taxonomy, "Taxonomy testing")

