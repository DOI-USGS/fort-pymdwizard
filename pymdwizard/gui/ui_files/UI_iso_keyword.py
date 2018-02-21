# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'iso_keyword.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(222, 20)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fgdc_themekey = QtWidgets.QComboBox(Form)
        self.fgdc_themekey.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.fgdc_themekey.setObjectName("fgdc_themekey")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.fgdc_themekey.addItem("")
        self.verticalLayout.addWidget(self.fgdc_themekey)

        self.retranslateUi(Form)
        self.fgdc_themekey.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fgdc_themekey.setItemText(0, _translate("Form", "farming"))
        self.fgdc_themekey.setItemText(1, _translate("Form", "biota"))
        self.fgdc_themekey.setItemText(2, _translate("Form", "boundaries"))
        self.fgdc_themekey.setItemText(3, _translate("Form", "climatologyMeteorologyAtmosphere"))
        self.fgdc_themekey.setItemText(4, _translate("Form", "economy"))
        self.fgdc_themekey.setItemText(5, _translate("Form", "elevation"))
        self.fgdc_themekey.setItemText(6, _translate("Form", "environment"))
        self.fgdc_themekey.setItemText(7, _translate("Form", "geoscientificInformation"))
        self.fgdc_themekey.setItemText(8, _translate("Form", "health"))
        self.fgdc_themekey.setItemText(9, _translate("Form", "imageryBaseMapsEarthCover"))
        self.fgdc_themekey.setItemText(10, _translate("Form", "intelligenceMilitary"))
        self.fgdc_themekey.setItemText(11, _translate("Form", "inlandWaters"))
        self.fgdc_themekey.setItemText(12, _translate("Form", "location"))
        self.fgdc_themekey.setItemText(13, _translate("Form", "oceans"))
        self.fgdc_themekey.setItemText(14, _translate("Form", "planningCadastre"))
        self.fgdc_themekey.setItemText(15, _translate("Form", "society"))
        self.fgdc_themekey.setItemText(16, _translate("Form", "structure"))
        self.fgdc_themekey.setItemText(17, _translate("Form", "transportation"))
        self.fgdc_themekey.setItemText(18, _translate("Form", "utilitiesCommunication"))

