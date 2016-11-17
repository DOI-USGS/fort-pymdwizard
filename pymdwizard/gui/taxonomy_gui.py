#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
Qt = QtCore.Qt

import pandas as pd

from pymdwizard.core import taxonomy

from ui_files import itis_search


class ItisMainForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = itis_search.Ui_ItisSearchWidget()
        self.ui.setupUi(self)

        self.ui.search_itis_button.clicked.connect(self.search_itis)
        self.ui.tableView.doubleClicked.connect(self.add_tsn)
        self.ui.gen_fgdc_button.clicked.connect(self.generate_fgdc)
        self.ui.search_term.returnPressed.connect(self.search_itis)

        self.selected_items = []

    def search_itis(self):

        if str(self.ui.comboBox.currentText()) == 'Scientific name':
            results = taxonomy.search_by_scientific_name(str(self.ui.search_term.text()))
        else:
            results = taxonomy.search_by_common_name(str(self.ui.search_term.text()))

        model = PandasModel(results)
        self.ui.tableView.setModel(model)

    def add_tsn(self, index):
        df = self.ui.tableView.model()._data
        if str(self.ui.comboBox.currentText()) == 'Scientific name':
            item_name = df['combinedName'][index.row()]
        else:
            item_name = str(df['commonName'][index.row()])

        item = {'tsn': df['tsn'][index.row()],
                'item': str(item_name)}

        self.selected_items.append(item)

        model = PandasModel(pd.DataFrame.from_dict(self.selected_items))
        self.ui.SpeciesToInclude.setModel(model)

    def generate_fgdc(self):
        fgdc_taxonomy = taxonomy.gen_fgdc_taxonomy(list(self.ui.SpeciesToInclude.model()._data.tsn))
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)

        from lxml import etree

        msg.setText(etree.tostring(fgdc_taxonomy, pretty_print=True).decode())
        msg.resize(1000, 400)
        retval = msg.exec_()


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


def main():
    app = QtGui.QApplication(sys.argv)

    # layout = QtGui.QVBoxLayout()
    # layout.addWidget()

    myapp = ItisMainForm()
    myapp.resize(1000, 400)

    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()