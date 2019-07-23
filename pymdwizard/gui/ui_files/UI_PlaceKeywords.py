# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PlaceKeywords.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_place_keywords(object):
    def setupUi(self, place_keywords):
        place_keywords.setObjectName("place_keywords")
        place_keywords.resize(600, 427)
        place_keywords.setStyleSheet(
            "QLabel{\n"
            'font: 9pt "Arial";\n'
            "color: rgb(90, 90, 90);\n"
            "}\n"
            "\n"
            "QLineEdit {\n"
            'font: 9pt "Arial";\n'
            "color: rgb(50, 50, 50);\n"
            "}"
        )
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(place_keywords)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.fgdc_place = QtWidgets.QGroupBox(place_keywords)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_place.sizePolicy().hasHeightForWidth())
        self.fgdc_place.setSizePolicy(sizePolicy)
        self.fgdc_place.setStyleSheet("QGroupBox{ font: 11pt } ")
        self.fgdc_place.setObjectName("fgdc_place")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.fgdc_place)
        self.verticalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.fgdc_keywords = QtWidgets.QWidget(self.fgdc_place)
        self.fgdc_keywords.setObjectName("fgdc_keywords")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.fgdc_keywords)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_7.setContentsMargins(2, 6, 2, 2)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.fgdc_keywords)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setStyleSheet("font: bold;")
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_4.addItem(spacerItem)
        self.rbtn_yes = QtWidgets.QRadioButton(self.fgdc_keywords)
        self.rbtn_yes.setAutoFillBackground(True)
        self.rbtn_yes.setChecked(False)
        self.rbtn_yes.setObjectName("rbtn_yes")
        self.horizontalLayout_4.addWidget(self.rbtn_yes)
        self.rbtn_no = QtWidgets.QRadioButton(self.fgdc_keywords)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtn_no.sizePolicy().hasHeightForWidth())
        self.rbtn_no.setSizePolicy(sizePolicy)
        self.rbtn_no.setAutoFillBackground(True)
        self.rbtn_no.setChecked(True)
        self.rbtn_no.setObjectName("rbtn_no")
        self.horizontalLayout_4.addWidget(self.rbtn_no)
        self.main_layout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.main_layout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_7.addLayout(self.main_layout)
        self.verticalLayout_9.addWidget(self.fgdc_keywords)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.verticalLayout_9.addItem(spacerItem1)
        self.place_contents = QtWidgets.QFrame(self.fgdc_place)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.place_contents.sizePolicy().hasHeightForWidth()
        )
        self.place_contents.setSizePolicy(sizePolicy)
        self.place_contents.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.place_contents.setFrameShadow(QtWidgets.QFrame.Raised)
        self.place_contents.setObjectName("place_contents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.place_contents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.place_contents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setStyleSheet(
            "QGroupBox{ \n"
            'font: 75 10pt "Arial";\n'
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
            "}"
        )
        self.groupBox_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_search_term_5.sizePolicy().hasHeightForWidth()
        )
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
        self.horizontalLayout_2.addWidget(self.label_search_term_5)
        spacerItem2 = QtWidgets.QSpacerItem(
            10, 29, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btn_search_controlled = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_search_controlled.setObjectName("btn_search_controlled")
        self.horizontalLayout_2.addWidget(self.btn_search_controlled)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_search_term_4 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_search_term_4.sizePolicy().hasHeightForWidth()
        )
        self.label_search_term_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_4.setFont(font)
        self.label_search_term_4.setObjectName("label_search_term_4")
        self.verticalLayout_2.addWidget(self.label_search_term_4)
        self.placekt = QtWidgets.QLineEdit(self.groupBox_2)
        self.placekt.setObjectName("placekt")
        self.verticalLayout_2.addWidget(self.placekt)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_search_term = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_search_term.sizePolicy().hasHeightForWidth()
        )
        self.label_search_term.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term.setFont(font)
        self.label_search_term.setObjectName("label_search_term")
        self.verticalLayout.addWidget(self.label_search_term)
        self.placekey = QtWidgets.QLineEdit(self.groupBox_2)
        self.placekey.setObjectName("placekey")
        self.verticalLayout.addWidget(self.placekey)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(
            24, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_4.addItem(spacerItem4)
        self.btn_add_custom = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_add_custom.setObjectName("btn_add_custom")
        self.verticalLayout_4.addWidget(self.btn_add_custom)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.place = QtWidgets.QTreeView(self.place_contents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.place.sizePolicy().hasHeightForWidth())
        self.place.setSizePolicy(sizePolicy)
        self.place.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.place.setFont(font)
        self.place.setStyleSheet(
            "QTreeView:item:has-children {\n"
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
            "}"
        )
        self.place.setLineWidth(1)
        self.place.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.place.setAlternatingRowColors(False)
        self.place.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.place.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.place.setIndentation(30)
        self.place.setAnimated(True)
        self.place.setHeaderHidden(False)
        self.place.setObjectName("place")
        self.verticalLayout_3.addWidget(self.place)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem5)
        self.btn_remove_keywords = QtWidgets.QPushButton(self.place_contents)
        self.btn_remove_keywords.setObjectName("btn_remove_keywords")
        self.horizontalLayout.addWidget(self.btn_remove_keywords)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_9.addWidget(self.place_contents)
        self.verticalLayout_8.addWidget(self.fgdc_place)

        self.retranslateUi(place_keywords)
        QtCore.QMetaObject.connectSlotsByName(place_keywords)

    def retranslateUi(self, place_keywords):
        _translate = QtCore.QCoreApplication.translate
        place_keywords.setWindowTitle(_translate("place_keywords", "ITIS Search"))
        self.fgdc_place.setTitle(
            _translate("place_keywords", "Place Keywords (Grouped by Thesaurus):  ")
        )
        self.label.setText(
            _translate(
                "place_keywords",
                "Are there any Place Keywords associated with this dataset?",
            )
        )
        self.rbtn_yes.setText(_translate("place_keywords", "Yes"))
        self.rbtn_no.setText(_translate("place_keywords", "No"))
        self.groupBox_2.setTitle(
            _translate("place_keywords", "Tools for adding Place Keywords:")
        )
        self.label_search_term_5.setText(
            _translate(
                "place_keywords",
                '<html><head/><body><p><span style=" font-style:italic;">We recommend that use keywords from a controlled vocabulary where possible -&gt;</span></p></body></html>',
            )
        )
        self.btn_search_controlled.setToolTip(
            _translate(
                "place_keywords", "Perform search of USGS Controlled Vocabularies"
            )
        )
        self.btn_search_controlled.setText(
            _translate("place_keywords", "Search Controlled Vocabularies")
        )
        self.label_search_term_4.setText(
            _translate("place_keywords", "Place Keyword Thesaurus:")
        )
        self.placekt.setToolTip(
            _translate("place_keywords", "terms to search ITIS for")
        )
        self.placekt.setText(_translate("place_keywords", "None"))
        self.label_search_term.setText(
            _translate("place_keywords", "Add Free-Text Place Keyword:")
        )
        self.placekey.setToolTip(
            _translate("place_keywords", "terms to search ITIS for")
        )
        self.btn_add_custom.setToolTip(
            _translate("place_keywords", "Add Custom Keyword")
        )
        self.btn_add_custom.setText(_translate("place_keywords", "Add Custom Keyword"))
        self.btn_remove_keywords.setText(
            _translate("place_keywords", "Remove Selected Keywords")
        )
