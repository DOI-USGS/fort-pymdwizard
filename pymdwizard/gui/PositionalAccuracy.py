#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Positional Accuracy <possacc> section


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
from pymdwizard.gui.ui_files import UI_PositionalAccuracy #


class PositionalAccuracy(WizardWidget): #

    drag_label = "Positional Accuracy <possacc>"
    acceptable_tags = ['abstract']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_PositionalAccuracy.Ui_Form()#.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)



    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'possacc'
        Parameters
        ----------
        e : qt event

        Returns
        -------
        None

        """
        print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'posacc':
                e.accept()
        else:
            e.ignore()


         
                
    def _to_xml(self):
        """
        encapsulates the QPlainTextEdit text in an element tag

        Returns
        -------
        possacc element tag in xml tree
        """
        possacc = etree.Element('posacc')
        horizpa = etree.Element('horizpa')
        horizpar = etree.Element('horizpar')
        horizpar_text = self.findChild(QPlainTextEdit, "fgdc_horizpa").toPlainText()
        if len(horizpar_text) > 0:
            horizpar.text = horizpar_text
            horizpa.append(horizpar)
            possacc.append(horizpa)

        vertacc = etree.Element('vertacc')
        vertaccr = etree.Element('vertaccr')
        vertaccr_text = self.findChild(QPlainTextEdit, "fgdc_vertacc").toPlainText()
        if len(vertaccr_text) > 0:
            vertaccr.text = vertaccr_text
            vertacc.append(vertaccr)
            possacc.append(vertacc)
        return possacc

    def _from_xml(self, positional_accuracy):
        """
        parses the xml code into the relevant possacc elements

        Parameters
        ----------
        postional_accuracy - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if positional_accuracy.tag == 'posacc':
                horizpa_text = positional_accuracy.findtext("horizpa/horizpar")
                horizpa_box = self.findChild(QPlainTextEdit, "fgdc_horizpa")
                horizpa_box.setPlainText(horizpa_text)

                vertacc_text = positional_accuracy.findtext("vertacc/vertaccr")
                vertacc_box = self.findChild(QPlainTextEdit, "fgdc_vertacc")
                vertacc_box.setPlainText(vertacc_text)
            else:
                print ("The tag is not possacc")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(PositionalAccuracy,
                        "Positional Accuracy testing")

