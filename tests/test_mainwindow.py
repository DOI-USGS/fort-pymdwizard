
import os
import shutil
import time

from pytestqt.qt_compat import qt_api
from PyQt5.QtWidgets import QMessageBox, QPlainTextEdit

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
