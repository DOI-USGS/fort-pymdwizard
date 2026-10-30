
import os
import shutil
import time

import pytest
from PyQt5.QtWidgets import QMessageBox, QPlainTextEdit
from pytestqt.qt_compat import qt_api

from pymdwizard import __version__
from pymdwizard.gui import MainWindow


@pytest.fixture(autouse=True)
def _no_blocking_content_loss_dialog(mocker):
    """
    Opening a record can raise the content-loss dialog (a real modal
    dialog). Make it return immediately, as if closed without choosing, in
    every test in this module so nothing blocks or writes backup files as a
    side effect. Tests that exercise the dialog install their own patch,
    which takes precedence. QMessageBox is patched too, for other modal
    message boxes.
    """
    mocker.patch.object(MainWindow.QMessageBox, "exec_", lambda self: 0)
    mocker.patch.object(MainWindow.ContentLossDialog, "exec_", lambda self: 0)


def test_mainwindow_from_xml(qtbot, mocker):

    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    test_record_fname = "tests/data/GenericFGDCTemplate_FGDCtemp.xml"
    with mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.No):
        widget.open_file(test_record_fname)

        assert (
            widget.metadata_root.findChild(QPlainTextEdit, "fgdc_logic").toPlainText()
            == "No formal logical accuracy tests were conducted. testing"
        )


def test_mainwindow_to_xml(qtbot):
    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    widget.metadata_root.findChild(QPlainTextEdit, "fgdc_logic").setPlainText(
        "this is a test"
    )
    dc = widget.metadata_root.to_xml()

    assert dc.xpath("dataqual/logic")[0].text == "this is a test"


def test_validation(qtbot, mocker, tmp_path):

    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    # Open a copy in tmp_path so the review doc (written next to the input as
    # <name>_REVIEW.docx) and any save land in the temp dir, not the repo.
    test_record_fname = str(tmp_path / "USGS_ASC_PolarBears_FGDC.xml")
    shutil.copy("tests/data/USGS_ASC_PolarBears_FGDC.xml", test_record_fname)

    with mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.No), \
         mocker.patch.object(QMessageBox, "warning", return_value=QMessageBox.Cancel), \
         mocker.patch.object(QMessageBox, "information", return_value=QMessageBox.Cancel):
        widget.open_file(test_record_fname)
        widget.validate()
        assert len(widget.error_list.errors) == 1

        # Don't launch Word (or any OS handler) during the test run.
        mocker.patch.object(os, "startfile", create=True)
        mocker.patch("pymdwizard.gui.MainWindow.subprocess.call")

        widget.last_updated = time.time()
        widget.generate_review_doc()

    # The review doc is created alongside the (temp) input, not in tests/data.
    expected_doc = str(tmp_path / "USGS_ASC_PolarBears_FGDC_REVIEW.docx")
    assert os.path.exists(expected_doc)


def test_splash(qtbot):

    MainWindow.show_splash()
    MainWindow.show_splash("2.1.9")


def test_misc(qtbot, mocker):
    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    with mocker.patch.object(QMessageBox, "about", return_value=QMessageBox.Ok):
        widget.about()


def test_settings(qtbot, mocker):

    settings = qt_api.QtCore.QSettings(
        "USGS_" + __version__, "pymdwizard_" + __version__
    )
    # Save original value to restore after test
    original_template = settings.value("template_fname")
    settings.setValue("template_fname", "tests/data/USGS_ASC_PolarBears_FGDC.xml")

    widget = MainWindow.PyMdWizardMainForm()
    qtbot.addWidget(widget)

    widget.get_save_name = lambda: "test_output.xml"

    with mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.No):
        widget.new_record()

        md = widget.metadata_root.to_xml()
        os.remove("test_output.xml")

        assert md.xpath("idinfo/spdom/bounding/westbc")[0].text == "178.2167"

    # Restore original setting
    if original_template is None:
        settings.remove("template_fname")
    else:
        settings.setValue("template_fname", original_template)


# ---------------------------------------------------------------------------
# Content-loss handling: detecting, previewing, and recording content the
# form cannot represent so it is not dropped silently. The functional dialog
# (with the backup offer) fires at import; a lighter notice fires at save.
# ---------------------------------------------------------------------------

