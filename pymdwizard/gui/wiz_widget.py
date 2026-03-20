#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
This module provides the base class for most gui components in the
MetadataWizard.


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import sys

# Non-standard python libraries.
try:
    from lxml import etree
    from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenu)
    from PyQt5.QtWidgets import (
        QMessageBox, QWidget, QLabel, QComboBox,
        QTabWidget, QSpacerItem, QToolButton, QGroupBox,
        QPlainTextEdit,
    )
    from PyQt5.QtGui import (QFont, QColor, QDrag, QPainter, QIcon)
    from PyQt5.QtCore import (
        Qt, QMimeData, QObject, QByteArray, QRegExp, QEvent,
    )
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, fgdc_utils)
    from pymdwizard.gui import repeating_element
except ImportError as err:
    raise ImportError(err, __file__)


class WizardWidget(QWidget):
    """
    Description:
        The base class all pymdwizard GUI components should inherit from.
        It provides core functionality for building the UI, handling XML
        conversion, and enabling drag-and-drop for metadata snippets.

    Passed arguments:
        xml (lxml node, optional): The original in-memory XML node.
        parent (PyQt QWidget, optional): The parent widget.
        original_xml (lxml node, optional): The original XML node before
            any changes.

    Returned objects:
        None

    Workflow:
        1. Initializes UI, styles, and events.
        2. Implements methods for XML serialization/deserialization.
        3. Implements drag-and-drop mechanics using MIME data.
        4. Provides utilities for context menus and widget clearing.

    Notes:
        Subclasses must override to_xml() and from_xml().
    """


    # Preferred widget size constants.
    # if widget doesn't collapse use -1 for COLLAPSED_HEIGHT
    WIDGET_WIDTH = 805
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 385

    acceptable_tags = []

    def __init__(self, parent=None):
        # Initialize the parent QWidget.
        QWidget.__init__(self, parent=parent)

        self.help_text = ""

        # For standalone testing and debugging (currently disabled).
        if __name__ == "__main__":
            QMainWindow.__init__(self, parent)

        self.in_context = False
        self.ui = None

        # Build the user interface.
        self.build_ui()

        # Set the widget's style sheet.
        self.set_stylesheet()

        # Connect signals and slots.
        self.connect_events()

        self.original_xml = None

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI class, sets up the layout, and configures
            drag-and-drop for the widget and its children.

        Notes:
            Subclasses should define self.ui_class and/or override
            this method for complex UI builds.
        """

        self.ui = self.ui_class()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # This is where more complex build information would go such as
        # instantiating child widgets, inserting them into the layout,
        # tweaking the layout or individual widget properties, etc.
        # If you are using this base class as intended this should not
        # include extensive widget building from scratch.

        # Setup drag-drop functionality for this widget and children.
        self.setup_dragdrop(self)

        # Any child widgets that have a separate drag-drop interactivity
        # need to be added to this widget after running self.setup_dragdrop
        # function so as not to override their individual drag-drop functions.

    def connect_events(self):
        """
        Description:
            Connects the appropriate GUI components with the
            corresponding functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Placeholder method to be overridden by subclasses.

        Notes:
            None
        """

        pass

    def to_xml(self):
        """
        Description:
            Subclass specific logic to convert the widget instance
            to an XML element.

        Passed arguments:
            None

        Returned objects:
            lxml element: The resulting XML snippet.

        Workflow:
            Must be overridden in subclass.

        Notes:
            None
        """

        print("_to_xml method Must be overridden in subclass")

    def from_xml(self, xml_element):
        """
        Description:
            Subclass specific logic to update the widget contents from
            an XML element.

        Passed arguments:
            xml_element (lxml element): Contains the FGDC section.

        Returned objects:
            None

        Workflow:
            Must be overridden in subclass.

        Notes:
            None
        """

        # Update self.xml appropriately (probably a full reace).
        print("_from_xml method Must be overridden in subclass")

    def make_tree(self, widget):
        """
        Description:
            Recursively traverses a widget hierarchy to build a
            corresponding XMLNode structure.

        Passed arguments:
            widget (PyQt5 widget): The starting widget.

        Returned objects:
            XMLNode: The root of the XML structure.

        Workflow:
            Traverses children, finds widgets prefixed with "fgdc_",
            creates an "XMLNode", and calls "add_children".

        Notes:
            Not used extensively in typical `WizardWidget` usage.
        """

        widget_children = widget.children()

        for child_widget in widget_children:
            try:
                widget_name = child_widget.objectName()
            except AttributeError:
                widget_name = "Unknown"

            if child_widget.objectName().startswith("fgdc_"):
                # Create root node for FGDC element.
                root_node = xml_utils.XMLNode(tag=widget_name.replace(
                    "fgdc_", ""))
                root_node.widget = child_widget

                # Recursively add children to this node.
                return self.add_children(child_widget, root_node)
            else:
                self.make_tree(child_widget)

    def get_children(self, widget):
        """
        Description:
            Returns a list of all relevant child objects/widgets of the
            passed widget, handling specific container types.

        Passed arguments:
            widget (PyQt5 widget): The widget to inspect.

        Returned objects:
            list: List of child objects.

        Workflow:
            Handles QTabWidget children separately from standard
            QObject children.

        Notes:
            None
        """

        try:
            if isinstance(widget, QTabWidget):
                # QTabWidget children are accessed by index.
                widget_children = [
                    widget.widget(i) for i in range(widget.count())
                ]
            else:
                # Standard QObject children.
                widget_children = widget.children()
        except AttributeError:
            try:
                # Handle layout items if object doesn't have .children().
                widget_children = [
                    widget.itemAt(i) for i in range(widget.count())
                ]
            except AttributeError:
                widget_children = []

        return widget_children

    def add_children(self, widget, parent_node):
        """
        Description:
            Recursively adds child widgets that correspond to FGDC tags
            to a parent "XMLNode" object.

        Passed arguments:
            widget (PyQt5 widget): The parent widget to search.
            parent_node (XMLNode object): The node to add children to.

        Returned objects:
            XMLNode: The updated parent node.

        Workflow:
            Traverses children, identifies widgets starting with "fgdc_",
            creates an "XMLNode", and attaches it to the parent.

        Notes:
            None
        """

        if isinstance(widget, WizardWidget):
            widget_children = widget.get_children(widget)
        else:
            widget_children = self.get_children(widget)

        for child_widget in widget_children:
            try:
                widget_name = child_widget.objectName()
            except AttributeError:
                widget_name = "Unknown"

            if widget_name.startswith("fgdc_"):
                # Create child node for FGDC element.
                child_node = xml_utils.XMLNode(tag=widget_name.replace(
                    "fgdc_", ""))
                child_node.widget = child_widget

                # Recurse for nested structure.
                self.add_children(child_widget, child_node)

                # Attach to parent.
                parent_node.add_child(child_node)
            else:
                self.add_children(child_widget, parent_node)
        return parent_node

    def dragEnterEvent(self, e):
        """
        Description:
            Accepts drag events only if the dragged content is plain text
            that can be converted to an XML node with a tag listed in
            `acceptable_tags`.

        Passed arguments:
            e (qt event): The drag enter event.

        Returned objects:
            None

        Workflow:
            Checks MIME format and validates XML tag against
            "acceptable_tags".

        Notes:
            None
        """

        mime_data = e.mimeData()
        if e.mimeData().hasFormat("text/plain"):
            try:
                element = xml_utils.string_to_node(mime_data.text())

                # Check if XML tag is acceptable for this widget.
                if element is not None and element.tag in self.acceptable_tags:
                    e.accept()
            except AttributeError:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Description:
            Updates the form with the contents of an XML node dropped
            onto it by calling "from_xml".

        Passed arguments:
            e (qt event): The drop event.

        Returned objects:
            None

        Workflow:
            Parses the dropped MIME data (plain text as XML) and calls
            the widget's "from_xml" method.

        Notes:
            None
        """

        try:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            mime_data = e.mimeData()

            # Convert plain text to XML node.
            element = xml_utils.string_to_node(mime_data.text())

            # Populate widget from XML.
            self.from_xml(element)
        except Exception:
            # Catch all exceptions during drop for logging/debugging.
            e = sys.exc_info()[0]
            print("problem drop", e)

    def get_mime(self):
        """
        Description:
            Creates and returns the MIME data representation of this
            widget's current content (as XML).

        Passed arguments:
            None

        Returned objects:
            Qt Mime data: MIME data containing XML snippet.

        Workflow:
            Calls "to_xml", pretty-prints it, and sets it as plain
            text and XML data in the MIME object.

        Notes:
            None
        """

        mime_data = QMimeData()

        # Convert widget content to pretty-printed XML string.
        pretty_xml = etree.tostring(self.to_xml(), pretty_print=True).decode()

        # Set plain text MIME format.
        mime_data.setText(pretty_xml)

        # Set custom XML MIME format
        mime_data.setData(
            'application/x-qt-windows-mime;value="XML"',
            QByteArray(pretty_xml.encode()),
        )

        return mime_data

    def copy_mime(self):
        """
        Description:
            Copies this object's XML MIME data onto the system clipboard.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the MIME data and sets it to the QApplication clipboard.

        Notes:
            None
        """

        clipboard = QApplication.clipboard()
        clipboard.setMimeData(self.get_mime())

    def paste_mime(self):
        """
        Description:
            Grabs the MIME data off the clipboard and attempts to paste
            it into this widget by calling `from_xml`.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Retrieves clipboard data, attempts to parse as XML, and
            updates the widget if successful, otherwise shows a warning.

        Notes:
            None
        """

        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasFormat("text/plain"):
            try:
                # Attempt to parse clipboard text as XML.
                element = xml_utils.string_to_node(mime_data.text())
            except:
                element = None

            if element is not None:
                # Update widget from XML.
                self.from_xml(element)
            else:
                # Show error if parsing fails.
                msg = (
                    "There was a problem pasting that content. \n "
                    "That content being drops does not appear to be "
                    "an xml element"
                )
                QMessageBox.warning(self, "Paste Error", msg)

    def mouseMoveEvent(self, e):
        """
        Description:
            Handles snippet capture and drag-drop initialization when
            the mouse moves with the left button pressed and Ctrl held.

        Passed arguments:
            e (qt event): The mouse move event.

        Returned objects:
            None

        Workflow:
            1. Checks for left button and Ctrl modifier.
            2. Checks distance threshold for drag start.
            3. Creates MIME data and a "ghost" pixmap for drag visual.
            4. Starts the drag operation.

        Notes:
            None
        """

        if e.buttons() != Qt.LeftButton:
            if hasattr(self, "drag_start_pos"):
                delattr(self, "drag_start_pos")

        if not hasattr(self, "drag_start_pos"):
            return

        # Check if mouse moved far enough to start a drag.
        if not (e.pos() - self.drag_start_pos).manhattanLength() > 75:
            return

        # Check for Ctrl modifier to initiate drag.
        modifiers = QApplication.keyboardModifiers()
        if not modifiers == Qt.ControlModifier:
            return

        mime_data = self.get_mime()

        # Create "ghost" pixmap for drag visual.
        pixmap = self.grab()
        size = pixmap.size() * 0.65
        half_pixmap = pixmap.scaled(
            size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
        )

        # Make the pixmap semi-transparent.
        painter = QPainter(half_pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationAtop)
        painter.fillRect(half_pixmap.rect(),
                         QColor(0, 0, 0, 127))

        # Draw the drag label on the pixmap.
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        painter.setFont(font)

        painter.setPen(Qt.red)
        painter.drawText(half_pixmap.rect(), Qt.AlignCenter,
                         self.drag_label)
        painter.end()

        # Start the drag operation.
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(half_pixmap)
        drag.setHotSpot(e.pos())

        # Execute the drag.
        # dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction)
        # dropAction = drag.exec_(Qt.TargetMoveAction)
        dropAction = drag.exec_()
        e.ignore()

    def setup_dragdrop(self, widget, enable=True, parent=None):
        """
        Description:
            Sets up mouse tracking and drag-drop on child widgets
            recursively.

        Passed arguments:
            widget (QObject): The starting widget/object.
            enable (bool): Flag to enable/disable drag-drop.
            parent (QObject, optional): Ignored in this implementation.

        Returned objects:
            None

        Workflow:
            Iterates through specific widget types, installs an event
            filter to handle mouse events, and sets drag-drop flags.

        Notes:
            None
        """

        self.setAcceptDrops(enable)

        # List of widgets to intercept drag events for.
        drag_types = [
            QLabel,
            QSpacerItem,
            QToolButton,
            QGroupBox,
            QPlainTextEdit,
            QComboBox,
        ]

        for drag_type in drag_types:
            # Find all children of a specific type.
            widgets = self.findChildren(drag_type, QRegExp(r".*"))
            for widget in widgets:
                # Install this widget's event filter.
                widget.installEventFilter(self)
                widget.setMouseTracking(enable)
                widget.setAcceptDrops(enable)

        # Populate tooltips after setting up event filters.
        self.populate_tooltips()

        # Ensure correct stylesheet is applied.
        self.set_stylesheet()

    def populate_tooltips(self):
        """
        Description:
            For this widget and any child widgets, populates tooltips
            and help text using the FGDC metadata lookup.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Loads the FGDC annotation lookup and calls
            "populate_tooltip" for all relevant widgets.

        Notes:
            None
        """

        # Load the centralized lookup data.
        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        if self.objectName().startswith("fgdc_"):
            self.populate_tooltip(self, annotation_lookup)

        # Find all child QObjects.
        widgets = self.findChildren(QObject, QRegExp(r".*"))
        for widget in widgets:
            self.populate_tooltip(widget, annotation_lookup)

    def populate_tooltip(self, widget, annotation_lookup):
        """
        Description:
            Formats and adds a tooltip to a single widget if its name
            starts with "fgdc_" or "help_".

        Passed arguments:
            widget (PyQt5 widget): The widget to add a tooltip to.
            annotation_lookup (dict): Dictionary for looking up help.

        Returned objects:
            None

        Workflow:
            Extracts the FGDC short name from the widget's object name,
            looks up the long name and annotation, and sets the tooltip
            and "help_text" attribute.

        Notes:
            None
        """

        if (widget.objectName().startswith("fgdc_") or
                widget.objectName().startswith("help_")):

            # Extract the short name (e.g., "fgdc_title" -> "title").
            shortname = widget.objectName()[5:]
            if shortname[-1].isdigit():
                # Handle repeating elements (e.g., "title1" -> "title").
                shortname = shortname[:-1]

            # Set the long name as the tooltip.
            widget.setToolTip(annotation_lookup[shortname]["long_name"])

            # Store the full annotation text.
            widget.help_text = annotation_lookup[shortname]["annotation"]

            try:
                # Propagate help text to the immediate parent if empty.
                if (
                    not hasattr(widget.parentWidget(), "help_text")
                    or not widget.parentWidget().help_text
                ):
                    widget.parentWidget().help_text = widget.help_text
            except:
                pass

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget and its child widgets
            that contain FGDC content.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Traverses children, clearing text-based widgets and
            recursively clearing "RepeatingElement" and "WizardWidget"
            children.

        Notes:
            Requires "pymdwizard.gui.repeating_element" to handle
            repeating groups.
        """

        widgets = self.findChildren(QWidget, QRegExp(r".*"))

        # Handle RepeatingElement widgets.
        for widget in widgets:
            if isinstance(widget, repeating_element.RepeatingElement):
                widget.clear_widgets()
                rep1_widget = widget.get_widgets()[0]
                if isinstance(rep1_widget, WizardWidget):
                    rep1_widget.clear_widget()

            # Handle simple FGDC text widgets.
            elif widget.objectName().startswith("fgdc_"):
                utils.set_text(widget, "")

        # Recurse into child WizardWidgets for a full clear.
        for widget in widgets:
            if isinstance(widget, WizardWidget):
                widget.clear_widget()

    def has_content(self):
        """
        Description:
            Returns if the widget contains legitimate content that should
            be written out to XML.

        Passed arguments:
            None

        Returned objects:
            bool: Always True by default; intended to be overridden.

        Workflow:
            Default implementation returns True.

        Notes:
            Subclasses should implement logic to check based on contents.
        """

        return True

    def leaveEvent(self, event):
        """
        Description:
            Resets the stylesheet when the mouse leaves the widget area
            (unless in context menu mode).

        Passed arguments:
            event (QEvent): The leave event.

        Returned objects:
            None

        Workflow:
            Sets the stylesheet to the normal style.

        Notes:
            None
        """

        if self.objectName() == "attribute_widget":
            return

        if not self.in_context:
            self.setStyleSheet(self.normal_style)

    def enterEvent(self, QEvent):
        """
        Description:
            Applies the focus stylesheet when the mouse enters the
            widget area.

        Passed arguments:
            QEvent (QEvent): The enter event.

        Returned objects:
            None

        Workflow:
            Sets the stylesheet to the focus style.

        Notes:
            None
        """

        if self.objectName() == "attribute_widget":
            return
        self.setStyleSheet(self.focus_style)

    def contextMenuEvent(self, event):
        """
        Description:
            Displays a context menu with Copy, Paste, Help, and Clear
            actions.

        Passed arguments:
            event (QEvent): The context menu event.

        Returned objects:
            None

        Workflow:
            1. Creates and populates the "QMenu".
            2. Executes the menu and handles the selected action, calling
               the appropriate copy/paste/clear methods.
            3. Displays the help text if requested.

        Notes:
            None
        """

        self.in_context = True

        # Identify the specific widget clicked.
        clicked_widget = self.childAt(event.pos())

        menu = QMenu(self)

        # Add Copy and Paste actions.
        copy_action = menu.addAction(QIcon("copy.png"), "&Copy")
        copy_action.setStatusTip("Copy to the Clipboard")

        paste_action = menu.addAction(QIcon("paste.png"), "&Paste")
        paste_action.setStatusTip("Paste from the Clipboard")

        # Add Help action if help text is available.
        if hasattr(clicked_widget, "help_text") and clicked_widget.help_text:
            menu.addSeparator()
            help_action = menu.addAction("Help")
        else:
            help_action = None

        # Add Clear action.
        menu.addSeparator()
        clear_action = menu.addAction("Clear content")

        # Display menu and wait for action.
        action = menu.exec_(self.mapToGlobal(event.pos()))

        # --- Handle Actions ---.
        if action == copy_action:
            if clicked_widget is None:
                pass
            elif clicked_widget.objectName() == "idinfo_button":
                self.idinfo.copy_mime()
            elif clicked_widget.objectName() == "dataquality_button":
                self.dataqual.copy_mime()
            elif clicked_widget.objectName() == "eainfo_button":
                self.eainfo.copy_mime()
            elif clicked_widget.objectName() == "distinfo_button":
                self.distinfo.copy_mime()
            elif clicked_widget.objectName() == "metainfo_button":
                self.metainfo.copy_mime()
            else:
                self.copy_mime()
        elif action == paste_action:
            self.paste_mime()
        elif action == clear_action:
            if clicked_widget is None:
                self.clear_widget()
            elif clicked_widget.objectName() == "idinfo_button":
                self.idinfo.clear_widget()
            elif clicked_widget.objectName() == "dataquality_button":
                self.dataqual.clear_widget()
            elif clicked_widget.objectName() == "eainfo_button":
                self.eainfo.clear_widget()
            elif clicked_widget.objectName() == "distinfo_button":
                self.distinfo.clear_widget()
            elif clicked_widget.objectName() == "metainfo_button":
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

    def set_stylesheet(self, recursive=False):
        """
        Description:
            Sets the widget's and its children's stylesheets based on
            user settings (font size/family) and defined styles.

        Passed arguments:
            recursive (bool): If True, applies styles to all child
                "WizardWidget" instances.

        Returned objects:
            None

        Workflow:
            Loads settings, formats the style strings, and applies them
            to the widget.

        Notes:
            None
        """

        # Load user settings.
        fontsize_i = utils.get_setting("fontsize", 9)
        fontsize = str(fontsize_i)
        fontsizeplus = str(fontsize_i + 3)
        fontfamily = utils.get_setting("fontfamily", "Arial")

        # Format normal style.
        self.normal_style = NORMAL_STYLE.replace("{fontsize}", fontsize)
        self.normal_style = self.normal_style.replace("{fontsizeplus}",
                                                      fontsizeplus)
        self.normal_style = self.normal_style.replace("Arial", fontfamily)

        # Format focus style.
        self.focus_style = FOCUS_STYLE.replace("{fontsize}", fontsize)
        self.focus_style = self.focus_style.replace("{fontsizeplus}",
                                                    fontsizeplus)
        self.focus_style = self.focus_style.replace("Arial", fontfamily)

        self.setStyleSheet(self.normal_style)

        # Recursively set stylesheet on child WizardWidgets.
        if recursive:
            widgets = self.findChildren(QWidget, QRegExp(r".*"))
            for widget in widgets:
                if isinstance(widget, WizardWidget):
                    widget.set_stylesheet(recursive=recursive)

    def eventFilter(self, obj, event):
        """
        Description:
            Filters events for child widgets to handle drag initiation
            and block unwanted events (e.g., mouse wheel on QComboBox).

        Passed arguments:
            obj (QObject): The object the event was sent to.
            event (QEvent): The event itself.

        Returned objects:
            bool: True if the event was handled and should be stopped,
                False otherwise.

        Workflow:
            Intercepts mouse press/move/release to check for drag start.
            Blocks mouse wheel events on "QComboBox".

        Notes:
            None
        """

        # It is possibel to use different groups of actions for different types
        # of widgets and either filtering the event or not.

        # Handle drag initiation events.
        if event.type() == event.MouseButtonPress:
            self.drag_start_pos = event.pos()
        elif event.type() == event.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == event.MouseButtonRelease:
            self.mouseMoveEvent(event)
        # Block mouse wheel on QComboBox.
        elif event.type() == QEvent.Wheel and isinstance(obj, QComboBox):
            event.ignore()
            return True
        elif event.type() == QEvent.ToolTip:
            pass
        else:
            pass

        # Call the base class event filter for unhandled events.
        return super(WizardWidget, self).eventFilter(obj, event)


#  ----------------------------------------------------------------------------
# TODO: move these into an external config file.
#  ----------------------------------------------------------------------------
NORMAL_STYLE = """
QGroupBox{
    background-color: transparent;
     subcontrol-position: top left; /* position at the top left*/
     padding-top: 20px;
    font: bold {fontsizeplus}pt "Arial";
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
font: {fontsize}pt "Arial";
color: rgb(90, 90, 90);
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QRadioButton {
font: {fontsize}pt "Arial";
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
    font: bold {fontsizeplus}pt "Arial";
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
font: {fontsize}pt "Arial";
color: rgb(90, 90, 90);
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QRadioButton {
font: {fontsize}pt "Arial";
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
