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
Provide a display widget with a list of schema errors that maintains
functionality to highlight them on the parent application


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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListWidgetItem

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_error_list


class ErrorList(QWidget):

    def __init__(self, main_form, parent=None):
        QWidget.__init__(self, parent=parent)
        self.ui = UI_error_list.Ui_error_list() # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.main_form = main_form
        self.errors = []
        self.ui.listWidget.itemClicked.connect(self.main_form.goto_error)

    def add_error(self, error_msg, xpath):
        action = QListWidgetItem()
        action.setText(error_msg)
        action.setHidden(False)
        action.setData(1, xpath)

        self.ui.listWidget.addItem(action)
        self.errors.append((error_msg, xpath))

    def clear_errors(self):
        self.ui.listWidget.clear()

if __name__ == "__main__":
    utils.launch_widget(ErrorList,
                        "ErrorList", url=r"c:/temp/text.html")