import html as _html
import re as _re

from pymdwizard.core import xml_utils

MainForm = MainWindow.PyMdWizardMainForm
Dialog = MainWindow.ContentLossDialog


def _plain(rich):
    """
    Reduce the dialogs' rich-text (HTML) to plain text: one line per
    paragraph, bullet, or line break, tags removed, entities decoded. Lets
    assertions check content and order without depending on the exact
    markup.
    """
    text = _re.sub(r"</p>|</li>|<br\s*/?>", "\n", rich)
    text = _re.sub(r"<[^>]+>", "", text)
    text = _html.unescape(text)
    return "\n".join(
        " ".join(line.split()) for line in text.splitlines() if line.strip()
    )


def test_original_backup_name_keeps_xml_extension():
    # The copy of the original keeps a usable .xml extension so it opens like
    # any other record: myrecord.xml -> myrecord.original.xml.
    assert MainForm._original_backup_name("/data/myrecord.xml") == (
        "/data/myrecord.original.xml"
    )
    # Missing extension defaults to .xml.
    assert MainForm._original_backup_name("/data/noext") == (
        "/data/noext.original.xml"
    )


def test_preview_not_truncated_for_short_list():
    # A handful of single-value groups fits entirely in the dialog, so no
    # sidecar file is needed.
    dropped = [
        ("metadata/distinfo/stdorder/fees", ["none"]),
        ("metadata/spdoinfo/direct", ["Vector"]),
        ("metadata/customext/@units", ["meters"]),
    ]
    assert MainForm._preview_is_truncated(dropped) is False


def test_preview_truncated_when_caps_exceeded():
    many_groups = [("metadata/s{}/leaf".format(i), ["v"]) for i in range(10)]
    many_values = [
        ("metadata/idinfo/keywords/theme/themekey", ["a", "b", "c", "d", "e"])
    ]
    # A long value only forces truncation once the list is no longer short.
    long_value = [
        ("metadata/distinfo/stdorder/ordering", ["x " * 80]),
        ("metadata/a/b", ["1"]),
        ("metadata/a/c", ["2"]),
        ("metadata/a/d", ["3"]),
    ]

    assert MainForm._preview_is_truncated(many_groups) is True
    assert MainForm._preview_is_truncated(many_values) is True
    assert MainForm._preview_is_truncated(long_value) is True

    # A short list is always shown in full, however long the value.
    short_long = [("metadata/distinfo/stdorder/ordering", ["x " * 80])]
    assert MainForm._preview_is_truncated(short_long) is False


def test_format_dropped_preview_groups_and_caps():
    dropped = [
        (
            "metadata/idinfo/keywords/theme/themekey",
            ["alpha", "beta", "gamma", "delta", "epsilon"],
        ),
        ("metadata/customext/@units", ["meters"]),
    ]
    preview = MainForm._format_dropped_preview(dropped)

    lines = _plain(preview).splitlines()

    # Each value is one bullet: field label, the full XML path of the field
    # (without the leading "metadata/"), then the value.
    tag_line = next(l for l in lines if "themekey" in l)
    i = lines.index(tag_line)
    assert lines[i + 1 : i + 3] == ["idinfo/keywords/theme/themekey", "alpha"]
    assert "metadata/" not in preview
    # Per-group cap of 4 collapses the fifth value.
    assert "+1 more in idinfo/keywords/theme" in lines
    # Attribute is labelled by its tag, with its full path and value.
    i = lines.index("@units")
    assert lines[i + 1 : i + 3] == ["customext/@units", "meters"]
    # Rendered as a bulleted list.
    assert preview.startswith("<ul") and preview.count("<li") == 6


def test_unique_path_never_overwrites(tmp_path):
    first = str(tmp_path / "record.original.xml")
    assert MainForm._unique_path(first) == first

    open(first, "w").close()
    second = MainForm._unique_path(first)
    assert second == str(tmp_path / "record.original-2.xml")

    open(second, "w").close()
    assert MainForm._unique_path(first) == str(
        tmp_path / "record.original-3.xml"
    )


