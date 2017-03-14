#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Metadata Date <timeperd> section
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
import os
from lxml import etree

import pandas as pd

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton, QInputDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QStackedWidget, QTabWidget, QDateEdit, QListWidget
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QGridLayout, QScrollArea, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QDate, QSettings

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import data_io

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_detailed
from pymdwizard.gui import attributes


class Detailed(WizardWidget):  #

    drag_label = "Detailed Description <detailed>"

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_detailed.Ui_Form()
        self.ui.setupUi(self)

        self.attributes = attributes.Attributes()
        self.ui.attribute_frame.layout().addWidget(self.attributes)

        self.setup_dragdrop(self)

        self.ui.btn_browse.clicked.connect(self.browse)

    def browse(self):
        settings = QSettings('USGS', 'pymdwizard')
        last_data_fname = settings.value('lastDataFname', '')
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(self, fname, dname)
        if fname[0]:
            settings.setValue('lastDataFname', fname[0])
            self.populate_from_fname(fname[0])

    def populate_from_fname(self, fname):
        shortname = os.path.split(fname)[1]

        ext = os.path.splitext(shortname)[1]
        if ext.lower() == '.csv':
            self.ui.fgdc_enttypl.setText(shortname)
            self.ui.fgdc_enttypd.setPlainText('Comma Separate Value (CSV) file containing data.')

            df = data_io.read_data(fname)
            self.attributes.load_df(df)
        elif ext.lower() == '.shp':
            self.ui.fgdc_enttypl.setText(shortname + ' Attribute Table')
            self.ui.fgdc_enttypd.setPlainText('Table containing attribute information associated with the data set.')

            df = data_io.read_data(fname)
            self.attributes.load_df(df)
        elif ext.lower() in ['.xlsm', '.xlsx', '.xls']:
            sheets = data_io.get_sheet_names(fname)

            sheet_name, ok = QInputDialog.getItem(self, "select sheet dialog",
                                "Pick one of the sheets from this workbook",
                                                  sheets, 0, False)
            if ok and sheet_name:
                self.ui.fgdc_enttypl.setText('{} ({})'.format(shortname, sheet_name))
                self.ui.fgdc_enttypd.setPlainText('Excel Worksheet')

                df = data_io.read_excel(fname, sheet_name)
                self.attributes.load_df(df)
        else:
            msg = "Can only read '.csv', '.shp', and Excel files here"
            QMessageBox.warning(self, "Unsupported file format", msg)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'timeperd'
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'detailed':
                e.accept()
        else:
            e.ignore()

    def clear_widget(self):
        """
        Clears all content from this widget

        Returns
        -------
        None
        """
        self.ui.fgdc_enttypl.setText('')
        self.ui.fgdc_enttypd.setPlainText('')
        self.attributes.clear_children()

    def has_content(self):
        """
        Checks for valid content in this widget

        Returns
        -------
        Boolean
        """
        has_content = False

        if self.ui.fgdc_enttypl.text():
            has_content = True
        if self.ui.fgdc_enttypd.toPlainText():
            has_content = True

        if len(self.attributes.attrs) > 0:
            has_content = True

        return has_content

    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        detailed = xml_utils.xml_node('detailed')
        enttyp = xml_utils.xml_node('enttyp', parent_node=detailed)
        enttypl = xml_utils.xml_node('enttypl', text=self.ui.fgdc_enttypl.text(), parent_node=enttyp)
        enttypd = xml_utils.xml_node('enttypd', text=self.ui.fgdc_enttypd.toPlainText(), parent_node=enttyp)
        enttypds = xml_utils.xml_node('enttyplds', text=self.ui.fgdc_enttypds.text(), parent_node=enttyp)

        attr = self.attributes._to_xml()
        for a in attr.xpath('attr'):
            detailed.append(a)
        return detailed

    def _from_xml(self, detailed):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if detailed.tag == 'detailed':
                utils.populate_widget(self, detailed)
                self.attributes._from_xml(detailed)
            else:
                print ("The tag is not a detailed")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Detailed,
                        "detailed testing")
