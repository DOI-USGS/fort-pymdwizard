#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Status <status> section
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
from pymdwizard.gui.ui_files import UI_Status  #


class Status(WizardWidget):  #

    drag_label = "Status <status>"
    acceptable_tags = ['abstract']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_Status.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'status'
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        #print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'status':
                #                print "element", element.text
                #                print "tag", element.tag
                # mime_data.setText(element.text)
                # print mime_data.text()
                # self.Q.setPlainText(_translate("Form", element.text))
                e.accept()
        else:
            e.ignore()

    def _to_xml(self):
        """
        encapsulates the two QComboBox's text into two separate element tags

        Returns
        -------
        status element tag in xml tree
        """
        status = etree.Element('status')
        progress = etree.Element('progress')
        #print "progress", type(progress)
        progress.text = self.findChild(QComboBox, 'fgdc_progress').currentText()
        #print progress.text
        status.append(progress)
        update = etree.Element('update')
        update.text = self.findChild(QComboBox, 'fgdc_update').currentText()
        status.append(update)

        # useconst.text = self.findChild(QPlainTextEdit, "useconst").toPlainText()
        #print "ok"

        return status

    def _from_xml(self, status):
        """
        parses the xml code into the relevant status elements

        Parameters
        ----------
        status - the xml element status and its contents

        Returns
        -------
        None
        """
        #print "Status", status.tag
        #print "text", status.find('progress').text
        try:
            if status.tag == 'status':
                progress_box = self.findChild(QComboBox, 'fgdc_progress')
                progress_text = status.find('progress').text
                #print progress_text
                progress_box.setCurrentText(progress_text)
                update_box = self.findChild(QComboBox, 'fgdc_update')
                update_text = status.find('update').text
                #print update_text
                update_box.setCurrentText(update_text)
            else:
                print ("The tag is not status")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Status,
                        "Status testing")
