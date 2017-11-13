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

from PyQt5.QtCore import QSize

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_PointOfContact
from pymdwizard.gui import ContactInfo


class ContactInfoPointOfContact(WizardWidget):

    WIDGET_WIDTH = 500
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Point of Contact <pntcontac>"
    acceptable_tags = ['pntcontac', 'cntinfo']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_PointOfContact.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.cntinfo = ContactInfo.ContactInfo(parent=self)
        self.ui.main_layout.addWidget(self.cntinfo)

        self.collaped_size = QSize(self.WIDGET_WIDTH,
                                          self.COLLAPSED_HEIGHT)
        self.expanded_size = QSize(self.WIDGET_WIDTH,
                                   self.EXPANDED_HEIGHT)
        self.resize(self.collaped_size)

        self.setObjectName("ptcontac")

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.rbtn_yes.toggled.connect(self.contact_used_change)

    def contact_used_change(self, b):
        if b:
            self.cntinfo.show()
        else:
            self.cntinfo.hide()

    def has_content(self):
        return self.ui.rbtn_yes.isChecked()

    def to_xml(self):
        if self.ui.rbtn_yes.isChecked():
            pntcontact = xml_utils.xml_node(tag='ptcontac')

            cntinfo = self.cntinfo.to_xml()
            pntcontact.append(cntinfo)
        else:
            pntcontact = None

        return pntcontact

    def from_xml(self, contact_information):

        if contact_information.tag == 'cntinfo':
            cntinfo_node = contact_information
        else:
            cntinfo_node = contact_information.xpath('cntinfo')[0]
        self.cntinfo.from_xml(cntinfo_node)


if __name__ == "__main__":
    utils.launch_widget(ContactInfoPointOfContact,
                        "ContactInfoPointOfContact testing")
