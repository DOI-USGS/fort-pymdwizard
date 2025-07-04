#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/DOI-USGS/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/DOI-USGS/fort-pymdwizard/tree/master/examples
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

import sys
import os
import platform
import tempfile
import time
import datetime
import shutil
from pathlib import Path
import subprocess

from os.path import dirname

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QFileInfo
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap


try:
    import docx
except ImportError:
    docx = None

from pymdwizard.gui.ui_files import UI_MainWindow
from pymdwizard.gui.MetadataRoot import MetadataRoot
from pymdwizard.core import xml_utils
from pymdwizard.core import utils
from pymdwizard.core import fgdc_utils
from pymdwizard.core import review_utils
from pymdwizard.gui.Preview import Preview
from pymdwizard.gui.error_list import ErrorList
from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.jupyterstarter import JupyterStarter
from pymdwizard.gui.settings import Settings
from pymdwizard.gui.sb_locator import SBLocator
from pymdwizard import __version__

import sip


class PyMdWizardMainForm(QMainWindow):

    max_recent_files = 10

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()

        self.settings = QSettings("USGS_2.1.1", "pymdwizard_2.1.1")
        self.cur_fname = ""
        self.file_watcher = None

        # list of buttons for opening recently accessed files
        self.recent_file_actions = []
        # list of widgets that are currently styled as errors
        self.error_widgets = []
        # the last error widget that was highlighted
        self.last_highlight = None
        self.last_updated = None
        self.ui = None
        self.metadata_root = None
        self.build_ui()
        self.connect_events()
        self.env_cache = {}

        self.sb_file = False
        self.sb_locator = SBLocator(mainform=self)
        utils.set_window_icon(self.sb_locator)

        self.load_default()

        use_spelling = self.settings.value("use_spelling", "true")
        if isinstance(use_spelling, str):
            use_spelling = eval(use_spelling.capitalize())
        self.switch_spelling(use_spelling)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        utils.set_window_icon(self, remove_help=False)

        # Initial window size/pos last saved. Use default values for first time
        self.resize(self.settings.value("size", QSize(1300, 700)))
        self.move(self.settings.value("pos", QPoint(50, 50)))

        self.metadata_root = MetadataRoot()
        self.ui.centralwidget.layout().addWidget(self.metadata_root)

        for i in range(PyMdWizardMainForm.max_recent_files):
            self.recent_file_actions.append(
                QAction(self, visible=False, triggered=self.open_recent_file)
            )
            self.ui.menuRecent_Files.addAction(self.recent_file_actions[i])
        self.update_recent_file_actions()

        template_fname = self.settings.value("template_fname")

        if template_fname is not None:
            just_fname = os.path.split(template_fname)[-1]
            self.ui.actionCurrentTemplate.setText("Current: " + just_fname)

        if docx is None:
            self.ui.generate_review.setEnabled(False)

        self.setAcceptDrops(True)

        self.error_list = ErrorList(main_form=self)
        self.error_list_dialog = QDialog(self)
        self.error_list_dialog.setWindowTitle("FGDC Validation Errors")
        self.error_list_dialog.setLayout(self.error_list.layout())
        self.error_list_dialog.resize(600, 400)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_as.triggered.connect(self.save_as)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionRun_Validation.triggered.connect(self.validate)
        self.ui.actionClear_validation.triggered.connect(self.clear_validation)
        self.ui.actionPreview.triggered.connect(self.preview)
        self.ui.actionNew.triggered.connect(self.new_record)
        self.ui.actionSettings.triggered.connect(self.set_settings)
        self.ui.actionLaunch_Jupyter.triggered.connect(self.launch_jupyter)
        self.ui.generate_review.triggered.connect(self.generate_review_doc)
        self.ui.actionLaunch_Help.triggered.connect(self.launch_help)
        self.ui.actionCheck_for_Updates.triggered.connect(self.check_for_updates)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionData_Quality.triggered.connect(self.use_dataqual)
        self.ui.actionSpatial.triggered.connect(self.use_spatial)
        self.ui.actionEntity_and_Attribute.triggered.connect(self.use_eainfo)
        self.ui.actionDistribution.triggered.connect(self.use_distinfo)
        self.ui.actionSpelling_flag.triggered.connect(self.spelling_switch_triggered)
        # self.ui.anacondaprompt.triggered.connect(self.anacondaprompt)
        # self.ui.actionOpen_sb.triggered.connect(self.open_sb_file)

    def anacondaprompt(self):

        if os.name == "nt":
            root_dir = utils.get_install_dname("root")
            my_env = os.environ.copy()
            my_env["PYTHONPATH"] = os.path.join(root_dir, "pymdwizard")
            my_env["PATH"] = ";".join(
                [
                    os.path.join(root_dir, "pymdwizard", "Scripts", "conda_exes"),
                    my_env["PATH"],
                ]
            )

            pydir = utils.get_install_dname("python")
            my_env["PATH"] = ";".join(
                [os.path.join(pydir, "Scripts", "conda_exes"), my_env["PATH"]]
            )
            self.ui.actionOpen_sb.triggered.connect(self.open_sb_file)
            activatebat = os.path.join(pydir, "Scripts", "conda_exe", "activate.bat")

            msg = "This is experimental functionality used for opening an Anaconda command prompt set to"
            msg += "\nthe Python environment shipped with the MetadataWizard.\n\n"
            msg += "The base conda env in this prompt is the one to use, so do not use the activate command."
            msg += "\nUse: conda install ...package.. to install new packages into the MetadataWizard envronment."
            QMessageBox.information(self, "Conda instructions", msg)

            subprocess.Popen(
                ["start", "cmd", activatebat, pydir], env=my_env, cwd=pydir, shell=True
            )
        else:
            msg = "This experimental functionality not yet implemented for Mac or Linux builds"
            QMessageBox.warning(self, "Not implemented", msg)

    def open_recent_file(self):
        """
        handles the opening of a recent file selection
        Returns
        -------
        None
        """
        action = self.sender()
        if action:
            self.load_file(action.data())
            self.set_current_file(action.data())

    def get_xml_fname(self):
        """

        Returns
        -------
        str: path and filename of the selected file or
        empty string if none was selected
        """
        recent_files = self.settings.value("recentFileList", [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(
            self, fname, dname, filter="XML Files (*.xml)"
        )

        if fname[0]:
            return fname[0]
        else:
            return ""

    def open_file(self, fname=None):
        """
        Browse to a file and load it if it is acceptable

        Returns
        -------
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
        download a
        Parameters
        ----------
        hash : str
            Tag of item to be edited on SB

        Returns
        -------
        None
        """
        self.sb_locator.show()

    def load_file(self, fname, check_for_changes=True):
        """
        load a file's content into the application.

        Parameters
        ----------
        fname : str
                full file path and name of the file to load
        check_for_changes : bool
                flag to check for save prompt if file has unsaved changes
        Returns
        -------
        None
        """

        if check_for_changes:
            changed = self.check_for_changes()
            if changed == "Cancel":
                return changed

        self.file_watcher = QFileSystemWatcher([fname])
        self.file_watcher.fileChanged.connect(self.file_updated)
        self.last_updated = time.time()

        self.clear_validation()

        # check that we have read write access to the file
        file = QFile(fname)
        if not file.open(QFile.ReadOnly | QFile.Text):
            msg = "Cannot read file %s:\n%s." % (fname, file.errorString())
            QMessageBox.warning(self, "Recent Files", msg)
            return
        file.close()

        self.load_file_content(fname)

    def load_file_content(self, fname):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()
        self.metadata_root.clear_widget()
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
        except BaseException as e:
            import traceback

            msg = "Cannot open file %s:\n%s." % (fname, traceback.format_exc())
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Recent Files", msg)
        QApplication.restoreOverrideCursor()

    def file_updated(self):
        """
        The function that fires when the file watcher detects that the
        current file has changed on the file system.  Prompts the user and
        loads the new file if they choose to.

        Returns
        -------
        None
        """
        if time.time() - self.last_updated > 4:
            msg = (
                "The file you are editing has been changed on disk.  "
                "Would you like to reload this File?"
            )
            alert = QDialog()
            self.last_updated = time.time()
            confirm = QMessageBox.question(
                self, "File Changed", msg, QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.load_file(self.cur_fname)

    def save_as(self):
        """
        Navigate to a new or existing file and save the current document
        into this file.

        Returns
        -------
        None
        """
        fname = self.get_save_name()
        if fname:
            self.set_current_file(fname)
            self.update_recent_file_actions()
            self.save_file()

    def get_save_name(self):
        """
        launches a saveas dialog to browse to a file to save to.
        starts in the directory of the most recently sopened file

        Returns
        -------
        str: file name and path
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
        Save the current xml document.  Prompts for a filename if one
        has not been set yet.

        Returns
        -------
        None
        """
        # Test
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
        comment = xml_utils.xml_node(tag="", text=tool_comment, index=0, comment=True)
        xml_contents.addprevious(comment)
        xml_utils.save_to_file(xml_contents, fname)
        self.last_updated = time.time()

        self.set_current_file(fname)
        self.statusBar().showMessage("File saved", 2000)

        # if self.sb_file:
        #     self.sb_locator.put_fgdc_file()

    def new_record(self):
        """
        Create a new record.
        Starts by making a copy of the template file 'CSDGM_Template.xml'.
            in the resources folder to a name selected in a save as dialog.
        Then updates the MD date to today.
        Returns
        -------
        None
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
            self.metadata_root.idinfo.citation.ui.pubdate_widget.set_date(this_year)

    def set_settings(self):
        self.settings_dialog = Settings(mainform=self)
        self.settings_dialog.setWindowTitle("MetadataWizard Settings")
        utils.set_window_icon(self.settings_dialog)
        self.settings_dialog.show()

    def load_default(self):
        template_fname = self.settings.value("template_fname")

        if template_fname is None:
            template_fname = utils.get_resource_path("CSDGM_Template.xml")
        elif not os.path.exists(template_fname):
            msg = (
                "The previous template file specified, {}, could not be "
                "found.".format(template_fname)
            )
            msg += "\nCheck that the file has not beed deleted, renamed " "or moved."
            msg += "Defaulting to the built in template.".format(template_fname)
            QMessageBox.warning(self, "Template file missing", msg)
            template_fname = utils.get_resource_path("CSDGM_Template.xml")

        self.load_file_content(template_fname)
        self.cur_fname = ""

        today = fgdc_utils.format_date(datetime.datetime.now())
        self.metadata_root.metainfo.metd.set_date(today)

    def set_current_file(self, fname):
        """
        The procedure for storing and displaying a new current file
        The following get done:
        1 - Display the file name without path in the apps title bar
        2 - Insert the file name into the top slot of the recent files
        3 - Save this list out to the setting variable

        Parameters
        ----------
        fname : str
            The file name and path that will be used

        Returns
        -------
        None
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
            del files[PyMdWizardMainForm.max_recent_files :]

            self.settings.setValue("recentFileList", files)

            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, PyMdWizardMainForm):
                    widget.update_recent_file_actions()
        else:
            self.setWindowTitle("Metadata Wizard")

    def update_recent_file_actions(self):
        """
        Update the actions (menu items) in the recent files list to
        reflect the recent file paths stored in the 'recentFileList' setting

        Returns
        -------
        None
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
        try:
            if self.cur_fname and os.path.exists(self.cur_fname):
                cur_xml = xml_utils.node_to_string(self.metadata_root.to_xml())
                disk_xml = xml_utils.node_to_string(
                    xml_utils.fname_to_node(self.cur_fname)
                )

            if cur_xml != disk_xml:
                msg = "Do you want to save your changes?"
                alert = QDialog()
                self.last_updated = time.time()
                confirm = QMessageBox.question(
                    self,
                    "Save Changes",
                    msg,
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                )
                if confirm == QMessageBox.Yes:
                    xml_utils.save_to_file(self.metadata_root.to_xml(), self.cur_fname)
                elif confirm == QMessageBox.Cancel:
                    return "Cancel"
        except:
            pass
        return None

    def exit(self):
        """
        Before exiting check if the current contents match what is on the
        file system.  If the do not match ask user if they would like to
        save or cancel the exit

        Returns
        -------
        str :
        'Close' or 'Cancel' depending on user choice.
        """
        changed = self.check_for_changes()
        if changed == "Cancel":
            return changed
        else:
            self.close()
            return "Close"

    def closeEvent(self, event):
        """ Intercept the builtin closeEvent so that we can check for
        changes and ask if we should change.

        Parameters
        ----------
        event

        Returns
        -------

        """
        if self.exit() == "Close":
            self.settings.setValue("size", self.size())
            self.settings.setValue("pos", self.pos())
            event.accept()
        else:
            event.ignore()

    def use_dataqual(self, sender=None):
        self.metadata_root.use_section("dataqual", sender)

    def use_spatial(self, sender=None):
        self.metadata_root.use_section("spatial", sender)

    def use_eainfo(self, sender=None):
        self.metadata_root.use_section("eainfo", sender)

    def use_distinfo(self, sender=None):
        self.metadata_root.use_section("distinfo", sender)

    def clear_validation(self):
        """
        Remove the error highlighting from all the error widgets

        Returns
        -------
        None
        """
        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        for widget in self.error_widgets:
            if not sip.isdeleted(widget) and widget.objectName() not in [
                "metadata_root",
                "fgdc_metadata",
            ]:
                widget.setStyleSheet("""""")
                print(widget.objectName())
                shortname = widget.objectName().replace("fgdc_", "")
                if shortname[-1].isdigit():
                    shortname = shortname[:-1]
                try:
                    widget.setToolTip(annotation_lookup[shortname]["annotation"])
                except KeyError:
                    widget.setToolTip("")

        self.error_widgets = []
        self.error_list.clear_errors()
        self.error_list_dialog.hide()

    def validate(self):
        """
        Check the current record against the schema and highlight any
        error widgets

        Returns
        -------
        None
        """

        self.error_list_dialog.show()
        if self.metadata_root.schema == "bdp":
            xsl_fname = utils.get_resource_path(
                "FGDC/BDPfgdc-std-001-1998-annotated.xsd"
            )
        else:
            xsl_fname = utils.get_resource_path("FGDC/fgdc-std-001-1998-annotated.xsd")
        from pymdwizard.core import fgdc_utils

        errors = fgdc_utils.validate_xml(self.metadata_root.to_xml(), xsl_fname)

        self.clear_validation()

        marked_errors = []

        # We need to expand / populate all attributes that have an error
        for error in errors:
            try:
                xpath, error_msg, line_num = error
                if "attr" in xpath:
                    try:
                        detailed_index = xpath.split("/detailed[")[1].split("/")[0][:-1]
                        detailed_index = int(detailed_index) - 1
                    except IndexError:
                        detailed_index = 0

                    try:
                        attr_index = xpath.split("/attr[")[1].split("/")[0][:-1]
                        attr_index = int(attr_index) - 1
                    except IndexError:
                        attr_index = 0

                    self.metadata_root.eainfo.detaileds[
                        detailed_index
                    ].attributes.attrs[attr_index].regular_me()
                    self.metadata_root.eainfo.detaileds[
                        detailed_index
                    ].attributes.attrs[attr_index].supersize_me()
            except:
                pass

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

                    # widget = self.metadata_root.get_widget(xpath)
                    widgets = widget_lookup.xpath_march(xpath, as_list=True)
                    for widget in widgets:
                        if isinstance(widget, list):
                            for w in widget:
                                print("problem highlighting error", xpath, widget)
                        else:
                            self.highlight_error(widget.widget, error_msg)
                            self.error_widgets.append(widget.widget)
                            error_count += 1
            except BaseException as e:
                import traceback

                msg = "Error encountered highlighting error:"
                msg += "\t" + xpath
                msg += "\n\n" + traceback.format_exc()
                QMessageBox.warning(self, "Bug encountered", msg)
        widget_lookup = self.metadata_root.make_tree(widget=self.metadata_root)
        if errors:
            msg = "There are {} errors in this record".format(error_count)
            self.statusBar().showMessage(msg, 20000)
            msg += "\n\n These errors are highlighted in red in the form below."
            msg += "\n\n These errors are also listed in the Validation Errors Form that just popped up."
            msg += "\n Clicking each error will take you to the section it is contained in."
            msg += "\n Note that some highlighed errors can be in collapsed items, scrolled out of view, or in non-selected tabs"
            QMessageBox.warning(self, "Validation", msg)
            self.error_list_dialog.show()
        else:
            msg = "Congratulations there were No FGDC Errors!"
            self.statusBar().showMessage(msg, 20000)
            QMessageBox.information(self, "Validation", msg)

    def goto_error(self, sender):
        """
        super highlight the selected error and switch the tab to the section
        that contains this error.

        Parameters
        ----------
        sender : QWidget

        Returns
        -------
        None
        """

        try:
            xpath = sender.data(1)
            section = xpath.split("/")[1]

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

            if self.last_highlight is not None and not sip.isdeleted(self.last_highlight):
                self.highlight_error(self.last_highlight, self.last_highlight.toolTip())

            widget_lookup = self.metadata_root.make_tree(widget=self.metadata_root)
            bad_widget = widget_lookup.xpath_march(xpath, as_list=True)

            try:
                parent_wizwidget = [
                    thing
                    for thing in parent_section.children()
                    if isinstance(thing, WizardWidget)
                ][0]
                parent_wizwidget.scroll_area.ensureWidgetVisible(bad_widget[0].widget)
            except:
                pass

            self.last_highlight = bad_widget[0].widget
            self.highlight_error(bad_widget[0].widget, sender.text(), superhot=True)
        except:
            msg = f"We encountered a problem highlighting and navigating to that error.\n\n"
            msg += f"The xpath of the xml error is:\n\n{xpath}"
            QMessageBox.warning(self, "Problem encountered", msg)

    def highlight_error(self, widget, error_msg, superhot=False):
        """
        Highlight the given widget and set it's tooltip msg to error_msg

        Parameters
        ----------
        widget : QWidget
        error_msg : str
                    the message that will appear in the tooltip
        superhot : bool
            whether to use the regular highlight
            or also include a black thick outline

        Returns
        -------
            None
        """

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

        if superhot:
            color = "rgb(223,1,74)"
            lw = "border: 3px solid black;"
        else:
            color = "rgb(223,1,74)"
            lw = ""

        color = "rgb(225,67,94)"

        if widget.objectName() not in ["metadata_root", "fgdc_metadata"]:
            try:
                widget.setToolTip(error_msg)
                widget.setStyleSheet(
                    """
                QGroupBox#{widgetname}{{
                background-color: {color};
                border: 2px solid red;
                subcontrol-position: top left; /* position at the top left*/
                padding-top: 20px;
                font: bold 14px;
                color: rgb(90, 90, 90);
                }}
                QGroupBox#{widgetname}::title {{
                text-align: left;
                subcontrol-origin: padding;
                subcontrol-position: top left; /* position at the top center */padding: 3 3px;
                }}
                QLabel{{
                font: 9pt "Arial";
                color: rgb(90, 90, 90);
                }}
                QLineEdit#{widgetname}, QPlainTextEdit#{widgetname}, QComboBox#{widgetname} {{
                font: 9pt "Arial";
                color: rgb(50, 50, 50);
                background-color: {color};
                opacity: 25;
                {lw}
                }}
                QToolTip {{
                background-color: rgb(255,76,77);
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
        widget_parent = widget
        attr_frame = widget

        while not widget_parent.objectName() == "fgdc_attr":
            widget_parent = widget_parent.parent()
            attr_frame = widget_parent
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

        widget_parent = widget.parent()
        while not type(widget_parent) == QTabWidget:
            widget_parent = widget_parent.parent()

        error_msg = "'Validation error in hidden contents, click to show'"
        widget_parent.setToolTip(error_msg)
        widget_parent.setStyleSheet(
            """
    QTabBar {{
    background-color: rgb(225,67,94);
    qproperty-drawBase:0;

}}
        """
        )

        self.error_widgets.append(widget_parent)

    def spelling_switch_triggered(self, e):
        spelling_action_text = self.ui.actionSpelling_flag.text()
        use_spelling = spelling_action_text == "Turn Spelling OFF"
        self.switch_spelling(not use_spelling)

    def switch_spelling(self, use_spelling):
        """
        Handle click event of the Turn Spelling (OFF | ON) action
        Changes the action's label and updates the widget's highlighter.

        Parameters
        ----------
        e : Qt event, not used

        Returns
        -------
        None
        """
        if use_spelling:
            self.ui.actionSpelling_flag.setText("Turn Spelling OFF")
        else:
            self.ui.actionSpelling_flag.setText("Turn Spelling ON")

        self.recursive_spell(self.metadata_root, use_spelling)

        self.settings.setValue("use_spelling", use_spelling)

    def recursive_spell(self, widget, which):
        """
        Turn on or off the spelling highlighter for this widget and
        iterate through the widget's child widgets to recursively do the
        same for them.

        Parameters
        ----------
        widget : Qwidget
        which : bool
                flag to turn spelling on or off
                True = turn spelling highlighting on
                False = turn spelling highlighting off

        Returns
        -------
            None
        """
        try:
            widget.highlighter.enabled = which
            widget.highlighter.rehighlight()
        except:
            pass

        for child_widget in self.metadata_root.get_children(widget):
            self.recursive_spell(child_widget, which)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls() and e.mimeData().urls()[0].isLocalFile():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Drop files directly onto the widget
        File locations are stored in fname
        :param e:
        :return:
        """
        try:
            if e.mimeData().hasUrls:
                e.setDropAction(Qt.CopyAction)

                url = e.mimeData().urls()[0]
                fname = url.toLocalFile()
                if os.path.isfile(fname):
                    self.open_file(fname)
                e.accept()
            else:
                e.ignore()
        except:
            # if anything goes wrong at all, pass silently.
            # This is just a convenience function
            pass

    def preview(self):
        """
        Shows a preview window with the xml content rendered using stylesheet

        Returns
        -------
        None
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
        root_dname = utils.get_install_dname("pymdwizard")

        help_html = os.path.join(root_dname, "docs", "html_output", "index.html")

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
        if self.cur_fname:
            out_fname = self.cur_fname[:-4] + "_REVIEW.docx"

            if self.metadata_root.schema == "bdp":
                which = "bdp"
            else:
                which = "fgdc"

            if time.time() - self.last_updated > 4:
                msg = "Would you like to save the current file before continuing?"
                exists_msg = "File already exists, would you like to overwrite it? Selecting 'No' "
                exists_msg += "will allow you to SaveAs."
                alert = QDialog()
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
                import os
                if os.path.exists(out_fname):
                    confirm2 = QMessageBox.question(self,
                        "File Overwrite",
                        exists_msg,
                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel ,
                    )
                    if confirm2 == QMessageBox.Yes:
                        self.save_file()
                    elif confirm2 == QMessageBox.No:
                        out_fname = QFileDialog.getSaveFileName(
                            self, "Save As", out_fname, filter="Document (*.docx)"
                        )[0]
                    elif confirm2 == QMessageBox.Cancel:
                        return

                review_utils.generate_review_report(cur_content, out_fname, which=which)

                import os, sys, subprocess

                def open_file(filename):
                    if sys.platform == "win32":
                        os.startfile('"{}"'.format(filename))
                    elif sys.platform == "darwin":
                        opener = "open"
                        subprocess.call([opener, filename])

                open_file(out_fname)

                msg = "Review document available at: {}".format(out_fname)
                msg += "\n\nReview document now opening in default application..."
                QMessageBox.information(self, "Review finished", msg)
            except BaseException:
                import traceback

                msg = "Problem encountered generating review document:\n{}".format(
                    traceback.format_exc()
                )
                QMessageBox.warning(self, "Problem encountered", msg)

    def launch_jupyter(self):
        """
        Launches a jupyter notebook server in our examples directory

        Returns
        -------
        None
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
        jupyter_dnames = self.settings.value("jupyter_dnames", [])

        try:
            jupyter_dnames.remove(dname)
        except ValueError:
            pass
            my_env = os.environ.copy()
            # my_env["PYTHONPATH"] = os.path.join(root_dir, "Python36_64")

        jupyter_dnames.insert(0, dname)
        del jupyter_dnames[PyMdWizardMainForm.max_recent_files :]
        self.settings.setValue("jupyter_dnames", jupyter_dnames)

    def about(self):
        """
        Display an 'about' message box with contanct info and current
        version number

        Returns
        -------
        None
        """
        msg = "The MetadataWizard was developed by the data management team <br> at the USGS Fort Collins Science Center,<br>"
        msg += "with support from the USGS Science Analytics and Synthesis (SAS), "
        msg += "and the USGS Community for Data Integration (CDI).<br><br>"
        msg += "Ongoing support provided by the USGS Science Analytics and Synthesis (SAS)<br>"
        msg += f"<br><br>Version: {__version__}<br>"
        msg += "<br> Project page: <a href='https://github.com/DOI-USGS/fort-pymdwizard'>https://github.com/DOI-USGS/fort-pymdwizard</a>"
        msg += "<br><br>Contact: Tamar Norkin at ask-sdm@usgs.gov"

        msgbox = QMessageBox.about(self, "About", msg)

    def check_for_updates(self, e=None, show_uptodate_msg=True):
        """
        Check if the usgs_root repo is at the same commit as this installation

        Parameters
        ----------
        e : qt event
            
        show_uptodate_msg : bool
           Whether to display a msg if no updates found

        Returns
        -------
        None
        """
        try:
            from git import Repo

            install_dir = utils.get_install_dname("pymdwizard")
            repo = Repo(install_dir)
            fetch = [r for r in repo.remotes if r.name == "origin"][0].fetch()
            master = [f for f in fetch if f.name == "origin/master"][0]

            if repo.head.commit != master.commit:
                msg = "An update(s) are available for the Metadata Wizard.\n"
                msg += "Would you like to install these now?"

                confirm = QMessageBox.question(
                    self, "Updates Available", msg, QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    self.update_from_github()
            elif show_uptodate_msg:
                msg = "MetadataWizard already up to date."
                QMessageBox.information(self, "No Update Needed", msg)

        except BaseException as e:
            if show_uptodate_msg:
                msg = (
                    "Problem Encountered Updating from USGS GitHub (https://github.com/DOI-USGS/fort-pymdwizard)\n\n"
                    "Please ensure that you have write access to the location where the Metadata Wizard is installed."
                )
                # msg += str(e)
                QMessageBox.information(self, "Update results", msg)

    def update_from_github(self):
        """
        Merge the latest version of the Wizard into the local repo

        Returns
        -------
        None
        """

        try:
            from git import Repo

            install_dir = utils.get_install_dname("pymdwizard")
            repo = Repo(install_dir)
            fetch = [r for r in repo.remotes if r.name == "origin"][0].fetch()
            master = [f for f in fetch if f.name == "origin/master"][0]

            merge_msg = repo.git.merge(master.name)

            msg = "Updated Successfully from GitHub. Close and re-open Metadata Wizard for changes to be implemented."
            QMessageBox.information(self, "Update results", msg)
        except BaseException as e:
            msg = (
                "Problem Encountered Updating from GitHub\n\n"
                "USGS users, if you experience issues, please try disconnecting/reconnecting to the internal USGS network and re-checking for updates."
            )
            # msg += str(e)
            QMessageBox.information(self, "Update results", msg)

        QApplication.restoreOverrideCursor()


def show_splash(version="2.x.x"):
    """
    Show the applications splash screen

    Parameters
    ----------
    version : str
            Version number as a string (only numerals, period or x supported)

    Returns
    -------
    None
    """
    splash_fname = utils.get_resource_path("icons/splash.jpg")
    splash_pix = QPixmap(splash_fname)

    size = splash_pix.size() * 0.35
    splash_pix = splash_pix.scaled(
        size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
    )
    numbers = {}
    for number in list(range(10)) + ["point", "x"]:
        fname = utils.get_resource_path("icons/{}.png".format(number))
        pix = QPixmap(fname)
        size = pix.size() * 0.65
        numbers[str(number)] = pix.scaled(
            size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
        )
    numbers["."] = numbers["point"]

    painter = QPainter(splash_pix)
    painter.begin(splash_pix)

    x, y = 470, 70
    for digit in version:
        painter.drawPixmap(int(x), y, numbers[digit])
        x += numbers[digit].rect().width() / 3

    painter.end()

    # Create splash screen with Window flag only
    splash = QSplashScreen(splash_pix, Qt.Window)

    splash.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

    splash.show()  # Show the splash screen
    splash.raise_()
    return splash


def launch_main(xml_fname=None, introspect_fname=None, env_cache={}):
    app = QApplication(sys.argv)

    splash = show_splash(__version__)

    app.processEvents()
    time.sleep(2)
    app.processEvents()
    mdwiz = PyMdWizardMainForm()
    mdwiz.show()
    mdwiz.env_cache = env_cache
    splash.finish(mdwiz)

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
        mdwiz.metadata_root.eainfo.detaileds[0].populate_from_fname(introspect_fname)
        mdwiz.metadata_root.eainfo.ui.fgdc_eainfo.setCurrentIndex(1)
    app.exec_()


if __name__ == "__main__":
    launch_main()
