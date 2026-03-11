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
    from PyQt5.QtWidgets import QWidget
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_iso_keyword
except ImportError as err:
    raise ImportError(err, __file__)


class IsoKeyword(QWidget):
    """
    Description:
        A widget for entering an ISO 19115 keyword (e.g., a specific
        key word or phrase) within the metadata. Inherits from QWidget.

    Passed arguments:
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        Initializes the UI elements provided by "UI_iso_keyword".

    Notes:
        This widget is often used inside a repeating list or part of a
        larger keyword container (e.g., Keywords).
    """

    def __init__(self, parent=None):
        # Initialize the parent QWidget class.
        QWidget.__init__(self, parent=parent)

        # Instantiate the UI class.
        self.ui = UI_iso_keyword.Ui_Form()

        # Set up the UI components on the widget instance.
        self.ui.setupUi(self)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(IsoKeyword, "IsoKeyword")
