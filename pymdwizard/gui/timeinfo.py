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

from PyQt5.QtWidgets import QStackedWidget

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.ui_files import UI_timeinfo
from pymdwizard.gui.fgdc_date import FGDCDate


class Timeinfo(WizardWidget):  #

    drag_label = "Time Period information <timeinfo>"
    acceptable_tags = ['timeinfo']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_timeinfo.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.single_date = FGDCDate(label='    Single Date ', fgdc_name='fgdc_caldate')
        self.ui.fgdc_sngdate.layout().insertWidget(0, self.single_date)

        self.range_start_date = FGDCDate(label='Start  ', fgdc_name='fgdc_begdate')
        self.range_end_date = FGDCDate(label='End  ', fgdc_name='fgdc_enddate')
        self.ui.layout_daterange.addWidget(self.range_start_date)
        self.ui.layout_daterange.addWidget(self.range_end_date)

        date_widget_kwargs = {'show_format': False,
                              'label': 'Individual Date   ',
                              'fgdc_name': 'fgdc_caldate',
                              'parent_fgdc_name': 'fgdc_sngdate'}

        self.multi_dates = RepeatingElement(widget=FGDCDate,
                                            widget_kwargs=date_widget_kwargs)


        self.multi_dates.add_another()
        self.switch_primary()


    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions
        Returns
        -------
        None
        """
        self.ui.radio_single.toggled.connect(self.switch_primary)
        self.ui.radio_range.toggled.connect(self.switch_primary)
        self.ui.radio_multiple.toggled.connect(self.switch_primary)

    def switch_primary(self):
        """
        Switches form to reflect either organization or person primary
        Returns
        -------
        None
        """
        if self.ui.radio_single.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(0)
            self.ui.fgdc_sngdate.show()
            self.ui.fgdc_rngdates.hide()
            self.ui.fgdc_mdattim.hide()
            self.ui.fgdc_mdattim.layout().removeWidget(self.multi_dates)
        elif self.ui.radio_range.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(1)
            self.ui.fgdc_rngdates.hide()
            self.ui.fgdc_rngdates.show()
            self.ui.fgdc_mdattim.hide()
            self.ui.fgdc_mdattim.layout().removeWidget(self.multi_dates)
        elif self.ui.radio_multiple.isChecked():
            self.findChild(QStackedWidget, "fgdc_timeinfo").setCurrentIndex(2)
            self.ui.fgdc_sngdate.hide()
            self.ui.fgdc_rngdates.hide()
            self.ui.fgdc_mdattim.layout().addWidget(self.multi_dates)
            self.ui.fgdc_mdattim.show()

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeinfo element tag in xml tree
        """
        timeinfo = xml_utils.xml_node('timeinfo')

        cur_index = self.ui.fgdc_timeinfo.currentIndex()
        if cur_index == 0:
            sngdate = xml_utils.xml_node("sngdate", parent_node=timeinfo)
            caldate = xml_utils.xml_node('caldate', parent_node=sngdate,
                                         text=self.single_date.get_date())
        if cur_index == 1:
            rngdates = xml_utils.xml_node("rngdates", parent_node=timeinfo)
            begdate = xml_utils.xml_node("begdate", parent_node=rngdates,
                                         text=self.range_start_date.get_date())
            enddate = xml_utils.xml_node("enddate", parent_node=rngdates,
                                         text=self.range_end_date.get_date())
        if cur_index == 2:
            mdattim = xml_utils.xml_node("mdattim", parent_node=timeinfo)

            for single_date in self.multi_dates.get_widgets():

                single_date_node = xml_utils.xml_node("sngdate", parent_node=mdattim)

                caldate =  xml_utils.xml_node('caldate', parent_node=single_date_node,
                                                      text=single_date.get_date())

        return timeinfo

    def from_xml(self, timeinfo):
        """
        parses the xml code into the relevant timeinfo elements
        Parameters
        ----------
        metadata_date - the xml element timeinfo and its contents
        Returns
        -------
        None
        """
        try:
            if timeinfo.tag == 'timeinfo':
                timeinfo_stack = self.ui.fgdc_timeinfo
                if timeinfo.xpath("rngdates"):
                    self.ui.radio_range.setChecked(True)
                    timeinfo_stack.setCurrentIndex(1)

                    begdate = timeinfo.findtext("rngdates/begdate")
                    self.range_start_date.set_date(begdate)

                    enddate = timeinfo.findtext("rngdates/enddate")
                    self.range_end_date.set_date(enddate)

                elif timeinfo.xpath("mdattim"):
                    self.ui.radio_multiple.setChecked(True)
                    timeinfo_stack.setCurrentIndex(2)

                    self.multi_dates.clear_widgets(add_another=False)
                    for caldate in timeinfo.xpath('mdattim/sngdate/caldate'):
                        date_widget = self.multi_dates.add_another()
                        date_widget.set_date(caldate.text)

                elif timeinfo.xpath("sngdate"):
                    self.ui.radio_single.setChecked(True)
                    timeinfo_stack.setCurrentIndex(0)

                    sngdate = timeinfo.findtext("sngdate/caldate")
                    self.single_date.set_date(sngdate)
                else:
                    pass
            elif timeinfo.tag == 'timeperd':
                try:
                    self.parent.from_xml(timeinfo)
                except:
                    pass

            else:
                print ("The tag is not timeinfo")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Timeinfo,
                        "Metadata Date testing")

