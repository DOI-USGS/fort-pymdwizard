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
    from PyQt5.QtWidgets import (QLineEdit, QLabel)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, spatial_utils, fgdc_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_mapproj
except ImportError as err:
    raise ImportError(err, __file__)


class MapProj(WizardWidget):
    """
    Description:
        A widget to handle the contents of the FGDC "mapproj"
        (Map Projection) tag, allowing the user to dynamically load and
        edit projection parameters based on a selected shortname.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        Manages the dynamic creation of input fields (QLineEdit) for
        specific map projection parameters defined in the "spatial_utils"
        lookup table.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Map Projection <mapproj>"
    acceptable_tags = ["mapproj"]

    ui_class = UI_mapproj.Ui_Form

    # Defines the maximum number of standard parallels expected.
    max_stdparall = 2

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Initializes the UI class.
            2. Calls "setupUi".
            3. Sets up drag-and-drop functionality for the widget.

        Notes:
            Initializes the "shortname" attribute to an empty string.
        """

        # Default.
        self.shortname = ""

        # Initialize the Qt UI object.
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Enable the widget for drag and drop operations.
        self.setup_dragdrop(self)

    def clear_widget(self):
        """
        Description:
            Removes all dynamically added widgets (projection parameters)
            from the layout.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Iterates in reverse over the items in the "mapproj_contents"
            layout and deletes each widget.

        Notes:
            This prepares the widget to load a new map projection.
        """

        layout = self.ui.mapproj_contents.layout()

        # Iterate in reverse to safely delete items from layout.
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def load_projection(self, shortname):
        """
        Description:
            Loads the required input fields for a specific map projection
            type into the widget.

        Passed arguments:
            shortname (str): The shortname of the map projection
                (e.g., "albers").

        Returned objects:
            None

        Workflow:
            1. Clears existing widgets.
            2. Looks up projection details and FGDC annotation lookup.
            3. Dynamically creates QLabel and QLineEdit widgets for each
               required parameter.
            4. Adds the label/lineedit pair to the layout.

        Notes:
            Handles the special case of "stdparll" by creating
            "stdparll_2" if needed.
        """

        self.clear_widget()
        self.shortname = shortname

        # Lookup projection parameters based on shortname.
        self.projection = spatial_utils.lookup_shortname(shortname)

        # Get FGDC lookup for parameter long names and annotations.
        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        # Handle the special case for the second standard parallel
        # Note: This is a hack to allow a second standard parallel field.
        annotation_lookup["stdparll_2"] = {
            "long_name": "Standard Parallel",
            "annotation": annotation_lookup["stdparll"]["annotation"],
        }

        self.clear_widget()  # TODO: why is this called again ??????????????????????????
        layout = self.ui.mapproj_contents.layout()

        # Iterate over required parameters and build the UI.
        for param in self.projection["elements"]:
            try:
                long_name = annotation_lookup[param]["long_name"]
                annotation = annotation_lookup[param]["annotation"]
            except:
                long_name = param
                annotation = "Unknown"

            # Create and configure the label.
            label = QLabel(long_name)
            label.setToolTip(annotation)
            label.help_text = annotation

            # Create and configure the line edit input.
            lineedit = QLineEdit("...")
            lineedit.setObjectName("fgdc_" + param)
            lineedit.setToolTip(annotation)

            # Add the label and input field to the layout.
            layout.addRow(label, lineedit)

    def to_xml(self):
        """
        Description:
            Converts the widget's contents into an FGDC XML element
            structure.

        Passed arguments:
            None

        Returned objects:
            proj_root (lxml.etree._Element): The XML node representing
                the map projection (<mapproj>).

        Workflow:
            1. Creates a root XML node with the projection shortname
               (e.g., <albers>).
            2. Iterates over the projection parameters.
            3. Finds the corresponding QLineEdit widget.
            4. Creates an XML sub-node for each parameter with the
               widget's text content.

        Notes:
            Returns "None" if no projection is loaded. Handles the
            "stdparll_2" parameter by mapping it back to "stdparll" in
            the output XML.
        """

        # Only proceed if a projection has been loaded.
        if self.shortname:
            # Create the root node with the projection shortname.
            proj_root = xml_utils.xml_node(self.shortname)

            # Iterate over all required parameters.
            for param in self.projection["elements"]:
                # Find the widget using its object name.
                widget = self.findChild(QLineEdit, "fgdc_" + param)

                # Handle the second standard parallel name change for XML
                xml_tag = "stdparll" if param == "stdparll_2" else param

                if widget is not None:
                    # Create XML node with widget's current text
                    xml_utils.xml_node(
                        xml_tag, text=widget.text(), parent_node=proj_root
                    )
                else:
                    # Create an empty XML node if widget not found
                    xml_utils.xml_node(
                        xml_tag, text="", parent_node=proj_root
                    )

            return proj_root
        else:
            return None

    def from_xml(self, mapproj_node):
        """
        Description:
            Populates the widget's input fields from an existing
            "mapproj" XML node.

        Passed arguments:
            mapproj_node (lxml.etree._Element): An XML node containing
                the map projection parameters.

        Returned objects:
            None

        Workflow:
            1. Extracts the shortname from the node tag (e.g., "albers").
            2. Calls "load_projection" to set up the necessary UI fields.
            3. Iterates over the XML children and finds the matching
               QLineEdit widgets to set their text content.
            4. Explicitly handles the mapping of the two "stdparll" XML
               tags to the two UI fields ("fgdc_stdparll" and
               "fgdc_stdparll_2").

        Notes:
            Uses "utils.set_text" for safe text assignment. Fails
            silently if "stdparll" handling encounters an error.
        """

        self.clear_widget()

        # Load projection UI based on the XML node's tag (shortname).
        shortname = mapproj_node.tag
        self.load_projection(shortname)

        # Iterate through XML children to populate UI fields.
        for item in mapproj_node.getchildren():
            tag = item.tag

            # Find the corresponding QLineEdit widget.
            item_widget = self.findChild(QLineEdit, "fgdc_" + tag)

            # Set the widget's text.
            utils.set_text(item_widget, item.text)

        # Special handling for standard parallel, as it can be repeated.
        stdparll = mapproj_node.xpath("stdparll")
        try:
            # Populate the first standard parallel
            stdparll_widget = self.findChildren(
                QLineEdit, "fgdc_stdparll"
            )[0]
            utils.set_text(stdparll_widget, stdparll[0].text)
            # Populate the second standard parallel
            stdparl_2_widget = self.findChildren(
                QLineEdit, "fgdc_stdparll_2"
            )[0]
            utils.set_text(stdparl_2_widget, stdparll[1].text)
        except IndexError:
            # Pass silently if one or both standard parallels are missing
            # in the XML but expected in the UI
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(MapProj, "spref testing")
