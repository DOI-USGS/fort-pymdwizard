# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogicalAccuracy.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(585, 160)
        Form.setMinimumSize(QtCore.QSize(0, 160))
        Form.setMaximumSize(QtCore.QSize(16777215, 180))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("font: italic;")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fgdc_logic = QtWidgets.QPlainTextEdit(self.groupBox)
        self.fgdc_logic.setAcceptDrops(False)
        self.fgdc_logic.setOverwriteMode(True)
        self.fgdc_logic.setObjectName("fgdc_logic")
        self.verticalLayout_2.addWidget(self.fgdc_logic)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Logical Accuracy Report"))
        self.label.setText(_translate("Form", "Does the actual data match up with the details you have provided about it?   Do all values fall within expected ranges?   Have you checked for data duplication/omission?   Were topology tests conducted to ensure the integrity of geospatial data?   See help for more info."))
        self.fgdc_logic.setPlainText(_translate("Form", "No formal logical accuracy tests were conducted."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

