
import os
import shutil
import time

from PyQt5.QtWidgets import QMessageBox, QPlainTextEdit
from pytestqt.qt_compat import qt_api

from pymdwizard import __version__
from pymdwizard.gui import MainWindow


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
# Content-loss warning on save (Option A): detecting, previewing, and
# recording content the form cannot represent so it is not dropped silently.
# ---------------------------------------------------------------------------

from pymdwizard.core import xml_utils

MainForm = MainWindow.PyMdWizardMainForm


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
    long_value = [("metadata/distinfo/stdorder/ordering", ["x " * 80])]

    assert MainForm._preview_is_truncated(many_groups) is True
    assert MainForm._preview_is_truncated(many_values) is True
    assert MainForm._preview_is_truncated(long_value) is True


def test_format_dropped_preview_groups_and_caps():
    dropped = [
        (
            "metadata/idinfo/keywords/theme/themekey",
            ["alpha", "beta", "gamma", "delta", "epsilon"],
        ),
        ("metadata/customext/@units", ["meters"]),
    ]
    preview = MainForm._format_dropped_preview(dropped)

    # Leaves are grouped under their parent path.
    assert "metadata/idinfo/keywords/theme" in preview
    assert "themekey:  alpha" in preview
    # Per-group cap of 4 collapses the fifth value.
    assert "+1 more" in preview
    # Attribute is shown with its value.
    assert "@units:  meters" in preview


def test_confirm_content_loss_proceeds_silently_when_nothing_dropped(
    qtbot, tmp_path
):
    widget = MainForm()
    qtbot.addWidget(widget)

    tree = xml_utils.string_to_node(
        "<metadata><spdoinfo><direct>Vector</direct></spdoinfo></metadata>"
    )
    widget.loaded_record = tree

    # Produced tree is identical, so no dialog and no sidecar; save proceeds.
    fname = str(tmp_path / "record.xml")
    assert widget.confirm_content_loss(tree, fname) is True
    assert not os.path.exists(fname + ".dropped.txt")


def test_confirm_content_loss_warns_and_writes_backup(qtbot, mocker, tmp_path):
    widget = MainForm()
    qtbot.addWidget(widget)

    # Original has a custom element the form cannot represent; produced tree
    # drops it.
    widget.loaded_record = xml_utils.string_to_node(
        "<metadata>"
        "<spdoinfo><direct>Vector</direct></spdoinfo>"
        "<customext units='meters'>99</customext>"
        "</metadata>"
    )
    produced = xml_utils.string_to_node(
        "<metadata><spdoinfo><direct>Vector</direct></spdoinfo></metadata>"
    )

    fname = str(tmp_path / "record.xml")

    # Simulate the user clicking "Save and keep a copy of the original":
    # QMessageBox.exec_ returns, and clickedButton() yields the backup button.
    def fake_exec(self):
        # The backup button is the one whose text mentions keeping a copy.
        for button in self.buttons():
            if "copy of the original" in button.text():
                self._test_clicked = button
                return 0
        return 0

    mocker.patch.object(QMessageBox, "exec_", fake_exec)
    mocker.patch.object(
        QMessageBox,
        "clickedButton",
        lambda self: getattr(self, "_test_clicked", None),
    )

    proceed = widget.confirm_content_loss(produced, fname)

    assert proceed is True
    # The copy of the original was written next to the save target.
    backup = str(tmp_path / "record.original.xml")
    assert os.path.exists(backup)
    reloaded = xml_utils.fname_to_node(backup)
    assert reloaded.xpath("customext")[0].text == "99"
