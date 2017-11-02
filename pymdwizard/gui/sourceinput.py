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
from pymdwizard.gui.ui_files import UI_sourceinput
from pymdwizard.gui.srcinfo import SRCInfo
from pymdwizard.gui.repeating_element import RepeatingElement


class SourceInput(WizardWidget):

    drag_label = "Source Information <srcinfo>"
    acceptable_tags = ['lineage']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_sourceinput.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.src_info = RepeatingElement(which='tab',
                        tab_label='Source', add_text='Add Source',
                        widget=SRCInfo, remove_text='Remove Source', italic_text='Source')

        self.src_info.add_another()
        self.ui.frame_sourceinfo.layout().addWidget(self.src_info)

        self.ui.frame_sourceinfo.hide()

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.radio_sourceyes.toggled.connect(self.include_sources_change)

    def include_sources_change(self, b):
        """
        Extended citation to support a larger body of information for the record.

        Parameters
        ----------
        b: qt event

        Returns
        -------
        None
        """
        if b:
            self.ui.frame_sourceinfo.show()
        else:
            self.ui.frame_sourceinfo.hide()

    def clear_widget(self):
        self.ui.radio_sourceno_2.setChecked(True)
        WizardWidget.clear_widget(self)

    def to_xml(self):
        """
        encapsulates the text in an element tree representing Sources Input

        Returns
        -------
        series of srcinfo element tag in lineage xml tree
        """
        lineage = xml_utils.xml_node(tag='lineage')
        if self.ui.radio_sourceyes.isChecked():
            cnt = 0
            srcinfo_list = self.src_info.get_widgets()
            for srcinfo in srcinfo_list:
                lineage.append(srcinfo.to_xml())
        return lineage


    def from_xml(self, xml_srcinput):
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
            if xml_srcinput.tag == 'lineage':
                self.src_info.clear_widgets(add_another=False)
                self.ui.frame_sourceinfo.show()
                self.ui.radio_sourceyes.setChecked(True)
                xml_srcinput = xml_srcinput.findall('srcinfo')
                if xml_srcinput:
                    for srcinput in xml_srcinput:
                        srcinfo_widget = self.src_info.add_another()
                        srcinfo_widget.from_xml(srcinput)

                else:
                    self.ui.radio_sourceno_2.setChecked(True)
                    self.src_info.add_another()
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(SourceInput,
                        "Source Input testing")







