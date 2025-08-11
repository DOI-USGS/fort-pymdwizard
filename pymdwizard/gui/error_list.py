#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a display widget with a list of schema errors that maintains
functionality to highlight them on the parent application


NOTES
------------------------------------------------------------------------------
None
"""

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtWidgets import QListWidgetItem
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_error_list
except ImportError as err:
    raise ImportError(err, __file__)


class ErrorList(QWidget):
    def __init__(self, main_form, parent=None):
        QWidget.__init__(self, parent=parent)
        self.ui = UI_error_list.Ui_error_list()  # .Ui_USGSContactInfoWidgetMain()
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
    utils.launch_widget(ErrorList, "ErrorList", url=r"c:/temp/text.html")