def _click_button_matching(mocker, substring):
    """
    Mock ContentLossDialog.exec_ so the dialog "clicks" the button whose
    label contains substring. Used to drive the import/save dialogs
    headlessly.
    """

    def fake_exec(self):
        self.clicked_key = None
        for key, button in self.buttons.items():
            if substring in button.text():
                self.clicked_key = key
                break
        return 0

    mocker.patch.object(Dialog, "exec_", fake_exec)


def _button_labels(dialog):
    return [button.text() for button in dialog.buttons.values()]


ORIGINAL_WITH_EXTRA = (
    "<metadata>"
    "<spdoinfo><direct>Vector</direct></spdoinfo>"
    "<customext units='meters'>99</customext>"
    "</metadata>"
)
ROUNDTRIP_WITHOUT_EXTRA = (
    "<metadata><spdoinfo><direct>Vector</direct></spdoinfo></metadata>"
)


def _stub_probe(mocker, widget, produced_xml):
    """Make the import probe's to_xml return a fixed tree (no GUI populate)."""
    mocker.patch.object(
        widget.metadata_root,
        "to_xml",
        return_value=xml_utils.string_to_node(produced_xml),
    )


def test_import_check_keeps_byte_exact_copy_of_original(
    qtbot, mocker, tmp_path
):
    # Choosing "Keep a copy" copies the file on disk byte for byte, so the
    # user gets exactly what they opened (not a re-serialized tree).
    widget = MainForm()
    qtbot.addWidget(widget)
    _stub_probe(mocker, widget, ROUNDTRIP_WITHOUT_EXTRA)

    fname = tmp_path / "record.xml"
    fname.write_bytes(
        b"<?xml version='1.0'?>\n<!-- keep me -->\n"
        + ORIGINAL_WITH_EXTRA.encode()
    )

    _click_button_matching(mocker, "Keep a copy")
    widget.check_content_loss_on_import(
        str(fname), xml_utils.string_to_node(ORIGINAL_WITH_EXTRA)
    )

    backup = tmp_path / "record.original.xml"
    assert widget.import_backup_fname == str(backup)
    assert backup.read_bytes() == fname.read_bytes()


def test_import_check_continue_without_copy(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)
    _stub_probe(mocker, widget, ROUNDTRIP_WITHOUT_EXTRA)

    fname = tmp_path / "record.xml"
    fname.write_text(ORIGINAL_WITH_EXTRA)

    _click_button_matching(mocker, "Continue without")
    widget.check_content_loss_on_import(
        str(fname), xml_utils.string_to_node(ORIGINAL_WITH_EXTRA)
    )

    # The loss is remembered for the save notice, but no copy was written.
    assert widget.import_dropped
    assert widget.import_backup_fname is None
    assert not (tmp_path / "record.original.xml").exists()


def test_import_check_silent_when_everything_fits(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)
    _stub_probe(mocker, widget, ROUNDTRIP_WITHOUT_EXTRA)

    shown = []
    mocker.patch.object(Dialog, "exec_", lambda self: shown.append(1))

    widget.check_content_loss_on_import(
        str(tmp_path / "record.xml"),
        xml_utils.string_to_node(ROUNDTRIP_WITHOUT_EXTRA),
    )

    assert shown == []
    assert widget.import_dropped == []


def test_import_check_failure_does_not_block_opening(qtbot, mocker, tmp_path):
    # If the probe itself blows up, the file must still open: the check is a
    # courtesy and may not turn into a new way to fail to load a record.
    widget = MainForm()
    qtbot.addWidget(widget)
    mocker.patch.object(
        widget.metadata_root, "to_xml", side_effect=RuntimeError("boom")
    )

    shown = []
    mocker.patch.object(Dialog, "exec_", lambda self: shown.append(1))

    widget.check_content_loss_on_import(
        str(tmp_path / "record.xml"),
        xml_utils.string_to_node(ORIGINAL_WITH_EXTRA),
    )

    assert shown == []
    assert widget.import_dropped == []


