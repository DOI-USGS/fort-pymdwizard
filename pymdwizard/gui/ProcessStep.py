#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Process Step <procstep> section


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
from pymdwizard.gui.ui_files import UI_ProcessStep
from pymdwizard.gui.fgdc_date import FGDCDate
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
        self.ui = UI_ProcessStep.Ui_Form()#.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.single_date = FGDCDate(show_format=False, required=True, label='', fgdc_name='fgdc_procdate')

        self.proccont = ProcessContact()

        self.ui.fgdc_procdate.setLayout(QVBoxLayout(self))
        self.ui.fgdc_procdate.layout().insertWidget(0, self.single_date)
        self.ui.widget_proccont.layout().insertWidget(0, self.proccont)

        self.clear_widget()

    def clear_widget(self):
        super(self.__class__, self).clear_widget()
        self.proccont.ui.rbtn_no.setChecked(True)

    def _to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        procstep element tag in xml tree
        """
        procstep = etree.Element('procstep')
        procdesc = etree.Element('procdesc')
        procdesc.text = self.findChild(QPlainTextEdit, "fgdc_procdesc").toPlainText()
        procstep.append(procdesc)

        srcused = etree.Element('srcused')
        srcused.text = self.findChild(QLineEdit, "fgdc_srcused").text()
        if len(srcused.text):
            procstep.append(srcused)

        procdate = etree.Element('procdate')
        date_var = self.single_date.findChild(QLineEdit, "fgdc_procdate").text()
        procdate.text = date_var
        procstep.append(procdate)

        srcprod = etree.Element('srcprod')
        srcprod.text = self.findChild(QLineEdit, "fgdc_srcprod").text()
        if len(srcprod.text):
            procstep.append(srcprod)

        if self.proccont.ui.rbtn_yes.isChecked():
            proccont = self.proccont._to_xml()
            procstep.append(proccont)

        return procstep

    def _from_xml(self, xml_processstep):
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
                else:
                    pass
                if xml_processstep.xpath('proccont'):
                    self.proccont.ui.rbtn_yes.setChecked(True)
                    cntinfo_node = xml_processstep.xpath('proccont/cntinfo')[0]
                    self.proccont._from_xml(cntinfo_node)
                else:
                    self.proccont.ui.rbtn_no.setChecked(True)
                    pass
            else:
                print ("The tag is not procstep")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(ProcessStep,
                        "Process Step testing")

