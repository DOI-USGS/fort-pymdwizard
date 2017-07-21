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

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    # def domXml(self):
    #     return '<widget class="PyAnalogClock" name="analogClock">\n' \
    #            ' <property name="toolTip">\n' \
    #            '  <string>The current time</string>\n' \
    #            ' </property>\n' \
    #            ' <property name="whatsThis">\n' \
    #            '  <string>The analog clock widget displays the current ' \
    #            'timewi.</string>\n' \
    #            ' </property>\n' \
    #            '</widget>\n'

    def includeFile(self):
        return "growingtextedit"

from PyQt5.QtWidgets import *
if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = pymdwizard.gui.ui_files.growingtextedit.GrowingTextEdit()
    led.show()
    sys.exit(app.exec_())