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
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_procstep
    from pymdwizard.gui.ProcessStep import ProcessStep
    from pymdwizard.gui.repeating_element import RepeatingElement
except ImportError as err:
    raise ImportError(err, __file__)


class ProcStep(WizardWidget):  #

    drag_label = "Process Step <procstep>"
    acceptable_tags = ["lineage"]

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

        self.proc_step = RepeatingElement(
            which="tab",
            tab_label="Step",
            add_text="Additional Step",
            widget=ProcessStep,
            remove_text="Remove Step",
            italic_text="Describe the methods performed to collect or generate the data.\n Provide as much detail as possible.",
        )

        self.proc_step.add_another()
        self.ui.widget_procstep.layout().addWidget(self.proc_step)

    def to_xml(self):
        """
        encapsulates the etree process step in an element tag

        Returns
        -------
        procstep portion of the lineageg element tag in xml tree
        """
        lineage = xml_utils.xml_node(tag="lineage")
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
            if xml_procstep.tag == "lineage":
                self.proc_step.clear_widgets(add_another=False)
                xml_procstep = xml_procstep.findall("procstep")
                if xml_procstep:
                    for procstep in xml_procstep:
                        procdesc_widget = self.proc_step.add_another()
                        procdesc_widget.from_xml(procstep)
                else:
                    self.proc_step.add_another()

        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(ProcStep, "Source Input testing")
