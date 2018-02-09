from __future__ import print_function

# import sys
# sys.path.append(r"../..")

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import sys
from pytestqt import qtbot
from lxml import etree

from PyQt5.QtWidgets import QLineEdit, QComboBox, QTabWidget, QStackedWidget
from PyQt5.QtCore import QDate

from pymdwizard.gui import spatial_tab


def test_import(qtbot):
    widget = spatial_tab.SpatialTab()
    qtbot.addWidget(widget)

    fname = "tests/data/projections/wgs84.shp"
    widget.populate_from_fname(fname)

    assert widget.spdom.ui.fgdc_northbc.text() == '39.3367364'


