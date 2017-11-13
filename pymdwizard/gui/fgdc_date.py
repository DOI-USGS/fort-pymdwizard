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

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_fgdc_date


class FGDCDate(QWidget):

    def __init__(self, parent=None, show_format=True, label='',
                 required=False, fgdc_name=None, parent_fgdc_name=None):
        QWidget.__init__(self, parent=parent)

        self.build_ui()

        if not show_format:
            self.ui.widget_format.hide()

        if label:
            self.ui.label.setText(label)
        else:
            self.ui.label.visible = False

        if not required:
            self.ui.lbl_required.hide()

        self.date_widget = self.ui.fgdc_caldate
        if fgdc_name is not None:
            self.ui.fgdc_caldate.setObjectName(fgdc_name)

        if parent_fgdc_name is not None:
            self.ui.parent_fgdc.setObjectName(parent_fgdc_name)

        self.last_checked_contents = ''
        self.connect_events()

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_fgdc_date.Ui_parent_widget()
        self.ui.setupUi(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.date_widget.editingFinished.connect(self.check_format)

    def check_format(self):

        cur_contents = self.date_widget.text()
        if cur_contents == self.last_checked_contents:
            return
        else:
            self.last_checked_contents = cur_contents

        msg = ''
        if len(cur_contents) not in (0, 4, 6, 8):
            msg = "An FGDC date needs to be 4, 6, or 8 numbers long, or be 'Unknown'"
        if not cur_contents.isdigit():
            msg = "An FGDC date can only consist of numbers"

        if cur_contents == 'Unknown':
            msg = ''

        if msg:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(msg)
            msgbox.setInformativeText("YYYY or YYYYMM or YYYYMMDD or 'Unknown'")
            msgbox.setWindowTitle("Problem with FGDC date format")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def get_date(self):
        return self.date_widget.text()

    def set_date(self, date_str):
        self.date_widget.setText(date_str)


if __name__ == "__main__":
    utils.launch_widget(FGDCDate, label='testing', show_format=False,
                        parent_fgdc_name='fgdc_sngdate')







