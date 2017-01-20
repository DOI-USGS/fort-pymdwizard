from __future__ import print_function

import sys
sys.path.append(r"../..")

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QWidget, QLineEdit

from pymdwizard.gui import ContactInfo

def test_contactinfo__from_xml(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    test_record_fname = "C:/Users/mhannon/dev_mdwizard/pymdwizard/tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    contact = test_record.xpath("idinfo/ptcontac/cntinfo")[0]

    widget._from_xml(contact)
    assert widget.findChild(QLineEdit, 'cntper').text() == "Jay Diffendorfer"
    assert widget.findChild(QLineEdit, 'cntpos').text() == ""
    assert widget.findChild(QLineEdit, 'cntvoice').text() == "303-236-5369"
    assert widget.findChild(QLineEdit, 'cntemail').text() == "jediffendorfer@usgs.gov"
    assert widget.findChild(QLineEdit, 'postal').text() == "80225"

