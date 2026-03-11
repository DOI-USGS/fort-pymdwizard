
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
+ The widget.setStyleSheet does not support rgba for highlights (only rgb).
"""

# Standard python libraries.
import sys
import os
import tempfile
import time
import datetime
import shutil
import subprocess
import traceback

# Non-standard python libraries.
try:
    from git import Repo

    # Cross-platform library that works on Windows, macOS, and Linux.
    import docx

except ImportError as err:
    raise ImportError(err, __file__)

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QMainWindow, QApplication, QSplashScreen,
                                 QMessageBox, QAction, QWidget, QFileDialog,
                                 QDialog, QTabWidget, QGraphicsOpacityEffect,
                                 QLineEdit, QLabel, QVBoxLayout)
    from PyQt5.QtCore import (QFile, QFileInfo, Qt, QSettings,
                              QFileSystemWatcher, QPoint, QSize)
    from PyQt5.QtGui import (QPainter, QPixmap, QMovie)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.gui.ui_files import UI_MainWindow
    from pymdwizard.gui.MetadataRoot import MetadataRoot
    from pymdwizard.core import (xml_utils, utils, fgdc_utils, review_utils)
    from pymdwizard.gui.Preview import Preview
    from pymdwizard.gui.error_list import ErrorList
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.jupyterstarter import JupyterStarter
    from pymdwizard.gui.settings import Settings
    from pymdwizard.gui.sb_locator import SBLocator
    from pymdwizard import __version__
except ImportError as err:
    raise ImportError(err, __file__)


# ---------------------------------------------------------------------------
# SIP-free helpers
# ---------------------------------------------------------------------------

def qwidget_is_valid(widget) -> bool:
    """
    Return True if 'widget' is a live Qt object we can safely touch.
    PyQt raises RuntimeError if a wrapped C/C++ object has been deleted.
    """
    if widget is None:
        return False
    try:
        _ = widget.objectName()
        return True
    except RuntimeError:
        return False


def apply_opacity_effect(target: QWidget, opacity_value: float) -> None:
    """
    Apply a QGraphicsOpacityEffect to the target widget (0.0–1.0).
    """
    if isinstance(target, QWidget):
        try:
            effect = QGraphicsOpacityEffect(target)
            effect.setOpacity(opacity_value)
            target.setGraphicsEffect(effect)
        except RuntimeError:
            pass


class SpinnerDialog(QDialog):
    """Class to generate spinner when checking for software updates."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window flags on dialog and exclude the "?", designated as
        # Qt.WindowContextHelpButtonHint.
        self.setWindowFlags(
            Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # Set the window title and size.
        self.setWindowTitle("USGS Metadata Wizard Update")
        self.setModal(True)
        # Set a rectangular fixed size for the dialog.
        self.setFixedSize(250, 75)

        # Create a label to display the message.
        self.message_label = QLabel("Checking for Software Updates...")
        self.message_label.setAlignment(Qt.AlignCenter)

        # Create a label to display the spinner animation.
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)  # Center the spinner
        gif_path = utils.get_resource_path("icons/spinner.gif")
        self.movie = QMovie(gif_path)  # Load the spinner GIF reliably
        self.label.setMovie(self.movie)  # Set the movie to the label
        self.movie.start()  # Start the animation

        # Create a vertical layout and add both labels.
        layout = QVBoxLayout()
        layout.addWidget(self.message_label)  # Add the message label to layout
        layout.addWidget(self.label)          # Add the spinner label to layout

        # Apply the layout to the dialog.
        self.setLayout(layout)


