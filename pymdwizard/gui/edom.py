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

from PyQt5.QtWidgets import QWidget

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.ui_files import UI_edom


class Edom(QWidget):  #

    drag_label = "Enumerated Domain <edom>"
    acceptable_tags = ['edom']

    def __init__(self, xml=None, parent=None, item=None):
        QWidget.__init__(self, parent=parent)
        self.item = item
        self.build_ui()

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_edom.Ui_fgdc_attrdomv()
        self.ui.setupUi(self)
        self.ui.fgdc_edomvd.item = self.item
        self.ui.fgdc_edomvd.heightMin = 25
        self.ui.fgdc_edomvd.heightMax = 150
        self.ui.fgdc_edomvd.sizeChange()

        defsource = utils.get_setting('defsource', 'Producer defined')
        self.ui.fgdc_edomvds.setText(defsource)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'timeperd'
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        e.ignore()

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        edom = xml_utils.xml_node('edom')
        edomv = xml_utils.xml_node('edomv', text=self.ui.fgdc_edomv.text(), parent_node=edom)
        edomvd = xml_utils.xml_node('edomvd', text=self.ui.fgdc_edomvd.toPlainText(), parent_node=edom)
        edomvds = xml_utils.xml_node('edomvds', text=self.ui.fgdc_edomvds.text(), parent_node=edom)

        return edom

    def from_xml(self, edom):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if edom.tag == 'edom':
                self.ui.fgdc_edomvds.setText('')
                utils.populate_widget(self, edom)
            else:
                print("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Edom,
                        "edom testing")
