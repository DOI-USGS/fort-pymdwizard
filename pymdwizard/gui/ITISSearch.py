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

import pandas as pd

from PyQt5.QtWidgets import QWidget

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