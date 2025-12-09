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
TODO: Fix commented functions (delete or add justification for keeping).
"""

# Standard python libraries.
import os
import platform
from subprocess import Popen

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QFileDialog, QDialog, QMessageBox)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui import wiz_widget
    from pymdwizard.gui.ui_files import UI_jupyterstarter
except ImportError as err:
    raise ImportError(err, __file__)


class JupyterStarter(QDialog):
    """
    Description:
        A dialog widget that allows the user to select a directory and
        launch a Jupyter Lab session within that directory.
        Inherits from QDialog.

    Passed arguments:
        previous_dnames (list): List of directories previously used.
        update_function (callable, optional): Function to call after
            launching Jupyter (e.g., to save settings).
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes the UI and populates the directory history.
        2. Provides buttons to browse for a directory, launch Jupyter,
           or cancel.
        3. Executes "jupyter lab" (or equivalent) in a subprocess
           within the selected directory.

    Notes:
        Code related to kernel discovery is commented out and ignored
        in this update.
    """

    def __init__(
        self,
        previous_dnames=[],
        # last_kernel="",
        # default_kernel="pymdwizard <<default>>",
        update_function=None,
        parent=None,
    ):

        # Initialize the parent QDialog class.
        super(self.__class__, self).__init__(parent=parent)

        self.build_ui()
        self.connect_events()

        # Set default values.
        # self.kernels = {}
        self.previous_dnames = previous_dnames
        if previous_dnames:
            self.ui.dname.setCurrentText(previous_dnames[0])

        # self.default_kernel = default_kernel
        # self.populate_kernels()
        self.update_function = update_function

        # Populate the directory dropdown with history.
        for dname in self.previous_dnames:
            self.ui.dname.addItem(dname)

        # if last_kernel and last_kernel in self.kernels:
        #     index = self.ui.kernel.findText(last_kernel)
        #     if index >= 0:
        #         self.ui.kernel.setCurrentIndex(index)

        # Apply window icon and style.
        utils.set_window_icon(self)
        self.setStyleSheet(wiz_widget.NORMAL_STYLE)

        # try:
        #     import jupyterlab
        #     self.ui.usejupyterframe.setEnabled(True)
        # except ImportError:
        #     self.ui.usejupyterframe.setEnabled(False)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates and sets up the UI elements.

        Notes:
            None
        """

        # Instantiate and setup the UI
        self.ui = UI_jupyterstarter.Ui_Form()
        self.ui.setupUi(self)

    # def populate_kernels(self):
    #     self.ui.kernel.addItem("pymdwizard <<default>>")
    #     self.kernels["pymdwizard <<default>>"] = utils.get_install_dname("python")
    #     try:

    #         conda_exe = os.path.join(self.get_conda_root()[0], "Scripts", "conda.exe")
    #         if os.path.exists(conda_exe):
    #             kernels = subprocess.check_output([conda_exe, "env", "list"])
    #         else:
    #             kernels = subprocess.check_output(["conda", "env", "list"])
    #         for line in kernels.split(b"\n"):
    #             if line and not line.strip().startswith(b"#"):
    #                 try:
    #                     parts = line.split()
    #                     if parts[1] == b"*":
    #                         parts = [parts[0], parts[2]]
    #                     name, path = parts
    #                     self.ui.kernel.addItem(str(name)[2:-1])
    #                     self.kernels[str(name)[2:-1]] = str(path)
    #                 except (ValueError, IndexError):
    #                     pass
    #     except:
    #         pass

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
            Connects Browse, Cancel, and Launch buttons to their
            respective methods.

        Notes:
            None
        """

        # Connect button signals.
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.btn_cancel.clicked.connect(self.close_form)
        self.ui.btn_launch.clicked.connect(self.launch)

    def browse(self):
        """
        Description:
            Opens a dialog to browse for a directory and sets the
            dropdown text to the selected path.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Determines the initial directory for the file dialog.
            2. Calls "QFileDialog.getExistingDirectory".
            3. Sets the selected directory as the current text in the
               directory dropdown.

        Notes:
            None
        """

        # Determine the default directory for the dialog.
        dname = self.previous_dnames[0] if self.previous_dnames else ""

        # Open file dialog to select the directory.
        jupyter_dname = QFileDialog.getExistingDirectory(
            self, "Select Directory to launch Jupyter from", dname
        )

        # Update the dropdown if a directory was selected.
        if jupyter_dname:
            self.ui.dname.setCurrentText(jupyter_dname)


    # def get_conda_root(self):
    #     try:
    #         from conda.core.envs_manager import list_all_known_prefixes

    #         prefixes = list_all_known_prefixes()
    #         return prefixes[0], os.path.join(prefixes[0], "envs")
    #     except:
    #         try:

    #             conda_info = subprocess.check_output(["conda", "info"]).decode("utf-8")
    #             info = {}
    #             for line in conda_info.split("\n")[1:]:
    #                 try:
    #                     key, value = line.strip().split(" : ")
    #                     info[key] = value
    #                 except ValueError:
    #                     pass

    #             envs_dname = info["envs directories"]
    #             try:
    #                 root_dname = (
    #                     info["root environment"].replace("(writable)", "").strip()
    #                 )
    #             except KeyError:
    #                 root_dname = (
    #                     info["base environment"].replace("(writable)", "").strip()
    #                 )

    #             return str(root_dname), str(envs_dname)
    #         except:
    #             return "", ""

    def launch(self):
        """
        Description:
            Launches a Jupyter Lab session in a subprocess.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Validates the selected directory.
            2. Configures the environment variables (PYTHONPATH).
            3. Executes the Jupyter Lab command using `Popen` based on
               the operating system (Mac/Windows).
            4. Displays a success message and closes the dialog.

        Notes:
            None
        """

        # Retrieve widget value.
        jupyter_dname = self.ui.dname.currentText()

        # Validate the directory existence
        if not os.path.exists(jupyter_dname):
            msg = (
                "The selected directory to lauch jupyter in does not "
                "exists.\nPlease check the location before launching "
                "Jupyter."
            )
            QMessageBox.information(self, "Missing Directory", msg)
            return

        python_dir = utils.get_install_dname("python")

        if platform.system() == "Darwin":
            # For Mac OS: direct execution of "jupyter lab".
            python_dir = utils.get_install_dname("python")
            jupyterexe = os.path.join(python_dir, "jupyter")
            my_env = os.environ.copy()
            my_env["PYTHONPATH"] = os.path.join(python_dir, "python")

            # Execute command.
            Popen([jupyterexe, "lab"], cwd=jupyter_dname, env=my_env)
        else:
            # For Windows/Other: execution via python module.
            root_dir = utils.get_install_dname("root")
            my_env = os.environ.copy()

            # Set PYTHONPATH to include pymdwizard root.
            my_env["PYTHONPATH"] = os.path.join(root_dir, "pymdwizard")

            pythonexe = os.path.join(
                utils.get_install_dname("python"), "python.exe"
            )

            # Execute command.
            Popen(
                [pythonexe, "-m", "jupyterlab"],
                cwd=jupyter_dname,
                env=my_env,
            )

            # Inform the user that launch is in progress.
            msg = (
                "Jupyter launching...\nJupyter will start momentarily in a "
                "new tab in your default internet browser."
            )
            QMessageBox.information(self, "Launching Jupyter", msg)

            # Call update function (e.g., to save directory history).
            self.update_function(self.ui.dname.currentText())
            self.close()

    def close_form(self):
        """
        Description:
            Safely closes the dialog box.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets parent to None, then deletes the widget safely and
            closes the window.

        Notes:
            None
        """

        self.parent = None
        self.deleteLater()
        self.close()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(
        JupyterStarter, "JupyterStarter",
        previous_dnames=[r"c:\temp", r"c:\temp\junk"]
    )
