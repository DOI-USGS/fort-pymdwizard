# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UseConstraints.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(597, 267)
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
        self.fgdc_useconst = QtWidgets.QPlainTextEdit(Form)
        self.fgdc_useconst.setAcceptDrops(False)
        self.fgdc_useconst.setOverwriteMode(True)
        self.fgdc_useconst.setObjectName("fgdc_useconst")
        self.gridLayout.addWidget(self.fgdc_useconst, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Data Use Constraints"))
        self.label.setText(_translate("Form", "Describe any restrictions or legal prerequisites for USING the data set.  Use Constraints may include restrictions applied to assure the protection of privacy or intellectual property, and any special restrictions or limitations on using the data set."))
        self.fgdc_useconst.setPlainText(_translate("Form", "None.  Users are advised to read the data set\'s metadata thoroughly to understand appropriate use and data limitations."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

