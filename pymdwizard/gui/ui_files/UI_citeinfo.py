# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'citeinfo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_parent_form(object):
    def setupUi(self, parent_form):
        parent_form.setObjectName("parent_form")
        parent_form.resize(1093, 436)
        parent_form.setStyleSheet(
            "QGroupBox{\n"
            "    background-color: transparent;\n"
            "     subcontrol-position: top left; /* position at the top left*/\n"
            "     padding-top: 20px;\n"
            "    font: bold 12px;\n"
            "    color: rgba(90, 90, 90, 225);\n"
            "    border: 1px solid gray;\n"
            "    border-radius: 2px;\n"
            "    border-color: rgba(90, 90, 90, 40);\n"
            "}\n"
            "QGroupBox::title {\n"
            "text-align: left;\n"
            "subcontrol-origin: padding;\n"
            "subcontrol-position: top left; /* position at the top center */padding: 3 3px;\n"
            "}\n"
            "QLabel{\n"
            'font: 9pt "Arial";\n'
            "color: rgb(90, 90, 90);\n"
            "}\n"
            "QLineEdit, QComboBox {\n"
            'font: 9pt "Arial";\n'
            "color: rgb(50, 50, 50);\n"
            "}\n"
            "\n"
            "QGroupBox:Hover {\n"
            "    border-color: rgba(90, 90, 90, 240);\n"
            "}\n"
            "\n"
            "QHBoxLayout#import_doi_layout{\n"
            "subcontrol-position: top left; /* position at the top left*/\n"
            "     padding-top: 200px;\n"
            "}\n"
            "\n"
            ".QFrame {\n"
            "    color: rgba(90, 90, 90, 225);\n"
            "    border: 1px solid gray;\n"
            "    border-radius: 2px;\n"
            "    border-color: rgba(90, 90, 90, 75);\n"
            "}"
        )
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(parent_form)
        self.horizontalLayout_13.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_13.setSpacing(2)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.fgdc_citeinfo = QtWidgets.QGroupBox(parent_form)
        self.fgdc_citeinfo.setMinimumSize(QtCore.QSize(1000, 360))
        self.fgdc_citeinfo.setObjectName("fgdc_citeinfo")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.fgdc_citeinfo)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.first_hbox = QtWidgets.QHBoxLayout()
        self.first_hbox.setContentsMargins(-1, -1, 0, -1)
        self.first_hbox.setObjectName("first_hbox")
        self.help_title = QtWidgets.QFrame(self.fgdc_citeinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_title.sizePolicy().hasHeightForWidth())
        self.help_title.setSizePolicy(sizePolicy)
        self.help_title.setObjectName("help_title")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.help_title)
        self.verticalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setContentsMargins(9, 3, 9, 3)
        self.verticalLayout_10.setSpacing(3)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.lbl_dataset_title = QtWidgets.QLabel(self.help_title)
        self.lbl_dataset_title.setStyleSheet("font: bold;")
        self.lbl_dataset_title.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.lbl_dataset_title.setObjectName("lbl_dataset_title")
        self.verticalLayout_10.addWidget(self.lbl_dataset_title)
        self.label_34 = QtWidgets.QLabel(self.help_title)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setStyleSheet("font: italic;")
        self.label_34.setObjectName("label_34")
        self.verticalLayout_10.addWidget(self.label_34)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.fgdc_title = QtWidgets.QPlainTextEdit(self.help_title)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_title.sizePolicy().hasHeightForWidth())
        self.fgdc_title.setSizePolicy(sizePolicy)
        self.fgdc_title.setMaximumSize(QtCore.QSize(16777215, 54))
        self.fgdc_title.setStyleSheet('font: 11pt "Arial";\n' "color: rgb(50, 50, 50);")
        self.fgdc_title.setInputMethodHints(QtCore.Qt.ImhNone)
        self.fgdc_title.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fgdc_title.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fgdc_title.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.fgdc_title.setMaximumBlockCount(0)
        self.fgdc_title.setObjectName("fgdc_title")
        self.horizontalLayout_4.addWidget(self.fgdc_title)
        self.label_5 = QtWidgets.QLabel(self.help_title)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(15, 0))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_5.setIndent(0)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.verticalLayout_10.addLayout(self.horizontalLayout_4)
        self.verticalLayout_11.addLayout(self.verticalLayout_10)
        self.first_hbox.addWidget(self.help_title)
        self.help_pubdate = QtWidgets.QFrame(self.fgdc_citeinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_pubdate.sizePolicy().hasHeightForWidth())
        self.help_pubdate.setSizePolicy(sizePolicy)
        self.help_pubdate.setObjectName("help_pubdate")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.help_pubdate)
        self.verticalLayout_2.setContentsMargins(-1, 3, -1, 3)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_46 = QtWidgets.QLabel(self.help_pubdate)
        self.label_46.setStyleSheet("font: bold;")
        self.label_46.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.label_46.setObjectName("label_46")
        self.verticalLayout_2.addWidget(self.label_46)
        self.label_38 = QtWidgets.QLabel(self.help_pubdate)
        self.label_38.setStyleSheet("font: italic;")
        self.label_38.setObjectName("label_38")
        self.verticalLayout_2.addWidget(self.label_38)
        self.pubdate_layout = QtWidgets.QHBoxLayout()
        self.pubdate_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.pubdate_layout.setObjectName("pubdate_layout")
        spacerItem = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        self.pubdate_layout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.pubdate_layout)
        self.first_hbox.addWidget(self.help_pubdate)
        self.btn_import_doi = QtWidgets.QPushButton(self.fgdc_citeinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_doi.sizePolicy().hasHeightForWidth()
        )
        self.btn_import_doi.setSizePolicy(sizePolicy)
        self.btn_import_doi.setMinimumSize(QtCore.QSize(50, 0))
        self.btn_import_doi.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btn_import_doi.setStyleSheet(
            "QGroupBox{\n"
            "    background-color: transparent;\n"
            "     subcontrol-position: top left; /* position at the top left*/\n"
            "     padding-top: 20px;\n"
            "    font: bold 12px;\n"
            "    color: rgba(90, 90, 90, 225);\n"
            "    border: 1px solid gray;\n"
            "    border-radius: 2px;\n"
            "    border-color: rgba(90, 90, 90, 40);\n"
            "}\n"
            "QGroupBox::title {\n"
            "text-align: left;\n"
            "subcontrol-origin: padding;\n"
            "subcontrol-position: top left; /* position at the top center */padding: 3 3px;\n"
            "}\n"
            "QLabel{\n"
            'font: 9pt "Arial";\n'
            "color: rgb(90, 90, 90);\n"
            "}\n"
            "QLineEdit, QComboBox {\n"
            'font: 9pt "Arial";\n'
            "color: rgb(50, 50, 50);\n"
            "}\n"
            "\n"
            "QGroupBox:Hover {\n"
            "    border-color: rgba(90, 90, 90, 240);\n"
            "}\n"
            "\n"
            ".QFrame {\n"
            "    color: rgba(90, 90, 90, 225);\n"
            "    border: 1px solid gray;\n"
            "    border-radius: 2px;\n"
            "    border-color: rgba(90, 90, 90, 75);\n"
            "}"
        )
        self.btn_import_doi.setObjectName("btn_import_doi")
        self.first_hbox.addWidget(self.btn_import_doi)
        self.verticalLayout_4.addLayout(self.first_hbox)
        self.second_hbox = QtWidgets.QHBoxLayout()
        self.second_hbox.setSpacing(10)
        self.second_hbox.setObjectName("second_hbox")
        self.help_origin = QtWidgets.QFrame(self.fgdc_citeinfo)
        self.help_origin.setObjectName("help_origin")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.help_origin)
        self.verticalLayout_13.setContentsMargins(3, 3, 9, 3)
        self.verticalLayout_13.setSpacing(3)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_47 = QtWidgets.QLabel(self.help_origin)
        self.label_47.setStyleSheet("font: bold;")
        self.label_47.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.label_47.setObjectName("label_47")
        self.verticalLayout_13.addWidget(self.label_47)
        self.originator_layout = QtWidgets.QVBoxLayout()
        self.originator_layout.setObjectName("originator_layout")
        self.verticalLayout_13.addLayout(self.originator_layout)
        self.second_hbox.addWidget(self.help_origin)
        self.framex = QtWidgets.QFrame(self.fgdc_citeinfo)
        self.framex.setObjectName("framex")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.framex)
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.help_geoform = QtWidgets.QFrame(self.framex)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_geoform.sizePolicy().hasHeightForWidth())
        self.help_geoform.setSizePolicy(sizePolicy)
        self.help_geoform.setMinimumSize(QtCore.QSize(0, 75))
        self.help_geoform.setObjectName("help_geoform")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.help_geoform)
        self.verticalLayout_15.setContentsMargins(9, 3, 9, 6)
        self.verticalLayout_15.setSpacing(3)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_53 = QtWidgets.QLabel(self.help_geoform)
        self.label_53.setStyleSheet("font: bold;")
        self.label_53.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.label_53.setObjectName("label_53")
        self.verticalLayout_15.addWidget(self.label_53)
        self.label_36 = QtWidgets.QLabel(self.help_geoform)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy)
        self.label_36.setStyleSheet("font: italic;")
        self.label_36.setObjectName("label_36")
        self.verticalLayout_15.addWidget(self.label_36)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.fgdc_geoform = QtWidgets.QComboBox(self.help_geoform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.fgdc_geoform.setFont(font)
        self.fgdc_geoform.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.fgdc_geoform.setEditable(True)
        self.fgdc_geoform.setObjectName("fgdc_geoform")
        self.fgdc_geoform.addItem("")
        self.fgdc_geoform.addItem("")
        self.fgdc_geoform.addItem("")
        self.fgdc_geoform.addItem("")
        self.fgdc_geoform.addItem("")
        self.fgdc_geoform.addItem("")
        self.fgdc_geoform.addItem("")
        self.horizontalLayout_14.addWidget(self.fgdc_geoform)
        self.label_9 = QtWidgets.QLabel(self.help_geoform)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(15, 0))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setScaledContents(True)
        self.label_9.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_9.setIndent(0)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_14.addWidget(self.label_9)
        self.verticalLayout_15.addLayout(self.horizontalLayout_14)
        self.verticalLayout_7.addWidget(self.help_geoform)
        self.help_edition = QtWidgets.QFrame(self.framex)
        self.help_edition.setObjectName("help_edition")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.help_edition)
        self.horizontalLayout.setContentsMargins(-1, 3, 9, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_55 = QtWidgets.QLabel(self.help_edition)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy)
        self.label_55.setStyleSheet("font: bold;")
        self.label_55.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.label_55.setObjectName("label_55")
        self.horizontalLayout.addWidget(self.label_55)
        self.fgdc_edition = QtWidgets.QLineEdit(self.help_edition)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_edition.sizePolicy().hasHeightForWidth())
        self.fgdc_edition.setSizePolicy(sizePolicy)
        self.fgdc_edition.setObjectName("fgdc_edition")
        self.horizontalLayout.addWidget(self.fgdc_edition)
        self.verticalLayout_7.addWidget(self.help_edition)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.verticalLayout_7.addItem(spacerItem1)
        self.second_hbox.addWidget(self.framex)
        self.help_onlink = QtWidgets.QFrame(self.fgdc_citeinfo)
        self.help_onlink.setObjectName("help_onlink")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.help_onlink)
        self.verticalLayout_17.setContentsMargins(3, 3, 9, 3)
        self.verticalLayout_17.setSpacing(3)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_51 = QtWidgets.QLabel(self.help_onlink)
        self.label_51.setStyleSheet("font: bold;")
        self.label_51.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.label_51.setObjectName("label_51")
        self.verticalLayout_17.addWidget(self.label_51)
        self.onlink_layout = QtWidgets.QVBoxLayout()
        self.onlink_layout.setObjectName("onlink_layout")
        self.verticalLayout_17.addLayout(self.onlink_layout)
        self.second_hbox.addWidget(self.help_onlink)
        self.verticalLayout_4.addLayout(self.second_hbox)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setContentsMargins(0, 3, 0, 3)
        self.horizontalLayout_15.setSpacing(6)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.fgdc_serinfo = QtWidgets.QFrame(self.fgdc_citeinfo)
        self.fgdc_serinfo.setObjectName("fgdc_serinfo")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.fgdc_serinfo)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_43 = QtWidgets.QLabel(self.fgdc_serinfo)
        self.label_43.setStyleSheet("font: bold;")
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_6.addWidget(self.label_43)
        spacerItem2 = QtWidgets.QSpacerItem(
            48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_6.addItem(spacerItem2)
        self.radio_seriesyes = QtWidgets.QRadioButton(self.fgdc_serinfo)
        self.radio_seriesyes.setObjectName("radio_seriesyes")
        self.horizontalLayout_6.addWidget(self.radio_seriesyes)
        self.radio_seriesno = QtWidgets.QRadioButton(self.fgdc_serinfo)
        self.radio_seriesno.setChecked(True)
        self.radio_seriesno.setObjectName("radio_seriesno")
        self.horizontalLayout_6.addWidget(self.radio_seriesno)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.label_44 = QtWidgets.QLabel(self.fgdc_serinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)
        self.label_44.setStyleSheet("font: italic;")
        self.label_44.setObjectName("label_44")
        self.verticalLayout.addWidget(self.label_44)
        self.series_ext = QtWidgets.QWidget(self.fgdc_serinfo)
        self.series_ext.setObjectName("series_ext")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.series_ext)
        self.horizontalLayout_10.setContentsMargins(3, 6, 3, 3)
        self.horizontalLayout_10.setSpacing(3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(10)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setSpacing(3)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.help_sername = QtWidgets.QLabel(self.series_ext)
        self.help_sername.setObjectName("help_sername")
        self.verticalLayout_21.addWidget(self.help_sername)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.fgdc_sername = QtWidgets.QLineEdit(self.series_ext)
        self.fgdc_sername.setObjectName("fgdc_sername")
        self.horizontalLayout_7.addWidget(self.fgdc_sername)
        self.label_6 = QtWidgets.QLabel(self.series_ext)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(15, 0))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setScaledContents(True)
        self.label_6.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_6.setIndent(0)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.verticalLayout_21.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_9.addLayout(self.verticalLayout_21)
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setSpacing(3)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.help_issue = QtWidgets.QLabel(self.series_ext)
        self.help_issue.setObjectName("help_issue")
        self.verticalLayout_22.addWidget(self.help_issue)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.fgdc_issue = QtWidgets.QLineEdit(self.series_ext)
        self.fgdc_issue.setObjectName("fgdc_issue")
        self.horizontalLayout_11.addWidget(self.fgdc_issue)
        self.label_7 = QtWidgets.QLabel(self.series_ext)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(15, 0))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_7.setIndent(0)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_11.addWidget(self.label_7)
        self.verticalLayout_22.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_9.addLayout(self.verticalLayout_22)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_9)
        self.verticalLayout.addWidget(self.series_ext)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_15.addWidget(self.fgdc_serinfo)
        self.fgdc_pubinfo = QtWidgets.QFrame(self.fgdc_citeinfo)
        self.fgdc_pubinfo.setObjectName("fgdc_pubinfo")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.fgdc_pubinfo)
        self.verticalLayout_24.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_24.setSpacing(3)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_49 = QtWidgets.QLabel(self.fgdc_pubinfo)
        self.label_49.setStyleSheet("font: bold;")
        self.label_49.setObjectName("label_49")
        self.horizontalLayout_8.addWidget(self.label_49)
        spacerItem4 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_8.addItem(spacerItem4)
        self.radio_pubinfoyes = QtWidgets.QRadioButton(self.fgdc_pubinfo)
        self.radio_pubinfoyes.setObjectName("radio_pubinfoyes")
        self.horizontalLayout_8.addWidget(self.radio_pubinfoyes)
        self.radio_pubinfono = QtWidgets.QRadioButton(self.fgdc_pubinfo)
        self.radio_pubinfono.setChecked(True)
        self.radio_pubinfono.setObjectName("radio_pubinfono")
        self.horizontalLayout_8.addWidget(self.radio_pubinfono)
        self.verticalLayout_24.addLayout(self.horizontalLayout_8)
        self.label_50 = QtWidgets.QLabel(self.fgdc_pubinfo)
        self.label_50.setStyleSheet("font: italic;")
        self.label_50.setObjectName("label_50")
        self.verticalLayout_24.addWidget(self.label_50)
        self.pub_ext = QtWidgets.QWidget(self.fgdc_pubinfo)
        self.pub_ext.setObjectName("pub_ext")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pub_ext)
        self.verticalLayout_3.setContentsMargins(3, 6, 3, 3)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(10)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout()
        self.verticalLayout_30.setSpacing(3)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.help_pubplace = QtWidgets.QLabel(self.pub_ext)
        self.help_pubplace.setObjectName("help_pubplace")
        self.verticalLayout_30.addWidget(self.help_pubplace)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fgdc_pubplace = QtWidgets.QLineEdit(self.pub_ext)
        self.fgdc_pubplace.setObjectName("fgdc_pubplace")
        self.horizontalLayout_2.addWidget(self.fgdc_pubplace)
        self.label_3 = QtWidgets.QLabel(self.pub_ext)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(15, 0))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_3.setIndent(0)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout_30.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_12.addLayout(self.verticalLayout_30)
        self.verticalLayout_31 = QtWidgets.QVBoxLayout()
        self.verticalLayout_31.setSpacing(3)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.help_publish = QtWidgets.QLabel(self.pub_ext)
        self.help_publish.setObjectName("help_publish")
        self.verticalLayout_31.addWidget(self.help_publish)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fgdc_publish = QtWidgets.QLineEdit(self.pub_ext)
        self.fgdc_publish.setObjectName("fgdc_publish")
        self.horizontalLayout_3.addWidget(self.fgdc_publish)
        self.label_4 = QtWidgets.QLabel(self.pub_ext)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(15, 0))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_4.setIndent(0)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout_31.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_12.addLayout(self.verticalLayout_31)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.verticalLayout_24.addWidget(self.pub_ext)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_24.addItem(spacerItem5)
        self.horizontalLayout_15.addWidget(self.fgdc_pubinfo)
        self.help_othercit = QtWidgets.QFrame(self.fgdc_citeinfo)
        self.help_othercit.setObjectName("help_othercit")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.help_othercit)
        self.verticalLayout_16.setContentsMargins(9, 3, 9, 3)
        self.verticalLayout_16.setSpacing(3)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_54 = QtWidgets.QLabel(self.help_othercit)
        self.label_54.setStyleSheet("font: bold;")
        self.label_54.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.label_54.setObjectName("label_54")
        self.verticalLayout_16.addWidget(self.label_54)
        self.fgdc_othercit = GrowingTextEdit(self.help_othercit)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_othercit.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_othercit.setSizePolicy(sizePolicy)
        self.fgdc_othercit.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow
        )
        self.fgdc_othercit.setObjectName("fgdc_othercit")
        self.verticalLayout_16.addWidget(self.fgdc_othercit)
        self.horizontalLayout_15.addWidget(self.help_othercit)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.fgdc_lworkcit = QtWidgets.QGroupBox(self.fgdc_citeinfo)
        self.fgdc_lworkcit.setObjectName("fgdc_lworkcit")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.fgdc_lworkcit)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_65 = QtWidgets.QLabel(self.fgdc_lworkcit)
        self.label_65.setStyleSheet("font: bold;")
        self.label_65.setObjectName("label_65")
        self.horizontalLayout_28.addWidget(self.label_65)
        spacerItem6 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_28.addItem(spacerItem6)
        self.radio_lworkyes = QtWidgets.QRadioButton(self.fgdc_lworkcit)
        self.radio_lworkyes.setObjectName("radio_lworkyes")
        self.horizontalLayout_28.addWidget(self.radio_lworkyes)
        self.radio_lworkno = QtWidgets.QRadioButton(self.fgdc_lworkcit)
        self.radio_lworkno.setChecked(True)
        self.radio_lworkno.setObjectName("radio_lworkno")
        self.horizontalLayout_28.addWidget(self.radio_lworkno)
        spacerItem7 = QtWidgets.QSpacerItem(
            80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_28.addItem(spacerItem7)
        self.label_66 = QtWidgets.QLabel(self.fgdc_lworkcit)
        self.label_66.setStyleSheet("font: italic;")
        self.label_66.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_66.setObjectName("label_66")
        self.horizontalLayout_28.addWidget(self.label_66)
        spacerItem8 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_28.addItem(spacerItem8)
        self.verticalLayout_5.addLayout(self.horizontalLayout_28)
        self.lworkcite_widget = QtWidgets.QWidget(self.fgdc_lworkcit)
        self.lworkcite_widget.setObjectName("lworkcite_widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.lworkcite_widget)
        self.horizontalLayout_5.setContentsMargins(15, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5.addWidget(self.lworkcite_widget)
        self.verticalLayout_4.addWidget(self.fgdc_lworkcit)
        self.horizontalLayout_13.addWidget(self.fgdc_citeinfo)

        self.retranslateUi(parent_form)
        QtCore.QMetaObject.connectSlotsByName(parent_form)

    def retranslateUi(self, parent_form):
        _translate = QtCore.QCoreApplication.translate
        parent_form.setWindowTitle(_translate("parent_form", "Form"))
        self.fgdc_citeinfo.setTitle(_translate("parent_form", "Citation"))
        self.lbl_dataset_title.setText(_translate("parent_form", "Dataset Title"))
        self.label_34.setText(
            _translate(
                "parent_form",
                "A good title includes 'What', 'Where', and 'When'.  (Example: Point Locations of Wind Turbines in Colorado, Derived from 2010 NAIP Imagery)",
            )
        )
        self.label_5.setToolTip(_translate("parent_form", "Required"))
        self.label_5.setText(
            _translate(
                "parent_form",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_46.setText(_translate("parent_form", "Publication Date"))
        self.label_38.setText(
            _translate("parent_form", "Date published or otherwise made available for release")
        )
        self.btn_import_doi.setToolTip(
            _translate("parent_form", "Import citation from Active (CrossRef) DOI")
        )
        self.btn_import_doi.setText(
            _translate("parent_form", "Import \n" "from \n" "DOI")
        )
        self.label_47.setText(_translate("parent_form", "Dataset Author/ Originator"))
        self.label_53.setText(_translate("parent_form", "Dataset Format"))
        self.label_36.setText(
            _translate(
                "parent_form", "Type directly in box below for items not in list."
            )
        )
        self.fgdc_geoform.setCurrentText(
            _translate("parent_form", "tabular digital data")
        )
        self.fgdc_geoform.setItemText(
            0, _translate("parent_form", "tabular digital data")
        )
        self.fgdc_geoform.setItemText(
            1, _translate("parent_form", "vector digital data")
        )
        self.fgdc_geoform.setItemText(
            2, _translate("parent_form", "raster digital data")
        )
        self.fgdc_geoform.setItemText(3, _translate("parent_form", "spreadsheet"))
        self.fgdc_geoform.setItemText(
            4, _translate("parent_form", "remote-sensing image")
        )
        self.fgdc_geoform.setItemText(
            5, _translate("parent_form", "application/service")
        )
        self.fgdc_geoform.setItemText(6, _translate("parent_form", "publication"))
        self.label_9.setToolTip(_translate("parent_form", "Required"))
        self.label_9.setText(
            _translate(
                "parent_form",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_55.setText(_translate("parent_form", "Edition"))
        self.label_51.setText(_translate("parent_form", "Online Link to the Dataset"))
        self.label_43.setText(
            _translate("parent_form", "Is this dataset part of a series?")
        )
        self.radio_seriesyes.setText(_translate("parent_form", "Yes"))
        self.radio_seriesno.setText(_translate("parent_form", "No"))
        self.label_44.setText(
            _translate(
                "parent_form",
                " Is it a release with an assigned issue number (e.g. USGS Data Series)",
            )
        )
        self.help_sername.setText(_translate("parent_form", "Series Name"))
        self.label_6.setToolTip(_translate("parent_form", "Required"))
        self.label_6.setText(
            _translate(
                "parent_form",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.help_issue.setText(
            _translate("parent_form", "Issue Name / Number within Series")
        )
        self.label_7.setToolTip(_translate("parent_form", "Required"))
        self.label_7.setText(
            _translate(
                "parent_form",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_49.setText(
            _translate(
                "parent_form",
                "Can you provide more publication information about this dataset?",
            )
        )
        self.radio_pubinfoyes.setText(_translate("parent_form", "Yes"))
        self.radio_pubinfono.setText(_translate("parent_form", "No"))
        self.label_50.setText(
            _translate(
                "parent_form",
                "More details are always helpful for finding and properly referencing data.",
            )
        )
        self.help_pubplace.setText(_translate("parent_form", "Publication Place"))
        self.label_3.setToolTip(_translate("parent_form", "Required"))
        self.label_3.setText(
            _translate(
                "parent_form",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.help_publish.setText(_translate("parent_form", "Publisher"))
        self.label_4.setToolTip(_translate("parent_form", "Required"))
        self.label_4.setText(
            _translate(
                "parent_form",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_54.setText(_translate("parent_form", "Other citation details"))
        self.fgdc_lworkcit.setTitle(_translate("parent_form", "Larger Work"))
        self.label_65.setText(
            _translate("parent_form", "Is this dataset associated with a larger work?")
        )
        self.radio_lworkyes.setText(_translate("parent_form", "Yes"))
        self.radio_lworkno.setText(_translate("parent_form", "No"))
        self.label_66.setText(
            _translate(
                "parent_form",
                "If this record is part of a publication or larger project, you may optionally cite it here.",
            )
        )


from growingtextedit import GrowingTextEdit
