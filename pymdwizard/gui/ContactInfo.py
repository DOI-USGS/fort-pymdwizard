#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Contact Info <cntinfo> widget


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

import sys

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core.xml_utils import xml_node

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_ContactInfo
from pymdwizard.gui.ui_files import UI_USGSContactImporter

class ContactInfo(WizardWidget):

    drag_label = "Contact Information <cntinfo>"
    acceptable_tags = ['ptcontac', 'cntinfo']

    ui_class = UI_ContactInfo.Ui_USGSContactInfoWidget

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.btn_import_contact.clicked.connect(self.find_usgs_contact)
        self.per_or_org = self.ui.fgdc_cntperp
        self.ui.rbtn_perp.toggled.connect(self.switch_primary)

    def find_usgs_contact(self):
        self.usgs_contact = QDialog(parent=self)
        self.usgs_contact_ui = UI_USGSContactImporter.Ui_ImportUsgsUser()
        self.usgs_contact_ui.setupUi(self.usgs_contact)
        self.usgs_contact_ui.btn_OK.clicked.connect(self.add_contact)
        self.usgs_contact_ui.btn_cancel.clicked.connect(self.cancel)
        utils.set_window_icon(self.usgs_contact)
        self.usgs_contact.show()

    def add_contact(self):
        username = self.usgs_contact_ui.le_usgs_ad_name.text()
        # strip off the @usgs.gov if they entered one
        username = username.split("@")[0]

        if not username:
            return

        try:
            cntperp = utils.get_usgs_contact_info(username,
                                                  as_dictionary=False)
            if cntperp.getchildren()[0].getchildren()[0].text.strip():
                self._from_xml(cntperp)
                self.usgs_contact.deleteLater()
            else:
                msg = QMessageBox(self)
                utils.set_window_icon(msg)
                msg.setIcon(QMessageBox.Information)
                msg.setText("'{}' Not Found".format(username))
                msg.setInformativeText("The Metadata Wizard was unable to locate the provided user name in the USGS directory")
                msg.setWindowTitle("Name Not Found")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        except:
            msg_text = "Make sure there is a working Internet connection or try again latter."
            msg = QMessageBox(self)
            utils.set_window_icon(msg)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Issue encountered while searching contact information.")
            msg.setInformativeText(msg_text)
            msg.setWindowTitle("Problem encountered")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def cancel(self):
        self.usgs_contact.deleteLater()

    def switch_primary(self):
        """
        Switches form to reflect either organization or person primary

        Returns
        -------
        None
        """
        if self.ui.rbtn_perp.isChecked():
            self.per_or_org.layout().insertWidget(0, self.ui.lbl_cntper)
            self.ui.required_horizontal_layout.insertWidget(0, self.ui.fgdc_cntper)
            self.per_or_org.layout().insertWidget(2, self.ui.lbl_cntorg)
            self.ui.optional_horizontal_layout.insertWidget(0, self.ui.fgdc_cntorg)
        else:
            self.per_or_org.layout().insertWidget(0, self.ui.lbl_cntorg)
            self.ui.required_horizontal_layout.insertWidget(0, self.ui.fgdc_cntorg)
            self.per_or_org.layout().insertWidget(2, self.ui.lbl_cntper)
            self.ui.optional_horizontal_layout.insertWidget(0, self.ui.fgdc_cntper)

    def _to_xml(self):

        cntinfo = xml_node("cntinfo")

        cntper_str = self.findChild(QLineEdit, "fgdc_cntper").text()
        cntorg_str = self.findChild(QLineEdit, "fgdc_cntorg").text()

        rbtn_perp = self.findChild(QRadioButton, 'rbtn_perp')
        if rbtn_perp.isChecked():
            cntperp = xml_node("cntperp", parent_node=cntinfo)
            cntper = xml_node("cntper", cntper_str, cntperp)
            if cntorg_str:
                cntorg = xml_node("cntorg", cntorg_str, cntperp)
        else:
            cntorgp = xml_node("cntorgp", parent_node=cntinfo)
            cntper = xml_node("cntorg", cntorg_str, cntorgp)
            if cntper_str:
                cntper = xml_node("cntper", cntper_str, cntorgp)

        cntpos_str = self.findChild(QLineEdit, "fgdc_cntpos").text()
        if cntpos_str:
            cntpos = xml_node("cntpos", cntpos_str, cntinfo)

        cntaddr = xml_node("cntaddr", parent_node=cntinfo)

        addrtype_str = self.findChild(QComboBox, "fgdc_addrtype").currentText()
        addrtype = xml_node("addrtype", addrtype_str, cntaddr)

        address_str = self.findChild(QLineEdit, "fgdc_address").text()
        node = xml_node('address', address_str, cntaddr)
        address2_str = self.findChild(QLineEdit, "fgdc_address2").text()
        if address2_str:
            node = xml_node('address', address2_str, cntaddr)
        address3_str = self.findChild(QLineEdit, "fgdc_address3").text()
        if address3_str:
            node = xml_node('address', address3_str, cntaddr)

        for label in ['city', 'state',
                      'postal']:
            widget_str = self.findChild(QLineEdit, "fgdc_" + label).text()
            try:
                node = xml_node(label, widget_str, cntaddr)
            except:
                pass

        country_str = self.ui.fgdc_country.text()
        if country_str:
            node = xml_node('country', country_str, cntaddr)

        for label in ['cntvoice', 'cntfax', 'cntemail']:
            widget_str = self.findChild(QLineEdit, "fgdc_" + label).text()
            try:
                if label == 'cntvoice' or widget_str:
                    node = xml_node(label, widget_str, cntinfo)
            except:
                pass


        return cntinfo

    def _from_xml(self, contact_information):

        self.clear_widget()

        contact_dict = xml_utils.node_to_dict(contact_information)
        utils.populate_widget(self, contact_dict)

        addrtype_widget = self.findChild(QComboBox, 'fgdc_addrtype')

        if 'cntinfo' in contact_dict:
            contact_dict = contact_dict['cntinfo']
        if 'fgdc_cntinfo' in contact_dict:
            contact_dict = contact_dict['fgdc_cntinfo']

        try:
            addrtype = contact_dict['cntaddr']['addrtype']
            addrtype_widget.setEditText(addrtype)
        except KeyError:
            pass

        try:
            if 'fgdc_cntorgp' in contact_dict:
                rbtn_orgp = self.findChild(QRadioButton, 'rbtn_orgp')
                rbtn_orgp.setChecked(True)
            elif 'fgdc_cntperp' in contact_dict:
                rbtn_perp = self.findChild(QRadioButton, 'rbtn_perp')
                rbtn_perp.setChecked(True)
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(ContactInfo)
