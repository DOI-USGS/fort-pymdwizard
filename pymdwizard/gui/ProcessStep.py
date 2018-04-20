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

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPlainTextEdit

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_ProcessStep
from pymdwizard.gui.fgdc_date import FGDCDate
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.proccont import ProcessContact


class ProcessStep(WizardWidget): #

    drag_label = "Process Step <procstep>"
    acceptable_tags = ['procstep']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_ProcessStep.Ui_Form()
        self.ui.setupUi(self)
        self.ui.fgdc_procdesc.heightMin = 150
        self.setup_dragdrop(self)

        self.single_date = FGDCDate(show_format=False, required=True, label='', fgdc_name='fgdc_procdate')

        self.proccont = ProcessContact()

        self.ui.fgdc_procdate.setLayout(QVBoxLayout())
        self.ui.fgdc_procdate.layout().insertWidget(0, self.single_date)
        self.ui.widget_proccont.layout().insertWidget(0, self.proccont)

        self.srcused_list = RepeatingElement(add_text='Add another',
                                            remove_text='Remove last',
                                            widget_kwargs={'label': 'Source used',
                                                           'line_name':'fgdc_srcused'})
        self.srcused_list.add_another()
        self.ui.srcused_groupbox.layout().addWidget(self.srcused_list)

        self.srcprod_list = RepeatingElement(add_text='Add another',
                                             remove_text='Remove last',
                                             widget_kwargs={'label': 'Source produced:',
                                                            'line_name':'fgdc_srcprod'})
        self.srcprod_list.add_another()
        self.ui.srcprod_groupbox.layout().addWidget(self.srcprod_list)


        self.clear_widget()

    def clear_widget(self):
        super(self.__class__, self).clear_widget()
        self.proccont.ui.rbtn_no.setChecked(True)

    def to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        procstep element tag in xml tree
        """
        procstep = xml_utils.xml_node(tag='procstep')
        procdesc = xml_utils.xml_node(tag='procdesc')
        procdesc.text = self.findChild(QPlainTextEdit, "fgdc_procdesc").toPlainText()
        procstep.append(procdesc)

        for srcused in self.srcused_list.get_widgets():
            if srcused.text():
                xml_utils.xml_node('srcused', text=srcused.text(),
                                   parent_node=procstep)

        procdate = xml_utils.xml_node(tag='procdate')
        date_var = self.single_date.findChild(QLineEdit, "fgdc_procdate").text()
        procdate.text = date_var
        procstep.append(procdate)

        for srcprod in self.srcprod_list.get_widgets():
            if srcprod.text():
                xml_utils.xml_node('srcprod', text=srcprod.text(),
                                   parent_node=procstep)

        if self.proccont.ui.rbtn_yes.isChecked():
            proccont = self.proccont.to_xml()
            procstep.append(proccont)

        return procstep

    def from_xml(self, xml_processstep):
        """
        parses the xml code into the relevant procstep elements

        Parameters
        ----------
        process_step - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if xml_processstep.tag == 'procstep':
                utils.populate_widget(self, xml_processstep)
                if xml_processstep.xpath('procdate'):
                    self.single_date.set_date(xml_processstep.xpath('procdate')[0].text)

                if xml_processstep.xpath('proccont'):
                    self.proccont.ui.rbtn_yes.setChecked(True)
                    cntinfo_node = xml_processstep.xpath('proccont/cntinfo')[0]
                    self.proccont.from_xml(cntinfo_node)
                else:
                    self.proccont.ui.rbtn_no.setChecked(True)
                    pass

                srcuseds = xml_processstep.findall("srcused")
                if srcuseds:
                    self.srcused_list.clear_widgets(add_another=False)
                    for srcused in srcuseds:
                        srcused_widget = self.srcused_list.add_another()
                        srcused_widget.setText(srcused.text)
                else:
                    self.srcused_list.clear_widgets(add_another=True)

                srcprods = xml_processstep.findall("srcprod")
                if srcprods:
                    self.srcprod_list.clear_widgets(add_another=False)
                    for srcprod in srcprods:
                        srcprod_widget = self.srcprod_list.add_another()
                        srcprod_widget.setText(srcprod.text)
                else:
                    self.srcprod_list.clear_widgets(add_another=True)

            else:
                print("The tag is not procstep")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(ProcessStep,
                        "Process Step testing")







