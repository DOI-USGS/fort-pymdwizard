# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'purpose.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(592, 150)
        Form.setMinimumSize(QtCore.QSize(0, 110))
        Form.setMaximumSize(QtCore.QSize(16777215, 150))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fgdc_descript = QtWidgets.QGroupBox(Form)
        self.fgdc_descript.setObjectName("fgdc_descript")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fgdc_descript)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.fgdc_descript)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("font: italic;")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fgdc_purpose = QtWidgets.QPlainTextEdit(self.fgdc_descript)
        self.fgdc_purpose.setAcceptDrops(False)
        self.fgdc_purpose.setPlainText("")
        self.fgdc_purpose.setOverwriteMode(False)
        self.fgdc_purpose.setObjectName("fgdc_purpose")
        self.verticalLayout_2.addWidget(self.fgdc_purpose)
        self.verticalLayout.addWidget(self.fgdc_descript)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fgdc_descript.setTitle(_translate("Form", "Purpose"))
        self.label.setText(_translate("Form", "Why were the data collected?  What is an appropriate use of the data?"))

