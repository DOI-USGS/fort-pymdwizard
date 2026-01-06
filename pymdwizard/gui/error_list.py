#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a display widget with a list of schema errors that maintains
functionality to highlight them on the parent application


NOTES
------------------------------------------------------------------------------
None
"""

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QWidget, QListWidgetItem)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_error_list
except ImportError as err:
    raise ImportError(err, __file__)


class ErrorList(QWidget):
    """
    Description:
        A widget for displaying a list of validation errors detected in
        the main form. Clicking an error item triggers navigation to the
        associated element in the main form. Inherits from QWidget.

    Passed arguments:
        main_form (Main_Form): A reference to the main application form
            or window, which must have a "goto_error" method.
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        Initializes the UI, stores a list of errors, and connects the
        item click signal to the "main_form.goto_error" method to allow
        user navigation.

    Notes:
        None
    """

    def __init__(self, main_form, parent=None):
        # Initialize the parent QWidget class.
        QWidget.__init__(self, parent=parent)

        # Instantiate and setup the UI elements.
        self.ui = UI_error_list.Ui_error_list()
        self.ui.setupUi(self)

        # Store reference to the main form.
        self.main_form = main_form

        # Internal list to track errors (msg, xpath).
        self.errors = []

        # Connect item click signal to main form's navigation method.
        self.ui.listWidget.itemClicked.connect(self.main_form.goto_error)

    def add_error(self, error_msg, xpath):
        """
        Description:
            Adds a new validation error message to the list widget.

        Passed arguments:
            error_msg (str): The human-readable error description.
            xpath (str): The XML path used to locate the offending
                element in the main form.

        Returned objects:
            None

        Workflow:
            Creates a new "QListWidgetItem", sets its text and hidden
            data (the xpath), adds it to the list, and stores it in the
            internal errors list.

        Notes:
            The error message is stored as text, and the xpath is stored
            as hidden data (data role 1) for easy retrieval during click.
        """

        # Create a new list item.
        action = QListWidgetItem()

        # Set the displayed text.
        action.setText(error_msg)

        # Ensure the item is visible.
        action.setHidden(False)

        # Store the XPath as hidden data (role 1).
        action.setData(1, xpath)

        # Add the item to the list widget.
        self.ui.listWidget.addItem(action)

        # Store the error tuple internally.
        self.errors.append((error_msg, xpath))

    def clear_errors(self):
        """
        Description:
            Clears all displayed error messages and the internal error
            list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the QListWidget's clear method to remove all items.

        Notes:
            None
        """

        # Clear all items from the list widget.
        self.ui.listWidget.clear()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ErrorList, "ErrorList", url=r"c:/temp/text.html")
