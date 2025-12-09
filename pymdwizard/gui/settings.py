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

# Standard python libraries.
import os

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QWidget, QMessageBox)
    from PyQt5.QtCore import QSettings
    from PyQt5.QtGui import QFont
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_settings
    from pymdwizard import __version__
except ImportError as err:
    raise ImportError(err, __file__)


class Settings(QWidget):
    """
    Description:
        A widget used to manage application settings, including the
        default template file, spelling checker status, row limits,
        default source, and font preferences.

    Passed arguments:
        url (str, optional): Not used, retained for compatibility.
        mainform (QWidget, optional): Reference to the main application
            form for applying settings changes.
        parent (QWidget, optional): The parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes UI and loads saved settings upon creation.
        2. Connects buttons for browsing, restoring, and saving settings.
        3. Persists settings using "QSettings".

    Notes:
        Inherits from "QWidget". Uses "USGS_x.x.x" and "pymdwizard_x.x.x"
        as QSettings organization and application names.
    """

    def __init__(self, url=None, mainform=None, parent=None):
        """
        Initialize the Settings widget.
        """

        # Call the base class constructor.
        QWidget.__init__(self, parent=parent)
        self.ui = UI_settings.Ui_Form()
        self.ui.setupUi(self)

        # Store reference to the main application form.
        self.mainform = mainform

        self.connect_events()

        # Load saved settings upon initialization.
        self.load_settings()

    def connect_events(self):
        """
        Description:
            Connects the appropriate GUI components with the
            corresponding functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects button clicks for template browsing, restoring
            settings, and saving.

        Notes:
            None
        """

        self.ui.btn_browse.clicked.connect(self.browse_template)
        self.ui.btn_restore_template.clicked.connect(self.restore_template)
        self.ui.btn_restore_defaults.clicked.connect(self.restore_defaults)
        self.ui.btn_save.clicked.connect(self.save_settings)

    def load_settings(self):
        """
        Description:
            Loads application settings from persistent storage and
            populates the UI fields.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Initializes "QSettings".
            2. Loads and sets values for template file, spelling,
               max rows, default source, and font preferences.

        Notes:
            None
        """

        # Initialize QSettings with app/org names.
        self.settings = QSettings("USGS_" + __version__,
                                  "pymdwizard_" + __version__)

        # Load Template File Name.
        template_fname = self.settings.value("template_fname")
        if template_fname is None:
            template_fname = utils.get_resource_path("CSDGM_Template.xml")
        self.ui.template_fname.setText(template_fname)

        # Load Spelling Status.
        use_spelling = self.settings.value("use_spelling", True)
        if use_spelling == "true":
            self.ui.spelling_on.setChecked(True)
        else:
            self.ui.spelling_off.setChecked(True)

        # Load Max Rows.
        max_rows = self.settings.value("maxrows", 1000000)
        self.ui.maxrows.setText(str(max_rows))

        # Load Default Source.
        defsource = self.settings.value("defsource",
                                        "Producer defined")
        self.ui.defsource.setText(defsource)

        # Load Font Family.
        fontfamily = self.settings.value("fontfamily", "Arial")
        self.ui.font.setFont(QFont(fontfamily))
        self.ui.font.setCurrentFont(QFont(fontfamily))

        # Load Font Size.
        fontsize = self.settings.value("fontsize", 9)
        self.ui.font_size.setValue(fontsize)

    def save_settings(self):
        """
        Description:
            Validates current settings, saves them to persistent
            storage, and applies font settings to the main form.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Validates template file existence and max rows value.
            2. Saves all setting values to "QSettings".
            3. Calls mainform methods to apply spelling and font changes.
            4. Closes the dialog.

        Notes:
            None
        """

        # Validate template file path.
        template_fname = self.ui.template_fname.text()
        if not os.path.exists(template_fname):
            msg = "Could not find specified template file"
            QMessageBox.warning(self, "Invalid template specified", msg)
            return

        self.settings.setValue("template_fname", template_fname)

        # Apply spelling change to main form.
        self.mainform.switch_spelling(self.ui.spelling_on.isChecked())

        # Define and validate Max Rows input.
        try:
            maxrows = int(self.ui.maxrows.text())
        except:
            maxrows = -9999
        if not maxrows > 0:
            msg = "Max rows must be an integer greater than 0"
            QMessageBox.warning(self, "Invalid Max Rows", msg)
            return

        # Save remaining settings.
        self.settings.setValue("maxrows", self.ui.maxrows.text())
        self.settings.setValue("defsource", self.ui.defsource.text())
        self.settings.setValue("fontfamily",
                               self.ui.font.currentFont().family())
        self.settings.setValue("fontsize", self.ui.font_size.value())

        # Apply font stylesheet recursively to main form.
        self.mainform.metadata_root.set_stylesheet(recursive=True)

        # Close the settings dialog.
        self.deleteLater()
        self.close()

    def restore_defaults(self):
        """
        Description:
            Sets all UI elements back to their default, recommended
            application values.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls "restore_template" and sets spelling, default source,
            max rows, and font size to their factory defaults.

        Notes:
            Does not save settings; requires a call to "save_settings".
        """

        self.restore_template()
        self.ui.spelling_on.setChecked(True)
        self.ui.defsource.setText("Producer defined")
        self.ui.maxrows.setText("1000000")
        self.ui.font_size.setValue(9)

    def restore_template(self):
        """
        Description:
            Sets the template file path back to the default internal
            CSDGM template resource path.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the resource path for "CSDGM_Template.xml" and updates
            the template file field.

        Notes:
            None
        """

        template_fname = utils.get_resource_path("CSDGM_Template.xml")
        self.ui.template_fname.setText(template_fname)

    def browse_template(self):
        """
        Description:
            Opens a file dialog to allow the user to select a custom
            XML template file.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls a mainform utility to open the dialog and updates
            the template file field if a file is selected.

        Notes:
            None
        """

        template_fname = self.mainform.get_xml_fname()
        if template_fname:
            self.ui.template_fname.setText(template_fname)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Settings, "Preview")