def test_backup_never_overwrites_an_earlier_copy(qtbot, tmp_path):
    # Reopening a record after a lossy save must not replace the first copy,
    # which is the only one that still holds the true original.
    widget = MainForm()
    qtbot.addWidget(widget)

    fname = tmp_path / "record.xml"
    fname.write_text("true original")
    first = widget._write_original_backup(str(fname))

    fname.write_text("lossy rewrite")
    second = widget._write_original_backup(str(fname))

    assert first != second
    assert open(first).read() == "true original"
    assert open(second).read() == "lossy rewrite"


def test_save_notice_uses_import_result_not_current_edits(
    qtbot, mocker
):
    # Regression: the save notice must not re-diff the edited form against the
    # original, or every ordinary edit would be reported as "dropped".
    widget = MainForm()
    qtbot.addWidget(widget)

    shown = []
    mocker.patch.object(Dialog, "exec_", lambda self: shown.append(1))

    # Nothing was flagged at import; the user then edits freely.
    widget.import_dropped = []
    widget.notify_content_loss_on_save()

    assert shown == []


def test_save_notice_is_info_only_when_copy_was_kept(qtbot, mocker):
    # With a copy of the original on disk, nothing is lost by saving, so the
    # notice is informational: no Cancel, never blocks, shown once.
    widget = MainForm()
    qtbot.addWidget(widget)

    widget.import_dropped = [("metadata/customext", ["99"])]
    widget.import_backup_fname = "/data/record.original.xml"

    seen = []

    def fake_exec(self):
        seen.append((self.text(), _button_labels(self)))
        return 0

    mocker.patch.object(Dialog, "exec_", fake_exec)

    assert widget.notify_content_loss_on_save() is True
    assert widget.notify_content_loss_on_save() is True

    assert len(seen) == 1
    text, buttons = seen[0]
    lines = _plain(text).splitlines()
    i = lines.index("customext")
    assert lines[i : i + 3] == ["customext", "customext", "99"]
    # The copy is named on its own line, by file name only.
    assert "record.original.xml" in lines
    assert "/data/" not in text
    assert not any("Cancel" in b for b in buttons)
    assert widget.import_dropped == []


def test_save_notice_offers_cancel_when_no_copy_was_kept(qtbot, mocker):
    widget = MainForm()
    qtbot.addWidget(widget)

    widget.import_dropped = [("metadata/customext", ["99"])]
    widget.import_backup_fname = None

    seen = []

    def fake_exec(self):
        default = next(
            b.text() for b in self.buttons.values() if b.isDefault()
        )
        seen.append((self.text(), _button_labels(self), default))
        self.clicked_key = None
        return 0

    mocker.patch.object(Dialog, "exec_", fake_exec)

    # Closing the dialog without choosing must cancel the save.
    assert widget.notify_content_loss_on_save() is False

    text, buttons, default = seen[0]
    assert "No copy of the original was kept" in text
    assert any("Save anyway" in b for b in buttons)
    assert any("Cancel" in b for b in buttons)
    # Enter/Esc must land on the safe choice.
    assert "Cancel" in default


def test_save_notice_cancel_aborts_and_asks_again(qtbot, mocker):
    widget = MainForm()
    qtbot.addWidget(widget)

    widget.import_dropped = [("metadata/customext", ["99"])]
    widget.import_backup_fname = None

    _click_button_matching(mocker, "Cancel")
    assert widget.notify_content_loss_on_save() is False

    # Cancelling must not consume the warning: it appears on the next save.
    assert widget.import_dropped


def test_save_notice_save_anyway_proceeds_once(qtbot, mocker):
    widget = MainForm()
    qtbot.addWidget(widget)

    widget.import_dropped = [("metadata/customext", ["99"])]
    widget.import_backup_fname = None

    _click_button_matching(mocker, "Save anyway")
    assert widget.notify_content_loss_on_save() is True
    assert widget.import_dropped == []

    # Nothing left to report on later saves.
    assert widget.notify_content_loss_on_save() is True


