#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Access Constraints <accconst> section


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

from lxml import etree

from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_accconst


class Accconst(WizardWidget): #

    drag_label = "Access Constraints <accconst>"
    acceptable_tags = ['accconst']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_accconst.Ui_Form()#.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def _to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        accconst element tag in xml tree
        """
        accconst = xml_utils.xml_node('accconst',
                                      text=self.ui.fgdc_accconst.toPlainText())
        return accconst

    def _from_xml(self, acconst):
        """
        parses the xml code into the relevant accconst elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if acconst.tag == 'accconst':
               self.ui.fgdc_accconst.setPlainText(acconst.text)
            else:
               print ("The tag is not accconst")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Accconst,
                        "Access Constraints testing")

