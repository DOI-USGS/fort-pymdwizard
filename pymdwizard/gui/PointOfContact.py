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
    acceptable_tags = ["pntcontac", "cntinfo"]

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

        self.collaped_size = QSize(self.WIDGET_WIDTH, self.COLLAPSED_HEIGHT)
        self.expanded_size = QSize(self.WIDGET_WIDTH, self.EXPANDED_HEIGHT)
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
            pntcontact = xml_utils.xml_node(tag="ptcontac")

            cntinfo = self.cntinfo.to_xml()
            pntcontact.append(cntinfo)
        else:
            pntcontact = None

        return pntcontact

    def from_xml(self, contact_information):

        if contact_information.tag == "cntinfo":
            cntinfo_node = contact_information
        else:
            cntinfo_node = contact_information.xpath("cntinfo")[0]
        self.cntinfo.from_xml(cntinfo_node)


if __name__ == "__main__":
    utils.launch_widget(ContactInfoPointOfContact, "ContactInfoPointOfContact testing")
