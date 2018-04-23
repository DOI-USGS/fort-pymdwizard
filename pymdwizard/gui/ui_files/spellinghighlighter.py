from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QApplication
import re

from pymdwizard.core import utils

fname = utils.get_resource_path("spelling/words.txt")
try:
    wordup = set(line.strip() for line in open(fname, 'r'))
except UnicodeDecodeError:
    wordup = set(line.strip() for line in open(fname, 'r', encoding='latin-1'))


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.sectionFormat = QtGui.QTextCharFormat()
        self.sectionFormat.setForeground(QtCore.Qt.blue)
        self.errorFormat = QtGui.QTextCharFormat()
        self.errorFormat.setForeground(QtCore.Qt.red)
        self.errorFormat.setBackground(QtCore.Qt.yellow)

        self.enabled = True

    def highlightBlock(self, text):
        if not self.enabled:
            return None

        words = re.findall(r"[\w]+", text)

        for word in words:
            if word.lower() not in wordup and \
                    re.search('[a-zA-Z]', word) is not None:
                clean = ' ' + re.sub(r"[^a-zA-Z]", " ", text) + ' '
                try:
                    self.setFormat(clean.index(" {} ".format(word)), len(word),
                                       self.errorFormat)
                except ValueError:
                    pass


class TestWindow(QWidget):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.editor = QTextEdit(self)
        self.highlighter = Highlighter(self.editor.document())
        self.editor.setText("""There is a spellling error here!""")
        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = TestWindow()
    window.setGeometry(500, 150, 300, 300)
    window.show()
    sys.exit(app.exec_())