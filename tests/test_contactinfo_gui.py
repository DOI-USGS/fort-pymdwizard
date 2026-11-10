
import types

from lxml import etree
from PyQt5.QtWidgets import QLabel, QLineEdit

from pymdwizard.gui import ContactInfo


def test_contactinfo_from_xml(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_States_through_July2013.xml"
    test_record = etree.parse(test_record_fname)
    contact = test_record.xpath("idinfo/ptcontac/cntinfo")[0]

    widget.from_xml(contact)
    assert widget.findChild(QLineEdit, "fgdc_cntper").text() == "Jay Diffendorfer"
    assert widget.findChild(QLineEdit, "fgdc_cntpos").text() == ""
    assert widget.findChild(QLineEdit, "fgdc_cntvoice").text() == "303-236-5369"
    assert (
        widget.findChild(QLineEdit, "fgdc_cntemail").text() == "jediffendorfer@usgs.gov"
    )
    assert widget.findChild(QLineEdit, "fgdc_postal").text() == "80225"


def test_contactinfo_to_xml(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    widget.findChild(QLineEdit, "fgdc_cntper").setText("Jay Diffendorfer")
    widget.findChild(QLineEdit, "fgdc_cntpos").setText("")
    widget.findChild(QLineEdit, "fgdc_cntvoice").setText("303-236-5369")
    widget.findChild(QLineEdit, "fgdc_cntemail").setText("jediffendorfer@usgs.gov")
    widget.findChild(QLineEdit, "fgdc_postal").setText("80225")

    cntinfo = widget.to_xml()

    assert (
        etree.tostring(cntinfo, pretty_print=True).decode()
        == """<cntinfo>
  <cntperp>
    <cntper>Jay Diffendorfer</cntper>
  </cntperp>
  <cntaddr>
    <addrtype>mailing</addrtype>
    <address/>
    <city/>
    <state/>
    <postal>80225</postal>
  </cntaddr>
  <cntvoice>303-236-5369</cntvoice>
  <cntemail>jediffendorfer@usgs.gov</cntemail>
</cntinfo>
"""
    )


# ---------------------------------------------------------------------------
# cntinst (Contact Instructions): an optional, multi-line field that follows
# the email address in the FGDC sequence.
# ---------------------------------------------------------------------------

CNTINST_TEXT = (
    "The contact email address is a generic address in the event the person "
    "is no longer with USGS. (updated on 20240319)"
)

CONTACT_WITH_CNTINST = """<cntinfo>
  <cntorgp><cntorg>U.S. Geological Survey</cntorg></cntorgp>
  <cntaddr>
    <addrtype>mailing</addrtype>
    <address>2150 Centre Avenue</address>
    <city>Fort Collins</city>
    <state>CO</state>
    <postal>80526</postal>
  </cntaddr>
  <cntvoice>970-226-9100</cntvoice>
  <cntemail>fort@usgs.gov</cntemail>
  <cntinst>{}</cntinst>
</cntinfo>""".format(
    CNTINST_TEXT
)


def _contact_with_cntinst():
    return etree.fromstring(CONTACT_WITH_CNTINST)


def test_cntinst_from_xml(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    widget.from_xml(_contact_with_cntinst())

    assert widget.ui.fgdc_cntinst.text() == CNTINST_TEXT


def test_cntinst_to_xml_follows_email(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    widget.from_xml(_contact_with_cntinst())
    cntinfo = widget.to_xml()

    # Last in the FGDC sequence, directly after the email address.
    assert [child.tag for child in cntinfo][-2:] == ["cntemail", "cntinst"]
    assert cntinfo.find("cntinst").text == CNTINST_TEXT


def test_cntinst_is_optional(qtbot):
    # No instructions entered: the element must not be written at all, not
    # even as an empty tag.
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    widget.from_xml(_contact_with_cntinst())
    widget.ui.fgdc_cntinst.setText("")
    assert widget.to_xml().find("cntinst") is None

    # Whitespace alone counts as empty.
    widget.ui.fgdc_cntinst.setText("   ")
    assert widget.to_xml().find("cntinst") is None


def test_cntinst_round_trip_keeps_text(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    widget.from_xml(_contact_with_cntinst())
    reloaded = ContactInfo.ContactInfo()
    qtbot.addWidget(reloaded)
    reloaded.from_xml(widget.to_xml())

    assert reloaded.ui.fgdc_cntinst.text() == CNTINST_TEXT


def test_cntinst_with_a_line_break_in_the_source(qtbot):
    # The field is one line. Record how a value that spans lines in the XML
    # is handled, so a change in behavior is noticed.
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    contact = etree.fromstring(CONTACT_WITH_CNTINST)
    contact.find("cntinst").text = "Call first.\nThen email."
    widget.from_xml(contact)

    saved = widget.to_xml().find("cntinst").text
    # Nothing is lost: both sentences survive, whatever the line break
    # becomes.
    assert "Call first." in saved and "Then email." in saved


def test_cntinst_is_cleared_with_the_widget(qtbot):
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    widget.from_xml(_contact_with_cntinst())
    widget.clear_widget()

    assert widget.ui.fgdc_cntinst.text() == ""


def test_cntinst_is_not_marked_required(qtbot):
    # Required fields carry a red asterisk label (tooltip "Required") beside
    # the input. Contact Instructions is optional, so its row must have none.
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    row = widget.ui.horizontalLayout_cntinst
    row_widgets = [row.itemAt(i).widget() for i in range(row.count())]
    assert not any(isinstance(w, QLabel) for w in row_widgets)
    # Same single-line box as Email Address, not a taller multi-line one.
    assert isinstance(widget.ui.fgdc_cntinst, QLineEdit)
    assert widget.ui.label_cntinst.text() == "Contact Instructions"
    assert "*" not in widget.ui.label_cntinst.text()


def test_cntinst_shows_fgdc_help(qtbot):
    # Like every fgdc_ widget, the app fills in the field's name as its
    # tooltip and keeps the schema definition for the help display.
    widget = ContactInfo.ContactInfo()
    qtbot.addWidget(widget)

    assert widget.ui.fgdc_cntinst.toolTip() == "Contact Instructions"
    assert "supplemental instructions" in widget.ui.fgdc_cntinst.help_text


def test_cntinst_survives_in_every_place_a_contact_appears(qtbot):
    # Real records had Contact Instructions on the metadata contact and on a
    # process step contact. Both embed ContactInfo, so both must keep it.
    from pymdwizard.gui.ProcessStep import ProcessStep
    from pymdwizard.gui.metainfo import MetaInfo

    process = ProcessStep()
    qtbot.addWidget(process)
    procstep = etree.fromstring(
        "<procstep><procdesc>step</procdesc><procdate>2024</procdate>"
        "<proccont>{}</proccont></procstep>".format(CONTACT_WITH_CNTINST)
    )
    process.from_xml(procstep)
    assert (
        process.to_xml().find("proccont/cntinfo/cntinst").text == CNTINST_TEXT
    )

    meta = MetaInfo()
    qtbot.addWidget(meta)
    # A standalone MetaInfo has no main window to switch the schema on.
    meta.root_widget = types.SimpleNamespace(switch_schema=lambda schema: None)
    metainfo = etree.fromstring(
        "<metainfo><metd>20240101</metd><metc>{}</metc>"
        "<metstdn>FGDC Content Standard for Digital Geospatial Metadata"
        "</metstdn><metstdv>FGDC-STD-001-1998</metstdv></metainfo>".format(
            CONTACT_WITH_CNTINST
        )
    )
    meta.from_xml(metainfo)
    assert meta.to_xml().find("metc/cntinfo/cntinst").text == CNTINST_TEXT
