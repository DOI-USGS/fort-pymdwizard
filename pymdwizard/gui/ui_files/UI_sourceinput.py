# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sourceinput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(632, 207)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_2.addWidget(self.radioButton)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.frame_sourceinfo = QtWidgets.QFrame(self.groupBox)
        self.frame_sourceinfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sourceinfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sourceinfo.setObjectName("frame_sourceinfo")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_sourceinfo)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.frame_sourceinfo)
        spacerItem = QtWidgets.QSpacerItem(20, 67, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Source inputs Used to Create the Data Set"))
        self.radioButton.setText(_translate("Form", "No Sources were used.\n"
"The data set represents 100% original content, derived first-hand (e.g. field collection, lab experiments, etc.)"))
        self.radioButton_2.setText(_translate("Form", "The source inputs are described below (reference imagery/material, assorted GIS inputs, etc.)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

