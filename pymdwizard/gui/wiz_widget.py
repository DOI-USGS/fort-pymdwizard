#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
This module provides the base class for most gui components in the
MetadataWizard.


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

import sys
from lxml import etree

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDrag
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QMimeData
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QEvent

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import fgdc_utils


class WizardWidget(QWidget):
    """
    The base class all pymdwizard GUI components should inherit from.
    Parameters
    ----------
    xml : lxml node
          The original in memory xml node being displayed by the widget.
          This node can contain content that does not get displayed in which
          case care should be taken to ensure that the from_xml and to_xml
          functions do not erase or overwrite this content.
    parent : PyQt5 QWidget
    original_xml : lxml node
                   The original xml node contents before any changes were made.
    """
    # Preferred widget size constants
    # if widget doesn't collapse use -1 for COLLAPSED_HEIGHT
    WIDGET_WIDTH = 805
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 385

    acceptable_tags = []

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.help_text = ''

        # for standalone testing and debugging
        if __name__ == "__main__":
            QMainWindow.__init__(self, parent)

        self.in_context = False
        self.ui = None
        self.build_ui()
        self.connect_events()

        self.original_xml = None

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
        pass

    def to_xml(self):
        """
        subclass specific logic to convert the widget instance to xml element.

        Returns
        -------
            lxml element with the contents of this form
            translated to an xml snippet
        """
        print("_to_xml method Must be overridden in subclass")

    def from_xml(self, xml_element):
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

    def make_tree(self, widget):
        widget_children = widget.children()

        for child_widget in widget_children:
            try:
                widget_name = child_widget.objectName()
            except AttributeError:
                widget_name = 'Unknown'

            if child_widget.objectName().startswith('fgdc_'):
                root_node = xml_utils.XMLNode(tag=widget_name.replace('fgdc_', ''))
                root_node.widget = child_widget
                return self.add_children(child_widget, root_node)
            else:
                self.make_tree(child_widget)

    def get_children(self, widget):
        """
        Returns a list of all the widgets on the widget passed

        Parameters
        ----------
        widget : PyQt5 widget

        Returns
        -------
        list of all widgets on the widget passed
        """
        try:
            if type(widget) == QTabWidget:
                widget_children = [widget.widget(i) for i in
                                   range(widget.count())]
            else:
                widget_children = widget.children()
        except AttributeError:
            try:
                widget_children = [widget.itemAt(i) for i in
                                   range(widget.count())]
            except AttributeError:
                widget_children = []
        return widget_children

    def add_children(self, widget, parent_node):
        """
        add child widgets to a parent XMLNode object.

        Parameters
        ----------
        widget : PyQt5 widget
        parent_node : XMLNode object
                The node that will be
        Returns
        -------

        """
        if isinstance(widget, WizardWidget):
            widget_children = widget.get_children(widget)
        else:
            widget_children = self.get_children(widget)

        for child_widget in widget_children:
            try:
                widget_name = child_widget.objectName()
            except AttributeError:
                widget_name = 'Unknown'

            if widget_name.startswith('fgdc_'):
                child_node = xml_utils.XMLNode(tag=widget_name.replace('fgdc_', ''))
                child_node.widget = child_widget
                self.add_children(child_widget, child_node)
                parent_node.add_child(child_node)
            else:
                self.add_children(child_widget, parent_node)
        return parent_node

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called in our list of acceptable_tags
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            try:
                element = xml_utils.string_to_node(mime_data.text())
                if element is not None and element.tag in self.acceptable_tags:
                    e.accept()
            except AttributeError:
                e.ignore()

        else:
            e.ignore()

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
            element = xml_utils.string_to_node(mime_data.text())

            self.from_xml(element)
        except:
            e = sys.exc_info()[0]
            print('problem drop', e)

    def get_mime(self):
        """
        return a copy of this widget's mime data

        Returns
        -------
        Qt Mime data from this widget
        """
        mime_data = QMimeData()
        pretty_xml = etree.tostring(self.to_xml(), pretty_print=True).decode()
        mime_data.setText(pretty_xml)
        mime_data.setData('application/x-qt-windows-mime;value="XML"',
                          QByteArray(pretty_xml.encode()))
        return mime_data

    def copy_mime(self):
        """
        Copy this objects mime data onto the system clipboard

        Returns
        -------
        None
        """
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(self.get_mime())

    def paste_mime(self):
        """
        Grab the last mime data off the clipboard and attempt to paste it
        into this widget.

        Returns
        -------
        None
        """
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasFormat('text/plain'):
            try:
                element = xml_utils.string_to_node(mime_data.text())
            except:
                element = None
            if element is not None:
                self.from_xml(element)
            else:
                msg = "There was a problem pasting that content."
                msg += "\n that content being drops does not appear to be an xml element"
                QMessageBox.warning(self, "Paste Error", msg)

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
            if hasattr(self, 'drag_start_pos'):
                delattr(self, 'drag_start_pos')

        if not hasattr(self, 'drag_start_pos'):
            return

        if not (e.pos() - self.drag_start_pos).manhattanLength() > 75:
            return
        modifiers = QApplication.keyboardModifiers()
        if not modifiers == Qt.ControlModifier:
            return

        mime_data = self.get_mime()

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
        drag.setHotSpot(e.pos())

        # dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction)
        # dropAction = drag.exec_(Qt.TargetMoveAction)
        dropAction = drag.exec_()
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

        drag_types = [QLabel, QSpacerItem, QToolButton, QGroupBox,
                      QPlainTextEdit, QComboBox]

        for drag_type in drag_types:
            widgets = self.findChildren(drag_type, QRegExp(r'.*'))
            for widget in widgets:
                widget.installEventFilter(self)
                widget.setMouseTracking(enable)
                widget.setAcceptDrops(enable)

        self.populate_tooltips()
        self.set_stylesheet()

    def populate_tooltips(self):
        """
        For this widget and any child widgets populate the tooltips
        for any with names that begin with FGDC_ or Help_

        Returns
        -------
        None
        """
        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        if self.objectName().startswith('fgdc_'):
            self.populate_tooltip(self, annotation_lookup)

        widgets = self.findChildren(QObject, QRegExp(r'.*'))
        for widget in widgets:
            self.populate_tooltip(widget, annotation_lookup)

    def populate_tooltip(self, widget, annotation_lookup):
        """
        Format and add a tooltip a single widget

        Parameters
        ----------
        widget : PyQt5 widget to add a tooltip to.
        annotation_lookup : dict
            The dictionary to use for looking up help documentation

        Returns
        -------
        None
        """
        if widget.objectName().startswith('fgdc_') or \
                widget.objectName().startswith('help_'):
            shortname = widget.objectName()[5:]
            if shortname[-1].isdigit():
                shortname = shortname[:-1]
            widget.setToolTip(annotation_lookup[shortname]['long_name'])
            widget.help_text = annotation_lookup[shortname]['annotation']
            try:
                if not hasattr(widget.parentWidget(), 'help_text') or \
                        not widget.parentWidget().help_text:
                    widget.parentWidget().help_text = widget.help_text
            except:
                pass

    def clear_widget(self):
        """
        Clears all content from this widget

        Returns
        -------
        None
        """
        from pymdwizard.gui import repeating_element
        widgets = self.findChildren(QWidget, QRegExp(r'.*'))

        for widget in widgets:
            if isinstance(widget, repeating_element.RepeatingElement):
                widget.clear_widgets()
                rep1_widget = widget.get_widgets()[0]
                if isinstance(rep1_widget, WizardWidget):
                    rep1_widget.clear_widget()

            elif widget.objectName().startswith('fgdc_'):
                utils.set_text(widget, '')

        for widget in widgets:
            if isinstance(widget, WizardWidget):
                widget.clear_widget()

    def has_content(self):
        """
        Returns if the widget contains legitimate content that should be
        written out to xml
        By default this is always true but should be implement in each
        subclass with logic to check based on contents

        Returns
        -------
        bool : True if there is content, False if no
        """
        return True

    def leaveEvent(self, event):
        if self.objectName() == 'attribute_widget':
            return

        if not self.in_context:
            self.setStyleSheet(NORMAL_STYLE)

    def enterEvent(self, QEvent):
        if self.objectName() == 'attribute_widget':
            return
        self.setStyleSheet(FOCUS_STYLE)

    def contextMenuEvent(self, event):
        """

        Parameters
        ----------
        event

        Returns
        -------

        """

        self.in_context = True
        clicked_widget = self.childAt(event.pos())


        menu = QMenu(self)
        copy_action = menu.addAction(QIcon('copy.png'), '&Copy')
        copy_action.setStatusTip('Copy to the Clipboard')

        paste_action = menu.addAction(QIcon('paste.png'), '&Paste')
        paste_action.setStatusTip('Paste from the Clipboard')

        if hasattr(clicked_widget, 'help_text') and clicked_widget.help_text:
            menu.addSeparator()
            help_action = menu.addAction("Help")
        else:
            help_action = None

        menu.addSeparator()
        clear_action = menu.addAction("Clear content")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == copy_action:
            if clicked_widget is None:
                pass
            elif clicked_widget.objectName() == 'idinfo_button':
                self.idinfo.copy_mime()
            elif clicked_widget.objectName() == 'dataquality_button':
                self.dataqual.copy_mime()
            elif clicked_widget.objectName() == 'eainfo_button':
                self.eainfo.copy_mime()
            elif clicked_widget.objectName() == 'distinfo_button':
                self.distinfo.copy_mime()
            elif clicked_widget.objectName() == 'metainfo_button':
                self.metainfo.copy_mime()
            else:
                self.copy_mime()
        elif action == paste_action:
            self.paste_mime()
        elif action == clear_action:
            if clicked_widget is None:
                self.clear_widget()
            elif clicked_widget.objectName() == 'idinfo_button':
                self.idinfo.clear_widget()
            elif clicked_widget.objectName() == 'dataquality_button':
                self.dataqual.clear_widget()
            elif clicked_widget.objectName() == 'eainfo_button':
                self.eainfo.clear_widget()
            elif clicked_widget.objectName() == 'distinfo_button':
                self.distinfo.clear_widget()
            elif clicked_widget.objectName() == 'metainfo_button':
                self.metainfo.clear_widget()
            else:
                self.clear_widget()
        elif help_action is not None and action == help_action:
            msg = QMessageBox(self)
            # msg.setTextFormat(Qt.RichText)
            msg.setText(clicked_widget.help_text)
            msg.setWindowTitle("Help")
            msg.show()
        self.in_context = False

    def set_stylesheet(self):
        self.setStyleSheet(NORMAL_STYLE)

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
            self.drag_start_pos = event.pos()
        elif event.type() == event.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == event.MouseButtonRelease:
            self.mouseMoveEvent(event)
        # regardless, just do the default
        elif event.type() == QEvent.ToolTip:
            pass
        elif event.type() == QEvent.Wheel and isinstance(obj, QComboBox):
            event.ignore()
            return True

        return super(WizardWidget, self).eventFilter(obj, event)

