#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Metadata Date <timeperd> section
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
import os
from lxml import etree

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import data_io

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_taxoncl
from pymdwizard.gui.repeating_element import RepeatingElement

class Taxoncl(WizardWidget):  #

    drag_label = "taxon class <taxoncl>"
    acceptable_tags = ['abstract']

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

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'timeperd'
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element is not None and element.tag == 'taxoncl':
                e.accept()
        else:
            e.ignore()

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


    def _to_xml(self):
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
            taxoncl.append(child_taxoncl._to_xml())

        return taxoncl

    def _from_xml(self, taxoncl):
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
                    child_widget._from_xml(child_taxoncl)
                    self.ui.child_taxoncl.layout().addWidget(child_widget)
                    self.child_taxoncl.append(child_widget)
            else:
                print ("The tag is not a detailed")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Taxoncl,
                        "detailed testing")
