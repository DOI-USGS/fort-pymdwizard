# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proccont.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_USGSContactInfoWidgetMain(object):
    def setupUi(self, USGSContactInfoWidgetMain):
        USGSContactInfoWidgetMain.setObjectName("USGSContactInfoWidgetMain")
        USGSContactInfoWidgetMain.resize(530, 114)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(USGSContactInfoWidgetMain.sizePolicy().hasHeightForWidth())
        USGSContactInfoWidgetMain.setSizePolicy(sizePolicy)
        USGSContactInfoWidgetMain.setMaximumSize(QtCore.QSize(16777215, 16777215))
        USGSContactInfoWidgetMain.setAcceptDrops(True)
        USGSContactInfoWidgetMain.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(USGSContactInfoWidgetMain)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fgdc_ptcontac = QtWidgets.QGroupBox(USGSContactInfoWidgetMain)
        self.fgdc_ptcontac.setObjectName("fgdc_ptcontac")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.fgdc_ptcontac)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.fgdc_ptcontac)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setStyleSheet("font: bold;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.rbtn_yes = QtWidgets.QRadioButton(self.fgdc_ptcontac)
        self.rbtn_yes.setAutoFillBackground(True)
        self.rbtn_yes.setChecked(True)
        self.rbtn_yes.setObjectName("rbtn_yes")
        self.horizontalLayout.addWidget(self.rbtn_yes)
        self.rbtn_no = QtWidgets.QRadioButton(self.fgdc_ptcontac)
        self.rbtn_no.setAutoFillBackground(True)
        self.rbtn_no.setChecked(False)
        self.rbtn_no.setObjectName("rbtn_no")
        self.horizontalLayout.addWidget(self.rbtn_no)
        self.main_layout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.fgdc_ptcontac)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setStyleSheet("font: italic;")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.main_layout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.main_layout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.main_layout)
        self.verticalLayout_2.addWidget(self.fgdc_ptcontac)

        self.retranslateUi(USGSContactInfoWidgetMain)
        QtCore.QMetaObject.connectSlotsByName(USGSContactInfoWidgetMain)

    def retranslateUi(self, USGSContactInfoWidgetMain):
        _translate = QtCore.QCoreApplication.translate
        USGSContactInfoWidgetMain.setWindowTitle(_translate("USGSContactInfoWidgetMain", "Form"))
        self.fgdc_ptcontac.setTitle(_translate("USGSContactInfoWidgetMain", "Process Step Contact"))
        self.label.setText(_translate("USGSContactInfoWidgetMain", "Is there a contact person or agency for this processing step?"))
        self.rbtn_yes.setText(_translate("USGSContactInfoWidgetMain", "Yes"))
        self.rbtn_no.setText(_translate("USGSContactInfoWidgetMain", "No"))
        self.label_2.setText(_translate("USGSContactInfoWidgetMain", "This is a resource for questions regarding the process undertaken."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    USGSContactInfoWidgetMain = QtWidgets.QWidget()
    ui = Ui_USGSContactInfoWidgetMain()
    ui.setupUi(USGSContactInfoWidgetMain)
    USGSContactInfoWidgetMain.show()
    sys.exit(app.exec_())

