# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PositionalAccuracy.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 233)
        Form.setMinimumSize(QtCore.QSize(0, 120))
        Form.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fg_dc_possacc = QtWidgets.QGroupBox(Form)
        self.fg_dc_possacc.setObjectName("fg_dc_possacc")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.fg_dc_possacc)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.fg_dc_possacc)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fgdc_horizpa = QtWidgets.QPlainTextEdit(self.fg_dc_possacc)
        self.fgdc_horizpa.setAcceptDrops(False)
        self.fgdc_horizpa.setOverwriteMode(True)
        self.fgdc_horizpa.setObjectName("fgdc_horizpa")
        self.verticalLayout_2.addWidget(self.fgdc_horizpa)
        self.label_2 = QtWidgets.QLabel(self.fg_dc_possacc)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.fgdc_vertacc = QtWidgets.QPlainTextEdit(self.fg_dc_possacc)
        self.fgdc_vertacc.setAcceptDrops(False)
        self.fgdc_vertacc.setOverwriteMode(True)
        self.fgdc_vertacc.setObjectName("fgdc_vertacc")
        self.verticalLayout_2.addWidget(self.fgdc_vertacc)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.fg_dc_possacc)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fg_dc_possacc.setTitle(_translate("Form", "Positional Accuracy"))
        self.label.setText(_translate("Form", "Horizontal Accuracy Report"))
        self.fgdc_horizpa.setPlainText(_translate("Form", "A formal accuracy assessment of the horizontal positional information in the dataset has not been conducted."))
        self.label_2.setText(_translate("Form", "Vertical Accuracy Report"))
        self.fgdc_vertacc.setPlainText(_translate("Form", "A formal accuracy assessment of the vertical positional information in the dataset has either not been conducted, or is not applicable."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

