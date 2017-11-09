#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Access Constraints <useconst> section


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

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_useconst


class Useconst(WizardWidget): #

    drag_label = "Use Constraints <useconst>"
    acceptable_tags = ['abstract']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_useconst.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'useconst'
        Parameters
        ----------
        e : qt event

        Returns
        -------
        None

        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'useconst':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        useconst element tag in xml tree
        """
        useconst = xml_utils.xml_node('useconst',
                                      text=self.ui.fgdc_useconst.toPlainText())
        return useconst

    def _from_xml(self, useconst):
        """
        parses the xml code into the relevant useconst elements

        Parameters
        ----------
        use_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if useconst.tag == 'useconst':
                self.ui.fgdc_useconst.setPlainText(useconst.text)
            else:
                print ("The tag is not useconst")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Useconst,
                        "Use Constraints testing")

