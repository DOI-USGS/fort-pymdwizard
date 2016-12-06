#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from lxml import etree

from PyQt4 import QtGui
from PyQt4 import QtCore
Qt = QtCore.Qt

from pymdwizard.core import taxonomy

from pymdwizard.gui.wiz_widget import WizardWidget

from ui_files import itis_search


class ItisMainForm(WizardWidget):

    drag_label = "Taxonomy"

    def __init__(self, parent=None):
        # QtGui.QMainWindow.__init__(self, parent)
        super(self.__class__, self).__init__()

        self.selected_items_df = pd.DataFrame(columns=['item', 'tsn'])
        self.selected_model = PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = itis_search.Ui_ItisSearchWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setSizes([300, 100])

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

        model = PandasModel(results)
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
        self.selected_model = PandasModel(self.selected_items_df)
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

    def _to_xml(self):

        df = self.ui.table_include.model().dataframe()
        include_common = self.ui.check_include_common.isChecked()

        fgdc_taxonomy = taxonomy.gen_taxonomy_section(keywords=list(df.item),
                                                      tsns=list(df.tsn),
                                           include_common_names=include_common)

        return fgdc_taxonomy

    def _from_xml(self, contact_information):
        pass
        # contact_dict = xml_utils.node_to_dict(contact_information)
        # utils.populate_widget(self, contact_dict)


class MyPopup(QtGui.QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QtGui.QVBoxLayout()


        self.textEdit = QtGui.QTextEdit()

        layout.addWidget(self.textEdit)

        self.setLayout(layout)



from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, Qt, QPoint
from PyQt4.QtGui import QStyleOptionHeader, QHeaderView, QPainter, QWidget, QStyle, QMatrix, QFont, QFontMetrics, QPalette, QBrush, QColor
import pandas as pd
import datetime


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    options = {"striped": True, "stripesColor": "#fafafa", "na_values": "least",
               "tooltip_min_len": 21}

    def __init__(self, dataframe, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.setDataFrame(dataframe if dataframe is not None else pd.DataFrame())

    def setDataFrame(self, dataframe):
        self.df = dataframe
        #        self.df_full = self.df
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.df.values)

    def columnCount(self, parent=None):
        return self.df.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):

        row, col = index.row(), index.column()
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            ret = self.df.iat[row, col]
            if ret is not None and ret==ret: #convert to str except for None, NaN, NaT
                if isinstance(ret, float):
                    ret = "{:n}".format(ret)
                elif isinstance(ret, datetime.date):
                    #FIXME: show microseconds optionally
                    ret = ret.strftime(("%x", "%c")[isinstance(ret, datetime.datetime)])
                else: ret = str(ret)
                if role == Qt.ToolTipRole:
                    if len(ret)<self.options["tooltip_min_len"]: ret = ""
                return ret
        elif role == Qt.BackgroundRole:
            if self.options["striped"] and row%2:
                return QBrush(QColor(self.options["stripesColor"]))

        return None

    def dataframe(self):
        return self.df

    def reorder(self, oldIndex, newIndex, orientation):
        "Reorder columns / rows"
        horizontal = orientation==Qt.Horizontal
        cols = list(self.df.columns if horizontal else self.df.index)
        cols.insert(newIndex, cols.pop(oldIndex))
        self.df = self.df[cols] if horizontal else self.df.T[cols].T
        return True

    #    def filter(self, filt=None):
    #        self.df = self.df_full if filt is None else self.df[filt]
    #        self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole: return
        label = getattr(self.df, ("columns", "index")[orientation!=Qt.Horizontal])[section]
        #        return label if type(label) is tuple else label
        return ("\n", " | ")[orientation!=Qt.Horizontal].join(str(i) for i in label) if type(label) is tuple else str(label)

    def dataFrame(self):
        return self.df

    def sort(self, column, order):
        if len(self.df):
            asc = order==Qt.AscendingOrder
            na_pos = 'first' if (self.options["na_values"]=="least") == asc else 'last'
            self.df.sort_values(self.df.columns[column], ascending=asc,
                                inplace=True, na_position=na_pos)
            self.layoutChanged.emit()


def main():
    app = QtGui.QApplication(sys.argv)

    # layout = QtGui.QVBoxLayout()
    # layout.addWidget()

    myapp = ItisMainForm()
    myapp.resize(1000, 400)
    myapp.setContentsMargins(0,0,0,0)
    myapp.layout().setContentsMargins(0,0,0,0)


    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()