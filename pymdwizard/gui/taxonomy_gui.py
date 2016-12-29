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

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_ITISSearch


class ItisMainForm(WizardWidget):

    drag_label = "Taxonomy"

    def __init__(self, parent=None):
        # QtGui.QMainWindow.__init__(self, parent)
        super(self.__class__, self).__init__()

        self.selected_items_df = pd.DataFrame(columns=['item', 'tsn'])
        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_ITISSearch.Ui_ItisSearchWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setSizes([300, 100])
        self.setup_dragdrop(self)

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
        self.ui.button_add_taxon.clicked.connect(self.add_tsn)
        self.ui.button_gen_fgdc.clicked.connect(self.generate_fgdc)
        self.ui.button_remove_selected.clicked.connect(self.remove_selected)
        self.ui.table_include.doubleClicked.connect(self.remove_selected)


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
        indexes = df.index[selected_indices]

        index = selected_indices[0]

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
        self.ui.table_include.setModel(self.selected_model)

    def remove_selected(self, index):
        indexes = self.ui.table_include.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]
        index = self.selected_items_df.index[selected_indices]
        self.selected_items_df.drop(index, inplace=True)
        self.ui.table_include.model().layoutChanged.emit()

    def generate_fgdc(self):
        self.w = MyPopup()
        self.w.setWindowTitle('FGDC Taxonomy Section')
        self.w.setGeometry(QRect(100, 100, 400, 200))

        fgdc_taxonomy = self._to_xml()

        self.w.textEdit.setText(etree.tostring(fgdc_taxonomy, pretty_print=True).decode())
        self.w.show()

    def dragEnterEvent(self, e):
        """

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
            if element.tag == 'taxonomy':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):

        df = self.ui.table_include.model().dataframe()
        include_common = self.ui.check_include_common.isChecked()

        fgdc_taxonomy = taxonomy.gen_taxonomy_section(keywords=list(df.item),
                                                      tsns=list(df.tsn),
                                           include_common_names=include_common)

        return fgdc_taxonomy

    def _from_xml(self, taxonomy_element):
        i = 0
        for common_node in taxonomy_element.findall('.//common'):
            if common_node.text.startswith('TSN: '):
                tsn = common_node.text[5:]
                scientific_name = taxonomy.get_full_record_from_tsn(tsn)['scientificName']['combinedName']
                self.selected_items_df.loc[i] = [scientific_name, tsn]
                i += 1

        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)


class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout()


        self.textEdit = QTextEdit()

        layout.addWidget(self.textEdit)

        self.setLayout(layout)



if __name__ == '__main__':
    utils.launch_widget(ItisMainForm, "Itis testing")