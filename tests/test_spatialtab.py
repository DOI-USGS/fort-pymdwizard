
from pymdwizard.gui import spatial_tab


def test_import(qtbot):
    widget = spatial_tab.SpatialTab()
    qtbot.addWidget(widget)

    fname = "tests/data/projections/wgs84.shp"
    widget.populate_from_fname(fname)

    assert widget.spdom.ui.fgdc_northbc.text() == "39.3367"
