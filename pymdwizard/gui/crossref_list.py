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

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_crossref
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.crossref import Crossref


class Crossref_list(WizardWidget):

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
                         widget=Crossref, remove_text='   Remove Selected Crossref   ', italic_text='')

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

    def has_content(self):
        return self.ui.radio_crossrefyes.isChecked()

    def get_children(self, widget=None):

        children = []

        for crossref in self.crossrefs.get_widgets():
            children.append(crossref)

        return children

    def clear_widget(self):
        super(Crossref_list, self).clear_widget()
        self.ui.radio_crossrefno.setChecked(True)

    def to_xml(self):
        """
        encapsulates the etree process step in an element tag

        Returns
        -------
        procstep portion of the lineageg element tag in xml tree
        """
        crossrefs = []
        idinfo = xml_utils.xml_node(tag='idinfo')
        for crossref in self.crossrefs.get_widgets():
            idinfo.append(crossref.to_xml())

        return idinfo

    def from_xml(self, xml_idinfo):
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
                    crossref_widget.from_xml(xml_utils.search_xpath(crossref, 'citeinfo'))


        except KeyError:
            self.ui.radio_crossrefno.setChecked(True)


if __name__ == "__main__":
    utils.launch_widget(Crossref_list,
                        "Source Input testing")







