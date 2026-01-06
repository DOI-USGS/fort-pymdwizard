#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a base class for items that can contain 0 to n elements.


NOTES
------------------------------------------------------------------------------
None
"""

# Non-standard python libraries.
try:
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import (QWidget, QPlainTextEdit, QHBoxLayout, QLabel)
    from PyQt5 import QtCore
    from PyQt5.QtCore import Qt
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_repeating_element
    from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
except ImportError as err:
    raise ImportError(err, __file__)


class DefaultWidget(QWidget):
    """
    Description:
        The default widget for a repeating element. It acts as a single-
        line text input (despite using QPlainTextEdit) with a label and
        an optional "required" asterisk.

    Passed arguments:
        label (str): The label text next to the input.
        line_name (str): The object name for the text edit.
        required (bool): Whether to display the required asterisk.
        placeholder_text (str): Text displayed when the field is empty.
        spellings (bool): Whether to enable spell checking/highlighting.
        parent (QWidget): The parent widget.

    Returned objects:
        None

    Workflow:
        Initializes a QLabel and a QPlainTextEdit (configured as single-
        line), handles UI setup, event connections (to block returns),
        and optional required label display.

    Notes:
        Inherits from "QWidget". Uses QPlainTextEdit but restricts it
        to single-line input.
    """

    def __init__(
        self,
        label="",
        line_name="na",
        required=False,
        placeholder_text=None,
        spellings=True,
        parent=None,
    ):
        """
        Initialize the DefaultWidget with a label and an input field.
        """

        # Call the base class constructor.
        QWidget.__init__(self, parent=parent)
        self.layout = QHBoxLayout()
        self.qlbl = QLabel(label, self)
        self.added_line = QPlainTextEdit()

        # Set max height to emulate a single QLineEdit.
        max_line_height = self.added_line.fontMetrics().height() + 10
        self.added_line.setMaximumHeight(max_line_height)

        # Disable vertical scrolling to enforce single-line behavior.
        self.added_line.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.added_line.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Override mouse move event to prevent vertical scrolling.
        self.added_line.mouseMoveEvent = self.mouse_move
        self.added_line.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Connect text changed signal to handler that blocks returns.
        self.added_line.textChanged.connect(self.remove_returns)

        # Enable spell checking/highlighting if requested.
        if spellings:
            self.highlighter = Highlighter(self.added_line.document())

        # Set placeholder text if provided.
        if placeholder_text is not None:
            self.added_line.setPlaceholderText(placeholder_text)

        # Set the object name for XML parsing/finding.
        self.added_line.setObjectName(line_name)

        # Add widgets to the layout.
        self.layout.addWidget(self.qlbl)
        self.layout.addWidget(self.added_line)

        # Add required asterisk if requested.
        if required:
            self.required_label = QLabel(self)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(9)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            self.required_label.setFont(font)
            self.required_label.setScaledContents(True)
            self.required_label.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            )
            self.required_label.setIndent(0)

            # HTML for blue, large asterisk.
            self.required_label.setText(
                QtCore.QCoreApplication.translate(
                    "",
                    '<html><head/><body><p align="center">'
                    '<span style=" font-size:18pt; color:#55aaff;">*'
                    "</span></p></body></html>",
                )
            )
            self.layout.addWidget(self.required_label)

        # Final layout adjustments.
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

    def mouse_move(self, e):
        """
        Description:
            Overrides the QPlainTextEdit mouse move event to ignore
            vertical scrolling, making the widget behave like a QLineEdit.

        Passed arguments:
            e (QMouseEvent): The PyQt mouse event.

        Returned objects:
            None

        Workflow:
            Calls the base "mouseMoveEvent" only if the cursor is within
            the main edit area, then forces the vertical scrollbar to
            remain at its minimum position.

        Notes:
            None
        """

        # Allow base event for horizontal movement.
        if (e.y() < self.added_line.height() - 3 and
                e.x() < self.added_line.width() - 3):
            QPlainTextEdit.mouseMoveEvent(self.added_line, e)

        # Lock vertical scrollbar to top position.
        self.added_line.verticalScrollBar().setValue(
            self.added_line.verticalScrollBar().minimum()
        )

    def remove_returns(self):
        """
        Description:
            Handles text changes by replacing any line returns ("\n")
            with a space (" "), enforcing single-line behavior.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Disconnects the signal, replaces "\n" with " ", restores the
            cursor position, and reconnects the signal.

        Notes:
            Disconnecting and reconnecting prevents recursive calls.
        """

        # Temporarily disconnect to prevent recursion.
        self.added_line.textChanged.disconnect()

        old_position = self.added_line.textCursor().position()
        curtext = self.added_line.toPlainText()
        newtext = curtext.replace("\n", " ")
        self.added_line.setPlainText(newtext)

        # Restore cursor position.
        cursor = self.added_line.textCursor()
        cursor.setPosition(old_position)
        self.added_line.setTextCursor(cursor)

        # Reconnect the signal.
        self.added_line.textChanged.connect(self.remove_returns)

    def setText(self, text):
        """
        Description:
            Sets the text content of the input field.

        Passed arguments:
            text (str): The text to set.

        Returned objects:
            None

        Workflow:
            Uses a utility function to set text and repositions the
            cursor to the start.

        Notes:
            None
        """

        # Set the text using a utility function (assumed).
        utils.set_text(self.added_line, text)

        # Move cursor to the beginning.
        cursor = self.added_line.textCursor()
        cursor.setPosition(0)
        self.added_line.setTextCursor(cursor)

    def text(self):
        """
        Description:
            Returns the current text content of the input field.

        Passed arguments:
            None

        Returned objects:
            str: The current plain text content.

        Workflow:
            Calls toPlainText() on the QPlainTextEdit widget.

        Notes:
            None
        """

        return self.added_line.toPlainText()


class RepeatingElement(QWidget):
    """
    Description:
        A container widget used to manage a dynamic, repeating list of
        child widgets. It supports vertical stacking or tabbed display.

    Passed arguments:
        which (str): "vertical" or "tab" layout.
        tab_label (str): Base label for tabs if "which='tab'".
        widget (QWidget): The class of the widget to repeat.
        widget_kwargs (dict): Keyword arguments passed to the repeated
                              widget's constructor.
        italic_text (str): Descriptive text shown above the elements.
        add_text (str): Text for the "Add" button.
        remove_text (str): Text for the "Remove" button.
        show_buttons (bool): Whether to display the add/remove buttons.
        add_another (function): Custom function to call for adding a
                                widget (overrides default).
        parent (QWidget): The parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes UI and determines layout type ("vertical" or "tab").
        2. Sets button texts and handles initial setup/connections.
        3. Provides methods to add, remove, and retrieve child widgets.

    Notes:
        Inherits from "QWidget". Requires "UI_repeating_element" and the
        "DefaultWidget" or similar class for "widget".
    """

    default_params = {
        "Title": "insert title here",
        "Italic Text": "add notes here",
        "Add text": "button add me",
        "Remove text": "button del me",
        "widget": DefaultWidget,
        "spellings": True,
        "widget_kwargs": {"label": "add a text label"},
    }

    def __init__(
        self,
        which="vertical",
        tab_label="tab",
        widget=DefaultWidget,
        widget_kwargs={},
        italic_text="",
        add_text="Add another",
        remove_text="Remove last",
        show_buttons=True,
        add_another=None,
        parent=None,
    ):
        """
        Initialize the RepeatingElement container.
        """

        # Call the base class constructor.
        QWidget.__init__(self, parent=parent)

        # List to hold references to the child widgets.
        self.widgets = []
        self.which = which
        self.tab_label = tab_label
        self.widget = widget
        self.widget_kwargs = widget_kwargs

        self.build_ui()

        # Set descriptive italic text.
        if italic_text:
            self.ui.italic_label.setText(italic_text)

        # Determine layout type and assign content widgets/layouts.
        if which == "vertical":
            # self.SA is a scroll area (assumed).
            self.SA = self.ui.vertical_widget
            self.content_layout = self.ui.vertical_widget.layout()
            self.tab = False
            # Remove the unused tab widget from the UI.
            self.ui.tab_widget.deleteLater()
        elif which == "tab":
            self.content_widget = self.ui.tab_widget
            self.tab = True
            # Remove the unused vertical container from the UI.
            self.ui.vertical_widget.deleteLater()

        # Custom function override for adding a widget.
        if add_another is not None:
            self.add_another = add_another

        self.connect_events()

        # Hide buttons if not requested.
        if not show_buttons:
            self.ui.button_widget.hide()

        # Set button texts.
        self.ui.addAnother.setText(add_text)
        self.ui.popOff.setText(remove_text)

        # Set parent context for child widget instantiation.
        self.widget_kwargs["parent"] = self

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI and sets layout spacing to zero for the
            vertical stacking container.

        Notes:
            None
        """

        self.ui = UI_repeating_element.Ui_Form()
        self.ui.setupUi(self)

        # Ensure no gap between vertically stacked widgets.
        self.ui.vertical_widget.layout().setSpacing(0)

    def connect_events(self):
        """
        Description:
            Connects the add and remove buttons to their corresponding
            handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects "addAnother.clicked" to "add_another" and
            "popOff.clicked" to "pop_off".

        Notes:
            None
        """

        # Connect "Add" button to the add handler.
        self.ui.addAnother.clicked.connect(self.add_another)

        # Connect "Remove" button to the remove handler.
        self.ui.popOff.clicked.connect(self.pop_off)

    def add_another(self, clicked=None, tab_label=""):
        """
        Description:
            Adds a new instance of the repeated widget to the container.

        Passed arguments:
            clicked (bool, optional): Ignored; used for signal connection.
            tab_label (str, optional): Specific label for the new tab.

        Returned objects:
            widget (QWidget): The newly created widget instance.

        Workflow:
            1. Instantiates the child widget using "widget_kwargs".
            2. Appends it to self.widgets.
            3. Adds it to the layout (tab or vertical stack) and makes
               it the current item (if tabbed).

        Notes:
            None
        """

        # Instantiate the widget.
        widget = self.widget(**self.widget_kwargs)
        self.widgets.append(widget)

        if self.tab:
            # Handle tab layout.
            if not tab_label:
                # Generate a default tab label.
                tab_label = " ".join([self.tab_label, str(len(self.widgets))])
            self.ui.tab_widget.addTab(widget, tab_label)

            # Switch to the newly added tab.
            self.ui.tab_widget.setCurrentIndex(self.ui.tab_widget.count() - 1)
        else:
            # Handle vertical layout (insert before the last item).
            self.content_layout.insertWidget(len(self.widgets) - 1, widget)

        return widget

    def pop_off(self):
        """
        Description:
            Removes the last added widget or the currently selected tab
            from the container.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. If more than one widget exists, removes the widget,
               deletes its UI object, and removes it from the list.
            2. If only one widget remains, calls clear_widgets().

        Notes:
            If in tab mode, removes the currently active tab.
        """

        if self.widgets and len(self.widgets) > 1:
            if self.which == "tab":
                # Remove the currently selected tab.
                current_tab = self.ui.tab_widget.currentIndex()
                current_widget = self.widgets[current_tab]
                current_widget.deleteLater()
                del self.widgets[current_tab]
            else:
                # Remove the last added widget from the vertical stack.
                last_added = self.widgets.pop()
                last_added.deleteLater()
        elif len(self.widgets) == 1:
            # If only one remains, clear and add a new default.
            self.clear_widgets()

    def get_widgets(self):
        """
        Description:
            Returns the list of currently managed child widgets.

        Passed arguments:
            None

        Returned objects:
            list: The list of QWidget objects managed by this container.

        Workflow:
            Returns self.widgets.

        Notes:
            None
        """

        return self.widgets

    def clear_widgets(self, add_another=True):
        """
        Description:
            Removes and deletes all current child widgets.

        Passed arguments:
            add_another (bool): If True, adds a single default widget
                                after clearing.

        Returned objects:
            None

        Workflow:
            Iterates through self.widgets, calls deleteLater() on
            each, clears the list, and optionally adds a new default.

        Notes:
            None
        """

        # Delete all UI elements.
        for widget in self.widgets:
            widget.deleteLater()

        # Clear the internal list.
        self.widgets = []

        # Optionally add a new default widget.
        if add_another:
            self.add_another()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    widget_kws = {"label": "hello", "required": True}

    utils.launch_widget(
        RepeatingElement,
        which="vertical",
        tab_label="Processing Step",
        add_text="test add",
        # widget = sourceinput.SourceInput,
        widget_kwargs=widget_kws,
        remove_text="test remove",
        italic_text="some instruction",
    )