class PyMdWizardMainForm(QMainWindow):
    """
    Description:
        The main window for the Metadata Wizard application. It handles
        application setup, file management (open/save/recent files),
        user settings, XML validation, error highlighting, and utility
        functions like launching external tools. Inherits from
        QMainWindow.
    """

    # Maximum number of files to monitor.
    max_recent_files = 10

    def __init__(self, parent=None):
        # Initialize the parent QMainWindow class.
        super(self.__class__, self).__init__()

        # Application settings and file state.
        self.settings = QSettings("USGS_" + __version__,
                                  "pymdwizard_" + __version__)
        self.cur_fname = ""
        self.file_watcher = None

        # list of buttons for opening recently accessed files.
        self.recent_file_actions = []

        # list of widgets that are currently styled as errors.
        self.error_widgets = []

        # the last error widget that was highlighted.
        self.last_highlight = None
        self.last_updated = None
        self.ui = None
        self.metadata_root = None

        # Build UI and connect events.
        self.build_ui()
        self.connect_events()
        self.env_cache = {}

        # ScienceBase (SB) locator setup.
        self.sb_file = False
        self.sb_locator = SBLocator(mainform=self)
        utils.set_window_icon(self.sb_locator)

        # Load default file/template.
        self.load_default()

        # Initialize spelling check setting.
        use_spelling = self.settings.value("use_spelling", True, type=bool)
        self.switch_spelling(use_spelling)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.
        """

        # Instantiate and setup the UI.
        self.ui = UI_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the main window icon.
        utils.set_window_icon(self, remove_help=False)

        # Initial window size/pos last saved. Use default values for first time.
        self.resize(self.settings.value("size", QSize(1300, 700)))
        self.move(self.settings.value("pos", QPoint(50, 50)))

        # Initialize and add the main metadata widget.
        self.metadata_root = MetadataRoot()
        self.ui.centralwidget.layout().addWidget(self.metadata_root)

        # Setup the Recent Files menu actions.
        for i in range(PyMdWizardMainForm.max_recent_files):
            self.recent_file_actions.append(
                QAction(self, visible=False,
                        triggered=self.open_recent_file)
            )
            self.ui.menuRecent_Files.addAction(self.recent_file_actions[i])
        self.update_recent_file_actions()

        # Update the Current Template menu item text.
        template_fname = self.settings.value("template_fname")
        if template_fname is not None:
            just_fname = os.path.split(template_fname)[-1]
            self.ui.actionCurrentTemplate.setText("Current: " + just_fname)

        # Disable review document generation if dependency is missing.
        if docx is None:
            self.ui.generate_review.setEnabled(False)

        # Enable drag-and-drop for the main window.
        self.setAcceptDrops(True)

        # Setup the Validation Error List dialog.
        self.error_list = ErrorList(main_form=self)
        self.error_list_dialog = QDialog(self)
        self.error_list_dialog.setWindowTitle("FGDC Validation Errors")
        self.error_list_dialog.setLayout(self.error_list.layout())
        self.error_list_dialog.resize(600, 400)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions.
        """

        # File Menu connections.
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_as.triggered.connect(self.save_as)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionNew.triggered.connect(self.new_record)
        self.ui.actionOpen_sb.triggered.connect(self.open_sb_file)

        # Validation/Preview connections.
        self.ui.actionRun_Validation.triggered.connect(self.validate)
        self.ui.actionClear_validation.triggered.connect(self.clear_validation)
        self.ui.actionPreview.triggered.connect(self.preview)

        # Tool connections.
        self.ui.actionSettings.triggered.connect(self.set_settings)
        self.ui.actionLaunch_Jupyter.triggered.connect(self.launch_jupyter)
        self.ui.generate_review.triggered.connect(self.generate_review_doc)

        # Help/About connections.
        self.ui.actionLaunch_Help.triggered.connect(self.launch_help)
        self.ui.actionCheck_for_Updates.triggered.connect(
            self.check_for_updates)
        self.ui.actionAbout.triggered.connect(self.about)

        # Tab visibility connections.
        self.ui.actionData_Quality.triggered.connect(self.use_dataqual)
        self.ui.actionSpatial.triggered.connect(self.use_spatial)
        self.ui.actionEntity_and_Attribute.triggered.connect(self.use_eainfo)
        self.ui.actionDistribution.triggered.connect(self.use_distinfo)

        # Spelling connection.
        self.ui.actionSpelling_flag.triggered.connect(
            self.spelling_switch_triggered
        )

    def anacondaprompt(self):
        """
        Launches a conda command prompt configured for the
        application's Python environment (Windows only).
        """

        if os.name == "nt":
            root_dir = utils.get_install_dname("root")
            my_env = os.environ.copy()
            my_env["PYTHONPATH"] = os.path.join(root_dir, "pymdwizard")
            # Modify PATH for conda executables
            my_env["PATH"] = ";".join(
                [
                    os.path.join(
                        root_dir, "pymdwizard", "Scripts", "conda_exes"
                    ),
                    my_env["PATH"],
                ]
            )

            pydir = utils.get_install_dname("python")
            my_env["PATH"] = ";".join(
                [os.path.join(pydir, "Scripts", "conda_exes"), my_env["PATH"]]
            )
            activatebat = os.path.join(
                pydir, "Scripts", "activate.bat"
            )

            # Display instructions.
            msg = (
                "This is experimental functionality used for opening "
                "a conda command prompt set to"
                "\nthe Python environment shipped with the "
                "MetadataWizard.\n\n"
                "The base conda env in this prompt is the one to use, "
                "so do not use the activate command."
                "\nUse: conda install ...package.. to install new "
                "packages into the MetadataWizard environment."
            )
            QMessageBox.information(self, "Conda instructions", msg)

            # Launch the command prompt subprocess.
            subprocess.Popen(
                ["start", "cmd", activatebat, pydir],
                env=my_env,
                cwd=pydir,
                shell=True,
            )
        else:
            # Display warning for unsupported OS.
            msg = (
                "This experimental functionality not yet implemented "
                "for Mac or Linux builds"
            )
            QMessageBox.warning(self, "Not implemented", msg)

    def open_recent_file(self):
        """
        Handles the opening of a file selected from the recent files menu.
        """

        action = self.sender()
        if action:
            self.load_file(action.data())
            self.set_current_file(action.data())

    def get_xml_fname(self):
        """
        Launches a file open dialog filtered for XML files.
        """

        recent_files = self.settings.value("recentFileList", [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(
            self, fname, dname, filter="XML Files (*.xml)"
        )

        return fname[0] if fname[0] else ""

    def open_file(self, fname=None):
        """
        Opens a file, either by browsing or using a provided path.
        """

        self.sb_file = False
        if fname is None or not fname:
            fname = self.get_xml_fname()

        if fname:
            self.load_file(fname)
            self.set_current_file(fname)
            self.update_recent_file_actions()

    def open_sb_file(self, hash=None):
        """
        Shows the ScienceBase (SB) locator dialog to download or edit a file.
        """
        self.sb_locator.show()

    def load_file(self, fname, check_for_changes=True):
        """
        Loads a file's content into the application.
        """

        if check_for_changes:
            changed = self.check_for_changes()
            if changed == "Cancel":
                return changed

        # Setup file watcher to monitor external changes.
        self.file_watcher = QFileSystemWatcher([fname])
        self.file_watcher.fileChanged.connect(self.file_updated)
        self.last_updated = time.time()

        self.clear_validation()

        # Check for read access.
        file = QFile(fname)
        if not file.open(QFile.ReadOnly | QFile.Text):
            msg = "Cannot read file {}:\n{}.".format(
                fname, file.errorString()
            )
            QMessageBox.warning(self, "Recent Files", msg)
            return
        file.close()

        self.load_file_content(fname)

    def load_file_content(self, fname):
        """
        Performs reading XML, clearing widgets, and populating the metadata form.
        """

        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()
        self.metadata_root.clear_widget()

        # Ensure all optional sections are visible.
        self.ui.actionData_Quality.setChecked(True)
        self.use_dataqual(True)
        self.ui.actionSpatial.setChecked(True)
        self.use_spatial(True)
        self.ui.actionEntity_and_Attribute.setChecked(True)
        self.use_eainfo(True)
        self.ui.actionDistribution.setChecked(True)
        self.use_distinfo(True)

        try:
            new_record = xml_utils.fname_to_node(fname)
            self.metadata_root.from_xml(new_record)
            self.statusBar().showMessage("File loaded", 10000)
        except BaseException:
            msg = "Cannot open file {}:\n{}.".format(
                fname, traceback.format_exc()
            )
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Recent Files", msg)
        QApplication.restoreOverrideCursor()

    def file_updated(self):
        """
        Fired when QFileSystemWatcher detects external file change. Prompts user to reload.
        """

        # Debounce check
        if not self.cur_fname:
            return

        if time.time() - self.last_updated >= 4:
            msg = (
                "The file you are editing has been changed on disk.  "
                "Would you like to reload this File?"
            )
            self.last_updated = time.time()
            confirm = QMessageBox.question(
                self,
                "File Changed",
                msg,
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                self.load_file(self.cur_fname)

    def save_as(self):
        """
        Prompts the user for a new filename and saves the current document to that location.
        """

        fname = self.get_save_name()
        if fname:
            self.set_current_file(fname)
            self.update_recent_file_actions()
            self.save_file()

    def get_save_name(self):
        """
        Launches a save-as dialog to select a save location.
        """

        recent_files = self.settings.value("recentFileList", [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        fname = QFileDialog.getSaveFileName(
            self, "Save As", dname, filter="XML Files (*.xml)"
        )

        return fname[0]

    def save_file(self):
        """
        Saves the current XML document.
        """

        utils.get_install_dname()

        if not self.cur_fname:
            fname = self.get_save_name()
            if not fname:
                return
        else:
            fname = self.cur_fname

        fname_msg = utils.check_fname(fname)
        if not fname_msg == "good":
            msg = "Cannot write to :\n  {}.".format(fname)
            QMessageBox.warning(self, "Metadata Wizard", msg)
            return

        tool_comment = (
            "Record created using version {} of the "
            "USGS Metadata Wizard tool. (https://github.com/DOI-USGS/"
            "fort-pymdwizard)".format(__version__)
        )
        xml_contents = self.metadata_root.to_xml()
        comment = xml_utils.xml_node(
            tag="", text=tool_comment, index=0, comment=True
        )
        xml_contents.addprevious(comment)

        xml_utils.save_to_file(xml_contents, fname)
        self.last_updated = time.time()

        self.set_current_file(fname)
        self.statusBar().showMessage("File saved", 2000)

    def new_record(self):
        """
        Creates a new record by copying the template file to a user-selected location.
        """

        self.load_default()
        save_as_fname = self.get_save_name()
        if save_as_fname:
            template_fname = self.settings.value("template_fname")
            if template_fname is None or not os.path.exists(template_fname):
                template_fname = utils.get_resource_path("CSDGM_Template.xml")

            shutil.copyfile(template_fname, save_as_fname)

            self.load_file(save_as_fname)
            self.set_current_file(save_as_fname)
            self.update_recent_file_actions()

            today = fgdc_utils.format_date(datetime.datetime.now())
            self.metadata_root.metainfo.metd.set_date(today)
            this_year = today[:4]
            self.metadata_root.idinfo.citation.ui.pubdate_widget.set_date(
                this_year
            )

    def set_settings(self):
        """
        Opens the application settings dialog.
        """

        self.settings_dialog = Settings(mainform=self)
        self.settings_dialog.setWindowTitle("MetadataWizard Settings")
        utils.set_window_icon(self.settings_dialog)
        self.settings_dialog.show()

    def load_default(self):
        """
        Loads the content of the default template file.
        """

        template_fname = self.settings.value("template_fname")

        if template_fname is None:
