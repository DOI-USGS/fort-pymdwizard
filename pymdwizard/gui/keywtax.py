#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.keywords_repeater import KeywordsRepeater


class Keywordtax(KeywordsRepeater):

    drag_label = "Taxonomic keywords <keywtax>"
    acceptable_tags = ['keywtax']

    def __init__(self, parent=None):
        KeywordsRepeater.__init__(self, keywords_label='Taxonomic keywords',
                                  spellings=False, parent=parent)
        self.ui.fgdc_themekt.name = 'fgdc_taxonkt'

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
        keywtax = xml_utils.xml_node('keywtax')
        taxonkt = xml_utils.xml_node("taxonkt",
                                     text=self.ui.fgdc_themekt.text(),
                                     parent_node=keywtax)
        for keyword in self.get_keywords():
            taxonkey = xml_utils.xml_node('taxonkey', text=keyword,
                                          parent_node=keywtax)

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
            if keywtax.tag == 'keywtax':
                thesaurus = keywtax.xpath('taxonkt')
                if thesaurus:
                    self.ui.fgdc_themekt.setText(thesaurus[0].text)

                keywords = keywtax.xpath('taxonkey')
                self.keywords.clear_widgets(add_another=False)
                for kw in keywords:
                    kw_widget = self.keywords.add_another()
                    kw_widget.setText(kw.text)

            else:
                print ("The tag is not keywtax")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Keywordtax,
                        " testing")
