# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'theme_list.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_theme_list(object):
    def setupUi(self, theme_list):
        theme_list.setObjectName("theme_list")
        theme_list.resize(608, 461)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(theme_list.sizePolicy().hasHeightForWidth())
        theme_list.setSizePolicy(sizePolicy)
        theme_list.setToolTip("")
        theme_list.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(theme_list)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.help_theme = QtWidgets.QGroupBox(theme_list)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_theme.sizePolicy().hasHeightForWidth())
        self.help_theme.setSizePolicy(sizePolicy)
        self.help_theme.setObjectName("help_theme")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.help_theme)
        self.verticalLayout_5.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_3 = QtWidgets.QWidget(self.help_theme)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
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
        self.label_search_term_3 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_search_term_3.sizePolicy().hasHeightForWidth()
        )
        self.label_search_term_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_3.setFont(font)
        self.label_search_term_3.setTextFormat(QtCore.Qt.RichText)
        self.label_search_term_3.setWordWrap(True)
        self.label_search_term_3.setObjectName("label_search_term_3")
        self.verticalLayout.addWidget(self.label_search_term_3)
        self.label_search_term_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_search_term_6.setFont(font)
        self.label_search_term_6.setTextFormat(QtCore.Qt.RichText)
        self.label_search_term_6.setWordWrap(True)
        self.label_search_term_6.setObjectName("label_search_term_6")
        self.verticalLayout.addWidget(self.label_search_term_6)
        spacerItem = QtWidgets.QSpacerItem(
            20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.verticalLayout.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addWidget(self.widget)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.widget_3)
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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
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
        self.verticalLayout_4.addWidget(self.btn_search_controlled)
        self.btn_add_iso = QtWidgets.QPushButton(self.frame)
        self.btn_add_iso.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_add_iso.setFont(font)
        self.btn_add_iso.setStyleSheet("")
        self.btn_add_iso.setObjectName("btn_add_iso")
        self.verticalLayout_4.addWidget(self.btn_add_iso)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addWidget(self.frame)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5.addWidget(self.widget_3)
        self.widget1 = QtWidgets.QWidget(self.help_theme)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.widget1.setObjectName("widget1")
        self.contents_layout = QtWidgets.QVBoxLayout(self.widget1)
        self.contents_layout.setContentsMargins(0, 0, 0, 0)
        self.contents_layout.setSpacing(0)
        self.contents_layout.setObjectName("contents_layout")
        self.theme_tabs = QtWidgets.QTabWidget(self.widget1)
        self.theme_tabs.setObjectName("theme_tabs")
        self.fgdc_theme = QtWidgets.QWidget()
        self.fgdc_theme.setObjectName("fgdc_theme")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.fgdc_theme)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget2 = QtWidgets.QWidget(self.fgdc_theme)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget2.sizePolicy().hasHeightForWidth())
        self.widget2.setSizePolicy(sizePolicy)
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.thesaurus_label = QtWidgets.QLabel(self.widget2)
        self.thesaurus_label.setObjectName("thesaurus_label")
        self.horizontalLayout_2.addWidget(self.thesaurus_label)
        self.fgdc_themekt = QtWidgets.QLineEdit(self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_themekt.sizePolicy().hasHeightForWidth())
        self.fgdc_themekt.setSizePolicy(sizePolicy)
        self.fgdc_themekt.setMinimumSize(QtCore.QSize(125, 0))
        self.fgdc_themekt.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_themekt.setReadOnly(True)
        self.fgdc_themekt.setPlaceholderText("")
        self.fgdc_themekt.setObjectName("fgdc_themekt")
        self.horizontalLayout_2.addWidget(self.fgdc_themekt)
        self.verticalLayout_6.addWidget(self.widget2)
        self.iso_keywords_layout = QtWidgets.QVBoxLayout()
        self.iso_keywords_layout.setObjectName("iso_keywords_layout")
        self.verticalLayout_6.addLayout(self.iso_keywords_layout)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_6.addItem(spacerItem4)
        self.theme_tabs.addTab(self.fgdc_theme, "")
        self.contents_layout.addWidget(self.theme_tabs)
        self.verticalLayout_5.addWidget(self.widget1)
        self.verticalLayout_2.addWidget(self.help_theme)

        self.retranslateUi(theme_list)
        QtCore.QMetaObject.connectSlotsByName(theme_list)

    def retranslateUi(self, theme_list):
        _translate = QtCore.QCoreApplication.translate
        theme_list.setWindowTitle(_translate("theme_list", "Form"))
        self.help_theme.setTitle(_translate("theme_list", "Theme Keywords"))
        self.label_search_term_5.setText(
            _translate(
                "theme_list",
                '<html><head/><body><p><span style=" font-style:italic;">We recommend to use keywords from a controlled vocabulary where possible -&gt;</span></p></body></html>',
            )
        )
        self.label_search_term_3.setText(
            _translate(
                "theme_list",
                '<html><head/><body><p><span style=" font-style:italic;">We also recommend that you include at least one keyword from the ISO 19115 Topic Category -&gt;</span></p></body></html>',
            )
        )
        self.label_search_term_6.setText(
            _translate(
                "theme_list",
                '<html><head/><body><p><span style=" font-style:italic;">If the controlled vocabularies and ISO keywords are not sufficient you can also add free text keywords:</span></p></body></html>',
            )
        )
        self.btn_add_thesaurus.setText(_translate("theme_list", "Add New Thesaurus"))
        self.btn_remove_selected.setText(_translate("theme_list", "Remove Selected"))
        self.btn_search_controlled.setText(
            _translate("theme_list", "Search \n" "Controlled Vocabularies")
        )
        self.btn_add_iso.setText(_translate("theme_list", "Add ISO 19115"))
        self.thesaurus_label.setText(_translate("theme_list", "Thesaurus"))
        self.fgdc_themekt.setToolTip(
            _translate(
                "theme_list",
                "Contact Person -- the name of the individual to which the contact type applies.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntper",
            )
        )
        self.fgdc_themekt.setText(_translate("theme_list", "ISO 19115 Topic Category"))
        self.theme_tabs.setTabText(
            self.theme_tabs.indexOf(self.fgdc_theme),
            _translate("theme_list", "ISO 19115"),
        )
