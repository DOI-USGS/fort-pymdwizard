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
from copy import deepcopy

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QSizePolicy, QSpacerItem)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_Keywords
    from pymdwizard.gui.theme_list import ThemeList
    from pymdwizard.gui.place_list import PlaceList
except ImportError as err:
    raise ImportError(err, __file__)


class Keywords(WizardWidget):
    """
    Description:
        A widget for managing the FGDC "Keywords" ("keywords") metadata
        section, which includes Theme, Place, Stratum, and Temporal
        keywords. Inherits from WizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Initializes and builds the child widgets "ThemeList" and
        "PlaceList", placing them into the UI layout. It aggregates the
        XML from these lists, while also preserving any existing Stratum
        and Temporal keywords from the original XML.

    Notes:
        Only Theme and Place keywords are managed via specific sub-
        widgets; Stratum and Temporal keywords are preserved via XML
        xpath searching.
    """

    # Class attributes.
    drag_label = "Keywords <keywords>"
    acceptable_tags = ["keywords", "theme"]

    # Assumed UI class for instantiation.
    ui_class = UI_Keywords.Ui_keyword_widget

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates the UI, creates the "ThemeList" and "PlaceList"
            widgets, and adds them to the layout. Also adds a spacer
            item for visual layout.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Initialize and add Theme Keywords list.
        self.theme_list = ThemeList(parent=self)
        self.ui.fgdc_keywords.layout().addWidget(self.theme_list)

        # Initialize and add Place Keywords list.
        self.place_list = PlaceList(parent=self)
        self.ui.fgdc_keywords.layout().addWidget(self.place_list)

        # Add a flexible spacer to push content up.
        spacerItem = QSpacerItem(24, 10, QSizePolicy.Preferred,
                                 QSizePolicy.Expanding)
        self.ui.fgdc_keywords.layout().addItem(spacerItem)

        # Setup drag-and-drop functionality.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Encapsulates all keyword information into a single 'keywords'
            XML element tag.

        Passed arguments:
            None

        Returned objects:
            keywords (ElementTree.Element): The merged keywords element
                tag in XML tree.

        Workflow:
            1. Gets the XML from "ThemeList" (which is the root
               <keywords> node).
            2. Appends the <place> nodes from "PlaceList" XML to the
               <keywords> node.
            3. Preserves any original <stratum> and <temporal> nodes
               if they exist in the source XML.

        Notes:
            None
        """

        # Start with keywords from the ThemeList.
        keywords = self.theme_list.to_xml()

        # Get the Place keywords XML.
        place_keywords = self.place_list.to_xml()

        # Append only the <place> nodes to the main <keywords> node.
        for child_node in place_keywords.xpath("place"):
            keywords.append(child_node)

        # Preserve existing <stratum> tags from original XML.
        if self.original_xml is not None:
            stratums = xml_utils.search_xpath(
                self.original_xml, "stratum", only_first=False
            )
            for stratum in stratums:
                stratum.tail = None
                keywords.append(deepcopy(stratum))

            # Preserve existing <temporal> tags from original XML.
            temporals = xml_utils.search_xpath(
                self.original_xml, "temporal", only_first=False
            )
            for temporal in temporals:
                temporal.tail = None
                keywords.append(deepcopy(temporal))

        return keywords

    def from_xml(self, keywords):
        """
        Description:
            Parses the XML code into the Theme and Place keyword list
            widgets.

        Passed arguments:
            keywords (ElementTree.Element): The XML element containing
                the keyword information.

        Returned objects:
            None

        Workflow:
            Stores the original XML, then calls the "from_xml" method on
            the "ThemeList" and "PlaceList" children.

        Notes:
            None
        """

        # Store the original XML for later use in to_xml().
        self.original_xml = keywords

        # Delegate XML parsing to the child widgets.
        self.theme_list.from_xml(keywords)
        self.place_list.from_xml(keywords)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Keywords, "keywords testing")
