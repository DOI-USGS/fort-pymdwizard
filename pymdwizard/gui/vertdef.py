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

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.ui_files import UI_vertdef
except ImportError as err:
    raise ImportError(err, __file__)


class Vertdef(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <vertdef> tag (Vertical
        Coordinate System Definition), used to describe the vertical
        measurement system used in the data set. This includes altitude
        and depth systems.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Provides options to include/exclude the entire <vertdef>
           section, and sub-sections for altitude (<altsys>) and
           depth (<depthsys>).
        2. Uses "RepeatingElement" for multiple altitude and depth
           resolution values.

    Notes:
        Inherits from "WizardWidget". The "RepeatingElement" widgets
        are assumed to contain a toPlainText() method for their value.
    """

    # Class attributes.
    drag_label = "Time Period information <vertdef>"
    acceptable_tags = ["vertdef", "altsys", "depthsys"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            initializing the repeating elements for resolutions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up repeating lists for altitude and
            depth resolutions, and adds them to the respective layouts.

        Notes:
            None
        """

        self.ui = UI_vertdef.Ui_Form()

        # Setup the UI defined in the separate class.
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # --- Setup Altitude Resolution Repeating Element ---
        self.altres_list = RepeatingElement(
            widget_kwargs={
                "label": "Altitude Resolution",
                "line_name": "fgdc_altres",
                "required": True,
            },
            add_text="+",
            remove_text="-",
        )
        self.altres_list.add_another()

        # Insert the repeating element into the altsys layout.
        self.ui.altsys_contents.layout().insertWidget(1, self.altres_list)

        # --- Setup Depth Resolution Repeating Element ---
        self.depthres_list = RepeatingElement(
            widget_kwargs={
                "label": "Depth Resolution",
                "line_name": "fgdc_depthres",
                "required": True,
            },
            add_text="+",
            remove_text="-",
        )
        self.depthres_list.add_another()

        # Insert the repeating element into the depthsys layout.
        self.ui.depthsys_contents.layout().insertWidget(1, self.depthres_list)

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects "yes" radio buttons to methods that show/hide the
            corresponding content sections.

        Notes:
            None
        """

        # Connect main vertdef 'yes' radio button.
        self.ui.rbtn_yes.toggled.connect(self.include_vertdef_change)

        # Connect altitude system 'yes' radio button.
        self.ui.rbtn_yes_alt.toggled.connect(self.include_alt_change)

        # Connect depth system 'yes' radio button.
        self.ui.rbtn_yes_depth.toggled.connect(self.include_depth_change)

    def has_content(self):
        """
        Description:
            Returns if the widget contains legitimate content that should
            be written out to XML.

        Passed arguments:
            None

        Returned objects:
            bool: True if the main "yes" radio button is checked,
                False otherwise.

        Workflow:
            Checks the state of the main <vertdef> toggle.

        Notes:
            None
        """

        # Content is present if the user has chosen to include vertdef.
        return self.ui.rbtn_yes.isChecked()

    def include_vertdef_change(self, b):
        """
        Description:
            Toggles the visibility of the altitude and depth system
            content sections based on the <vertdef> "Yes/No" toggle.

        Passed arguments:
            b (bool): State of the radio button (True if checked).

        Returned objects:
            None

        Workflow:
            Shows or hides the content layout.

        Notes:
            This function has a duplicated inner function in the
            original code, which has been removed here.
        """

        # Show or hide the main content container.
        if b:
            self.ui.content_layout.show()
        else:
            self.ui.content_layout.hide()

    def include_alt_change(self, b):
        """
        Description:
            Toggles the visibility of the altitude system (<altsys>)
            content section.

        Passed arguments:
            b (bool): State of the radio button (True if checked).

        Returned objects:
            None

        Workflow:
            Shows or hides the altitude system layout.

        Notes:
            None
        """

        # Show or hide the altitude system container.
        if b:
            self.ui.altsys_contents.show()
        else:
            self.ui.altsys_contents.hide()

    def include_depth_change(self, b):
        """
        Description:
            Toggles the visibility of the depth system (<depthsys>)
            content section.

        Passed arguments:
            b (bool): State of the radio button (True if checked).

        Returned objects:
            None

        Workflow:
            Shows or hides the depth system layout.

        Notes:
            None
        """

        # Show or hide the depth system container.
        if b:
            self.ui.depthsys_contents.show()
        else:
            self.ui.depthsys_contents.hide()

    def clear_widget(self):
        """
        Description:
            Clears all content and resets the radio buttons to "No".

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the parent clear method and resets all relevant
            radio buttons.

        Notes:
            None
        """

        # Call parent's clear method.
        WizardWidget.clear_widget(self)

        # Reset all "include" radio buttons to "No".
        self.ui.rbtn_no.setChecked(True)
        self.ui.rbtn_no_alt.setChecked(True)
        self.ui.rbtn_no_depth.setChecked(True)

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <vertdef> XML
            element, including optional <altsys> and <depthsys>.

        Passed arguments:
            None

        Returned objects:
            vertdef (lxml.etree._Element or None): The <vertdef>
                element tag in the XML tree, or None if excluded.

        Workflow:
            1. Creates <vertdef> node if enabled.
            2. Appends <altsys> nodes if enabled, including resolutions.
            3. Appends <depthsys> nodes if enabled, including resolutions.

        Notes:
            None
        """

        # Only create <vertdef> if the main "yes" is checked.
        if self.ui.rbtn_yes.isChecked():
            vertdef = xml_utils.xml_node("vertdef")

            # --- Process Altitude System (<altsys>) ---
            if self.ui.rbtn_yes_alt.isChecked():
                altsys = xml_utils.xml_node("altsys", parent_node=vertdef)

                # Altitude Datum.
                altdatum = xml_utils.xml_node(
                    "altdatum",
                    text=self.ui.fgdc_altdatum.currentText(),
                    parent_node=altsys,
                )

                # Altitude Resolution(s).
                for widget in self.altres_list.get_widgets():
                    altres = xml_utils.xml_node(
                        "altres", widget.added_line.toPlainText(),
                        parent_node=altsys
                    )

                # Altitude Units.
                altunits = xml_utils.xml_node(
                    "altunits",
                    text=self.ui.fgdc_altunits.currentText(),
                    parent_node=altsys,
                )

                # Altitude Encoding.
                altenc = xml_utils.xml_node(
                    "altenc", text=self.ui.fgdc_altenc.currentText(),
                    parent_node=altsys
                )

            # --- Process Depth System (<depthsys>) ---
            if self.ui.rbtn_yes_depth.isChecked():
                depth = xml_utils.xml_node("depthsys",
                                           parent_node=vertdef)

                # Depth Datum.
                depthdn = xml_utils.xml_node(
                    "depthdn",
                    text=self.ui.fgdc_depthdn.currentText(),
                    parent_node=depth,
                )

                # Depth Resolution(s).
                for widget in self.depthres_list.get_widgets():
                    depthres = xml_utils.xml_node(
                        "depthres", widget.added_line.toPlainText(),
                        parent_node=depth
                    )

                # Depth Units.
                depthdu = xml_utils.xml_node(
                    "depthdu",
                    text=self.ui.fgdc_depthdu.currentText(),
                    parent_node=depth,
                )

                # Depth Encoding.
                depthem = xml_utils.xml_node(
                    "depthem",
                    text=self.ui.fgdc_depthem.currentText(),
                    parent_node=depth,
                )
            return vertdef
        else:
            return None

    def from_xml(self, vertdef):
        """
        Description:
            Parses an XML element and populates the widget fields,
            including resolutions and settings.

        Passed arguments:
            vertdef (lxml.etree._Element): The XML element, expected
                to be <vertdef>.

        Returned objects:
            None

        Workflow:
            1. Sets main <vertdef> to "Yes".
            2. Checks for <altsys>/<depthsys> and sets sub-toggles.
            3. Populates "RepeatingElement" lists for resolutions.
            4. Uses "utils.populate_widget" for dropdowns.

        Notes:
            None
        """

        # Clear existing content.
        self.clear_widget()
        try:
            if vertdef.tag == "vertdef":
                self.ui.rbtn_yes.setChecked(True)

                # --- Parse Altitude System (<altsys>) ---.
                if vertdef.xpath("altsys"):
                    self.ui.rbtn_yes_alt.setChecked(True)
                    self.altres_list.clear_widgets(add_another=False)

                    # Populate repeating resolutions.
                    for altres in vertdef.xpath("altsys/altres"):
                        altres_widget = self.altres_list.add_another()
                        altres_widget.added_line.setPlainText(altres.text)

                    # Add a default if resolutions list was empty.
                    if len(vertdef.xpath("altsys/altres")) == 0:
                        self.altres_list.add_another()
                else:
                    self.ui.rbtn_no_alt.setChecked(True)

                # --- Parse Depth System (<depthsys>) ---
                if vertdef.xpath("depthsys"):
                    self.ui.rbtn_yes_depth.setChecked(True)
                    self.depthres_list.clear_widgets(add_another=False)

                    # Populate repeating resolutions.
                    for depthres in vertdef.xpath("depthsys/depthres"):
                        depthres_widget = self.depthres_list.add_another()
                        depthres_widget.added_line.setPlainText(depthres.text)

                    # Add a default if resolutions list was empty.
                    if len(vertdef.xpath("depthsys/depthres")) == 0:
                        self.depthres_list.add_another()
                else:
                    self.ui.rbtn_no_depth.setChecked(True)

                # Populate remaining fields (dropdowns) using generic utility.
                utils.populate_widget(self, vertdef)
            else:
                print("The tag is not a vertdef")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Vertdef, "Vertdef testing")
