# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'supplinf.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(592, 133)
        Form.setMinimumSize(QtCore.QSize(0, 100))
        Form.setMaximumSize(QtCore.QSize(16777215, 133))
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
        self.fgdc_supplinf = QtWidgets.QPlainTextEdit(self.fgdc_descript)
        self.fgdc_supplinf.setAcceptDrops(False)
        self.fgdc_supplinf.setPlainText("")
        self.fgdc_supplinf.setOverwriteMode(False)
        self.fgdc_supplinf.setObjectName("fgdc_supplinf")
        self.verticalLayout_2.addWidget(self.fgdc_supplinf)
        self.verticalLayout.addWidget(self.fgdc_descript)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fgdc_descript.setTitle(_translate("Form", "Supplemental Information"))
        self.label.setText(_translate("Form", "Use this optional section to add ANY other details or information about the data set that may be helpful to future users."))

