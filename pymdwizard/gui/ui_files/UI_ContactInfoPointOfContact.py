# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContactInfoPointOfContact.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_USGSContactInfoWidgetMain(object):
    def setupUi(self, USGSContactInfoWidgetMain):
        USGSContactInfoWidgetMain.setObjectName(_fromUtf8("USGSContactInfoWidgetMain"))
        USGSContactInfoWidgetMain.resize(530, 90)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(USGSContactInfoWidgetMain.sizePolicy().hasHeightForWidth())
        USGSContactInfoWidgetMain.setSizePolicy(sizePolicy)
        USGSContactInfoWidgetMain.setMaximumSize(QtCore.QSize(16777215, 16777215))
        USGSContactInfoWidgetMain.setAcceptDrops(True)
        USGSContactInfoWidgetMain.setStyleSheet(_fromUtf8("font: 9pt \"Arial\";\n"
"color: rgb(60, 60, 60);"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(USGSContactInfoWidgetMain)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_2.setMargin(6)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(USGSContactInfoWidgetMain)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_3.setContentsMargins(2, 6, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(_fromUtf8("main_layout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setStyleSheet(_fromUtf8("font: bold;"))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.rbtn_yes = QtGui.QRadioButton(self.groupBox)
        self.rbtn_yes.setAutoFillBackground(True)
        self.rbtn_yes.setObjectName(_fromUtf8("rbtn_yes"))
        self.horizontalLayout.addWidget(self.rbtn_yes)
        self.rbtn_no = QtGui.QRadioButton(self.groupBox)
        self.rbtn_no.setAutoFillBackground(True)
        self.rbtn_no.setChecked(True)
        self.rbtn_no.setObjectName(_fromUtf8("rbtn_no"))
        self.horizontalLayout.addWidget(self.rbtn_no)
        self.main_layout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setStyleSheet(_fromUtf8("font: italic;"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.main_layout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setStyleSheet(_fromUtf8("font: italic;"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.main_layout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.main_layout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.main_layout)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(USGSContactInfoWidgetMain)
        QtCore.QMetaObject.connectSlotsByName(USGSContactInfoWidgetMain)

    def retranslateUi(self, USGSContactInfoWidgetMain):
        USGSContactInfoWidgetMain.setWindowTitle(_translate("USGSContactInfoWidgetMain", "Form", None))
        self.label.setText(_translate("USGSContactInfoWidgetMain", "Is there a contact person or agency for this dataset?", None))
        self.rbtn_yes.setText(_translate("USGSContactInfoWidgetMain", "Yes", None))
        self.rbtn_no.setText(_translate("USGSContactInfoWidgetMain", "No", None))
        self.label_3.setText(_translate("USGSContactInfoWidgetMain", "Having a data set contact is very helpful.", None))
        self.label_2.setText(_translate("USGSContactInfoWidgetMain", "This is someone who could be contacted for questions about the dataset.", None))

