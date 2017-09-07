# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DOICiteinfoImporter.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportUsgsUser(object):
    def setupUi(self, ImportUsgsUser):
        ImportUsgsUser.setObjectName("ImportUsgsUser")
        ImportUsgsUser.resize(489, 82)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImportUsgsUser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
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
        self.horizontalLayout_2.addWidget(self.label)
        self.le_doi = QtWidgets.QLineEdit(ImportUsgsUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_doi.sizePolicy().hasHeightForWidth())
        self.le_doi.setSizePolicy(sizePolicy)
        self.le_doi.setMinimumSize(QtCore.QSize(0, 0))
        self.le_doi.setObjectName("le_doi")
        self.horizontalLayout_2.addWidget(self.le_doi)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_OK = QtWidgets.QPushButton(ImportUsgsUser)
        self.btn_OK.setObjectName("btn_OK")
        self.horizontalLayout.addWidget(self.btn_OK)
        self.btn_cancel = QtWidgets.QPushButton(ImportUsgsUser)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ImportUsgsUser)
        QtCore.QMetaObject.connectSlotsByName(ImportUsgsUser)

    def retranslateUi(self, ImportUsgsUser):
        _translate = QtCore.QCoreApplication.translate
        ImportUsgsUser.setWindowTitle(_translate("ImportUsgsUser", "DOI search"))
        self.label.setText(_translate("ImportUsgsUser", "Enter a valid (live) publication DOI"))
        self.btn_OK.setText(_translate("ImportUsgsUser", "OK"))
        self.btn_cancel.setText(_translate("ImportUsgsUser", "Cancel"))

