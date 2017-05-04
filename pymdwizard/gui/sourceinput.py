#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Overview frame for SourceInfo element


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
from pymdwizard.gui.ui_files import UI_sourceinput
from pymdwizard.gui.SRCInfo import SRCInfo
from pymdwizard.gui.repeating_element import RepeatingElement


class SourceInput(WizardWidget):

    drag_label = "Source Information <srcinfo>"
    acceptable_tags = ['abstract']

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
                        tab_label='Source', add_text='Source Input',
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

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'accconst'
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
            if element is not None and element.tag == 'lineage':
                e.accept()
        else:
            e.ignore()

    def clear_widget(self):
        self.ui.radio_sourceno_2.setChecked(True)
        WizardWidget.clear_widget(self)
         

    def _to_xml(self):
        """
        encapsulates the text in an element tree representing Sources Input

        Returns
        -------
        series of srcinfo element tag in lineage xml tree
        """
        lineage = etree.Element('lineage')
        if self.ui.radio_sourceyes.isChecked():
            print ("in to xml")
            cnt = 0
            srcinfo_list = self.src_info.get_widgets()
            for srcinfo in srcinfo_list:
                lineage.append(srcinfo._to_xml())
            # while cnt < len(list_widgets):
            #     #lineage.append(list_widgets[cnt]._to_xml())
            #     lineage.append(SRCInfo._to_xml(list_widgets[cnt]))
            #     cnt += 1
        return lineage
        # elif self.ui.radio_sourceno.isChecked():
        #     pass


    def _from_xml(self, xml_srcinput):
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
                        srcinfo_widget._from_xml(srcinput)

                else:
                    self.ui.radio_sourceno_2.setChecked(True)
                    self.src_info.add_another()
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(SourceInput,
                        "Source Input testing")

