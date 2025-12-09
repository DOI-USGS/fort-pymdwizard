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

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_theme_list
    from pymdwizard.gui import ThesaurusSearch
    from pymdwizard.gui.theme import Theme
    from pymdwizard.gui.iso_keyword import IsoKeyword
    from pymdwizard.gui.repeating_element import RepeatingElement
except ImportError as err:
    raise ImportError(err, __file__)


class ThemeList(WizardWidget):  #
    """
        Description:
            A master widget managing all theme keyword lists, including
            the fixed ISO 19115 Topic Category keywords and an arbitrary
            number of user-defined thesaurus/keyword lists (using the
            Theme child widget).

        Passed arguments:
            None (Inherited from WizardWidget)

        Returned objects:
            None

        Workflow:
            1. Uses a "QTabWidget" to separate the ISO keywords tab (fixed)
               from user-defined keyword tabs.
            2. Manages a list of "Theme" widget instances (self.thesauri).
            3. Provides functionality to add/remove custom keyword lists
               and search controlled vocabularies.

        Notes:
            Inherits from "WizardWidget". The ISO keywords section is managed
            by a "RepeatingElement" of "IsoKeyword" widgets within the first
            tab.
        """

    # Class attributes.
    drag_label = "Theme Keywords <keywords>"
    acceptable_tags = ["keywords"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            initializing the ISO keyword repeater.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up the ISO keywords "RepeatingElement",
            and adds the first default ISO keyword.

        Notes:
            Disables styling for hidden tabs on the "QTabWidget".
        """

        self.ui = UI_theme_list.Ui_theme_list()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Style to hide disabled tabs (ISO tab is disabled by default)
        self.ui.theme_tabs.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; "
            "padding: 0; border: none;} "
        )

        # Setup RepeatingElement for ISO Keywords.
        self.iso_kws = RepeatingElement(
            which="vertical",
            add_text="Add additonal",
            widget=IsoKeyword,
            remove_text="Remove Keyword",
            italic_text="ISO Topic Category Keywords",
        )

        # Add the first ISO keyword widget.
        self.iso_kws.add_another()

        # Add the repeating element to the ISO tab layout.
        self.ui.iso_keywords_layout.addWidget(self.iso_kws)

        # List to hold custom Theme widgets.
        self.thesauri = []

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects buttons for adding/removing thesauri, managing
            the ISO tab, and searching controlled vocabularies.

        Notes:
            None
        """

        # Connect buttons to manage custom thesaurus tabs.
        self.ui.btn_add_thesaurus.clicked.connect(self.add_another)
        self.ui.btn_remove_selected.clicked.connect(self.remove_selected)

        # Connect button to manage the ISO keywords tab.
        self.ui.btn_add_iso.clicked.connect(self.add_iso)

        # Connect button to launch the search utility.
        self.ui.btn_search_controlled.clicked.connect(self.search_controlled)

    def add_another(self, click=False, tab_label="", locked=False):
        """
        Description:
            Adds a new custom keyword list (Theme widget) as a new tab.

        Passed arguments:
            click (bool): Not used.
            tab_label (str): Initial label for the tab.
            locked (bool): Not used here.

        Returned objects:
            theme_widget (Theme): The newly created Theme widget instance.

        Workflow:
            Creates a new "Theme" widget, connects its thesaurus text
            change signal, adds it as a new tab, and stores it in
            self.thesauri.

        Notes:
            If the current list contains "None" as a thesaurus name
            (default), it should typically be replaced, but this
            logic appears to force a new one if "tab_label" is empty.
        """

        # Logic to skip adding a new tab if one exists with "None"
        # and we are adding a custom one (tab_label="").
        if (
                "None" not in [t.get_thesaurus_name() for t in self.thesauri]
                and tab_label == ""
        ):
            # Fallback to internal add_keyword if logic dictates.
            theme_widget = self.add_keyword(
                keyword="", thesaurus="None", locked=False
            )
        else:
            # Create a new Theme widget instance.
            theme_widget = Theme()

            # Connect its thesaurus text change to update the tab label.
            theme_widget.ui.fgdc_themekt.textChanged.connect(
                self.changed_thesaurus
            )

            # Add the new widget as a new tab.
            self.ui.theme_tabs.addTab(theme_widget, tab_label)

            # Switch to the newly created tab.
            self.ui.theme_tabs.setCurrentIndex(
                self.ui.theme_tabs.count() - 1
            )

            # Store the widget instance.
            self.thesauri.append(theme_widget)

        return theme_widget

    def changed_thesaurus(self, s):
        """
        Description:
            Updates the current tab's label based on the text entered
            into the thesaurus field of the corresponding Theme widget.

        Passed arguments:
            s (str): The new text from the thesaurus line edit.

        Returned objects:
            None

        Workflow:
            Gets the current tab index and updates the tab text.

        Notes:
            None
        """

        current_index = self.ui.theme_tabs.currentIndex()

        # Prepend "Thesaurus: " to the tab text.
        self.ui.theme_tabs.setTabText(current_index, "Thesaurus: " + s)

    def remove_selected(self):
        """
        Description:
            Removes the currently selected tab/keyword list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            If index 0 (ISO) is selected, calls "remove_iso". Otherwise,
            removes the tab and deletes the corresponding "Theme" widget
            from self.thesauri.

        Notes:
            The ISO tab is handled separately. Custom tabs start at index 1
            in the tab widget.
        """

        current_index = self.ui.theme_tabs.currentIndex()
        if current_index == 0:
            # Index 0 is the ISO tab.
            self.remove_iso()
        else:
            # Remove the tab from the QTabWidget.
            self.ui.theme_tabs.removeTab(current_index)

            # Remove the corresponding widget instance.
            del self.thesauri[current_index - 1]

    def remove_iso(self):
        """
        Description:
            Disables and hides the ISO keywords tab.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets the ISO tab (index 0) to disabled/hidden.

        Notes:
            None
        """

        # Disable the ISO tab.
        self.ui.theme_tabs.setTabEnabled(0, False)

        # Hide the content of the ISO tab.
        self.ui.fgdc_theme.hide()

    def add_iso(self):
        """
        Description:
            Enables, shows, and sets the focus to the ISO keywords tab.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Enables the tab, sets its label, shows its contents, and
            switches to it. Resizes the window as a hint.

        Notes:
            None
        """

        # Enable the ISO tab.
        self.ui.theme_tabs.setTabEnabled(0, True)

        # Set the tab label.
        self.ui.theme_tabs.setTabText(0, "ISO 19115")

        # Show the content of the ISO tab.
        self.ui.fgdc_theme.show()

        # Switch to the ISO tab.
        self.ui.theme_tabs.setCurrentIndex(0)

        # Resize as a visual hint (often necessary after showing/hiding).
        self.resize(100, 100)

    def get_children(self, widget):
        """
        Description:
            Gathers all child keyword widgets that contain content
            and should be included in the XML.

        Passed arguments:
            widget (object): Reference to the current widget instance.

        Returned objects:
            children (list): List of all active keyword widgets.

        Workflow:
            1. Includes the ISO tab content if it is enabled.
            2. Includes all custom "Theme" widgets in self.thesauri.

        Notes:
            None
        """

        children = []

        # Include the ISO tab widget if it is currently enabled.
        if self.ui.theme_tabs.isTabEnabled(0):
            children.append(self.ui.fgdc_theme)

        # Include all custom Theme widgets.
        for theme in self.thesauri:
            children.append(theme)

        return children

    def clear_widget(self, remove_iso=False):
        """
        Description:
            Clears all content from this widget, removing all keywords
            and custom thesaurus tabs.

        Passed arguments:
            remove_iso (bool): If True, also removes the ISO tab.

        Returned objects:
            None

        Workflow:
            Clears ISO keywords, optionally removes the ISO tab,
            removes all custom tabs, and resets the default thesaurus text.

        Notes:
            Iterates backward when removing tabs to avoid index issues.
        """

        # Clear all keywords from the ISO repeating element.
        self.iso_kws.clear_widgets()
        if remove_iso:
            self.remove_iso()

        # Remove all custom thesaurus tabs (indices > 0).
        # Iterate backward to safely remove items.
        for i in range(len(self.thesauri), -1, -1):
            self.ui.theme_tabs.setCurrentIndex(i)
            self.remove_selected()

        # Reset the thesaurus text field on the ISO tab.
        self.ui.fgdc_themekt.setText("ISO 19115 Topic Category")

    def search_controlled(self):
        """
        Description:
            Launches the Thesaurus Search utility GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the "ThesaurusSearch" form, passing self.add_keyword
            as a callback function, and displays it.

        Notes:
            None
        """

        # Initialize the search form, passing the add_keyword method.
        self.thesaurus_search = ThesaurusSearch.ThesaurusSearch(
            add_term_function=self.add_keyword, parent=self
        )
        self.thesaurus_search.setWindowTitle(
            "Search USGS Controlled Vocabularies"
        )
        self.thesaurus_search.show()

    def add_keyword(self, keyword=None, thesaurus=None, locked=True):
        """
        Description:
            Adds a keyword to the appropriate Theme widget based on the
            provided thesaurus name. If the thesaurus doesn't exist,
            a new Theme tab is created for it.

        Passed arguments:
            keyword (str): The keyword to add.
            thesaurus (str): The name of the thesaurus.
            locked (bool): If True, the keyword is read-only.

        Returned objects:
            theme_widget (Theme): The Theme widget instance where the
                keyword was added.

        Workflow:
            1. Searches self.thesauri for a matching thesaurus name.
            2. If found, switches to that tab.
            3. If not found, creates a new tab/Theme widget.
            4. Calls the found/new "Theme" widget's "add_keyword" method.

        Notes:
            None
        """

        # Default value,
        theme_widget = None

        # 1. Search for an existing thesaurus tab.
        for i, theme in enumerate(self.thesauri):
            if theme.ui.fgdc_themekt.text() == thesaurus:
                theme_widget = theme
                try:
                    # 2. Switch to the found tab (index i + 1).
                    self.ui.theme_tabs.setCurrentIndex(i + 1)
                except IndexError:
                    pass

        # 3. If not found, create a new thesaurus tab.
        if theme_widget is None:
            # Use the first word as a short tab name.
            shortname = thesaurus.split(" ")[0]
            theme_widget = self.add_another(tab_label=shortname, locked=locked)
            theme_widget.ui.fgdc_themekt.setText(thesaurus)
            if locked:
                theme_widget.lock()
            self.changed_thesaurus(shortname)

        # 4. Add the keyword to the found or newly created Theme widget.
        theme_widget.add_keyword(keyword, locked=locked)

        return theme_widget

    def to_xml(self):
        """
        Description:
            Converts the widget's content into the FGDC <keywords>
            XML element, combining ISO and custom theme keywords.

        Passed arguments:
            None

        Returned objects:
            keywords (lxml.etree._Element): The <keywords> element
                tag in the XML tree.

        Workflow:
            1. Creates <keywords> node.
            2. Appends ISO keywords if the tab is enabled.
            3. Iterates through self.thesauri, appending their XML,
               while skipping empty default-named theme lists.

        Notes:
            None
        """

        # Create the root <keywords> node.
        keywords = xml_utils.xml_node("keywords")

        # --- Process ISO Keywords (if tab is enabled) ---
        if self.ui.theme_tabs.isTabEnabled(0):
            theme = xml_utils.xml_node("theme", parent_node=keywords)
            themekt = xml_utils.xml_node(
                "themekt", text=self.ui.fgdc_themekt.text(), parent_node=theme
            )

            # Add ISO keywords as <themekey>.
            for isokw in self.iso_kws.get_widgets():
                themekey = xml_utils.xml_node(
                    "themekey",
                    text=isokw.ui.fgdc_themekey.currentText(),
                    parent_node=theme,
                )

        # --- Process Custom Thesauri ---
        for theme in self.thesauri:
            theme_xml = theme.to_xml()

            # Check for empty default-named theme list.
            is_empty_default = (
                    theme_xml.xpath("themekt")[0].text == "None"
                    and len(theme_xml.xpath("themekey")) == 1
                    and theme_xml.xpath("themekey")[0].text is None
                    and len(self.thesauri) >= 2
            )

            if not is_empty_default:
                keywords.append(theme_xml)

        return keywords

    def from_xml(self, keywords_xml):
        """
        Description:
            Parses an FGDC <keywords> XML element and populates the
            ISO and custom theme keyword lists.

        Passed arguments:
            keywords_xml (lxml.etree._Element): The XML element,
                expected to be <keywords>.

        Returned objects:
            None

        Workflow:
            1. Clears existing content.
            2. Iterates through all <theme> elements in the XML.
            3. If thesaurus is "ISO 19115", populates the ISO tab.
            4. Otherwise, creates a new "Theme" tab and calls
               "theme.from_xml" recursively.

        Notes:
            None
        """

        # Clear existing content before loading.
        self.clear_widget(remove_iso=True)

        self.original_xml = keywords_xml
        if keywords_xml.tag == "keywords":
            # Search for all <theme> elements.
            for theme_xml in xml_utils.search_xpath(keywords_xml,
                                                    "theme",
                                                    False):
                themekt = xml_utils.get_text_content(theme_xml,
                                                     "themekt")

                # Check for ISO keywords.
                if themekt is not None and "iso 19115" in themekt.lower():
                    self.add_iso()
                    self.iso_kws.clear_widgets(add_another=False)

                    # Populate ISO keywords.
                    for themekey in xml_utils.search_xpath(
                        theme_xml, "themekey", only_first=False
                    ):
                        iso = self.iso_kws.add_another()
                        iso.ui.fgdc_themekey.setCurrentText(themekey.text)

                # Handle custom themes.
                else:
                    theme = self.add_another()
                    theme.from_xml(theme_xml)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ThemeList, "ThemeList Step testing")
