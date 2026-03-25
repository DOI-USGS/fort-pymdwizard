
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
            template_fname = utils.get_resource_path("CSDGM_Template.xml")
        elif not os.path.exists(template_fname):
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

        self.load_file_content(template_fname)
        self.cur_fname = ""

        today = fgdc_utils.format_date(datetime.datetime.now())
        self.metadata_root.metainfo.metd.set_date(today)

    def set_current_file(self, fname):
        """
        The procedure for storing and displaying a new current file.
        """

        self.cur_fname = fname
        if fname:
            stripped_name = QFileInfo(fname).fileName()
            title = "Metadata Wizard - {}".format(stripped_name)
            self.setWindowTitle(title)

            files = self.settings.value("recentFileList", [])

            try:
                files.remove(fname)
            except ValueError:
                pass

            files.insert(0, fname)
            del files[PyMdWizardMainForm.max_recent_files:]

            self.settings.setValue("recentFileList", files)

            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, PyMdWizardMainForm):
                    widget.update_recent_file_actions()
        else:
            self.setWindowTitle("Metadata Wizard")

    def update_recent_file_actions(self):
        """
        Updates the actions in the recent files list to reflect the stored file paths.
        """

        files = self.settings.value("recentFileList", [])
        num_recent_files = min(len(files), PyMdWizardMainForm.max_recent_files)

        for i in range(num_recent_files):
            stripped_name = QFileInfo(files[i]).fileName()
            text = "&%d %s" % (i + 1, stripped_name)
            self.recent_file_actions[i].setText(text)
            self.recent_file_actions[i].setData(files[i])
            self.recent_file_actions[i].setVisible(True)

        for j in range(num_recent_files, PyMdWizardMainForm.max_recent_files):
            self.recent_file_actions[j].setVisible(False)

    def check_for_changes(self):
        """
        Checks if the current document has unsaved changes by comparing the form's XML to disk.
        """

        try:
            if self.cur_fname and os.path.exists(self.cur_fname):
                cur_xml = xml_utils.node_to_string(
                    self.metadata_root.to_xml()
                )
                disk_xml = xml_utils.node_to_string(
                    xml_utils.fname_to_node(self.cur_fname)
                )

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
                    xml_utils.save_to_file(
                        self.metadata_root.to_xml(), self.cur_fname
                    )
                elif confirm == QMessageBox.Cancel:
                    return "Cancel"
        except:
            pass

    def exit(self):
        """
        Checks for unsaved changes and prompts the user before closing the application.
        """

        changed = self.check_for_changes()
        if changed == "Cancel":
            return changed
        else:
            self.close()
            return "Close"

    def closeEvent(self, event):
        """
        Intercepts the built-in closeEvent to run the save-check before closing the window.
        """

        if self.exit() == "Close":
            self.settings.setValue("size", self.size())
            self.settings.setValue("pos", self.pos())
            event.accept()
        else:
            event.ignore()

    def use_dataqual(self, sender=None):
        """Toggles the visibility of the Data Quality tab."""
        self.metadata_root.use_section("dataqual", sender)

    def use_spatial(self, sender=None):
        """Toggles the visibility of the Spatial tab."""
        self.metadata_root.use_section("spatial", sender)

    def use_eainfo(self, sender=None):
        """Toggles the visibility of the Entity and Attribute tab."""
        self.metadata_root.use_section("eainfo", sender)

    def use_distinfo(self, sender=None):
        """Toggles the visibility of the Distribution tab."""
        self.metadata_root.use_section("distinfo", sender)

    def clear_validation(self):
        """
        Removes the error highlighting from all marked widgets and clears the error list.
        """

        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        for widget in self.error_widgets:
            if not qwidget_is_valid(widget):
                continue
            if widget.objectName() in ["metadata_root", "fgdc_metadata"]:
                continue
            try:
                widget.setStyleSheet("")  # clear highlight
                shortname = widget.objectName().replace("fgdc_", "")
                if shortname and shortname[-1].isdigit():
                    shortname = shortname[:-1]
                widget.setToolTip(annotation_lookup.get(shortname, {}).get("annotation", ""))
            except RuntimeError:
                pass
            except Exception:
                widget.setToolTip("")

        self.error_widgets = []
        self.error_list.clear_errors()
        self.error_list_dialog.hide()

    def validate(self):
        """
        Checks the current record against the FGDC schema using XSD validation and highlights errors.
        """

        self.error_list_dialog.show()

        if self.metadata_root.schema == "bdp":
            xsl_fname = utils.get_resource_path(
                "FGDC/BDPfgdc-std-001-1998-annotated.xsd"
            )
        else:
            xsl_fname = utils.get_resource_path(
                "FGDC/fgdc-std-001-1998-annotated.xsd"
            )

        errors = fgdc_utils.validate_xml(self.metadata_root.to_xml(),
                                         xsl_fname)

        self.clear_validation()
        marked_errors = []

        # First pass: Expand complex widgets related to Eainfo errors.
        for error in errors:
            try:
                xpath, error_msg, line_num = error
                if "attr" in xpath:
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

        error_count = 0
        for error in errors:
            try:
                xpath, error_msg, line_num = error
                if xpath not in marked_errors:
                    self.error_list.add_error(error_msg, xpath)
                    marked_errors.append(xpath)

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
            except BaseException:
                msg = "Error encountered highlighting error:\t" + xpath
                msg += "\n\n" + traceback.format_exc()
                QMessageBox.warning(self, "Bug encountered", msg)

        widget_lookup = self.metadata_root.make_tree(widget=self.metadata_root)

        if errors:
            msg = "There are {} errors in this record".format(error_count)
            self.statusBar().showMessage(msg, 20000)
            msg = (
                "\n\n These errors are highlighted in red in the form below."
                "\n\n These errors are also listed in the Validation Errors "
                "Form that just popped up."
                "\n Clicking each error will take you to the section it is "
                "contained in."
                "\n Note that some highlighted errors can be in collapsed "
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
        Highlights the selected error in the form and switches to the containing tab/section.
        """

        try:
            xpath = sender.data(1)
        except Exception:
            return

        try:
            section = xpath.split("/")[1]
        except Exception:
            section = ""

        if section == "idinfo":
            subsection = xpath.split("/")[2] if len(xpath.split("/")) > 2 else ""
            if subsection == "spdom":
                parent_section = self.metadata_root.switch_section(2)
            else:
                parent_section = self.metadata_root.switch_section(0)
        elif section == "dataqual":
            parent_section = self.metadata_root.switch_section(1)
        elif section in ("spdoinfo", "spref"):
            parent_section = self.metadata_root.switch_section(2)
        elif section == "eainfo":
            parent_section = self.metadata_root.switch_section(3)
        elif section == "distinfo":
            parent_section = self.metadata_root.switch_section(4)
        elif section == "metainfo":
            parent_section = self.metadata_root.switch_section(5)

            # Clear previous super-highlight safely.
            if self.last_highlight is not None and qwidget_is_valid(self.last_highlight):
                try:
                    self.highlight_error(self.last_highlight, self.last_highlight.toolTip())
                except RuntimeError:
                    pass

        widget_lookup = self.metadata_root.make_tree(
            widget=self.metadata_root
        )
        bad_widget = widget_lookup.xpath_march(xpath, as_list=True)

        try:
            parent_wizwidget = [
                thing
                for thing in parent_section.children()
                if isinstance(thing, WizardWidget)
            ][0]
            if bad_widget and qwidget_is_valid(bad_widget[0].widget):
                parent_wizwidget.scroll_area.ensureWidgetVisible(
                    bad_widget[0].widget)
        except:
            pass

        try:
            self.last_highlight = bad_widget[0].widget if bad_widget else None
            if qwidget_is_valid(self.last_highlight):
                self.highlight_error(self.last_highlight, sender.text(),
                                     superhot=True)
        except Exception:
            msg = (
                f"We encountered a problem highlighting and navigating "
                f"to that error.\n\nThe xpath of the xml error is:\n\n"
                f"{xpath}"
            )
            QMessageBox.warning(self, "Problem encountered", msg)

    def highlight_error(self, widget, error_msg, superhot=False):
        """
        Highlights the given widget and sets its tooltip message to the error message.
        """

        if not qwidget_is_valid(widget):
            return

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

        color = "rgb(225, 67, 94)"
        lw = "border: 3px solid black;" if superhot else "border: 2px solid red;"

        try:
            widget.setToolTip(f"<b>Validation error</b><br/>{error_msg}")
            if widget.objectName() not in ["metadata_root", "fgdc_metadata"]:
                widget.setStyleSheet(
                    f"""
                QWidget#{widget.objectName()} {{
                    background-color: {color};
                    {lw}
                }}
                """
                )

                # soften text fields if present
                line_edit = widget.findChild(QLineEdit)
                if line_edit:
                    apply_opacity_effect(line_edit, 0.95)

                self.error_widgets.append(widget)
        except RuntimeError:
            pass

    def highlight_attr(self, widget):
        """
        Highlights the parent 'fgdc_attr' frame when an error is found in one of its child widgets.
        """

        if not qwidget_is_valid(widget):
            return

        widget_parent = widget
        attr_frame = widget

        while True:
            if not qwidget_is_valid(widget_parent):
                return
            try:
                if widget_parent.objectName() == "fgdc_attr":
                    break
                widget_parent = widget_parent.parent()
                attr_frame = widget_parent
            except RuntimeError:
                return

        self.error_widgets.append(attr_frame)
        try:
            parent_of_attr = widget_parent.parent()
            if hasattr(parent_of_attr, "supersize_me"):
                parent_of_attr.supersize_me()

            error_msg = "Validation error in hidden contents, click to show"
            widget_parent.setToolTip(error_msg)
            widget_parent.setStyleSheet(
                f"""
    QFrame#{attr_frame.objectName()} {{
    border: 2px solid red;
    }}
                """
            )

            self.error_widgets.append(parent_of_attr)
        except RuntimeError:
            pass

    def highlight_tab(self, widget):
        """
        Highlights the parent QTabWidget's tab bar when an error is found within one of its hidden tabs.
        """

        if not qwidget_is_valid(widget):
            return

        try:
            widget_parent = widget.parent()
        except RuntimeError:
            return

        while True:
            if not qwidget_is_valid(widget_parent):
                return
            if isinstance(widget_parent, QTabWidget):
                break
            try:
                widget_parent = widget_parent.parent()
            except RuntimeError:
                return

        error_msg = "Validation error in hidden contents, click to show"
        try:
            widget_parent.setToolTip(error_msg)
            widget_parent.setStyleSheet(
                """
    QTabBar {
        background-color: rgb(225, 67, 94);
        qproperty-drawBase:0;
    }
                """
            )

            self.error_widgets.append(widget_parent)
        except RuntimeError:
            pass

    def spelling_switch_triggered(self, e):
        """
        Toggles the spelling/autocomplete feature state.
        """

        spelling_action_text = self.ui.actionSpelling_flag.text()
        use_spelling = spelling_action_text == "Turn Spelling OFF"
        self.switch_spelling(not use_spelling)

    def switch_spelling(self, use_spelling):
        """
        Updates the GUI flag and recursively enables or disables spelling highlighting.
        """

        if use_spelling:
            self.ui.actionSpelling_flag.setText("Turn Spelling OFF")
        else:
            self.ui.actionSpelling_flag.setText("Turn Spelling ON")

        self.recursive_spell(self.metadata_root, use_spelling)
        self.settings.setValue("use_spelling", use_spelling)

    def recursive_spell(self, widget, which):
        """
        Turns the spelling highlighter on or off for a given widget and iterates through its children.
        """

        try:
            widget.highlighter.enabled = which
            widget.highlighter.rehighlight()
        except:
            pass

        for child_widget in self.metadata_root.get_children(widget):
            self.recursive_spell(child_widget, which)

    def dragEnterEvent(self, e):
        """
        Accepts the drag event if the MIME data contains URLs.
        """

        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """
        Accepts the move event if the URL refers to a local file.
        """

        if e.mimeData().hasUrls() and e.mimeData().urls()[0].isLocalFile():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Handles the dropping of files onto the main widget by loading the dropped file.
        """

        try:
            if e.mimeData().hasUrls():
                e.setDropAction(Qt.CopyAction)

                url = e.mimeData().urls()[0]
                fname = url.toLocalFile()

                if os.path.isfile(fname):
                    self.open_file(fname)
                e.accept()
            else:
                e.ignore()
        except:
            pass

    def preview(self):
        """
        Shows a preview window with the XML content rendered using the FGDC XSLT stylesheet.
        """

        xsl_fname = utils.get_resource_path("FGDC/FGDC_Stylesheet.xsl")
        transform = xml_utils.load_xslt(xsl_fname)
        result = transform(self.metadata_root.to_xml())

        tmp = tempfile.NamedTemporaryFile(suffix=".html")
        tmp.close()
        result.write(tmp.name)

        self.preview = Preview(url=tmp.name)
        self.preview_dialog = QDialog(self)
        self.preview_dialog.setWindowTitle("Metadata Preview")
        self.preview_dialog.setLayout(self.preview.layout())

        self.preview_dialog.resize(600, 600)
        self.preview_dialog.exec_()

    def launch_help(self):
        """
        Opens the application's documentation/help page in a preview dialog.
        """

        root_dname = utils.get_install_dname("pymdwizard")
        help_html = os.path.join(
            root_dname, "docs", "html_output", "index.html"
        )

        if not os.path.exists(help_html):
            gui_fname = os.path.dirname(os.path.realpath(__file__))
            help_html = os.path.join(
                gui_fname, "..", "..", "docs", "html_output", "index.html"
            )

        self.preview = Preview(url=help_html)
        self.preview_dialog = QDialog(self)
        self.preview_dialog.setWindowTitle("MetadataWizard Help")
        self.preview_dialog.setLayout(self.preview.layout())
        self.preview_dialog.resize(1000, 600)
        self.preview_dialog.exec_()

    def generate_review_doc(self):
        """
        Generates a Microsoft Word (.docx) review document from the current metadata record.
        """

        if self.cur_fname:
            out_fname = self.cur_fname[:-4] + "_REVIEW.docx"
            which = "bdp" if self.metadata_root.schema == "bdp" else "fgdc"
            exists_msg = (
                "File already exists, would you like to overwrite it? "
                "Selecting 'No' will allow you to Save As."
            )

            if time.time() - self.last_updated >= 4:
                msg = (
                    "Would you like to save the current file "
                    "before continuing?"
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
                cur_content = xml_utils.XMLRecord(self.cur_fname)

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

                review_utils.generate_review_report(cur_content, out_fname,
                                                    which=which)

                def open_file(filename):
                    """Helper function to open file using OS defaults."""
                    if sys.platform == "win32":
                        os.startfile(filename)
                    elif sys.platform == "darwin":  # macOS
                        opener = "open"
                        subprocess.call([opener, filename])
                    else:  # Linux/others
                        opener = "xdg-open"
                        subprocess.call([opener, filename])

                open_file(out_fname)

                msg = "Review document available at: {}".format(out_fname)
                msg += (
                    "\n\nReview document now opening in default "
                    "application..."
                )
                QMessageBox.information(self, "Review finished", msg)
            except BaseException:
                msg = "Problem encountered generating review document:\n"
                msg += "{}".format(traceback.format_exc())
                QMessageBox.warning(self, "Problem encountered", msg)

    def launch_jupyter(self):
        """
        Launches the Jupyter Notebook starter dialog.
        """

        jupyter_dnames = self.settings.value("jupyter_dnames", [])

        if not jupyter_dnames:
            install_dir = utils.get_install_dname()
            jupyter_dnames = [os.path.join(install_dir, "examples")]
            self.settings.setValue("jupyter_dnames", jupyter_dnames)

        self.jupyter_dialog = JupyterStarter(
            previous_dnames=jupyter_dnames,
            update_function=self.update_jupyter_dnames
        )
        utils.set_window_icon(self.jupyter_dialog)
        self.jupyter_dialog.show()

    def update_jupyter_dnames(self, dname):
        """
        Updates the list of recently used Jupyter directories stored in application settings.
        """

        jupyter_dnames = self.settings.value("jupyter_dnames", [])

        try:
            jupyter_dnames.remove(dname)
        except ValueError:
            pass

        jupyter_dnames.insert(0, dname)
        del jupyter_dnames[PyMdWizardMainForm.max_recent_files:]

        self.settings.setValue("jupyter_dnames", jupyter_dnames)


    def about(self):
        """
        Displays an 'about' message box with contact information, version number, and project links.
        """

        msg = (
            "The Metadata Wizard was developed by the data management team at the USGS Fort Collins Science Center, with support from the USGS Science Analytics and Synthesis (SAS) program, and the USGS Community for Data Integration (CDI).<br><br>"
            "Ongoing support provided by the USGS Science Analytics and Synthesis (SAS)."
            f"<br><br><b>Version</b>: {__version__}<br>"
            "<br><b>Project page</b>: "
            "<a href='https://github.com/DOI-USGS/fort-pymdwizard'>https://github.com/DOI-USGS/fort-pymdwizard</a>"
            "<br><br><b>Contact</b>: Tamar Norkin at ask-sdm@usgs.gov"
        )

        # Use a configured QMessageBox to render rich text and enable clickable links
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle("About")
        msgbox.setTextFormat(Qt.RichText)  # Render HTML
        msgbox.setText(msg)
        msgbox.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Allow link interaction

        # Ensure links open externally in the default browser
        label = msgbox.findChild(QLabel, "qt_msgbox_label")
        if label is not None:
            label.setOpenExternalLinks(True)

        msgbox.exec_()


    def check_for_updates(self, e=None, show_uptodate_msg=True):
        """
        Checks if the local installation's commit is behind the master branch of the USGS GitHub repository.
        """

        spinner = SpinnerDialog(self)
        spinner.show()
        QApplication.processEvents()

        try:
            install_dir = utils.get_install_dname("pymdwizard")
            repo = Repo(install_dir)

            fetch = [r for r in repo.remotes if r.name == "origin"][0].fetch()
            master = [f for f in fetch if f.name == "origin/master"][0]

            spinner.close()

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
                msg = "MetadataWizard already up to date."
                QMessageBox.information(self, "No Update Needed", msg)

        except Exception as err:
            if spinner:
                spinner.close()

            if show_uptodate_msg:
                msg = (
                    "Problem Encountered Updating from USGS GitHub "
                    "(https://github.com/DOI-USGS/fort-pymdwizard)\n\n"
                    "Please ensure that you have write access to the "
                    "location where the Metadata Wizard is installed."
                    f"\n\nTechnical details:\n{err}"
                )
                QMessageBox.information(self, "Update results", msg)

    def update_from_github(self):
        """
        Merges the latest version of the application from the GitHub repository into the local repository.
        """

        try:
            install_dir = utils.get_install_dname("pymdwizard")
            repo = Repo(install_dir)

            fetch = [r for r in repo.remotes if r.name == "origin"][0].fetch()
            master = [f for f in fetch if f.name == "origin/master"][0]

            repo.git.merge(master.name)

            msg = (
                "Updated Successfully from GitHub. Close and re-open "
                "Metadata Wizard for changes to be implemented."
            )
            QMessageBox.information(self, "Update results", msg)
        except Exception as err:
            msg = (
                "Problem Encountered Updating from GitHub\n\n"
                "USGS users, if you experience issues, please try "
                "disconnecting/reconnecting to the internal USGS network "
                "and re-checking for updates."
                f"\n\nTechnical details:\n{err}"
            )
            QMessageBox.information(self, "Update results", msg)

        QApplication.restoreOverrideCursor()


def show_splash(version="2.x.x"):
    """
    Displays the application's splash screen with the version number rendered over the image.
    """

    splash_fname = utils.get_resource_path("icons/splash.jpg")
    splash_pix = QPixmap(splash_fname)

    size = splash_pix.size() * 0.3
    splash_pix = splash_pix.scaled(
        size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
    )

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

    painter = QPainter(splash_pix)
    painter.begin(splash_pix)

    x, y = 400, 65
    for digit in version:
        painter.drawPixmap(int(x), y, numbers[digit])
        x += numbers[digit].rect().width() / 3

    painter.end()
    del painter

    splash = QSplashScreen(splash_pix, Qt.Window)
    splash.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
    splash.show()
    splash.raise_()

    return splash


def launch_main(xml_fname=None, introspect_fname=None, env_cache=None):
    """
    The main function to initialize and run the PyQt application.
    """

    if env_cache is None:
        env_cache = {}

    app = QApplication(sys.argv)

    splash = show_splash(__version__)
    app.processEvents()

    mdwiz = PyMdWizardMainForm()
    mdwiz.show()
    mdwiz.env_cache = env_cache
    splash.finish(mdwiz)
    app.processEvents()
    del splash

    try:
        mdwiz.check_for_updates(show_uptodate_msg=False)
    except:
        pass

    if xml_fname is not None and os.path.exists(xml_fname):
        mdwiz.open_file(xml_fname)

    if introspect_fname is not None and introspect_fname.endswith("$"):
        just_fname, _ = os.path.split(introspect_fname)
    else:
        just_fname = introspect_fname

    if introspect_fname is not None and os.path.exists(just_fname):
        mdwiz.metadata_root.eainfo.detaileds[0].populate_from_fname(
            introspect_fname)

        mdwiz.metadata_root.eainfo.ui.fgdc_eainfo.setCurrentIndex(1)

    app.exec_()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """
    launch_main()