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
    from PyQt5.QtWidgets import QComboBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_Status
except ImportError as err:
    raise ImportError(err, __file__)

class Status(WizardWidget):

    drag_label = "Status <status>"
    acceptable_tags = ["status"]

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_Status.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        encapsulates the two QComboBox's text into two separate element tags

        Returns
        -------
        status element tag in xml tree
        """
        status = xml_utils.xml_node(tag="status")

        progress_text = self.findChild(QComboBox, "fgdc_progress").currentText()
        progress = xml_utils.xml_node(
            tag="progress", text=progress_text, parent_node=status
        )
        update_text = self.findChild(QComboBox, "fgdc_update").currentText()
        update = xml_utils.xml_node(tag="update", text=update_text, parent_node=status)

        status.append(update)
        return status

    def from_xml(self, status):
        """
        parses the xml code into the relevant status elements

        Parameters
        ----------
        status - the xml element status and its contents

        Returns
        -------
        None
        """
        # print "Status", status.tag
        # print "text", status.find('progress').text
        try:
            if status.tag == "status":
                progress_box = self.findChild(QComboBox, "fgdc_progress")
                progress_text = status.find("progress").text
                # print progress_text
                progress_box.setCurrentText(progress_text)
                update_box = self.findChild(QComboBox, "fgdc_update")
                update_text = status.find("update").text
                # print update_text
                update_box.setCurrentText(update_text)
            else:
                print("The tag is not status")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Status, "Status testing")
