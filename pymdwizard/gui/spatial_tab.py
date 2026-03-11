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

# Standard python libraries.
import os

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QMessageBox, QFileDialog)
    from PyQt5.QtCore import QSettings
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, spatial_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_spatial_tab
    from pymdwizard.gui import (spref, spdoinfo, spdom)
    from pymdwizard import __version__
except ImportError as err:
    raise ImportError(err, __file__)


class SpatialTab(WizardWidget):
    """
        Description:
            A top-level tab widget that organizes spatial information for
            a metadata record, including Spatial Domain (<spdom>),
            Spatial Reference (<spref>), and Spatial Data Organization
            (<spdoinfo>).

        Passed arguments:
            root_widget (QWidget, optional): Reference to the main
                MetadataRoot widget.

        Returned objects:
            None

        Workflow:
            1. Initializes UI and embeds child widgets ("Spdom", "SpRef",
               "SpdoInfo").
            2. Provides a file browser ("browse") and a utility method
               ("populate_from_fname") to extract spatial information
               from a data file.
            3. XML serialization/deserialization is deferred to the
               parent "MetadataRoot" widget.

        Notes:
            Inherits from "WizardWidget". The class contains logic to
            read common spatial file formats (e.g., shapefiles, GeoTIFFs)
            and populate relevant metadata fields.
        """

    # Class attributes.
    drag_label = "Spatial org and Spatial Ref <...>"
    acceptable_tags = ["idinfo"]

    # Assign the UI class.
    ui_class = UI_spatial_tab.Ui_spatial_tab

    def __init__(self, root_widget=None):
        """
        Initialize the SpatialTab widget.
        """

        # Call the base class constructor.
        super(self.__class__, self).__init__()
        self.schema = "bdp"

        # Store reference to the root widget.
        self.root_widget = root_widget

        # Store a reference to the scroll area.
        self.scroll_area = self.ui.spatial_scroll_area

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding the three child spatial widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up drag-and-drop, creates "Spdom",
            "SpRef", and "SpdoInfo" instances, and inserts them into
            the appropriate UI columns.

        Notes:
            None
        """

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self)

        # Initialize and embed Spdom (Spatial Domain).
        self.spdom = spdom.Spdom()
        self.ui.spatial_main_widget.layout().insertWidget(0, self.spdom)

        # Initialize and embed SpRef (Spatial Reference).
        self.spref = spref.SpRef()
        self.ui.two_column_left.layout().insertWidget(0, self.spref)

        # Initialize and embed SpdoInfo (Spatial Data Organization).
        self.spdoinfo = spdoinfo.SpdoInfo()
        self.ui.two_column_right.layout().insertWidget(0, self.spdoinfo)

        # Connect the browse button to the file selector.
        self.ui.btn_browse.clicked.connect(self.browse)

        # Clear all child widgets initially.
        self.clear_widget()

    def browse(self):
        """
        Description:
            Opens a file dialog to allow the user to select a spatial
            data file. If a file is selected, it calls
            "populate_from_fname".

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Retrieves the last used directory from QSettings.
            2. Opens a file dialog filtered for common spatial formats.
            3. If a file is selected, saves the path to QSettings and
               calls the population method.

        Notes:
            None
        """

        # Retrieve software version and last update info.
        settings = QSettings("USGS_" + __version__,
                             "pymdwizard_" + __version__)
        last_data_fname = settings.value("lastDataFname", "")

        # Determine starting directory/filename for dialog.
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        # Open the file selection dialog.
        fname = QFileDialog.getOpenFileName(
            self,
            fname,
            dname,
            filter=("Spatial files (*.shp *.tif *.jpg *.bmp *.img "
                    "*.jp2 *.png *.grd *.las *.laz)"),
        )

        if fname[0]:
            # Save the last file path and populate from the selected file.
            settings.setValue("lastDataFname", fname[0])
            self.populate_from_fname(fname[0])

    def populate_from_fname(self, fname):
        """
        Description:
            Extracts spatial metadata (bounding box, spatial data
            organization, and spatial reference) from a given file
            path and populates the child widgets.

        Passed arguments:
            fname (str): The full path to the spatial data file.

        Returned objects:
            None

        Workflow:
            1. Attempts to extract bounding box, spatial data org, and
               spatial reference sequentially using "spatial_utils".
            2. If extraction fails, clears the corresponding widget and
               builds an error message.
            3. Displays a warning if any extraction failed.

        Notes:
            Relies on external "spatial_utils" for file parsing.
        """

        # Default message value.
        msg = ""

        # 1. Extract and populate Spatial Domain (bounding box).
        try:
            spdom = spatial_utils.get_bounding(fname)
            self.spdom.from_xml(spdom)
        except:
            msg = "Problem encountered extracting bounding coordinates"
            self.spdom.clear_widget()

        # 2. Extract and populate Spatial Data Organization.
        try:
            spdoinfo = spatial_utils.get_spdoinfo(fname)
            self.spdoinfo.from_xml(spdoinfo)
        except:
            msg += "\nProblem encountered extracting spatial data organization"
            self.spdoinfo.clear_widget()

        # 3. Extract and populate Spatial Reference.
        try:
            spref = spatial_utils.get_spref(fname)
            self.spref.from_xml(spref)
        except:
            msg += "\nProblem encountered extracting spatial reference"
            self.spref.clear_widget()

        # Display compiled warning message if any operation failed.
        if msg:
            QMessageBox.warning(self, "Problem encountered", msg)

    def switch_schema(self, schema):
        """
        Description:
            Passes the schema switch instruction down to child widgets
            that support different metadata standards.

        Passed arguments:
            schema (str): The new schema identifier (e.g., "bdp").

        Returned objects:
            None

        Workflow:
            Calls "switch_schema" on the "spdom" child widget.

        Notes:
            None
        """

        # Only spdom (spatial domain) currently has schema-specific logic.
        self.spdom.switch_schema(schema)

    def clear_widget(self):
        """
        Description:
            Clears the content of all embedded spatial child widgets.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls "clear_widget" on "spdoinfo", "spdom", and "spref".

        Notes:
            None
        """

        self.spdoinfo.clear_widget()
        self.spdom.clear_widget()
        self.spref.clear_widget()

    def to_xml(self):
        """
        Description:
            Converts the spatial content managed by this tab into XML.

        Passed arguments:
            None

        Returned objects:
            lxml.etree._Element: The XML output of the "spdom" widget.

        Workflow:
            Returns the XML from the "spdom" child widget, as the
            overall serialization is handled by the parent
            "MetadataRoot".

        Notes:
            The parent widget is expected to manage the assembly of
            <spdom>, <spdoinfo>, and <spref>.
        """

        # XML functions are primarily handled by the parent widget,
        # but this method is required by the framework.
        return self.spdom.to_xml()

    def from_xml(self, xml_unknown):
        """
        Description:
            Parses an XML element and directs it to the appropriate
            child widget ("spdom", "spref", or "spdoinfo") for population.

        Passed arguments:
            xml_unknown (lxml.etree._Element): An XML node that could
                be <spdom>, <spref>, or <spdoinfo>.

        Returned objects:
            None

        Workflow:
            Routes the XML node to the correct child widget based on
            its tag name.

        Notes:
            This method is used when the parent widget iterates over
            XML children to populate the overall spatial section.
        """

        if xml_unknown.tag == "spdoinfo":
            self.spdoinfo.from_xml(xml_unknown)
        elif xml_unknown.tag == "spref":
            self.spref.from_xml(xml_unknown)
        elif xml_unknown.tag == "spdom":
            self.spdom.from_xml(xml_unknown)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SpatialTab, "IdInfo testing")
