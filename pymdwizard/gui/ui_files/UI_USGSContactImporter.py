# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'USGSContactImporter.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportUsgsUser(object):
    def setupUi(self, ImportUsgsUser):
        ImportUsgsUser.setObjectName("ImportUsgsUser")
        ImportUsgsUser.resize(489, 97)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImportUsgsUser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.le_usgs_ad_name = QtWidgets.QLineEdit(ImportUsgsUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_usgs_ad_name.sizePolicy().hasHeightForWidth())
        self.le_usgs_ad_name.setSizePolicy(sizePolicy)
        self.le_usgs_ad_name.setMinimumSize(QtCore.QSize(0, 0))
        self.le_usgs_ad_name.setObjectName("le_usgs_ad_name")
        self.verticalLayout.addWidget(self.le_usgs_ad_name)
        self.label = QtWidgets.QLabel(ImportUsgsUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("font: italic;")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(ImportUsgsUser)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ImportUsgsUser)
        QtCore.QMetaObject.connectSlotsByName(ImportUsgsUser)

    def retranslateUi(self, ImportUsgsUser):
        _translate = QtCore.QCoreApplication.translate
        ImportUsgsUser.setWindowTitle(_translate("ImportUsgsUser", "Import Contact Info from USGS Active Directory"))
        self.label.setText(_translate("ImportUsgsUser", "Enter a valid USGS user name or email address"))

