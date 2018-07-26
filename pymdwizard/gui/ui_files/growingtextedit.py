#!/usr/bin/python3
import textwrap

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter


class GrowingTextEdit(QPlainTextEdit):
    """
    Custom QPlainTextEdit Widget that resizes
    to fit the contents dynamically
    """

    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.highlighter = Highlighter(self.document())
        self.heightMin = 45
        self.heightMax = 300

        self.setFixedHeight(self.heightMin)

    def resizeEvent(self, e):
        super(GrowingTextEdit, self).resizeEvent(e)
        self.sizeChange()

    def sizeChange(self):
        """
        When the string in this widget is updated resize to contain the
        appropriate number of lines displayed.

        returns: None
        """
        self.setUpdatesEnabled(False)
        contents = self.toPlainText()
        lines = contents.split('\n')

        adj_doc_height = 25
        for line in lines:
            width = self.fontMetrics().boundingRect(line).width()
            if width and (self.width()-10) > 0:
                adj_doc_height += (round(width/(self.width()-10))+1) * self.fontMetrics().height()
            else:
                adj_doc_height += self.fontMetrics().height()

        if adj_doc_height <= self.heightMin:
            self.setFixedHeight(self.heightMin)
            size_hint = self.heightMin
        elif self.heightMin <= adj_doc_height <= self.heightMax:
            self.setFixedHeight(adj_doc_height)
            size_hint = adj_doc_height
        elif adj_doc_height > self.heightMax:
            self.setFixedHeight(self.heightMax)
            size_hint = self.heightMax

        try:
            self.item.setSizeHint(QSize(self.width(), size_hint + 100))
        except:
            pass

        self.setUpdatesEnabled(True)

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = GrowingTextEdit()
    led.show()
    sys.exit(app.exec_())
