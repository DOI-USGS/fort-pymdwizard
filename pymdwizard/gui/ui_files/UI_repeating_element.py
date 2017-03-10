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
        Form.resize(442, 375)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vertical_scroll = QtWidgets.QScrollArea(Form)
        self.vertical_scroll.setWidgetResizable(True)
        self.vertical_scroll.setObjectName("vertical_scroll")
        self.vertical_contents = QtWidgets.QWidget()
        self.vertical_contents.setGeometry(QtCore.QRect(0, 0, 438, 113))
        self.vertical_contents.setObjectName("vertical_contents")
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.vertical_contents)
        self.vertical_layout_2.setContentsMargins(3, 3, 3, 3)
        self.vertical_layout_2.setSpacing(3)
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout_2.addItem(spacerItem)
        self.vertical_scroll.setWidget(self.vertical_contents)
        self.verticalLayout.addWidget(self.vertical_scroll)
        self.horizontal_scroll = QtWidgets.QScrollArea(Form)
        self.horizontal_scroll.setWidgetResizable(True)
        self.horizontal_scroll.setObjectName("horizontal_scroll")
        self.horizontal_contents = QtWidgets.QWidget()
        self.horizontal_contents.setGeometry(QtCore.QRect(0, 0, 438, 113))
        self.horizontal_contents.setObjectName("horizontal_contents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontal_contents)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontal_scroll.setWidget(self.horizontal_contents)
        self.verticalLayout.addWidget(self.horizontal_scroll)
        self.tab_widget = QtWidgets.QTabWidget(Form)
        self.tab_widget.setElideMode(QtCore.Qt.ElideLeft)
        self.tab_widget.setObjectName("tab_widget")
        self.verticalLayout.addWidget(self.tab_widget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("button_layout")
        spacerItem2 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem2)
        self.addAnother = QtWidgets.QPushButton(Form)
        self.addAnother.setObjectName("addAnother")
        self.button_layout.addWidget(self.addAnother)
        self.popOff = QtWidgets.QPushButton(Form)
        self.popOff.setObjectName("popOff")
        self.button_layout.addWidget(self.popOff)
        self.verticalLayout_2.addLayout(self.button_layout)

        self.retranslateUi(Form)
        self.tab_widget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addAnother.setText(_translate("Form", "PushButton"))
        self.popOff.setText(_translate("Form", "PushButton"))

