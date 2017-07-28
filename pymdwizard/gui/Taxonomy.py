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
from pymdwizard.gui.ui_files import UI_taxonomy2
from pymdwizard.gui import taxonomy_gui
from pymdwizard.gui.repeating_element import RepeatingElement

from pymdwizard.gui.taxoncl import Taxoncl
from pymdwizard.gui.keywtax import Keywordtax


class Taxonomy(WizardWidget):

    drag_label = "Taxonomy"
    acceptable_tags = ['taxonomy']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_taxonomy2.Ui_Taxonomy()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.keywtax = Keywordtax()
        self.ui.kws_layout.addWidget(self.keywtax)

        self.taxoncl = Taxoncl()
        self.ui.taxoncl_contents.layout().addWidget(self.taxoncl)

        self.include_taxonomy_change(False)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_search.clicked.connect(self.search_itis)
        self.ui.rbtn_yes.toggled.connect(self.include_taxonomy_change)


    def include_taxonomy_change(self, b):
        if b:
            self.ui.widget_contents.show()
        else:
            self.ui.widget_contents.hide()

    def search_itis(self):

        self.tax_gui = taxonomy_gui.ItisMainForm(xml=self._to_xml(),
                                                 fgdc_function=self._from_xml)
        fg = self.frameGeometry()
        self.tax_gui.move(fg.topRight() - QPoint(150, -25))
        self.tax_gui.show()

        # self.taxgui_dialog = QDialog(self)
        # self.taxgui_dialog.setWindowTitle('Search Integrated Taxonomic Information System (ITIS)')
        # self.taxgui_dialog.setLayout(self.tax_gui.layout())
        #
        # self.taxgui_dialog.exec_()

    def remove_selected(self):
        indexes = self.ui.table_include.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]
        index = self.selected_items_df.index[selected_indices]
        self.selected_items_df.drop(index, inplace=True)
        self.ui.table_include.model().layoutChanged.emit()

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

    def clear_widget(self):
        self.keywtax.clear_widget()
        self.taxoncl.clear_widget()

    def _to_xml(self):

        taxonomy = xml_utils.xml_node('taxonomy')
        taxonomy.append(self.keywtax._to_xml())
        taxonomy.append(self.taxoncl._to_xml())
        return taxonomy

    def _from_xml(self, taxonomy_element):
        self.clear_widget()
        self.ui.rbtn_yes.setChecked(True)

        keywtax = taxonomy_element.xpath('keywtax')
        if keywtax:
            self.keywtax._from_xml(taxonomy_element.xpath('keywtax')[0])

        taxoncl = taxonomy_element.xpath('taxoncl')
        if taxoncl:
            self.taxoncl._from_xml(taxoncl[0])

if __name__ == "__main__":
    utils.launch_widget(Taxonomy, "Taxonomy testing")

