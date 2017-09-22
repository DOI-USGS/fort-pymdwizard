# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_list.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_error_list(object):
    def setupUi(self, error_list):
        error_list.setObjectName("error_list")
        error_list.resize(645, 429)
        self.verticalLayout = QtWidgets.QVBoxLayout(error_list)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(error_list)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(error_list)
        QtCore.QMetaObject.connectSlotsByName(error_list)

    def retranslateUi(self, error_list):
        _translate = QtCore.QCoreApplication.translate
        error_list.setWindowTitle(_translate("error_list", "Form"))

