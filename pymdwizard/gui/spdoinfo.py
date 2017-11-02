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

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_spdoinfo



class SpdoInfo(WizardWidget):

    drag_label = "Spatial Domain Info <spdoinfo>"
    acceptable_tags = ['spdoinfo']

    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_spdoinfo.Ui_spatial_domain_widget()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)
        self.clear_widget()

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """
        self.ui.rbtn_yes.toggled.connect(self.spdoinfo_used_change)
        self.ui.fgdc_direct.currentIndexChanged.connect(self.change_type)

    def spdoinfo_used_change(self, b):
        if b:
            self.ui.content_widget.show()
        else:
            self.ui.content_widget.hide()

    def change_type(self):
        if self.ui.fgdc_direct.currentText() == 'Raster':
            self.ui.vector_or_raster.setCurrentIndex(1)
        else:
            self.ui.vector_or_raster.setCurrentIndex(0)

    def has_content(self):
        """
        Returns if the widget contains legitimate content that should be
        written out to xml

        By default this is always true but should be implement in each
        subclass with logic to check based on contents

        Returns
        -------
        bool : True if there is content, False if no
        """
        return self.ui.rbtn_yes.isChecked()

    def clear_widget(self):
        """
        Clears all content from this widget

        Returns
        -------
        None
        """
        self.ui.fgdc_rowcount.setText('')
        self.ui.fgdc_colcount.setText('')
        self.ui.fgdc_vrtcount.setText('')
        self.ui.fgdc_ptvctcnt.setText('')

        self.ui.fgdc_sdtstype.setCurrentIndex(0)
        self.ui.fgdc_rasttype.setCurrentIndex(0)
        self.ui.fgdc_direct.setCurrentIndex(2)

        self.ui.rbtn_no.setChecked(True)
        self.spdoinfo_used_change(False)

    def to_xml(self):
        if self.ui.rbtn_yes.isChecked():
            spdoinfo = xml_utils.xml_node('spdoinfo')

            if self.original_xml is not None:
                indspref = xml_utils.search_xpath(self.original_xml, 'indspref')
                if indspref is not None:
                    indspref.tail = None
                    spdoinfo.append(deepcopy(indspref))


            direct = xml_utils.xml_node('direct', text=self.ui.fgdc_direct.currentText(),
                                        parent_node=spdoinfo)
            if self.ui.fgdc_direct.currentText() == 'Raster':
                rasttype = self.ui.fgdc_rasttype.currentText()
                if rasttype:
                    rastinfo = xml_utils.xml_node('rastinfo', parent_node=spdoinfo)
                    rasttype = xml_utils.xml_node('rasttype', text=rasttype, parent_node=rastinfo)

                    rowcount_str = self.ui.fgdc_rowcount.text()
                    colcount_str = self.ui.fgdc_colcount.text()
                    vrtcount_str = self.ui.fgdc_vrtcount.text()

                    if rowcount_str or colcount_str:
                        rowcount = xml_utils.xml_node('rowcount', text=rowcount_str,
                                                      parent_node=rastinfo)
                        colcount = xml_utils.xml_node('colcount', text=colcount_str,
                                                      parent_node=rastinfo)
                        if vrtcount_str:
                            vrtcount = xml_utils.xml_node('vrtcount', text=vrtcount_str,
                                                      parent_node=rastinfo)
            else:
                sdtstype = self.ui.fgdc_sdtstype.currentText()
                ptvctcnt = self.ui.fgdc_ptvctcnt.text()

                if sdtstype or ptvctcnt:
                    ptvctinf = xml_utils.xml_node('ptvctinf', parent_node=spdoinfo)
                    sdtsterm = xml_utils.xml_node('sdtsterm', parent_node=ptvctinf)
                    sdtstype = xml_utils.xml_node('sdtstype', text=sdtstype, parent_node=sdtsterm)

                    ptvctcnt_str = self.ui.fgdc_ptvctcnt.text()
                    if ptvctcnt_str:
                        sdtsterm = xml_utils.xml_node('ptvctcnt', text = ptvctcnt_str, parent_node=sdtsterm)
        else:
            spdoinfo = None

        return spdoinfo

    def from_xml(self, spdoinfo):

        self.clear_widget()
        if spdoinfo.tag == 'spdoinfo':
            self.original_xml = spdoinfo

            self.ui.rbtn_yes.setChecked(True)

            direct = xml_utils.get_text_content(spdoinfo, 'direct')
            if direct is not None:
                if 'raster' in direct.lower():
                    self.ui.fgdc_direct.setCurrentIndex(0)
                    self.ui.fgdc_direct.setCurrentIndex(2)
                elif 'point' in direct.lower():
                    self.ui.fgdc_direct.setCurrentIndex(2)
                    self.ui.fgdc_direct.setCurrentIndex(0)
                elif 'vector' in direct.lower():
                    self.ui.fgdc_direct.setCurrentIndex(0)
                    self.ui.fgdc_direct.setCurrentIndex(1)

            rasttype = xml_utils.get_text_content(spdoinfo, 'rastinfo/rastype')
            if rasttype is not None:
                self.ui.fgdc_rasttype.setCurrentText(rasttype)

            sdtstype = xml_utils.get_text_content(spdoinfo, 'ptvctinf/sdtsterm/sdtstype')
            if sdtstype is not None:
                self.ui.fgdc_sdtstype.setCurrentText(sdtstype)

            ptvctcnt = xml_utils.get_text_content(spdoinfo, 'ptvctinf/sdtsterm/ptvctcnt')
            if ptvctcnt is not None:
                self.ui.fgdc_ptvctcnt.setText(ptvctcnt)

            rasttype = xml_utils.get_text_content(spdoinfo, 'rastinfo/rasttype')
            if rasttype is not None:
                self.ui.fgdc_rasttype.setCurrentText(rasttype)

            rowcount = xml_utils.get_text_content(spdoinfo, 'rastinfo/rowcount')
            if rowcount is not None:
                self.ui.fgdc_rowcount.setText(rowcount)

            colcount = xml_utils.get_text_content(spdoinfo, 'rastinfo/colcount')
            if colcount is not None:
                self.ui.fgdc_colcount.setText(colcount)

            vrtcount = xml_utils.get_text_content(spdoinfo, 'rastinfo/vrtcount')
            if vrtcount is not None:
                self.ui.fgdc_vrtcount.setText(vrtcount)

if __name__ == "__main__":
    utils.launch_widget(SpdoInfo,
                        "Spatial Domain Information")







