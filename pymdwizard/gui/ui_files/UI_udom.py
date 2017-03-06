# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'udom.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_udom_widget(object):
    def setupUi(self, udom_widget):
        udom_widget.setObjectName("udom_widget")
        udom_widget.resize(171, 442)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(udom_widget.sizePolicy().hasHeightForWidth())
        udom_widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(udom_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(udom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.fgdc_udom = QtWidgets.QPlainTextEdit(udom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_udom.sizePolicy().hasHeightForWidth())
        self.fgdc_udom.setSizePolicy(sizePolicy)
        self.fgdc_udom.setObjectName("fgdc_udom")
        self.verticalLayout.addWidget(self.fgdc_udom)

        self.retranslateUi(udom_widget)
        QtCore.QMetaObject.connectSlotsByName(udom_widget)

    def retranslateUi(self, udom_widget):
        _translate = QtCore.QCoreApplication.translate
        udom_widget.setWindowTitle(_translate("udom_widget", "Form"))
        self.label.setText(_translate("udom_widget", "Enter a Description of the Values Recorded in the Field"))

