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


class Theme(KeywordsRepeater):  #

    drag_label = "Theme Keywords <theme>"
    acceptable_tags = ['theme']

    def __init__(self, which='theme', parent=None):
        self.acceptable_tags = [which, ]
        self.which = which
        KeywordsRepeater.__init__(self, keywords_label='Keyword   ',
                                  parent=parent, line_name='fgdc_{}key'.format(self.which))

        self.kt = self.ui.fgdc_themekt
        if which == 'place':
            self.setObjectName('fgdc_place')
            self.drag_label = "Place Keywords <place>"
            self.ui.fgdc_themekt.setObjectName('fgdc_placekt')
            self.acceptable_tags = ['place']
        else:
            self.setObjectName('fgdc_theme')

    def add_keyword(self, keyword, locked=False):
        """
        Adds a given keyword to the current list of keywords,
        if it is not currently in the list.

        Parameters
        ----------
        keyword : str
                  String to add to the list.
        locked : bool
                 Flag specifying if the added item will be editable

        Returns
        -------
        None
        """
        existing_kws = self.get_keywords()
        if existing_kws[0] == '':
            kw = self.keywords.get_widgets()[0]
            kw.setText(keyword)
            kw.added_line.setReadOnly(locked)
        elif keyword not in existing_kws:
            kw = self.keywords.add_another()
            kw.setText(keyword)
            kw.added_line.setReadOnly(locked)

    def get_thesaurus_name(self):
        """
        Return the current thesaurus name for this widget.

        Returns
        -------
        str
        """
        return self.kt.text()

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        keywtax = xml_utils.xml_node(self.which)
        taxonkt = xml_utils.xml_node("{}kt".format(self.which),
                                     text=self.ui.fgdc_themekt.text(),
                                     parent_node=keywtax)
        for keyword in self.get_keywords():
            taxonkey = xml_utils.xml_node("{}key".format(self.which),
                                          text=keyword,
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
            if keywtax.tag == self.which:
                thesaurus = keywtax.xpath("{}kt".format(self.which))
                if thesaurus:
                    self.ui.fgdc_themekt.setText(thesaurus[0].text)

                keywords = keywtax.xpath("{}key".format(self.which))
                for kw in keywords:
                    if self.keywords.get_widgets()[0].text() == '':
                        kw_widget = self.get_widgets()[0]
                    else:
                        kw_widget = self.keywords.add_another()

                    kw_widget.setText(kw.text)

            else:
                print ("The tag is not theme")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Theme,
                        " testing", which='place')

