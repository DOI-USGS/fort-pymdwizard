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
import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_settings


class Settings(QWidget):

    def __init__(self, url=None, mainform=None, parent=None):
        QWidget.__init__(self, parent=parent)
        self.ui = UI_settings.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.mainform = mainform

        self.connect_events()

        self.load_settings()

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_browse.clicked.connect(self.browse_template)
        self.ui.btn_restore_template.clicked.connect(self.restore_template)
        self.ui.btn_restore_defaults.clicked.connect(self.restore_defaults)
        self.ui.btn_save.clicked.connect(self.save_settings)

    def load_settings(self):
        self.settings = QSettings('USGS', 'pymdwizard')
        template_fname = self.settings.value('template_fname')

        if template_fname is None:
            template_fname = utils.get_resource_path('CSDGM_Template.xml')

        self.ui.template_fname.setText(template_fname)

        use_spelling = self.settings.value('use_spelling', True)
        if use_spelling == 'true':
            self.ui.spelling_on.setChecked(True)
        else:
            self.ui.spelling_off.setChecked(True)

        max_rows = self.settings.value('maxrows', 1000000)
        self.ui.maxrows.setText(str(max_rows))

        defsource = self.settings.value('defsource', 'Producer defined')
        self.ui.defsource.setText(defsource)

        fontfamily = self.settings.value('fontfamily', 'Arial')
        self.ui.font.setFont(QFont(fontfamily))
        self.ui.font.setCurrentFont(QFont(fontfamily))

        fontsize = self.settings.value('fontsize', 9)
        self.ui.font_size.setValue(fontsize)

    def save_settings(self):
        template_fname = self.ui.template_fname.text()
        if not os.path.exists(template_fname):
            msg = "Could not find specified template file"
            QMessageBox.warning(self, "Invalid template specified", msg)
            return

        self.settings.setValue('template_fname', template_fname)

        self.mainform.switch_spelling(self.ui.spelling_on.isChecked())

        try:
            maxrows = int(self.ui.maxrows.text())
        except:
            maxrows = -9999

        if not maxrows > 0:
            msg = "Max rows must be an integer greater than 0"
            QMessageBox.warning(self, "Invalid Max Rows", msg)
            return

        self.settings.setValue('maxrows', self.ui.maxrows.text())
        self.settings.setValue('defsource', self.ui.defsource.text())

        self.settings.setValue('fontfamily', self.ui.font.currentFont().family())

        self.settings.setValue('fontsize', self.ui.font_size.value())
        self.mainform.metadata_root.set_stylesheet(recursive=True)

        self.deleteLater()
        self.close()

    def restore_defaults(self):
        self.restore_template()
        self.ui.spelling_on.setChecked(True)
        self.ui.defsource.setText('Producer defined')
        self.ui.maxrows.setText('1000000')
        self.ui.font_size.setValue(9)

    def restore_template(self):
        template_fname = utils.get_resource_path('CSDGM_Template.xml')
        self.ui.template_fname.setText(template_fname)

    def browse_template(self):
        template_fname = self.mainform.get_xml_fname()
        if template_fname:
            self.ui.template_fname.setText(template_fname)




if __name__ == "__main__":
    utils.launch_widget(Settings,
                        "Preview")
