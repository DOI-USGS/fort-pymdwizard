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
import sys
from lxml import etree

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QRadioButton, QPushButton, QComboBox, QToolButton, QCheckBox, QSpacerItem, QLabel, QGroupBox, QFrame
from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QBrush, QCursor
from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter
from PyQt5.QtCore import Qt, QMimeData, QObject, QByteArray, QRegExp, QEvent



class WizardWidget(QWidget):
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
        QWidget.__init__(self, parent=parent)

        # for standalone testing and debugging
        if __name__ == "__main__":
            QMainWindow.__init__(self, parent)

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
        # Update self.xml appropriately (probably a full reace)
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
        xpath_items = xpath.split('/')

        cur_item = self
        for item_string in xpath_items:
            cur_item = self.find_descendant(cur_item, item_string)
            if not cur_item:
                cur_item = self
        return cur_item

    def find_descendant(self, search_widget, search_name):

        for widget in search_widget.children():
            if widget.objectName() == 'fgdc_' + search_name:
                return widget
            else:
                result = self.find_descendant(widget, search_name)
                if result:
                    return result
        return None

    def dropEvent(self, e):
        """
        Updates the form with the contents of an xml node dropped onto it.

        Parameters
        ----------
        e : qt event

        Returns
        -------
        None
        """
        try:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            mime_data = e.mimeData()
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)

            self._from_xml(element)
        except:
            e = sys.exc_info()[0]
            print('problem drop', e)

    def mouseMoveEvent(self, e):
        """
        Handles the snippet capture and drag drop initialization
        based off of: http://stackoverflow.com/questions/28258050/drag-n-drop-button-and-drop-down-menu-pyqt-qt-designer

        Parameters
        ----------
        e : qt event

        Returns
        -------
        None
        """
        if e.buttons() != Qt.LeftButton:
            return
        if hasattr(self, 'drag_start_pos') and \
                not (e.pos() - self.drag_start_pos).manhattanLength() > 75:
            return


        mime_data = QMimeData()
        pretty_xml = etree.tostring(self._to_xml(), pretty_print=True).decode()
        mime_data.setText(pretty_xml)
        mime_data.setData('application/x-qt-windows-mime;value="XML"',
                          QByteArray(pretty_xml.encode()))


        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = self.grab()
        size = pixmap.size()*.65
        half_pixmap = pixmap.scaled(size, Qt.KeepAspectRatio,
                                    transformMode=Qt.SmoothTransformation)

        # below makes the pixmap half transparent
        painter = QPainter(half_pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationAtop)
        painter.fillRect(half_pixmap.rect(), QColor(0, 0, 0, 127))

        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(15)
        font.setBold(True)
        painter.setFont(font)

        painter.setPen(Qt.red)
        painter.drawText(half_pixmap.rect(), Qt.AlignCenter,
                         self.drag_label)
        painter.end()

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(half_pixmap)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction)
        e.ignore()

    def setup_dragdrop(self, widget, enable=True, parent=None):
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
        self.setAcceptDrops(enable)

        drag_types = [QLabel, QSpacerItem, QToolButton, QGroupBox]

        for drag_type in drag_types:
            widgets = self.findChildren(drag_type, QRegExp(r'.*'))
            for widget in widgets:
                widget.installEventFilter(self)
                widget.setMouseTracking(enable)
                widget.setAcceptDrops(enable)

        self.populate_tooltips()

    def populate_tooltips(self):
        import json
        annotation_lookup_fname = r"N:\Metadata\MetadataWizard\pymdwizard\pymdwizard\resources\FGDC_schemas\bdp_lookup"
        with open(annotation_lookup_fname, encoding='utf-8') as data_file:
            annotation_lookup= json.loads(data_file.read())


        widgets = self.findChildren(QObject, QRegExp(r'.*'))
        for widget in widgets:
            if widget.objectName().startswith('fgdc_'):
                shortname = widget.objectName().replace('fgdc_', '')
                if shortname[-1].isdigit():
                    shortname = shortname[:-1]
                widget.setToolTip(annotation_lookup[shortname]['annotation'])

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
        if event.type() == event.MouseButtonPress:
            print(event.pos())
            self.drag_start_pos = event.pos()
        elif event.type() == event.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == event.MouseButtonRelease:
            # print('event filter mouse release')
            self.mouseMoveEvent(event)
        # elif event.type() == event.DragLeave:
        #     print ('event dragleave')
        # elif event.type() == event.DragLeave:
        #     print ('NonClientAreaMouseButtonRelease')
        # else:
        #     pass

        # regardless, just do the default
        elif event.type() == QEvent.ToolTip:
            pass
        return super(WizardWidget, self).eventFilter(obj, event)

