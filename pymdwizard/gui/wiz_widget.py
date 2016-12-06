"""
Contains the baseclass that all pymdwizard GUI baseclasses inherit from
"""
from lxml import etree

from PyQt4 import QtGui
from PyQt4 import QtCore

class WizardWidget(QtGui.QWidget):

    # Prefered widget size constants
    # if widget doesn't collapse use -1 for COLLAPSED_HEIGHT
    WIDGET_WIDTH = 805
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT

    def __init__(self, xml=None, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        # for standalone testing and debugging
        if __name__ == "__main__":
            QtGui.QMainWindow.__init__(self, parent)

        self.xml = xml

        self.build_ui()
        self.connect_events()
        if self.xml:
            self._from_xml(self.xml)

        # setup the drag and drop functionality
        self.setMouseTracking(True)
        self.setup_dragdrop(self)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        print("build_ui method Must be overridden in subclass")

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        print("connect_events method Must be overridden in subclass")

    def _to_xml(self):
        """
        subclass specific logic to convert the widget instance to xml element.

        Returns
        -------
            lxml element with the contents of this form
            translated to an xml snippet
        """

        print("_to_xml method Must be overridden in subclass")

    def _from_xml(self, xml_element):
        """
        subclass specific logic to update the widget contents from xml element.

        Parameters
        ----------
        xml_element : lxml element
                      Contains well-formatted and appropriate FGDC section
                      that will be translated into this GUI representation

        Returns
        -------
            None
        """
        # Update self.xml appropriately (probably a full replace)
        print("_from_xml method Must be overridden in subclass")

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
        pixmap = QtGui.QPixmap.grabWidget(self.ui.groupBox)
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
        painter.drawText( half_pixmap.rect(),
                          QtCore.Qt.AlignCenter,
                          "Contact Information (cntinfo)", )

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
        if not isinstance(widget, QtGui.QLineEdit):
            try:

                widget.setMouseTracking(True)
                widget.setAcceptDrops(True)
                widget.mouseMoveEvent = self.mouseMoveEvent
                widget.setDragEnabled(True)
            except:
                pass

        for child in widget.findChildren(QtCore.QObject):
            self.setup_dragdrop(child)
