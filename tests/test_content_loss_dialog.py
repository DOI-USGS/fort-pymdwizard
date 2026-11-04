"""Unittests for gui.content_loss_dialog"""

from PyQt5.QtCore import Qt

from pymdwizard.gui.content_loss_dialog import ContentLossDialog


def _make_dialog(qtbot, html_text="<p>hello</p>", default_key="b"):
    dialog = ContentLossDialog(
        None,
        title="t",
        html_text=html_text,
        buttons=[("Button A", "a"), ("Button B", "b")],
        default_key=default_key,
    )
    qtbot.addWidget(dialog)
    return dialog


def test_dialog_records_pressed_button(qtbot):
    dialog = _make_dialog(qtbot)
    dialog.buttons["a"].click()

    assert dialog.clicked_key == "a"


def test_dialog_closed_without_choosing_has_no_key(qtbot):
    dialog = _make_dialog(qtbot)
    dialog.reject()

    assert dialog.clicked_key is None


def test_dialog_has_no_whats_this_button(qtbot):
    # Regression: Qt adds a "?" button to dialogs on Windows. There is no
    # help text behind it here, so it must not be shown.
    dialog = _make_dialog(qtbot)

    assert not dialog.windowFlags() & Qt.WindowContextHelpButtonHint


def test_dialog_default_button(qtbot):
    dialog = _make_dialog(qtbot, default_key="b")

    assert dialog.buttons["b"].isDefault()
    assert not dialog.buttons["a"].isDefault()


def test_dialog_is_resizable_and_scrolls_long_text(qtbot):
    long_html = "".join("<p>line {}</p>".format(i) for i in range(300))
    dialog = _make_dialog(qtbot, html_text=long_html)

    assert dialog.isSizeGripEnabled()
    # Opens capped in height; the rest scrolls.
    assert dialog.height() < 800
    assert dialog.browser.verticalScrollBar().maximum() >= 0
    assert "line 299" in dialog.browser.toPlainText()