def test_save_file_stops_when_notice_is_cancelled(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)

    fname = tmp_path / "record.xml"
    fname.write_text("untouched")
    widget.cur_fname = str(fname)

    mocker.patch.object(widget, "notify_content_loss_on_save", return_value=False)
    mocker.patch.object(MainWindow.utils, "check_fname", return_value="good")

    widget.save_file()

    # The user backed out, so the file on disk was not rewritten.
    assert fname.read_text() == "untouched"


def test_template_load_skips_content_loss_check(qtbot, mocker):
    # A template is not the user's record: no dialog on New, and no backup
    # files written next to the template.
    widget = MainForm()
    qtbot.addWidget(widget)

    check = mocker.patch.object(MainForm, "check_content_loss_on_import")
    widget.load_default()

    check.assert_not_called()


def test_loading_a_real_record_offers_and_writes_copy(qtbot, mocker, tmp_path):
    # End to end on a real USGS record whose attribute-domain and entity
    # details the form cannot fully hold: load it, accept the copy, and check
    # the copy is identical to what was opened.
    widget = MainForm()
    qtbot.addWidget(widget)

    source = (
        "tests/data/Onshore_Industrial_Wind_Turbine_Locations_for_the_United_"
        "States_through_July2013.xml"
    )
    fname = tmp_path / "turbines.xml"
    shutil.copy(source, fname)

    mocker.patch.object(QMessageBox, "warning", return_value=QMessageBox.Ok)
    _click_button_matching(mocker, "Keep a copy")
    widget.load_file_content(str(fname))

    assert widget.import_dropped or widget.import_rewritten
    backup = tmp_path / "turbines.original.xml"
    assert backup.exists()
    assert backup.read_bytes() == fname.read_bytes()


# ---------------------------------------------------------------------------
# Dropped vs rewritten: genuine losses are shown first; values the form only
# rewrites follow in a separate, shorter section.
# ---------------------------------------------------------------------------

DROPPED = [("metadata/customext", ["99"])]
REWRITTEN = [("metadata/metainfo/metstdn", [("old standard", "new standard")])]


def test_message_lists_dropped_before_rewritten():
    msg = MainForm._dropped_content_message(
        DROPPED, REWRITTEN, None, intro="Intro.", closing="Closing."
    )

    text = _plain(msg)
    assert text.index("Will be removed") < text.index("Will be reworded")
    assert text.index("99") < text.index("was: old standard")
    assert "now: new standard" in text
    assert text.startswith("Intro.")
    assert text.endswith("Closing.")


def test_message_omits_empty_sections():
    only_dropped = MainForm._dropped_content_message(
        DROPPED, [], None, intro="i", closing="c"
    )
    only_rewritten = MainForm._dropped_content_message(
        [], REWRITTEN, None, intro="i", closing="c"
    )

    assert "Will be reworded" not in only_dropped
    assert "Will be removed" not in only_rewritten


def test_message_counts_each_section_separately():
    dropped = [("metadata/a", ["1", "2"])]
    rewritten = [("metadata/b", [("x", "y")])]
    msg = MainForm._dropped_content_message(
        dropped, rewritten, None, intro="i", closing="c"
    )

    assert "Will be removed (2 fields)" in msg
    assert "Will be reworded (1 field)" in msg


def test_rewritten_preview_shows_was_and_now_and_caps():
    rewritten = [
        ("metadata/p{}".format(i), [("old{}".format(i), "new{}".format(i))])
        for i in range(5)
    ]
    preview = MainForm._format_rewritten_preview(rewritten)

    text = _plain(preview)
    assert "was: old0" in text
    assert "now: new0" in text
    # Capped at 3 items; the other two are summarized.
    assert "old3" not in preview
    assert "+2 more" in preview


def test_preview_truncation_accounts_for_rewritten():
    few = [("metadata/p", [("a", "b")])]
    many = [("metadata/p{}".format(i), [("a", "b")]) for i in range(4)]
    long_pair = [("metadata/p", [("x " * 80, "short")])]
    padding = [("metadata/a/b", ["1", "2", "3"])]

    assert MainForm._preview_is_truncated([], few) is False
    assert MainForm._preview_is_truncated([], many) is True
    # A long reworded value forces truncation only once the list isn't short.
    assert MainForm._preview_is_truncated([], long_pair) is False
    assert MainForm._preview_is_truncated(padding, long_pair) is True