# TODO: move these into an external config file
NORMAL_STYLE = """
QGroupBox{
    background-color: transparent;
     subcontrol-position: top left; /* position at the top left*/
     padding-top: 20px;
    font: bold 12px;
    color: rgba(90, 90, 90, 225);
    border: 1px solid gray;
    border-radius: 2px;
    border-color: rgba(90, 90, 90, 40);
}
QGroupBox::title {
text-align: left;
subcontrol-origin: padding;
subcontrol-position: top left; /* position at the top center */padding: 3 3px;
}
QLabel{
font: 9pt "Arial";
color: rgb(90, 90, 90);
}
QLineEdit, QComboBox {
font: 9pt "Arial";
color: rgb(50, 50, 50);
}

QGroupBox:Hover {
    border-color: rgba(90, 90, 90, 240);
}

.QFrame {
    color: rgba(90, 90, 90, 225);
    border: 1px solid gray;
    border-radius: 2px;
    border-color: rgba(90, 90, 90, 75);
}
"""

FOCUS_STYLE = """
QGroupBox{
    background-color: transparent;
     subcontrol-position: top left; /* position at the top left*/
     padding-top: 20px;
    font: bold 12px;
    color: rgba(90, 90, 90);
    border: 1px solid gray;
    border-radius: 2px;
    border-color: rgba(90, 90, 90, 200);
}
QGroupBox::title {
text-align: left;
subcontrol-origin: padding;
subcontrol-position: top left; /* position at the top center */padding: 3 3px;
}
QLabel{
font: 9pt "Arial";
color: rgb(90, 90, 90);
}
QLineEdit, QComboBox {
font: 9pt "Arial";
color: rgb(50, 50, 50);
}

.QFrame {
    color: rgba(90, 90, 90, 225);
    border: 1px solid gray;
    border-radius: 2px;
    border-color: rgba(90, 90, 90, 75);
}
"""

ERROR_STYLE = """"""

ERROR_FOCUS_STYLE = """"""
