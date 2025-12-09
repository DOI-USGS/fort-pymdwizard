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
    from PyQt5.QtCore import QSize
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_proccont
    from pymdwizard.gui import ContactInfo
except ImportError as err:
    raise ImportError(err, __file__)


class ProcessContact(WizardWidget):
    """
    Description:
        A specialized widget for the FGDC <proccont> (Process Contact)
        tag. It wraps a ContactInfo widget and provides the logic to
        control its visibility based on a 'Yes/No' radio button.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds the generic "ContactInfo" widget.
        2. Manages the widget's collapsed/expanded state.
        3. Allows conditional XML serialization based on the "Yes/No"
           selection.

    Notes:
        Inherits from "WizardWidget". Provides a dynamic UI size change.
    """

    # Class attributes for defining widget sizes.
    WIDGET_WIDTH = 500
    COLLAPSED_HEIGHT = 75

    # Calculate expanded height based on internal widget size.
    EXPANDED_HEIGHT = 310 + COLLAPSED_HEIGHT
    drag_label = "Process Contact <proccont>"
    acceptable_tags = ["proccont", "cntinfo"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            and initializes the embedded ContactInfo widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Initializes the UI and drag-and-drop setup.
            2. Create and embed the "ContactInfo" child widget.
            3. Set the initial size to the collapsed state.
            4. Set the widget's object name to "ptcontac" (for internal
               compatibility/reuse).

        Notes:
            None
        """

        self.ui = UI_proccont.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        # Initialize and embed the ContactInfo child widget.
        self.cntinfo = ContactInfo.ContactInfo()
        self.ui.main_layout.addWidget(self.cntinfo)

        # Define QSize objects for the collapsed and expanded states.
        self.collaped_size = QSize(self.WIDGET_WIDTH,
                                   self.COLLAPSED_HEIGHT)
        self.expanded_size = QSize(self.WIDGET_WIDTH,
                                   self.EXPANDED_HEIGHT)

        # Set the initial size to collapsed.
        self.resize(self.collaped_size)

        # Set the object name (often reused from ptcontac).
        self.setObjectName("ptcontac")

    def connect_events(self):
        """
        Description:
            Connects the "Yes/No" radio button toggled signal to the
            "contact_used_change" handler.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects "rbtn_yes.toggled" to self.contact_used_change.

        Notes:
            None
        """

        # Connect the radio button signal to the visibility handler.
        self.ui.rbtn_yes.toggled.connect(self.contact_used_change)

    def contact_used_change(self, b):
        """
        Description:
            Shows or hides the embedded ContactInfo widget based on the
            state of the "Yes/No" radio button.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Calls cntinfo.show() if True, or cntinfo.hide() if False.

        Notes:
            None
        """

        if b:
            # Show the contact information section.
            self.cntinfo.show()
        else:
            # Hide the contact information section.
            self.cntinfo.hide()

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <proccont> XML
            element. Returns None if the contact is not used.

        Passed arguments:
            None

        Returned objects:
            proccont (lxml.etree._Element or None): The <proccont>
                element or None.

        Workflow:
            1. Checks "rbtn_yes".
            2. If checked, creates <proccont> and appends the XML
               from the "cntinfo" child widget.
            3. If not checked, sets the 'No' radio button and returns None.

        Notes:
            None
        """

        if self.ui.rbtn_yes.isChecked():
            # Create the <proccont> node.
            proccont = xml_utils.xml_node(tag="proccont")

            # Get and append the child <cntinfo> XML.
            cntinfo = self.cntinfo.to_xml()
            proccont.append(cntinfo)
        else:
            # Ensure "No" is checked and return None if not used.
            self.ui.rbtn_no.setChecked(True)
            proccont = None

        return proccont

    def from_xml(self, contact_information):
        """
        Description:
            Populates the embedded ContactInfo widget from an XML
            element, which may be <proccont> or directly <cntinfo>.

        Passed arguments:
            contact_information (lxml.etree._Element): The XML node to
                load, expected to be <proccont> or <cntinfo>.

        Returned objects:
            None

        Workflow:
            1. Locates the child <cntinfo> node.
            2. Sets the "Yes" radio button if loading <cntinfo> directly.
            3. Calls cntinfo.from_xml() on the child node.

        Notes:
            None
        """

        if contact_information.tag == "cntinfo":
            # If the element is <cntinfo>, set to "Yes".
            self.ui.rbtn_yes.setChecked(True)
            cntinfo_node = contact_information
        else:
            # Otherwise, search for the child <cntinfo> node.
            cntinfo_node = contact_information.xpath("cntinfo")[0]

        self.cntinfo.from_xml(cntinfo_node)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ProcessContact, "ProcessContact testing")
