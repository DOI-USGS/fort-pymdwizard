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


        date_widget_kwargs = {'show_format': False,
                              'label':'Individual Date   '}

        self.multi_dates = RepeatingElement(widget=SingleDate,
                                            widget_kwargs=date_widget_kwargs)


        self.multi_dates.add_another()


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions
        Returns
        -------
        None
        """
        self.ui.radio_single.toggled.connect(self.switch_primary)
        self.ui.radio_range.toggled.connect(self.switch_primary)
        self.ui.radio_multiple.toggled.connect(self.switch_primary)

    def switch_primary(self):
        """
        Switches form to reflect either organization or person primary
        Returns
        -------
        None
        """
        if self.ui.radio_single.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(0)
            self.ui.page_singledate.show()
            self.ui.page_daterange.hide()
            self.ui.page_multipledates.hide()
            self.ui.page_multipledates.layout().removeWidget(self.multi_dates)
        elif self.ui.radio_range.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(1)
            self.ui.page_singledate.hide()
            self.ui.page_daterange.show()
            self.ui.page_multipledates.hide()
            self.ui.page_multipledates.layout().removeWidget(self.multi_dates)
        elif self.ui.radio_multiple.isChecked():
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
        timeperd = xml_utils.xml_node('timeperd')
        timeinfo = xml_utils.xml_node("timeinfo", parent_node=timeperd)
        tabIndex = self.ui.fgdc_timeinfo.currentIndex()

        if tabIndex == 0:
            sngdate = xml_utils.xml_node("sngdate", parent_node=timeinfo)
            caldate = xml_utils.xml_node('caldate', parent_node=sngdate,
                                         text=self.single_date.get_date())
        if tabIndex == 1:
            rngdates = xml_utils.xml_node("rngdates", parent_node=timeinfo)
            begdate = xml_utils.xml_node("begdate", parent_node=rngdates,
                                         text=self.range_start_date.get_date())
            enddate = xml_utils.xml_node("enddate", parent_node=rngdates,
                                         text=self.range_end_date.get_date())
        if tabIndex == 2:
            mdattim = xml_utils.xml_node("mdattim", parent_node=timeinfo)

            for single_date in self.multi_dates.get_widgets():
                single_date_node = xml_utils.xml_node('caldate', parent_node=mdattim,
                                                      text=single_date.get_date())

        current = xml_utils.xml_node('current', parent_node=timeperd,
                                     text= self.ui.fgdc_current.currentText())

        return timeperd

    def _from_xml(self, timeperd):
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
            if timeperd.tag == 'timeperd':

                if timeperd.findall("current"):
                    current_text = timeperd.findtext("current")
                    current_box = self.findChild(QComboBox, 'fgdc_current')
                    current_box.setCurrentText(current_text)
                else:
                    pass

                timeinfo_stack = self.ui.fgdc_timeinfo
                if timeperd.find("timeinfo/rngdates"):
                    self.ui.radio_range.setChecked(True)
                    timeinfo_stack.setCurrentIndex(1)

                    begdate = timeperd.findtext("timeinfo/rngdates/begdate")
                    self.range_start_date.set_date(begdate)

                    enddate = timeperd.findtext("timeinfo/rngdates/enddate")
                    self.range_end_date.set_date(enddate)

                    # utils.populate_widget_element(self.range_start_date,
                    #                               timeperd, "timeinfo/rngdates/begdate")
                    # utils.populate_widget_element(self.range_end_date,
                    #                               timeperd, "timeinfo/rngdates/enddate")

                elif timeperd.find("timeinfo/mdattim"):
                    self.ui.radio_multiple.setChecked(True)
                    timeinfo_stack.setCurrentIndex(2)

                    self.multi_dates.clear_widgets()
                    for caldate in timeperd.xpath('timeinfo/mdattim/caldate'):
                        date_widget = self.multi_dates.add_another()
                        date_widget.set_date(caldate.text)

                elif timeperd.find("timeinfo/sngdate"):
                    self.ui.radio_single.setChecked(True)
                    timeinfo_stack.setCurrentIndex(0)

                    sngdate = timeperd.findtext("timeinfo/sngdate/caldate")
                    self.single_date.set_date(sngdate)
                else:
                    pass


            else:
                print ("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Timeperd,
                        "Metadata Date testing")
