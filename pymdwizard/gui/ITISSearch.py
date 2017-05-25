#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime

from lxml import etree
import pandas as pd


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QTableView, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolButton
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint
from PyQt5.QtCore import Qt, QMimeData, QObject, QTimeLine

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QEvent, QCoreApplication
from PyQt5.QtGui import QMouseEvent

from pymdwizard.core import taxonomy
from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_ITISSearchSimple


class ItisSearch(QWidget):

    def __init__(self, table=None, selected_items_df=None, parent=None):
        super(self.__class__, self).__init__()

        self.build_ui()
        self.connect_events()

        self.table_include = table
        self.selected_items_df = selected_items_df
        utils.set_window_icon(self)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_ITISSearchSimple.Ui_ItisSearchWidget()
        self.ui.setupUi(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.button_search.clicked.connect(self.search_itis)
        self.ui.search_term.returnPressed.connect(self.search_itis)
        self.ui.table_results.doubleClicked.connect(self.add_tsn)
        self.ui.btn_add_taxon.clicked.connect(self.add_tsn)
        self.ui.btn_close.clicked.connect(self.close)

    def search_itis(self):

        if str(self.ui.combo_search_type.currentText()) == 'Scientific name':
            results = taxonomy.search_by_scientific_name(str(self.ui.search_term.text()))
        else:
            results = taxonomy.search_by_common_name(str(self.ui.search_term.text()))

        model = utils.PandasModel(results)
        self.ui.table_results.setModel(model)

    def add_tsn(self, index):
        indexes = self.ui.table_results.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]
        df = self.ui.table_results.model().dataframe()
        indices = df.index[selected_indices]

        for index in indices:
            if 'combinedName' in df.columns:
                item_name = df.iloc[index]['combinedName']
            else:
                item_name = str(df.iloc[index]['commonName'])

            tsn = df.iloc[index]['tsn']
            i = self.selected_items_df.index.max()+1
            if pd.isnull(i):
                i = 0
            self.selected_items_df.loc[i] = [str(item_name), tsn]

        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.table_include.setModel(self.selected_model)

    def close(self):
        self.deleteLater()


if __name__ == '__main__':
    utils.launch_widget(ItisSearch, "Itis testing")