#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Access Constraints <acconst> section


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
#import sys #

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

#sys.path.append('C:/Users/mhannon/dev_mdwizard/pymdwizard') #


from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_AccessConstraints #
#from pymdwizard.gui import AccessConstraints #


class AccessConstraints(WizardWidget): #

    #WIDGET_WIDTH = 500
    #COLLAPSED_HEIGHT = 75
    #EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Access Constraints <acconst>"

    # This dictionary provides a mechanism for crosswalking between
    # gui elements (pyqt widgets) and the xml document
    #xpath_lookup = {'acconst': 'acconst'}
#    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
#                    'cntorg': 'cntinfo/cntperp/cntorg',
#                    'cntpos': 'cntinfo/cntpos',
#                    'address': 'cntinfo/cntaddr/address',
#                    'address2': 'cntinfo/cntaddr/address[2]',
#                    'address3': 'cntinfo/cntaddr/address[3]',
#                    'city': 'cntinfo/cntaddr/city',
#                    'state': 'cntinfo/cntaddr/state',
#                    'postal': 'cntinfo/cntaddr/postal',
#                    'state': 'cntinfo/cntaddr/state',
#                    'country': 'cntinfo/cntaddr/country',
#                    'addrtype': 'cntinfo/cntaddr/addrtype',
#                    'cntvoice': 'cntinfo/cntvoice',
#                    'cntfax': 'cntinfo/cntfax',
#                    'cntemail': 'cntinfo/cntemail'}

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        #print "here"
        self.ui = UI_AccessConstraints.Ui_Form()#.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)
        

        #####self.acconst = AccessConstraints.AccessConstraints()#
        #####self.ui.main_layout.addWidget(self.acconst)

       # self.collaped_size = QSize(self.WIDGET_WIDTH,
       #                                   self.COLLAPSED_HEIGHT)
        #self.expanded_size = QSize(self.WIDGET_WIDTH,
       #                            self.EXPANDED_HEIGHT)
       # self.resize(self.collaped_size)


        #self.setObjectName("acconst")

#    def connect_events(self):
#        """
#        Connect the appropriate GUI components with the corresponding functions
#
#        Returns
#        -------
#        None
#        """
#        self.ui.rbtn_yes.toggled.connect(self.access_constraints_change)
#
#    def access_constraints_change(self, b):
#        if b:
#            self.acconst.show()
#        else:
#            self.acconst.hide()

    def dragEnterEvent(self, e):
        """

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
            if element.tag == 'acconst':
                print "element", element.text
                print "parser", parser
                print mime_data.text()
                e.accept(element.text)
            else:
                e.ignore()

    def _to_xml(self):
        acconst = etree.Element('acconst')

        acconst.text = self.findChild(QPlainTextEdit, "acconst").toPlainText()
        print "ok"

        return acconst

#    def _from_xml(self, access_constraints):
#        try:
#            if access_constraints.tag == 'acconst':
#                print "This", access_constraints
#                acconst_node = access_constraints
#            else:
#                print "why", "/?"
#                acconst_node = access_constraints.xpath('acconst')[0]
#            self.acconst._from_xml(acconst_node)
#        except KeyError:
#            pass

if __name__ == "__main__":
    utils.launch_widget(AccessConstraints,
                        "Access Constraints testing")

