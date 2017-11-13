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

from PyQt5.QtWidgets import QComboBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_Status


class Status(WizardWidget):

    drag_label = "Status <status>"
    acceptable_tags = ['status']

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
        status = xml_utils.xml_node(tag='status')

        progress_text = self.findChild(QComboBox, 'fgdc_progress').currentText()
        progress = xml_utils.xml_node(tag='progress', text=progress_text,
                                      parent_node=status)
        update_text = self.findChild(QComboBox, 'fgdc_update').currentText()
        update = xml_utils.xml_node(tag='update', text=update_text,
                                       parent_node=status)

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
        #print "Status", status.tag
        #print "text", status.find('progress').text
        try:
            if status.tag == 'status':
                progress_box = self.findChild(QComboBox, 'fgdc_progress')
                progress_text = status.find('progress').text
                #print progress_text
                progress_box.setCurrentText(progress_text)
                update_box = self.findChild(QComboBox, 'fgdc_update')
                update_text = status.find('update').text
                #print update_text
                update_box.setCurrentText(update_text)
            else:
                print ("The tag is not status")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Status,
                        "Status testing")
