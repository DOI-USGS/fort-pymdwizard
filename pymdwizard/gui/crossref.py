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

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.citeinfo import Citeinfo


class Crossref(Citeinfo):

    drag_label = "Cross Reference <crossref>"
    acceptable_tags = ["crossref", "citeinfo"]

    def build_ui(self,):
        Citeinfo.build_ui(self)

        self.setObjectName("fgdc_crossref")
        self.ui.fgdc_lworkcit.hide()
        self.ui.lbl_dataset_title.setText("Crossref Title")
        self.ui.label_34.hide()
        self.ui.label_38.hide()
        self.ui.label_47.setText("Author/Originator")
        self.ui.label_53.setText("Format")
        self.ui.fgdc_geoform.setCurrentText("publication")
        self.ui.label_51.setText("Online Link to the Publication")
        self.ui.label_53.setText("Can you provide more publication information?")
        self.ui.label_43.setText("Is this publication part of a series?")

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.radio_lworkyes.toggled.connect(self.include_lworkext_change)
        self.ui.radio_seriesyes.toggled.connect(self.include_seriesext_change)
        self.ui.radio_pubinfoyes.toggled.connect(self.include_pubext_change)

        self.ui.btn_import_doi.clicked.connect(self.get_doi_citation)

    def to_xml(self):
        """
        encapsulates the QLineEdit text in an element tag

        Returns
        -------
        citation element tag in xml tree
        """
        citeinfo = Citeinfo.to_xml(self)
        crossref = xml_utils.xml_node("crossref")
        crossref.append(citeinfo)

        return crossref

    def from_xml(self, citeinfo):
        """
        parses the xml code into the relevant citation elements

        Parameters
        ----------
        citation - the xml element status and its contents

        Returns
        -------
        None
        """
        self.original_xml = citeinfo
        self.clear_widget()
        try:
            if citeinfo.tag == "citation":
                citeinfo = citeinfo.xpath("citeinfo")[0]
            if citeinfo.tag == "crossref":
                citeinfo = citeinfo.xpath("citeinfo")[0]
            elif citeinfo.tag != "citeinfo":
                print("The tag is not 'citation' or 'citeinfo'")
                return

            Citeinfo.from_xml(self, citeinfo)

        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Crossref, "Crossref testing")
