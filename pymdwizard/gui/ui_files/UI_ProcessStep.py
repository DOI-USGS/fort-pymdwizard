# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProcessStep.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(647, 242)
        Form.setMinimumSize(QtCore.QSize(0, 175))
        Form.setMaximumSize(QtCore.QSize(16777215, 280))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fgdc_procstep = QtWidgets.QGroupBox(Form)
        self.fgdc_procstep.setTitle("")
        self.fgdc_procstep.setObjectName("fgdc_procstep")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.fgdc_procstep)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.fgdc_procstep)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.fgdc_procdesc = QtWidgets.QPlainTextEdit(self.fgdc_procstep)
        self.fgdc_procdesc.setObjectName("fgdc_procdesc")
        self.verticalLayout.addWidget(self.fgdc_procdesc)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_37 = QtWidgets.QLabel(self.fgdc_procstep)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_2.addWidget(self.label_37)
        self.fgdc_procdate = QtWidgets.QWidget(self.fgdc_procstep)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_procdate.sizePolicy().hasHeightForWidth())
        self.fgdc_procdate.setSizePolicy(sizePolicy)
        self.fgdc_procdate.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_procdate.setMaximumSize(QtCore.QSize(221, 100))
        self.fgdc_procdate.setObjectName("fgdc_procdate")
        self.verticalLayout_2.addWidget(self.fgdc_procdate)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addWidget(self.fgdc_procstep)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Describe the processing step or method below:"))
        self.fgdc_procdesc.setPlainText(_translate("Form", "Development of the data set by the agency / individuals identified in the \'Originator\' element in the Identification Info section of the record."))
        self.label_37.setText(_translate("Form", "Publication Date (YYYYMMDD)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

