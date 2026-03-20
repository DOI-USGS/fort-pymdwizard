#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import sys

# Non-standard python libraries.
try:
    import habanero
    from PyQt5.QtWidgets import (QMessageBox, QDialog, QPlainTextEdit)
    from PyQt5.QtCore import Qt

    # TODO: Remove this switch here and below.
    hananero_installed = True
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, doi_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_citeinfo
    from pymdwizard.gui.fgdc_date import FGDCDate
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.ui_files import UI_DOICiteinfoImporter
    from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
except ImportError as err:
    raise ImportError(err, __file__)


class Citeinfo(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "citation information"
        ("citeinfo") metadata element. Inherits from QgsWizardWidget.

    Passed arguments:
        parent (QWidget, optional): Parent widget. Defaults to None.
        include_lwork (bool, optional): If True, includes fields for a
            larger work citation. Defaults to True.

    Returned objects:
        None

    Workflow:
        Manages UI elements for citation (title, originator, links,
        date), handles specialized mouse events for title, supports
        DOI lookup, and performs XML conversion.

    Notes:
        The "mouse_move" method overrides standard behavior to simulate
        a QLineEdit for the QPlainTextEdit title field.
    """

    # Class attributes.
    drag_label = "Citation information <citeinfo>"
    acceptable_tags = ["citation", "citeinfo"]

    def __init__(self, parent=None, include_lwork=True):
        # Set instance attributes.
        self.origin_hint = 'Suggested format "First M. Last"'
        self.include_lwork = include_lwork
        self.schema = "bdp"

        # Initialize the base class.
        WizardWidget.__init__(self, parent=parent)
        self.doi_lookup = None

        # Initialize components for title widget.
        self.highlighter = Highlighter(self.ui.fgdc_title.document())
        self.ui.fgdc_title.textChanged.connect(self.remove_returns)
        self.ui.fgdc_title.setMaximumHeight(self.ui.fgdc_geoform.height())

        # Override mouse move event for single-line behavior.
        self.ui.fgdc_title.mouseMoveEvent = self.mouse_move

    def mouse_move(self, e):
        """
        Description:
            Override the mouse move event to ignore vertical scrolling,
            making QPlainTextEdit behave like a QLineEdit.

        Passed arguments:
            e (QEvent): The PyQt mouse event object.

        Returned objects:
            None

        Workflow:
            1. If the mouse is within the main text area, call the
               default handler.
            2. Force the vertical scroll bar to its minimum value.

        Notes:
            None
        """

        # Check if mouse is within the primary text area.
        if (
                e.y() < self.ui.fgdc_title.height() - 3
                and e.x() < self.ui.fgdc_title.width() - 3
        ):
            QPlainTextEdit.mouseMoveEvent(self.ui.fgdc_title, e)

        # Force scrollbar to the top (minimum value).
        self.ui.fgdc_title.verticalScrollBar().setValue(
            self.ui.fgdc_title.verticalScrollBar().minimum()
        )

    def remove_returns(self):
        """
        Description:
            Ensure the title field remains a single line by replacing
            any line returns ('\\n') with a space (' ').

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Temporarily disconnect the signal to prevent recursion.
            2. Get the current text and cursor position.
            3. Replace line returns and set the new text.
            4. Restore the cursor position and reconnect the signal.

        Notes:
            None
        """

        self.ui.fgdc_title.textChanged.disconnect()

        # Store cursor position to maintain user focus.
        old_position = self.ui.fgdc_title.textCursor().position()
        curtext = self.ui.fgdc_title.toPlainText()

        # Replace line returns with spaces.
        newtext = curtext.replace("\n", " ")
        self.ui.fgdc_title.setPlainText(newtext)

        # Restore cursor position.
        cursor = self.ui.fgdc_title.textCursor()
        cursor.setPosition(old_position)
        self.ui.fgdc_title.setTextCursor(cursor)

        # Reconnect the signal.
        self.ui.fgdc_title.textChanged.connect(self.remove_returns)

    def build_ui(self,):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the main UI, conditionally adds the Larger Work
            widget, sets up date and repeating link/originator widgets,
            and initializes drag-and-drop.

        Notes:
            None
        """

        # Instantiate the main UI elements.
        self.ui = UI_citeinfo.Ui_parent_form()
        self.ui.setupUi(self)

        # Conditionally include Larger Work Citation widget.
        if self.include_lwork:
            # Create a nested Citeinfo widget for larger work.
            self.lworkcit_widget = Citeinfo(parent=self, include_lwork=False)

            # Set a custom label for the nested widget's title field.
            self.lworkcit_widget.ui.lbl_dataset_title.setText(
                "Larger Work Title")

            # Add the widget to the layout.
            self.ui.lworkcite_widget.layout().addWidget(self.lworkcit_widget)

            # Set default geoform for larger work.
            self.lworkcit_widget.ui.fgdc_geoform.setEditText("publication")
        else:
            # Hide the larger work section if not included.
            self.ui.fgdc_lworkcit.hide()

        # Initial call to update visibility of larger work fields.
        self.include_lworkext_change(self.ui.radio_lworkyes.isChecked())

        # Hide extended sections initially.
        self.ui.series_ext.hide()
        self.ui.pub_ext.hide()

        # Initialize and add the publication date widget.
        self.ui.pubdate_widget = FGDCDate(
            label="YYYYMMDD  ",
            show_format=False,
            required=True,
            fgdc_name="fgdc_pubdate",
        )
        self.ui.pubdate_layout.addWidget(self.ui.pubdate_widget)

        # Initialize and add the RepeatingElement for Online Links.
        self.onlink_list = RepeatingElement(
            add_text="Add online link",
            remove_text="Remove last",
            italic_text="Is there a link to the data or the agency "
                        "that produced it? if so, provide the URL(s) ",
            widget_kwargs={"label": "Link", "line_name": "fgdc_onlink"},
        )
        self.onlink_list.add_another()
        self.ui.onlink_layout.addWidget(self.onlink_list)

        # Initialize and add the RepeatingElement for Originators.
        self.fgdc_origin = RepeatingElement(
            add_text="Add originator",
            remove_text="Remove last",
            italic_text="Who created the dataset? List the organization "
                        "and/or person(s)",
            widget_kwargs={
                "label": "Originator",
                "line_name": "fgdc_origin",
                "required": True,
                "placeholder_text": self.origin_hint,
                "spellings": False,
            },
        )
        self.ui.originator_layout.addWidget(self.fgdc_origin)
        self.fgdc_origin.add_another()

        # Setup drag-and-drop functionality for the main widget.
        self.setup_dragdrop(self)

        # Hide DOI button if the dependency is not installed.
        if not hananero_installed:
            self.ui.btn_import_doi.hide()

    def connect_events(self):
        """
        Description:
            Connect the appropriate GUI components with the corresponding
            functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects radio button toggles to visibility change functions
            and the DOI button to the import function.

        Notes:
            None
        """

        # Connect radio buttons to visibility handlers.
        self.ui.radio_lworkyes.toggled.connect(self.include_lworkext_change)
        self.ui.radio_seriesyes.toggled.connect(self.include_seriesext_change)
        self.ui.radio_pubinfoyes.toggled.connect(self.include_pubext_change)

        # Connect the DOI import button.
        self.ui.btn_import_doi.clicked.connect(self.get_doi_citation)

    def get_doi_citation(self):
        """
        Description:
            Initializes and displays the DOI lookup dialog.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Creates the dialog and its UI if it does not exist, connects
            OK/Cancel buttons, sets the icon, and shows the dialog.

        Notes:
            None
        """

        if self.doi_lookup is None:
            # Create the dialog instance.
            self.doi_lookup = QDialog(parent=self)

            # Load the dialog UI.
            self.doi_lookup_ui = UI_DOICiteinfoImporter.Ui_ImportUsgsUser()
            self.doi_lookup_ui.setupUi(self.doi_lookup)

            # Connect buttons to handlers.
            self.doi_lookup_ui.btn_OK.clicked.connect(self.add_doi)
            self.doi_lookup_ui.btn_cancel.clicked.connect(self.cancel)

            # Set application window icon.
            utils.set_window_icon(self.doi_lookup)

        # Show the dialog.
        self.doi_lookup.show()

    def add_doi(self):
        """
        Description:
            Attempts to retrieve citation metadata using a DOI, then
            parses the resulting XML into the widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Get DOI text.
            2. Attempt to fetch citation XML using "doi_utils".
            3. If successful, call "from_xml".
            4. If citation is not found, show a warning message.
            5. If an unexpected error occurs, show a problem warning.
            6. Close the lookup dialog via "cancel".

        Notes:
            None
        """

        # Fetch DOI value.
        doi = self.doi_lookup_ui.le_doi.text()

        try:
            # Fetch the citation object from the DOI.
            citeinfo = doi_utils.get_doi_citation(doi)

            if citeinfo is None:
                # DOI not found or invalid.
                msgbox = QMessageBox(self)
                utils.set_window_icon(msgbox)
                msgbox.setIcon(QMessageBox.Warning)
                msg = "'{}' Not Found on DataCite".format(doi)
                msg += "\nMake sure the DOI is valid and active."
                msgbox.setText(msg)
                msgbox.setInformativeText("No matching citation found")
                msgbox.setWindowTitle("DOI Not Found")
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.exec_()
            else:
                # Load the citation into the widget.
                self.from_xml(citeinfo.to_xml())
        except:
            # Catch unexpected network or parsing errors.
            msg = "We ran into a problem creating a citeinfo element "
            msg += "from that DOI({}).".format(doi)
            msg += "Check the DOI and/or manually create the citation "
            msg += "for it"
            QMessageBox.warning(self, "Problem DOI", msg)
        self.cancel()

    def cancel(self):
        """
        Description:
            Closes and deletes the DOI lookup dialog.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Schedules the dialog for deletion and resets the reference.

        Notes:
            None
        """

        # Delete the dialog.
        self.doi_lookup.deleteLater()

        # Reset the reference.
        self.doi_lookup = None

    def dragEnterEvent(self, e):
        """
        Description:
            Handles incoming drag events, accepting XML text that can be
            converted to a citation element or a DOI link/string.

        Passed arguments:
            e (QEvent): The drag event object.

        Returned objects:
            None

        Workflow:
            Checks for: 1) URL containing "doi", 2) plain text that is a
            valid DOI string, or 3) plain text that is valid XML for an
            acceptable tag.

        Notes:
            None
        """

        # Retrieve value.
        mime_data = e.mimeData()

        # Check for URL containing "doi".
        if e.mimeData().hasUrls():
            url = e.mimeData().urls()[0].url().lower()
            if "doi" in url:
                e.accept()

        # Check for plain text.
        elif e.mimeData().hasFormat("text/plain"):
            # Check if the text is a DOI string.
            if self.is_doi_str(mime_data.text()):
                e.accept()
            else:
                try:
                    # Check if the text is valid XML for citation.
                    element = xml_utils.string_to_node(
                        mime_data.text()
                    )
                    if (
                            element is not None
                            and element.tag in self.acceptable_tags
                    ):
                        e.accept()
                except AttributeError:
                    e.ignore()
        else:
            e.ignore()

    def is_doi_str(self, string):
        """
        Description:
            Checks if a given string is a valid DOI format string.

        Passed arguments:
            string (str): The string to check.

        Returned objects:
            bool: True if the string appears to be a DOI, False otherwise.

        Workflow:
            Checks for common DOI prefixes (http, https, doi:) and checks
            the cleaned string after processing by `doi_utils.clean_doi`.

        Notes:
            None
        """

        # Check for common URL prefixes.
        if string.startswith("https://doi.org"):
            return True
        if string.startswith("doi.org"):
            return True
        if string.startswith("https://dx.doi.org"):
            return True
        if string.startswith("doi:"):
            return True

        # Check cleaned DOI format.
        cleaned_doi = doi_utils.clean_doi(string).lower().strip()

        if cleaned_doi.startswith("doi:"):
            return True

        return False

    def dropEvent(self, e):
        """
        Description:
            Updates the form with the contents of an XML node or DOI
            dropped onto it.

        Passed arguments:
            e (QEvent): The drop event object.

        Returned objects:
            None

        Workflow:
            1. Accepts the drop action.
            2. If content is a DOI URL/string, look up citation via DOI
               and parse XML.
            3. Otherwise, parse the content as XML directly.
            4. Handles lookup/parsing exceptions with a warning message.

        Notes:
            Uses a bare "except" to catch generic errors during XML/DOI
            processing.
        """

        try:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            mime_data = e.mimeData()

            # Check for DOI drop (URL or plain text).
            if mime_data.hasUrls() or self.is_doi_str(mime_data.text()):
                if self.is_doi_str(mime_data.text()):
                    doi = mime_data.text()
                else:
                    doi = e.mimeData().urls()[0].url()
                try:
                    # Get citation object from DOI and convert to XML.
                    citeinfo = doi_utils.get_doi_citation(doi)
                    self.from_xml(citeinfo.to_xml())
                except:
                    # Catch errors during DOI lookup or XML conversion.
                    msg = "We ran into a problem creating a citeinfo "
                    msg += "element from that DOI({})".format(doi)
                    msg += "Check the DOI and/or manually create the "
                    msg += "citation for it"
                    QMessageBox.warning(self, "Problem DOI", msg)
            else:
                # Handle XML text drop.
                element = xml_utils.string_to_node(mime_data.text())
                self.from_xml(element)
        except:
            # Catch unexpected errors during drop handling.
            exc_type = sys.exc_info()[0]
            print("problem drop", exc_type)

    def include_seriesext_change(self, b):
        """
        Description:
            Toggle visibility of extended citation fields supporting
            series information.

        Passed arguments:
            b (bool): True to show the fields, False to hide them.

        Returned objects:
            None

        Workflow:
            Shows or hides the "series_ext" container based on "b".

        Notes:
            None
        """

        if b:
            self.ui.series_ext.show()
        else:
            self.ui.series_ext.hide()

    def include_pubext_change(self, b):
        """
        Description:
            Toggle visibility of extended citation fields supporting
            publication information.

        Passed arguments:
            b (bool): True to show the fields, False to hide them.

        Returned objects:
            None

        Workflow:
            Shows or hides the "pub_ext" container based on "b".

        Notes:
            None
                """

        if b:
            self.ui.pub_ext.show()
        else:
            self.ui.pub_ext.hide()

    def include_lworkext_change(self, b):
        """
        Description:
            Toggle visibility of the larger work citation widget.

        Passed arguments:
            b (bool): True to show the widget, False to hide it.

        Returned objects:
            None

        Workflow:
            Shows or hides the "lworkcite_widget" container based on "b".

        Notes:
            Only runs if the widget was initially included ("include_lwork").
        """

        if b:
            self.ui.lworkcite_widget.show()
        else:
            self.ui.lworkcite_widget.hide()

    def clear_widget(self):
        """
        Description:
            Clears the content of the widget and resets radio buttons
            controlling extended sections.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the base class clear method and sets the radio buttons
            to hide optional sections.

        Notes:
            None
        """

        # Call base class clear method.
        WizardWidget.clear_widget(self)

        # Reset radio buttons to hide optional sections.
        self.ui.radio_pubinfono.setChecked(True)
        self.ui.radio_seriesno.setChecked(True)

    def to_xml(self):
        """
        Description:
            Encapsulates the widget's content into an XML "citeinfo"
            element tag.

        Passed arguments:
            None

        Returned objects:
            citeinfo (xml.etree.ElementTree.Element): Citation
                information element tag in XML tree.

        Workflow:
            Creates the "citeinfo" node, then iterates through repeating
            elements (originator, onlink) and conditional sections
            (series, publication info, larger work) to construct the XML.

        Notes:
            None
        """

        # Create the parent "citeinfo" XML node.
        citeinfo = xml_utils.xml_node("citeinfo")

        # Add Originator nodes
        for origin in self.fgdc_origin.get_widgets():
            xml_utils.xml_node(
                "origin", text=origin.text(), parent_node=citeinfo
            )

        # Add Publication Date and Title nodes.
        pubdate = xml_utils.xml_node(
            "pubdate",
            text=self.ui.pubdate_widget.get_date(),
            parent_node=citeinfo,
        )
        title = xml_utils.xml_node(
            "title", self.ui.fgdc_title.toPlainText(), parent_node=citeinfo
        )

        # Add Edition node if text exists.
        if self.ui.fgdc_edition.text():
            xml_utils.xml_node(
                "edition",
                self.ui.fgdc_edition.text(),
                parent_node=citeinfo,
            )

        # Add Geoform node.
        xml_utils.xml_node(
            "geoform",
            self.ui.fgdc_geoform.currentText(),
            parent_node=citeinfo,
        )

        # Add Series Information (serinfo) if selected.
        if self.ui.radio_seriesyes.isChecked():
            serinfo = xml_utils.xml_node("serinfo", parent_node=citeinfo)
            xml_utils.xml_node(
                "sername",
                text=self.ui.fgdc_sername.text(),
                parent_node=serinfo,
            )
            xml_utils.xml_node(
                "issue",
                text=self.ui.fgdc_issue.text(),
                parent_node=serinfo,
            )

        # Add Publication Information (pubinfo) if selected and not empty.
        has_pub_info = (
                self.ui.fgdc_pubplace.text() != ""
                or self.ui.fgdc_publish.text() != ""
        )
        if self.ui.radio_pubinfoyes.isChecked() and has_pub_info:
            pubinfo = xml_utils.xml_node("pubinfo", parent_node=citeinfo)
            xml_utils.xml_node(
                "pubplace",
                parent_node=pubinfo,
                text=self.ui.fgdc_pubplace.text(),
            )
            xml_utils.xml_node(
                "publish",
                parent_node=pubinfo,
                text=self.ui.fgdc_publish.text(),
            )

        # Add Other Citation Information if text exists.
        if self.ui.fgdc_othercit.toPlainText():
            xml_utils.xml_node(
                "othercit",
                self.ui.fgdc_othercit.toPlainText(),
                parent_node=citeinfo,
            )

        # Add Online Link (onlink) nodes.
        for onlink in self.onlink_list.get_widgets():
            if onlink.text() != "":
                xml_utils.xml_node(
                    "onlink",
                    parent_node=citeinfo,
                    text=onlink.text(),
                )

        # Add Larger Work Citation (lworkcit) if included and selected.
        if self.include_lwork and self.ui.radio_lworkyes.isChecked():
            lworkcit = xml_utils.xml_node("lworkcit", parent_node=citeinfo)
            lwork = self.lworkcit_widget.to_xml()
            lworkcit.append(lwork)

        return citeinfo

    def from_xml(self, citeinfo):
        """
        Description:
            Parse the XML code into the relevant citation elements.

        Passed arguments:
            citeinfo (xml.etree.ElementTree.Element): The XML element
                containing citation ("citation" or "citeinfo") details.

        Returned objects:
            None

        Workflow:
            1. Extracts the "citeinfo" node if wrapped in "citation".
            2. Clears existing content.
            3. Populates repeating fields (originator, onlink) and
               conditional sections (series, pubinfo, lworkcit) from the
               XML nodes using helper functions.

        Notes:
            Handles nested "lworkcit" and gracefully skips if the XML
            structure is unexpected.
        """

        self.original_xml = citeinfo
        self.clear_widget()

        try:
            # Unwrap "citeinfo" if it is wrapped in "citation".
            if citeinfo.tag == "citation":
                citeinfo = citeinfo.xpath("citeinfo")[0]
            elif citeinfo.tag != "citeinfo":
                print("The tag is not 'citation' or 'citeinfo'")
                return

            # Clear widgets
            self.fgdc_origin.clear_widgets(add_another=False)

            # Originators.
            originators = citeinfo.findall("origin")
            if originators:
                for origin in originators:
                    origin_widget = self.fgdc_origin.add_another()
                    origin_widget.setText(origin.text)
            else:
                self.fgdc_origin.add_another()

            # Geoform.
            if citeinfo.findall("geoform"):
                self.ui.fgdc_geoform.setEditText(
                    citeinfo.findall("geoform")[0].text
                )

            # Fields (Date, Title, Edition, Othercit).
            utils.populate_widget_element(
                self.ui.pubdate_widget.ui.fgdc_caldate,
                citeinfo,
                "pubdate",
            )
            utils.populate_widget_element(self.ui.fgdc_title, citeinfo,
                                          "title")
            utils.populate_widget_element(
                self.ui.fgdc_edition, citeinfo, "edition"
            )
            utils.populate_widget_element(
                self.ui.fgdc_othercit, citeinfo, "othercit"
            )

            # Online Links (Onlink).
            self.onlink_list.clear_widgets()
            if citeinfo.findall("onlink"):
                self.onlink_list.clear_widgets(add_another=False)
                for onlink in citeinfo.findall("onlink"):
                    self.onlink_list.add_another()
                    onlink_widget = self.onlink_list.widgets[-1]
                    onlink_widget.setText(onlink.text)

            # Series Information (serinfo).
            if citeinfo.xpath("serinfo"):
                self.ui.radio_seriesyes.setChecked(True)
                utils.populate_widget(self, citeinfo.xpath("serinfo")[0])
            else:
                self.ui.radio_seriesno.setChecked(True)

            # Publication Information (pubinfo).
            pubinfo = citeinfo.xpath("pubinfo")
            if pubinfo:
                self.ui.radio_pubinfoyes.setChecked(True)
                utils.populate_widget_element(
                    self.ui.fgdc_publish, pubinfo[0], "publish"
                )
                utils.populate_widget_element(
                    self.ui.fgdc_pubplace, pubinfo[0], "pubplace"
                )
            else:
                # self.ui.radio_pubinfono.setChecked(True)
                self.ui.radio_pubinfoyes.setChecked(True)
                self.ui.radio_pubinfono.setChecked(False)

            # Larger Work Citation (lworkcit).
            if citeinfo.xpath("lworkcit"):
                try:
                    self.ui.radio_lworkyes.setChecked(True)
                    self.lworkcit_widget.from_xml(
                        citeinfo.xpath("lworkcit/citeinfo")[0]
                    )
                except AttributeError:
                    # Catch error if nested lworkcit is found.
                    msg = "You pasted a citation element into the larger "
                    msg += "work citation area that contained a larger "
                    msg += "work citation. Multiple nested larger work "
                    msg += "citations are not currently supported in the "
                    msg += "tool. The larger work citation being pasted "
                    msg += "will be ignored."
                    QMessageBox.warning(
                        self, "Dropped Content Warning", msg
                    )
            else:
                self.ui.radio_lworkno.setChecked(True)

        except KeyError:
            # Handle if the element is not found/accessible.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Citeinfo, "Citation testing")
