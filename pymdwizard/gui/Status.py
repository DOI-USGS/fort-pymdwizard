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
    from pymdwizard.gui.ui_files import UI_Status
except ImportError as err:
    raise ImportError(err, __file__)

class Status(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <status> tag, which describes
        the state and update frequency of a metadata record or dataset.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Manages two "QComboBox" elements for progress and update
           frequency.
        2. Handles XML serialization/deserialization for the <status>
           tag and its children (<progress> and <update>).

    Notes:
        Inherits from "WizardWidget".
    """

    # Class attributes.
    drag_label = "Status <status>"
    acceptable_tags = ["status"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI and sets up drag-and-drop.

        Notes:
            None
        """

        self.ui = UI_Status.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

    def to_xml(self):
        """
        Description:
            Converts the two comboboxes' text into two separate element
            tags (<progress> and <update>) encapsulated by a <status> tag.

        Passed arguments:
            None

        Returned objects:
            status (lxml.etree._Element): The <status> element tag in the
                XML tree.

        Workflow:
            1. Creates <status> node.
            2. Finds values from "fgdc_progress" and "fgdc_update".
            3. Creates and appends <progress> and <update> children.

        Notes:
            None
        """

        # Create the root <status> node.
        status = xml_utils.xml_node(tag="status")

        # --- Progress ---
        progress_text = self.findChild(QComboBox,
                                       "fgdc_progress").currentText()
        xml_utils.xml_node(
            tag="progress",
            text=progress_text,
            parent_node=status,
        )

        # --- Update Frequency ---
        update_text = self.findChild(QComboBox,
                                     "fgdc_update").currentText()
        update = xml_utils.xml_node(
            tag="update",
            text=update_text,
            parent_node=status,
        )

        # Append update node to the status node (progress is already appended
        # via parent_node argument)
        status.append(update)
        return status

    def from_xml(self, status):
        """
        Description:
            Parses an XML element and populates the relevant status
            comboboxes.

        Passed arguments:
            status (lxml.etree._Element): The XML element, expected to
                be <status>.

        Returned objects:
            None

        Workflow:
            1. Checks for the <status> tag.
            2. Extracts text content from <progress> and <update>.
            3. Sets the extracted text as the current value for the
               corresponding "QComboBox" widgets.

        Notes:
            None
        """

        try:
            # Populate Progress QComboBox.
            if status.tag == "status":
                progress_box = self.findChild(QComboBox,
                                              "fgdc_progress")
                progress_text = status.find("progress").text
                progress_box.setCurrentText(progress_text)

                # Populate Update QComboBox.
                update_box = self.findChild(QComboBox,
                                            "fgdc_update")
                update_text = status.find("update").text
                update_box.setCurrentText(update_text)
            else:
                # Print statement for debugging/logging purposes.
                print("The tag is not status")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Status, "Status testing")