def test_manifest_contains_both_sections(tmp_path):
    fname = str(tmp_path / "record.xml")
    manifest = MainForm._write_dropped_manifest(
        None, fname, DROPPED, REWRITTEN
    )

    # Named like the record with its extension replaced, matching the style
    # of the "<record>.original.xml" copy.
    assert manifest == str(tmp_path / "record.dropped.txt")

    text = open(manifest, encoding="utf-8").read()
    assert text.index("WILL BE REMOVED") < text.index("WILL BE REWORDED")
    assert "metadata/customext:  99" in text
    assert "was:  old standard" in text
    assert "now:  new standard" in text


def test_save_notice_rewritten_only_never_offers_cancel(qtbot, mocker):
    # Rewritten values are kept, so even with no copy of the original the
    # save is not gated: OK only, and it proceeds.
    widget = MainForm()
    qtbot.addWidget(widget)

    widget.import_dropped = []
    widget.import_rewritten = REWRITTEN
    widget.import_backup_fname = None

    seen = []

    def fake_exec(self):
        seen.append((self.text(), _button_labels(self)))
        return 0

    mocker.patch.object(Dialog, "exec_", fake_exec)

    assert widget.notify_content_loss_on_save() is True

    text, buttons = seen[0]
    assert "Will be reworded" in text
    assert "Will be removed" not in text
    assert not any("Cancel" in b for b in buttons)
    assert widget.import_rewritten == []


def test_import_check_separates_dropped_from_rewritten(
    qtbot, mocker, tmp_path
):
    widget = MainForm()
    qtbot.addWidget(widget)

    # The form drops <customext> and rewrites <metstdn>.
    _stub_probe(
        mocker,
        widget,
        "<metadata><metainfo><metstdn>new standard</metstdn></metainfo>"
        "</metadata>",
    )
    original = xml_utils.string_to_node(
        "<metadata><customext>99</customext>"
        "<metainfo><metstdn>old standard</metstdn></metainfo></metadata>"
    )
    fname = tmp_path / "record.xml"
    fname.write_text("<metadata/>")

    texts = []
    mocker.patch.object(
        Dialog, "exec_", lambda self: texts.append(self.text())
    )
    widget.check_content_loss_on_import(str(fname), original)

    assert dict(widget.import_dropped) == {"metadata/customext": ["99"]}
    assert widget.import_rewritten == [
        ("metadata/metainfo/metstdn", [("old standard", "new standard")])
    ]
    assert texts[0].index("Will be removed") < texts[0].index(
        "Will be reworded"
    )


# ---------------------------------------------------------------------------
# Dialog readability: short lists in full, short paths, plain wording, and a
# manifest named like the record.
# ---------------------------------------------------------------------------

LONG_TEXT = (
    "The metadata contact email address is a generic address in the event "
    "the person is no longer available, so that questions can still be "
    "routed to someone who can answer them."
)


def _capture_import_dialog(mocker, widget, original_xml, tmp_path, produced):
    """Run the import check headlessly; return the dialog text shown."""
    _stub_probe(mocker, widget, produced)
    fname = tmp_path / "record.xml"
    fname.write_text("<metadata/>")

    texts = []
    mocker.patch.object(
        Dialog, "exec_", lambda self: texts.append(self.text())
    )
    widget.check_content_loss_on_import(
        str(fname), xml_utils.string_to_node(original_xml)
    )
    return texts[0]


def test_short_list_shows_full_value_and_writes_no_manifest(
    qtbot, mocker, tmp_path
):
    # One long dropped field used to be cut off with "..." and pushed into a
    # manifest file. A short list is now shown whole, with no file.
    widget = MainForm()
    qtbot.addWidget(widget)

    text = _capture_import_dialog(
        mocker,
        widget,
        "<metadata><cntinst>{}</cntinst></metadata>".format(LONG_TEXT),
        tmp_path,
        "<metadata></metadata>",
    )

    assert LONG_TEXT in text
    assert "\u2026" not in text
    assert "complete list" not in text
    assert widget.import_manifest_fname is None
    assert list(tmp_path.glob("*.dropped.txt")) == []


