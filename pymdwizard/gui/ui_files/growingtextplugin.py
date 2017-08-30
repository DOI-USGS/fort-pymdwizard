#!/usr/bin/python3

from PyQt5.QtGui import QIcon
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

import pymdwizard


class GrowingTextEditPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(GrowingTextEditPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return pymdwizard.gui.ui_files.growingtextedit.GrowingTextEdit(parent)

    def name(self):
        return "GrowingTextEdit"

    def group(self):
        return "MDWIZ Custom Widgets"

    def icon(self):
        return QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def includeFile(self):
        return "growingtextedit"

from PyQt5.QtWidgets import *
if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = pymdwizard.gui.ui_files.growingtextedit.GrowingTextEdit()
    led.show()
    sys.exit(app.exec_())