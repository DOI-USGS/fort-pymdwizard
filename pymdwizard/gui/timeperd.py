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
    from PyQt5.QtWidgets import QComboBox
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_timeperd
    from pymdwizard.gui import timeinfo
except ImportError as err:
    raise ImportError(err, __file__)


class Timeperd(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <timeperd> tag, which
        serves as a container for detailed time information (<timeinfo>)
        and the update status (<current>) of the data.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds the "Timeinfo" widget to manage the period start/end
           or list of dates.
        2. Manages a "QComboBox" for the <current> status (e.g.,
           "ground condition", "live data", "historical archive").

    Notes:
        Inherits from "WizardWidget". Relies on the child "Timeinfo"
        widget for complex date handling.
    """

    # Class attributes.
    drag_label = "Time Period of Content <timeperd>"
    acceptable_tags = ["timeperd"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding the "Timeinfo" child widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, creates an instance of "Timeinfo", and
            adds it to the main layout.

        Notes:
            None
        """

        self.ui = UI_timeperd.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Embed Timeinfo widget for date/time details.
        self.timeinfo = timeinfo.Timeinfo(parent=self)
        self.ui.fgdc_timeperd.layout().insertWidget(0, self.timeinfo)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <timeperd> XML
            element, including the child <timeinfo> and <current>.

        Passed arguments:
            None

        Returned objects:
            timeperd (lxml.etree._Element): The <timeperd> element
                tag in the XML tree.

        Workflow:
            1. Creates <timeperd> node.
            2. Appends XML from "self.timeinfo".
            3. Appends the <current> status from the combo box.

        Notes:
            None
        """

        # Create the root <timeperd> node.
        timeperd = xml_utils.xml_node("timeperd")

        # Get XML from the child Timeinfo widget.
        timeinfo = self.timeinfo.to_xml()

        # Append the <timeinfo> XML to <timeperd>.
        timeperd.append(timeinfo)

        # Add the <current> status from the QComboBox.
        xml_utils.xml_node(
            "current",
            parent_node=timeperd,
            text=self.ui.fgdc_current.currentText(),
        )

        return timeperd

    def from_xml(self, timeperd):
        """
        Description:
            Parses an XML element and populates the widget fields and
            child widget.

        Passed arguments:
            timeperd (lxml.etree._Element): The XML element, expected
                to be <timeperd>.

        Returned objects:
            None

        Workflow:
            1. Extracts and sets the <current> text into the QComboBox.
            2. Calls self.timeinfo.from_xml to populate the date fields.

        Notes:
            None
        """

        try:
            if timeperd.tag == "timeperd":

                # Populate the <current> status QComboBox.
                if timeperd.findall("current"):
                    current_text = timeperd.findtext("current")
                    current_box = self.findChild(QComboBox,
                                                 "fgdc_current")
                    current_box.setCurrentText(current_text)

                # Populate the child Timeinfo widget.
                if timeperd.findall("timeinfo"):
                    self.timeinfo.from_xml(timeperd.xpath("timeinfo")[0])

            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not timeperd")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Timeperd, "Metadata Date testing")
