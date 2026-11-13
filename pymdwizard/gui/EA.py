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
None
"""

# Non-standard python libraries.
try:
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import (QMenu, QProxyStyle, QStyle, QTabBar,
                                 QWidget)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_EA
    from pymdwizard.gui.detailed import Detailed
    from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
except ImportError as err:
    raise ImportError(err, __file__)


# Tab text colors for the "+" (add Detailed) and Overview tabs.
ADD_TAB_COLOR = QColor(0, 110, 0)
OVERVIEW_TAB_COLOR = QColor(110, 70, 150)

# Extra thickness (pixels) added to each tab on the left-hand tab strip.
TAB_EXTRA_THICKNESS = 8


class WiderTabStyle(QProxyStyle):
    """
    Description:
        Makes the tabs on a vertical (West) tab bar thicker, leaving
        fonts and everything else in the base style unchanged.

    Notes:
        A style is used instead of a stylesheet because
        "MainWindow.highlight_tab" and "clear_validation" replace and
        clear the tab widget's stylesheet.
    """

    def sizeFromContents(self, contents_type, option, size, widget=None):
        size = super().sizeFromContents(contents_type, option, size, widget)
        if contents_type == QStyle.CT_TabBarTab and option.shape in (
            QTabBar.RoundedWest,
            QTabBar.TriangularWest,
        ):
            # For vertical tabs the width is the tab's thickness.
            size.setWidth(size.width() + TAB_EXTRA_THICKNESS)
        return size


class EA(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "Entity and Attribute Information"
        ("eainfo") metadata section. It handles both overview fields
        and a repeating list of "Detailed" description widgets.
        Inherits from WizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages UI for Entity/Attribute Overview ("eaover") and
        Detailed Citation ("eadetcit"). Uses a tab widget to contain a
        list of dynamically added "Detailed" description widgets.

    Notes:
        The tab widget structure requires special handling for adding/
        removing the "Detailed" tabs.
    """

    # Class attributes.
    drag_label = "Entity and Attributes <eainfo>"
    acceptable_tags = ["eainfo", "detailed"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, sets up the list for "Detailed" widgets,
            adds the initial "Detailed" tab, sets up drag-and-drop, and
            applies syntax highlighting to text areas.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_EA.Ui_Form()
        self.ui.setupUi(self)

        # List to hold references to Detailed widgets.
        self.detaileds = []

        # Make the left-hand tabs a bit thicker so they are easier to see.
        # A reference is kept because Qt does not own the style.
        tab_bar = self.ui.fgdc_eainfo.tabBar()
        self._tab_style = WiderTabStyle()
        tab_bar.setStyle(self._tab_style)

        # Tab order is: Instructions, Detailed tab(s), "+", Overview.
        # The "+" tab holds an empty placeholder page. Selecting it adds
        # a new Detailed tab (see "on_tab_changed").
        self.add_tab = QWidget()
        self.add_tab.setObjectName("tab_add_detailed")
        self.ui.fgdc_eainfo.insertTab(1, self.add_tab, "+")
        self.ui.fgdc_eainfo.setTabToolTip(1, "Add another Detailed section")
        self.ui.fgdc_eainfo.tabBar().setTabTextColor(1, ADD_TAB_COLOR)

        # Color the Overview tab text to show it is a different kind of
        # tab than the Detailed ones.
        overview_index = self.ui.fgdc_eainfo.indexOf(self.ui.fgdc_overview)
        self.ui.fgdc_eainfo.tabBar().setTabTextColor(
            overview_index, OVERVIEW_TAB_COLOR
        )

        # Add the first required Detailed tab.
        self.add_detailed()

        # Initialize drag-and-drop features.
        self.setup_dragdrop(self)

        # Setup syntax highlighting for overview fields.
        self.highlighter = Highlighter(self.ui.fgdc_eaover.document())
        self.highlighter2 = Highlighter(self.ui.fgdc_eadetcit.document())

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
            Connects the "Add Detailed" button to the "add_detailed"
            method.

        Notes:
            None
        """

        # Connect the button to add a new Detailed tab.
        self.ui.btn_add_detailed.clicked.connect(self.add_detailed)

        # Selecting the "+" tab adds a new Detailed tab.
        self.ui.fgdc_eainfo.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """
        Description:
            Adds a new "Detailed" tab when the "+" tab is selected.

        Passed arguments:
            index (int): Index of the newly selected tab.

        Returned objects:
            None

        Workflow:
            If the selected tab is the "+" placeholder, creates a new
            Detailed tab and selects it, so the empty placeholder page
            is never left on screen.

        Notes:
            Code that removes tabs blocks this signal while it works,
            so Qt moving the selection onto the "+" tab does not add a
            tab.
        """

        if self.ui.fgdc_eainfo.widget(index) is self.add_tab:
            new_detailed = self.add_detailed()
            self.ui.fgdc_eainfo.setCurrentWidget(new_detailed)

    def remove_detailed(self):
        """
        Description:
            Removes the currently selected "Detailed" tab from the UI
            and the internal list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the current tab index, removes the tab from the UI
            widget, and deletes the corresponding object from the
            "detaileds" list.

        Notes:
            The first "Detailed" widget cannot be removed.
        """

        self.remove_detailed_at(self.ui.fgdc_eainfo.currentIndex())

    def remove_detailed_at(self, index):
        """
        Description:
            Removes the "Detailed" tab at the given tab index.

        Passed arguments:
            index (int): Tab index of the Detailed tab to remove.

        Returned objects:
            None

        Workflow:
            Removes the tab and its entry in the "detaileds" list. If
            the removed tab was the selected one, selects a neighboring
            Detailed tab (Instructions if none are left).

        Notes:
            Used by the "Remove this Detailed" button (current tab) and
            the tab bar right-click menu (any tab).
        """

        was_current = index == self.ui.fgdc_eainfo.currentIndex()

        # Remove the tab from the QTabWidget. Signals are blocked because
        # Qt may move the selection onto the "+" tab, which would add a tab.
        self.ui.fgdc_eainfo.blockSignals(True)
        self.ui.fgdc_eainfo.removeTab(index)
        self.ui.fgdc_eainfo.blockSignals(False)

        # Remove the widget instance from the internal list.
        # Note: Index is -1 because the first tab (index 0) is reserved.
        del self.detaileds[index - 1]

        # If the selected tab was removed, select the previous Detailed tab
        # (or the next one if the first was removed). Fall back to
        # Instructions if none are left.
        if was_current:
            if self.detaileds:
                self.ui.fgdc_eainfo.setCurrentIndex(max(index - 1, 1))
            else:
                self.ui.fgdc_eainfo.setCurrentIndex(0)

    def contextMenuEvent(self, event):
        """
        Description:
            Shows a menu specific to the tab label that was right-clicked.

        Passed arguments:
            event (QContextMenuEvent): The context menu event.

        Returned objects:
            None

        Workflow:
            - Detailed tab label: menu with "Remove this Detailed",
              which removes that tab (not necessarily the selected one).
            - Overview tab label: menu with "Clear Overview", which
              clears only the two overview text fields.
            - Instructions and "+" tab labels: no menu.
            - Anywhere else: the standard WizardWidget menu.

        Notes:
            Without this, right-clicking a tab label reaches the
            standard menu, whose "Clear content" clears the whole
            Entity and Attribute section, including every Detailed tab.
        """

        tab_bar = self.ui.fgdc_eainfo.tabBar()
        index = tab_bar.tabAt(tab_bar.mapFrom(self, event.pos()))

        # Not on a tab label: use the standard menu.
        if index < 0:
            WizardWidget.contextMenuEvent(self, event)
            return

        tab = self.ui.fgdc_eainfo.widget(index)
        if tab in self.detaileds:
            action_text = "Remove this Detailed"
        elif tab is self.ui.fgdc_overview:
            action_text = "Clear Overview"
        else:
            # Instructions and "+" tabs: no menu.
            event.accept()
            return

        self.in_context = True
        menu = QMenu(self)
        tab_action = menu.addAction(action_text)
        action = menu.exec_(event.globalPos())
        if action == tab_action:
            if tab is self.ui.fgdc_overview:
                utils.set_text(self.ui.fgdc_eaover, "")
                utils.set_text(self.ui.fgdc_eadetcit, "")
            else:
                self.remove_detailed_at(index)
        self.in_context = False

    def add_detailed(self):
        """
        Description:
            Adds another "Detailed" tab to the form.

        Passed arguments:
            None

        Returned objects:
            new_detailed (Detailed): The newly created Detailed widget.

        Workflow:
            Creates a new "Detailed" widget, passes the "remove_detailed"
            function, inserts the new widget just before the "+" tab
            (after the last Detailed tab), and appends it to the
            internal list.

        Notes:
            None
        """

        # Instantiate a new Detailed widget.
        new_detailed = Detailed(remove_function=self.remove_detailed,
                                parent=self)
        # Insert the new tab after the last Detailed tab, before the "+" tab.
        # Tab 0 is Instructions, so Detailed tab n sits at index n + 1.
        self.ui.fgdc_eainfo.insertTab(
            len(self.detaileds) + 1, new_detailed, "Detailed"
        )

        # Store the new widget instance.
        self.detaileds.append(new_detailed)

        return new_detailed

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears the content of the first "Detailed" tab, removes all
            subsequent "Detailed" tabs, and clears the overview text
            fields. If every Detailed tab was removed, adds a blank one
            first.

        Notes:
            Users can remove every Detailed tab, but this method and
            "from_xml" need at least one to exist.
        """

        # Users can remove all Detailed tabs; restore one so there is
        # always a first Detailed widget to clear and populate.
        if not self.detaileds:
            self.add_detailed()

        # Clear the content of the first Detailed widget.
        self.detaileds[0].clear_widget()

        # Remove all extra Detailed tabs (from end to 1). Signals are
        # blocked because Qt may move the selection onto the "+" tab,
        # which would add a tab.
        self.ui.fgdc_eainfo.blockSignals(True)
        for i in range(len(self.detaileds), 1, -1):
            self.ui.fgdc_eainfo.removeTab(i)

            # Remove from the internal list.
            del self.detaileds[i - 1]
        self.ui.fgdc_eainfo.blockSignals(False)

        # Don't leave the empty "+" placeholder page showing.
        if self.ui.fgdc_eainfo.currentWidget() is self.add_tab:
            self.ui.fgdc_eainfo.setCurrentIndex(1)

        # Clear the overview text fields.
        utils.set_text(self.ui.fgdc_eaover, "")
        utils.set_text(self.ui.fgdc_eadetcit, "")

    def has_content(self):
        """
        Description:
            Checks for valid content in this widget.

        Passed arguments:
            None

        Returned objects:
            bool: True if any text fields are populated or if any
                "Detailed" widget has content.

        Workflow:
            Checks the overview texts and iterates through all "Detailed"
            widgets to see if any have content.

        Notes:
            None
        """

        # Initiate default value.
        has_content = False

        # Check overview text fields.
        if self.ui.fgdc_eadetcit.toPlainText():
            has_content = True
        if self.ui.fgdc_eaover.toPlainText():
            has_content = True

        # Check if the first Detailed widget has content.
        if self.detaileds and self.detaileds[0].has_content():
            has_content = True

        # Check all other Detailed widgets.
        for detailed in self.detaileds:
            if detailed.has_content():
                has_content = True

        return has_content

    def to_xml(self):
        """
        Description:
            Encapsulates the Entity and Attribute information into a
            single "eainfo" XML element tag.

        Passed arguments:
            None

        Returned objects:
            eainfo (xml.etree.ElementTree.Element): Entity and Attribute
                element tag in XML tree.

        Workflow:
            1. Creates the <eainfo> parent node.
            2. Appends the XML for all "Detailed" widgets.
            3. If overview text exists, creates the <overview> node
               with <eaover> and <eadetcit> children.

        Notes:
            The first "Detailed" node is only output if it has content,
            but subsequent nodes are output regardless.
        """

        # Create the parent "eainfo" XML node.
        eainfo = xml_utils.xml_node("eainfo")

        # Only output the first detailed if it has content
        if self.detaileds and self.detaileds[0].has_content():
            detailed_xml = self.detaileds[0].to_xml()
            eainfo.append(detailed_xml)

        # The remaining detaileds will get output regardless.
        for detailed in self.detaileds[1:]:
            detailed_xml = detailed.to_xml()
            eainfo.append(detailed_xml)

        # Get the overview text fields.
        eaover_str = self.ui.fgdc_eaover.toPlainText()
        eadetcit_str = self.ui.fgdc_eadetcit.toPlainText()

        # Create and append <overview> if either text field is populated.
        if eaover_str or eadetcit_str:
            overview = xml_utils.xml_node("overview", parent_node=eainfo)
            # <eaover>
            xml_utils.xml_node("eaover", text=eaover_str,
                               parent_node=overview)
            # <eadetcit>
            xml_utils.xml_node(
                "eadetcit", text=eadetcit_str, parent_node=overview
            )

        return eainfo

    def from_xml(self, eainfo):
        """
        Description:
            Parse the XML code into the relevant E&A elements.

        Passed arguments:
            eainfo (xml.etree.ElementTree.Element): The XML element
                containing the entity and attribute information.

        Returned objects:
            None

        Workflow:
            1. Clears existing widgets.
            2. Parses <overview> and populates text fields.
            3. Parses the first <detailed> node into the initial tab.
            4. Iterates over remaining <detailed> nodes, adding a new
               tab for each, and populating its content.

        Notes:
            None
        """

        try:
            # Clear all existing content first.
            self.ui.fgdc_eainfo.setCurrentIndex(0)
            self.clear_widget()

            if eainfo.tag == "eainfo":
                self.original_xml = eainfo
                overview = eainfo.xpath("overview")

                # Parse and populate overview text fields.
                if overview:
                    eaover = eainfo.xpath("overview/eaover")
                    if eaover:
                        utils.set_text(self.ui.fgdc_eaover, eaover[0].text)

                    eadetcit = eainfo.xpath("overview/eadetcit")
                    if eadetcit:
                        utils.set_text(self.ui.fgdc_eadetcit, eadetcit[0].text)

                    # Switch to the overview tab after populating.
                    self.ui.fgdc_eainfo.setCurrentWidget(
                        self.ui.fgdc_overview
                    )

                # Parse and populate detailed sections.
                detailed = eainfo.xpath("detailed")
                if detailed:
                    # Populate the first required Detailed tab.
                    self.ui.fgdc_eainfo.setCurrentIndex(1)
                    self.detaileds[0].from_xml(detailed[0])

                    # Loop through all remaining Detailed nodes.
                    for i, additional_detailed in enumerate(detailed[1:]):
                        # Add a new tab for each.
                        new_detailed = self.add_detailed()

                        # Set current tab to the new one.
                        self.ui.fgdc_eainfo.setCurrentIndex(i + 2)

                        # Populate the new tab.
                        new_detailed.from_xml(additional_detailed)
            else:
                print("The tag is not EA")
        except KeyError:
            return None


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(EA, "detailed testing")
