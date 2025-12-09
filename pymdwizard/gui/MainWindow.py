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

    # Use functions, classes, and other elements from C/C++ libraries directly
    # within your Python code.
    import sip
except ImportError as err:
    raise ImportError(err, __file__)

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QMainWindow, QApplication, QSplashScreen,
                                 QMessageBox, QAction, QWidget, QFileDialog,
                                 QDialog, QTabWidget)
    from PyQt5.QtCore import (QFile, QFileInfo, Qt, QSettings,
                              QFileSystemWatcher, QPoint, QSize)
    from PyQt5.QtGui import (QPainter, QPixmap)
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


class PyMdWizardMainForm(QMainWindow):
    """
    Description:
        The main window for the Metadata Wizard application. It handles
        application setup, file management (open/save/recent files),
        user settings, XML validation, error highlighting, and utility
        functions like launching external tools. Inherits from
        QMainWindow.

    Passed arguments:
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes settings, UI components, and event connections.
        2. Loads the default or template file content.
        3. Manages state for file watching, recent files, and validation
           errors.

    Notes:
        The "file_watcher" monitors the currently open file for external
        changes, prompting the user to reload if detected.
    """

    # Maximum number of files to monitor.
    max_recent_files = 10

    def __init__(self, parent=None):
        # Initialize the parent QMainWindow class.
        super(self.__class__, self).__init__()

        # Application settings and file state. TODO: Remove hardcoding ???????????????????
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
        use_spelling = self.settings.value("use_spelling", "true")
        if isinstance(use_spelling, str):
            use_spelling = eval(use_spelling.capitalize())
        self.switch_spelling(use_spelling)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets up the main UI from the designer file, restores window
            size/position, initializes the "MetadataRoot" widget, sets
            up the Recent Files menu, and initializes the Error List
            dialog.

        Notes:
            Disables the "Generate Review" action if the "docx" library
            is not available.
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
        Description:
            Connect the appropriate GUI components with the corresponding
            functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects all Menu Bar actions (File, Tools, Help, etc.) to
            their respective handler methods.

        Notes:
            None
        """

        # File Menu connections.
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_as.triggered.connect(self.save_as)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionNew.triggered.connect(self.new_record)

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
        Description:
            Launches an Anaconda command prompt configured for the
            application's Python environment (Windows only).

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Configures necessary environment variables (PYTHONPATH, PATH),
            displays instructional warning, and starts a command prompt
            subprocess.

        Notes:
            None
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
            self.ui.actionOpen_sb.triggered.connect(self.open_sb_file)
            activatebat = os.path.join(
                pydir, "Scripts", "conda_exe", "activate.bat"
            )

            # Display instructions.  TODO: Anaconda is not allowed. ??????????????????????????????????????
            msg = (
                "This is experimental functionality used for opening "
                "an Anaconda command prompt set to"
                "\nthe Python environment shipped with the "
                "MetadataWizard.\n\n"
                "The base conda env in this prompt is the one to use, "
                "so do not use the activate command."
                "\nUse: conda install ...package.. to install new "
                "packages into the MetadataWizard envronment."
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
        Description:
            Handles the opening of a file selected from the recent files
            menu.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the QAction object that triggered the event, extracts
            the file path (data), and calls "load_file" and
            "set_current_file".

        Notes:
            None
        """

        # Get the QAction that triggered the event.
        action = self.sender()
        if action:
            # action.data() holds the file path.
            self.load_file(action.data())
            self.set_current_file(action.data())

    def get_xml_fname(self):
        """
        Description:
            Launches a file open dialog filtered for XML files.

        Passed arguments:
            None

        Returned objects:
            str: Path and filename of the selected file, or empty string
                if none was selected.

        Workflow:
            Initializes the dialog using the directory of the most
            recently opened file and returns the selected path.

        Notes:
            None
        """

        # Get the directory of the most recent file for starting location.
        recent_files = self.settings.value("recentFileList", [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        # Launch the open file dialog.
        fname = QFileDialog.getOpenFileName(
            self, fname, dname, filter="XML Files (*.xml)"
        )

        # Return the file path (first element of the tuple).
        if fname[0]:
            return fname[0]
        else:
            return ""

    def open_file(self, fname=None):
        """
        Description:
            Opens a file, either by browsing or using a provided path.

        Passed arguments:
            fname (str, optional): Full path to the file to open. If
                None, a dialog is launched.

        Returned objects:
            None

        Workflow:
            1. Prompts for file name if not provided.
            2. Calls "load_file" and updates recent file actions.

        Notes:
            None
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
        Description:
            Shows the ScienceBase (SB) locator dialog to download or
            edit a file from SB.

        Passed arguments:
            hash (str, optional): SB item ID/hash to be edited (unused
                in this simple implementation).

        Returned objects:
            None

        Workflow:
            Simply shows the SB locator widget.

        Notes:
            None
        """

        self.sb_locator.show()

    def load_file(self, fname, check_for_changes=True):
        """
        Description:
            Loads a file's content into the application.

        Passed arguments:
            fname (str): Full file path and name of the file to load.
            check_for_changes (bool): If True, checks for unsaved
                changes before loading.

        Returned objects:
            str or None: "Cancel" if the user cancels saving changes,
                otherwise None.

        Workflow:
            1. Checks for unsaved changes.
            2. Sets up the "QFileSystemWatcher".
            3. Clears validation errors.
            4. Checks for file read access.
            5. Calls "load_file_content" to perform the actual load.

        Notes:
            None
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
        Description:
            Performs the heavy lifting of reading XML, clearing widgets,
            and populating the metadata form.

        Passed arguments:
            fname (str): Full file path and name.

        Returned objects:
            None

        Workflow:
            1. Sets the cursor to Wait mode.
            2. Clears the root widget and ensures all optional sections
               are initially visible (checked).
            3. Reads XML from file, populates "metadata_root".
            4. Handles potential exceptions during parsing.

        Notes:
            None
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
            # Convert file to XML node and populate form.
            new_record = xml_utils.fname_to_node(fname)
            self.metadata_root.from_xml(new_record)
            self.statusBar().showMessage("File loaded", 10000)
        except BaseException as e:
            msg = "Cannot open file {}:\n{}.".format(
                fname, traceback.format_exc()
            )
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Recent Files", msg)
        QApplication.restoreOverrideCursor()

    def file_updated(self):
        """
        Description:
            Fired when "QFileSystemWatcher" detects external file change.
            Prompts user to reload.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Checks time since last update (debounce).
            2. Displays confirmation dialog.
            3. Reloads the file if user confirms.

        Notes:
            The 4-second delay prevents self-triggering from save
            operations.
        """

        # Debounce check
        if time.time() - self.last_updated > 4:
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
        Description:
            Prompts the user for a new filename and saves the current
            document to that location.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Gets the new save name via dialog.
            2. Updates current file/recent file list.
            3. Calls "save_file".

        Notes:
            None
        """

        fname = self.get_save_name()
        if fname:
            self.set_current_file(fname)
            self.update_recent_file_actions()
            self.save_file()

    def get_save_name(self):
        """
        Description:
            Launches a save-as dialog to select a save location.

        Passed arguments:
            None

        Returned objects:
            str: File name and path, or empty string if canceled.

        Workflow:
            Initializes the dialog using the directory of the most
            recently opened file and returns the selected path.

        Notes:
            None
        """

        # Get starting directory from recent files.
        recent_files = self.settings.value("recentFileList", [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        # Launch the save file dialog.
        fname = QFileDialog.getSaveFileName(
            self, "Save As", dname, filter="XML Files (*.xml)"
        )

        return fname[0]

    def save_file(self):
        """
        Description:
            Saves the current XML document. Prompts for a filename if
            "self.cur_fname" is not set.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Checks if a filename is set; if not, calls "get_save_name".
            2. Validates write access.
            3. Generates XML from "metadata_root".
            4. Adds the application version comment to the XML header.
            5. Writes XML to file and updates status bar/file state.

        Notes:
            None
        """

        # Ensure utility path is accessible (Test/Initialization).
        utils.get_install_dname()

        # Check/Get filename.
        if not self.cur_fname:
            fname = self.get_save_name()
            if not fname:
                return
        else:
            fname = self.cur_fname

        # Check for write access.
        fname_msg = utils.check_fname(fname)
        if not fname_msg == "good":
            msg = "Cannot write to :\n  {}.".format(fname)
            QMessageBox.warning(self, "Metadata Wizard", msg)
            return

        # Generate XML and add tool comment.
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

        # Save to file.
        xml_utils.save_to_file(xml_contents, fname)
        self.last_updated = time.time()

        self.set_current_file(fname)
        self.statusBar().showMessage("File saved", 2000)

    def new_record(self):
        """
        Description:
            Creates a new record by copying the template file to a
            user-selected location.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Loads the default template content.
            2. Prompts user for a save-as filename.
            3. Copies the template to the new filename.
            4. Loads the new file and updates the metadata date fields.

        Notes:
            None
        """

        self.load_default()
        save_as_fname = self.get_save_name()
        if save_as_fname:
            # Determine the template source file.
            template_fname = self.settings.value("template_fname")
            if template_fname is None or not os.path.exists(template_fname):
                template_fname = utils.get_resource_path("CSDGM_Template.xml")

            # Copy template to the new file path.
            shutil.copyfile(template_fname, save_as_fname)

            # Load the new file and update history.
            self.load_file(save_as_fname)
            self.set_current_file(save_as_fname)
            self.update_recent_file_actions()

            # Update Metadata Date and Citation Pub Date to current date.
            today = fgdc_utils.format_date(datetime.datetime.now())
            self.metadata_root.metainfo.metd.set_date(today)
            this_year = today[:4]
            self.metadata_root.idinfo.citation.ui.pubdate_widget.set_date(
                this_year
            )

    def set_settings(self):
        """
        Description:
            Opens the application settings dialog.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates and shows the "Settings" dialog.

        Notes:
            None
        """

        self.settings_dialog = Settings(mainform=self)
        self.settings_dialog.setWindowTitle("MetadataWizard Settings")
        utils.set_window_icon(self.settings_dialog)
        self.settings_dialog.show()

    def load_default(self):
        """
        Description:
            Loads the content of the default template file.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Determines the template file path (user setting or default).
            2. Handles cases where the user's template file is missing.
            3. Loads the content and clears the current filename/path.
            4. Sets the metadata date to today.

        Notes:
            None
        """

        template_fname = self.settings.value("template_fname")

        # Determine if template is user-defined or default.
        if template_fname is None:
            template_fname = utils.get_resource_path("CSDGM_Template.xml")
        elif not os.path.exists(template_fname):
            # Warn if user-defined template is missing
            msg = (
                "The previous template file specified, {}, could not be "
                "found.".format(template_fname)
            )
            msg += (
                "\nCheck that the file has not beed deleted, renamed "
                "or moved. Defaulting to the built in template.".format(
                    template_fname
                )
            )
            QMessageBox.warning(self, "Template file missing", msg)
            template_fname = utils.get_resource_path("CSDGM_Template.xml")

        # Load template content and reset current file tracking.
        self.load_file_content(template_fname)
        self.cur_fname = ""

        # Set metadata date to today.
        today = fgdc_utils.format_date(datetime.datetime.now())
        self.metadata_root.metainfo.metd.set_date(today)

    def set_current_file(self, fname):
        """
        Description:
            The procedure for storing and displaying a new current file.

        Passed arguments:
            fname (str): The file name and path that will be used.

        Returned objects:
            None

        Workflow:
            1. Updates the main window title.
            2. Manages the "recentFileList" in QSettings (removes old,
               inserts new, truncates list).
            3. Triggers the update of the Recent Files menu.

        Notes:
            None
        """

        self.cur_fname = fname
        if fname:
            # Update window title.
            stripped_name = QFileInfo(fname).fileName()
            title = "Metadata Wizard - {}".format(stripped_name)
            self.setWindowTitle(title)

            # Update recent file list in settings.
            files = self.settings.value("recentFileList", [])

            try:
                files.remove(fname)
            except ValueError:
                pass

            files.insert(0, fname)

            # Truncate list to max_recent_files.
            del files[PyMdWizardMainForm.max_recent_files :]

            self.settings.setValue("recentFileList", files)

            # Update menu actions across all main windows.
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, PyMdWizardMainForm):
                    widget.update_recent_file_actions()
        else:
            self.setWindowTitle("Metadata Wizard")

    def update_recent_file_actions(self):
        """
        Description:
            Updates the actions (menu items) in the recent files list to
            reflect the stored file paths.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Retrieves the recent file list from settings.
            2. Iterates, sets text (with index prefix), sets file data,
               and makes actions visible/invisible as needed.

        Notes:
            None
        """

        files = self.settings.value("recentFileList", [])

        num_recent_files = min(len(files), PyMdWizardMainForm.max_recent_files)

        # Set visible actions.
        for i in range(num_recent_files):
            stripped_name = QFileInfo(files[i]).fileName()
            text = "&%d %s" % (i + 1, stripped_name)
            self.recent_file_actions[i].setText(text)
            self.recent_file_actions[i].setData(files[i])
            self.recent_file_actions[i].setVisible(True)

        # Hide unused actions.
        for j in range(num_recent_files, PyMdWizardMainForm.max_recent_files):
            self.recent_file_actions[j].setVisible(False)

    def check_for_changes(self):
        """
        Description:
            Checks if the current document has unsaved changes by comparing
            the form's XML content to the file on disk.

        Passed arguments:
            None

        Returned objects:
            str or None: "Cancel" if user cancels exit, otherwise None.

        Workflow:
            1. Reads XML from the current file and generates XML from the
               form.
            2. Compares the string representations.
            3. If different, prompts the user to save, discard, or cancel.

        Notes:
            None
        """

        try:
            # Check if file exists and current filename is set.
            if self.cur_fname and os.path.exists(self.cur_fname):
                # Generate XML from current form state.
                cur_xml = xml_utils.node_to_string(
                    self.metadata_root.to_xml()
                )

                # Read XML from disk.
                disk_xml = xml_utils.node_to_string(
                    xml_utils.fname_to_node(self.cur_fname)
                )

            # Compare XML content.
            if cur_xml != disk_xml:
                msg = "Do you want to save your changes?"
                self.last_updated = time.time()
                confirm = QMessageBox.question(
                    self,
                    "Save Changes",
                    msg,
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                )
                if confirm == QMessageBox.Yes:
                    # Save the file
                    xml_utils.save_to_file(
                        self.metadata_root.to_xml(), self.cur_fname
                    )
                elif confirm == QMessageBox.Cancel:
                    return "Cancel"
        except:
            pass

    def exit(self):
        """
        Description:
            Checks for unsaved changes and prompts the user before closing
            the application.

        Passed arguments:
            None

        Returned objects:
            str: "Close" or "Cancel" depending on user choice.

        Workflow:
            Calls "check_for_changes" and then either closes or returns
            "Cancel".

        Notes:
            None
        """

        changed = self.check_for_changes()
        if changed == "Cancel":
            return changed
        else:
            self.close()
            return "Close"

    def closeEvent(self, event):
        """
        Description:
            Intercepts the built-in "closeEvent" to run the save-check
            (self.exit()) before closing the main window.

        Passed arguments:
            event (QCloseEvent): The closing event object.

        Returned objects:
            None

        Workflow:
            1. Calls self.exit().
            2. If "Close" is returned, saves window position/size and
               accepts the event.
            3. If "Cancel" is returned, ignores the event.

        Notes:
            None
        """

        if self.exit() == "Close":
            # Save geometry before closing.
            self.settings.setValue("size", self.size())
            self.settings.setValue("pos", self.pos())
            event.accept()
        else:
            event.ignore()

    def use_dataqual(self, sender=None):
        """
        Description:
            Toggles the visibility of the Data Quality tab.

        Passed arguments:
            sender (bool, optional): State from the triggered action.

        Returned objects:
            None

        Workflow:
            Calls the root widget's section toggler.

        Notes:
            None
        """

        self.metadata_root.use_section("dataqual", sender)

    def use_spatial(self, sender=None):
        """
        Description:
            Toggles the visibility of the Spatial tab.

        Passed arguments:
            sender (bool, optional): State from the triggered action.

        Returned objects:
            None

        Workflow:
            Calls the root widget's section toggler.

        Notes:
            None
        """

        self.metadata_root.use_section("spatial", sender)

    def use_eainfo(self, sender=None):
        """
        Description:
            Toggles the visibility of the Entity and Attribute tab.

        Passed arguments:
            sender (bool, optional): State from the triggered action.

        Returned objects:
            None

        Workflow:
            Calls the root widget's section toggler.

        Notes:
            None
        """

        self.metadata_root.use_section("eainfo", sender)

    def use_distinfo(self, sender=None):
        """
        Description:
            Toggles the visibility of the Distribution tab.

        Passed arguments:
            sender (bool, optional): State from the triggered action.

        Returned objects:
            None

        Workflow:
            Calls the root widget's section toggler.

        Notes:
            None
        """

        self.metadata_root.use_section("distinfo", sender)

    def clear_validation(self):
        """
        Description:
            Removes the error highlighting (red border/background) from
            all previously marked widgets and clears the error list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Iterates through "error_widgets".
            2. Resets the widget's style sheet and tool tip to default.
            3. Clears the "error_widgets" list and the "ErrorList" dialog.

        Notes:
            Uses "sip.isdeleted" to safely check widget lifecycle.
        """

        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        for widget in self.error_widgets:
            # Check if the widget still exists.
            if not sip.isdeleted(widget) and widget.objectName() not in [
                "metadata_root",
                "fgdc_metadata",
            ]:
                widget.setStyleSheet("""""")
                print(widget.objectName())

                # Attempt to restore default tooltip (annotation).
                shortname = widget.objectName().replace("fgdc_", "")
                if shortname[-1].isdigit():
                    shortname = shortname[:-1]
                try:
                    widget.setToolTip(
                        annotation_lookup[shortname]["annotation"])
                except KeyError:
                    widget.setToolTip("")

        self.error_widgets = []
        self.error_list.clear_errors()
        self.error_list_dialog.hide()

    def validate(self):
        """
        Description:
            Checks the current record against the FGDC schema using XSD
            validation and highlights error widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Shows the error list dialog.
            2. Determines the correct XSD schema file.
            3. Calls "fgdc_utils.validate_xml".
            4. Clears previous validation highlights.
            5. Iterates through errors: expands complex sections (e.g.,
               attributes) and calls "highlight_error" for relevant widgets.
            6. Displays success/failure messages.

        Notes:
            Uses "xpath_march" to find the correct widget corresponding
            to the XML error XPath.
        """

        self.error_list_dialog.show()

        # Determine schema location.
        if self.metadata_root.schema == "bdp":
            xsl_fname = utils.get_resource_path(
                "FGDC/BDPfgdc-std-001-1998-annotated.xsd"
            )
        else:
            xsl_fname = utils.get_resource_path(
                "FGDC/fgdc-std-001-1998-annotated.xsd"
            )

        # Run validation.
        errors = fgdc_utils.validate_xml(self.metadata_root.to_xml(),
                                         xsl_fname)

        self.clear_validation()

        marked_errors = []

        # First pass: Expand complex widgets related to Eainfo errors.
        for error in errors:
            try:
                xpath, error_msg, line_num = error
                if "attr" in xpath:
                    # Logic to find and expand attribute sections.
                    try:
                        detailed_index = xpath.split("/detailed[")[1].split(
                            "/")[0][:-1]
                        detailed_index = int(detailed_index) - 1
                    except IndexError:
                        detailed_index = 0

                    try:
                        attr_index = xpath.split("/attr[")[1].split("/")[0][:-1]
                        attr_index = int(attr_index) - 1
                    except IndexError:
                        attr_index = 0

                    # Expand the attribute widget.
                    self.metadata_root.eainfo.detaileds[
                        detailed_index
                    ].attributes.attrs[attr_index].regular_me()
                    self.metadata_root.eainfo.detaileds[
                        detailed_index
                    ].attributes.attrs[attr_index].supersize_me()
            except:
                pass

        # Rebuild widget lookup tree after expansions.
        widget_lookup = self.metadata_root.make_tree(widget=self.metadata_root)
        self.metadata_root.add_children(
            self.metadata_root.spatial_tab, widget_lookup.metadata.idinfo
        )
        self.metadata_root.add_children(
            self.metadata_root.dataqual.sourceinput,
            widget_lookup.metadata.dataqual.lineage,
        )

        # Second pass: Highlight widgets and populate error list.
        error_count = 0
        for error in errors:

            try:
                xpath, error_msg, line_num = error
                if xpath not in marked_errors:
                    self.error_list.add_error(error_msg, xpath)
                    marked_errors.append(xpath)

                    # Get widget(s) corresponding to XPath.
                    widgets = widget_lookup.xpath_march(xpath, as_list=True)
                    for widget in widgets:
                        if isinstance(widget, list):
                            for w in widget:
                                print("problem highlighting error", xpath,
                                      widget)
                        else:
                            self.highlight_error(widget.widget, error_msg)
                            self.error_widgets.append(widget.widget)
                            error_count += 1
            except BaseException as e:
                # Catch exceptions during highlighting/lookup.
                msg = "Error encountered highlighting error:\t" + xpath
                msg += "\n\n" + traceback.format_exc()
                QMessageBox.warning(self, "Bug encountered", msg)

        widget_lookup = self.metadata_root.make_tree(widget=self.metadata_root)

        # Display results message.
        if errors:
            msg = "There are {} errors in this record".format(error_count)
            self.statusBar().showMessage(msg, 20000)
            msg = (
                "\n\n These errors are highlighted in red in the form below."
                "\n\n These errors are also listed in the Validation Errors "
                "Form that just popped up."
                "\n Clicking each error will take you to the section it is "
                "contained in."
                "\n Note that some highlighed errors can be in collapsed "
                "items, scrolled out of view, or in non-selected tabs."
            )
            QMessageBox.warning(self, "Validation", msg)
            self.error_list_dialog.show()
        else:
            msg = "Congratulations there were No FGDC Errors!"
            self.statusBar().showMessage(msg, 20000)
            QMessageBox.information(self, "Validation", msg)

    def goto_error(self, sender):
        """
        Description:
            Highlights the selected error in the form and switches to the
            containing tab/section.

        Passed arguments:
            sender (QWidget): The list item (QAction/QListWidgetItem)
                from the error list that was clicked.

        Returned objects:
            None

        Workflow:
            1. Extracts XPath from the sender data.
            2. Determines which main tab to switch to.
            3. Finds the target widget using the XPath.
            4. Ensures the target widget is visible in its scroll area.
            5. Calls "highlight_error" with "superhot=True" for extra focus.

        Notes:
            None
        """

        try:
            xpath = sender.data(1)
            section = xpath.split("/")[1]

            # Determine and switch to the correct main tab.
            if section == "idinfo":
                subsection = xpath.split("/")[2]
                if subsection == "spdom":
                    parent_section = self.metadata_root.switch_section(2)
                else:
                    parent_section = self.metadata_root.switch_section(0)
            elif section == "dataqual":
                parent_section = self.metadata_root.switch_section(1)
            elif section == "spdoinfo" or section == "spref":
                parent_section = self.metadata_root.switch_section(2)
            elif section == "eainfo":
                parent_section = self.metadata_root.switch_section(3)
            elif section == "eainfo":
                parent_section = self.metadata_root.switch_section(3)
            elif section == "distinfo":
                parent_section = self.metadata_root.switch_section(4)
            elif section == "metainfo":
                parent_section = self.metadata_root.switch_section(5)

                # Clear previous super-highlight.
                if (self.last_highlight is not None
                        and not sip.isdeleted(self.last_highlight)
                ):
                    self.highlight_error(
                        self.last_highlight, self.last_highlight.toolTip()
                    )

            # Find the widget corresponding to the error.
            widget_lookup = self.metadata_root.make_tree(
                widget=self.metadata_root
            )
            bad_widget = widget_lookup.xpath_march(xpath, as_list=True)

            try:
                # Scroll to make the widget visible.
                parent_wizwidget = [
                    thing
                    for thing in parent_section.children()
                    if isinstance(thing, WizardWidget)
                ][0]
                parent_wizwidget.scroll_area.ensureWidgetVisible(
                    bad_widget[0].widget)
            except:
                pass

            # Apply super-highlight and store reference.
            self.last_highlight = bad_widget[0].widget
            self.highlight_error(bad_widget[0].widget, sender.text(),
                                 superhot=True)
        except:
            # Handle failure to navigate/highlight.
            msg = (
                f"We encountered a problem highlighting and navigating "
                f"to that error.\n\nThe xpath of the xml error is:\n\n"
                f"{xpath}"
            )
            QMessageBox.warning(self, "Problem encountered", msg)

    def highlight_error(self, widget, error_msg, superhot=False):
        """
        Description:
            Highlights the given widget and sets its tooltip message to
            the error message.

        Passed arguments:
            widget (QWidget): The widget to highlight.
            error_msg (str): The message that will appear in the tooltip.
            superhot (bool): If True, applies a thicker black outline for
                extra focus (used when navigating from the error list).

        Returned objects:
            None

        Workflow:
            1. Calls specific helper methods ("highlight_attr",
               "highlight_tab") for complex nested widgets.
            2. Constructs a dynamic QSS (Qt Style Sheet) to apply a red
               background/border, custom tooltip style, and handles
               "superhot" styling.
            3. Sets the tooltip and applies the stylesheet.

        Notes:
            None
        """

        # Handle highlighting for widgets nested in collapsed attribute frames.
        if widget.objectName() in [
            "fgdc_attr",
            "fgdc_edomv",
            "fgdc_edomvd",
            "fgdc_edomvds",
            "fgdc_attrlabl",
            "fgdc_attrdef",
            "fgdc_attrdefs",
            "fgdc_codesetd",
            "fgdc_edom",
            "fgdc_rdom",
            "fgdc_udom",
            "fgdc_rdommin",
            "fgdc_rdommax",
            "fgdc_codesetn",
            "fgdc_codesets",
            "fgdc_attrdomv",
        ]:
            self.highlight_attr(widget)

        # Handle highlighting for widgets nested in tabs (e.g., Lineage).
        if widget.objectName() in [
            "fgdc_themekey",
            "fgdc_themekt",
            "fgdc_placekey",
            "fgdc_placekt",
            "fgdc_procdesc",
            "fgdc_srcused",
            "fgdc_srcprod",
        ]:
            self.highlight_tab(widget)

        # Determine styling based on superhot status.
        color = "rgba(225, 67, 94, 0)"
        lw = ""
        if superhot:
            lw = "border: 3px solid black;"

        # Apply general widget styling.
        if widget.objectName() not in ["metadata_root", "fgdc_metadata"]:
            try:
                widget.setToolTip(error_msg)
                widget.setStyleSheet(
                    """
                QGroupBox#{widgetname}{{
                background-color: {color};
                border: 2px solid red;
                subcontrol-position: top left;
                padding-top: 20px;
                font: bold 14px;
                color: rgba(90, 90, 90, 0);
                }}
                QGroupBox#{widgetname}::title {{
                text-align: left;
                subcontrol-origin: padding;
                subcontrol-position: top left;
                padding: 3 3px;
                }}
                QLabel{{
                font: 9pt "Arial";
                color: rgba(90, 90, 90, 0);
                }}
                QLineEdit#{widgetname}, QPlainTextEdit#{widgetname}, QComboBox#{widgetname} {{
                font: 9pt "Arial";
                color: rgba(50, 50, 50, 0);
                background-color: {color};
                opacity: 25;
                {lw}
                }}
                QToolTip {{
                background-color: rgba(255, 76, 77, 0);
                border-color: red;
                opacity: 255;
                }}
                """.format(
                        widgetname=widget.objectName(), color=color, lw=lw
                    )
                )
            except:
                pass

    def highlight_attr(self, widget):
        """
        Description:
            Highlights the parent "fgdc_attr" frame when an error is
            found in one of its child widgets.

        Passed arguments:
            widget (QWidget): The inner child widget with the error.

        Returned objects:
            None

        Workflow:
            Traverses up the widget hierarchy until the "fgdc_attr"
            frame is found, then applies a red border to that frame.

        Notes:
            None
        """

        widget_parent = widget
        attr_frame = widget

        # Traverse up to find the "fgdc_attr" frame.
        while not widget_parent.objectName() == "fgdc_attr":
            widget_parent = widget_parent.parent()
            attr_frame = widget_parent

        # Add the parent frame to error list and apply style.
        self.error_widgets.append(attr_frame)
        widget_parent = widget_parent.parent()

        widget_parent.supersize_me()
        error_msg = "'Validation error in hidden contents, click to show'"
        widget_parent.setToolTip(error_msg)
        widget_parent.setStyleSheet(
            """
    QFrame#{widgetname}{{
    border: 2px solid red;
    }}
        """.format(
                widgetname=attr_frame.objectName()
            )
        )

        self.error_widgets.append(widget_parent)

    def highlight_tab(self, widget):
        """
        Description:
            Highlights the parent "QTabWidget"'s tab bar when an error is
            found in a widget contained within one of its hidden tabs.

        Passed arguments:
            widget (QWidget): The inner child widget with the error.

        Returned objects:
            None

        Workflow:
            Traverses up the widget hierarchy until a `QTabWidget` is
            found, then applies a red background to its tab bar.

        Notes:
            None
        """

        widget_parent = widget.parent()

        # Traverse up to find the QTabWidget.
        while not type(widget_parent) == QTabWidget:
            widget_parent = widget_parent.parent()

        # Apply style to the QTabBar.
        error_msg = "'Validation error in hidden contents, click to show'"
        widget_parent.setToolTip(error_msg)
        widget_parent.setStyleSheet(
            """
    QTabBar {{
    background-color: rgba(225, 67, 94, 0);
    qproperty-drawBase:0;

}}
        """
        )

        self.error_widgets.append(widget_parent)

    def spelling_switch_triggered(self, e):
        """
        Description:
            Toggles the spelling/autocomplete feature state.

        Passed arguments:
            e: The event trigger (unused).

        Returned objects:
            None

        Workflow:
            Determines the new state and calls "switch_spelling".

        Notes:
            None
        """

        spelling_action_text = self.ui.actionSpelling_flag.text()

        # Determine the new desired state.
        use_spelling = spelling_action_text == "Turn Spelling OFF"
        self.switch_spelling(not use_spelling)

    def switch_spelling(self, use_spelling):
        """
        Description:
            Updates the GUI flag and recursively enables or disables
            spelling highlighting across all widgets.

        Passed arguments:
            use_spelling (bool): True to enable highlighting, False to
                disable.

        Returned objects:
            None

        Workflow:
            1. Updates the menu action label.
            2. Recursively calls "recursive_spell" on the root widget.
            3. Saves the state to application settings.

        Notes:
            None
        """

        # Update the action's label text.
        if use_spelling:
            self.ui.actionSpelling_flag.setText("Turn Spelling OFF")
        else:
            self.ui.actionSpelling_flag.setText("Turn Spelling ON")

        # Recursively apply the spelling state change.
        self.recursive_spell(self.metadata_root, use_spelling)

        # Save the preference to QSettings.
        self.settings.setValue("use_spelling", use_spelling)

    def recursive_spell(self, widget, which):
        """
        Description:
            Turns the spelling highlighter on or off for a given widget
            and iterates through its children recursively.

        Passed arguments:
            widget (QWidget): The widget to update.
            which (bool): Flag to turn spelling on (True) or off (False).

        Returned objects:
            None

        Workflow:
            1. Attempts to enable/disable the widget's highlighter and
               re-highlight.
            2. Recurses into child widgets.

        Notes:
            Uses try/except to handle widgets that do not possess a
            "highlighter" attribute.
        """

        try:
            # Set enabled state and force re-highlighting.
            widget.highlighter.enabled = which
            widget.highlighter.rehighlight()
        except:
            # Fail silently if widget has no highlighter.
            pass

        # Recursively call this function on all child widgets.
        for child_widget in self.metadata_root.get_children(widget):
            self.recursive_spell(child_widget, which)

    def dragEnterEvent(self, e):
        """
        Description:
            Accepts the drag event if the MIME data contains URLs.

        Passed arguments:
            e (QDragEnterEvent): The drag event object.

        Returned objects:
            None

        Workflow:
            Accepts if "e.mimeData().hasUrls()" is true, otherwise ignores.

        Notes:
            Part of Qt's drag-and-drop mechanism.
        """

        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """
        Description:
            Accepts the move event if the URL refers to a local file.

        Passed arguments:
            e (QDragMoveEvent): The drag move event object.

        Returned objects:
            None

        Workflow:
            Accepts if the dragged item is a URL that points to a local
            file.

        Notes:
            Part of Qt's drag-and-drop mechanism.
        """

        if e.mimeData().hasUrls() and e.mimeData().urls()[0].isLocalFile():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Description:
            Handles the dropping of files onto the main widget by loading
            the dropped file.

        Passed arguments:
            e (QDropEvent): The drop event object.

        Returned objects:
            None

        Workflow:
            1. Checks for URLs in MIME data and sets copy action.
            2. Extracts the local file path from the URL.
            3. If the path is a file, calls "open_file".
            4. Accepts the event if successful, otherwise ignores.

        Notes:
            This is a convenience function that fails silently on error.
        """

        try:
            if e.mimeData().hasUrls():
                e.setDropAction(Qt.CopyAction)

                url = e.mimeData().urls()[0]
                fname = url.toLocalFile()

                # Check if the path points to an actual file.
                if os.path.isfile(fname):
                    self.open_file(fname)
                e.accept()
            else:
                e.ignore()
        except:
            # If anything goes wrong at all, pass silently.
            pass

    def preview(self):
        """
        Description:
            Shows a preview window with the XML content rendered using
            the FGDC XSLT stylesheet.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Loads the XSLT file.
            2. Transforms the current XML record.
            3. Writes the resulting HTML to a temporary file.
            4. Launches a "Preview" dialog using the temporary HTML file.

        Notes:
            The temporary file is used as the URL source for the preview.
        """

        # Load the FGDC XSLT stylesheet.
        xsl_fname = utils.get_resource_path("FGDC/FGDC_Stylesheet.xsl")
        transform = xml_utils.load_xslt(xsl_fname)

        # Apply the transformation to the current XML tree.
        result = transform(self.metadata_root.to_xml())

        # Create a temporary file to hold the HTML result.
        tmp = tempfile.NamedTemporaryFile(suffix=".html")
        tmp.close()
        result.write(tmp.name)

        # Initialize and show the preview dialog.
        self.preview = Preview(url=tmp.name)

        self.preview_dialog = QDialog(self)
        self.preview_dialog.setWindowTitle("Metadata Preview")
        self.preview_dialog.setLayout(self.preview.layout())

        self.preview_dialog.resize(600, 600)

        # Launch the modal dialog.
        self.preview_dialog.exec_()

    def launch_help(self):
        """
        Description:
            Opens the application's documentation/help page in a preview
            dialog.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Locates the path to the main HTML help file (index.html).
            2. Initializes and shows a "Preview" dialog using that path.

        Notes:
            Checks multiple paths to account for different installation
            methods (e.g., source vs. packaged).
        """

        # Determine the root directory of the installation.
        root_dname = utils.get_install_dname("pymdwizard")

        # Construct the expected path to the help index.
        help_html = os.path.join(
            root_dname, "docs", "html_output", "index.html"
        )

        # Fallback path check for source installations.
        if not os.path.exists(help_html):
            gui_fname = os.path.dirname(os.path.realpath(__file__))
            help_html = os.path.join(
                gui_fname, "..", "..", "docs", "html_output", "index.html"
            )

        # Initialize and show the help dialog.
        self.preview = Preview(url=help_html)

        self.preview_dialog = QDialog(self)
        self.preview_dialog.setWindowTitle("MetadataWizard Help")
        self.preview_dialog.setLayout(self.preview.layout())

        self.preview_dialog.resize(1000, 600)

        self.preview_dialog.exec_()

    def generate_review_doc(self):
        """
        Description:
            Generates a Microsoft Word (.docx) review document from the
            current metadata record.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Checks for unsaved changes and prompts the user to save.
            2. Determines the output filename (e.g., "_REVIEW.docx").
            3. Prompts for overwrite if the review document exists.
            4. Calls "review_utils.generate_review_report".
            5. Launches the generated DOCX file using the OS default
               application.
            6. Displays a confirmation message.

        Notes:
            None
        """

        if self.cur_fname:
            # Determine output filename.
            out_fname = self.cur_fname[:-4] + "_REVIEW.docx"

            # Determine the schema type for the utility.
            if self.metadata_root.schema == "bdp":
                which = "bdp"
            else:
                which = "fgdc"

            # Check for unsaved changes (debounced by last_updated check).
            if time.time() - self.last_updated > 4:
                msg = (
                    "Would you like to save the current file "
                    "before continuing?"
                )
                exists_msg = (
                    "File already exists, would you like to "
                    "overwrite it? Selecting 'No' will allow you to "
                    "SaveAs."
                )

                self.last_updated = time.time()
                confirm = QMessageBox.question(
                    self,
                    "File save",
                    msg,
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                )
                if confirm == QMessageBox.Yes:
                    self.save_as()

                elif confirm == QMessageBox.Cancel:
                    return
            try:
                # Load the current XML record.
                cur_content = xml_utils.XMLRecord(self.cur_fname)

                # Check if review document already exists.
                if os.path.exists(out_fname):
                    confirm2 = QMessageBox.question(self,
                        "File Overwrite",
                        exists_msg,
                        QMessageBox.Yes | QMessageBox.No |
                                                    QMessageBox.Cancel ,
                    )
                    if confirm2 == QMessageBox.Yes:
                        self.save_file()
                    elif confirm2 == QMessageBox.No:
                        out_fname = QFileDialog.getSaveFileName(
                            self, "Save As", out_fname,
                            filter="Document (*.docx)"
                        )[0]
                    elif confirm2 == QMessageBox.Cancel:
                        return

                # Generate the review report.
                review_utils.generate_review_report(cur_content, out_fname,
                                                    which=which)

                def open_file(filename):
                    """Helper function to open file using OS defaults."""
                    if sys.platform == "win32":
                        os.startfile('"{}"'.format(filename))
                    elif sys.platform == "darwin":  # macOS
                        opener = "open"
                        subprocess.call([opener, filename])
                    else:  # Linux/others
                        opener = "xdg-open"
                        subprocess.call([opener, filename])

                # Open the generated file.
                open_file(out_fname)

                # Display confirmation message
                msg = "Review document available at: {}".format(out_fname)
                msg += (
                    "\n\nReview document now opening in default "
                    "application..."
                )
                QMessageBox.information(self, "Review finished", msg)
            except BaseException:
                # Handle any errors during generation
                msg = "Problem encountered generating review document:\n"
                msg += "{}".format(traceback.format_exc())
                QMessageBox.warning(self, "Problem encountered", msg)

    def launch_jupyter(self):
        """
        Description:
            Launches the Jupyter Notebook starter dialog, allowing the
            user to select a directory to run a server from.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Loads recent Jupyter directories from settings, defaulting
               to the application's "examples" folder.
            2. Initializes and shows the "JupyterStarter" dialog.

        Notes:
            The "update_jupyter_dnames" method is used as a callback to
            save the last used directory.
        """

        # Load recent Jupyter directories from settings.
        jupyter_dnames = self.settings.value("jupyter_dnames", [])


        if not jupyter_dnames:
            # Default to examples directory if none are saved.
            install_dir = utils.get_install_dname()
            jupyter_dnames = [os.path.join(install_dir, "examples")]
            self.settings.setValue("jupyter_dnames", jupyter_dnames)

        # Initialize and show the starter dialog.
        self.jupyter_dialog = JupyterStarter(
            previous_dnames=jupyter_dnames,
            update_function=self.update_jupyter_dnames
        )
        utils.set_window_icon(self.jupyter_dialog)
        self.jupyter_dialog.show()

    def update_jupyter_dnames(self, dname):
        """
        Description:
            Updates the list of recently used Jupyter directories stored
            in application settings.

        Passed arguments:
            dname (str): The new directory name to add to the list.

        Returned objects:
            None

        Workflow:
            1. Retrieves the current list from settings.
            2. Removes duplicates and inserts the new directory at the
               front.
            3. Truncates the list and saves it back to settings.

        Notes:
            None
        """

        jupyter_dnames = self.settings.value("jupyter_dnames", [])

        # Remove the directory if it already exists in the list.
        try:
            jupyter_dnames.remove(dname)
        except ValueError:
            my_env = os.environ.copy()
            pass

        # Insert new directory at the front.
        jupyter_dnames.insert(0, dname)

        # Truncate the list to max allowed size.
        del jupyter_dnames[PyMdWizardMainForm.max_recent_files :]

        # Save the updated list.
        self.settings.setValue("jupyter_dnames", jupyter_dnames)

    def about(self):
        """
        Description:
            Displays an 'about' message box with contact information,
            current version number, and project page links.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Constructs the HTML message content and displays it in a
            "QMessageBox".

        Notes:
            None
        """

        msg = (
            "The MetadataWizard was developed by the data management "
            "team <br> at the USGS Fort Collins Science Center,<br>"
            "with support from the USGS Science Analytics and Synthesis "
            "(SAS), "
            "and the USGS Community for Data Integration (CDI).<br><br>"
            "Ongoing support provided by the USGS Science Analytics "
            "and Synthesis (SAS)<br>"
            f"<br><br>Version: {__version__}<br>"
            "<br> Project page: <a href='https://github.com/DOI-USGS/"
            "fort-pymdwizard'>https://github.com/DOI-USGS/"
            "fort-pymdwizard</a>"
            "<br><br>Contact: Tamar Norkin at ask-sdm@usgs.gov"
        )

        msgbox = QMessageBox.about(self, "About", msg)

    def check_for_updates(self, e=None, show_uptodate_msg=True):
        """
        Description:
            Checks if the local installation's commit is behind the
            master branch of the USGS GitHub repository.

        Passed arguments:
            e (QEvent, optional): Qt event (unused).
            show_uptodate_msg (bool): Whether to display a message if
                no updates are found.

        Returned objects:
            None

        Workflow:
            1. Uses the "git.Repo" library to fetch the remote status.
            2. Compares the local HEAD commit to the remote master commit.
            3. If an update is available, prompts the user to install.

        Notes:
            None
        """

        try:
            install_dir = utils.get_install_dname("pymdwizard")
            repo = Repo(install_dir)

            # Fetch remote changes.
            fetch = [r for r in repo.remotes if r.name == "origin"][0].fetch()
            master = [f for f in fetch if f.name == "origin/master"][0]

            if repo.head.commit != master.commit:
                msg = (
                    "An update(s) are available for the Metadata Wizard.\n"
                    "Would you like to install these now?"
                )

                confirm = QMessageBox.question(
                    self,
                    "Updates Available",
                    msg,
                    QMessageBox.Yes | QMessageBox.No,
                )

                if confirm == QMessageBox.Yes:
                    self.update_from_github()
            elif show_uptodate_msg:
                # Display message if up to date.
                msg = "MetadataWizard already up to date."
                QMessageBox.information(self, "No Update Needed", msg)

        except BaseException as e:
            if show_uptodate_msg:
                msg = (
                    "Problem Encountered Updating from USGS GitHub "
                    "(https://github.com/DOI-USGS/fort-pymdwizard)\n\n"
                    "Please ensure that you have write access to the "
                    "location where the Metadata Wizard is installed."
                )
                QMessageBox.information(self, "Update results", msg)

    def update_from_github(self):
        """
        Description:
            Merges the latest version of the application from the GitHub
            repository into the local repository.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Uses "git.Repo" to fetch the remote master.
            2. Executes a "git merge" command.
            3. Displays success or failure messages.

        Notes:
            Requires restart after successful update.
        """

        try:
            install_dir = utils.get_install_dname("pymdwizard")
            repo = Repo(install_dir)

            # Fetch and identify remote master.
            fetch = [r for r in repo.remotes if r.name == "origin"][0].fetch()
            master = [f for f in fetch if f.name == "origin/master"][0]

            # Execute git merge
            repo.git.merge(master.name)

            # Success message
            msg = (
                "Updated Successfully from GitHub. Close and re-open "
                "Metadata Wizard for changes to be implemented."
            )
            QMessageBox.information(self, "Update results", msg)
        except BaseException as e:
            # Failure message
            msg = (
                "Problem Encountered Updating from GitHub\n\n"
                "USGS users, if you experience issues, please try "
                "disconnecting/reconnecting to the internal USGS network "
                "and re-checking for updates."
            )
            QMessageBox.information(self, "Update results", msg)

        QApplication.restoreOverrideCursor()


def show_splash(version="2.x.x"):
    """
    Description:
        Displays the application's splash screen with the version number
        rendered over the image.

    Passed arguments:
        version (str): Version number as a string (e.g., "2.1.1").

    Returned objects:
        splash (QSplashScreen): The created splash screen object.

    Workflow:
        1. Loads the splash image.
        2. Loads individual image files for version digits ("0", "1", ...).
        3. Uses a `QPainter` to draw the version digits onto the splash image.
        4. Initializes and shows the `QSplashScreen`.

    Notes:
        Requires version digits to be available as image files.
    """

    # Load and scale the base splash image.
    splash_fname = utils.get_resource_path("icons/splash.jpg")
    splash_pix = QPixmap(splash_fname)

    size = splash_pix.size() * 0.35
    splash_pix = splash_pix.scaled(
        size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
    )

    # Load and scale individual version digits.
    numbers = {}
    for number in list(range(10)) + ["point", "x"]:
        fname = utils.get_resource_path("icons/{}.png".format(number))
        pix = QPixmap(fname)
        size = pix.size() * 0.65
        numbers[str(number)] = pix.scaled(
            size, Qt.KeepAspectRatio,
            transformMode=Qt.SmoothTransformation
        )
    numbers["."] = numbers["point"]

    # Use QPainter to draw the version number.
    painter = QPainter(splash_pix)
    painter.begin(splash_pix)

    x, y = 470, 70
    for digit in version:
        painter.drawPixmap(int(x), y, numbers[digit])
        x += numbers[digit].rect().width() / 3

    painter.end()

    # Create and show the splash screen.
    splash = QSplashScreen(splash_pix, Qt.Window)
    splash.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
    splash.show()  # Show the splash screen
    splash.raise_()

    return splash


def launch_main(xml_fname=None, introspect_fname=None, env_cache={}):
    """
    Description:
        The main function to initialize and run the PyQt application.

    Passed arguments:
        xml_fname (str, optional): An XML file path to open on startup.
        introspect_fname (str, optional): A file path to use for initial
            Entity and Attribute population.
        env_cache (dict): Dictionary of cached environment variables.

    Returned objects:
        None

    Workflow:
        1. Creates the "QApplication" instance.
        2. Displays the splash screen and waits.
        3. Initializes and shows the main form ("PyMdWizardMainForm").
        4. Calls "check_for_updates".
        5. If provided, opens a starting XML file or populates attributes
           from an introspection file.
        6. Starts the Qt event loop (app.exec_()).

    Notes:
        The splash screen provides visual feedback during startup.
    """

    app = QApplication(sys.argv)

    # Show splash screen.
    splash = show_splash(__version__)

    # Process events and wait to allow splash screen to display.
    app.processEvents()

    # Initialize and show the main window.
    mdwiz = PyMdWizardMainForm()
    mdwiz.show()
    mdwiz.env_cache = env_cache
    splash.finish(mdwiz)
    app.processEvents()

    # Check for updates silently on startup.
    try:
        mdwiz.check_for_updates(show_uptodate_msg=False)
    except:
        pass

    # Open specified XML file if provided.
    if xml_fname is not None and os.path.exists(xml_fname):
        mdwiz.open_file(xml_fname)

    # Handle introspection file for Entity/Attribute information.
    if introspect_fname is not None and introspect_fname.endswith("$"):
        just_fname, _ = os.path.split(introspect_fname)
    else:
        just_fname = introspect_fname

    if introspect_fname is not None and os.path.exists(just_fname):
        # Populate Entity/Attribute (EAINFO) section.
        mdwiz.metadata_root.eainfo.detaileds[0].populate_from_fname(
            introspect_fname)

        # Switch to EAINFO tab.
        mdwiz.metadata_root.eainfo.ui.fgdc_eainfo.setCurrentIndex(1)

    # Start the application event loop.
    app.exec_()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    launch_main()
