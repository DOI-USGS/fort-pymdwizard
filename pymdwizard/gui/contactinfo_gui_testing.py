import sys

from lxml import etree

from PyQt4 import QtGui
from PyQt4 import QtCore

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.ui_files import contact_info
from pymdwizard.gui.ui_files import contact_info_main
from pymdwizard.gui.ui_files import usgs_contact_importer


class ContactInfoWidget(QtGui.QWidget):

    WIDGET_WIDTH = 805
    COLLAPSED_HEIGHT = 75
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT

    def __init__(self, parent=None):

        if __name__ == "__main__":
            QtGui.QMainWindow.__init__(self, parent)

        self.ui = contact_info_main.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.ui.rbtn_yes.toggled.connect(self.contact_used_change)
        self.ui.mouseMoveEvent = self.mouseMoveEvent

        self.contact_info_widget = QtGui.QWidget(self)
        self.contact_info_ui = contact_info.Ui_USGSContactInfoWidget()
        self.contact_info_ui.setupUi(self.contact_info_widget)
        self.contact_info_widget.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.ui.main_layout.addWidget(self.contact_info_widget)

        self.collapsed_size = QtCore.QSize(self.WIDGET_WIDTH, self.COLLAPSED_HEIGHT)
        self.expanded_size = QtCore.QSize(self.WIDGET_WIDTH, self.EXPANDED_HEIGHT)

        self.contact_info_ui.btn_import_contact.clicked.connect(self.usgs_contact)
        self.setMouseTracking(True)
        self.setup_dragdrop(self)

    def usgs_contact(self):
        self.usgs_contact = QtGui.QDialog(self)
        self.usgs_contact_ui = usgs_contact_importer.Ui_ImportUsgsUser()
        self.usgs_contact_ui.setupUi(self.usgs_contact)
        self.usgs_contact_ui.buttonBox.clicked.connect(self.button_pressed)
        self.usgs_contact_ui.le_usgs_ad_name.returnPressed.connect(self.add_contact)

        self.usgs_contact.show()

    def button_pressed(self, button):
        if button.text() == 'OK':
            self.add_contact()
        elif button.text() == 'Cancel':
            self.usgs_contact.deleteLater()

    def add_contact(self):
            username = self.usgs_contact_ui.le_usgs_ad_name.text()
            # strip off the @usgs.gov if they entered one
            username = username.split("@")[0]

            contact_information = utils.get_usgs_contact_info(username)
            if contact_information['cntperp']['cntper'].strip():
                self._from_xml(contact_information)
                self.usgs_contact.deleteLater()
            else:
                QtGui.QMessageBox.warning(self.usgs_contact, "Name Not Found", "The Metadata Wizard was unable to locate the provided user name in the USGS directory")

    def contact_used_change(self, b):
        self.animation = QtCore.QPropertyAnimation(self, "size")
        self.animation.setDuration(250)
        if b:
            self.animation.setEndValue(self.expanded_size)
            self.animation.start()
        else:
            self.animation.setEndValue(self.collapsed_size)
            self.animation.start()

    def _to_xml(self):

        cntinfo = etree.Element("cntinfo")

        cntperp = etree.Element("cntperp")
        cntper = etree.Element("cntper")
        cntper.text = self.findChild(QtGui.QLineEdit, "cntper").text()
        cntorg = etree.Element("cntorg")
        cntorg.text = self.findChild(QtGui.QLineEdit, "cntorg").text()
        cntperp.append(cntper)
        cntperp.append(cntorg)
        cntinfo.append(cntperp)

        cntpos = etree.Element("cntpos")
        cntpos.text = self.findChild(QtGui.QLineEdit, "cntpos").text()
        cntinfo.append(cntpos)

        cntaddr = etree.Element("cntaddr")
        addrtype = etree.Element("addrtype")
        addrtype.text = self.findChild(QtGui.QComboBox, "addrtype").currentText()
        cntaddr.append(addrtype)

        for label in ['address', 'address2', 'address3', 'city', 'state',
                      'postal', 'country']:
            widget = self.findChild(QtGui.QLineEdit, label)
            try:

                if widget.text().strip():
                    node = etree.Element(label)
                    node.text = widget.text()
                    cntaddr.append(node)
            except:
                pass

        cntinfo.append(cntaddr)

        return cntinfo

    def _from_xml(self, contact_information):
        utils.populate_widget(self, contact_information)

    def dropEvent(self, e):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        element = etree.fromstring(e.mimeData().text(), parser=parser)
        contact_dict = xml_utils.node_to_dict(element)
        self._from_xml(contact_dict)

    def dragEnterEvent(self, e):
        e.accept()

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(etree.tostring(self._to_xml(), pretty_print=True).decode())

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)

    def setup_dragdrop(self, widget):

        # QtGui.QWidget.setMouseTracking(widget, True)

        try:
            widget.setMouseTracking(True)
            widget.setAcceptDrops(True)
            widget.mouseMoveEvent = self.mouseMoveEvent
            widget.setDragEnabled(True)
        except:
            pass

        for child in widget.findChildren(QtCore.QObject):
            self.setup_dragdrop(child)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myApp')
    dialog = ContactInfoWidget()
    dialog.resize(dialog.collapsed_size)
    dialog.show()
    sys.exit(app.exec_())

