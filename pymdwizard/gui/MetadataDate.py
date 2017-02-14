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
from pymdwizard.gui.ui_files import UI_MetadataDate #
from pymdwizard.gui.single_date import SingleDate

class MetadataDate(WizardWidget): #

    drag_label = "Metadata Date <timeperd>"


    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_MetadataDate.Ui_Form()#.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.first_date = SingleDate()
        self.first_date.ui.lbl_format.deleteLater()
        self.range_date1 = SingleDate()
        self.range_date1.ui.lbl_format.deleteLater()
        self.range_date2 = SingleDate()
        self.range_date2.ui.lbl_format.deleteLater()
        self.single_date = SingleDate()
        self.single_date.ui.lbl_format.deleteLater()
        self.ui.single_date_content.setLayout(QVBoxLayout(self))
        self.ui.single_date_content.layout().insertWidget(0, self.single_date)
        self.multi_dates = [self.first_date, ]
        self.ui.sa_multi_dates_content.layout().insertWidget(0, self.first_date)
        self.ui.range_date_content_1.setLayout(QVBoxLayout(self))
        self.ui.range_date_content_1.layout().insertWidget(0, self.range_date1)
        self.ui.range_date_content_2.setLayout(QVBoxLayout(self))
        self.ui.range_date_content_2.layout().insertWidget(0, self.range_date2)


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_clicked)
        self.ui.radioButton.toggled.connect(self.switch_primary)
        self.ui.radioButton_2.toggled.connect(self.switch_primary)
        self.ui.radioButton_3.toggled.connect(self.switch_primary)
        #self.ui.dateEdit0.dateChanged.connect(self.onDateChanged)

    # def onDateChanged(self, newDate):
    #     newDate = newDate.toString('yyyyMMdd')
    #     print("The new date is " + newDate)
    #     self.findChild(QLineEdit, "dateEdit").setText(newDate)

    def pushButton_clicked(self):
        new_date = SingleDate()
        new_date.ui.lbl_format.deleteLater()

        self.ui.sa_multi_dates_content.layout().insertWidget(len(self.multi_dates), new_date)
        self.multi_dates.append(new_date)
        area = self.findChild(QScrollArea, "SA_multi_dates")
        vbar = area.verticalScrollBar()
        vbar.setValue(vbar.maximum()+90)

        # temp_var0 = self.findChild(QLineEdit, "dateEdit_4").text()
        # #var_name0 = temp_var0.toPyDate()
        # #print var_name0
        # listV = self.findChild(QListWidget, "listWidget")
        # listV.addItem(temp_var0)

    def pushButton2_clicked(self):
        last_date = self.multi_dates.pop()
        last_date.deleteLater()
        # temp_var00 = self.findChild(QListWidget, "listWidget")
        # temp_var01 = temp_var00.currentRow()
        # temp_var00.takeItem(temp_var01)

    def switch_primary(self):
        """
        Switches form to reflect either organization or person primary

        Returns
        -------
        None
        """
        if self.ui.radioButton.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(0)
        elif self.ui.radioButton_2.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(1)
        elif self.ui.radioButton_3.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(2)




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
#                print "element", element.text
#                print "tag", element.tag
                #mime_data.setText(element.text)
                #print mime_data.text()
                #self.Q.setPlainText(_translate("Form", element.text))
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
        #print tabIndex

        if tabIndex == 0:
            #print ("0")
            sngdate = etree.Element("sngdate")
            # abstract = etree.Element("abstract")
            # abstract.text = self.findChild(QPlainTextEdit, "fgdc_abstract").toPlainText()
            # descript.append(abstract)
            #temp_var = self.findChild(QLineEdit, "dateEdit").text()
            # var_name = temp_var.toPyDate()
            # var_name = str(var_name)
            temp_var = self.single_date.findChild(QLineEdit, "lineEdit").text()
            #print temp_var
            sngdate.text = temp_var #var_name.replace('-', '')
            timeinfo.append(sngdate)
            timeperd.append(timeinfo)
        if tabIndex == 1:
            #print ("1")
            rngdates = etree.Element("rngdates")
            begdate = etree.Element("begdate")
            enddate = etree.Element("enddate")
            # abstract.text = self.findChild(QPlainTextEdit, "fgdc_abstract").toPlainText()
            # descript.append(abstract)
            #temp_var2 = self.findChild(QLineEdit, "dateEdit_2").text()
            # var_name2 = temp_var2.toPyDate()
            # var_name2 = str(var_name2)
            temp_var2 = self.range_date1.findChild(QLineEdit, "lineEdit").text()
            begdate.text = temp_var2 #var_name2.replace('-', '')
            #temp_var3 = self.findChild(QLineEdit, "dateEdit_3").text()
            # var_name3 = temp_var3.toPyDate()
            # var_name3 = str(var_name3)
            temp_var3 = self.range_date2.findChild(QLineEdit, "lineEdit").text()
            enddate.text = temp_var3 #.replace('-', '')
            rngdates.append(begdate)
            rngdates.append(enddate)
            timeinfo.append(rngdates)
            #print var_name3
            timeperd.append(timeinfo)
        if tabIndex == 2:
            #print ("2")
            mdattim = etree.Element("mdattim")
            #sngdate = etree.Element("sngdate")
            # items = []
            # for index in xrange(self.findChild(QListWidget, "listWidget").count()):
            #     items.append(self.findChild(QListWidget, "listWidget").item(index))
            # labels = [i.text() for i in items]
            #for index in xrange(self.findChild(QListWidget, "listWidget").count()):

            for index in self.multi_dates:
                rowEach = index.findChild(QLineEdit, "lineEdit").text()
                sngdate = etree.Element("sngdate")
                #rowEach = self.multi_dates(index).text()
                strEach = str(rowEach)
                #print strEach
                #strSimple = strEach.replace("-", '')

                sngdate.text = strEach
                mdattim.append(sngdate)
            #labels = [i.text() for i in items]
           # print labels
            #abstract.text = str(labels)
                timeinfo.append(mdattim)
                timeperd.append(timeinfo)


        #timeperd.append(timeinfo)

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
                    #date_edit2 = self.findChild(QLineEdit, "dateEdit_2")
                    date_edit2 = self.range_date1.findChild(QLineEdit, "lineEdit")
                    date_edit2.setText(begdate)
                    #date_edit3 = self.findChild(QLineEdit, "dateEdit_3")
                    date_edit3 = self.range_date2.findChild(QLineEdit, "lineEdit")
                    date_edit3.setText(enddate)

                elif metadata_date.find("timeinfo/mdattim"):
                    self.ui.radioButton_3.setChecked(True)
                    tabIndex.setCurrentIndex(2)
                    listW = [b.text for b in metadata_date.iterfind(".//sngdate")]
                    lenLW = len(listW)
                    #print lenLW
                    self.first_date.findChild(QLineEdit, "lineEdit").setText(listW[0])
                    # new_date = SingleDate()
                    # new_date.ui.lbl_format.deleteLater()
                    #qListW = self.findChild(QListWidget, "listWidget")
                    cnt = 1
                    for lw in listW[1:]:
                        #print "here", type(lw)
                        new_date = "new_date" + str(cnt)
                        #print new_date
                        new_date = SingleDate()

                        new_date.ui.lbl_format.deleteLater()
                        #print new_date
                        self.ui.sa_multi_dates_content.layout().insertWidget(cnt, new_date)
                        #self.multi_dates.append(new_date)
                        new_date.findChild(QLineEdit, "lineEdit").setText(listW[cnt])
                        #print cnt
                        cnt +=1
                        #qListW.addItem(lw)


                elif metadata_date.find("timeinfo"):
                    self.ui.radioButton.setChecked(True)
                    tabIndex.setCurrentIndex(0)

                    sngdate = metadata_date.findtext("timeinfo/sngdate")
                    #date_edit = self.findChild(QLineEdit, "dateEdit")
                    date_edit = self.single_date.findChild(QLineEdit, "lineEdit")
                    date_edit.setText(sngdate)
                else:
                    pass

                # for child in metadata_date:
                #     print child.tag, '- ', child.text

            else:
                print ("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(MetadataDate,
                        "Metadata Date testing")

