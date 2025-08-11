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

# Non-standard python libraries.
try:
    from PyQt5.QtCore import QSize
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_proccont
    from pymdwizard.gui import ContactInfo
except ImportError as err:
    raise ImportError(err, __file__)


class ProcessContact(WizardWidget):

    WIDGET_WIDTH = 500
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Process Contact <proccont>"
    acceptable_tags = ["proccont", "cntinfo"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_proccont.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.cntinfo = ContactInfo.ContactInfo()
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

    def to_xml(self):
        if self.ui.rbtn_yes.isChecked():
            proccont = xml_utils.xml_node(tag="proccont")

            cntinfo = self.cntinfo.to_xml()
            proccont.append(cntinfo)
        else:
            self.ui.rbtn_no.setChecked(True)
            proccont = None

        return proccont

    def from_xml(self, contact_information):

        if contact_information.tag == "cntinfo":
            self.ui.rbtn_yes.setChecked(True)
            cntinfo_node = contact_information
        else:
            cntinfo_node = contact_information.xpath("cntinfo")[0]

        self.cntinfo.from_xml(cntinfo_node)


if __name__ == "__main__":
    utils.launch_widget(ProcessContact, "ProcessContact testing")
