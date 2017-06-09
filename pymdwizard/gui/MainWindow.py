#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt application for the main pymdwizard application


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""
import sys, os
import json
import tempfile
import time
import datetime
import shutil

from lxml import etree


from PyQt5.QtWidgets import QMainWindow, QApplication, QSplashScreen, QMessageBox, QAction
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5.QtCore import QFile, QFileInfo
from PyQt5.QtCore import Qt, QSettings, QFileSystemWatcher
from PyQt5.QtGui import QPainter, QPixmap


from pymdwizard.gui.ui_files import UI_MainWindow
from pymdwizard.gui.MetadataRoot import MetadataRoot
from pymdwizard.core import xml_utils, utils, fgdc_utils
from pymdwizard.gui.Preview import Preview

import sip

class PyMdWizardMainForm(QMainWindow):

    max_recent_files = 10

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()

        self.cur_fname = ''
        self.file_watcher = None

        # list of buttons for opening recently accessed files
        self.recent_file_actions = []
        # list of widgets that are currently styled as errors
        self.error_widgets = []
        # the last error widget that was highlighted
        self.last_highlight = None

        self.build_ui()
        self.connect_events()

        self.load_default()

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        utils.set_window_icon(self)

        self.metadata_root = MetadataRoot()
        self.ui.centralwidget.layout().addWidget(self.metadata_root)

        for i in range(PyMdWizardMainForm.max_recent_files):
            self.recent_file_actions.append(
                QAction(self, visible=False,
                        triggered=self.open_recent_file))
            self.ui.menuRecent_Files.addAction(self.recent_file_actions[i])
        self.update_recent_file_actions()

        self.ui.menuErrors.clear()

        settings = QSettings('USGS', 'pymdwizard')
        template_fname = settings.value('template_fname')

        if template_fname is not None:
            just_fname = os.path.split(template_fname)[-1]
            self.ui.actionCurrentTemplate.setText('Current: ' + just_fname)

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
        self.ui.actionBrowseTemplate.triggered.connect(self.set_template)
        self.ui.actionRestoreBuiltIn.triggered.connect(self.restore_template)
        self.ui.actionLaunch_Jupyter.triggered.connect(self.launch_jupyter)
        self.ui.actionUpdate.triggered.connect(self.update_from_github)

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
        settings = QSettings('USGS', 'pymdwizard')
        recent_files = settings.value('recentFileList', [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(self, fname, dname, \
                                            filter="XML Files (*.xml)")

        if fname[0]:
            return fname[0]
        else:
            return ''

    def open_file(self, fname=None):
        """
        Browse to a file and load it if it is acceptable

        Returns
        -------
        None
        """
        if fname is None or not fname:
            fname = self.get_xml_fname()

        if fname:
            self.load_file(fname)
            self.set_current_file(fname)
            self.update_recent_file_actions()

    def load_file(self, fname):
        """
        load a file's content into the application.

        Parameters
        ----------
        fname : str
                full file path and name of the file to load
        Returns
        -------
        None
        """
        self.file_watcher = QFileSystemWatcher([fname])
        self.file_watcher.fileChanged.connect(self.file_updated)
        self.last_updated = time.time()

        self.clear_validation()

        #check that we have read write access to the file
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
        exc_info = sys.exc_info()
        try:
            new_record = etree.parse(fname)
            self.metadata_root._from_xml(new_record)
            self.statusBar().showMessage("File loaded", 10000)
        except BaseException as e:
            import traceback
            msg = "Cannot open file %s:\n%s." % (fname, traceback.format_exc())
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
            msg = "The file you are editing has been changed on disk.  Would you like to reload this File?"
            alert = QDialog()
            self.last_updated = time.time()
            confirm = QMessageBox.question(self, "File Changed", msg, QMessageBox.Yes | QMessageBox.No)
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
        settings = QSettings('USGS', 'pymdwizard')
        recent_files = settings.value('recentFileList', [])
        if recent_files:
            dname, fname = os.path.split(recent_files[0])
        else:
            fname, dname = "", ""

        fname = QFileDialog.getSaveFileName(self, "Save As", dname, \
                                            filter="XML Files (*.xml)")

        return fname[0]

    def save_file(self):
        """
        Save the current xml document.  Prompts for a filename if one
        has not been set yet.

        Returns
        -------
        None
        """
        if not self.cur_fname:
            fname = self.get_save_name()
            if not fname:
                return
        else:
            fname = self.cur_fname

        fname_msg = utils.check_fname(fname)
        if not fname_msg == 'good':
            msg = "Cannot write to :\n  {}.".format(fname)
            QMessageBox.warning(self, "Metadata Wizard", msg)
            return

        xml_utils.save_to_file(self.metadata_root._to_xml(), fname)
        self.last_updated = time.time()

        self.set_current_file(fname)
        self.statusBar().showMessage("File saved", 2000)

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
            template_fname = utils.get_resource_path('CSDGM_Template.xml')
            shutil.copyfile(template_fname, save_as_fname)
            self.load_file(save_as_fname)
            self.set_current_file(save_as_fname)
            self.update_recent_file_actions()

            today = fgdc_utils.format_date(datetime.datetime.now())
            self.metadata_root.metainfo.metd.set_date(today)

    def set_template(self):
        fname = self.get_xml_fname()

        if fname:
            settings = QSettings('USGS', 'pymdwizard')
            settings.setValue('template_fname', fname)
            just_fname = os.path.split(fname)[-1]
            self.ui.actionCurrentTemplate.setText('Current: ' + just_fname)

    def restore_template(self):
        settings = QSettings('USGS', 'pymdwizard')
        fname = utils.get_resource_path('CSDGM_Template.xml')
        settings.setValue('template_fname', None)
        self.ui.actionCurrentTemplate.setText('Current: Built-in')

    def load_default(self):
        settings = QSettings('USGS', 'pymdwizard')
        template_fname = settings.value('template_fname')

        if template_fname is None:
            template_fname = utils.get_resource_path('CSDGM_Template.xml')

        self.load_file_content(template_fname)
        self.cur_fname = ''

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

            settings = QSettings('USGS', 'pymdwizard')
            files = settings.value('recentFileList', [])

            try:
                files.remove(fname)
            except ValueError:
                pass

            files.insert(0, fname)
            del files[PyMdWizardMainForm.max_recent_files:]

            settings.setValue('recentFileList', files)

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
        settings = QSettings('USGS', 'pymdwizard')
        files = settings.value('recentFileList', [])

        num_recent_files = min(len(files), PyMdWizardMainForm.max_recent_files)

        for i in range(num_recent_files):
            stripped_name = QFileInfo(files[i]).fileName()
            text = "&%d %s" % (i + 1, stripped_name)
            self.recent_file_actions[i].setText(text)
            self.recent_file_actions[i].setData(files[i])
            self.recent_file_actions[i].setVisible(True)

        for j in range(num_recent_files, PyMdWizardMainForm.max_recent_files):
            self.recent_file_actions[j].setVisible(False)

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
        if self.cur_fname:
            cur_xml = xml_utils.node_to_string(self.metadata_root._to_xml())
            disk_xml = xml_utils.node_to_string(xml_utils.fname_to_node(self.cur_fname))

            if cur_xml != disk_xml:
                msg = "Would you like to save before exiting?"
                alert = QDialog()
                self.last_updated = time.time()
                confirm = QMessageBox.question(self, "File Changed", msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if confirm == QMessageBox.Yes:
                    self.save_file()
                elif confirm == QMessageBox.Cancel:
                    return 'Cancel'
                self.cur_fname = ''

        self.close()
        return 'Close'

    def closeEvent(self, event):
        """ Intercept the builtin closeEvent so that we can check for
        changes and ask if we should change.

        Parameters
        ----------
        event

        Returns
        -------

        """
        if self.exit() == 'Close':
            event.accept()
        else:
            event.ignore()

    def clear_validation(self):
        """
        Remove the error highlighting from all the error widgets

        Returns
        -------
        None
        """
        self.ui.menuErrors.clear()

        annotation_lookup_fname = utils.get_resource_path("FGDC/bdp_lookup")
        with open(annotation_lookup_fname, encoding='utf-8') as data_file:
            annotation_lookup = json.loads(data_file.read())

        for widget in self.error_widgets:

            if not sip.isdeleted(widget) and \
                    widget.objectName() not in ['metadata_root', 'fgdc_metadata']:
                widget.setStyleSheet("""""")
                shortname = widget.objectName().replace('fgdc_', '')
                if shortname[-1].isdigit():
                    shortname = shortname[:-1]
                widget.setToolTip(annotation_lookup[shortname]['annotation'])

        self.error_widgets = []

    def validate(self):
        """
        Check the current record against the schema and highlight any
        error widgets

        Returns
        -------
        None
        """

        if self.metadata_root.schema == 'bdp':
            xsl_fname = utils.get_resource_path('FGDC/BDPfgdc-std-001-1998-annotated.xsd')
        else:
            xsl_fname = utils.get_resource_path('FGDC/fgdc-std-001-1998-annotated.xsd')
        from pymdwizard.core import fgdc_utils
        errors = fgdc_utils.validate_xml(self.metadata_root._to_xml(), xsl_fname)

        self.clear_validation()

        marked_errors = []

        self.widget_lookup = self.metadata_root.make_tree(widget=self.metadata_root)

        error_count = 0
        for error in errors:
            xpath, error_msg, line_num = error
            if xpath not in marked_errors:

                action = QAction(self, visible=True)
                action.setText(error_msg)
                action.setData(xpath)
                action.triggered.connect(self.goto_error)
                self.ui.menuErrors.addAction(action)
                marked_errors.append(xpath)

                # widget = self.metadata_root.get_widget(xpath)
                widgets = self.widget_lookup.xpath_march(xpath, as_list=True)
                for widget in widgets:
                    if isinstance(widget, list):
                        for w in widget:
                            print('problem highlighting error', xpath, widget)
                    else:
                        self.highlight_error(widget.widget, error_msg)
                        self.error_widgets.append(widget.widget)
                        error_count += 1

        if errors:
            msg = "There are {} errors in this record".format(error_count)
            self.statusBar().showMessage(msg, 20000)
            msg += "\n\n These errors are highlighted in red in the form below."
            msg += "\n\n These errors are also listed in the Validation Menu's Errors submenu item above."
            msg += "\n Clicking each error will take you to the section it is contained in."
            msg += "\n Note that some highlighed errors can be in collapsed items, scrolled out of view, or in non-selected tabs"
            QMessageBox.warning(self, "Validation", msg)
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

        xpath = self.sender().data()
        section = xpath.split('/')[1]

        if section == 'idinfo':
            subsection = xpath.split('/')[2]
            if subsection == 'spdom':
                self.metadata_root.switch_section(2)
            else:
                self.metadata_root.switch_section(0)
        elif section == 'dataqual':
            self.metadata_root.switch_section(1)
        elif section == 'spdoinfo' or section == 'spref':
            self.metadata_root.switch_section(2)
        elif section == 'eainfo':
            self.metadata_root.switch_section(3)
        elif section == 'eainfo':
            self.metadata_root.switch_section(3)
        elif section == 'distinfo':
            self.metadata_root.switch_section(4)
        elif section == 'metainfo':
            self.metadata_root.switch_section(5)

        if self.last_highlight is not None and \
                not sip.isdeleted(self.last_highlight):
            self.highlight_error(self.last_highlight, self.last_highlight.toolTip())

        bad_widget = self.widget_lookup.xpath_march(xpath, as_list=True)
        self.last_highlight = bad_widget[0].widget
        self.highlight_error(bad_widget[0].widget, self.sender().text(), superhot=True)

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

        if widget.objectName() in ['fgdc_edomv', 'fgdc_edomvd', 'fgdc_edomvds',
                                   'fgdc_attrlabl', 'fgdc_attrdef',
                                   'fgdc_attrdefs', 'fgdc_attrdomv',
                                   'fgdc_codesetd', 'fgdc_edom', 'fgdc_rdom',
                                   'fgdc_udom', 'fgdc_rdommin', 'fgdc_rdommax',
                                   'fgdc_codesetn', 'fgdc_codesets']:
            self.highlight_attr(widget)

        if widget.objectName() in ['fgdc_themekey', 'fgdc_themekt',
                                   'fgdc_placekey', 'fgdc_placekt',
                                   'fgdc_procdesc', 'fgdc_srcused',
                                   'fgdc_srcprod']:
            self.highlight_tab(widget)


        if superhot:
            color = "rgb(223,1,74)"
            lw = "border: 3px solid black;"
        else:
            color = 'rgb(223,1,74)'
            lw = ''

        color = "rgb(225,67,94)"

        if widget.objectName() not in ['metadata_root', 'fgdc_metadata']:
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
        """.format(widgetname=widget.objectName(), color=color, lw=lw))



    def highlight_attr(self, widget):
        widget_parent = widget.parent()

        while not widget_parent.objectName() == 'fgdc_attr':
            widget_parent = widget_parent.parent()

        error_msg = "'Validation error in hidden contents, click to show'"
        widget_parent.setToolTip(error_msg)
        widget_parent.setStyleSheet(
            """
    QFrame#{widgetname}{{
    border: 2px solid red;
    }}
        """.format(widgetname=widget_parent.objectName()))

        self.error_widgets.append(widget_parent)

    def highlight_tab(self, widget):
        pass
    #         widget_parent = widget.parent()
    #
    #     while not widget_parent.
    #         widget_parent = widget_parent.parent()
    #
    #     error_msg = "'Validation error in hidden contents, click to show'"
    #     widget_parent.setToolTip(error_msg)
    #     widget_parent.setStyleSheet(
    #         """
    # QTab#{widgetname}{{
    # border: 2px solid red;
    # }}
    #     """.format(widgetname=widget_parent.objectName()))
    #
    #     self.error_widgets.append(widget_parent

    def preview(self):
        """
        Shows a preview window with the xml content rendered using stylesheet

        Returns
        -------
        None
        """

        xsl_fname = utils.get_resource_path("FGDC/FGDC_Stylesheet.xsl")
        transform = etree.XSLT(etree.parse(xsl_fname))
        result = transform(self.metadata_root._to_xml())

        tmp = tempfile.NamedTemporaryFile(suffix='.html')
        tmp.close()
        result.write(tmp.name)

        self.preview = Preview(url=tmp.name)

        self.preview_dialog = QDialog(self)
        self.preview_dialog.setWindowTitle('Metadata Preview')
        self.preview_dialog.setLayout(self.preview.layout())

        self.preview_dialog.exec_()

    def launch_jupyter(self):
        """
        Launches a jupyter notebook server in our examples directory

        Returns
        -------
        None
        """
        from subprocess import Popen

        jupyter_dialog = JupyterLocationDialog()
        utils.set_window_icon(jupyter_dialog.msgBox)
        jupyter_dialog.msgBox.setWindowTitle("Where do you want to launch Jupyter?")
        ret = jupyter_dialog.msgBox.exec_()

        install_dir = utils.get_install_dname()
        if ret == 0:
            jupyter_dname = os.path.join(install_dir, 'examples')
        elif ret == 1:
            settings = QSettings('USGS', 'pymdwizard')
            last_jupyter_dname = settings.value('last_jupyter_dname')

            if last_jupyter_dname is None:
                last_jupyter_dname = os.path.join(install_dir, 'examples')
            jupyter_dname = QFileDialog.getExistingDirectory(self, "Select Directory to launch Jupyter from", last_jupyter_dname)
            if jupyter_dname:
                settings.setValue('last_jupyter_dname', jupyter_dname)
        else:
            return

        root_dir = os.path.dirname(install_dir)
        jupyterexe = os.path.join(root_dir, "Python35_64", "scripts", "jupyter.exe")

        if os.path.exists(jupyterexe) and os.path.exists(root_dir):
            p = Popen([jupyterexe, 'notebook'], cwd=jupyter_dname)

            msg = 'Jupyter launching...\nJupyter will start momentarily in a new tab in your default internet browser.'

            QMessageBox.information(self, "Launching Jupyter", msg)

    def update_from_github(self):
        from subprocess import check_output

        install_dir = utils.get_install_dname()
        root_dir = os.path.dirname(install_dir)
        update_bat = os.path.join(root_dir, 'update_wizard.bat')
        if os.path.exists(update_bat) and os.path.exists(root_dir):
            try:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                p = check_output([update_bat], cwd=root_dir, shell=False)
                if p.splitlines()[-1] == b'Already up-to-date.':
                    msg = 'Application already up to date.'
                else:
                    msg = 'Application updated.\n\n'
                    msg += 'Please close and restart for these updates to take effect'
                QApplication.restoreOverrideCursor()
            except BaseException as e:
                import traceback
                msg = "Could not update application:\n{}".format(traceback.format_exc())
                QMessageBox.warning(self, "Recent Files", msg)

        else:
            msg = 'Could not find the batch file to update the application'

        QMessageBox.information(self, "Update results", msg)


class JupyterLocationDialog(QDialog):
    def __init__(self, parent=None):
        super(JupyterLocationDialog, self).__init__(parent)

        self.msgBox = QMessageBox()
        self.msgBox.setText('Choose option below:')
        self.msgBox.addButton(QPushButton('Default (MetadataWizard examples folder)'), QMessageBox.YesRole)
        self.msgBox.addButton(QPushButton('Browse to different folder'), QMessageBox.NoRole)
        self.msgBox.addButton(QPushButton('Cancel'), QMessageBox.RejectRole)


def launch_main(xml_fname=None, introspect_fname=None):
    app = QApplication(sys.argv)

    import time
    start = time.time()
    splash_fname = utils.get_resource_path('icons/splash.jpg')
    splash_pix = QPixmap(splash_fname)

    size = splash_pix.size()*.35
    splash_pix = splash_pix.scaled(size, Qt.KeepAspectRatio,
                                transformMode=Qt.SmoothTransformation)

    # # below makes the pixmap half transparent
    painter = QPainter(splash_pix)
    painter.setCompositionMode(painter.CompositionMode_DestinationAtop)
    painter.end()

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    time.sleep(2)

    app.processEvents()
    mdwiz = PyMdWizardMainForm()
    mdwiz.show()
    splash.finish(mdwiz)

    if xml_fname is not None and os.path.exists(xml_fname):
        mdwiz.open_file(xml_fname)

    if introspect_fname is not None and os.path.exists(introspect_fname):
        mdwiz.metadata_root.eainfo.detaileds[0].populate_from_fname(introspect_fname)
        mdwiz.metadata_root.eainfo.ui.fgdc_eainfo.setCurrentIndex(1)
    app.exec_()


if __name__ == '__main__':
    launch_main()