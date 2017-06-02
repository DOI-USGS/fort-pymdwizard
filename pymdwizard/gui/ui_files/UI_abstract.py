# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'abstract.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(592, 240)
        Form.setMinimumSize(QtCore.QSize(0, 120))
        Form.setMaximumSize(QtCore.QSize(16777215, 240))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.parent = QtWidgets.QGroupBox(Form)
        self.parent.setObjectName("parent")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.parent)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.parent)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("font: italic;")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fgdc_abstract = QtWidgets.QPlainTextEdit(self.parent)
        self.fgdc_abstract.setAcceptDrops(False)
        self.fgdc_abstract.setPlainText("")
        self.fgdc_abstract.setOverwriteMode(False)
        self.fgdc_abstract.setObjectName("fgdc_abstract")
        self.verticalLayout_2.addWidget(self.fgdc_abstract)
        self.verticalLayout.addWidget(self.parent)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.parent.setTitle(_translate("Form", "Abstract"))
        self.label.setText(_translate("Form", "Provide a description of the data set."))

