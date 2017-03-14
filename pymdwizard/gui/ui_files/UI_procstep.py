# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procstep.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(529, 311)
        Form.setMinimumSize(QtCore.QSize(0, 270))
        Form.setMaximumSize(QtCore.QSize(16777215, 435))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_procstep = QtWidgets.QFrame(self.groupBox)
        self.frame_procstep.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_procstep.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_procstep.setObjectName("frame_procstep")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_procstep)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2.addWidget(self.frame_procstep)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Process Step"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

