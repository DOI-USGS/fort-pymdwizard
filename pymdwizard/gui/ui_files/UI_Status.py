# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Status.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(268, 234)
        Form.setMinimumSize(QtCore.QSize(268, 234))
        Form.setMaximumSize(QtCore.QSize(268, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.update = QtWidgets.QComboBox(self.groupBox)
        self.update.setGeometry(QtCore.QRect(30, 161, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.update.setFont(font)
        self.update.setObjectName("update")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.update.addItem("")
        self.progress = QtWidgets.QComboBox(self.groupBox)
        self.progress.setGeometry(QtCore.QRect(30, 80, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.progress.setFont(font)
        self.progress.setEditable(False)
        self.progress.setObjectName("progress")
        self.progress.addItem("")
        self.progress.addItem("")
        self.progress.addItem("")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 251, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.update.setItemText(0, _translate("Form", "Continually"))
        self.update.setItemText(1, _translate("Form", "Daily"))
        self.update.setItemText(2, _translate("Form", "Weekly"))
        self.update.setItemText(3, _translate("Form", "Monthly"))
        self.update.setItemText(4, _translate("Form", "Annually"))
        self.update.setItemText(5, _translate("Form", "Unknown"))
        self.update.setItemText(6, _translate("Form", "As needed"))
        self.update.setItemText(7, _translate("Form", "Irregular"))
        self.update.setItemText(8, _translate("Form", "None planned"))
        self.progress.setCurrentText(_translate("Form", "Complete"))
        self.progress.setItemText(0, _translate("Form", "Complete"))
        self.progress.setItemText(1, _translate("Form", "In Work"))
        self.progress.setItemText(2, _translate("Form", "Planned"))
        self.label.setText(_translate("Form", "Data Status and Update Plans"))
        self.label_2.setText(_translate("Form", "Status"))
        self.label_3.setText(_translate("Form", "Update Plans"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

