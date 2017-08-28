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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(fgdc_attrdomv)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(fgdc_attrdomv)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(15, 0))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_3.setIndent(0)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.label_3.setToolTip(_translate("fgdc_attrdomv", "Required"))
        self.label_3.setText(_translate("fgdc_attrdomv", "<html><head/><body><p><span style=\" font-size:18pt; color:#55aaff;\">*</span></p></body></html>"))

