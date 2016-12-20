#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from lxml import etree

from PyQt4 import QtGui
from PyQt4 import QtCore
Qt = QtCore.Qt

from pymdwizard.core import taxonomy

from pymdwizard.gui.wiz_widget import WizardWidget

from pymdwizard.gui.ui_files import UI_MainWindow
from pymdwizard.gui.IDInfo import IdInfo

class PyMdWizardMainForm(QtGui.QMainWindow):

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

        return self.findChildren(QtGui.QLineEdit)


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
        if e.buttons() != QtCore.Qt.LeftButton:
            return

        mime_data = QtCore.QMimeData()
        pretty_xml = etree.tostring(self._to_xml(), pretty_print=True).decode()
        mime_data.setText(pretty_xml)

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = QtGui.QPixmap.grabWidget(self)
        size = pixmap.size()*.65
        half_pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio,
                                    transformMode=QtCore.Qt.SmoothTransformation)

        # below makes the pixmap half transparent
        painter = QtGui.QPainter(half_pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationAtop)
        painter.fillRect(half_pixmap.rect(), QtGui.QColor(0, 0, 0, 127))

        font = QtGui.QFont()
        font.setFamily('Arial')
        # font.setFixedPitch(True)
        font.setPointSize(15)
        # font.setBold(True)
        painter.setFont(font)

        painter.setPen(QtCore.Qt.red)
        painter.drawText(half_pixmap.rect(), QtCore.Qt.AlignCenter,
                         self.drag_label)

        painter.end()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(half_pixmap)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)

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
        if not isinstance(widget, (QtGui.QLineEdit, QtGui.QTableView)):
            try:

                widget.setMouseTracking(True)
                widget.setAcceptDrops(True)
                widget.mouseMoveEvent = self.mouseMoveEvent
                widget.setDragEnabled(True)
            except:
                pass

        for child in widget.findChildren(QtCore.QObject):
            self.setup_dragdrop(child)



class FaderWidget(QtGui.QWidget):

    def __init__(self, old_widget, new_widget):

        QWidget.__init__(self, new_widget)

        self.old_pixmap = QtGui.QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QtCore.QTimeLine()
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


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, Qt, QPoint
from PyQt4.QtGui import QStyleOptionHeader, QHeaderView, QPainter, QWidget, QStyle, QMatrix, QFont, QFontMetrics, QPalette, QBrush, QColor


def main():
    app = QtGui.QApplication(sys.argv)

    # layout = QtGui.QVBoxLayout()
    # layout.addWidget()

    myapp = PyMdWizardMainForm()
    # myapp.resize(1186, 561)
    # myapp.setContentsMargins(0,0,0,0)
    # myapp.layout().setContentsMargins(0,0,0,0)


    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()