def test_long_list_writes_manifest_named_like_the_record(
    qtbot, mocker, tmp_path
):
    # Past the short-list limit, long values are shortened and the full list
    # goes to "<record>.dropped.txt". The dialog names the file only; a full
    # path (with its forward slashes) would wrap awkwardly.
    widget = MainForm()
    qtbot.addWidget(widget)

    original = (
        "<metadata><a>{}</a><b>2</b><c>3</c><d>4</d></metadata>".format(
            LONG_TEXT
        )
    )
    text = _capture_import_dialog(
        mocker, widget, original, tmp_path, "<metadata></metadata>"
    )

    manifest = tmp_path / "record.dropped.txt"
    assert manifest.exists()
    assert widget.import_manifest_fname == str(manifest)
    assert LONG_TEXT in manifest.read_text(encoding="utf-8")
    assert LONG_TEXT not in text
    assert "record.dropped.txt" in text
    assert str(tmp_path) not in text
    assert "same folder as the file you opened" in text


def test_import_dialog_names_the_copy_it_will_make(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)

    text = _capture_import_dialog(
        mocker,
        widget,
        ORIGINAL_WITH_EXTRA,
        tmp_path,
        ROUNDTRIP_WITHOUT_EXTRA,
    )

    assert "record.original.xml" in text


def test_import_dialog_uses_plain_wording(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)

    text = _capture_import_dialog(
        mocker,
        widget,
        ORIGINAL_WITH_EXTRA,
        tmp_path,
        ROUNDTRIP_WITHOUT_EXTRA,
    )

    assert "Will be removed" in text
    assert "DROPPED" not in text
    assert "metadata/" not in text


def test_intro_action_matches_what_is_listed():
    def intro_for(dropped, rewritten):
        return MainForm._dropped_content_message(
            dropped, rewritten, None, intro="Saving will {action}.", closing=""
        )

    assert _plain(intro_for(DROPPED, [])).startswith("Saving will remove.")
    assert _plain(intro_for([], REWRITTEN)).startswith("Saving will reword.")
    assert _plain(intro_for(DROPPED, REWRITTEN)).startswith(
        "Saving will remove or reword."
    )
    # The action word is emphasized.
    assert "<b>remove</b>" in intro_for(DROPPED, [])


def test_display_path_drops_leading_metadata():
    assert MainForm._display_path("metadata/idinfo/keywords") == (
        "idinfo/keywords"
    )
    assert MainForm._display_path("metadata") == "(top level)"
    assert MainForm._display_path("") == "(top level)"
    assert MainForm._display_path("other/path") == "other/path"


def test_top_level_element_is_labelled_top_level():
    msg = MainForm._dropped_content_message(
        DROPPED, [], None, intro="i", closing="c"
    )

    lines = _plain(msg).splitlines()
    i = lines.index("customext")
    # Label, then the path (just the element, since it is top level), then
    # the value.
    assert lines[i : i + 3] == ["customext", "customext", "99"]


# ---------------------------------------------------------------------------
# Rich-text dialog layout: readable field names, escaping, hanging indent,
# and the message box actually rendering HTML.
# ---------------------------------------------------------------------------


def test_field_label_uses_readable_fgdc_name():
    # Names come from resources/FGDC/bdp_lookup.
    label = MainForm._field_label("cntinst")

    assert _plain(label) == "Contact Instructions (cntinst)"
    assert "<b>Contact Instructions</b>" in label


def test_field_label_falls_back_to_tag():
    assert _plain(MainForm._field_label("customext")) == "customext"
    assert _plain(MainForm._field_label("@units")) == "@units"


def test_values_are_html_escaped():
    # Record values can contain markup characters; they must display as
    # text, not be interpreted as formatting.
    dropped = [("metadata/a/b", ["<b>bold</b> & co"])]
    rewritten = [("metadata/c/d", [("x < y", "x > y")])]
    msg = MainForm._dropped_content_message(
        dropped, rewritten, None, intro="i", closing="c & d"
    )

    assert "<b>bold</b> & co" not in msg
    assert "&lt;b&gt;bold&lt;/b&gt; &amp; co" in msg
    text = _plain(msg)
    assert "<b>bold</b> & co" in text
    assert "was: x < y" in text
    assert "c & d" in text


