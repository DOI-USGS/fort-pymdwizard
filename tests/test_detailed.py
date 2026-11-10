#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.
License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/
PURPOSE
------------------------------------------------------------------------------
pytest-qt tests for the Detailed (entity and attribute) widget
(pymdwizard/gui/detailed.py), covering File Geodatabase loading through
populate_from_fname():
1. A file picked inside a .gdb folder (its 'gdb' file) loads the geodatabase.
2. With several feature classes, the user is prompted and the chosen one is
   loaded, with object ID and Shape defaults filled in.
3. Cancelling the feature class prompt loads nothing.


NOTES
------------------------------------------------------------------------------
The geodatabase is built in tmp_path by the gdb_path fixture in conftest.py.
QInputDialog.getItem is patched so the feature class prompt never blocks, and
QMessageBox.warning is patched so a read error fails the test instead of
opening a dialog.
"""

# Standard python libraries.
import os

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QInputDialog, QMessageBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.gui import detailed
except ImportError as err:
    raise ImportError(err, __file__)


def _make_widget(qtbot, mocker):
    """
    Construct a Detailed widget registered with qtbot, with
    QMessageBox.warning patched and returned so tests can assert that no
    error dialog was shown.
    """
    widget = detailed.Detailed()
    qtbot.addWidget(widget)
    warning = mocker.patch.object(QMessageBox, "warning")
    return widget, warning


def _attr_labels(widget):
    return [attr.ui.fgdc_attrlabl.text() for attr in widget.attributes.attrs]


def test_gdb_file_inside_folder_loads_chosen_feature_class(
    qtbot, mocker, gdb_path
):
    widget, warning = _make_widget(qtbot, mocker)
    get_item = mocker.patch.object(
        QInputDialog, "getItem", return_value=("wells", True)
    )

    # The file dialog can't select a folder, so the user picks the 'gdb'
    # file inside it.
    widget.populate_from_fname(os.path.join(gdb_path, "gdb"))

    warning.assert_not_called()
    get_item.assert_called_once()
    offered_layers = get_item.call_args[0][3]
    assert sorted(offered_layers) == ["roads", "wells"]

    assert (
        widget.ui.fgdc_enttypl.text() == "sample.gdb (wells) Feature Class"
    )
    assert _attr_labels(widget) == ["OBJECTID", "Shape", "name", "depth"]

    oid_attr = widget.attributes.get_attr("OBJECTID")
    assert oid_attr.ui.fgdc_attrdef.toPlainText() == "Internal feature number."
    assert oid_attr.ui.fgdc_attrdefs.text() == "ESRI"
    shape_attr = widget.attributes.get_attr("Shape")
    assert shape_attr.ui.fgdc_attrdef.toPlainText() == "Feature geometry."
    assert shape_attr.ui.fgdc_attrdefs.text() == "ESRI"


def test_gdb_folder_path_loads_other_feature_class(qtbot, mocker, gdb_path):
    widget, warning = _make_widget(qtbot, mocker)
    mocker.patch.object(QInputDialog, "getItem", return_value=("roads", True))

    widget.populate_from_fname(gdb_path)

    warning.assert_not_called()
    assert (
        widget.ui.fgdc_enttypl.text() == "sample.gdb (roads) Feature Class"
    )
    assert _attr_labels(widget) == ["OBJECTID", "Shape", "name"]


def test_gdb_cancelled_prompt_loads_nothing(qtbot, mocker, gdb_path):
    widget, warning = _make_widget(qtbot, mocker)
    mocker.patch.object(QInputDialog, "getItem", return_value=("", False))

    widget.populate_from_fname(os.path.join(gdb_path, "gdb"))

    warning.assert_not_called()
    assert widget.ui.fgdc_enttypl.text() == ""
    assert widget.attributes.attrs == []
