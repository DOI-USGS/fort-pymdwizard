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
        Form.resize(225, 21)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)

        self.retranslateUi(Form)
        self.comboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox.setItemText(0, _translate("Form", "farming"))
        self.comboBox.setItemText(1, _translate("Form", "biota"))
        self.comboBox.setItemText(2, _translate("Form", "boundaries"))
        self.comboBox.setItemText(3, _translate("Form", "climateologyMeteorologyAtmosphere"))
        self.comboBox.setItemText(4, _translate("Form", "economy"))
        self.comboBox.setItemText(5, _translate("Form", "elevation"))
        self.comboBox.setItemText(6, _translate("Form", "environment"))
        self.comboBox.setItemText(7, _translate("Form", "geoscientificInformation"))
        self.comboBox.setItemText(8, _translate("Form", "health"))
        self.comboBox.setItemText(9, _translate("Form", "imageryBaseMapsEarthCover"))
        self.comboBox.setItemText(10, _translate("Form", "intelligenceMilitary"))
        self.comboBox.setItemText(11, _translate("Form", "inlandWaters"))
        self.comboBox.setItemText(12, _translate("Form", "location"))
        self.comboBox.setItemText(13, _translate("Form", "oceans"))
        self.comboBox.setItemText(14, _translate("Form", "planningCadastre"))
        self.comboBox.setItemText(15, _translate("Form", "society"))
        self.comboBox.setItemText(16, _translate("Form", "structure"))
        self.comboBox.setItemText(17, _translate("Form", "transportation"))
        self.comboBox.setItemText(18, _translate("Form", "utilitiesCommunication"))

