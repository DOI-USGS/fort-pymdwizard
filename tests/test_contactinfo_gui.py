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

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    contact = test_record.xpath("idinfo/ptcontac/cntinfo")[0]

    widget._from_xml(contact)
    assert widget.findChild(QLineEdit, 'fgdc_cntper').text() == "Jay Diffendorfer"
    assert widget.findChild(QLineEdit, 'fgdc_cntpos').text() == ""
    assert widget.findChild(QLineEdit, 'fgdc_cntvoice').text() == "303-236-5369"
    assert widget.findChild(QLineEdit, 'fgdc_cntemail').text() == "jediffendorfer@usgs.gov"
    assert widget.findChild(QLineEdit, 'fgdc_postal').text() == "80225"


def test_contactinfo__to_xml(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)



    widget.findChild(QLineEdit, 'fgdc_cntper').setText("Jay Diffendorfer")
    widget.findChild(QLineEdit, 'fgdc_cntpos').setText("")
    widget.findChild(QLineEdit, 'fgdc_cntvoice').setText("303-236-5369")
    widget.findChild(QLineEdit, 'fgdc_cntemail').setText("jediffendorfer@usgs.gov")
    widget.findChild(QLineEdit, 'fgdc_postal').setText("80225")

    cntinfo = widget._to_xml()

    assert etree.tostring(cntinfo, pretty_print=True).decode() \
    == """<cntinfo>
  <cntperp>
    <cntper>Jay Diffendorfer</cntper>
  </cntperp>
  <cntaddr>
    <addrtype>Mailing</addrtype>
    <address/>
    <city/>
    <state/>
    <postal>80225</postal>
  </cntaddr>
  <cntvoice>303-236-5369</cntvoice>
  <cntemail>jediffendorfer@usgs.gov</cntemail>
</cntinfo>
"""


