# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ThemeKeywords.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fgdc_keywords(object):
    def setupUi(self, fgdc_keywords):
        fgdc_keywords.setObjectName("fgdc_keywords")
        fgdc_keywords.resize(770, 472)
        fgdc_keywords.setStyleSheet("QLabel{\n"
"font: 9pt \"Arial\";\n"
"color: rgb(90, 90, 90);\n"
"}\n"
"\n"
"QLineEdit {\n"
"font: 9pt \"Arial\";\n"
"color: rgb(50, 50, 50);\n"
"}")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(fgdc_keywords)
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(fgdc_keywords)
        self.groupBox_2.setStyleSheet("QGroupBox{ \n"
"font: 75 12pt \"Arial\";\n"
"border: 1px solid black;\n"
"border-radius: 3px;\n"
"background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf);\n"
"} \n"
"\n"
"QLineEdit {\n"
"padding: 1px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 2px;\n"
"}")
        self.groupBox_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_search_term_5 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_5.setFont(font)
        self.label_search_term_5.setTextFormat(QtCore.Qt.RichText)
        self.label_search_term_5.setObjectName("label_search_term_5")
        self.horizontalLayout_2.addWidget(self.label_search_term_5)
        spacerItem = QtWidgets.QSpacerItem(108, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_search_controlled = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_search_controlled.setObjectName("btn_search_controlled")
        self.horizontalLayout_2.addWidget(self.btn_search_controlled)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(0, 5, 5, 7)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_search_term_3 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_3.setFont(font)
        self.label_search_term_3.setTextFormat(QtCore.Qt.RichText)
        self.label_search_term_3.setObjectName("label_search_term_3")
        self.horizontalLayout_8.addWidget(self.label_search_term_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.btn_browse_iso = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_browse_iso.setObjectName("btn_browse_iso")
        self.horizontalLayout_8.addWidget(self.btn_browse_iso)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.label_search_term_6 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_6.setFont(font)
        self.label_search_term_6.setTextFormat(QtCore.Qt.RichText)
        self.label_search_term_6.setObjectName("label_search_term_6")
        self.verticalLayout_5.addWidget(self.label_search_term_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_search_term_4 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_4.setFont(font)
        self.label_search_term_4.setObjectName("label_search_term_4")
        self.verticalLayout_2.addWidget(self.label_search_term_4)
        self.themekt = QtWidgets.QLineEdit(self.groupBox_2)
        self.themekt.setObjectName("themekt")
        self.verticalLayout_2.addWidget(self.themekt)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_search_term = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term.setFont(font)
        self.label_search_term.setObjectName("label_search_term")
        self.verticalLayout.addWidget(self.label_search_term)
        self.themekey = QtWidgets.QLineEdit(self.groupBox_2)
        self.themekey.setObjectName("themekey")
        self.verticalLayout.addWidget(self.themekey)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(24, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem3)
        self.btn_add_custom = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_add_custom.setObjectName("btn_add_custom")
        self.verticalLayout_4.addWidget(self.btn_add_custom)
        spacerItem4 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.fgdc_theme = QtWidgets.QGroupBox(fgdc_keywords)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_theme.sizePolicy().hasHeightForWidth())
        self.fgdc_theme.setSizePolicy(sizePolicy)
        self.fgdc_theme.setStyleSheet("QGroupBox{ font: 11pt } ")
        self.fgdc_theme.setObjectName("fgdc_theme")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.fgdc_theme)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.theme = QtWidgets.QTreeView(self.fgdc_theme)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.theme.setFont(font)
        self.theme.setStyleSheet("QTreeView:item:has-children {\n"
"\n"
"color: rgb(90, 90, 190);\n"
"}\n"
"\n"
"QTreeView:item:!has-children {\n"
"font: 9px;\n"
"color: rgb(56, 56, 70);\n"
"}\n"
"\n"
"QTreeView::item:selected {\n"
"    background-color:  rgb(158, 213, 76);\n"
"    color: white;\n"
"}")
        self.theme.setLineWidth(1)
        self.theme.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.theme.setAlternatingRowColors(False)
        self.theme.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.theme.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.theme.setIndentation(30)
        self.theme.setAnimated(True)
        self.theme.setHeaderHidden(False)
        self.theme.setObjectName("theme")
        self.verticalLayout_3.addWidget(self.theme)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.btn_remove_keywords = QtWidgets.QPushButton(self.fgdc_theme)
        self.btn_remove_keywords.setObjectName("btn_remove_keywords")
        self.horizontalLayout.addWidget(self.btn_remove_keywords)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_7.addWidget(self.fgdc_theme)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.retranslateUi(fgdc_keywords)
        QtCore.QMetaObject.connectSlotsByName(fgdc_keywords)

    def retranslateUi(self, fgdc_keywords):
        _translate = QtCore.QCoreApplication.translate
        fgdc_keywords.setWindowTitle(_translate("fgdc_keywords", "ITIS Search"))
        self.groupBox_2.setTitle(_translate("fgdc_keywords", "Tools for adding Theme Keywords:"))
        self.label_search_term_5.setText(_translate("fgdc_keywords", "<html><head/><body><p><span style=\" font-style:italic;\">We recommend that use keywords from a controlled vocabulary where possible -&gt;</span></p></body></html>"))
        self.btn_search_controlled.setToolTip(_translate("fgdc_keywords", "Perform search of USGS Controlled Vocabularies"))
        self.btn_search_controlled.setText(_translate("fgdc_keywords", "Search Controlled Vocabularies"))
        self.label_search_term_3.setText(_translate("fgdc_keywords", "<html><head/><body><p><span style=\" font-style:italic;\">We also recommend that you include at least one keyword from the ISO 19115 Topic Category -&gt;</span></p></body></html>"))
        self.btn_browse_iso.setToolTip(_translate("fgdc_keywords", "Add ISO 19115 keywords"))
        self.btn_browse_iso.setText(_translate("fgdc_keywords", "Browse ISO 19115"))
        self.label_search_term_6.setText(_translate("fgdc_keywords", "<html><head/><body><p><span style=\" font-style:italic;\">If the controlled vocabularies and ISO keywords are not sufficient you can also add free text keywords:</span></p></body></html>"))
        self.label_search_term_4.setText(_translate("fgdc_keywords", "Theme Keyword Thesaurus:"))
        self.themekt.setToolTip(_translate("fgdc_keywords", "terms to search ITIS for"))
        self.themekt.setText(_translate("fgdc_keywords", "None"))
        self.label_search_term.setText(_translate("fgdc_keywords", "Add Free-Text Theme Keyword:"))
        self.themekey.setToolTip(_translate("fgdc_keywords", "terms to search ITIS for"))
        self.btn_add_custom.setToolTip(_translate("fgdc_keywords", "Add Custom Keyword"))
        self.btn_add_custom.setText(_translate("fgdc_keywords", "Add Custom Keyword"))
        self.fgdc_theme.setTitle(_translate("fgdc_keywords", "Theme Keywords (Grouped by Thesaurus):  "))
        self.btn_remove_keywords.setText(_translate("fgdc_keywords", "Remove Selected Keywords"))

