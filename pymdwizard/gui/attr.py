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
from pymdwizard.gui import udom, rdom, codesetd, edom_list


class Attr(WizardWidget):  #

    drag_label = "Attribute <attr>"

    def __init__(self, xml=None, parent=None):
        self.parent_ui = parent
        self.series = None
        WizardWidget.__init__(self, xml=xml, parent=parent)

        self._previous_index = -1
        self._domain_content = {'Range (Numeric data)': None,
                               'Enumerated (Categorical Data)': None,
                               'Unrepresentable (None of the above)': None,
                               'Codeset (Published Categories)': None}

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_attr.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        #

        self.ui.fgdc_attrlabl.installEventFilter(self)
        self.ui.fgdc_attrdef.installEventFilter(self)
        self.ui.fgdc_attrdef.setMouseTracking(True)
        self.ui.fgdc_attrdefs.installEventFilter(self)
        self.ui.fgdc_attrdomv.installEventFilter(self)
        self.ui.place_holder.installEventFilter(self)

        self.setup_dragdrop(self)
        self.ui.comboBox.currentIndexChanged.connect(self.change_domain)

    def clear_domain(self):
        for child in self.ui.fgdc_attrdomv.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def set_series(self, series):
        self.series = series

    def guess_domain(self):

        cbo = self.ui.comboBox

        if self.series is not None:
            uniques = self.series.unique()
            if len(uniques) < 15:
                self.enumerateds = []
                enumerated = edom_list.EdomList()
                enumerated.populate_from_list(uniques)

                self.domain = enumerated
                cbo.setCurrentIndex(0)

            elif self.series.dtype == np.float or \
                            self.series.dtype == np.int:
                self.domain = rdom.Rdom()
                self.domain.ui.fgdc_rdommin.setText(str(self.series.min()))
                self.domain.ui.fgdc_rdommax.setText(str(self.series.max()))
                cbo.setCurrentIndex(1)
            else:
                self.domain = udom.Udom()
                cbo.setCurrentIndex(3)

        self.ui.fgdc_attrdomv.layout().addWidget(self.domain)

    def change_domain(self, index):

        previous_domain = self.ui.comboBox.itemText(self._previous_index)
        self._domain_content[previous_domain] = self.domain._to_xml()

        self._previous_index = index
        self.clear_domain()

        domain = self.ui.comboBox.currentText().lower()
        if 'enumerated' in domain:
            self.domain = edom_list.EdomList(parent=self)
            if self._domain_content['Enumerated (Categorical Data)'] is not None:
                self.domain._from_xml(self._domain_content['Enumerated (Categorical Data)'])
            elif self.series is not None:
                uniques = self.series.unique()
                if len(uniques) > 100:
                    msg = "There are more than 100 unique values in this field."
                    msg += "\n This tool cannot smoothly display that many entries. "
                    msg += "\nTypically an enumerated domain is not used with that many unique entries."
                    msg += "\n\nOnly the first one hundred are displayed below!"
                    msg += "\nYou will likely want to change the domain to one of the other options."
                    QMessageBox.warning(self, "Too many unique entries", msg)
                    self.domain.populate_from_list(uniques[:101])
                else:
                    self.domain.populate_from_list(uniques)
        elif 'range' in domain:
            self.domain = rdom.Rdom(parent=self)
            if self._domain_content['Range (Numeric data)'] is not None:
                self.domain._from_xml(self._domain_content['Range (Numeric data)'])
            elif self.series is not None:
                try:
                    series_min = self.series.min()
                    series_max = self.series.max()
                except TypeError:
                    series_min = ''
                    series_max = ''

                self.domain.ui.fgdc_rdommin.setText(str(series_min))
                self.domain.ui.fgdc_rdommax.setText(str(series_max))
        elif 'codeset' in domain:
            self.domain = codesetd.Codesetd(parent=self)
            if self._domain_content['Codeset (Published Categories)'] is not None:
                self.domain._from_xml(self._domain_content['Codeset (Published Categories)'])
        elif 'unrepresentable' in domain:
            self.domain = udom.Udom(parent=self)
            if self._domain_content['Unrepresentable (None of the above)'] is not None:
                self.domain._from_xml(self._domain_content['Unrepresentable (None of the above)'])
        else:
            pass

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
            if element is not None and element.tag == 'attr':
                e.accept()
        else:
            e.ignore()

    def supersize_me(self, s=''):
        self.animation = QPropertyAnimation(self, b"minimumSize")
        self.animation.setDuration(400)
        self.animation.setEndValue(QSize(325, self.height()))
        self.animation.start()
        self.ui.fgdc_attrdomv.show()
        self.ui.place_holder.hide()


    def regularsize_me(self):
        self.animation = QPropertyAnimation(self, b"minimumSize")
        self.animation.setDuration(33)
        self.animation.setEndValue(QSize(100, self.height()))
        self.animation.start()
        self.ui.fgdc_attrdomv.hide()
        self.ui.place_holder.show()

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
        if event.type() == event.MouseButtonPress or \
                event.type() == 207:
            self.parent_ui.minimize_children()
            self.supersize_me()

        return super(Attr, self).eventFilter(obj, event)

    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        attr = xml_utils.xml_node('attr')
        if self.ui.comboBox.currentIndex() == 0:
            attr = self.domain._to_xml()
        else:
            attr = xml_utils.xml_node('attr')
            attrdomv = xml_utils.xml_node('attrdomv', parent_node=attr)
            domain_node = self.domain._to_xml()
            attrdomv.append(domain_node)

        attrlabl = xml_utils.xml_node('attrlabl',
                                      text=self.ui.fgdc_attrlabl.text(),
                                      parent_node=attr, index=0)
        attrdef = xml_utils.xml_node('attrdef',
                                     text=self.ui.fgdc_attrdef.toPlainText(),
                                     parent_node=attr, index=1)
        attrdefs = xml_utils.xml_node('attrdefs',
                                      text=self.ui.fgdc_attrdefs.text(),
                                      parent_node=attr, index=2)

        return attr

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

                utils.populate_widget(self, attr)
                attr_dict = xml_utils.node_to_dict(attr)

                if not 'fgdc_attrdomv' in attr_dict.keys():
                    self.ui.comboBox.setCurrentIndex(3)
                elif 'fgdc_udom' in attr_dict['fgdc_attrdomv'].keys():
                    self.ui.comboBox.setCurrentIndex(3)
                    self.domain._from_xml(attr.xpath('attrdomv/udom')[0])
                elif 'fgdc_rdom' in attr_dict['fgdc_attrdomv'].keys():
                    self.ui.comboBox.setCurrentIndex(1)
                    self.domain._from_xml(attr.xpath('attrdomv/rdom')[0])
                elif 'fgdc_edom' in attr_dict['fgdc_attrdomv'].keys():
                    self.ui.comboBox.setCurrentIndex(0)
                    self.change_domain(None)
                    self.domain._from_xml(attr)
                elif 'fgdc_codesetd' in attr_dict['fgdc_attrdomv'].keys():
                    self.ui.comboBox.setCurrentIndex(2)
                    self.domain._from_xml(attr.xpath('attrdomv/codesetd')[0])
                else:
                    self.ui.comboBox.setCurrentIndex(3)





            else:
                print ("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Attr,
                        "attr testing")
