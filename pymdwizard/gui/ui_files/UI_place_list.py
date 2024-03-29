# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'place_list.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_place_keywords(object):
    def setupUi(self, place_keywords):
        place_keywords.setObjectName("place_keywords")
        place_keywords.resize(668, 427)
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
        self.help_place = QtWidgets.QGroupBox(place_keywords)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_place.sizePolicy().hasHeightForWidth())
        self.help_place.setSizePolicy(sizePolicy)
        self.help_place.setStyleSheet("QGroupBox{ font: 11pt } ")
        self.help_place.setObjectName("help_place")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.help_place)
        self.verticalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.keywords = QtWidgets.QWidget(self.help_place)
        self.keywords.setObjectName("keywords")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.keywords)
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
        self.label = QtWidgets.QLabel(self.keywords)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setStyleSheet("font: bold;")
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_4.addItem(spacerItem)
        self.rbtn_yes = QtWidgets.QRadioButton(self.keywords)
        self.rbtn_yes.setAutoFillBackground(True)
        self.rbtn_yes.setChecked(False)
        self.rbtn_yes.setObjectName("rbtn_yes")
        self.horizontalLayout_4.addWidget(self.rbtn_yes)
        self.rbtn_no = QtWidgets.QRadioButton(self.keywords)
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
        self.verticalLayout_9.addWidget(self.keywords)
        self.place_contents = QtWidgets.QFrame(self.help_place)
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
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.widget = QtWidgets.QWidget(self.place_contents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_search_term_5 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
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
        self.verticalLayout.addWidget(self.label_search_term_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_add_thesaurus = QtWidgets.QPushButton(self.widget)
        self.btn_add_thesaurus.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_add_thesaurus.setFont(font)
        self.btn_add_thesaurus.setStyleSheet("")
        self.btn_add_thesaurus.setObjectName("btn_add_thesaurus")
        self.horizontalLayout_3.addWidget(self.btn_add_thesaurus)
        self.btn_remove_selected = QtWidgets.QPushButton(self.widget)
        self.btn_remove_selected.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_remove_selected.setFont(font)
        self.btn_remove_selected.setStyleSheet("")
        self.btn_remove_selected.setObjectName("btn_remove_selected")
        self.horizontalLayout_3.addWidget(self.btn_remove_selected)
        spacerItem1 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6.addWidget(self.widget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame = QtWidgets.QFrame(self.place_contents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(
            "QFrame{ \n"
            'font: 75 10pt "Arial";\n'
            "border: 1px solid black;\n"
            "border-radius: 3px;\n"
            "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf);\n"
            "} "
        )
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btn_search_controlled = QtWidgets.QPushButton(self.frame)
        self.btn_search_controlled.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_search_controlled.setFont(font)
        self.btn_search_controlled.setStyleSheet("")
        self.btn_search_controlled.setObjectName("btn_search_controlled")
        self.verticalLayout_5.addWidget(self.btn_search_controlled)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_4.addWidget(self.frame)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.theme_tabs = QtWidgets.QTabWidget(self.place_contents)
        self.theme_tabs.setObjectName("theme_tabs")
        self.verticalLayout_3.addWidget(self.theme_tabs)
        self.verticalLayout_9.addWidget(self.place_contents)
        self.verticalLayout_8.addWidget(self.help_place)

        self.retranslateUi(place_keywords)
        QtCore.QMetaObject.connectSlotsByName(place_keywords)

    def retranslateUi(self, place_keywords):
        _translate = QtCore.QCoreApplication.translate
        place_keywords.setWindowTitle(_translate("place_keywords", "ITIS Search"))
        self.help_place.setTitle(
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
        self.label_search_term_5.setText(
            _translate(
                "place_keywords",
                '<html><head/><body><p><span style=" font-style:italic;">We recommend to use keywords from a controlled vocabulary where possible -&gt;</span></p></body></html>',
            )
        )
        self.btn_add_thesaurus.setText(
            _translate("place_keywords", "Add New Thesaurus")
        )
        self.btn_remove_selected.setText(
            _translate("place_keywords", "Remove Selected")
        )
        self.btn_search_controlled.setText(
            _translate("place_keywords", "Search \n" "Controlled Vocabularies")
        )
