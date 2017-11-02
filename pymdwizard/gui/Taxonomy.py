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

from copy import deepcopy

from PyQt5.QtCore import QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_taxonomy
from pymdwizard.gui import taxonomy_gui

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
        self.ui = UI_taxonomy.Ui_Taxonomy()
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

        self.tax_gui = taxonomy_gui.ItisMainForm(xml=self.to_xml(),
                                                 fgdc_function=self.from_xml)
        fg = self.frameGeometry()
        self.tax_gui.move(fg.topRight() - QPoint(150, -25))
        self.tax_gui.show()

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

    def to_xml(self):

        taxonomy = xml_utils.xml_node('taxonomy')
        taxonomy.append(self.keywtax.to_xml())

        if self.original_xml is not None:
            taxonsys = xml_utils.search_xpath(self.original_xml, 'taxonsys')
            if taxonsys is not None:
                taxonsys.tail = None
                taxonomy.append(deepcopy(taxonsys))

            taxongen = xml_utils.search_xpath(self.original_xml, 'taxongen')
            if taxongen is not None:
                taxongen.tail = None
                taxonomy.append(deepcopy(taxongen))

        taxonomy.append(self.taxoncl.to_xml())
        return taxonomy

    def from_xml(self, taxonomy_element):
        self.original_xml = taxonomy_element

        self.clear_widget()
        self.ui.rbtn_yes.setChecked(True)

        keywtax = taxonomy_element.xpath('keywtax')
        if keywtax:
            self.keywtax.from_xml(taxonomy_element.xpath('keywtax')[0])

        taxoncl = taxonomy_element.xpath('taxoncl')
        if taxoncl:
            self.taxoncl.from_xml(taxoncl[0])

if __name__ == "__main__":
    utils.launch_widget(Taxonomy, "Taxonomy testing")







