#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Overview frame for Process Step element


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

from lxml import etree

from pymdwizard.core import utils, xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_crossref
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.citeinfo import Citeinfo


class CrossRef(WizardWidget): #

    drag_label = "Cross Reference <crossref>"
    acceptable_tags = ['idinfo']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_crossref.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.crossrefs = RepeatingElement(which='tab',
                         tab_label='Crossref', add_text='   Add Additional Crossref   ',
                         widget=Citeinfo, remove_text='   Remove Selected Crossref   ', italic_text='')

        self.crossrefs.add_another()
        self.ui.crossref_widget.layout().addWidget(self.crossrefs)

        self.ui.crossref_widget.hide()

    def connect_events(self):
        """
            Connect the appropriate GUI components with the corresponding functions

            Returns
            -------
            None
            """
        self.ui.radio_crossrefyes.toggled.connect(self.crossref_used_change)

    def crossref_used_change(self, b):
        if b:
            self.ui.crossref_widget.show()
        else:
            self.ui.crossref_widget.hide()


    def _to_xml(self):
        """
        encapsulates the etree process step in an element tag

        Returns
        -------
        procstep portion of the lineageg element tag in xml tree
        """
        crossrefs = []
        for citeinfo in self.crossrefs.get_widgets():
            crossref = xml_utils.xml_node('crossref')
            crossref.append(citeinfo._to_xml())
            crossrefs.append(crossref)

        return crossrefs

    def _from_xml(self, xml_idinfo):
        """
        parses the xml code into the relevant accconst elements

        Parameters
        ----------
        access_constraints - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if xml_idinfo.tag == 'idinfo':
                self.crossrefs.clear_widgets(add_another=False)

                crossrefs = xml_utils.search_xpath(xml_idinfo, 'crossref', only_first=False)

                if crossrefs:
                    self.ui.radio_crossrefyes.setChecked(True)
                else:
                    self.crossrefs.add_another()
                    self.ui.radio_crossrefno.setChecked(True)

                for crossref in crossrefs:
                    crossref_widget = self.crossrefs.add_another()
                    crossref_widget._from_xml(xml_utils.search_xpath(crossref, 'citeinfo'))


        except KeyError:
            self.ui.radio_crossrefno.setChecked(True)


if __name__ == "__main__":
    utils.launch_widget(CrossRef,
                        "Source Input testing")

