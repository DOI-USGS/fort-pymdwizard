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

import numpy as np
import pandas as pd

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QStackedWidget, QTabWidget, QDateEdit, QListWidget
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QGridLayout, QScrollArea
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, QDate, QPropertyAnimation

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_attr
from pymdwizard.gui import udom, edom, rdom, codesetd


class Attr(WizardWidget):  #

    drag_label = "Attribute <attr>"

    def __init__(self, xml=None, parent=None):
        self.parent_ui = parent
        self.series = None
        WizardWidget.__init__(self, xml=xml, parent=parent)

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_attr.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.ui.fgdc_attrlabl.installEventFilter(self)
        self.ui.fgdc_attrdef.installEventFilter(self)
        self.ui.fgdc_attrdefs.installEventFilter(self)
        self.ui.fgdc_attrdomv.installEventFilter(self)
        # self.ui.comboBox.installEventFilter(self)

        self.ui.comboBox.currentIndexChanged.connect(self.change_domain)

    def clear_domain(self):
        for child in self.ui.fgdc_attrdomv.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def set_series(self, series):
        self.series = series

    def guess_domain(self):
        if self.series is not None:
            if self.series.dtype == np.float:
                min = self.series.min()
                max = self.series.max()
                self.domain = rdom.Rdom()
                self.domain.ui.fgdc_rdommin.setText(str(min))
                self.domain.ui.fgdc_rdommax.setText(str(max))
            elif self.series.dtype == np.object or \
                 self.series.dtype == np.int:
                uniques = self.series.unique()
                if len(uniques) < 15:
                    self.enumerateds = []
                    for unique in uniques:
                        enumerated = edom.Edom()
                        enumerated.ui.fgdc_edomv.setText(str(unique))
                        self.enumerateds.append(enumerated)
                        self.ui.fgdc_attrdomv.layout().addWidget(enumerated)
                    self.domain = edom.Edom()
                else:
                    self.domain = udom.Udom()
            else:
                self.domain = udom.Udom()

        self.ui.fgdc_attrdomv.layout().addWidget(self.domain)
    # def change_domain(self, which):

    # def to_range_domain(self):
    #     if self.series

    def change_domain(self, e):

        self.clear_domain()

        domain = self.ui.comboBox.currentText().lower()
        if 'enumerated' in domain:
            self.domain = edom.Edom()
        elif 'range' in domain:
            self.domain = rdom.Rdom()
        elif 'codeset' in domain:
            self.domain = codesetd.Codesetd()
        elif 'unrepresentable' in domain:
            self.domain = udom.Udom()

        self.ui.fgdc_attrdomv.layout().addWidget(self.domain)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'timeperd'
        Parameters
        ----------
        e : qt eventr
        Returns
        -------
        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'attr':
                e.accept()
        else:
            e.ignore()

    def supersize_me(self, s=''):
        self.animation = QPropertyAnimation(self, b"minimumSize")
        self.animation.setDuration(300)
        self.animation.setEndValue(QSize(300, self.height()))
        self.animation.start()


    def regularsize_me(self):
        self.animation = QPropertyAnimation(self, b"minimumSize")
        self.animation.setDuration(33)
        self.animation.setEndValue(QSize(100, self.height()))
        self.animation.start()

    def eventFilter(self, obj, event):
        """

        Parameters
        ----------
        obj
        event

        Returns
        -------

        """
        # you could be doing different groups of actions
        # for different types of widgets and either filtering
        # the event or not.
        # Here we just check if its one of the layout widget
        print(event.type())
        if event.type() == event.MouseButtonPress:
            self.parent_ui.minimize_children()
            self.supersize_me()

        return super(Attr, self).eventFilter(obj, event)

    def enterEvent(self, QEvent):
        pass
        # self.parent_ui.minimize_children()
        # self.supersize_me()


    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        udom = xml_utils.xml_node('attr')

        return udom

    def _from_xml(self, attr):
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
            if attr.tag == 'attr':
                pass
                # self.ui.fgdc_udom.setText(udom.text)
            else:
                print ("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Attr,
                        "attr testing")
