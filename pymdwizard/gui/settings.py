#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


NOTES
------------------------------------------------------------------------------
None
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
        self.settings = QSettings("USGS_2.1.1", "pymdwizard_2.1.1")
        template_fname = self.settings.value("template_fname")

        if template_fname is None:
            template_fname = utils.get_resource_path("CSDGM_Template.xml")

        self.ui.template_fname.setText(template_fname)

        use_spelling = self.settings.value("use_spelling", True)
        if use_spelling == "true":
            self.ui.spelling_on.setChecked(True)
        else:
            self.ui.spelling_off.setChecked(True)

        max_rows = self.settings.value("maxrows", 1000000)
        self.ui.maxrows.setText(str(max_rows))

        defsource = self.settings.value("defsource", "Producer defined")
        self.ui.defsource.setText(defsource)

        fontfamily = self.settings.value("fontfamily", "Arial")
        self.ui.font.setFont(QFont(fontfamily))
        self.ui.font.setCurrentFont(QFont(fontfamily))

        fontsize = self.settings.value("fontsize", 9)
        self.ui.font_size.setValue(fontsize)

    def save_settings(self):
        template_fname = self.ui.template_fname.text()
        if not os.path.exists(template_fname):
            msg = "Could not find specified template file"
            QMessageBox.warning(self, "Invalid template specified", msg)
            return

        self.settings.setValue("template_fname", template_fname)

        self.mainform.switch_spelling(self.ui.spelling_on.isChecked())

        try:
            maxrows = int(self.ui.maxrows.text())
        except:
            maxrows = -9999

        if not maxrows > 0:
            msg = "Max rows must be an integer greater than 0"
            QMessageBox.warning(self, "Invalid Max Rows", msg)
            return

        self.settings.setValue("maxrows", self.ui.maxrows.text())
        self.settings.setValue("defsource", self.ui.defsource.text())

        self.settings.setValue("fontfamily", self.ui.font.currentFont().family())

        self.settings.setValue("fontsize", self.ui.font_size.value())
        self.mainform.metadata_root.set_stylesheet(recursive=True)

        self.deleteLater()
        self.close()

    def restore_defaults(self):
        self.restore_template()
        self.ui.spelling_on.setChecked(True)
        self.ui.defsource.setText("Producer defined")
        self.ui.maxrows.setText("1000000")
        self.ui.font_size.setValue(9)

    def restore_template(self):
        template_fname = utils.get_resource_path("CSDGM_Template.xml")
        self.ui.template_fname.setText(template_fname)

    def browse_template(self):
        template_fname = self.mainform.get_xml_fname()
        if template_fname:
            self.ui.template_fname.setText(template_fname)


if __name__ == "__main__":
    utils.launch_widget(Settings, "Preview")
