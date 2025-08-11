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
    from PyQt5.QtWidgets import QLineEdit
    from PyQt5.QtWidgets import QVBoxLayout
    from PyQt5.QtWidgets import QPlainTextEdit
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_ProcessStep
    from pymdwizard.gui.fgdc_date import FGDCDate
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.proccont import ProcessContact
except ImportError as err:
    raise ImportError(err, __file__)


class ProcessStep(WizardWidget):  #

    drag_label = "Process Step <procstep>"
    acceptable_tags = ["procstep"]

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

        self.single_date = FGDCDate(
            show_format=False, required=True, label="", fgdc_name="fgdc_procdate"
        )

        self.proccont = ProcessContact()

        self.ui.fgdc_procdate.setLayout(QVBoxLayout())
        self.ui.fgdc_procdate.layout().insertWidget(0, self.single_date)
        self.ui.widget_proccont.layout().insertWidget(0, self.proccont)

        self.srcused_list = RepeatingElement(
            add_text="Add another",
            remove_text="Remove last",
            widget_kwargs={"label": "Source used", "line_name": "fgdc_srcused"},
        )
        self.srcused_list.add_another()
        self.ui.srcused_groupbox.layout().addWidget(self.srcused_list)

        self.srcprod_list = RepeatingElement(
            add_text="Add another",
            remove_text="Remove last",
            widget_kwargs={"label": "Source produced:", "line_name": "fgdc_srcprod"},
        )
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
        procstep = xml_utils.xml_node(tag="procstep")
        procdesc = xml_utils.xml_node(tag="procdesc")
        procdesc.text = self.findChild(QPlainTextEdit, "fgdc_procdesc").toPlainText()
        procstep.append(procdesc)

        for srcused in self.srcused_list.get_widgets():
            if srcused.text():
                xml_utils.xml_node("srcused", text=srcused.text(), parent_node=procstep)

        procdate = xml_utils.xml_node(tag="procdate")
        date_var = self.single_date.findChild(QLineEdit, "fgdc_procdate").text()
        procdate.text = date_var
        procstep.append(procdate)

        for srcprod in self.srcprod_list.get_widgets():
            if srcprod.text():
                xml_utils.xml_node("srcprod", text=srcprod.text(), parent_node=procstep)

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
            if xml_processstep.tag == "procstep":
                utils.populate_widget(self, xml_processstep)
                if xml_processstep.xpath("procdate"):
                    self.single_date.set_date(xml_processstep.xpath("procdate")[0].text)

                if xml_processstep.xpath("proccont"):
                    self.proccont.ui.rbtn_yes.setChecked(True)
                    cntinfo_node = xml_processstep.xpath("proccont/cntinfo")[0]
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
    utils.launch_widget(ProcessStep, "Process Step testing")
