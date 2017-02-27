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
        self.fgdc_udom = QtWidgets.QTextBrowser(udom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_udom.sizePolicy().hasHeightForWidth())
        self.fgdc_udom.setSizePolicy(sizePolicy)
        self.fgdc_udom.setReadOnly(False)
        self.fgdc_udom.setObjectName("fgdc_udom")
        self.verticalLayout.addWidget(self.fgdc_udom)
        self.label_2 = QtWidgets.QLabel(udom_widget)
        self.label_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet("font: bold;")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(udom_widget)
        self.label_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet("font: italic;")
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.retranslateUi(udom_widget)
        QtCore.QMetaObject.connectSlotsByName(udom_widget)

    def retranslateUi(self, udom_widget):
        _translate = QtCore.QCoreApplication.translate
        udom_widget.setWindowTitle(_translate("udom_widget", "Form"))
        self.label.setText(_translate("udom_widget", "Enter a Description of the Values Recorded in the Field"))
        self.label_2.setText(_translate("udom_widget", "\"Unrepresentable Domain\""))
        self.label_3.setText(_translate("udom_widget", "This attribute type should be used for any attribute value that is not a codeset, an enumerated domain, or a range. When uncertain about which domain type should be used, this is often a good option. Clearly explain what a field represents to assist future data users. If a description is simple, it may be appropriate to have the same text in the \'Attribute Definition\' and the free text description of the field. \n"
"\n"
"Examples: name of a data technician, dates, notes, free text descriptions/entries, etc."))

