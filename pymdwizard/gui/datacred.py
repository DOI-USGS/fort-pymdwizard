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

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_datacred


class Datacred(WizardWidget): #

    drag_label = "Data Credit <datacred>"
    acceptable_tags = ['datacred']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_datacred.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'datacred'
        Parameters
        ----------
        e : qt event

        Returns
        -------
        None

        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            element = xml_utils.string_to_node(mime_data.text())
            if element is not None and element.tag == 'datacred':
                e.accept()
        else:
            e.ignore()

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        datacred element tag in xml tree
        """
        datacred = xml_utils.xml_node('datacred',
                                                    text=self.ui.fgdc_datacred.toPlainText())
        return datacred

    def from_xml(self, data_credit):
        """
        parses the xml code into the relevant datacred elements

        Parameters
        ----------
        data_credit - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if data_credit.tag == 'datacred':
                self.ui.fgdc_datacred.setPlainText(data_credit.text)
            else:
               print ("The tag is not datacred")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Datacred,
                        "Data Credit testing")







