# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProcessStep.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(545, 376)
        Form.setMinimumSize(QtCore.QSize(0, 175))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Form.setStyleSheet("QGroupBox{\n"
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
"font: 9pt \"Arial\";\n"
"color: rgb(90, 90, 90);\n"
"}\n"
"QLineEdit, QComboBox {\n"
"font: 9pt \"Arial\";\n"
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
"}")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fgdc_procstep = QtWidgets.QWidget(Form)
        self.fgdc_procstep.setObjectName("fgdc_procstep")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.fgdc_procstep)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.fgdc_procstep)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.fgdc_procdesc = GrowingTextEdit(self.fgdc_procstep)
        self.fgdc_procdesc.setMaximumSize(QtCore.QSize(16777215, 155))
        self.fgdc_procdesc.setObjectName("fgdc_procdesc")
        self.verticalLayout_5.addWidget(self.fgdc_procdesc)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_37 = QtWidgets.QLabel(self.fgdc_procstep)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_2.addWidget(self.label_37)
        self.fgdc_procdate = QtWidgets.QWidget(self.fgdc_procstep)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fgdc_procdate.sizePolicy().hasHeightForWidth())
        self.fgdc_procdate.setSizePolicy(sizePolicy)
        self.fgdc_procdate.setMinimumSize(QtCore.QSize(0, 0))
        self.fgdc_procdate.setMaximumSize(QtCore.QSize(221, 100))
        self.fgdc_procdate.setObjectName("fgdc_procdate")
        self.verticalLayout_2.addWidget(self.fgdc_procdate)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.src_widget = QtWidgets.QWidget(self.fgdc_procstep)
        self.src_widget.setObjectName("src_widget")
        self.src_layout = QtWidgets.QHBoxLayout(self.src_widget)
        self.src_layout.setContentsMargins(0, 0, 0, 0)
        self.src_layout.setObjectName("src_layout")
        self.srcused_groupbox = QtWidgets.QFrame(self.src_widget)
        self.srcused_groupbox.setObjectName("srcused_groupbox")
        self.srcused_layout = QtWidgets.QVBoxLayout(self.srcused_groupbox)
        self.srcused_layout.setObjectName("srcused_layout")
        self.lbl_dataset_title = QtWidgets.QLabel(self.srcused_groupbox)
        self.lbl_dataset_title.setStyleSheet("font: bold;")
        self.lbl_dataset_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_dataset_title.setObjectName("lbl_dataset_title")
        self.srcused_layout.addWidget(self.lbl_dataset_title)
        self.label_34 = QtWidgets.QLabel(self.srcused_groupbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setStyleSheet("font: italic;")
        self.label_34.setWordWrap(True)
        self.label_34.setObjectName("label_34")
        self.srcused_layout.addWidget(self.label_34)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.srcused_layout.addItem(spacerItem2)
        self.src_layout.addWidget(self.srcused_groupbox)
        self.srcprod_groupbox = QtWidgets.QFrame(self.src_widget)
        self.srcprod_groupbox.setObjectName("srcprod_groupbox")
        self.srcprod_layout = QtWidgets.QVBoxLayout(self.srcprod_groupbox)
        self.srcprod_layout.setObjectName("srcprod_layout")
        self.lbl_dataset_title_2 = QtWidgets.QLabel(self.srcprod_groupbox)
        self.lbl_dataset_title_2.setStyleSheet("font: bold;")
        self.lbl_dataset_title_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_dataset_title_2.setObjectName("lbl_dataset_title_2")
        self.srcprod_layout.addWidget(self.lbl_dataset_title_2)
        self.label_35 = QtWidgets.QLabel(self.srcprod_groupbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy)
        self.label_35.setStyleSheet("font: italic;")
        self.label_35.setWordWrap(True)
        self.label_35.setObjectName("label_35")
        self.srcprod_layout.addWidget(self.label_35)
        spacerItem3 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.srcprod_layout.addItem(spacerItem3)
        self.src_layout.addWidget(self.srcprod_groupbox)
        self.verticalLayout_5.addWidget(self.src_widget)
        self.widget_proccont = QtWidgets.QWidget(self.fgdc_procstep)
        self.widget_proccont.setObjectName("widget_proccont")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_proccont)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5.addWidget(self.widget_proccont)
        spacerItem4 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_3.addWidget(self.fgdc_procstep)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Describe the processing step or method below:"))
        self.fgdc_procdesc.setPlainText(_translate("Form", "Development of the dataset by the agency / individuals identified in the \'Originator\' element in the Identification Info section of the record."))
        self.label_37.setText(_translate("Form", "Process Date (YYYYMMDD)"))
        self.lbl_dataset_title.setText(_translate("Form", "Source Used Citation Abbreviation(s)"))
        self.label_34.setText(_translate("Form", "List any data sources used in this step.  These can be listed in sources section below."))
        self.lbl_dataset_title_2.setText(_translate("Form", "Source Produced Citation Abbreviation (s)"))
        self.label_35.setText(_translate("Form", "List data produced from this step that was used in a subsequent step.  These must also be added to the source inputs below. "))

from growingtextedit import GrowingTextEdit
