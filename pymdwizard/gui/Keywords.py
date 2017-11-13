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

from copy import deepcopy

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_Keywords
from pymdwizard.gui.theme_list import ThemeList
from pymdwizard.gui.place_list import PlaceList


class Keywords(WizardWidget):

    drag_label = "Keywords <keywords>"
    acceptable_tags = ['keywords', 'theme']

    ui_class = UI_Keywords.Ui_keyword_widget

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.theme_list = ThemeList(parent=self)
        self.ui.fgdc_keywords.layout().addWidget(self.theme_list)

        self.place_list = PlaceList(parent=self)
        self.ui.fgdc_keywords.layout().addWidget(self.place_list)

        spacerItem = QSpacerItem(24, 10, QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.ui.fgdc_keywords.layout().addItem(spacerItem)
        self.setup_dragdrop(self)

    def to_xml(self):
        keywords = self.theme_list.to_xml()

        place_keywords = self.place_list.to_xml()
        for child_node in place_keywords.xpath('place'):
            keywords.append(child_node)

        if self.original_xml is not None:
            stratums = xml_utils.search_xpath(self.original_xml, 'stratum',
                                              only_first=False)
            for stratum in stratums:
                stratum.tail = None
                keywords.append(deepcopy(stratum))

            temporals = xml_utils.search_xpath(self.original_xml, 'temporal',
                                               only_first=False)
            for temporal in temporals:
                temporal.tail = None
                keywords.append(deepcopy(temporal))

        return keywords

    def from_xml(self, keywords):

        self.original_xml = keywords

        self.theme_list.from_xml(keywords)
        self.place_list.from_xml(keywords)


if __name__ == "__main__":
    utils.launch_widget(Keywords,
                        "keywords testing")







