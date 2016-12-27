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
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint
from PyQt5.QtCore import Qt, QMimeData, QObject, QTimeLine
from PyQt5.QtGui import QPainter, QFont, QFontMetrics, QPalette, QBrush, QColor, QPixmap, QDrag

from pymdwizard.core import taxonomy

from pymdwizard.gui.wiz_widget import WizardWidget

from pymdwizard.gui.ui_files import UI_MainWindow
from pymdwizard.gui.IDInfo import IdInfo


class PyMdWizardMainForm(QMainWindow):

    drag_label = "metadata"

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
        self.ui = UI_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.idinfo = IdInfo()
        self.ui.page_idinfo.setLayout(self.idinfo.layout())

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        # switch_section_mapper = QtCore.QSignalMapper(self)
        # switch_section_mapper.setMapping()

        self.ui.idinfo_button.released.connect(self.section_changed)
        self.ui.dataquality_button.released.connect(self.section_changed)
        self.ui.spatial_button.released.connect(self.section_changed)
        self.ui.eainfo_button.released.connect(self.section_changed)
        self.ui.distinfo_button.released.connect(self.section_changed)
        self.ui.metainfo_button.released.connect(self.section_changed)
        self.ui.validation_button.released.connect(self.section_changed)

        # self.ui.button_search.clicked.connect(self.search_itis)
        # self.ui.search_term.returnPressed.connect(self.search_itis)
        # self.ui.table_results.doubleClicked.connect(self.add_tsn)
        # self.ui.button_add_taxon.clicked.connect(self.add_tsn)
        # self.ui.button_gen_fgdc.clicked.connect(self.generate_fgdc)
        # self.ui.button_remove_selected.clicked.connect(self.remove_selected)
        # self.ui.table_include.doubleClicked.connect(self.remove_selected)

    def section_changed(self):

        index_lookup = {'idinfo_button': 0, 'dataquality_button': 1,
                        'spatial_button': 2, 'eainfo_button': 3,
                        'distinfo_button': 4, 'metainfo_button': 5,
                        'validation_button': 6}
        button_name = self.sender().objectName()
        old_widget = self.ui.stackedWidget.currentWidget()
        new_index = index_lookup[button_name]
        new_widget = self.ui.stackedWidget.widget(new_index)

        fader_widget = FaderWidget(old_widget, new_widget)

        self.ui.stackedWidget.setCurrentIndex(new_index)

    def _to_xml(self):
        metadata_node = etree.Element('metadata')
        idinfo = self.idinfo._to_xml()
        metadata_node.append(idinfo)

        return metadata_node


    def _from_xml(self, contact_information):
        return "testing"
        # contact_dict = xml_utils.node_to_dict(contact_information)
        # utils.populate_widget(self, contact_dict)

    def get_widget(self, xpath):
        """
        returns the widget (QLineEdit, QComboBox, etc) that corresponds to
        a given xpath

        Parameters
        ----------
        xpath : str

        Returns
        -------
        pyqt widget
        """

        return self.findChildren(QLineEdit)


    def dropEvent(self, e):
        """
        Updates the form with the

        Parameters
        ----------
        e : qt event

        Returns
        -------
        None
        """
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        element = etree.fromstring(e.mimeData().text(), parser=parser)

        self._from_xml(element)

    def dragEnterEvent(self, e):
        """

        Parameters
        ----------
        e : qt event

        Returns
        -------

        """
        # should this always be accepted?
        e.accept()

    def mouseMoveEvent(self, e):
        """
        Handles the snippet capture and drag drop initialization

        Parameters
        ----------
        e : qt event

        Returns
        -------
        None
        """
        if e.buttons() != Qt.LeftButton:
            return

        mime_data = QMimeData()
        pretty_xml = etree.tostring(self._to_xml(), pretty_print=True).decode()
        mime_data.setText(pretty_xml)

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = QPixmap.grabWidget(self)
        size = pixmap.size()*.65
        half_pixmap = pixmap.scaled(size, Qt.KeepAspectRatio,
                                    transformMode=Qt.SmoothTransformation)

        # below makes the pixmap half transparent
        painter = QPainter(half_pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationAtop)
        painter.fillRect(half_pixmap.rect(), QColor(0, 0, 0, 127))

        font = QFont()
        font.setFamily('Arial')
        # font.setFixedPitch(True)
        font.setPointSize(15)
        # font.setBold(True)
        painter.setFont(font)

        painter.setPen(Qt.red)
        painter.drawText(half_pixmap.rect(), Qt.AlignCenter,
                         self.drag_label)

        painter.end()

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(half_pixmap)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(Qt.MoveAction)

    def setup_dragdrop(self, widget):
        """
        Sets up mouse tracking and drag drop on child widgets

        Parameters
        ----------
        widget : QObject

        Returns
        -------

        None
        """
        if not isinstance(widget, (QLineEdit, QTableView)):
            try:

                widget.setMouseTracking(True)
                widget.setAcceptDrops(True)
                widget.mouseMoveEvent = self.mouseMoveEvent
                widget.setDragEnabled(True)
            except:
                pass

        for child in widget.findChildren(QObject):
            self.setup_dragdrop(child)


class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):

        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(450)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):

        self.pixmap_opacity = 1.0 - value
        self.repaint()


def main():
    app = QApplication(sys.argv)

    mdwiz = PyMdWizardMainForm()
    mdwiz.show()
    app.exec_()


if __name__ == '__main__':
    main()