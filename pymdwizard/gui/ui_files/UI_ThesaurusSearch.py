# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ThesaurusSearch.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ThesaurusSearch(object):
    def setupUi(self, ThesaurusSearch):
        ThesaurusSearch.setObjectName("ThesaurusSearch")
        ThesaurusSearch.resize(516, 487)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ThesaurusSearch)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(ThesaurusSearch)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 5, 5, 7)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_search_term = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_search_term.setFont(font)
        self.label_search_term.setObjectName("label_search_term")
        self.horizontalLayout.addWidget(self.label_search_term)
        self.search_term = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.search_term.setObjectName("search_term")
        self.horizontalLayout.addWidget(self.search_term)
        self.button_search = QtWidgets.QPushButton(self.layoutWidget_2)
        self.button_search.setObjectName("button_search")
        self.horizontalLayout.addWidget(self.button_search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_search_results = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_search_results.setFont(font)
        self.label_search_results.setObjectName("label_search_results")
        self.horizontalLayout_6.addWidget(self.label_search_results)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.treeview_results = QtWidgets.QTreeView(self.layoutWidget_2)
        self.treeview_results.setStyleSheet("QTreeView:item:has-children {\n"
"\n"
"color: rgb(90, 90, 190);\n"
"font: 400 29.3pt \"Segoe UI\";\n"
"}\n"
"\n"
"QTreeView:item:!has-children {\n"
"font: 9px;\n"
"color: rgb(190, 90, 90);\n"
"}\n"
"\n"
"QTreeView::item:selected {\n"
"    background-color:  rgb(190, 190, 90);\n"
"    color: white;\n"
"}")
        self.treeview_results.setLineWidth(1)
        self.treeview_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeview_results.setAlternatingRowColors(False)
        self.treeview_results.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeview_results.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeview_results.setIndentation(30)
        self.treeview_results.setAnimated(True)
        self.treeview_results.setHeaderHidden(True)
        self.treeview_results.setObjectName("treeview_results")
        self.verticalLayout.addWidget(self.treeview_results)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_search_results_3 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_search_results_3.setFont(font)
        self.label_search_results_3.setObjectName("label_search_results_3")
        self.horizontalLayout_8.addWidget(self.label_search_results_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.textBrowser = QtWidgets.QTextBrowser(self.layoutWidget_2)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btn_add_term = QtWidgets.QPushButton(self.layoutWidget_2)
        self.btn_add_term.setObjectName("btn_add_term")
        self.horizontalLayout_3.addWidget(self.btn_add_term)
        spacerItem3 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.btn_close = QtWidgets.QPushButton(self.layoutWidget_2)
        self.btn_close.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_3.addWidget(self.btn_close)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.splitter)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(ThesaurusSearch)
        QtCore.QMetaObject.connectSlotsByName(ThesaurusSearch)

    def retranslateUi(self, ThesaurusSearch):
        _translate = QtCore.QCoreApplication.translate
        ThesaurusSearch.setWindowTitle(_translate("ThesaurusSearch", "Dialog"))
        self.label_search_term.setText(_translate("ThesaurusSearch", "Search Term:"))
        self.search_term.setToolTip(_translate("ThesaurusSearch", "terms to search ITIS for"))
        self.button_search.setToolTip(_translate("ThesaurusSearch", "Perform search of ITIS"))
        self.button_search.setText(_translate("ThesaurusSearch", "Search"))
        self.label_search_results.setToolTip(_translate("ThesaurusSearch", "Results from the ITIS common or scientific name search"))
        self.label_search_results.setText(_translate("ThesaurusSearch", "Search Results:"))
        self.label_search_results_3.setToolTip(_translate("ThesaurusSearch", "Results from the ITIS common or scientific name search"))
        self.label_search_results_3.setText(_translate("ThesaurusSearch", "Details:"))
        self.btn_add_term.setToolTip(_translate("ThesaurusSearch", "Add the selected item above to the list of include species (right)"))
        self.btn_add_term.setText(_translate("ThesaurusSearch", "Add Selection"))
        self.btn_close.setText(_translate("ThesaurusSearch", "Close"))

