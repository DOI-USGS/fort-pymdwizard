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
    from pymdwizard.gui.keywords_repeater import KeywordsRepeater
except ImportError as err:
    raise ImportError(err, __file__)


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
        taxonkt = xml_utils.xml_node(
            "{}kt".format(self.which),
            text=self.ui.fgdc_themekt.text(),
            parent_node=keywtax,
        )

        # Create and append individual keyword nodes (e.g., <themkey>).
        for keyword in self.get_keywords():
            taxonkey = xml_utils.xml_node(
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
