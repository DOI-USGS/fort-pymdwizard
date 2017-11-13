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
from pymdwizard.gui.ui_files import UI_DataQuality
from pymdwizard.gui.AttributeAccuracy import AttributeAccuracy
from pymdwizard.gui.LogicalAccuracy import LogicalAccuracy
from pymdwizard.gui.Completeness import Completeness
from pymdwizard.gui.PositionalAccuracy import PositionalAccuracy
from pymdwizard.gui.sourceinput import SourceInput
from pymdwizard.gui.procstep import ProcStep



class DataQuality(WizardWidget):

    drag_label = "Data Quality <dataqual>"
    acceptable_tags = ['dataqual']

    ui_class = UI_DataQuality.Ui_fgdc_dataqual

    def build_ui(self):

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        self.attraccr = AttributeAccuracy(parent=self)
        self.logic = LogicalAccuracy(parent=self)
        # self.complete = Completeness(parent=self)
        self.complete = Completeness(parent=self)
        self.posacc = PositionalAccuracy(parent=self)
        self.sourceinput = SourceInput(parent=self)
        self.procstep = ProcStep(parent=self)


        self.ui.two_column_left.layout().addWidget(self.attraccr)
        self.ui.two_column_left.layout().addWidget(self.logic)
        self.ui.two_column_left.layout().addWidget(self.complete)
        self.ui.two_column_left.layout().addWidget(self.posacc)

        self.ui.bottom_layout.layout().addWidget(self.sourceinput)
        self.ui.fgdc_lineage.layout().addWidget(self.procstep)
        self.scroll_area = self.ui.idinfo_scroll_area

    def clear_widget(self):
        self.sourceinput.clear_widget()
        WizardWidget.clear_widget(self)
        self.complete.ui.fgdc_complete.sizeChange()

    def to_xml(self):
        # add code here to translate the form into xml representation
        dataqual_node = xml_utils.xml_node(tag='dataqual')

        attraccr_node = self.attraccr.to_xml()
        dataqual_node.append(attraccr_node)

        logic_node = self.logic.to_xml()
        dataqual_node.append(logic_node)

        complete_node = self.complete.to_xml()
        dataqual_node.append(complete_node)

        if self.posacc.has_content():
            posacc_node = self.posacc.to_xml()
            dataqual_node.append(posacc_node)

        if self.sourceinput.has_content():
            srcinfo_node = self.sourceinput.to_xml()

        procstep_node = self.procstep.to_xml()
        procstep_children = procstep_node.getchildren()

        for i in procstep_children:
            srcinfo_node.append(i)

        if self.original_xml is not None:
            methods = xml_utils.search_xpath(self.original_xml,
                                             'lineage/method', only_first=False)
            for i, method in enumerate(methods):
                method.tail = None
                srcinfo_node.insert(i, deepcopy(method))

        dataqual_node.append(srcinfo_node)

        if self.original_xml is not None:
            cloud = xml_utils.search_xpath(self.original_xml, 'cloud')
            if cloud is not None:
                cloud.tail = None
                dataqual_node.append(deepcopy(cloud))

        return dataqual_node

    def from_xml(self, xml_dataqual):

        self.original_xml = xml_dataqual

        try:
            attraccr = xml_dataqual.xpath('attracc')[0]
            self.attraccr.from_xml(attraccr)
        except IndexError:
            pass

        try:
            logic = xml_dataqual.xpath('logic')[0]
            self.logic.from_xml(logic)
        except IndexError:
            pass

        try:
            complete = xml_dataqual.xpath('complete')[0]
            self.complete.from_xml(complete)
        except IndexError:
            pass

        try:
            posacc = xml_dataqual.xpath('posacc')[0]
            self.posacc.from_xml(posacc)
        except IndexError:
            pass

        try:
            sourceinput = xml_dataqual.xpath('lineage')[0]
            self.sourceinput.from_xml(sourceinput)
        except IndexError:
            pass

        try:
            procstep = xml_dataqual.xpath('lineage')[0]
            self.procstep.from_xml(procstep)
        except IndexError:
            pass


if __name__ == "__main__":
    utils.launch_widget(DataQuality, "DataQual testing")