# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itis_search.ui'
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

class Ui_ItisSearchWidget(object):
    def setupUi(self, ItisSearchWidget):
        ItisSearchWidget.setObjectName(_fromUtf8("ItisSearchWidget"))
        ItisSearchWidget.resize(1010, 608)
        self.verticalLayout_4 = QtGui.QVBoxLayout(ItisSearchWidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(ItisSearchWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.horizontalLayoutWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.SpeciesToInclude = QtGui.QTableView(self.horizontalLayoutWidget)
        self.SpeciesToInclude.setObjectName(_fromUtf8("SpeciesToInclude"))
        self.verticalLayout_2.addWidget(self.SpeciesToInclude)
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 5, 10, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.search_term_label = QtGui.QLabel(self.widget)
        self.search_term_label.setObjectName(_fromUtf8("search_term_label"))
        self.horizontalLayout.addWidget(self.search_term_label)
        self.search_term = QtGui.QLineEdit(self.widget)
        self.search_term.setObjectName(_fromUtf8("search_term"))
        self.horizontalLayout.addWidget(self.search_term)
        self.search_term_label_2 = QtGui.QLabel(self.widget)
        self.search_term_label_2.setAccessibleName(_fromUtf8(""))
        self.search_term_label_2.setObjectName(_fromUtf8("search_term_label_2"))
        self.horizontalLayout.addWidget(self.search_term_label_2)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.search_itis_button = QtGui.QPushButton(self.widget)
        self.search_itis_button.setObjectName(_fromUtf8("search_itis_button"))
        self.horizontalLayout_2.addWidget(self.search_itis_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableView = QtGui.QTableView(self.widget)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout_3.addWidget(self.splitter)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gen_fgdc_button = QtGui.QPushButton(ItisSearchWidget)
        self.gen_fgdc_button.setObjectName(_fromUtf8("gen_fgdc_button"))
        self.horizontalLayout_3.addWidget(self.gen_fgdc_button)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(ItisSearchWidget)
        QtCore.QMetaObject.connectSlotsByName(ItisSearchWidget)

    def retranslateUi(self, ItisSearchWidget):
        ItisSearchWidget.setWindowTitle(_translate("ItisSearchWidget", "ITIS Search", None))
        self.label.setText(_translate("ItisSearchWidget", "Items to include:", None))
        self.search_term_label.setText(_translate("ItisSearchWidget", "Search Term:", None))
        self.search_term_label_2.setToolTip(_translate("ItisSearchWidget", "The type of ITIS search to perform (Scientific or Common name)", None))
        self.search_term_label_2.setText(_translate("ItisSearchWidget", "Search Type:", None))
        self.comboBox.setItemText(0, _translate("ItisSearchWidget", "Common name", None))
        self.comboBox.setItemText(1, _translate("ItisSearchWidget", "Scientific name", None))
        self.search_itis_button.setText(_translate("ItisSearchWidget", "Seach ITIS", None))
        self.gen_fgdc_button.setText(_translate("ItisSearchWidget", "Generate Taxonomy Section", None))

