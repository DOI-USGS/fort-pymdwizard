#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GrowingTextEdit(QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)

        self.heightMin = 25
        self.heightMax = 400

        self.setMinimumHeight(self.heightMin)

    def sizeChange(self):
        docHeight = self.document().size().height()
        factor = 14
        if self.heightMin <= docHeight*factor <= self.heightMax:
            self.setMinimumHeight(docHeight*factor)
        elif docHeight*factor > self.heightMax:
            self.setMinimumHeight(self.heightMax)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = GrowingTextEdit()
    led.show()
    sys.exit(app.exec_())
