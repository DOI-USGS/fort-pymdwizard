#!/usr/bin/python3
import textwrap

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GrowingTextEdit(QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)

        self.heightMin = 45
        self.heightMax = 300

        self.setFixedHeight(self.heightMin)

    def sizeChange(self):
        width = min(self.width(), 500)

        char_width = int(width/5.25)
        contents = self.toPlainText()
        lines = textwrap.wrap(contents, char_width)
        adj_doc_height = (len(lines) + contents.count('\n')) * 13 + 25

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


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = GrowingTextEdit()
    led.show()
    sys.exit(app.exec_())
