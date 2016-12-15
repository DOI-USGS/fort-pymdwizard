from PyQt4 import QtGui
from PyQt4 import QtCore

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import Ui_WidgetName

class WidgetName((WizardWidget):

#drag_label = "Some human readable label <content xpath root>"

# This dictionary provides a mechanism for crosswalking between
# gui elements (pyqt widgets) and the xml document
    xpath_lookup = {'cntper': 'cntinfo/cntperp/cntper',
                    'cntorg': 'cntinfo/cntperp/cntorg',
                    'cntpos': 'cntinfo/cntpos',}

self.ui_class = Ui_WidgetName.Ui_WidgetName

def connect_events(self):
    self.ui.some_button.clicked.connect(self.do_something)

def do_something(self):
    print('I did something')

def _to_xml(self):
    # add code here to translate the form into xml representation
    xml = "<metadata></metadata>"
return xml

def _from_xml(self, xml_element):
# add code here to translate the form back into xml