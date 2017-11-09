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
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QListWidgetItem
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, Qt
from PyQt5 import QtCore

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_repeating_element
from pymdwizard.gui.fgdc_date import FGDCDate
from pymdwizard.gui.wiz_widget import WizardWidget

class DefaultWidget(QWidget):
    """
    The default widget for a repeating element
    a simple line edit with a label and an option required astrix
    """
    def __init__(self, label='', line_name='na', required=False,
                 parent=None):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.qlbl = QLabel(label, self)
        self.added_line = QLineEdit()
        self.added_line.setObjectName(line_name)
        self.layout.addWidget(self.qlbl)
        self.layout.addWidget(self.added_line)

        if required:
            self.required_label = QLabel(self)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(9)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            self.required_label.setFont(font)
            self.required_label.setScaledContents(True)
            self.required_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.required_label.setIndent(0)

            self.required_label.setText(QtCore.QCoreApplication.translate("USGSContactInfoWidget", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; color:#55aaff;\">*</span></p></body></html>"))
            self.layout.addWidget(self.required_label)


        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(6)
        self.setLayout(self.layout)

    def setText(self, text):
        self.added_line.setText(text)

    def text(self):
        return self.added_line.text()


class RepeatingElement(QWidget):

    default_params = {'Title': 'insert title here',
                       'Italic Text': 'add notes here',
                       'Add text': 'button add me',
                       'Remove text': 'button del me',
                       'widget': DefaultWidget,
                       'widget_kwargs': {'label': 'add a text label'}}

    def __init__(self, which='vertical', tab_label='tab',
                 widget=DefaultWidget, widget_kwargs={},
                 italic_text='',
                 add_text="Add another", remove_text="Remove last",
                 show_buttons=True, add_another=None, parent=None):
        QWidget.__init__(self, parent=parent)

        self.widgets = []

        self.build_ui()

        if italic_text:
            self.ui.italic_label.setText(italic_text)

        self.which = which
        if which == 'vertical':
            self.SA = self.ui.vertical_widget
            self.content_layout = self.ui.vertical_widget.layout()
            self.tab = False
            self.ui.tab_widget.deleteLater()
        elif which == 'tab':
            self.content_widget = self.ui.tab_widget
            self.tab = True
            self.ui.vertical_widget.deleteLater()

        self.tab_label = tab_label

        if add_another is not None:
            self.add_another = add_another

        self.connect_events()

        if not show_buttons:
            self.ui.button_widget.hide()

        self.ui.addAnother.setText(add_text)
        self.ui.popOff.setText(remove_text)

        self.widget = widget
        self.widget_kwargs = widget_kwargs
        self.widget_kwargs['parent'] = self

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_repeating_element.Ui_Form()
        self.ui.setupUi(self)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.addAnother.clicked.connect(self.add_another)
        self.ui.popOff.clicked.connect(self.pop_off)


    def add_another(self, clicked=None, tab_label=''):
        """
        Adds another instance of a widget or ____

        Returns
        -------

        """
        widget = self.widget(**self.widget_kwargs)
        self.widgets.append(widget)

        if self.tab:
            if not tab_label:
                tab_label = ' '.join([self.tab_label,
                                      str(len(self.widgets))])
            self.ui.tab_widget.addTab(widget, tab_label)
            self.ui.tab_widget.setCurrentIndex(self.ui.tab_widget.count()-1)
        else:
            self.content_layout.insertWidget(len(self.widgets)-1, widget)
        return widget

    def pop_off(self):
        if self.widgets and len(self.widgets) > 1:
            if self.which == 'tab':
                current_tab = self.ui.tab_widget.currentIndex()
                current_widget = self.widgets[current_tab]
                current_widget.deleteLater()
                del self.widgets[current_tab]
            else:
                last_added = self.widgets.pop()
                last_added.deleteLater()
        elif len(self.widgets) == 1:
            self.clear_widgets()

    def get_widgets(self):
        return self.widgets

    def clear_widgets(self, add_another=True):
        for widget in self.widgets:
            widget.deleteLater()
        self.widgets = []

        if add_another:
            self.add_another()




if __name__ == "__main__":

    from pymdwizard.gui import attr, edom, fgdc_date, sourceinput
    import random

    widget_kws={'label' : 'hello', 'required' : True}


    utils.launch_widget(RepeatingElement, which='vertical',
                        tab_label='Processing Step', add_text='test add',
                        # widget = sourceinput.SourceInput,
                        widget_kwargs=widget_kws,
                        remove_text='test remove', italic_text='some instruction')



