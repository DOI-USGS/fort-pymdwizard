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
        Form.resize(592, 109)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 100))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fgdc_descript = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_descript.sizePolicy().hasHeightForWidth())
        self.fgdc_descript.setSizePolicy(sizePolicy)
        self.fgdc_descript.setObjectName("fgdc_descript")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fgdc_descript)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.fgdc_descript)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("font: italic;")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fgdc_supplinf = GrowingTextEdit(self.fgdc_descript)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_supplinf.sizePolicy().hasHeightForWidth())
        self.fgdc_supplinf.setSizePolicy(sizePolicy)
        self.fgdc_supplinf.setMinimumSize(QtCore.QSize(0, 35))
        self.fgdc_supplinf.setObjectName("fgdc_supplinf")
        self.verticalLayout_2.addWidget(self.fgdc_supplinf)
        self.verticalLayout.addWidget(self.fgdc_descript)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fgdc_descript.setTitle(_translate("Form", "Supplemental Information"))
        self.label.setText(_translate("Form", "Use this optional section to add ANY other details or information about the dataset that may be helpful to future users."))

from growingtextedit import GrowingTextEdit
