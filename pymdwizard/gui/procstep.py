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
from pymdwizard.gui.ui_files import UI_procstep
from pymdwizard.gui.ProcessStep import ProcessStep
from pymdwizard.gui.repeating_element import RepeatingElement


class ProcStep(WizardWidget): #

    drag_label = "Process Step <procstep>"
    acceptable_tags = ['lineage']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_procstep.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.proc_step = RepeatingElement(which='tab',
                         tab_label='Step', add_text='Additional Step',
                         widget=ProcessStep, remove_text='Remove Step', italic_text='Describe the methods performed to collect or generate the data.\n Provide as much detail as possible.')

        self.proc_step.add_another()
        self.ui.widget_procstep.layout().addWidget(self.proc_step)
                
    def to_xml(self):
        """
        encapsulates the etree process step in an element tag

        Returns
        -------
        procstep portion of the lineageg element tag in xml tree
        """
        lineage = xml_utils.xml_node(tag='lineage')
        procstep_list = self.proc_step.get_widgets()
        for procstep in procstep_list:
            lineage.append(procstep.to_xml())

        return lineage

    def from_xml(self, xml_procstep):
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
            if xml_procstep.tag == 'lineage':
                self.proc_step.clear_widgets(add_another=False)
                xml_procstep = xml_procstep.findall('procstep')
                if xml_procstep:
                    for procstep in xml_procstep:
                        procdesc_widget = self.proc_step.add_another()
                        procdesc_widget.from_xml(procstep)
                else:
                    self.proc_step.add_another()

        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(ProcStep,
                        "Source Input testing")







