#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


NOTES
------------------------------------------------------------------------------
None
"""

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QMessageBox, QWidget)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_fgdc_date
except ImportError as err:
    raise ImportError(err, __file__)


class FGDCDate(QWidget):
    """
    Description:
        A reusable widget for entering and validating dates according to
        FGDC CSDGM format rules (YYYY, YYYYMM, YYYYMMDD, or "Unknown").
        Inherits from QWidget.

    Passed arguments:
        parent (QWidget, optional): Parent widget.
        show_format (bool): If True, shows the format helper widget.
        label (str): Text label for the date field.
        required (bool): If True, shows the required indicator.
        fgdc_name (str, optional): Object name for the date input
            field ("fgdc_caldate").
        parent_fgdc_name (str, optional): Object name for the parent
            widget container ("parent_fgdc").

    Returned objects:
        None

    Workflow:
        1. Initializes the UI.
        2. Configures display based on "show_format", "label", and
           "required" flags.
        3. Sets object names for XML identification.
        4. Connects the "editingFinished" signal to the validation
           method.

    Notes:
        Validation logic uses a QMessageBox to notify the user of
        formatting errors.
    """

    def __init__(
        self,
        parent=None,
        show_format=True,
        label="",
        required=False,
        fgdc_name=None,
        parent_fgdc_name=None,
    ):

        # Initialize the parent QWidget class.
        QWidget.__init__(self, parent=parent)
        self.build_ui()

        # Configure UI visibility based on initialization flags.
        if not show_format:
            self.ui.widget_format.hide()

        if label:
            self.ui.label.setText(label)
        else:
            # Hide the label if no text is provided.
            self.ui.label.visible = False

        if not required:
            self.ui.lbl_required.hide()

        # Store reference to the actual date input widget.
        self.date_widget = self.ui.fgdc_caldate

        # Set object name for the date input widget (for XML/utility).
        if fgdc_name is not None:
            self.ui.fgdc_caldate.setObjectName(fgdc_name)

        # Set object name for the parent container (for XML/utility).
        if parent_fgdc_name is not None:
            self.ui.parent_fgdc.setObjectName(parent_fgdc_name)

        # Used to prevent repetitive checks if content has not changed.
        self.last_checked_contents = ""
        self.connect_events()

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates and sets up the UI elements.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_fgdc_date.Ui_parent_widget()
        self.ui.setupUi(self)

    def connect_events(self):
        """
        Description:
            Connect the appropriate GUI components with the corresponding
            functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the date input field's "editingFinished" signal to
            the "check_format" validation method.

        Notes:
            None
        """

        # Connect the date widget's signal to the validation function.
        self.date_widget.editingFinished.connect(self.check_format)

    def check_format(self):
        """
        Description:
            Validates the date format upon completion of editing.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Checks if the content has changed since the last check.
            2. Validates length (must be 4, 6, 8, or 0) and content
               (must be digits or "Unknown").
            3. If invalid, displays a "QMessageBox" detailing the error
               and required formats.

        Notes:
            None
        """

        # Retrieve date value.
        cur_contents = self.date_widget.text()

        # Skip validation if content is unchanged.
        if cur_contents == self.last_checked_contents:
            return
        else:
            self.last_checked_contents = cur_contents

        msg = ""
        # Check if length is valid (0 for empty, 4, 6, or 8).
        if len(cur_contents) not in (0, 4, 6, 8):
            msg = (
                "An FGDC date needs to be 4, 6, or 8 numbers long, "
                "or be 'Unknown'"
            )

        # Check if content consists of only digits.
        if not cur_contents.isdigit() and cur_contents != "Unknown":
            msg = "An FGDC date can only consist of numbers or 'Unknown'"

        # Clear message if explicitly set to "Unknown" (redundant with
        # previous check, but safer).
        if cur_contents == "Unknown":
            msg = ""

        # Show message box if an error message was generated.
        if msg:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(msg)
            msgbox.setInformativeText("YYYY or YYYYMM or YYYYMMDD or 'Unknown'")
            msgbox.setWindowTitle("Problem with FGDC date format")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def get_date(self):
        """
        Description:
            Returns the current text in the date input field.

        Passed arguments:
            None

        Returned objects:
            str: The current date string.

        Workflow:
            Retrieves text from the internal date widget.

        Notes:
            None
        """

        return self.date_widget.text()

    def set_date(self, date_str):
        """
        Description:
            Sets the text content of the date input field.

        Passed arguments:
            date_str (str): The new date string to set.

        Returned objects:
            None

        Workflow:
            Sets the text of the internal date widget.

        Notes:
            None
        """

        self.date_widget.setText(date_str)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(
        FGDCDate, label="testing", show_format=False,
        parent_fgdc_name="fgdc_sngdate"
    )
