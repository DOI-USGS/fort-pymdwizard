#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt base class for all the widgets that that make up the Wizard GUI

Provides standardized functionality to enable input and output of xml content
drop and drop functionality for xml content, xpath navigation cross walking,
and widget collapse/expand.


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

from PyQt4 import QtGui
from PyQt4 import QtCore


class WizardWidget(QtGui.QWidget):
    """
    The base class all pymdwizard GUI components should inherit from.

    Parameters
    ----------

    xml : lxml node
          The original in memory xml node being displayed by the widget.
          This node can contain content that does not get displayed in which
          case care should be taken to ensure that the _from_xml and _to_xml
          functions do not erase or overwrite this content.

    parent : PyQt4 QWidget

    original_xml : lxml node
                   The original xml node contents before any changes were made.
                   Note: This is not currently implemented
    """


    # Preferred widget size constants
    # if widget doesn't collapse use -1 for COLLAPSED_HEIGHT
    WIDGET_WIDTH = 805
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 385

    def __init__(self, xml=None, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        # for standalone testing and debugging
        if __name__ == "__main__":
            QtGui.QMainWindow.__init__(self, parent)

        self.original_xml = xml

        self.build_ui()
        self.connect_events()
        if xml:
            self.original_xml = xml
            self._from_xml(self.xml)

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # this is where more complex build information would go such as
        # instantiating child widgets, inserting them into the layout,
        # tweaking the layout or individual widget properties, etc.
        # If you are using this base class as intended this should not
        # include extensive widget building from scratch.

        # setup drag-drop functionality for this widget and all it's children.
        self.setup_dragdrop(self)

        # Any child widgets that have a separate drag-drop interactivity
        # need to be added to this widget after running self.setup_dragdrop
        # function so as not to override their individual drag-drop functions.

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

    def get_widget(self, xpath):
        """
        returns the widget (QLineEdit, QComboBox, etc) that corresponds to
        a given xpath.

        TODO: finalize general implementation details, although there's
        no reason that these couldn't be unique for different widgets.

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
        Sets up mouse tracking and drag drop on child widgets.
        This works recursively on all the child widgets and their children...

        Parameters
        ----------
        widget : QObject

        Returns
        -------

        None
        """

        # Dragging from QLineEdits and QTableViews has awkward side effects,
        # such as not being able to select text in the line edit.
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
