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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QUrl

from pymdwizard.core import utils

from pymdwizard.gui.ui_files import UI_Preview


class Preview(QWidget):
    def __init__(self, url=None, parent=None):
        QWidget.__init__(self, parent=parent)
        self.ui = UI_Preview.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.url = url
        if url:
            self.ui.webView.setUrl(QUrl.fromLocalFile(self.url))


if __name__ == "__main__":
    utils.launch_widget(Preview, "Preview", url=r"c:/temp/text.html")
