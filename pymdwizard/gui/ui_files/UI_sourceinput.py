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
        Form.resize(1125, 188)
        Form.setMinimumSize(QtCore.QSize(0, 100))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radio_sourceno_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radio_sourceno_2.setChecked(True)
        self.radio_sourceno_2.setObjectName("radio_sourceno_2")
        self.verticalLayout_2.addWidget(self.radio_sourceno_2)
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.line = QtWidgets.QFrame(self.splitter)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.line_2 = QtWidgets.QFrame(self.splitter)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.splitter)
        self.radio_sourceyes = QtWidgets.QRadioButton(self.groupBox)
        self.radio_sourceyes.setObjectName("radio_sourceyes")
        self.verticalLayout_2.addWidget(self.radio_sourceyes)
        self.frame_sourceinfo = QtWidgets.QFrame(self.groupBox)
        self.frame_sourceinfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sourceinfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sourceinfo.setObjectName("frame_sourceinfo")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_sourceinfo)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2.addWidget(self.frame_sourceinfo)
        spacerItem2 = QtWidgets.QSpacerItem(20, 67, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Source inputs Used to Create the Data Set"))
        self.radio_sourceno_2.setText(_translate("Form", "No Sources were used.  The data set represents 100% original content, derived first-hand (e.g. field collection, lab experiments, etc.)"))
        self.label.setText(_translate("Form", "OR"))
        self.radio_sourceyes.setText(_translate("Form", "The source inputs are described below (reference imagery/material, assorted GIS inputs, etc.)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

