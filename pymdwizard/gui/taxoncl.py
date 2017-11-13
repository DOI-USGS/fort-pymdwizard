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
from pymdwizard.gui.ui_files import UI_taxoncl
from pymdwizard.gui.repeating_element import RepeatingElement


class Taxoncl(WizardWidget):

    drag_label = "taxon class <taxoncl>"
    acceptable_tags = ['taxoncl']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_taxoncl.Ui_fgdc_taxoncl()
        self.ui.setupUi(self)

        widget_kwargs = {'line_name':'common',
                         'required':False}

        self.commons = RepeatingElement(add_text='Add Common',
                                         remove_text='Remove last',
                                         widget_kwargs=widget_kwargs,
                                         show_buttons=False
                                         )
        self.commons.add_another()
        self.ui.horizontalLayout_4.addWidget(self.commons)

        self.child_taxoncl = []

        self.setup_dragdrop(self)

    def clear_widget(self):
        """
        Clears all content from this widget

        Returns
        -------
        None
        """
        self.ui.fgdc_taxonrn.clear()
        self.ui.fgdc_taxonrv.clear()
        self.commons.clear_widgets()

        for taxoncl in self.child_taxoncl:
            taxoncl.deleteLater()
        self.child_taxoncl = []

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        taxoncl = xml_utils.xml_node('taxoncl')
        taxonrn = xml_utils.xml_node('taxonrn', text=self.ui.fgdc_taxonrn.text(),
                                    parent_node=taxoncl)
        taxonrv = xml_utils.xml_node('taxonrv', text=self.ui.fgdc_taxonrv.text(),
                                     parent_node=taxoncl)

        common_names = [c.text() for c in self.commons.get_widgets()]
        for common_name in common_names:
            if common_name:
                common = xml_utils.xml_node('common',
                                            text=common_name,
                                            parent_node=taxoncl)

        for child_taxoncl in self.child_taxoncl:
            taxoncl.append(child_taxoncl.to_xml())

        return taxoncl

    def from_xml(self, taxoncl):
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
            if taxoncl.tag == 'taxoncl':
                self.ui.fgdc_taxonrn.setText(taxoncl.xpath('taxonrn')[0].text)
                self.ui.fgdc_taxonrv.setText(taxoncl.xpath('taxonrv')[0].text)

                commons = xml_utils.search_xpath(taxoncl, 'common', only_first=False)
                if commons:
                    self.commons.clear_widgets(add_another=False)
                    for common in commons:
                        this_common = self.commons.add_another()
                        this_common.setText(common.text)

                children_taxoncl = taxoncl.xpath('taxoncl')
                for child_taxoncl in children_taxoncl:
                    child_widget = Taxoncl()
                    child_widget.from_xml(child_taxoncl)
                    self.ui.child_taxoncl.layout().addWidget(child_widget)
                    self.child_taxoncl.append(child_widget)
            else:
                print ("The tag is not a detailed")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Taxoncl,
                        "detailed testing")
