# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Keywords.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_keyword_widget(object):
    def setupUi(self, keyword_widget):
        keyword_widget.setObjectName("keyword_widget")
        keyword_widget.resize(534, 75)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(keyword_widget.sizePolicy().hasHeightForWidth())
        keyword_widget.setSizePolicy(sizePolicy)
        keyword_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        keyword_widget.setAcceptDrops(True)
        keyword_widget.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(60, 60, 60);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(keyword_widget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fgdc_keywords = QtWidgets.QGroupBox(keyword_widget)
        self.fgdc_keywords.setObjectName("fgdc_keywords")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.fgdc_keywords)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_search_term_5 = QtWidgets.QLabel(self.fgdc_keywords)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_search_term_5.sizePolicy().hasHeightForWidth())
        self.label_search_term_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_5.setFont(font)
        self.label_search_term_5.setTextFormat(QtCore.Qt.RichText)
        self.label_search_term_5.setWordWrap(True)
        self.label_search_term_5.setObjectName("label_search_term_5")
        self.verticalLayout.addWidget(self.label_search_term_5)
        self.verticalLayout_2.addWidget(self.fgdc_keywords)

        self.retranslateUi(keyword_widget)
        QtCore.QMetaObject.connectSlotsByName(keyword_widget)

    def retranslateUi(self, keyword_widget):
        _translate = QtCore.QCoreApplication.translate
        keyword_widget.setWindowTitle(_translate("keyword_widget", "Form"))
        self.fgdc_keywords.setTitle(_translate("keyword_widget", "Keywords"))
        self.label_search_term_5.setText(_translate("keyword_widget", "<html><head/><body><p><span style=\" font-style:italic;\">Keywords are often used in the search function of GIS data portals and data clearinghouses. Provide a list of descriptive keywords related to the content of your dataset.</span></p></body></html>"))

