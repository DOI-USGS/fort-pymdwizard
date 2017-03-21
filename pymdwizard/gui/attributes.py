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
from pymdwizard.gui.ui_files import UI_attributes
from pymdwizard.gui import attr


class Attributes(WizardWidget):  #

    drag_label = "Attributes <attr>"

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_attributes.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.main_layout = self.ui.scrollAreaWidgetContents.layout()

        self.attrs = []


        import pandas as pd
        # df = pd.read_csv(r"C:\Users\talbertc\Downloads\Titanic.csv")
        # self.load_df(df)
        self.minimize_children()

    def load_df(self, df):
        self.clear_children()

        for col_label in df.columns:
            col = df[col_label]
            attr_i = attr.Attr(parent=self)
            attr_i.ui.fgdc_attrlabl.setText(col_label)

            attr_i.set_series(col)
            attr_i.guess_domain()

            self.attrs.append(attr_i)
            attr_i.regularsize_me()
            self.main_layout.insertWidget(len(self.main_layout) - 1, attr_i)

        self.attrs[0].supersize_me()

    def clear_children(self):

        for attribute in self.attrs:
            attribute.deleteLater()
        self.attrs = []

    def minimize_children(self):
        for attr_widget in self.attrs:
            attr_widget.regularsize_me()
            attr_widget.ui.fgdc_attrlabl.setCursorPosition(0)

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
        e.ignore()


    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        detailed = xml_utils.xml_node('detailed')
        for a in self.attrs:
            detailed.append(a._to_xml())

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
                self.clear_children()
                for attr_node in detailed.xpath('attr'):
                    attr_widget = attr.Attr(parent=self)
                    attr_widget._from_xml(attr_node)

                    self.attrs.append(attr_widget)
                    self.main_layout.insertWidget(len(self.main_layout) - 1, attr_widget)

                self.minimize_children()
                self.attrs[0].supersize_me()
            else:
                print ("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Attributes,
                        "attr_list testing")
