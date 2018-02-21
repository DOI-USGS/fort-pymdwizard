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
import platform
import subprocess
from subprocess import Popen

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from pymdwizard.core import utils
from pymdwizard.gui import wiz_widget

from pymdwizard.gui.ui_files import UI_jupyterstarter


class JupyterStarter(QDialog):

    def __init__(self, previous_dnames=[], last_kernel='',
                 default_kernel = 'pymdwizard <<default>>',
                 update_function=None, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.build_ui()
        self.connect_events()

        self.kernels = {}
        self.previous_dnames = previous_dnames
        if previous_dnames:
            self.ui.dname.setCurrentText(previous_dnames[0])

        self.default_kernel = default_kernel
        self.populate_kernels()
        self.update_function = update_function

        for dname in self.previous_dnames:
            self.ui.dname.addItem(dname)

        if last_kernel and last_kernel in self.kernels:
            index = self.ui.kernel.findText(last_kernel)
            if index >= 0:
                self.ui.kernel.setCurrentIndex(index)

        utils.set_window_icon(self)
        self.setStyleSheet(wiz_widget.NORMAL_STYLE)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_jupyterstarter.Ui_Form()
        self.ui.setupUi(self)

    def populate_kernels(self):
        self.ui.kernel.addItem('pymdwizard <<default>>')
        self.kernels['pymdwizard <<default>>'] = \
                             utils.get_install_dname('python')

        try:
            kernels = subprocess.check_output(['conda', 'env', 'list'])
            for line in kernels.split(b'\n'):
                if line and not line.strip().startswith(b'#'):
                    try:
                        parts = line.split()
                        if parts[1] == b'*':
                            parts = [parts[0], parts[2]]
                        name, path = parts
                        self.ui.kernel.addItem(str(name)[2:-1])
                        self.kernels[str(name)[2:-1]] = str(path)
                    except (ValueError, IndexError):
                        pass
        except:
            pass

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.btn_cancel.clicked.connect(self.close_form)
        self.ui.btn_launch.clicked.connect(self.launch)

    def browse(self):
        if not self.previous_dnames:
            dname = ''
        else:
            dname = self.previous_dnames[0]

        jupyter_dname = QFileDialog.getExistingDirectory(self, "Select Directory to launch Jupyter from",
                                                         dname)
        if jupyter_dname:
            self.ui.dname.setCurrentText(jupyter_dname)

    def get_conda_root(self):
        try:
            conda_info = subprocess.check_output(['conda', 'info']).decode("utf-8")
            info = {}
            for line in conda_info.split('\n')[1:]:
                try:
                    key, value = line.strip().split(' : ')
                    info[key] = value
                except ValueError:
                    pass

            envs_dname = info['envs directories']
            try:
                root_dname = info["root environment"].replace('(writable)', '').strip()
            except KeyError:
                root_dname = info["base environment"].replace('(writable)', '').strip()

            return str(root_dname), str(envs_dname)
        except:
            return "", ""

    def launch(self):
        jupyter_dname = self.ui.dname.currentText()
        if not os.path.exists(jupyter_dname):
            msg = 'The selected directory to lauch jupyter in does not exists.'
            msg += '\nPlease check the location before launching Jupyter.'
            QMessageBox.information(self, "Missing Directory", msg)
            return

        if self.ui.kernel.currentText() == self.default_kernel:
            # this is pymdwizard specific

            python_dir = utils.get_install_dname('python')
            if platform.system() == 'Darwin':
                jupyterexe = os.path.join(python_dir, 'jupyter')
                p = Popen([jupyterexe, 'notebook'], cwd=jupyter_dname)
            else:
                root_dir = utils.get_install_dname('root')

                jupyterexe = os.path.join(python_dir, "scripts", "jupyter.exe")
                my_env = os.environ.copy()
                my_env["PYTHONPATH"] = os.path.join(root_dir, "Python36_64")

                p = Popen([jupyterexe, 'notebook'], cwd=jupyter_dname, env=my_env)

        else:
            root_dname, envs_dname = self.get_conda_root()
            activate_fname = os.path.join(root_dname, 'Scripts',
                                          'activate.bat')
            jupyter_exe_name = os.path.join(envs_dname,
                                            self.ui.kernel.currentText(),
                                            'Scripts', 'jupyter.exe')
            if not os.path.exists(jupyter_exe_name):
                jupyter_exe_name = os.path.join(root_dname, 'Scripts',
                                                'jupyter.exe')

            if self.ui.kernel.currentText() == 'root':
                cmds = ['"{}"'.format(jupyter_exe_name), 'notebook']
            else:
                cmds = ['"{}"'.format(activate_fname), self.ui.kernel.currentText(),
                        '&&', '"{}"'.format(jupyter_exe_name), 'notebook']
            Popen(" ".join(cmds), cwd=jupyter_dname)

        msg = 'Jupyter launching...\nJupyter will start momentarily in a new tab in your default internet browser.'
        QMessageBox.information(self, "Launching Jupyter", msg)

        self.update_function(self.ui.kernel.currentText(),
                              self.ui.dname.currentText())
        self.close()

    def close_form(self):
        self.parent = None
        self.deleteLater()
        self.close()


if __name__ == '__main__':
    utils.launch_widget(JupyterStarter, "JupyterStarter", previous_dnames=[r"c:\temp", r"c:\temp\junk"])

