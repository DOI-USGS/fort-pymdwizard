#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for multiple instances widget


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

import sys

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_multiple_instances
from pymdwizard.gui.single_date import SingleDate


class Multi_Instance(QWidget):

    def __init__(self, xml=None, params={}, parent=None):
        QWidget.__init__(self, parent=parent)

        self.widget_instances = []

        self.build_ui()
        self.connect_events()

        self.params = params
        if self.params:
            self.load_params(self.params)
        self.add_another()

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_multiple_instances.Ui_Form()
        self.ui.setupUi(self)

        # self.ui.scrollArea.setLayout(QVBoxLayout(self))
        # self.ui.qlbl = QLabel(self)
        # self.ui.label.deleteLater()
        # self.ui.lineEdit.setText('this')

        # self.multi_instances = [self.ui.lineEdit, ]



        # self.ui.scrollAreaWidgetContents.setLayout(QVBoxLayout(self))
        # self.horiz = QHBoxLayout()
        # self.qlbl = QLabel('Orig', self)
        # self.first_line_edit = QLineEdit()
        # self.horiz.addWidget(self.qlbl)
        # self.horiz.addWidget(self.first_line_edit)
        # print self.first_line_edit
        # self.ui.scrollAreaWidgetContents.layout().addLayout(self.horiz)
        # self.multi_instances = [self.first_line_edit, ]
        # area = self.findChild(QScrollArea, "scrollArea")
        # vbar = area.verticalScrollBar()
        # vbar.setValue(vbar.maximum()+90)


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        #self.ui.lineEdit.editingFinished.connect(self.check_format)
        self.ui.addAnother.clicked.connect(self.add_another)
        self.ui.popOff.clicked.connect(self.pop_off)

    def load_params(self, params):
        if 'widget' in params.keys():
            self.widget = params['widget']
        else:
            self.widget = DefaultWidget
            # def widget_load_params(self):
            #     self.qlbl.setText(params['Label'])

            # self.widget.load_params = widget_load_params


        self.ui.QLabel_Title.setText(params['Title'])
        self.ui.QLabelItalic.setText(params['Italic Text'])
        self.ui.addAnother.setText(params['Add text'])
        self.ui.popOff.setText(params['Remove text'])


    def add_another(self):
        # if 'widget' in params.keys():
        #     self.widget = params['widget']
        # else:
        #     self.widget = DefaultWidget
        ###self.widget = DefaultWidget
        widget_instance = self.widget(label=self.params['Label'])
        self.ui.verticalLayout.insertWidget(len(self.ui.verticalLayout) - 1, widget_instance)

        self.widget_instances.append(widget_instance)

        area = self.findChild(QScrollArea, "scrollArea")
        vbar = area.verticalScrollBar()
        vbar.setValue(vbar.maximum()+90)



    def pop_off(self):
        last_added = self.widget_instances.pop()
        last_added.deleteLater()


class DefaultWidget(QWidget):

    def __init__(self, label='', parent=None):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.qlbl = QLabel(label, self)
        self.added_line = QLineEdit()
        self.layout.addWidget(self.qlbl)
        self.layout.addWidget(self.added_line)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.layout)

        # self.load_params()

    def load_params(self):
        pass

from pymdwizard.gui import single_date
class CoolSingleDate(single_date.SingleDate):

    def __init__(self, parent=None):

        single_date.SingleDate.__init__(self, parent=parent)
        self.ui.label.setText('testing')
        self.ui.lbl_format.deleteLater()

if __name__ == "__main__":

    #from pymdwizard.gui import  Citation

    # params = {'Title':'hello',
    #           'Italic Text':'world',
    #           'Label': 'This is a label',
    #           'Add text':'button add me',
    #           'Remove text': 'button eat me',
    #           'widget':Citation.Citation}





    utils.launch_widget(Multi_Instance, params=params)


