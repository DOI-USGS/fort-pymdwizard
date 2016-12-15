# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'USGSContactImporter.ui'
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

class Ui_ImportUsgsUser(object):
    def setupUi(self, ImportUsgsUser):
        ImportUsgsUser.setObjectName(_fromUtf8("ImportUsgsUser"))
        ImportUsgsUser.resize(489, 97)
        self.verticalLayout = QtGui.QVBoxLayout(ImportUsgsUser)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.le_usgs_ad_name = QtGui.QLineEdit(ImportUsgsUser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_usgs_ad_name.sizePolicy().hasHeightForWidth())
        self.le_usgs_ad_name.setSizePolicy(sizePolicy)
        self.le_usgs_ad_name.setMinimumSize(QtCore.QSize(0, 0))
        self.le_usgs_ad_name.setObjectName(_fromUtf8("le_usgs_ad_name"))
        self.verticalLayout.addWidget(self.le_usgs_ad_name)
        self.label = QtGui.QLabel(ImportUsgsUser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("font: italic;"))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(ImportUsgsUser)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ImportUsgsUser)
        QtCore.QMetaObject.connectSlotsByName(ImportUsgsUser)

    def retranslateUi(self, ImportUsgsUser):
        ImportUsgsUser.setWindowTitle(_translate("ImportUsgsUser", "Import Contact Info from USGS Active Directory", None))
        self.label.setText(_translate("ImportUsgsUser", "Enter a valid USGS user name or email address", None))

