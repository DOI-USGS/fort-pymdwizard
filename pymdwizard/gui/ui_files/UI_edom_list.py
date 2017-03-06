# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edom_list.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fgdc_udom(object):
    def setupUi(self, fgdc_udom):
        fgdc_udom.setObjectName("fgdc_udom")
        fgdc_udom.resize(620, 740)
        self.verticalLayout = QtWidgets.QVBoxLayout(fgdc_udom)
        self.verticalLayout.setContentsMargins(2, 9, 2, 4)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(fgdc_udom)
        self.label.setWordWrap(True)
        self.label.setIndent(9)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(fgdc_udom)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setAutoFillBackground(True)
        self.listWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listWidget.setMidLineWidth(0)
        self.listWidget.setAutoScrollMargin(25)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.frame = QtWidgets.QFrame(fgdc_udom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_addone = QtWidgets.QPushButton(self.frame)
        self.btn_addone.setObjectName("btn_addone")
        self.horizontalLayout.addWidget(self.btn_addone)
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_delete = QtWidgets.QPushButton(self.frame)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(fgdc_udom)
        QtCore.QMetaObject.connectSlotsByName(fgdc_udom)

    def retranslateUi(self, fgdc_udom):
        _translate = QtCore.QCoreApplication.translate
        fgdc_udom.setWindowTitle(_translate("fgdc_udom", "Form"))
        self.label.setText(_translate("fgdc_udom", "For each unique value contained in this column, provide a definition below."))
        self.btn_addone.setText(_translate("fgdc_udom", "Add"))
        self.btn_delete.setText(_translate("fgdc_udom", "Delete"))

