#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

PURPOSE
------------------------------------------------------------------------------
pytest-qt tests for the Spdom spatial-domain widget (pymdwizard/gui/spdom.py),
covering two behaviors:

1. Silent map-drag North/South auto-correction.
2. The non-modal North/South ordering inline cue on the manual-entry path.

Map-drag auto-correction:
    A corner drag that inverts the pair is silently corrected so North >=
    South, the East/West values are left unchanged, and no modal dialog is
    shown.

Manual-entry inline cue:
    For a manually entered North/South pair with north < south, coord_updated
    presents the non-modal inline cue and leaves the North/South field values
    exactly as typed (no swap, no modal dialog). Entering an ordered pair
    (north >= south) or a non-comparable entry clears any previously shown cue.


NOTES
------------------------------------------------------------------------------
These tests drive the corner-drag handler, _enforce_ns_order(), and
coord_updated() directly. The Leaflet/WebEngine JavaScript bridge is not
exercised: update_map and evaluate_js (which run JavaScript via the WebEngine
bridge) are patched so the tests stay focused on the coordinate-field logic and
never touch a QWebEngine page. QMessageBox.warning is patched to assert the
silent auto-correction and ordering paths never open a dialog.

coord_updated() reads self.sender().objectName(), so the integration-style
checks drive the field's editingFinished signal to set the sender during
dispatch.
"""

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QMessageBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.gui import spdom
except ImportError as err:
    raise ImportError(err, __file__)


def _make_widget(qtbot, mocker):
    """
    Construct an Spdom widget registered with qtbot, with the live map/JS
    bridge calls patched out so the tests never touch a QWebEngine page.

    update_map and evaluate_js run JavaScript against the Leaflet map via the
    WebEngine bridge; patching both keeps the tests focused on the
    coordinate-field logic. Patching evaluate_js in addition to update_map is
    safe for the map-drag tests (which only require update_map patched).
    """

    widget = spdom.Spdom()
    qtbot.addWidget(widget)

    # No live JS bridge during tests: stub the map refresh and JS execution.
    mocker.patch.object(widget, "update_map")
    mocker.patch.object(widget, "evaluate_js")

    return widget


# ===========================================================================
# Map-drag auto-correction tests
# ===========================================================================

def test_drag_handler_silently_corrects_inverted_ns(qtbot, mocker):
    """
    A corner drag that produces North < South is silently corrected so
    North >= South, without a dialog.
    """

    widget = _make_widget(qtbot, mocker)

    # Assert no dialog is shown on the drag auto-correction path.
    warn = mocker.patch.object(QMessageBox, "warning")

    # Normal-editing path (not an XML load) so format_bounding does not run and
    # the test targets the field-ordering logic directly.
    widget.in_xml_load = False

    # Pre-set South high; then drag the NE corner to a LOW latitude so the
    # handler sets North below South, i.e. an inverted pair.
    widget.ui.fgdc_southbc.setText("41.25")
    widget.handle_ne_move(lat=34.95, lng=-100.0)

    north = float(widget.ui.fgdc_northbc.text())
    south = float(widget.ui.fgdc_southbc.text())

    # North must end up >= South after correction.
    assert north >= south

    # The multiset of latitudes is preserved (values swapped, not invented).
    assert sorted([north, south]) == sorted([34.95, 41.25])

    # No modal dialog shown during the drag correction.
    warn.assert_not_called()


def test_drag_handler_leaves_east_west_unchanged(qtbot, mocker):
    """
    The North/South correction on the map-drag path leaves the East and West
    coordinate values unchanged.
    """

    widget = _make_widget(qtbot, mocker)
    warn = mocker.patch.object(QMessageBox, "warning")
    widget.in_xml_load = False

    # Establish a known East/West state and a South that will invert on drag.
    widget.ui.fgdc_eastbc.setText("-64.5843")
    widget.ui.fgdc_westbc.setText("-178.6194")
    widget.ui.fgdc_southbc.setText("41.25")

    east_before = widget.ui.fgdc_eastbc.text()
    west_before = widget.ui.fgdc_westbc.text()

    # Drag the SW corner to a HIGH latitude, inverting the pair (South > North).
    # The SW handler sets South; East is untouched by the handler, and the
    # correction path must not alter East or West.
    widget.handle_sw_move(lat=88.0, lng=-150.0)

    # North/South corrected.
    assert float(widget.ui.fgdc_northbc.text()) >= float(
        widget.ui.fgdc_southbc.text())

    # East unchanged. West is set by this handler (it is the dragged longitude
    # field), so it is not asserted unchanged here.
    assert widget.ui.fgdc_eastbc.text() == east_before

    warn.assert_not_called()

    # Sanity: the West field that the handler set holds the dragged longitude,
    # confirming only the intended longitude field moved.
    assert west_before != widget.ui.fgdc_westbc.text()


def test_enforce_ns_order_swaps_inverted_pair(qtbot, mocker):
    """
    _enforce_ns_order swaps an inverted pair in place, returns True, and shows
    no dialog. East/West are untouched.
    """

    widget = _make_widget(qtbot, mocker)
    warn = mocker.patch.object(QMessageBox, "warning")

    # Inverted pair set directly in the fields.
    widget.ui.fgdc_northbc.setText("34.95")
    widget.ui.fgdc_southbc.setText("41.25")
    widget.ui.fgdc_eastbc.setText("-64.5843")
    widget.ui.fgdc_westbc.setText("-178.6194")

    east_before = widget.ui.fgdc_eastbc.text()
    west_before = widget.ui.fgdc_westbc.text()

    swapped = widget._enforce_ns_order()

    assert swapped is True
    north = float(widget.ui.fgdc_northbc.text())
    south = float(widget.ui.fgdc_southbc.text())
    assert north >= south
    assert sorted([north, south]) == sorted([34.95, 41.25])

    # East and West unchanged by the N/S correction.
    assert widget.ui.fgdc_eastbc.text() == east_before
    assert widget.ui.fgdc_westbc.text() == west_before

    # No dialog shown.
    warn.assert_not_called()


def test_enforce_ns_order_leaves_ordered_pair_unchanged(qtbot, mocker):
    """
    _enforce_ns_order returns False and leaves values unchanged for an already
    ordered North/South pair.
    """

    widget = _make_widget(qtbot, mocker)
    warn = mocker.patch.object(QMessageBox, "warning")

    # Already ordered: North >= South.
    widget.ui.fgdc_northbc.setText("41.25")
    widget.ui.fgdc_southbc.setText("34.95")
    widget.ui.fgdc_eastbc.setText("-64.5843")
    widget.ui.fgdc_westbc.setText("-178.6194")

    north_before = widget.ui.fgdc_northbc.text()
    south_before = widget.ui.fgdc_southbc.text()
    east_before = widget.ui.fgdc_eastbc.text()
    west_before = widget.ui.fgdc_westbc.text()

    swapped = widget._enforce_ns_order()

    assert swapped is False
    assert widget.ui.fgdc_northbc.text() == north_before
    assert widget.ui.fgdc_southbc.text() == south_before
    assert widget.ui.fgdc_eastbc.text() == east_before
    assert widget.ui.fgdc_westbc.text() == west_before

    warn.assert_not_called()


def test_enforce_ns_order_negative_latitudes(qtbot, mocker):
    """
    _enforce_ns_order corrects an inverted Southern-Hemisphere pair (the
    negative-latitude case that motivated the report).
    """

    widget = _make_widget(qtbot, mocker)
    warn = mocker.patch.object(QMessageBox, "warning")

    # Inverted negative latitudes: North (-40) < South (-10).
    widget.ui.fgdc_northbc.setText("-40.0")
    widget.ui.fgdc_southbc.setText("-10.0")

    swapped = widget._enforce_ns_order()

    assert swapped is True
    north = float(widget.ui.fgdc_northbc.text())
    south = float(widget.ui.fgdc_southbc.text())
    assert north >= south
    assert sorted([north, south]) == sorted([-40.0, -10.0])

    warn.assert_not_called()


# ===========================================================================
# Manual-entry inline cue tests
# ===========================================================================

# ---------------------------------------------------------------------------
# Manual entry inversion shows the cue and retains typed values
# ---------------------------------------------------------------------------

def test_inverted_manual_entry_shows_cue_and_retains_values(qtbot, mocker):
    """
    Set an inverted North/South pair (north < south) and trigger coord_updated
    via the field's editingFinished signal (which sets sender()). The inline
    cue must activate, the typed values must be retained unchanged, and no
    modal QMessageBox must be raised for the ordering case.
    """

    widget = _make_widget(qtbot, mocker)

    # Spy on the modal warning so we can assert the ordering case never opens
    # a dialog. return_value keeps any incidental call non-blocking.
    warn = mocker.patch.object(QMessageBox, "warning",
                               return_value=QMessageBox.Ok)

    # Inverted pair: North below South (the reported bug scenario).
    widget.ui.fgdc_northbc.setText("34.95")
    widget.ui.fgdc_southbc.setText("41.25")

    # Drive coord_updated through the real signal path so self.sender() is set
    # to the North field during dispatch.
    widget.ui.fgdc_northbc.editingFinished.emit()

    # Cue is active and the status label is visible.
    assert widget._ns_cue_active is True
    assert widget.ui.ns_order_cue.isHidden() is False

    # Typed values are retained exactly (no swap on the manual-entry path).
    assert widget.ui.fgdc_northbc.text() == "34.95"
    assert widget.ui.fgdc_southbc.text() == "41.25"

    # No modal dialog for the ordering case.
    warn.assert_not_called()


# ---------------------------------------------------------------------------
# Valid manual ordering clears any previously shown cue
# ---------------------------------------------------------------------------

def test_valid_manual_ordering_clears_cue(qtbot, mocker):
    """
    Starting from a cue-active state, entering an ordered pair (north >= south)
    and triggering coord_updated clears the cue.
    """

    widget = _make_widget(qtbot, mocker)
    mocker.patch.object(QMessageBox, "warning", return_value=QMessageBox.Ok)

    # Establish the cue-active state from an inverted entry.
    widget.ui.fgdc_northbc.setText("34.95")
    widget.ui.fgdc_southbc.setText("41.25")
    widget.ui.fgdc_northbc.editingFinished.emit()
    assert widget._ns_cue_active is True

    # Now enter an ordered pair (North >= South) and re-trigger.
    widget.ui.fgdc_northbc.setText("41.25")
    widget.ui.fgdc_southbc.setText("34.95")
    widget.ui.fgdc_northbc.editingFinished.emit()

    # Cue cleared and status label hidden.
    assert widget._ns_cue_active is False
    assert widget.ui.ns_order_cue.isHidden() is True


def test_non_numeric_entry_does_not_raise_ordering_cue(qtbot, mocker):
    """
    Non-numeric / empty entries are not comparable, so ns_is_inverted returns
    False and the ordering cue is cleared rather than falsely raised.
    """

    widget = _make_widget(qtbot, mocker)
    mocker.patch.object(QMessageBox, "warning", return_value=QMessageBox.Ok)

    # Start from a cue-active state.
    widget.ui.fgdc_northbc.setText("34.95")
    widget.ui.fgdc_southbc.setText("41.25")
    widget.ui.fgdc_northbc.editingFinished.emit()
    assert widget._ns_cue_active is True

    # A non-numeric North value is not comparable -> cue must clear.
    widget.ui.fgdc_northbc.setText("not-a-number")
    widget.ui.fgdc_northbc.editingFinished.emit()
    assert widget._ns_cue_active is False
    assert widget.ui.ns_order_cue.isHidden() is True

    # An empty South value is likewise not comparable -> cue stays cleared.
    widget.ui.fgdc_northbc.setText("41.25")
    widget.ui.fgdc_southbc.setText("")
    widget.ui.fgdc_southbc.editingFinished.emit()
    assert widget._ns_cue_active is False
    assert widget.ui.ns_order_cue.isHidden() is True


# ---------------------------------------------------------------------------
# Direct _set_ns_cue contract (both indications toggle together)
# ---------------------------------------------------------------------------

def test_set_ns_cue_contract_activate_and_clear(qtbot, mocker):
    """
    _set_ns_cue is the single toggle for the inline cue. Active shows the label,
    sets _ns_cue_active, and applies the error stylesheet to both N/S fields;
    inactive hides the label, clears the flag, and resets the stylesheets.
    """

    widget = _make_widget(qtbot, mocker)

    # Activate the cue.
    widget._set_ns_cue(True)
    assert widget._ns_cue_active is True
    assert widget.ui.ns_order_cue.isHidden() is False
    assert widget.ui.fgdc_northbc.styleSheet() == spdom.NS_ERROR_FIELD_STYLE
    assert widget.ui.fgdc_southbc.styleSheet() == spdom.NS_ERROR_FIELD_STYLE

    # Clear the cue.
    widget._set_ns_cue(False)
    assert widget._ns_cue_active is False
    assert widget.ui.ns_order_cue.isHidden() is True
    assert widget.ui.fgdc_northbc.styleSheet() == ""
    assert widget.ui.fgdc_southbc.styleSheet() == ""
