# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'distinfo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fgdc_distinfo(object):
    def setupUi(self, fgdc_distinfo):
        fgdc_distinfo.setObjectName("fgdc_distinfo")
        fgdc_distinfo.resize(1103, 862)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(fgdc_distinfo)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget = QtWidgets.QWidget(fgdc_distinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(10, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.widget)
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
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_5.setIndent(0)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        spacerItem = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(100, 0))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
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
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_4.setIndent(0)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(79, 0))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.label_3.setIndent(0)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addWidget(self.widget_2)
        self.verticalLayout_10.addWidget(self.widget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radio_distno = QtWidgets.QRadioButton(fgdc_distinfo)
        self.radio_distno.setChecked(True)
        self.radio_distno.setObjectName("radio_distno")
        self.verticalLayout_2.addWidget(self.radio_distno)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.line = QtWidgets.QFrame(fgdc_distinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMaximumSize(QtCore.QSize(16777215, 100))
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.horizontalLayout_9.addWidget(self.line)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_10.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(fgdc_distinfo)
        self.label.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label.setObjectName("label")
        self.horizontalLayout_10.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_10.addItem(spacerItem2)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_10)
        self.line_2 = QtWidgets.QFrame(fgdc_distinfo)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_9.addWidget(self.line_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.radio_distyes = QtWidgets.QRadioButton(fgdc_distinfo)
        self.radio_distyes.setObjectName("radio_distyes")
        self.verticalLayout_2.addWidget(self.radio_distyes)
        self.verticalLayout_10.addLayout(self.verticalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(fgdc_distinfo)
        font = QtGui.QFont()
        font.setKerning(False)
        self.scrollArea.setFont(font)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1068, 717))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_distinfo = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_distinfo.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_distinfo.setObjectName("widget_distinfo")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_distinfo)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.two_column = QtWidgets.QWidget(self.widget_distinfo)
        self.two_column.setObjectName("two_column")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.two_column)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.two_column_left = QtWidgets.QWidget(self.two_column)
        self.two_column_left.setObjectName("two_column_left")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.two_column_left)
        self.verticalLayout_5.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fgdc_distrib = QtWidgets.QGroupBox(self.two_column_left)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_distrib.sizePolicy().hasHeightForWidth())
        self.fgdc_distrib.setSizePolicy(sizePolicy)
        self.fgdc_distrib.setObjectName("fgdc_distrib")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.fgdc_distrib)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.fgdc_distrib)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setStyleSheet("font: italic;")
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.frame = QtWidgets.QFrame(self.fgdc_distrib)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(
            "QFrame#frame{ \n"
            'font: 75 10pt "Arial";\n'
            "border: 1px solid black;\n"
            "border-radius: 3px;\n"
            "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf);\n"
            "}\n"
            ""
        )
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(0, 20))
        self.label_6.setStyleSheet("font: italic;")
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        spacerItem3 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_5.addItem(spacerItem3)
        self.button_use_sb = QtWidgets.QPushButton(self.frame)
        self.button_use_sb.setMinimumSize(QtCore.QSize(150, 0))
        self.button_use_sb.setObjectName("button_use_sb")
        self.horizontalLayout_5.addWidget(self.button_use_sb)
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8.addLayout(self.verticalLayout_11)
        self.verticalLayout_4.addWidget(self.frame)
        self.verticalLayout_5.addWidget(self.fgdc_distrib)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_4.addWidget(self.two_column_left)
        self.two_column_right = QtWidgets.QWidget(self.two_column)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.two_column_right.sizePolicy().hasHeightForWidth()
        )
        self.two_column_right.setSizePolicy(sizePolicy)
        self.two_column_right.setObjectName("two_column_right")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.two_column_right)
        self.verticalLayout_6.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_6.setSpacing(1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.two_column_right)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radio_online = QtWidgets.QRadioButton(self.groupBox_3)
        self.radio_online.setObjectName("radio_online")
        self.verticalLayout.addWidget(self.radio_online)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_7.addItem(spacerItem5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        # self.label_7.setObjectName("label_7")
        # self.horizontalLayout_6.addWidget(self.label_7)
        # self.fgdc_networkr = QtWidgets.QLineEdit(self.groupBox_3)
        # self.fgdc_networkr.setEnabled(False)
        # self.fgdc_networkr.setClearButtonEnabled(False)
        # self.fgdc_networkr.setObjectName("fgdc_networkr")
        # self.horizontalLayout_6.addWidget(self.fgdc_networkr)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.radio_dist = QtWidgets.QRadioButton(self.groupBox_3)
        self.radio_dist.setObjectName("radio_dist")
        self.verticalLayout.addWidget(self.radio_dist)
        self.radio_otherdist = QtWidgets.QRadioButton(self.groupBox_3)
        self.radio_otherdist.setObjectName("radio_otherdist")
        self.verticalLayout.addWidget(self.radio_otherdist)
        self.fgdc_custom = QtWidgets.QPlainTextEdit(self.groupBox_3)
        self.fgdc_custom.setEnabled(False)
        self.fgdc_custom.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.fgdc_custom.setObjectName("fgdc_custom")
        self.verticalLayout.addWidget(self.fgdc_custom)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.two_column_right)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(0, 20))
        self.label_10.setStyleSheet("font: italic;")
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.fgdc_distliab = GrowingTextEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fgdc_distliab.sizePolicy().hasHeightForWidth()
        )
        self.fgdc_distliab.setSizePolicy(sizePolicy)
        self.fgdc_distliab.setObjectName("fgdc_distliab")
        self.verticalLayout_8.addWidget(self.fgdc_distliab)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.group_datafees = QtWidgets.QGroupBox(self.two_column_right)
        self.group_datafees.setMaximumSize(QtCore.QSize(16777215, 100))
        self.group_datafees.setObjectName("group_datafees")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.group_datafees)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_12 = QtWidgets.QLabel(self.group_datafees)
        self.label_12.setMinimumSize(QtCore.QSize(0, 20))
        self.label_12.setStyleSheet("font: italic;")
        self.label_12.setWordWrap(True)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_9.addWidget(self.label_12)
        self.fgdc_fees = QtWidgets.QPlainTextEdit(self.group_datafees)
        self.fgdc_fees.setEnabled(False)
        self.fgdc_fees.setMaximumSize(QtCore.QSize(16777215, 50))
        self.fgdc_fees.setObjectName("fgdc_fees")
        self.verticalLayout_9.addWidget(self.fgdc_fees)
        self.verticalLayout_6.addWidget(self.group_datafees)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_6.addItem(spacerItem6)
        self.groupBox_3.raise_()
        self.groupBox.raise_()
        self.group_datafees.raise_()
        self.horizontalLayout_4.addWidget(self.two_column_right)
        self.horizontalLayout_2.addWidget(self.two_column)
        self.verticalLayout_3.addWidget(self.widget_distinfo)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_10.addWidget(self.scrollArea)

        self.retranslateUi(fgdc_distinfo)
        QtCore.QMetaObject.connectSlotsByName(fgdc_distinfo)

    def retranslateUi(self, fgdc_distinfo):
        _translate = QtCore.QCoreApplication.translate
        fgdc_distinfo.setWindowTitle(_translate("fgdc_distinfo", "Form"))
        self.label_5.setToolTip(_translate("fgdc_distinfo", "Required"))
        self.label_5.setText(
            _translate(
                "fgdc_distinfo",
                '<html><head/><body><p><span style=" font-style:italic; color:#55aaff;">Provide information about access to the data, the data distribution format, and the data distributor.</span></p></body></html>',
            )
        )
        self.label_4.setToolTip(_translate("fgdc_distinfo", "Required"))
        self.label_4.setText(
            _translate(
                "fgdc_distinfo",
                '<html><head/><body><p><span style=" font-size:15pt; color:#55aaff;">*</span></p></body></html>',
            )
        )
        self.label_3.setToolTip(_translate("fgdc_distinfo", "Required"))
        self.label_3.setText(
            _translate(
                "fgdc_distinfo",
                '<html><head/><body><p><span style=" font-size:9pt; font-style:italic; color:#55aaff;">= Required</span></p></body></html>',
            )
        )
        self.radio_distno.setText(
            _translate(
                "fgdc_distinfo",
                "Dataset is for internal use only and will NOT be shared or distributed.  The metadata record does not need distribution information.",
            )
        )
        self.label.setText(_translate("fgdc_distinfo", "OR"))
        self.radio_distyes.setText(
            _translate(
                "fgdc_distinfo",
                "Details on how to acquire/access the data are described below.",
            )
        )
        self.fgdc_distrib.setTitle(_translate("fgdc_distinfo", "Distribution Contact"))
        self.label_2.setText(
            _translate(
                "fgdc_distinfo",
                "Contact information for the person or organization responsible for the distribution of the data.",
            )
        )
        self.label_6.setText(
            _translate(
                "fgdc_distinfo",
                "Will this dataset be distributed on the USGS ScienceBase System?",
            )
        )
        self.button_use_sb.setText(_translate("fgdc_distinfo", "Add ScienceBase Info"))
        self.groupBox_3.setTitle(
            _translate("fgdc_distinfo", "How Can Others Access the Data?")
        )
        self.radio_online.setText(
            _translate("fgdc_distinfo", "The dataset is available online.")
        )
        # self.label_7.setText(
        #     _translate("fgdc_distinfo", "URL of website or GIS service:")
        # )
        self.radio_dist.setText(
            _translate(
                "fgdc_distinfo",
                "The dataset is not available online.  Interested parties should contact the distributor for details on \n"
                "acquiring the data. (Provide 'Distributor Contact' information.",
            )
        )
        self.radio_otherdist.setText(
            _translate("fgdc_distinfo", "Other Distribution method. (Describe below)")
        )
        self.groupBox.setTitle(_translate("fgdc_distinfo", "Distribution Liability"))
        self.label_10.setText(
            _translate(
                "fgdc_distinfo",
                "List any distribution disclaimers or limitations of liability.",
            )
        )
        self.group_datafees.setTitle(_translate("fgdc_distinfo", "Data Fees"))
        self.label_12.setText(
            _translate("fgdc_distinfo", "Describe any fees associated with this data.")
        )


from growingtextedit import GrowingTextEdit
