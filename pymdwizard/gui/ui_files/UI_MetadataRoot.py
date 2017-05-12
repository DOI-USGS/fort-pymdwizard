# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MetadataRoot.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_metadata_root(object):
    def setupUi(self, metadata_root):
        metadata_root.setObjectName("metadata_root")
        metadata_root.resize(1327, 585)
        metadata_root.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/Ducky.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        metadata_root.setWindowIcon(icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(metadata_root)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(metadata_root)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.frame.setStyleSheet("QFrame {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(150, 150, 150, 70), stop:1 rgba(255, 255, 255, 255));\n"
"}\n"
"\n"
"QToolButton{\n"
"    background-color: none;\n"
"    color:rgb(0, 170, 255);\n"
"    border:none;\n"
"    font: 13pt \"Arial\";\n"
"}\n"
"\n"
"QToolButton:Checked, QToolButton:Pressed{\n"
"    background-color: rgb(193, 210, 238);\n"
"    font: bold 13pt \"Arial\";\n"
"    border: 1px solid rgb(60, 127, 177);\n"
"}\n"
"\n"
"QToolButton:Hover {\n"
"    background-color:rgb(224,232,245);\n"
"}\n"
"\n"
"QToolButton:checked:Hover{\n"
"    background-color: rgb(193, 210, 238);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.idinfo_button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idinfo_button.sizePolicy().hasHeightForWidth())
        self.idinfo_button.setSizePolicy(sizePolicy)
        self.idinfo_button.setCheckable(True)
        self.idinfo_button.setChecked(True)
        self.idinfo_button.setAutoExclusive(True)
        self.idinfo_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.idinfo_button.setObjectName("idinfo_button")
        self.horizontalLayout.addWidget(self.idinfo_button)
        self.dataquality_button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataquality_button.sizePolicy().hasHeightForWidth())
        self.dataquality_button.setSizePolicy(sizePolicy)
        self.dataquality_button.setCheckable(True)
        self.dataquality_button.setChecked(False)
        self.dataquality_button.setAutoExclusive(True)
        self.dataquality_button.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.dataquality_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.dataquality_button.setObjectName("dataquality_button")
        self.horizontalLayout.addWidget(self.dataquality_button)
        self.spatial_button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spatial_button.sizePolicy().hasHeightForWidth())
        self.spatial_button.setSizePolicy(sizePolicy)
        self.spatial_button.setCheckable(True)
        self.spatial_button.setChecked(False)
        self.spatial_button.setAutoExclusive(True)
        self.spatial_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.spatial_button.setObjectName("spatial_button")
        self.horizontalLayout.addWidget(self.spatial_button)
        self.eainfo_button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eainfo_button.sizePolicy().hasHeightForWidth())
        self.eainfo_button.setSizePolicy(sizePolicy)
        self.eainfo_button.setCheckable(True)
        self.eainfo_button.setChecked(False)
        self.eainfo_button.setAutoExclusive(True)
        self.eainfo_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.eainfo_button.setObjectName("eainfo_button")
        self.horizontalLayout.addWidget(self.eainfo_button)
        self.distinfo_button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distinfo_button.sizePolicy().hasHeightForWidth())
        self.distinfo_button.setSizePolicy(sizePolicy)
        self.distinfo_button.setCheckable(True)
        self.distinfo_button.setChecked(False)
        self.distinfo_button.setAutoExclusive(True)
        self.distinfo_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.distinfo_button.setObjectName("distinfo_button")
        self.horizontalLayout.addWidget(self.distinfo_button)
        self.metainfo_button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.metainfo_button.sizePolicy().hasHeightForWidth())
        self.metainfo_button.setSizePolicy(sizePolicy)
        self.metainfo_button.setCheckable(True)
        self.metainfo_button.setChecked(False)
        self.metainfo_button.setAutoExclusive(True)
        self.metainfo_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.metainfo_button.setObjectName("metainfo_button")
        self.horizontalLayout.addWidget(self.metainfo_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.frame)
        self.fgdc_metadata = QtWidgets.QStackedWidget(metadata_root)
        self.fgdc_metadata.setObjectName("fgdc_metadata")
        self.page_idinfo = QtWidgets.QWidget()
        self.page_idinfo.setObjectName("page_idinfo")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_idinfo)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.fgdc_metadata.addWidget(self.page_idinfo)
        self.page_dataqual = QtWidgets.QWidget()
        self.page_dataqual.setObjectName("page_dataqual")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_dataqual)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fgdc_metadata.addWidget(self.page_dataqual)
        self.page_spatial = QtWidgets.QWidget()
        self.page_spatial.setObjectName("page_spatial")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_spatial)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.fgdc_metadata.addWidget(self.page_spatial)
        self.page_eainfo = QtWidgets.QWidget()
        self.page_eainfo.setObjectName("page_eainfo")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_eainfo)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.fgdc_metadata.addWidget(self.page_eainfo)
        self.page_distinfo = QtWidgets.QWidget()
        self.page_distinfo.setObjectName("page_distinfo")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.page_distinfo)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.fgdc_metadata.addWidget(self.page_distinfo)
        self.page_metainfo = QtWidgets.QWidget()
        self.page_metainfo.setObjectName("page_metainfo")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_metainfo)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fgdc_metadata.addWidget(self.page_metainfo)
        self.verticalLayout_2.addWidget(self.fgdc_metadata)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(metadata_root)
        self.fgdc_metadata.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(metadata_root)

    def retranslateUi(self, metadata_root):
        _translate = QtCore.QCoreApplication.translate
        metadata_root.setWindowTitle(_translate("metadata_root", "Form"))
        self.idinfo_button.setText(_translate("metadata_root", "Identification"))
        self.dataquality_button.setText(_translate("metadata_root", "Data Quality"))
        self.spatial_button.setText(_translate("metadata_root", "Spatial"))
        self.eainfo_button.setText(_translate("metadata_root", "Entity and Attribute"))
        self.distinfo_button.setText(_translate("metadata_root", "Distribution"))
        self.metainfo_button.setText(_translate("metadata_root", "Metadata Reference"))

