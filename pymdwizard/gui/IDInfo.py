import sys
from lxml import etree

from PyQt4 import QtGui
from PyQt4 import QtCore

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_idinfo
from pymdwizard.gui.ContactInfoPointOfContact import ContactInfoPointOfContact

class IdInfo(WizardWidget):

    drag_label = "Identification Information <idinfo>"

    # This dictionary provides a mechanism for crosswalking between
    # gui elements (pyqt widgets) and the xml document
    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
                        'cntorg': 'cntinfo/cntperp/cntorg',
                        'cntpos': 'cntinfo/cntpos',}

    ui_class = UI_idinfo.Ui_idinfo

    def build_ui(self):

        self.ui = UI_idinfo.Ui_idinfo()
        self.ui.setupUi(self)

        self.main_layout = self.ui.main_layout
        self.setup_dragdrop(self)

        self.ptcontac = ContactInfoPointOfContact(parent=self)


        section1 = QtGui.QHBoxLayout()
        section1.setObjectName("hbox1")
        section1.addWidget(self.ptcontac)
        self.main_layout.addLayout(section1)


    def _to_xml(self):
        print(self)
        # add code here to translate the form into xml representation
        idinfo_node = etree.Element('idinfo')

        ptcontac = self.ptcontac._to_xml()
        idinfo_node.append(ptcontac)

        return idinfo_node

    def _from_xml(self, xml_idinfo):
        idinfo_dict = xml_utils.node_to_dict(xml_idinfo)
        utils.populate_widget(self, idinfo_dict)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    app.title = 'test'
    dialog = IdInfo()
    dialog.setWindowTitle("WidgetName")
    # dialog.resize(dialog.collapsed_size)
    dialog.show()
    sys.exit(app.exec_())