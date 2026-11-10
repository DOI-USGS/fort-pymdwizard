"""Tests for the Citeinfo (citation) widget.

Covers the from_xml -> widget round trip (populating the widget from an FGDC
citeinfo element) and the to_xml serialization.
"""

from lxml import etree
from PyQt5.QtWidgets import QLineEdit

from pymdwizard.gui import citeinfo

POLARBEARS_FIXTURE = "tests/data/USGS_ASC_PolarBears_FGDC.xml"


def test_citation_from_xml(qtbot):
    """from_xml populates the citation fields from a real FGDC citeinfo node.

    Replaces a previously commented-out test that referenced the old
    Citation.Citation class; the current widget is citeinfo.Citeinfo.
    """
    widget = citeinfo.Citeinfo()
    qtbot.addWidget(widget)

    record = etree.parse(POLARBEARS_FIXTURE)
    citeinfo_node = record.xpath("idinfo/citation/citeinfo")[0]

    widget.from_xml(citeinfo_node)

    # Title, publication date, and geoform come through from the record.
    assert widget.ui.fgdc_title.toPlainText().startswith(
        "Catalogue of Polar Bear"
    )
    assert widget.ui.pubdate_widget.ui.fgdc_caldate.text() == "20101231"
    assert widget.ui.fgdc_geoform.currentText() == "Tabular Digital Data"


def test_citation_to_xml(qtbot):
    widget = citeinfo.Citeinfo()
    qtbot.addWidget(widget)

    widget.ui.fgdc_title.setPlainText("test title")
    widget.ui.pubdate_widget.set_date("1234")
    widget.ui.fgdc_geoform.setCurrentText("book")

    widget.ui.radio_seriesyes.setChecked(True)
    series = widget.findChild(QLineEdit, "fgdc_sername")
    series2 = widget.findChild(QLineEdit, "fgdc_issue")
    series.setText("Name 25")
    series2.setText("Issue 45")

    cit = widget.to_xml()

    assert (
        etree.tostring(cit, pretty_print=True).decode()
        == """<citeinfo>
  <origin/>
  <pubdate>1234</pubdate>
  <title>test title</title>
  <geoform>book</geoform>
  <serinfo>
    <sername>Name 25</sername>
    <issue>Issue 45</issue>
  </serinfo>
</citeinfo>
"""
    )
