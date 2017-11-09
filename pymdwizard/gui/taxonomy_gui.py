#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt

from pymdwizard.core import taxonomy
from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_ITISSearch


class ItisMainForm(QWidget):

    drag_label = "Taxonomy"
    acceptable_tags = ['abstract']

    def __init__(self, xml=None, fgdc_function=None,  parent=None):
        QWidget.__init__(self, parent=parent)
        self.build_ui()
        self.connect_events()

        self.selected_items_df = pd.DataFrame(columns=['item', 'tsn'])
        self.selected_model = utils.PandasModel(self.selected_items_df)
        self.ui.table_include.setModel(self.selected_model)

        self._from_xml(xml)
        self.fgdc_function = fgdc_function

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
        utils.set_window_icon(self)

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

        QApplication.setOverrideCursor(Qt.WaitCursor)
        if str(self.ui.combo_search_type.currentText()) == 'Scientific name':
            results = taxonomy.search_by_scientific_name(str(self.ui.search_term.text()))
        else:
            results = taxonomy.search_by_common_name(str(self.ui.search_term.text()))

        model = utils.PandasModel(results)
        self.ui.table_results.setModel(model)
        QApplication.restoreOverrideCursor()

    def add_tsn(self, index):
        try:
            indexes = self.ui.table_results.selectionModel().selectedRows()
            selected_indices = [int(index.row()) for index in list(indexes)]
            df = self.ui.table_results.model().dataframe()
            indexes = df.index[selected_indices]

            if df.shape[0] == 1:
                index = 0
            elif selected_indices:
                index = selected_indices[0]
            else:
                return

            if 'combinedName' in df.columns:
                item_name = df.iloc[index]['combinedName']
            else:
                try:
                    item_name = str(df.iloc[index]['commonName'])
                except KeyError:
                    msg = "Error, No taxon was selected in the Search Results table!"
                    msg += '\nMake sure the ITIS search returned results and select one before clicking Add Selection. '
                    QMessageBox.information(self, "Problem adding tason", msg)

                    return None

            tsn = df.iloc[index]['tsn']
            i = self.selected_items_df.index.max()+1
            if pd.isnull(i):
                i = 0
            self.selected_items_df.loc[i] = [str(item_name), tsn]
            self.selected_model = utils.PandasModel(self.selected_items_df)
            self.ui.table_include.setModel(self.selected_model)
        except AttributeError:
            pass


    def remove_selected(self, index):
        indexes = self.ui.table_include.selectionModel().selectedRows()
        selected_indices = [int(index.row()) for index in list(indexes)]
        index = self.selected_items_df.index[selected_indices]
        self.selected_items_df.drop(index, inplace=True)
        self.ui.table_include.model().layoutChanged.emit()

    def generate_fgdc(self):
        """
        Generates a FGDC taxonomy section from the content currently in the
        to_include data frame.

        This function then passes the resulting XML to the fgdc_function
        and closes()
        Returns
        -------
        None
        """

        QApplication.setOverrideCursor(Qt.WaitCursor)
        fgdc_taxonomy = self._to_xml()
        self.fgdc_function(fgdc_taxonomy)
        QApplication.restoreOverrideCursor()

        msg = "A taxonomy section has been created and added below"
        QMessageBox.information(self, "Taxonomy created", msg)

        self.close()


    def _to_xml(self):

        df = self.ui.table_include.model().dataframe()
        include_common = self.ui.check_include_common.isChecked()

        fgdc_taxonomy = taxonomy.gen_taxonomy_section(keywords=list(df.item),
                                                      tsns=list(df.tsn),
                                           include_common_names=include_common)

        return fgdc_taxonomy

    def _from_xml(self, taxonomy_element):

        if taxonomy_element is not None:
            i = 0
            for common_node in taxonomy_element.findall('.//common'):
                if common_node.text.startswith('TSN: '):
                    tsn = common_node.text[5:]
                    scientific_name = taxonomy.get_full_record_from_tsn(tsn)['scientificName']['combinedName']
                    self.selected_items_df.loc[i] = [scientific_name, tsn]
                    i += 1

            self.selected_model = utils.PandasModel(self.selected_items_df)
            self.ui.table_include.setModel(self.selected_model)



if __name__ == '__main__':
    utils.launch_widget(ItisMainForm, "Itis testing")