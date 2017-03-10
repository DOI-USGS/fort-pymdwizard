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

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QStackedWidget, QTabWidget, QDateEdit, QListWidget
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QGridLayout, QScrollArea
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QDate

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.ui_files import UI_timeperd #
from pymdwizard.gui.single_date import SingleDate


class Timeperd(WizardWidget):  #

    drag_label = "Time Period of Content <timeperd>"

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_timeperd.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.single_date = SingleDate(label='    Single Date ')
        self.ui.page_singledate.layout().insertWidget(0, self.single_date)

        self.range_start_date = SingleDate(label='Start  ')
        self.range_end_date = SingleDate(label='End  ')
        self.ui.layout_daterange.addWidget(self.range_end_date)
        self.ui.layout_daterange.addWidget(self.range_start_date)

        multidate_params = {'Add text': 'Add additional',
                            'Remove text': 'Remove last',
                            'widget': SingleDate,
                            'widget_kwargs': {'show_format': False,
                                              'label':'Individual Date   '}}
        self.multi_dates = RepeatingElement(params=multidate_params)
        self.multi_dates.add_another()
        # self.ui.layout_multipledates.addWidget(self.multi_dates)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions
        Returns
        -------
        None
        """
        self.ui.radioButton.toggled.connect(self.switch_primary)
        self.ui.radioButton_2.toggled.connect(self.switch_primary)
        self.ui.radioButton_3.toggled.connect(self.switch_primary)

    def switch_primary(self):
        """
        Switches form to reflect either organization or person primary
        Returns
        -------
        None
        """
        if self.ui.radioButton.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(0)
            self.ui.page_singledate.show()
            self.ui.page_daterange.hide()
            self.ui.page_multipledates.hide()
            self.ui.page_multipledates.layout().removeWidget(self.multi_dates)
        elif self.ui.radioButton_2.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(1)
            self.ui.page_singledate.hide()
            self.ui.page_daterange.show()
            self.ui.page_multipledates.hide()
            self.ui.page_multipledates.layout().removeWidget(self.multi_dates)
        elif self.ui.radioButton_3.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(2)
            self.ui.page_singledate.hide()
            self.ui.page_daterange.hide()
            self.ui.page_multipledates.layout().addWidget(self.multi_dates)
            self.ui.page_multipledates.show()

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
        print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'timeperd':
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        timeperd = etree.Element('timeperd')
        timeinfo = etree.Element("timeinfo")
        tabIndex = self.findChild(QStackedWidget, "fgdc_timeinfo").currentIndex()

        if tabIndex == 0:
            sngdate = etree.Element("sngdate")
            temp_var = self.single_date.findChild(QLineEdit, "lineEdit").text()
            sngdate.text = temp_var
            timeinfo.append(sngdate)
            timeperd.append(timeinfo)
        if tabIndex == 1:
            rngdates = etree.Element("rngdates")
            begdate = etree.Element("begdate")
            enddate = etree.Element("enddate")

            temp_var2 = self.range_date1.findChild(QLineEdit, "lineEdit").text()
            begdate.text = temp_var2
            temp_var3 = self.range_date2.findChild(QLineEdit, "lineEdit").text()
            enddate.text = temp_var3
            rngdates.append(begdate)
            rngdates.append(enddate)
            timeinfo.append(rngdates)
            timeperd.append(timeinfo)
        if tabIndex == 2:
            mdattim = etree.Element("mdattim")

            for index in self.multi_dates:
                rowEach = index.findChild(QLineEdit, "lineEdit").text()
                sngdate = etree.Element("sngdate")
                strEach = str(rowEach)

                sngdate.text = strEach
                mdattim.append(sngdate)
                timeinfo.append(mdattim)
                timeperd.append(timeinfo)


        current = etree.Element('current')
        current.text = self.findChild(QComboBox, 'fgdc_current').currentText()
        timeperd.append(current)

        return timeperd

    def _from_xml(self, metadata_date):
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
            if metadata_date.tag == 'timeperd':

                if metadata_date.findall("current"):
                    current_text = metadata_date.findtext("current")
                    current_box = self.findChild(QComboBox, 'fgdc_current')
                    current_box.setCurrentText(current_text)
                else:
                    pass

                tabIndex = self.findChild(QStackedWidget, "fgdc_timeinfo")
                print (tabIndex.currentIndex())
                if metadata_date.find("timeinfo/rngdates"):
                    self.ui.radioButton_2.setChecked(True)
                    tabIndex.setCurrentIndex(1)
                    begdate = metadata_date.findtext("timeinfo/rngdates/begdate")
                    enddate = metadata_date.findtext("timeinfo/rngdates/enddate")
                    date_edit2 = self.range_date1.findChild(QLineEdit, "lineEdit")
                    date_edit2.setText(begdate)
                    date_edit3 = self.range_date2.findChild(QLineEdit, "lineEdit")
                    date_edit3.setText(enddate)

                elif metadata_date.find("timeinfo/mdattim"):
                    self.ui.radioButton_3.setChecked(True)
                    tabIndex.setCurrentIndex(2)
                    listW = [b.text for b in metadata_date.iterfind(".//sngdate")]
                    lenLW = len(listW)
                    self.first_date.findChild(QLineEdit, "lineEdit").setText(listW[0])
                    cnt = 1
                    for lw in listW[1:]:
                        new_date = "new_date" + str(cnt)
                        new_date = SingleDate()

                        new_date.ui.lbl_format.deleteLater()
                        self.ui.sa_multi_dates_content.layout().insertWidget(cnt, new_date)
                        new_date.findChild(QLineEdit, "lineEdit").setText(listW[cnt])
                        cnt += 1


                elif metadata_date.find("timeinfo"):
                    self.ui.radioButton.setChecked(True)
                    tabIndex.setCurrentIndex(0)

                    sngdate = metadata_date.findtext("timeinfo/sngdate")
                    date_edit = self.single_date.findChild(QLineEdit, "lineEdit")
                    date_edit.setText(sngdate)
                else:
                    pass


            else:
                print ("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Timeperd,
                        "Metadata Date testing")
