"""Smoke test for the FGDCDate widget construction.

Historical note: this file previously held a commented-out from_xml/to_xml
test for a compound date-range widget (the old MetadataDate.MetadataDate with a
QStackedWidget and range_date1/range_date2). That widget no longer exists. The
current date widget is the single-date fgdc_date.FGDCDate, which has a flat
set_date()/get_date() API and no from_xml/to_xml. Its behavior is covered by
test_single_date.py; this file just verifies the widget constructs cleanly.
"""

from pymdwizard.gui import fgdc_date


def test_fgdc_date_constructs(qtbot):
    """FGDCDate instantiates and registers with qtbot without error."""
    widget = fgdc_date.FGDCDate()
    qtbot.addWidget(widget)

    # Sanity: the date input widget is wired up and starts empty.
    assert widget.get_date() == ""
