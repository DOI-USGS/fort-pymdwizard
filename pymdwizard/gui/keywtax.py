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


class Keywordtax(KeywordsRepeater):
    """
    Description:
        A specialized widget for managing FGDC "Taxonomic Keywords"
        ("keywtax"). It inherits from KeywordsRepeater and customizes
        labels and XML generation/parsing for taxonomic terms.
        Inherits from KeywordsRepeater.

    Passed arguments:
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        Initializes the base repeater with specific labels and disables
        spelling/autocomplete (as taxonomic terms may be unique), and
        then customizes the XML tag names.

    Notes:
        The thesaurus input line uses the object name "fgdc_taxonkt"
        instead of the default thematic one.
    """

    # Class attributes.
    drag_label = "Taxonomic keywords <keywtax>"
    acceptable_tags = ["keywtax"]

    def __init__(self, parent=None):
        # Initialize the parent class with specific parameters.
        KeywordsRepeater.__init__(
            self, keywords_label="Taxonomic keywords", spellings=False,
            parent=parent
        )

        # Set the correct object name for the thesaurus input.
        self.ui.fgdc_themekt.name = "fgdc_taxonkt"

    def clear_widget(self):
        """
        Description:
            Clears the text from the thesaurus and removes all keyword
            input lines.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears the thesaurus text and calls the repeater's clear
            method to remove keywords.

        Notes:
            None
        """

        # Clear the thesaurus text input.
        self.ui.fgdc_themekt.clear()

        # Clear all dynamically added keyword widgets.
        self.keywords.clear_widgets()

    def to_xml(self):
        """
        Description:
            Encapsulates the taxonomic keywords into a single "keywtax"
            XML element tag.

        Passed arguments:
            None

        Returned objects:
            keywtax (ElementTree.Element): Taxonomic keywords element
                tag in XML tree.

        Workflow:
            Creates the <keywtax> parent node, appends <taxonkt>
            (thesaurus), and then appends a <taxonkey> node for each
            keyword in the list.

        Notes:
            None
        """

        # Create the parent "keywtax" XML node.
        keywtax = xml_utils.xml_node("keywtax")

        # Create the "taxonkt" (Taxonomic Keyword Thesaurus) node.
        xml_utils.xml_node(
            "taxonkt",
            text=self.ui.fgdc_themekt.text(),
            parent_node=keywtax,
        )

        # Create a "taxonkey" node for each keyword.
        for keyword in self.get_keywords():
            xml_utils.xml_node(
                "taxonkey", text=keyword, parent_node=keywtax
            )

        return keywtax

    def from_xml(self, keywtax):
        """
        Description:
            Parses the XML code into the thesaurus and keyword widgets.

        Passed arguments:
            keywtax (ElementTree.Element): The XML element containing
                the taxonomic keyword information.

        Returned objects:
            None

        Workflow:
            1. Checks for the "keywtax" tag.
            2. Populates the thesaurus field from the <taxonkt> child.
            3. Clears the existing keyword list.
            4. Populates the repeating keyword lines from <taxonkey>
               children.

        Notes:
            None
        """

        try:
            if keywtax.tag == "keywtax":
                # Find the thesaurus (taxonkt) tag.
                thesaurus = keywtax.xpath("taxonkt")

                if thesaurus:
                    # Set the thesaurus text field.
                    self.ui.fgdc_themekt.setText(thesaurus[0].text)

                # Find all individual keyword tags.
                keywords = keywtax.xpath("taxonkey")

                # Clear existing keyword widgets before repopulating.
                self.keywords.clear_widgets(add_another=False)
                for kw in keywords:
                    # Add a new keyword widget for each XML node.
                    kw_widget = self.keywords.add_another()

                    # Set the text of the new widget.
                    kw_widget.setText(kw.text)
            else:
                print("The tag is not keywtax")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Keywordtax, " testing")
