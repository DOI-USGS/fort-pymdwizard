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
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.ui = UI_iso_keyword.Ui_Form()

        self.ui.setupUi(self)


if __name__ == "__main__":
    utils.launch_widget(IsoKeyword, "IsoKeyword")
