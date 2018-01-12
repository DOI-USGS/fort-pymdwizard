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

import pysb

from pymdwizard.core import utils, xml_utils

from pymdwizard.gui.ui_files import UI_sb_locator


class SBLocator(QWidget):

    def __init__(self, username=None, password=None,
                 hash='593af2e0e4b0764e6c602207',
                 parent=None,
                 mainform=None):

        self.mainform = mainform

        if username is None:
            username = getpass.getuser()
            contact = utils.get_usgs_contact_info(username, True)
            self.username = contact['fgdc_cntemail']
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

        self.connect_events()

    def log_into_sb(self):
        sb = pysb.SbSession()
        sb.login(username=self.username, password=self.password)
        return sb

    def connect_events(self):
        self.ui.btn_ok.clicked.connect(self.ok_click)

    def ok_click(self):
        self.hash = self.ui.hash.text()
        self.password = self.ui.password.text()
        self.username = self.ui.username.text()

        self.get_fgdc_file()
        print(self.fname)

        self.mainform.load_file(self.fname)
        self.mainform.sb_file = True
        self.mainform.cur_fname = self.fname
        self.hide()

    def check_permissions(self):
        sb = self.log_into_sb()

        permissions = sb.get_permissions(self.hash)
        return 'USER:{}'.format(self.username) in permissions['write']['acl']

    def get_fgdc_file(self):

        sb = self.log_into_sb()
        tempdir = tempfile.gettempdir()

        print(tempdir)

        item_json = sb.get_item(self.hash)

        try:
            fgdc_files = [f for f in item_json['files'] if
                          f['contentType'] == 'application/fgdc+xml']
            fgdc_url = fgdc_files[0]['url']
        except KeyError:
            fgdc_files = [f for f in item_json['facets'][0]['files'] if
                          f['name'].endswith('.xml')]
            fgdc_url = fgdc_files[0]['url']


        url = fgdc_files[0]["url"]
        fname = fgdc_files[0]['name']

        sb.download_file(url, fname, tempdir)
        self.fname = os.path.join(tempdir, fname)

    def put_fgdc_file(self):
        sb = self.log_into_sb()
        item_json = sb.get_item(self.hash)

        sb.replace_file(self.fname, item_json)

        # md = xml_utils.XMLRecord(self.fname)
        #
        # item_json = sb.get_item(self.hash)
        # item_json['title'] = md.metadata.idinfo.citation.citeinfo.title.text
        # item_json['body'] = md.metadata.idinfo.descript.abstract.text
        # item_json['purpose'] = md.metadata.idinfo.descript.purpose.text
        #
        # try:
        #     item_json['spatial']['boundingBox']['maxX'] = float(md.metadata.idinfo.spdom.bounding.eastbc.text)
        #     item_json['spatial']['boundingBox']['minX'] = float(md.metadata.idinfo.spdom.bounding.westbc.text)
        #     item_json['spatial']['boundingBox']['maxY'] = float(md.metadata.idinfo.spdom.bounding.northbc.text)
        #     item_json['spatial']['boundingBox']['minY'] = float(md.metadata.idinfo.spdom.bounding.southbc.text)
        # except:
        #     pass
        #
        # # ToDo: add keywords
        #
        #
        # sb.update_item(item_json=item_json)


if __name__ == "__main__":
    utils.launch_widget(SBLocator,
                        "SBLocator", password='')
