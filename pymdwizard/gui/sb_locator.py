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
import tempfile
import getpass

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit

try:
    import pysb
except ImportError:
    import sciencebasepy as pysb

from pymdwizard.core import utils, xml_utils

from pymdwizard.gui.ui_files import UI_sb_locator


class SBLocator(QWidget):
    def __init__(
        self,
        username=None,
        password=None,
        hash="593af2e0e4b0764e6c602207",
        parent=None,
        mainform=None,
    ):

        self.mainform = mainform

        if username is None:
            try:
                username = getpass.getuser()
                contact = utils.get_usgs_contact_info(username, True)
                self.username = contact["fgdc_cntemail"]
            except:
                self.username = ""
        else:
            self.username = username

        QWidget.__init__(self, parent=parent)
        self.ui = UI_sb_locator.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.password = password
        self.hash = hash

        self.ui.username.setText(self.username)
        self.ui.password.setText(password)
        self.ui.hash.setText(hash)

        self.setWindowTitle("ScienceBase Item/User Identifier")

        self.connect_events()

    def log_into_sb(self):
        sb = pysb.SbSession()
        sb.login(username=self.username, password=self.password)
        return sb

    def connect_events(self):
        self.ui.btn_ok.clicked.connect(self.ok_click)
        self.ui.btn_check.clicked.connect(self.check_permissions)

    def update_content(self):
        self.password = self.ui.password.text()
        self.username = self.ui.username.text()

        self.hash = self.ui.hash.text()

    def ok_click(self):
        self.update_content()

        if not self.check_permissions():
            return False

        fname = self.get_fgdc_file()
        if not fname:
            return None

        self.mainform.load_file(self.fname)
        self.mainform.sb_file = True
        self.mainform.cur_fname = self.fname
        self.hide()

    def check_item_click(self):
        self.update_content()
        accessible = self.check_permissions()

    def check_permissions(self):
        try:
            self.update_content()
            sb = self.log_into_sb()
        except:
            msg = "Login to ScienceBase Failed. \nCheck username and password"
            QMessageBox.warning(self, "SB Login Failed", msg)
            return False

        try:
            permissions = sb.get_permissions(self.hash)
            writable = "USER:{}".format(self.username) in permissions["write"]["acl"]
        except:
            writable = False

        if not writable:
            try: 
                writable = permissions['write']['inherited'] == True
            except: 
                writable = False

        if not writable:
            msg = "This item does not appear to be writable by the designated user."
            QMessageBox.warning(self, "Write permission error", msg)
            return False
        if writable:
            item = sb.get_item(self.hash)
            title = item['title']

            fname = self.get_fgdc_file()

            if fname:
                msg = f"SB item:\n {self.hash} ready to open and edit."
                QMessageBox.information(self, "Good to go!", msg)
            else:
                return False

        return True

    def get_fgdc_file(self):

        if self.mainform.cur_fname:
            self.mainform.save_file()

        sb = self.log_into_sb()
        tempdir = tempfile.gettempdir()

        item_json = sb.get_item(self.hash)

        try:
            fgdc_files = [
                f
                for f in item_json["files"]
                if f["contentType"] == "application/fgdc+xml"
            ]
        except KeyError:
            try:
                fgdc_files = [
                    f for f in item_json["facets"][0]["files"] if f["name"].endswith(".xml")
                ]
            except:
                fgdc_files = []

        if len(fgdc_files) == 1:
            # Perfect.  There is one and only one xml file.
            url = fgdc_files[0]["url"]
            fname = fgdc_files[0]["name"]

            sb.download_file(url, fname, tempdir)
            self.fname = os.path.join(tempdir, fname)

            return self.fname
        elif len(fgdc_files) == 0:
            msg = f"There doesn't appear to be an FGDC XML file associated with item: {self.hash}.\n"
            msg += "You will need to upload a new FGDC record to the item to use this functionality."
            QMessageBox.warning(self, "No existing Metadata file!", msg)
            return False
        else:
            msg = f"There appears to be more than one FGDC XML file associated with item: {self.hash}.\n"
            msg += "Since we can't determine which to edit, this functionality won't work."
            msg += "\nYou will need to download and edit the file directly."
            QMessageBox.warning(self, "More than one XML file!", msg)
            return False

    def put_fgdc_file(self):
        sb = self.log_into_sb()
        item_json = sb.get_item(self.hash)

        sb.replace_file(self.fname, item_json)


if __name__ == "__main__":
    utils.launch_widget(SBLocator, "SBLocator", password="")
