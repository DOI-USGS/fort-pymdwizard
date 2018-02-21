# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edom_list.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_edom_contents(object):
    def setupUi(self, edom_contents):
        edom_contents.setObjectName("edom_contents")
        edom_contents.resize(539, 740)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(edom_contents.sizePolicy().hasHeightForWidth())
        edom_contents.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(edom_contents)
        self.verticalLayout.setContentsMargins(2, 9, 2, 4)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(edom_contents)
        self.label.setWordWrap(True)
        self.label.setIndent(9)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(edom_contents)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setAutoFillBackground(True)
        self.listWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listWidget.setMidLineWidth(0)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listWidget.setAutoScrollMargin(25)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget = QtWidgets.QWidget(edom_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_addone = QtWidgets.QPushButton(self.widget)
        self.btn_addone.setObjectName("btn_addone")
        self.horizontalLayout.addWidget(self.btn_addone)
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_delete = QtWidgets.QPushButton(self.widget)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(edom_contents)
        QtCore.QMetaObject.connectSlotsByName(edom_contents)

    def retranslateUi(self, edom_contents):
        _translate = QtCore.QCoreApplication.translate
        edom_contents.setWindowTitle(_translate("edom_contents", "Form"))
        self.label.setText(_translate("edom_contents", "For each unique value contained in this column, provide a definition below."))
        self.btn_addone.setText(_translate("edom_contents", "Add Value"))
        self.btn_delete.setText(_translate("edom_contents", "Delete Selected"))

