# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crossref.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1125, 79)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fgdc_crossref = QtWidgets.QGroupBox(Form)
        self.fgdc_crossref.setObjectName("fgdc_crossref")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.fgdc_crossref)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_65 = QtWidgets.QLabel(self.fgdc_crossref)
        self.label_65.setStyleSheet("font: bold;")
        self.label_65.setObjectName("label_65")
        self.horizontalLayout_28.addWidget(self.label_65)
        spacerItem = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_28.addItem(spacerItem)
        self.radio_crossrefyes = QtWidgets.QRadioButton(self.fgdc_crossref)
        self.radio_crossrefyes.setObjectName("radio_crossrefyes")
        self.horizontalLayout_28.addWidget(self.radio_crossrefyes)
        self.radio_crossrefno = QtWidgets.QRadioButton(self.fgdc_crossref)
        self.radio_crossrefno.setChecked(True)
        self.radio_crossrefno.setObjectName("radio_crossrefno")
        self.horizontalLayout_28.addWidget(self.radio_crossrefno)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_28.addItem(spacerItem1)
        self.label_66 = QtWidgets.QLabel(self.fgdc_crossref)
        self.label_66.setStyleSheet("font: italic;")
        self.label_66.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_66.setObjectName("label_66")
        self.horizontalLayout_28.addWidget(self.label_66)
        self.verticalLayout_5.addLayout(self.horizontalLayout_28)
        self.crossref_widget = QtWidgets.QWidget(self.fgdc_crossref)
        self.crossref_widget.setObjectName("crossref_widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.crossref_widget)
        self.horizontalLayout_5.setContentsMargins(15, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5.addWidget(self.crossref_widget)
        self.verticalLayout.addWidget(self.fgdc_crossref)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fgdc_crossref.setTitle(_translate("Form", "Cross Reference"))
        self.label_65.setText(_translate("Form", "Are there related data sets or publications that you would like to add a reference for? "))
        self.radio_crossrefyes.setText(_translate("Form", "Yes"))
        self.radio_crossrefno.setText(_translate("Form", "No"))
        self.label_66.setText(_translate("Form", " "))

