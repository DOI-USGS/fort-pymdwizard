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
    from PyQt5.QtCore import QUrl
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.gui.ui_files import UI_Preview
except ImportError as err:
    raise ImportError(err, __file__)


class Preview(QWidget):
    """
    Description:
        A simple widget used to display the HTML preview of the
        metadata record in an embedded web view component.

    Passed arguments:
        url (str, optional): The file path (URL) of the HTML file
            to display. Defaults to None.
        parent (QWidget, optional): The parent widget. Defaults to None.

    Returned objects:
        None

    Workflow:
        1. Initializes the base QWidget and sets up the UI.
        2. If a URL is provided, it loads the HTML file into the
           `QWebEngineView` (referred to as `webView` in the UI).

    Notes:
        Inherits from "QWidget".
    """

    def __init__(self, url=None, parent=None):
        # Initialize the base class (QWidget).
        QWidget.__init__(self, parent=parent)

        # Assuming UI_Preview is the auto-generated class.
        self.ui = UI_Preview.Ui_Form()
        self.ui.setupUi(self)

        # Store the URL path.
        self.url = url
        if url:
            # Load the local HTML file into the web view.
            self.ui.webView.setUrl(QUrl.fromLocalFile(self.url))


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Preview, "Preview", url=r"c:/temp/text.html")