def test_each_field_is_one_bullet_with_label_path_and_value():
    # Label, path and value share one <li>, separated by line breaks, so a
    # long value wraps under the bullet text instead of back to the margin.
    preview = MainForm._format_dropped_preview(
        [("metadata/metainfo/metc/cntinfo/cntinst", ["a long value"])]
    )

    bullets = _re.findall(r"<li[^>]*>(.*?)</li>", preview)
    assert len(bullets) == 1
    parts = bullets[0].split("<br/>")
    assert _plain(parts[0]) == "Contact Instructions (cntinst)"
    # The path includes the field itself, so it is a complete location.
    assert _plain(parts[1]) == "metainfo/metc/cntinfo/cntinst"
    assert parts[2] == "a long value"


def test_path_is_normal_size():
    # Regression: the path used to be in <small>, which was hard to read.
    preview = MainForm._format_dropped_preview(
        [("metadata/metainfo/metc/cntinfo/cntinst", ["v"])]
    )
    rewritten = MainForm._format_rewritten_preview(
        [("metadata/metainfo/metstdn", [("a", "b")])]
    )

    assert "<small" not in preview and "<small" not in rewritten
    assert "font-size" not in preview and "font-size" not in rewritten


def test_rewritten_is_bulleted_too():
    preview = MainForm._format_rewritten_preview(REWRITTEN)
    bullets = _re.findall(r"<li[^>]*>(.*?)</li>", preview)

    assert len(bullets) == 1
    assert _plain(bullets[0]).splitlines() == [
        "Metadata Standard Name (metstdn)",
        "metainfo/metstdn",
        "was: old standard",
        "now: new standard",
    ]


def test_every_dialog_block_sets_bottom_margin():
    # Qt gives <p> and <li> a default bottom margin, which opens uneven
    # gaps. Every block must set it to 0 explicitly.
    msg = MainForm._dropped_content_message(
        DROPPED,
        REWRITTEN,
        "record.dropped.txt",
        intro="i",
        closing="c",
        closing_emphasis="record.original.xml",
    )
    blocks = _re.findall(r"<(?:p|li|ul)(?: style=\"([^\"]*)\")?>", msg)

    assert blocks
    assert all("margin-bottom:0px" in s for s in blocks)


def test_closing_emphasis_is_its_own_bold_line():
    msg = MainForm._dropped_content_message(
        DROPPED,
        [],
        None,
        intro="i",
        closing="It will be saved as:",
        closing_emphasis="record.original.xml",
    )

    lines = _plain(msg).splitlines()
    assert lines[-2:] == ["It will be saved as:", "record.original.xml"]
    assert "<b>record.original.xml</b>" in msg


def test_both_dialogs_use_the_resizable_dialog(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)

    shown = []
    mocker.patch.object(Dialog, "exec_", lambda self: shown.append(self))

    _stub_probe(mocker, widget, ROUNDTRIP_WITHOUT_EXTRA)
    fname = tmp_path / "record.xml"
    fname.write_text("<metadata/>")
    widget.check_content_loss_on_import(
        str(fname), xml_utils.string_to_node(ORIGINAL_WITH_EXTRA)
    )

    widget.import_dropped = DROPPED
    widget.import_backup_fname = None
    widget.notify_content_loss_on_save()

    assert len(shown) == 2
    for dialog in shown:
        assert dialog.isSizeGripEnabled()
        # The rich text renders in a scrollable browser, not a fixed label.
        assert "customext" in dialog.browser.toPlainText()


# ---------------------------------------------------------------------------
# ContentLossDialog itself.
# ---------------------------------------------------------------------------


def _make_dialog(qtbot, html_text="<p>hello</p>", default_key="b"):
    dialog = Dialog(
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

    assert not dialog.windowFlags() & MainWindow.Qt.WindowContextHelpButtonHint


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
