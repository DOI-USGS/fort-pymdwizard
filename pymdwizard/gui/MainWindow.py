#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt application for the main pymdwizard application


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


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QTableView
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QFileDialog
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint
from PyQt5.QtCore import Qt, QMimeData, QObject, QTimeLine
from PyQt5.QtGui import QPainter, QFont, QFontMetrics, QPalette, QBrush, QColor, QPixmap, QDrag


from pymdwizard.gui.ui_files import Ui_main_window
from pymdwizard.gui.MetadataRoot import MetadataRoot


class PyMdWizardMainForm(QMainWindow):


    def __init__(self, parent=None):
        # QtGui.QMainWindow.__init__(self, parent)
        super(self.__class__, self).__init__()

        self.build_ui()
        self.connect_events()

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = Ui_main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.metadata_root = MetadataRoot()
        self.ui.centralwidget.setLayout(self.metadata_root.layout())

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.actionOpen.triggered.connect(self.open)

    def open(self):
        fname = QFileDialog.getOpenFileName(self, 'USGS_ASC_PolarBears_FGDC.xml', r"N:\Metadata\MetadataWizard\pymdwizard\tests\data")
        if fname[0]:
            new_record = etree.parse(fname[0])
            self.metadata_root._from_xml(new_record)



def main():
    app = QApplication(sys.argv)

    mdwiz = PyMdWizardMainForm()
    mdwiz.show()
    app.exec_()


if __name__ == '__main__':
    main()