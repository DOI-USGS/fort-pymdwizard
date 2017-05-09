#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Overview frame for Process Step element


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

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint



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
        self.ui = UI_procstep.Ui_Form()#.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.proc_step = RepeatingElement(which='tab',
                         tab_label='Step', add_text='Additional Step',
                         widget=ProcessStep, remove_text='Remove Step', italic_text='Processing Steps Taken')

        #self.proc_step = RepeatingElement(params=params, which='tab', tab_label='Source',)
        self.proc_step.add_another()
        self.ui.widget_procstep.layout().addWidget(self.proc_step)
                
    def _to_xml(self):
        """
        encapsulates the etree process step in an element tag

        Returns
        -------
        procstep portion of the lineageg element tag in xml tree
        """
        lineage = etree.Element('lineage')
        procstep_list = self.proc_step.get_widgets()
        for procstep in procstep_list:
            lineage.append(procstep._to_xml())

        return lineage

    def _from_xml(self, xml_procstep):
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
                        procdesc_widget._from_xml(procstep)
                else:
                    self.proc_step.add_another()

        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(ProcStep,
                        "Source Input testing")

