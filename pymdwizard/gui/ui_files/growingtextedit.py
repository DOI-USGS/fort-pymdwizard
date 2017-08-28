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
        factor = 13
        if self.heightMin <= docHeight*factor <= self.heightMax:
            self.setMinimumHeight(docHeight*factor + 8)
        elif docHeight*factor > self.heightMax:
            self.setMinimumHeight(self.heightMax)

        try:
            self.item.setSizeHint(QSize(self.width(), self.minimumHeight()+120))
        except:
            pass


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = GrowingTextEdit()
    led.show()
    sys.exit(app.exec_())
