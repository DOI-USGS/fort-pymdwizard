# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'repeating_element.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(271, 52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 0)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_widget.sizePolicy().hasHeightForWidth())
        self.button_widget.setSizePolicy(sizePolicy)
        self.button_widget.setObjectName("button_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.button_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.italic_label = QtWidgets.QLabel(self.button_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.italic_label.sizePolicy().hasHeightForWidth())
        self.italic_label.setSizePolicy(sizePolicy)
        self.italic_label.setStyleSheet("font: italic;")
        self.italic_label.setText("")
        self.italic_label.setObjectName("italic_label")
        self.horizontalLayout.addWidget(self.italic_label)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addAnother = QtWidgets.QPushButton(self.button_widget)
        self.addAnother.setObjectName("addAnother")
        self.horizontalLayout.addWidget(self.addAnother)
        self.popOff = QtWidgets.QPushButton(self.button_widget)
        self.popOff.setObjectName("popOff")
        self.horizontalLayout.addWidget(self.popOff)
        self.verticalLayout_2.addWidget(self.button_widget)
        self.tab_widget = QtWidgets.QTabWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)
        self.tab_widget.setStyleSheet("")
        self.tab_widget.setElideMode(QtCore.Qt.ElideNone)
        self.tab_widget.setObjectName("tab_widget")
        self.verticalLayout_2.addWidget(self.tab_widget)
        self.vertical_widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vertical_widget.sizePolicy().hasHeightForWidth())
        self.vertical_widget.setSizePolicy(sizePolicy)
        self.vertical_widget.setMinimumSize(QtCore.QSize(0, 1))
        self.vertical_widget.setObjectName("vertical_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.vertical_widget)
        self.verticalLayout_4.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2.addWidget(self.vertical_widget)

        self.retranslateUi(Form)
        self.tab_widget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addAnother.setText(_translate("Form", "PushButton"))
        self.popOff.setText(_translate("Form", "PushButton"))

