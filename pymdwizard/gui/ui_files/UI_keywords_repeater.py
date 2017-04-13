# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keywords_repeater.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(312, 69)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.thesaurus_label = QtWidgets.QLabel(Form)
        self.thesaurus_label.setObjectName("thesaurus_label")
        self.horizontalLayout.addWidget(self.thesaurus_label)
        self.fgdc_themekt = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_themekt.sizePolicy().hasHeightForWidth())
        self.fgdc_themekt.setSizePolicy(sizePolicy)
        self.fgdc_themekt.setMinimumSize(QtCore.QSize(125, 0))
        self.fgdc_themekt.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_themekt.setText("")
        self.fgdc_themekt.setPlaceholderText("")
        self.fgdc_themekt.setObjectName("fgdc_themekt")
        self.horizontalLayout.addWidget(self.fgdc_themekt)
        self.required_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.required_2.sizePolicy().hasHeightForWidth())
        self.required_2.setSizePolicy(sizePolicy)
        self.required_2.setMinimumSize(QtCore.QSize(15, 0))
        self.required_2.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.required_2.setFont(font)
        self.required_2.setScaledContents(True)
        self.required_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.required_2.setIndent(0)
        self.required_2.setObjectName("required_2")
        self.horizontalLayout.addWidget(self.required_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.keywords_layout = QtWidgets.QVBoxLayout()
        self.keywords_layout.setObjectName("keywords_layout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.keywords_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.keywords_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.thesaurus_label.setText(_translate("Form", "Thesaurus"))
        self.fgdc_themekt.setToolTip(_translate("Form", "Contact Person -- the name of the individual to which the contact type applies.\n"
"Type: text\n"
"Domain: free text\n"
"Short Name: cntper"))
        self.required_2.setToolTip(_translate("Form", "Required"))
        self.required_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt; color:#55aaff;\">*</span></p></body></html>"))

