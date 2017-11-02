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

from copy import deepcopy

from PyQt5.QtWidgets import QPlainTextEdit
from pymdwizard.core import xml_utils
from pymdwizard.core import utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_attracc


class AttributeAccuracy(WizardWidget):

    drag_label = "Attribute Accuracy <attracc>"
    acceptable_tags = ['attracc']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_attracc.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)
        self.ui.fgdc_attraccr.setFixedHeight(55)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        attraccr element tag in xml tree
        """
        attracc = xml_utils.xml_node(tag='attracc')
        attraccr_str = self.findChild(QPlainTextEdit,
                                      "fgdc_attraccr").toPlainText()
        attraccr = xml_utils.xml_node(tag='attraccr',
                                      text=attraccr_str,
                                      parent_node=attracc)

        if self.original_xml is not None:
            qattracc = xml_utils.search_xpath(self.original_xml, 'qattracc')
            if qattracc is not None:
                qattracc.tail = None
                attracc.append(deepcopy(qattracc))

        return attracc

    def from_xml(self, attribute_accuracy):
        """
        parses the xml code into the relevant attraccr elements

        Parameters
        ----------
        attribute_accuracy - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if attribute_accuracy.tag == 'attracc':
                self.original_xml = attribute_accuracy
                attraccr_text = attribute_accuracy.findtext("attraccr")
                accost_box = self.findChild(QPlainTextEdit, "fgdc_attraccr")
                accost_box.setPlainText(attraccr_text)
            else:
                print("The tag is not attracc")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(AttributeAccuracy,
                        "Attribute Accuracy testing")







