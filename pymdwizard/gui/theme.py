#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


NOTES
------------------------------------------------------------------------------
Theme keyword lists whose thesaurus is "USGS Thesaurus" show a hint and a
"Search USGS Thesaurus" button, and check each typed keyword against the
USGS Thesaurus web service when the keyword field loses focus.
"""

# Non-standard python libraries.
try:
    from PyQt5.QtCore import QThread, pyqtSignal
    from PyQt5.QtWidgets import QApplication, QPushButton
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, thesaurus_utils)
    from pymdwizard.gui.keywords_repeater import KeywordsRepeater
except ImportError as err:
    raise ImportError(err, __file__)

# Thesaurus name (<themekt>) that gets the hint, search button, and term
# check.
USGS_THESAURUS = thesaurus_utils.USGS_THESAURUS_NAME
USGS_HINT = "Keywords must be terms from the USGS Thesaurus."

# Highlight for a keyword the USGS Thesaurus does not recognize. Same colors
# as the regular (non-selected) FGDC validation highlight in MainWindow.
UNKNOWN_TERM_STYLE = (
    "QPlainTextEdit#{name} {{"
    " background-color: rgb(254, 226, 226);"
    " border: 2px solid rgb(248, 113, 113); }}"
)
UNKNOWN_TERM_TOOLTIP = (
    "<b>Not a USGS Thesaurus term</b><br/>"
    '"{term}" is not a term in the USGS Thesaurus. Use '
    '"Search USGS Thesaurus" to find the preferred term.'
)

# Thesaurus name -> thcode mapping, fetched once on first use.
_thesauri_lookup = None

# Running term-check threads. Holding a reference here, rather than
# parenting the thread to a widget, keeps a thread alive if its keyword
# tab is removed before the lookup returns.
_active_checks = set()


def qwidget_is_valid(widget):
    """
    Return True if 'widget' is a live Qt object we can safely touch.
    PyQt raises RuntimeError if the wrapped C/C++ object has been deleted.
    """
    if widget is None:
        return False
    try:
        _ = widget.objectName()
        return True
    except RuntimeError:
        return False


class TermCheckThread(QThread):
    """
    Description:
        Checks one keyword against a named thesaurus in the background,
        so the web service lookup does not freeze the form.

    Passed arguments:
        thesaurus (str): The thesaurus name (<themekt>).
        term (str): The keyword to check.

    Returned objects:
        checked (pyqtSignal(str, object)): Emitted with the checked term
            and the result of thesaurus_utils.find_invalid_keywords:
            [] if the term is known, [term] if not, or None if the check
            could not be completed.

    Workflow:
        Fetches the thesaurus lookup if not yet cached, then checks the
        term.

    Notes:
        Inherits from "QThread".
    """

    checked = pyqtSignal(str, object)

    def __init__(self, thesaurus, term):
        super(TermCheckThread, self).__init__()
        self.thesaurus = thesaurus
        self.term = term

    def run(self):
        global _thesauri_lookup

        if _thesauri_lookup is None:
            _thesauri_lookup = thesaurus_utils.get_thesauri_lookup()

        if _thesauri_lookup is None:
            result = None
        else:
            result = thesaurus_utils.find_invalid_keywords(
                self.thesaurus, [self.term], lookup=_thesauri_lookup
            )

        self.checked.emit(self.term, result)


class Theme(KeywordsRepeater):  #
    """
    Description:
        A widget derived from "KeywordsRepeater" used to manage a
        set of FGDC keyword elements, specifically for Theme, Place,
        Stratum, or Temporal keywords. It handles the thesaurus name
        (e.g., <themekt>) and individual keywords (e.g., <themkey>).

    Passed arguments:
        which (str): Specifies the type of keyword ("theme", "place",
                     "stratum", "temporal"). Defaults to "theme".
        parent (QWidget): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes the base "KeywordsRepeater" with dynamic
           names based on the "which" parameter.
        2. Provides methods to add keywords and manage the thesaurus
           text field.
        3. Handles serialization to and deserialization from XML for
           the keyword set.

    Notes:
        Inherits from "KeywordsRepeater". Dynamically renames itself
        and its child widgets based on the "which" argument.
    """

    # Class attributes.
    drag_label = "Theme Keywords <theme>"
    acceptable_tags = ["theme"]

    def __init__(self, which="theme", parent=None):
        """
        Description:
            Initializes the keyword widget, setting dynamic names for
            tags and object properties.

        Passed arguments:
            which (str): Specifies the keyword type ("theme", "place",
                         etc.).
            parent (object): Parent widget.

        Returned objects:
            None

        Workflow:
            Sets dynamic tags, initializes the base class, and handles
            special case logic for "place" keywords.

        Notes:
            None
        """

        self.acceptable_tags = [which]
        self.which = which

        # Initialize parent KeywordsRepeater class.
        KeywordsRepeater.__init__(
            self,
            keywords_label="Keyword   ",
            parent=parent,
            line_name="fgdc_{}key".format(self.which),
        )

        # Reference to the thesaurus text field.
        self.kt = self.ui.fgdc_themekt

        # --- Handle specific keyword types (e.g., Place) ---
        if which == "place":
            self.setObjectName("fgdc_place")
            self.drag_label = "Place Keywords <place>"
            self.ui.fgdc_themekt.setObjectName("fgdc_placekt")
            self.acceptable_tags = ["place"]
        else:
            self.setObjectName("fgdc_theme")

    def build_ui(self):
        """
        Description:
            Builds the base keyword list UI and, for theme keywords, adds
            a hidden "Search USGS Thesaurus" button next to "Add keyword".

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls KeywordsRepeater.build_ui, then inserts the button into
            the keyword list's button row.

        Notes:
            The button is shown only while the thesaurus is
            "USGS Thesaurus" (see update_usgs_guidance). The parent
            ThemeList connects its click to the search dialog.
        """

        KeywordsRepeater.build_ui(self)

        self.btn_search_usgs = None
        if self.which == "theme":
            button_row = self.keywords.ui.horizontalLayout
            self.btn_search_usgs = QPushButton(
                "Search USGS Thesaurus", self.keywords.ui.button_widget
            )
            self.btn_search_usgs.setObjectName("btn_search_usgs")
            button_row.insertWidget(
                button_row.indexOf(self.keywords.ui.addAnother),
                self.btn_search_usgs,
            )
            self.btn_search_usgs.hide()

    def connect_events(self):
        """
        Description:
            For theme keywords, updates the USGS Thesaurus hint when the
            thesaurus name changes, and checks keywords when they lose
            focus.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the thesaurus field's textChanged signal and the
            application's focusChanged signal.

        Notes:
            QPlainTextEdit has no editingFinished signal, so
            focusChanged is used to detect when a keyword field is left.
        """

        if self.which != "theme":
            return

        self.ui.fgdc_themekt.textChanged.connect(self.update_usgs_guidance)
        QApplication.instance().focusChanged.connect(self.focus_changed)

    def is_usgs_thesaurus(self):
        """
        Description:
            Returns True if this is a theme keyword list for the USGS
            Thesaurus.

        Passed arguments:
            None

        Returned objects:
            bool
        """

        return (
            self.which == "theme"
            and self.ui.fgdc_themekt.text().strip() == USGS_THESAURUS
        )

    def update_usgs_guidance(self, text=None):
        """
        Description:
            Shows the USGS Thesaurus hint and search button while the
            thesaurus is "USGS Thesaurus", and hides them otherwise.

        Passed arguments:
            text (str): Not used; passed by the textChanged signal.

        Returned objects:
            None

        Workflow:
            Sets the italic label in the keyword button row and toggles
            the search button. When the thesaurus changes away from
            USGS Thesaurus, removes any unknown-term highlights.

        Notes:
            None
        """

        is_usgs = self.is_usgs_thesaurus()

        label = self.keywords.ui.italic_label
        if is_usgs:
            label.setText(USGS_HINT)
            label.setStyleSheet("font: italic;")
        else:
            label.setText("")
            label.setStyleSheet("")
            for kw in self.keywords.get_widgets():
                self.clear_unknown_term(kw)

        if self.btn_search_usgs is not None:
            self.btn_search_usgs.setVisible(is_usgs)

    def focus_changed(self, old, new):
        """
        Description:
            Checks a keyword against the USGS Thesaurus when the user
            leaves its field.

        Passed arguments:
            old (QWidget): The widget that lost focus.
            new (QWidget): The widget that gained focus (not used).

        Returned objects:
            None
        """

        if old is None or not self.is_usgs_thesaurus():
            return

        for kw in self.keywords.get_widgets():
            if kw.added_line is old:
                self.check_keyword(kw)
                break

    def check_keyword(self, kw):
        """
        Description:
            Starts a background check of one keyword against the USGS
            Thesaurus.

        Passed arguments:
            kw (DefaultWidget): The keyword row to check.

        Returned objects:
            None

        Workflow:
            Empty keywords are cleared without a lookup. Read-only
            keywords came from the search dialog and are not checked.
            Otherwise a TermCheckThread is started, and its result is
            applied only if the keyword text has not changed since.

        Notes:
            If the service cannot be reached, nothing is highlighted.
        """

        term = kw.text().strip()
        if not term:
            self.clear_unknown_term(kw)
            return

        if kw.added_line.isReadOnly():
            return

        thread = TermCheckThread(USGS_THESAURUS, term)

        def apply_result(checked_term, result):
            if not qwidget_is_valid(kw) or not self.is_usgs_thesaurus():
                return
            if kw.text().strip() != checked_term or result is None:
                return
            if result:
                self.flag_unknown_term(kw, checked_term)
            else:
                self.clear_unknown_term(kw)

        thread.checked.connect(apply_result)
        thread.finished.connect(lambda: _active_checks.discard(thread))
        _active_checks.add(thread)
        thread.start()

    def flag_unknown_term(self, kw, term):
        """
        Description:
            Highlights a keyword field the USGS Thesaurus does not
            recognize and explains why in its tooltip.

        Passed arguments:
            kw (DefaultWidget): The keyword row.
            term (str): The unrecognized keyword.

        Returned objects:
            None
        """

        line = kw.added_line
        if not getattr(kw, "unknown_term_flagged", False):
            kw.tooltip_before_flag = line.toolTip()
        kw.unknown_term_flagged = True
        line.setStyleSheet(UNKNOWN_TERM_STYLE.format(name=line.objectName()))
        line.setToolTip(UNKNOWN_TERM_TOOLTIP.format(term=term))

    def clear_unknown_term(self, kw):
        """
        Description:
            Removes the unknown-term highlight from a keyword field, if
            this widget set one.

        Passed arguments:
            kw (DefaultWidget): The keyword row.

        Returned objects:
            None

        Notes:
            Fields this widget did not flag are left alone, so an FGDC
            validation highlight on the same field is not removed.
        """

        if not getattr(kw, "unknown_term_flagged", False):
            return

        kw.added_line.setStyleSheet("")
        kw.added_line.setToolTip(getattr(kw, "tooltip_before_flag", ""))
        kw.unknown_term_flagged = False

    def add_keyword(self, keyword, locked=False):
        """
        Description:
            Adds a given keyword to the current list, ensuring duplicates
            are not added (unless the list is empty).

        Passed arguments:
            keyword (str): String to add to the list.
            locked (bool): If True, the added keyword field is read-only.

        Returned objects:
            None

        Workflow:
            Checks for existence and adds the keyword via the
            keywords.add_another() method, setting the locked state.

        Notes:
            None
        """

        existing_kws = self.get_keywords()

        # If the first widget is empty, use it.
        if existing_kws[0] == "":
            kw = self.keywords.get_widgets()[0]
            kw.setText(keyword)
            kw.added_line.setReadOnly(locked)

        # Otherwise, add a new widget if the keyword is not a duplicate.
        elif keyword not in existing_kws:
            kw = self.keywords.add_another()
            kw.setText(keyword)
            kw.added_line.setReadOnly(locked)

    def get_thesaurus_name(self):
        """
        Description:
            Returns the current thesaurus name for this widget.

        Passed arguments:
            None

        Returned objects:
            str: The text content of the thesaurus field.

        Workflow:
            Returns self.kt.text().

        Notes:
            None
        """

        return self.kt.text()

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC keyword element
            (e.g., `<theme>`), including the thesaurus and all keywords.

        Passed arguments:
            None

        Returned objects:
            keywtax (lxml.etree._Element): The keyword element tag in
                the XML tree.

        Workflow:
            1. Creates the root keyword node (e.g., <theme>).
            2. Appends the thesaurus name node (e.g., <themekt>).
            3. Appends all individual keyword nodes (e.g., <themkey>).

        Notes:
            None
        """

        # Create the root keyword node (e.g., <theme>).
        keywtax = xml_utils.xml_node(self.which)

        # Create and append the thesaurus node (e.g., <themekt>).
        xml_utils.xml_node(
            "{}kt".format(self.which),
            text=self.ui.fgdc_themekt.text(),
            parent_node=keywtax,
        )

        # Create and append individual keyword nodes (e.g., <themkey>).
        for keyword in self.get_keywords():
            xml_utils.xml_node(
                "{}key".format(self.which), text=keyword, parent_node=keywtax
            )

        return keywtax

    def from_xml(self, keywtax):
        """
        Description:
            Parses an FGDC keyword XML element (e.g., <theme>) and
            populates the thesaurus and individual keyword fields.

        Passed arguments:
            keywtax (lxml.etree._Element): The keyword XML element
                and its contents.

        Returned objects:
            None

        Workflow:
            1. Checks for the correct tag.
            2. Populates the thesaurus text field.
            3. Iterates through keyword nodes, adding them to the
               "KeywordsRepeater".

        Notes:
            None
        """

        try:
            if keywtax.tag == self.which:
                # Populate the thesaurus field (e.g., <themekt>).
                thesaurus = keywtax.xpath("{}kt".format(self.which))
                if thesaurus:
                    self.ui.fgdc_themekt.setText(thesaurus[0].text)

                # Populate the individual keywords (e.g., <themkey>)
                keywords = keywtax.xpath("{}key".format(self.which))

                # Use a flag to check if the first widget has been used.
                first_kw = True
                for kw in keywords:
                    if first_kw:
                        # Use the default first widget.
                        kw_widget = self.keywords.get_widgets()[0]
                        first_kw = False
                    else:
                        # Add a new widget for subsequent keywords.
                        kw_widget = self.keywords.add_another()

                    kw_widget.setText(kw.text)
            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not theme")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Theme, " testing", which="place")
