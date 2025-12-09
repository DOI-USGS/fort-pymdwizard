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
    from pymdwizard.gui.ui_files import UI_PointOfContact
    from pymdwizard.gui import ContactInfo
except ImportError as err:
    raise ImportError(err, __file__)


class ContactInfoPointOfContact(WizardWidget):
    """
    Description:
        A specialized widget for the FGDC <ptcontac> (Point of Contact)
        tag. It wraps a ContactInfo widget and provides the logic to
        control its visibility based on a "Yes/No" radio button.

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
    drag_label = "Point of Contact <pntcontac>"
    acceptable_tags = ["pntcontac", "cntinfo"]

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
            2. Creates and embeds the "ContactInfo" child widget.
            3. Sets the initial size to the collapsed state.
            4. Sets the widget's object name to "ptcontac".

        Notes:
            None
        """

        self.ui = UI_PointOfContact.Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        # Initialize and embed the ContactInfo child widget.
        self.cntinfo = ContactInfo.ContactInfo(parent=self)
        self.ui.main_layout.addWidget(self.cntinfo)

        # Define QSize objects for the collapsed and expanded states.
        self.collaped_size = QSize(self.WIDGET_WIDTH,
                                   self.COLLAPSED_HEIGHT)
        self.expanded_size = QSize(self.WIDGET_WIDTH,
                                   self.EXPANDED_HEIGHT)

        # Set the initial size to collapsed.
        self.resize(self.collaped_size)

        # Set the widget's object name for identification.
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

    def has_content(self):
        """
        Description:
            Checks if the point of contact section is enabled (i.e., used).

        Passed arguments:
            None

        Returned objects:
            bool: True if the "Yes" radio button is checked, False otherwise.

        Workflow:
            Checks the state of the "Yes" radio button.

        Notes:
            None
        """

        # Content exists if the 'Yes' radio button is checked.
        return self.ui.rbtn_yes.isChecked()

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <ptcontac> XML
            element. Returns None if the contact is not used.

        Passed arguments:
            None

        Returned objects:
            pntcontact (lxml.etree._Element or None): The <ptcontac>
                element or None.

        Workflow:
            1. Checks "rbtn_yes".
            2. If checked, creates <ptcontac> and appends the XML
               from the "cntinfo" child widget.

        Notes:
            None
        """

        if self.ui.rbtn_yes.isChecked():
            # Create the <ptcontac> node.
            pntcontact = xml_utils.xml_node(tag="ptcontac")

            # Get and append the child <cntinfo> XML.
            cntinfo = self.cntinfo.to_xml()
            pntcontact.append(cntinfo)
        else:
            pntcontact = None

        return pntcontact

    def from_xml(self, contact_information):
        """
        Description:
            Populates the embedded ContactInfo widget from an XML
            element, which may be <ptcontac> or directly <cntinfo>.

        Passed arguments:
            contact_information (lxml.etree._Element): The XML node to
                load, expected to be <ptcontac> or <cntinfo>.

        Returned objects:
            None

        Workflow:
            1. Locates the child <cntinfo> node.
            2. Calls cntinfo.from_xml() on that node.
            3. (Implicitly) Assumes the contact is used and enables the
               "Yes" radio button.

        Notes:
            None
        """

        if contact_information.tag == "cntinfo":
            # If the element is already <cntinfo>, use it directly.
            cntinfo_node = contact_information
        else:
            # Otherwise, search for the child <cntinfo> node.
            cntinfo_node = contact_information.xpath("cntinfo")[0]

        # Populate the child widget.
        self.cntinfo.from_xml(cntinfo_node)

        # Ensure the "Yes" button is checked since content was loaded.
        self.ui.rbtn_yes.setChecked(True)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ContactInfoPointOfContact,
                        "ContactInfoPointOfContact testing")
