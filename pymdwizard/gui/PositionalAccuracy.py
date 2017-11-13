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

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_posacc


class PositionalAccuracy(WizardWidget): #

    drag_label = "Positional Accuracy <possacc>"
    acceptable_tags = ['posacc']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_posacc.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def has_content(self):
        """
        Checks for valid content in this widget

        Returns
        -------
        Boolean
        """
        has_content = False

        if self.ui.fgdc_horizpa.toPlainText():
            has_content = True
        if self.ui.fgdc_vertacc.toPlainText():
            has_content = True

        return has_content
         
                
    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        possacc element tag in xml tree
        """
        possacc = xml_utils.xml_node(tag='posacc')
        horizpa = xml_utils.xml_node(tag='horizpa')
        horizpar = xml_utils.xml_node(tag='horizpar')
        horizpar_text = self.findChild(QPlainTextEdit,
                                       "fgdc_horizpa").toPlainText()
        if len(horizpar_text) > 0:
            horizpar.text = horizpar_text
            horizpa.append(horizpar)
            possacc.append(horizpa)

        vertacc = xml_utils.xml_node(tag='vertacc')
        vertaccr = xml_utils.xml_node(tag='vertaccr')
        vertaccr_text = self.findChild(QPlainTextEdit,
                                       "fgdc_vertacc").toPlainText()
        if len(vertaccr_text) > 0:
            vertaccr.text = vertaccr_text
            vertacc.append(vertaccr)
            possacc.append(vertacc)
        return possacc

    def from_xml(self, positional_accuracy):
        """
        parses the xml code into the relevant possacc elements

        Parameters
        ----------
        postional_accuracy - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if positional_accuracy.tag == 'posacc':
                horizpa_text = positional_accuracy.findtext("horizpa/horizpar")
                horizpa_box = self.findChild(QPlainTextEdit, "fgdc_horizpa")
                horizpa_box.setPlainText(horizpa_text)

                vertacc_text = positional_accuracy.findtext("vertacc/vertaccr")
                vertacc_box = self.findChild(QPlainTextEdit, "fgdc_vertacc")
                vertacc_box.setPlainText(vertacc_text)
            else:
                print ("The tag is not possacc")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(PositionalAccuracy,
                        "Positional Accuracy testing")







