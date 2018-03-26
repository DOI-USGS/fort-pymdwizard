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

import math
import pandas as pd

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QAbstractItemView

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_edom_list
from pymdwizard.gui import edom


class EdomList(WizardWidget):  #

    drag_label = "Enumerated Domain <edom>"
    acceptable_tags = ['attr']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_edom_list.Ui_edom_contents()
        self.ui.setupUi(self)

        self.edoms = []

        self.setup_dragdrop(self)
        self.ui.listWidget.setDragDropMode(QAbstractItemView.InternalMove)

        self.ui.btn_addone.clicked.connect(self.add_clicked)
        self.ui.btn_delete.clicked.connect(self.remove_selected)

    def populate_from_list(self, items):
        self.edoms = []
        self.ui.listWidget.clear()

        for item_label in items:
            if (pd.isnull(item_label) or \
                    str(item_label) == '' or \
                    (type(item_label) != str and math.isnan(item_label))):
                if not self.parent().nodata == "<< empty cell >>":
                    self.add_edom("<< empty cell >>")
            else:
                self.add_edom(str(item_label))

    def add_clicked(self):
        self.add_edom()

    def remove_selected(self):
        for item in self.ui.listWidget.selectedItems():
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def add_edom(self, edomv='', edomvd='', edomvds=''):
        item = QListWidgetItem()
        e = edom.Edom(item=item)
        e.ui.fgdc_edomv.setText(edomv)
        if edomvd:
            e.ui.fgdc_edomvd.setPlainText(edomvd)
        if edomvds:
            e.ui.fgdc_edomvds.setText(edomvds)

        item.setSizeHint(e.sizeHint())

        self.ui.listWidget.addItem(item)
        self.ui.listWidget.setItemWidget(item, e)

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        attr = xml_utils.xml_node('attr')
        for i in range(self.ui.listWidget.count()):
            e = self.ui.listWidget.item(i)
            e2  = self.ui.listWidget.itemWidget(e)
            attrdomv = xml_utils.xml_node('attrdomv', parent_node=attr)
            e_node = e2.to_xml()
            attrdomv.append(e_node)

        return attr

    def from_xml(self, attr):
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
            if attr.tag == 'attr':

                self.edoms = []
                self.ui.listWidget.clear()


                for edom in attr.xpath('attrdomv/edom'):
                    edom_dict = xml_utils.node_to_dict(edom, False)

                    self.add_edom(**edom_dict)
            else:
                print ("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(EdomList,
                        "udom testing")

