# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataCredit.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(453, 267)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.fgdc_datacred = QtWidgets.QPlainTextEdit(Form)
        self.fgdc_datacred.setAcceptDrops(False)
        self.fgdc_datacred.setPlainText("")
        self.fgdc_datacred.setOverwriteMode(True)
        self.fgdc_datacred.setObjectName("fgdc_datacred")
        self.gridLayout.addWidget(self.fgdc_datacred, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Data Set Credit(s)"))
        self.label.setText(_translate("Form", "Are there other organizations / individuals who should get credit for support, funding, data collection, or analysis?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

