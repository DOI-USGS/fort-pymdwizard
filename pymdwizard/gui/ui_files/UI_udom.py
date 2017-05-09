# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'udom.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fgdc_attrdomv(object):
    def setupUi(self, fgdc_attrdomv):
        fgdc_attrdomv.setObjectName("fgdc_attrdomv")
        fgdc_attrdomv.resize(426, 442)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(fgdc_attrdomv.sizePolicy().hasHeightForWidth())
        fgdc_attrdomv.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(fgdc_attrdomv)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(fgdc_attrdomv)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.fgdc_udom = QtWidgets.QPlainTextEdit(fgdc_attrdomv)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_udom.sizePolicy().hasHeightForWidth())
        self.fgdc_udom.setSizePolicy(sizePolicy)
        self.fgdc_udom.setObjectName("fgdc_udom")
        self.verticalLayout.addWidget(self.fgdc_udom)

        self.retranslateUi(fgdc_attrdomv)
        QtCore.QMetaObject.connectSlotsByName(fgdc_attrdomv)

    def retranslateUi(self, fgdc_attrdomv):
        _translate = QtCore.QCoreApplication.translate
        fgdc_attrdomv.setWindowTitle(_translate("fgdc_attrdomv", "Form"))
        self.label.setText(_translate("fgdc_attrdomv", "Enter a Description of the Values Recorded in the Field"))

