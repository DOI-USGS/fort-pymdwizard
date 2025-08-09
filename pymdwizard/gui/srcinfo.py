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


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


NOTES
------------------------------------------------------------------------------
None
"""

from PyQt5.QtWidgets import QComboBox

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_srcinfo
from pymdwizard.gui.citeinfo import Citeinfo
from pymdwizard.gui.timeinfo import Timeinfo


class SRCInfo(WizardWidget):  #

    drag_label = "SRCInfo <srcinfo>"
    acceptable_tags = ["srcinfo"]

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_srcinfo.Ui_Form()
        self.ui.setupUi(self)
        self.timeinfo = Timeinfo()
        self.citation = Citeinfo(parent=self, include_lwork=False)

        self.ui.fgdc_srccite.layout().addWidget(self.citation)
        self.ui.fgdc_srctime.layout().insertWidget(0, self.timeinfo)

        self.setup_dragdrop(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.fgdc_srccitea.editingFinished.connect(self.update_tab_label)
        self.ui.fgdc_srcscale.editingFinished.connect(self.format_scale)

    def update_tab_label(self):
        new_label = "Source: {}".format(self.ui.fgdc_srccitea.text()[:15])
        tab_widget = self.ui.fgdc_srccitea.parent().parent().parent().parent()
        current_index = tab_widget.currentIndex()
        tab_widget.setTabText(current_index, new_label)

    def format_scale(self):
        cur_text = self.ui.fgdc_srcscale.text().replace(",", "")
        try:
            if "." in cur_text:
                formatted_text = "{:,}".format(float(cur_text))
            else:
                formatted_text = "{:,}".format(int(cur_text))
            self.ui.fgdc_srcscale.setText(formatted_text)
        except:
            pass

    def to_xml(self):
        """
        encapsulates the QLineEdit text in an element tag

        Returns
        -------
        srcinfo element tag in xml tree
        """
        srcinfo = xml_utils.xml_node("srcinfo")
        srccite = xml_utils.xml_node("srccite", parent_node=srcinfo)

        cite = self.citation.to_xml()
        srccite.append(cite)

        if self.ui.fgdc_srcscale.text():
            srcscale = xml_utils.xml_node(
                "srcscale",
                text=self.ui.fgdc_srcscale.text().replace(",", ""),
                parent_node=srcinfo,
            )

        typesrc = xml_utils.xml_node(
            "typesrc", text=self.ui.fgdc_typesrc.currentText(), parent_node=srcinfo
        )

        srctime = xml_utils.xml_node("srctime", parent_node=srcinfo)
        timeinfo = self.timeinfo.to_xml()
        srctime.append(timeinfo)

        srccurr = xml_utils.xml_node(
            "srccurr", text=self.ui.fgdc_srccurr.currentText(), parent_node=srctime
        )

        srccitea = xml_utils.xml_node(
            "srccitea", text=self.ui.fgdc_srccitea.text(), parent_node=srcinfo
        )

        srccontr = xml_utils.xml_node(
            "srccontr", text=self.ui.fgdc_srccontr.toPlainText(), parent_node=srcinfo
        )

        return srcinfo

    def from_xml(self, srcinfo):
        """
        parses the xml code into the relevant srcinfo elements

        Parameters
        ----------
        srcinfo - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if srcinfo.tag == "srcinfo":
                utils.populate_widget(self, srcinfo)
                srccite = srcinfo.xpath("srccite")[0]
                citeinfo = srccite.xpath("citeinfo")[0]
            elif srcinfo.tag != "srcinfo":
                print("The tag is not 'srcinfo'")
                return

            self.citation.from_xml(citeinfo)

            utils.populate_widget_element(self.ui.fgdc_srcscale, srcinfo, "srcscale")
            self.format_scale()

            typesrc = srcinfo.xpath("typesrc/text()")
            typesrc_text = str(typesrc[0])
            self.findChild(QComboBox, "fgdc_typesrc").setCurrentText(typesrc_text)

            utils.populate_widget_element(self.ui.fgdc_srccitea, srcinfo, "srccitea")
            utils.populate_widget_element(self.ui.fgdc_srccontr, srcinfo, "srccontr")

            if srcinfo.xpath("srctime"):
                timeinfo = srcinfo.xpath("srctime/timeinfo")[0]
                srccurr = srcinfo.xpath("srctime/srccurr")[0]
                self.timeinfo.from_xml(timeinfo)
                self.ui.fgdc_srccurr.setCurrentText(srccurr.text)

            self.update_tab_label()

        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(SRCInfo, "SRCInfo testing")
