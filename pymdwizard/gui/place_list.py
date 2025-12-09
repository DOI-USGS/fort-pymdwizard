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

# Non-standard python libraries.
try:
    from PyQt5.QtCore import QPoint
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_place_list
    from pymdwizard.gui import ThesaurusSearch
    from pymdwizard.gui.theme import Theme
except ImportError as err:
    raise ImportError(err, __file__)


class PlaceList(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC Place Keywords structure.
        It manages a list of thesauri tabs, each containing a set of
        place keywords.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Manages a dynamic set of tabs, where each tab holds a
           <place> element (thesaurus and keywords).
        2. Handles adding/removing thesaurus tabs.
        3. Integrates with a Thesaurus Search tool.
        4. Serializes/deserializes the keywords to/from XML.

    Notes:
        Inherits from "WizardWidget". Uses special stylesheet to hide
        disabled tabs.
    """

    # Class attributes.
    drag_label = "Place Keywords <keywords>"
    acceptable_tags = ["keywords", "place"]

    def __init__(self, parent=None):
        # Initialize base class.
        super(self.__class__, self).__init__(parent=parent)
        self.thesauri = []
        self.original_xml = None

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, sets up drag-and-drop, applies a
            stylesheet to hide disabled tabs, and sets the initial
            state.

        Notes:
            None
        """

        self.ui = UI_place_list.Ui_place_keywords()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        # Apply stylesheet to hide disabled tabs (e.g., when adding/
        # removing tabs without changing the displayed content).
        self.ui.theme_tabs.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; "
            "margin: 0; padding: 0; border: none;} "
        )

        # Set initial state (content hidden, no keywords present).
        self.contact_include_place_change(False)

    def connect_events(self):
        """
        Description:
            Connects GUI component signals to the corresponding handler
            functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects buttons for adding/removing/searching keywords, and
            the radio button for showing/hiding the section.

        Notes:
            None
        """

        self.ui.btn_add_thesaurus.clicked.connect(self.add_another)
        self.ui.btn_remove_selected.clicked.connect(self.remove_selected)
        self.ui.btn_search_controlled.clicked.connect(self.search_controlled)

        # Connect "Yes/No" radio button to handler.
        self.ui.rbtn_yes.toggled.connect(self.contact_include_place_change)

    def contact_include_place_change(self, b):
        """
        Description:
            Shows or hides the keyword entry section based on the "Yes/No"
            radio button selection. Adds a default empty keyword tab if
            "Yes" is checked and no tabs exist.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Shows/hides "place_contents". If showing, ensures at least
            one thesaurus tab exists with a default None thesaurus.

        Notes:
            None
        """

        if b:
            # Show the keyword contents area.
            self.ui.place_contents.show()

            if not self.thesauri:
                # Add a default None thesaurus if none exist.
                theme_widget = self.add_keyword(
                    keyword="", thesaurus="None", locked=False
                )
        else:
            # Hide the keyword contents area.
            self.ui.place_contents.hide()

    def add_another(self, click=False, tab_label="", locked=False):
        """
        Description:
            Adds a new, empty thesaurus tab to the widget.

        Passed arguments:
            click (bool, optional): Ignored; used for connection compatibility.
            tab_label (str, optional): The initial label for the tab.
            locked (bool, optional): If True, the thesaurus name field
                in the new tab will be locked.

        Returned objects:
            theme_widget (Theme): The newly created Theme widget (tab).

        Workflow:
            Creates a new "Theme" widget, connects its name change event,
            adds it as a tab, makes it current, and adds it to
            self.thesauri. If a None thesaurus exists and "tab_label"
            is empty, no new tab is created.

        Notes:
            A new tab is generally added unless there is an existing
            "None" tab and no specific label is provided.
        """

        has_none_thesaurus = "None" in [
            t.ui.fgdc_themekt.text() for t in self.thesauri
        ]

        if has_none_thesaurus and tab_label == "":
            # If 'None' exists, don't create a second one via button click.
            return self.thesauri[0]
        else:
            # Create a new Theme widget for keywords.
            theme_widget = Theme(which="place")
            theme_widget.ui.fgdc_themekt.textChanged.connect(
                self.changed_thesaurus
            )

            # Add as a tab and make it the current tab.
            self.ui.theme_tabs.addTab(theme_widget, tab_label)
            self.ui.theme_tabs.setCurrentIndex(
                self.ui.theme_tabs.count() - 1
            )

            # Keep track of the thesaurus widget.
            self.thesauri.append(theme_widget)
            return theme_widget

    def changed_thesaurus(self, thesaurus_name):
        """
        Description:
            Updates the label of the current tab to reflect the contents
            of its thesaurus name field.

        Passed arguments:
            thesaurus_name (str): The new text content of the thesaurus
                name field.

        Returned objects:
            None

        Workflow:
            Gets the current tab index and updates the tab's text label.

        Notes:
            None
        """

        cur_index = self.ui.theme_tabs.currentIndex()
        self.ui.theme_tabs.setTabText(cur_index, "Thesaurus: " + thesaurus_name)

    def remove_selected(self):
        """
        Description:
            Removes the currently selected thesaurus tab.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the current index and calls "remove_tab".

        Notes:
            None
        """

        current_index = self.ui.theme_tabs.currentIndex()
        if current_index >= 0:
            self.remove_tab(current_index)

    def remove_tab(self, index):
        """
        Description:
            Removes a thesaurus tab at a given index.

        Passed arguments:
            index (int): The index of the tab to remove.

        Returned objects:
            None

        Workflow:
            Removes the tab from the QTabWidget and deletes the
            corresponding widget from self.thesauri.

        Notes:
            None
        """

        self.ui.theme_tabs.removeTab(index)
        del self.thesauri[index]

    def get_children(self, widget):
        """
        Description:
            Returns the list of child thesaurus widgets if the section
            is enabled.

        Passed arguments:
            widget: Ignored.

        Returned objects:
            children (list): List of Theme widgets (thesauri).

        Workflow:
            Checks "rbtn_yes". If checked, returns self.thesauri.

        Notes:
            Part of the parent widget's structure traversal.
        """

        children = []

        if self.ui.rbtn_yes.isChecked():
            for place in self.thesauri:
                children.append(place)

        return children

    def clear_widget(self):
        """
        Description:
            Clears all thesaurus tabs and their contents.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Iterates backward through the thesauri list, removing each
            tab and clearing the list.

        Notes:
            None
        """

        # Iterate backwards to safely remove tabs.
        for i in range(len(self.thesauri) - 1, -1, -1):
            self.remove_tab(i)
        self.thesauri = []

    def search_controlled(self):
        """
        Description:
            Opens the Thesaurus Search window to allow selection of
            controlled keywords.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Creates an instance of "ThesaurusSearch".
            2. Configures it to add keywords via self.add_keyword.
            3. Positions and shows the search window.

        Notes:
            The search is specifically for place keywords.
        """

        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(
            add_term_function=self.add_keyword, place=True, parent=self
        )

        self.thesaurus_search.setWindowTitle("Place Keyword Thesaurus Search")

        # Move the search window relative to this widget.
        fg = self.frameGeometry()
        self.thesaurus_search.move(fg.topRight() - QPoint(150, -25))

        self.thesaurus_search.show()

    def add_keyword(self, keyword=None, thesaurus=None, locked=True):
        """
        Description:
            Adds a single keyword to an existing thesaurus tab, or
            creates a new thesaurus tab if the thesaurus does not exist.

        Passed arguments:
            keyword (str, optional): The keyword term to add.
            thesaurus (str, optional): The thesaurus name (e.g., "GNS").
            locked (bool, optional): If True, the thesaurus name is
                locked from editing.

        Returned objects:
            theme_widget (Theme): The widget where the keyword was added.

        Workflow:
            1. Searches for an existing tab with the matching thesaurus.
            2. If none found, calls "add_another" to create a new tab.
            3. Adds the keyword to the found/new tab using
               theme_widget.add_keyword().

        Notes:
            None
        """

        # Search for an existing thesaurus tab.
        theme_widget = None
        for theme in self.thesauri:
            if theme.ui.fgdc_themekt.text() == thesaurus:
                theme_widget = theme

        if theme_widget is None:
            # Thesaurus not found, create a new tab.
            shortname = thesaurus.split(" ")[0]
            theme_widget = self.add_another(tab_label=shortname, locked=locked)

            # Set the new tab's thesaurus name and lock it.
            theme_widget.ui.fgdc_themekt.setText(thesaurus)
            if locked:
                theme_widget.lock()
            self.changed_thesaurus(shortname)

        # Add the actual keyword to the determined tab.
        theme_widget.add_keyword(keyword)

        return theme_widget

    def to_xml(self):
        """
        Description:
            Converts the widget's contents into an FGDC <keywords>
            XML element containing nested <place> elements.

        Passed arguments:
            None

        Returned objects:
            keywords (lxml.etree._Element): The <keywords> element.

        Workflow:
            Iterates through all self.thesauri. If the section is enabled
            and the thesaurus is not the default empty one, it appends
            the thesaurus's XML (<place>) to the main <keywords> node.

        Notes:
            Excludes empty default thesauri (Thesaurus="None" and only
            one empty keyword).
        """

        keywords = xml_utils.xml_node("keywords")

        if self.ui.rbtn_yes.isChecked():
            for place in self.thesauri:
                place_xml = place.to_xml()
                place_node = xml_utils.XMLNode(place_xml)

                # Check for the default empty thesaurus case.
                place_keys = place_node.xpath("placekey", as_list=True)
                is_empty_default = (
                        place_node.placekt.text == "None"
                        and len(place_keys) <= 1
                        and place_keys[0].text == ""
                        and len(self.thesauri) > 1
                )

                if not is_empty_default:
                    # Append the <place> XML to <keywords>.
                    keywords.append(place_xml)

        return keywords

    def from_xml(self, keywords_xml):
        """
        Description:
            Parses an FGDC <keywords> element and populates the
            widget with place thesauri and keywords.

        Passed arguments:
            keywords_xml (lxml.etree._Element): The XML node to load.

        Returned objects:
            None

        Workflow:
            1. Clears existing content.
            2. Extracts all <place> elements.
            3. For each <place>, creates a new tab and loads its content.
            4. Sets the "Yes" radio button if any place keywords are found.

        Notes:
            None
        """

        self.clear_widget()

        self.original_xml = keywords_xml
        if keywords_xml.tag == "keywords":
            # Extract all <place> elements.
            place_kws = keywords_xml.xpath("place")

            for place_xml in place_kws:
                # Add a new tab for each <place>.
                place = self.add_another(tab_label="x")
                place.from_xml(place_xml)

            if place_kws:
                # Set the radio button to "Yes" if keywords were loaded.
                self.ui.rbtn_yes.setChecked(True)
            else:
                # Set the radio button to "No" if no keywords were found.
                self.ui.rbtn_no.setChecked(True)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(PlaceList, "ThemeList Step testing")
