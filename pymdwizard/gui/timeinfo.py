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

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QStackedWidget
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.ui_files import UI_timeinfo
    from pymdwizard.gui.fgdc_date import FGDCDate
except ImportError as err:
    raise ImportError(err, __file__)


class Timeinfo(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <timeinfo> tag, which
        contains detailed information about the time period (or periods)
        represented by the data. It allows for single date, date range,
        or multiple individual dates.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Manages three primary display modes using radio buttons and a
           "QStackedWidget": single date, date range, and multiple dates.
        2. Embeds "FGDCDate" widgets for date inputs.
        3. Uses "RepeatingElement" to handle the list of multiple dates.

    Notes:
        Inherits from "WizardWidget". The date input widgets ("FGDCDate")
        are assumed to handle date formatting and output.
    """

    # Class attributes.
    drag_label = "Time Period information <timeinfo>"
    acceptable_tags = ["timeinfo"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding child date widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, creates "FGDCDate" instances for single/range
            dates, sets up the "RepeatingElement" for multiple dates,
            and calls "switch_primary" to set the initial view.

        Notes:
            None
        """

        self.ui = UI_timeinfo.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # --- Setup Single Date Input ---
        self.single_date = FGDCDate(label="    Single Date ",
                                    fgdc_name="fgdc_caldate")
        self.ui.fgdc_sngdate.layout().insertWidget(0, self.single_date)

        # --- Setup Date Range Inputs ---
        self.range_start_date = FGDCDate(label="Start  ",
                                         fgdc_name="fgdc_begdate")
        self.range_end_date = FGDCDate(label="End  ",
                                       fgdc_name="fgdc_enddate")
        self.ui.layout_daterange.addWidget(self.range_start_date)
        self.ui.layout_daterange.addWidget(self.range_end_date)

        # --- Setup Multiple Dates Input (RepeatingElement) ---
        date_widget_kwargs = {
            "show_format": False,
            "label": "Individual Date   ",
            "fgdc_name": "fgdc_caldate",
            "parent_fgdc_name": "fgdc_sngdate",
        }

        self.multi_dates = RepeatingElement(
            widget=FGDCDate, widget_kwargs=date_widget_kwargs
        )

        # Add initial date widgets for the multiple dates view.
        self.multi_dates.add_another()
        self.multi_dates.add_another()

        # Set the initial primary view mode.
        self.switch_primary()

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects the three radio buttons to the "switch_primary"
            method to update the view.

        Notes:
            None
        """

        # Connect radio buttons to the view switching method.
        self.ui.radio_single.toggled.connect(self.switch_primary)
        self.ui.radio_range.toggled.connect(self.switch_primary)
        self.ui.radio_multiple.toggled.connect(self.switch_primary)

    def switch_primary(self):
        """
        Description:
            Updates the "QStackedWidget" to display the content
            corresponding to the checked radio button (single, range,
            or multiple dates).

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Determines the checked radio button and sets the index of
            the stacked widget, showing/hiding relevant content.

        Notes:
            The "multi_dates" widget must be added/removed from the
            layout in the multiple-dates case to ensure proper display.
        """

        timeinfo_stack = self.findChild(QStackedWidget, "fgdc_timeinfo")

        if self.ui.radio_single.isChecked():
            # Switch to Single Date view (index 0).
            timeinfo_stack.setCurrentIndex(0)
            self.ui.fgdc_sngdate.show()
            self.ui.fgdc_rngdates.hide()
            self.ui.fgdc_mdattim.hide()
            # Ensure multi_dates is removed from layout.
            self.ui.fgdc_mdattim.layout().removeWidget(self.multi_dates)

        elif self.ui.radio_range.isChecked():
            # Switch to Date Range view (index 1).
            timeinfo_stack.setCurrentIndex(1)
            self.ui.fgdc_rngdates.hide()
            self.ui.fgdc_rngdates.show()
            self.ui.fgdc_mdattim.hide()
            # Ensure multi_dates is removed from layout
            self.ui.fgdc_mdattim.layout().removeWidget(self.multi_dates)

        elif self.ui.radio_multiple.isChecked():
            # Switch to Multiple Dates view (index 2).
            timeinfo_stack.setCurrentIndex(2)
            self.ui.fgdc_sngdate.hide()
            self.ui.fgdc_rngdates.hide()
            # Add multi_dates to the layout
            self.ui.fgdc_mdattim.layout().addWidget(self.multi_dates)
            self.ui.fgdc_mdattim.show()

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <timeinfo> XML
            element based on the currently selected time period type.

        Passed arguments:
            None

        Returned objects:
            timeinfo (lxml.etree._Element): The <timeinfo> element
                tag in the XML tree.

        Workflow:
            1. Determines the active time mode via "currentIndex".
            2. Creates and populates the corresponding XML structure
               (<sngdate>, <rngdates>, or <mdattim>).

        Notes:
            Uses FGDCDate.get_date() to retrieve formatted date strings.
        """

        # Create the root <timeinfo> node.
        timeinfo = xml_utils.xml_node("timeinfo")

        cur_index = self.ui.fgdc_timeinfo.currentIndex()

        if cur_index == 0:
            # Single Date (<sngdate>).
            sngdate = xml_utils.xml_node("sngdate", parent_node=timeinfo)
            xml_utils.xml_node(
                "caldate",
                parent_node=sngdate,
                text=self.single_date.get_date(),
            )

        elif cur_index == 1:
            # Date Range (<rngdates>).
            rngdates = xml_utils.xml_node("rngdates", parent_node=timeinfo)
            xml_utils.xml_node(
                "begdate",
                parent_node=rngdates,
                text=self.range_start_date.get_date(),
            )
            xml_utils.xml_node(
                "enddate",
                parent_node=rngdates,
                text=self.range_end_date.get_date(),
            )

        elif cur_index == 2:
            # Multiple Dates (<mdattim>).
            mdattim = xml_utils.xml_node("mdattim", parent_node=timeinfo)

            for single_date in self.multi_dates.get_widgets():
                single_date_node = xml_utils.xml_node(
                    "sngdate", parent_node=mdattim
                )

                xml_utils.xml_node(
                    "caldate",
                    parent_node=single_date_node,
                    text=single_date.get_date(),
                )

        return timeinfo

    def from_xml(self, timeinfo):
        """
        Description:
            Parses an XML element and populates the widget fields,
            setting the correct primary mode (single, range, or multiple).

        Passed arguments:
            timeinfo (lxml.etree._Element): The XML element, expected
                to be <timeinfo> or <timeperd>.

        Returned objects:
            None

        Workflow:
            1. Checks for <rngdates>, <mdattim>, or <sngdate> to
               determine the time mode.
            2. Sets the appropriate radio button and stacked widget index.
            3. Populates date fields using FGDCDate.set_date().
            4. Recursively calls "from_xml" if the tag is <timeperd>.

        Notes:
            None
        """

        try:
            if timeinfo.tag == "timeinfo":
                timeinfo_stack = self.ui.fgdc_timeinfo

                # Check for Date Range (<rngdates>).
                if timeinfo.xpath("rngdates"):
                    self.ui.radio_range.setChecked(True)
                    timeinfo_stack.setCurrentIndex(1)

                    begdate = timeinfo.findtext("rngdates/begdate")
                    self.range_start_date.set_date(begdate)

                    enddate = timeinfo.findtext("rngdates/enddate")
                    self.range_end_date.set_date(enddate)

                # Check for Multiple Dates (<mdattim>).
                elif timeinfo.xpath("mdattim"):
                    self.ui.radio_multiple.setChecked(True)
                    timeinfo_stack.setCurrentIndex(2)

                    self.multi_dates.clear_widgets(add_another=False)
                    for caldate in timeinfo.xpath("mdattim/sngdate/caldate"):
                        date_widget = self.multi_dates.add_another()
                        date_widget.set_date(caldate.text)

                # Check for Single Date (<sngdate>).
                elif timeinfo.xpath("sngdate"):
                    self.ui.radio_single.setChecked(True)
                    timeinfo_stack.setCurrentIndex(0)

                    sngdate = timeinfo.findtext("sngdate/caldate")
                    self.single_date.set_date(sngdate)
                else:
                    pass
            elif timeinfo.tag == "timeperd":
                # Handle parent element <timeperd> by recursing to parent.
                try:
                    self.parent.from_xml(timeinfo)
                except:
                    pass
            else:
                print("The tag is not timeinfo")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Timeinfo, "Metadata Date testing")
