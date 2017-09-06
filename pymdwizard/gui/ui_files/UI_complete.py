# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'complete.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(599, 131)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("font: italic;")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fgdc_complete = GrowingTextEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_complete.sizePolicy().hasHeightForWidth())
        self.fgdc_complete.setSizePolicy(sizePolicy)
        self.fgdc_complete.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_complete.setObjectName("fgdc_complete")
        self.verticalLayout_2.addWidget(self.fgdc_complete)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Completeness Report"))
        self.label.setText(_translate("Form", "Does the dataset represent only certain types of instances of a phenomenon?   Do the data represent occurrences only within a fixed geographic area?   Provide information about what is included in the dataset versus what is not.   See help for more info."))
        self.fgdc_complete.setPlainText(_translate("Form", "Dataset is considered complete for the information presented, as described in the abstract.  Users are advised to read the rest of the metadata record carefully for additional details."))

from growingtextedit import GrowingTextEdit
