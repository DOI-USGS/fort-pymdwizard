# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContactInfo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_USGSContactInfoWidget(object):
    def setupUi(self, USGSContactInfoWidget):
        USGSContactInfoWidget.setObjectName("USGSContactInfoWidget")
        USGSContactInfoWidget.resize(563, 360)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            USGSContactInfoWidget.sizePolicy().hasHeightForWidth()
        )
        USGSContactInfoWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        USGSContactInfoWidget.setFont(font)
        USGSContactInfoWidget.setFocusPolicy(QtCore.Qt.WheelFocus)
        USGSContactInfoWidget.setAcceptDrops(True)
        USGSContactInfoWidget.setStyleSheet(
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
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(USGSContactInfoWidget)
        self.verticalLayout_11.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_11.setContentsMargins(4, 0, 4, 4)
        self.verticalLayout_11.setSpacing(4)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.fgdc_cntinfo = QtWidgets.QWidget(USGSContactInfoWidget)
        self.fgdc_cntinfo.setObjectName("fgdc_cntinfo")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.fgdc_cntinfo)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_7.setContentsMargins(0, 9, 0, 0)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_17.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.rbtn_orgp = QtWidgets.QRadioButton(self.fgdc_cntinfo)
        self.rbtn_orgp.setObjectName("rbtn_orgp")
        self.horizontalLayout_17.addWidget(self.rbtn_orgp)
        self.rbtn_perp = QtWidgets.QRadioButton(self.fgdc_cntinfo)
        self.rbtn_perp.setChecked(True)
        self.rbtn_perp.setObjectName("rbtn_perp")
        self.horizontalLayout_17.addWidget(self.rbtn_perp)
        spacerItem = QtWidgets.QSpacerItem(
            40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_17.addItem(spacerItem)
        self.btn_import_contact = QtWidgets.QPushButton(self.fgdc_cntinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_contact.sizePolicy().hasHeightForWidth()
        )
        self.btn_import_contact.setSizePolicy(sizePolicy)
        self.btn_import_contact.setMinimumSize(QtCore.QSize(140, 40))
        self.btn_import_contact.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btn_import_contact.setObjectName("btn_import_contact")
        self.horizontalLayout_17.addWidget(self.btn_import_contact)
        self.verticalLayout_7.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setSpacing(2)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.widget_2 = QtWidgets.QWidget(self.fgdc_cntinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setStyleSheet("")
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.left_vertical_layout = QtWidgets.QVBoxLayout()
        self.left_vertical_layout.setSpacing(2)
        self.left_vertical_layout.setObjectName("left_vertical_layout")
        self.fgdc_cntperp = QtWidgets.QWidget(self.widget_2)
        self.fgdc_cntperp.setObjectName("fgdc_cntperp")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.fgdc_cntperp)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_cntper = QtWidgets.QLabel(self.fgdc_cntperp)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_cntper.sizePolicy().hasHeightForWidth())
        self.lbl_cntper.setSizePolicy(sizePolicy)
        self.lbl_cntper.setMinimumSize(QtCore.QSize(30, 0))
        self.lbl_cntper.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_cntper.setFont(font)
        self.lbl_cntper.setStyleSheet("")
        self.lbl_cntper.setScaledContents(False)
        self.lbl_cntper.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.lbl_cntper.setWordWrap(False)
        self.lbl_cntper.setIndent(0)
        self.lbl_cntper.setObjectName("lbl_cntper")
        self.verticalLayout.addWidget(self.lbl_cntper)
        self.required_horizontal_layout = QtWidgets.QHBoxLayout()
        self.required_horizontal_layout.setSpacing(0)
        self.required_horizontal_layout.setObjectName("required_horizontal_layout")
        self.fgdc_cntper = QtWidgets.QLineEdit(self.fgdc_cntperp)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_cntper.sizePolicy().hasHeightForWidth())
        self.fgdc_cntper.setSizePolicy(sizePolicy)
        self.fgdc_cntper.setMinimumSize(QtCore.QSize(217, 0))
        self.fgdc_cntper.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_cntper.setText("")
        self.fgdc_cntper.setPlaceholderText("")
        self.fgdc_cntper.setObjectName("fgdc_cntper")
        self.required_horizontal_layout.addWidget(self.fgdc_cntper)
        self.label_3 = QtWidgets.QLabel(self.fgdc_cntperp)
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
        self.required_horizontal_layout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.required_horizontal_layout)
        self.lbl_cntorg = QtWidgets.QLabel(self.fgdc_cntperp)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_cntorg.sizePolicy().hasHeightForWidth())
        self.lbl_cntorg.setSizePolicy(sizePolicy)
        self.lbl_cntorg.setMinimumSize(QtCore.QSize(0, 0))
        self.lbl_cntorg.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_cntorg.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.lbl_cntorg.setObjectName("lbl_cntorg")
        self.verticalLayout.addWidget(self.lbl_cntorg)
        self.optional_horizontal_layout = QtWidgets.QHBoxLayout()
        self.optional_horizontal_layout.setSpacing(0)
        self.optional_horizontal_layout.setObjectName("optional_horizontal_layout")
        self.fgdc_cntorg = QtWidgets.QLineEdit(self.fgdc_cntperp)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_cntorg.sizePolicy().hasHeightForWidth())
        self.fgdc_cntorg.setSizePolicy(sizePolicy)
        self.fgdc_cntorg.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_cntorg.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_cntorg.setObjectName("fgdc_cntorg")
        self.optional_horizontal_layout.addWidget(self.fgdc_cntorg)
        spacerItem1 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.optional_horizontal_layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.optional_horizontal_layout)
        self.left_vertical_layout.addWidget(self.fgdc_cntperp)
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_5.setObjectName("label_5")
        self.left_vertical_layout.addWidget(self.label_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.fgdc_cntpos = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_cntpos.sizePolicy().hasHeightForWidth())
        self.fgdc_cntpos.setSizePolicy(sizePolicy)
        self.fgdc_cntpos.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_cntpos.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_cntpos.setObjectName("fgdc_cntpos")
        self.horizontalLayout_4.addWidget(self.fgdc_cntpos)
        spacerItem2 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_4.addItem(spacerItem2)
        self.left_vertical_layout.addLayout(self.horizontalLayout_4)
        self.label_8 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_8.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_8.setObjectName("label_8")
        self.left_vertical_layout.addWidget(self.label_8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.fgdc_cntvoice = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_cntvoice.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_cntvoice.setSizePolicy(sizePolicy)
        self.fgdc_cntvoice.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_cntvoice.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_cntvoice.setObjectName("fgdc_cntvoice")
        self.horizontalLayout_5.addWidget(self.fgdc_cntvoice)
        self.label_7 = QtWidgets.QLabel(self.widget_2)
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
        self.horizontalLayout_5.addWidget(self.label_7)
        self.left_vertical_layout.addLayout(self.horizontalLayout_5)
        self.label_9 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_9.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_9.setObjectName("label_9")
        self.left_vertical_layout.addWidget(self.label_9)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.fgdc_cntfax = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_cntfax.sizePolicy().hasHeightForWidth())
        self.fgdc_cntfax.setSizePolicy(sizePolicy)
        self.fgdc_cntfax.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_cntfax.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_cntfax.setObjectName("fgdc_cntfax")
        self.horizontalLayout_6.addWidget(self.fgdc_cntfax)
        spacerItem3 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_6.addItem(spacerItem3)
        self.left_vertical_layout.addLayout(self.horizontalLayout_6)
        self.label_18 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QtCore.QSize(0, 0))
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_18.setStyleSheet("")
        self.label_18.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_18.setObjectName("label_18")
        self.left_vertical_layout.addWidget(self.label_18)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.fgdc_cntemail = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_cntemail.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_cntemail.setSizePolicy(sizePolicy)
        self.fgdc_cntemail.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_cntemail.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_cntemail.setObjectName("fgdc_cntemail")
        self.horizontalLayout_7.addWidget(self.fgdc_cntemail)
        spacerItem4 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_7.addItem(spacerItem4)
        self.left_vertical_layout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addLayout(self.left_vertical_layout)
        self.horizontalLayout_14.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.fgdc_cntinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setStyleSheet("")
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.fgdc_cntaddr = QtWidgets.QWidget(self.widget_3)
        self.fgdc_cntaddr.setObjectName("fgdc_cntaddr")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.fgdc_cntaddr)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_19 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QtCore.QSize(0, 0))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("")
        self.label_19.setScaledContents(False)
        self.label_19.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_19.setWordWrap(False)
        self.label_19.setIndent(0)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_5.addWidget(self.label_19)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.fgdc_address = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_address.sizePolicy().hasHeightForWidth())
        self.fgdc_address.setSizePolicy(sizePolicy)
        self.fgdc_address.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_address.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_address.setObjectName("fgdc_address")
        self.horizontalLayout_8.addWidget(self.fgdc_address)
        self.label_20 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QtCore.QSize(15, 0))
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setScaledContents(True)
        self.label_20.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_20.setIndent(0)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_8.addWidget(self.label_20)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.label_21 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QtCore.QSize(0, 0))
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_21.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_21.setObjectName("label_21")
        self.verticalLayout_5.addWidget(self.label_21)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.fgdc_address2 = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_address2.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_address2.setSizePolicy(sizePolicy)
        self.fgdc_address2.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_address2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_address2.setObjectName("fgdc_address2")
        self.horizontalLayout_9.addWidget(self.fgdc_address2)
        spacerItem5 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_9.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.label_22 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setMinimumSize(QtCore.QSize(0, 0))
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_22.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_22.setObjectName("label_22")
        self.verticalLayout_5.addWidget(self.label_22)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.fgdc_address3 = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_address3.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_address3.setSizePolicy(sizePolicy)
        self.fgdc_address3.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_address3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_address3.setObjectName("fgdc_address3")
        self.horizontalLayout_10.addWidget(self.fgdc_address3)
        spacerItem6 = QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_10.addItem(spacerItem6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.label_23 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setMinimumSize(QtCore.QSize(0, 0))
        self.label_23.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_23.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_23.setObjectName("label_23")
        self.verticalLayout_5.addWidget(self.label_23)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.fgdc_city = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_city.sizePolicy().hasHeightForWidth())
        self.fgdc_city.setSizePolicy(sizePolicy)
        self.fgdc_city.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_city.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_city.setObjectName("fgdc_city")
        self.horizontalLayout_11.addWidget(self.fgdc_city)
        self.label_24 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setMinimumSize(QtCore.QSize(15, 20))
        self.label_24.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setScaledContents(True)
        self.label_24.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_24.setIndent(0)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_11.addWidget(self.label_24)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_27 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setMinimumSize(QtCore.QSize(0, 0))
        self.label_27.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_27.setStyleSheet("")
        self.label_27.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_27.setObjectName("label_27")
        self.verticalLayout_8.addWidget(self.label_27)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.fgdc_state = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_state.sizePolicy().hasHeightForWidth())
        self.fgdc_state.setSizePolicy(sizePolicy)
        self.fgdc_state.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_state.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_state.setObjectName("fgdc_state")
        self.horizontalLayout_18.addWidget(self.fgdc_state)
        self.label_28 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QtCore.QSize(15, 0))
        self.label_28.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_28.setFont(font)
        self.label_28.setScaledContents(True)
        self.label_28.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_28.setIndent(0)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_18.addWidget(self.label_28)
        self.verticalLayout_8.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19.addLayout(self.verticalLayout_8)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_30 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setMinimumSize(QtCore.QSize(0, 0))
        self.label_30.setMaximumSize(QtCore.QSize(75, 20))
        self.label_30.setStyleSheet("")
        self.label_30.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_30.setObjectName("label_30")
        self.verticalLayout_2.addWidget(self.label_30)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fgdc_postal = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_postal.sizePolicy().hasHeightForWidth())
        self.fgdc_postal.setSizePolicy(sizePolicy)
        self.fgdc_postal.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_postal.setMaximumSize(QtCore.QSize(75, 20))
        self.fgdc_postal.setObjectName("fgdc_postal")
        self.horizontalLayout_2.addWidget(self.fgdc_postal)
        self.label_29 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setMinimumSize(QtCore.QSize(15, 0))
        self.label_29.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_29.setFont(font)
        self.label_29.setScaledContents(True)
        self.label_29.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_29.setIndent(0)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_2.addWidget(self.label_29)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_19.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setSpacing(6)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_31 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setMinimumSize(QtCore.QSize(0, 0))
        self.label_31.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_31.setStyleSheet("")
        self.label_31.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_31.setObjectName("label_31")
        self.verticalLayout_9.addWidget(self.label_31)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setSpacing(2)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.fgdc_country = QtWidgets.QLineEdit(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_country.sizePolicy().hasHeightForWidth())
        self.fgdc_country.setSizePolicy(sizePolicy)
        self.fgdc_country.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_country.setMaximumSize(QtCore.QSize(16777215, 20))
        self.fgdc_country.setBaseSize(QtCore.QSize(25, 0))
        self.fgdc_country.setObjectName("fgdc_country")
        self.horizontalLayout_21.addWidget(self.fgdc_country)
        self.verticalLayout_9.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_20.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_33 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setMinimumSize(QtCore.QSize(0, 0))
        self.label_33.setMaximumSize(QtCore.QSize(75, 20))
        self.label_33.setStyleSheet("")
        self.label_33.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_33.setObjectName("label_33")
        self.verticalLayout_10.addWidget(self.label_33)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.fgdc_addrtype = QtWidgets.QComboBox(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_addrtype.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_addrtype.setSizePolicy(sizePolicy)
        self.fgdc_addrtype.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_addrtype.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.fgdc_addrtype.setEditable(True)
        self.fgdc_addrtype.setObjectName("fgdc_addrtype")
        self.fgdc_addrtype.addItem("")
        self.fgdc_addrtype.addItem("")
        self.fgdc_addrtype.addItem("")
        self.horizontalLayout_12.addWidget(self.fgdc_addrtype)
        self.label_34 = QtWidgets.QLabel(self.fgdc_cntaddr)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setMinimumSize(QtCore.QSize(15, 20))
        self.label_34.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_34.setFont(font)
        self.label_34.setScaledContents(True)
        self.label_34.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_34.setIndent(0)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_12.addWidget(self.label_34)
        self.verticalLayout_10.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_20.addLayout(self.verticalLayout_10)
        self.verticalLayout_5.addLayout(self.horizontalLayout_20)
        self.verticalLayout_4.addWidget(self.fgdc_cntaddr)
        self.horizontalLayout_14.addWidget(self.widget_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.verticalLayout_11.addWidget(self.fgdc_cntinfo)

        self.retranslateUi(USGSContactInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(USGSContactInfoWidget)

    def retranslateUi(self, USGSContactInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        USGSContactInfoWidget.setWindowTitle(
            _translate("USGSContactInfoWidget", "Form")
        )
        self.rbtn_orgp.setText(_translate("USGSContactInfoWidget", "Organization"))
        self.rbtn_perp.setText(_translate("USGSContactInfoWidget", "Person"))
        self.btn_import_contact.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Import contact information from USGS Active Directory",
            )
        )
        self.btn_import_contact.setText(
            _translate("USGSContactInfoWidget", "Import USGS Contact")
        )
        self.lbl_cntper.setToolTip(
            _translate("USGSContactInfoWidget", "The name of the person to contact")
        )
        self.lbl_cntper.setText(_translate("USGSContactInfoWidget", "Contact Person"))
        self.fgdc_cntper.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Contact Person -- the name of the individual to which the contact type applies.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntper",
            )
        )
        self.label_3.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_3.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.lbl_cntorg.setText(
            _translate("USGSContactInfoWidget", "Organization Name")
        )
        self.fgdc_cntorg.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Contact Organization -- the name of the organization to which the contact type applies.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntorg",
            )
        )
        self.label_5.setText(_translate("USGSContactInfoWidget", "Title of Position"))
        self.fgdc_cntpos.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Contact Position -- the title of individual.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntpos",
            )
        )
        self.label_8.setText(_translate("USGSContactInfoWidget", "Telephone Number"))
        self.fgdc_cntvoice.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Contact Voice Telephone -- the telephone number by which individuals can speak to the\n"
                "organization or individual.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntvoice",
            )
        )
        self.label_7.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_7.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_9.setText(_translate("USGSContactInfoWidget", "Fax Number"))
        self.fgdc_cntfax.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Contact Facsimile Telephone -- the telephone number of a facsimile machine of the organization or\n"
                "individual.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntfax",
            )
        )
        self.label_18.setText(_translate("USGSContactInfoWidget", "Email Address"))
        self.fgdc_cntemail.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Contact Electronic Mail Address -- the address of the electronic mailbox of the organization or\n"
                "individual.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: cntemail",
            )
        )
        self.label_19.setText(
            _translate("USGSContactInfoWidget", "Address 1 (Number of Street)")
        )
        self.fgdc_address.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Address -- an address line for the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: address",
            )
        )
        self.label_20.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_20.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_21.setText(
            _translate("USGSContactInfoWidget", "Address 2 (if Applicable)")
        )
        self.fgdc_address2.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Address -- an address line for the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: address",
            )
        )
        self.label_22.setText(
            _translate("USGSContactInfoWidget", "Address 3 (if Applicable) ")
        )
        self.fgdc_address3.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Address -- an address line for the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: address",
            )
        )
        self.label_23.setText(_translate("USGSContactInfoWidget", "City"))
        self.fgdc_city.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "City -- the city of the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: city",
            )
        )
        self.label_24.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_24.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_27.setText(_translate("USGSContactInfoWidget", "State / Province"))
        self.fgdc_state.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "State or Province -- the state or province of the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: state",
            )
        )
        self.label_28.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_28.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_30.setText(_translate("USGSContactInfoWidget", "Zipcode"))
        self.fgdc_postal.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Postal Code -- the ZIP or other postal code of the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: postal",
            )
        )
        self.label_29.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_29.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_31.setText(_translate("USGSContactInfoWidget", "Country"))
        self.fgdc_country.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Country -- the country of the address.\n"
                "Type: text\n"
                "Domain: free text\n"
                "Short Name: country",
            )
        )
        self.label_33.setText(_translate("USGSContactInfoWidget", "Address Type"))
        self.fgdc_addrtype.setToolTip(
            _translate(
                "USGSContactInfoWidget",
                "Address Type -- the information provided by the address.\n"
                "Type: text\n"
                'Domain: "mailing" "physical" "mailing and physical", free text\n'
                "Short Name: addrtype",
            )
        )
        self.fgdc_addrtype.setItemText(
            0, _translate("USGSContactInfoWidget", "mailing")
        )
        self.fgdc_addrtype.setItemText(
            1, _translate("USGSContactInfoWidget", "physical")
        )
        self.fgdc_addrtype.setItemText(
            2, _translate("USGSContactInfoWidget", "mailing and physical")
        )
        self.label_34.setToolTip(_translate("USGSContactInfoWidget", "Required"))
        self.label_34.setText(
            _translate(
                "USGSContactInfoWidget",
                '<html><head/><body><p align="center"><span style=" font-size:18pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
