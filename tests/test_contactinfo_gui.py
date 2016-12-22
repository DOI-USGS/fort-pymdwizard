from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt4 import QtGui

from pymdwizard.gui import ContactInfoPointOfContact

def test_contactinfo_gui(qtbot):
    widget = ContactInfoPointOfContact.ContactInfoPointOfContact()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    contact = test_record.xpath("idinfo/ptcontac/cntinfo")[0]

    widget._from_xml(contact)
    assert widget.findChild(QtGui.QLineEdit, 'cntper').text() == "Jay Diffendorfer"
    assert widget.findChild(QtGui.QLineEdit, 'cntpos').text() == ""
    assert widget.findChild(QtGui.QLineEdit, 'cntvoice').text() == "303-236-5369"
    assert widget.findChild(QtGui.QLineEdit, 'cntemail').text() == "jediffendorfer@usgs.gov"
    assert widget.findChild(QtGui.QLineEdit, 'postal').text() == "80225"

