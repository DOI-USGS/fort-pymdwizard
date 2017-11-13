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

from PyQt5.QtWidgets import QHBoxLayout

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_IdInfo
from pymdwizard.gui.PointOfContact import ContactInfoPointOfContact
from pymdwizard.gui.Taxonomy import Taxonomy
from pymdwizard.gui.Keywords import Keywords
from pymdwizard.gui.accconst import Accconst
from pymdwizard.gui.useconst import Useconst
from pymdwizard.gui.Status import Status
from pymdwizard.gui.timeperd import Timeperd
from pymdwizard.gui.citeinfo import Citeinfo
from pymdwizard.gui.datacred import Datacred
from pymdwizard.gui.descript import Descript
from pymdwizard.gui.supplinf import SupplInf
from pymdwizard.gui.native import Native
from pymdwizard.gui.purpose import Purpose
from pymdwizard.gui.crossref_list import Crossref_list


class IdInfo(WizardWidget):

    drag_label = "Identification Information <idinfo>"
    acceptable_tags = ['idinfo']

    ui_class = UI_IdInfo.Ui_fgdc_idinfo

    def __init__(self, root_widget=None, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        self.schema = 'bdp'
        self.root_widget = root_widget
        self.scroll_area = self.ui.idinfo_scroll_area

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.ptcontac = ContactInfoPointOfContact(parent=self)
        self.taxonomy = Taxonomy(parent=self)
        self.keywords = Keywords(parent=self)
        self.accconst = Accconst(parent=self)
        self.useconst = Useconst(parent=self)
        self.status = Status(parent=self)
        self.timeperd = Timeperd(parent=self)
        self.citation = Citeinfo(parent=self)
        self.citation.ui.btn_import_doi.hide()
        self.datacredit = Datacred(parent=self)

        self.descript = Descript(parent=self)

        self.purpose = Purpose(parent=self)
        self.supplinf = SupplInf(parent=self)
        self.native = Native(parent=self)

        self.ui.fgdc_citation.layout().addWidget(self.citation)

        #bottom to top in layout
        time_hbox = QHBoxLayout()
        time_hbox.addWidget(self.status)
        time_hbox.addWidget(self.timeperd)
        self.ui.two_column_left.layout().insertWidget(0, self.native)
        self.ui.two_column_left.layout().insertLayout(0, time_hbox)
        self.ui.two_column_left.layout().insertWidget(0, self.datacredit)
        self.ui.two_column_left.layout().insertWidget(0, self.taxonomy)
        self.ui.two_column_left.layout().insertWidget(0, self.ptcontac)
        self.ui.two_column_left.layout().insertWidget(0, self.useconst)
        self.ui.two_column_left.layout().insertWidget(0, self.accconst)


        self.ui.two_column_right.layout().insertWidget(0, self.supplinf)
        self.ui.two_column_right.layout().insertWidget(0, self.keywords)
        self.ui.two_column_right.layout().insertWidget(0, self.purpose)
        self.ui.two_column_right.layout().insertWidget(0, self.descript)

        self.crossref_list = Crossref_list()
        self.ui.help_crossref.layout().addWidget(self.crossref_list)

    def children(self):
        return super(IdInfo, self).children() + [self.root_widget.spatial_tab.spdom]

    def switch_schema(self, schema):
        self.schema = schema
        if schema == 'bdp':
            self.taxonomy.show()
        else:
            self.taxonomy.hide()

    def clear_widget(self):
        self.root_widget.spatial_tab.spdom.clear_widget()
        self.taxonomy.clear_widget()
        self.taxonomy.ui.rbtn_no.setChecked(True)
        WizardWidget.clear_widget(self)

    def to_xml(self):
        # add code here to translate the form into xml representation
        idinfo_node = xml_utils.xml_node('idinfo')

        citation_node = xml_utils.xml_node('citation', parent_node=idinfo_node)
        citeinfo_node = self.citation.to_xml()
        citation_node.append(citeinfo_node)
        idinfo_node.append(citation_node)

        descript_node = xml_utils.xml_node('descript', parent_node=idinfo_node)
        abstract_node = self.descript.to_xml()
        descript_node.append(abstract_node)
        purpose_node = self.purpose.to_xml()
        descript_node.append(purpose_node)
        supplinf_node = self.supplinf.to_xml()
        if supplinf_node.text is not None:
            descript_node.append(supplinf_node)

        idinfo_node.append(descript_node)

        timeperd_node = self.timeperd.to_xml()
        idinfo_node.append(timeperd_node)

        status_node = self.status.to_xml()
        idinfo_node.append(status_node)

        if self.root_widget.use_spatial:
            spdom_node = self.root_widget.spatial_tab.spdom.to_xml()
            idinfo_node.append(spdom_node)

        keywords = self.keywords.to_xml()
        idinfo_node.append(keywords)

        if self.schema == 'bdp' and self.taxonomy.has_content():
            taxonomy = self.taxonomy.to_xml()
            idinfo_node.append(taxonomy)

        accconst_node = self.accconst.to_xml()
        idinfo_node.append(accconst_node)

        useconst_node = self.useconst.to_xml()
        idinfo_node.append(useconst_node)

        if self.ptcontac.has_content():
            ptcontac = self.ptcontac.to_xml()
            idinfo_node.append(ptcontac)

        if self.original_xml is not None:
            browse = xml_utils.search_xpath(self.original_xml, 'browse')
            if browse is not None:
                browse.tail = None
                idinfo_node.append(deepcopy(browse))

        datacredit_node = self.datacredit.to_xml()
        if datacredit_node.text:
            idinfo_node.append(datacredit_node)

        if self.original_xml is not None:
            secinfo = xml_utils.search_xpath(self.original_xml, 'secinfo')
            if secinfo is not None:
                secinfo.tail = None
                idinfo_node.append(deepcopy(secinfo))

        if self.native.has_content():
            idinfo_node.append(self.native.to_xml())

        if self.crossref_list.has_content():
            for crossref in self.crossref_list.get_children():
                idinfo_node.append(crossref.to_xml())

        if self.original_xml is not None:
            tools = xml_utils.search_xpath(self.original_xml, 'tool',
                                           only_first=False)
            for tool in tools:
                tool.tail = None
                idinfo_node.append(deepcopy(tool))

        return idinfo_node

    def from_xml(self, xml_idinfo):

        self.original_xml = xml_idinfo

        citation = xml_utils.search_xpath(xml_idinfo, 'citation')
        if citation is not None:
            self.citation.from_xml(citation)

        abstract = xml_utils.search_xpath(xml_idinfo, 'descript/abstract')
        if abstract is not None:
            self.descript.from_xml(abstract)

        purpose = xml_utils.search_xpath(xml_idinfo, 'descript/purpose')
        if purpose is not None:
            self.purpose.from_xml(purpose)

        supplinf = xml_utils.search_xpath(xml_idinfo, 'descript/supplinf')
        if supplinf is not None:
            self.supplinf.from_xml(supplinf)

        timeperd = xml_utils.search_xpath(xml_idinfo, 'timeperd')
        if timeperd is not None:
            self.timeperd.from_xml(timeperd)

        status = xml_utils.search_xpath(xml_idinfo, 'status')
        if status is not None:
            self.status.from_xml(status)

        spdom = xml_utils.search_xpath(xml_idinfo, 'spdom')
        if spdom is not None:
            self.root_widget.spatial_tab.spdom.from_xml(spdom)

        keywords = xml_utils.search_xpath(xml_idinfo, 'keywords')
        if keywords is not None:
            self.keywords.from_xml(keywords)

        taxonomy = xml_utils.search_xpath(xml_idinfo, 'taxonomy')
        if taxonomy is not None:
            self.taxonomy.from_xml(taxonomy)

        accconst = xml_utils.search_xpath(xml_idinfo, 'accconst')
        if accconst is not None:
            self.accconst.from_xml(accconst)

        useconst =xml_utils.search_xpath(xml_idinfo, 'useconst')
        if useconst is not None:
            self.useconst.from_xml(useconst)

        ptcontac = xml_utils.search_xpath(xml_idinfo, 'ptcontac')
        if ptcontac is not None:
            self.ptcontac.from_xml(ptcontac)

        datacred = xml_utils.search_xpath(xml_idinfo, 'datacred')
        if datacred is not None:
            self.datacredit.from_xml(datacred)

        native = xml_utils.search_xpath(xml_idinfo, 'native')
        if native is not None:
            self.native.from_xml(native)

        crossref = xml_utils.search_xpath(xml_idinfo, 'crossref')
        if crossref is not None:
            self.crossref_list.from_xml(xml_idinfo)


if __name__ == "__main__":
    utils.launch_widget(IdInfo, "IdInfo testing")
