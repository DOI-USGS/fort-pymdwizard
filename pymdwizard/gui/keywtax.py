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
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.keywords_repeater import KeywordsRepeater
except ImportError as err:
    raise ImportError(err, __file__)


class Keywordtax(KeywordsRepeater):

    drag_label = "Taxonomic keywords <keywtax>"
    acceptable_tags = ["keywtax"]

    def __init__(self, parent=None):
        KeywordsRepeater.__init__(
            self, keywords_label="Taxonomic keywords", spellings=False, parent=parent
        )
        self.ui.fgdc_themekt.name = "fgdc_taxonkt"

    def clear_widget(self):
        self.ui.fgdc_themekt.clear()
        self.keywords.clear_widgets()

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        keywtax = xml_utils.xml_node("keywtax")
        taxonkt = xml_utils.xml_node(
            "taxonkt", text=self.ui.fgdc_themekt.text(), parent_node=keywtax
        )
        for keyword in self.get_keywords():
            taxonkey = xml_utils.xml_node("taxonkey", text=keyword, parent_node=keywtax)

        return keywtax

    def from_xml(self, keywtax):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if keywtax.tag == "keywtax":
                thesaurus = keywtax.xpath("taxonkt")
                if thesaurus:
                    self.ui.fgdc_themekt.setText(thesaurus[0].text)

                keywords = keywtax.xpath("taxonkey")
                self.keywords.clear_widgets(add_another=False)
                for kw in keywords:
                    kw_widget = self.keywords.add_another()
                    kw_widget.setText(kw.text)

            else:
                print("The tag is not keywtax")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Keywordtax, " testing")
