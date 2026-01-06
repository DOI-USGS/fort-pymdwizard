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
import pickle
import traceback

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import (QMessageBox, QFileDialog, QInputDialog)
    from PyQt5.QtCore import QSettings
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, data_io, spatial_utils)
    from pymdwizard.core.spatial_utils import get_raster_attribute_table
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_detailed
    from pymdwizard.gui import attributes
    from pymdwizard import __version__
except ImportError as err:
    raise ImportError(err, __file__)

# Get the default source definition text from settings.
default_def_source = utils.get_setting("defsource",
                                       "Producer Defined")


class Detailed(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "detailed description"
        ("detailed") metadata element, focusing on entity and
        attribute information. Inherits from WizardWidget.

    Passed arguments:
        remove_function (callable, optional): Function to call when
            the remove button is clicked. Defaults to None.
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Manages UI for Entity Type Label, Definition, and Source.
        2. Embeds an "Attributes" widget to handle attribute listing.
        3. Provides file browsing functionality to auto-populate
           entity/attribute details from various data file types.

    Notes:
        The class references an "EA" parent attribute (likely
        "EntityAndAttribute") for tooltip updates.
    """

    # Class attributes.
    drag_label = "Detailed Description <detailed>"
    acceptable_tags = ["detailed"]

    def __init__(self, remove_function=None, parent=None):
        # Store EntityAndAttribute parent for tooltip updates.
        self.EA = parent
        WizardWidget.__init__(self, parent=parent)

        # Conditionally hide or connect the remove button.
        if remove_function is None:
            self.ui.btn_remove.hide()
        else:
            self.ui.btn_remove.clicked.connect(remove_function)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, hides an internal widget, creates and
            embeds the "Attributes" child widget, sets up drag-and-drop,
            and connects event handlers.

        Notes:
            None
        """

        # Instantiate the UI elements.
        self.ui = UI_detailed.Ui_fgdc_detailed()
        self.ui.setupUi(self)

        # Hide internal widget (original code).
        self.ui.displayed_widget.hide()

        # Create and embed the child Attributes widget.
        self.attributes = attributes.Attributes(parent=self)
        self.ui.attribute_frame.layout().addWidget(self.attributes)

        # Initialize drag-and-drop features.
        self.setup_dragdrop(self)

        # Connect event handlers.
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.fgdc_enttypl.textChanged.connect(self.update_tooltip)

        # Set the default source definition.
        self.ui.fgdc_enttypds.setText(default_def_source)

    def browse(self):
        """
        Description:
            Opens a file dialog to select a data file, then calls
            "populate_from_fname" to load data from it.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Reads the last used file path from settings.
            2. Defines a comprehensive file filter for various data types.
            3. Opens the file dialog.
            4. If a file is selected, updates settings and calls the
               population function, displaying a warning on failure.

        Notes:
            None
        """

        # Read last used file path from QSettings.
        settings = QSettings("USGS_" + __version__,
                             "pymdwizard_" + __version__)
        last_data_fname = settings.value("lastDataFname", "")
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        # Define the file filter string.
        filter = (
            "data files (*.csv *.txt *.shp *.xls *.xlsm *.xlsx "
            "*.tif *.grd *.png *.img *.jpg *.hdr *.bmp *.adf "
            "*.las *.laz)"
        )

        # Open file dialog.
        fname = QFileDialog.getOpenFileName(self, fname, dname, filter=filter)
        if fname[0]:
            # Save the new file path and attempt to populate.
            settings.setValue("lastDataFname", fname[0])
            try:
                self.populate_from_fname(fname[0])
            except BaseException as e:
                msg = "Could not extract data from file %s:\n%s." % (
                    fname,
                    traceback.format_exc(),
                )
                QMessageBox.warning(self, "Data file error", msg)

    def update_tooltip(self):
        """
        Description:
            Updates the tooltip for the current tab in the parent
            Entity and Attribute widget ("EA").

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Gets the current text of the Entity Type Label and sets it
            as the tooltip for the current tab in the parent's tab widget.

        Notes:
            None
        """

        try:
            cur_text = self.ui.fgdc_enttypl.text()
            cur_index = self.EA.ui.fgdc_eainfo.currentIndex()

            # Set the new tooltip for the current tab.
            self.EA.ui.fgdc_eainfo.setTabToolTip(cur_index, cur_text)
        except:
            pass

    def populate_from_fname(self, fname):
        """
        Description:
            Clears the widget and populates the entity and attribute
            information by reading the contents of the given data file.

        Passed arguments:
            fname (str): Full path to the data file.

        Returned objects:
            None

        Workflow:
            Handles file types including CSV, Shapefile, Excel, Raster,
            Pickle, and generic text files, setting the entity label
            and definition, and loading attributes into the child widget.

        Notes:
            Uses "data_io" and "spatial_utils" for file handling.
            Includes logic for handling large CSV files and setting
            defaults for Shapefile/Raster internal attributes.
        """

        # Handle Excel sheet name embedded in path (e.g.,
        # path/file.xlsx$Sheet1).
        if fname.endswith("$"):
            fname, sheet_name = os.path.split(fname)
            sheet_name = sheet_name[:-1]
            ok = True
        else:
            sheet_name = None

        shortname = os.path.split(fname)[1]
        ext = os.path.splitext(shortname)[1]

        self.ui.fgdc_enttypds.setText(default_def_source)

        # --- CSV File Handling ---
        if ext.lower() == ".csv":
            try:
                self.clear_widget()
                self.ui.fgdc_enttypl.setText(shortname)
                self.ui.fgdc_enttypd.setPlainText(
                    "Comma Separated Value (CSV) file containing data."
                )

                # Open file as DataFrame.
                df = data_io.read_data(fname)
                max_rows = int(utils.get_setting("maxrows",
                                                 1000000))

                # Warn user if the file is too large.
                if df.shape[0] == max_rows:
                    msg = (
                        f"This CSV file contains more than "
                        f"{data_io.MAX_ROWS:,} rows!\n\n Due to speed "
                        f"and memory constraints, \ndata from rows "
                        f"past\nthe first {max_rows:,} rows"
                        f"\nwere not used to populate this section.\n\n"
                        f"Check that the values displayed are complete "
                        f"\nand appropriate for the entire record."
                    )
                    QMessageBox.warning(self, "Large File Warning", msg)

                self.attributes.load_df(df)
            except BaseException as e:
                msg = (
                    f"Cannot read csv {fname}:\n"
                    f"{traceback.format_exc()}."
                )

                QMessageBox.warning(self, "Recent Files", msg)

        # --- Shapefile Handling ---
        elif ext.lower() == ".shp":
            self.clear_widget()
            self.ui.fgdc_enttypl.setText(shortname + " Attribute Table")
            self.ui.fgdc_enttypd.setPlainText(
                "Table containing attribute information "
                "associated with the data set."
            )

            # Open dataset.
            df = data_io.read_data(fname)
            self.attributes.load_df(df)

            # Set defaults for required ESRI attributes (FID and Shape).
            fid_attr = self.attributes.get_attr("FID")
            if fid_attr is not None:
                fid_attr.populate_domain_content(3)
                fid_attr.ui.fgdc_attrdef.setPlainText(
                    "Internal feature number.")
                utils.set_text(fid_attr.ui.fgdc_attrdefs, "ESRI")
                fid_attr.domain.ui.fgdc_udom.setPlainText(
                    "Sequential unique whole numbers that are "
                    "automatically generated."
                )
                fid_attr.regularsize_me()
                fid_attr.supersize_me()
            shape_attr = self.attributes.get_attr("Shape")
            if shape_attr is not None:
                shape_attr.populate_domain_content(3)
                shape_attr.ui.fgdc_attrdef.setPlainText("Feature geometry.")
                utils.set_text(shape_attr.ui.fgdc_attrdefs, "ESRI")
                shape_attr.domain.ui.fgdc_udom.setPlainText("Shape type.")
                shape_attr.store_current_content()
                shape_attr.supersize_me()
                shape_attr.store_current_content()
                shape_attr.regularsize_me()

        # --- Excel File Handling ---
        elif ext.lower() in [".xlsm", ".xlsx", ".xls"]:
            if sheet_name is None:
                sheets = data_io.get_sheet_names(fname)

                sheet_name, ok = QInputDialog.getItem(
                    self,
                    "select sheet dialog",
                    "Pick one of the sheets from this workbook",
                    sheets,
                    0,
                    False,
                )
            if ok and sheet_name:
                self.clear_widget()
                self.ui.fgdc_enttypl.setText(f"{shortname} ({sheet_name})")
                self.ui.fgdc_enttypd.setPlainText("Excel Worksheet")

                df = data_io.read_excel(fname, sheet_name)
                self.attributes.load_df(df)

        # --- Raster File Handling ---
        elif ext.lower() in [
            ".tif",
            ".grd",
            ".png",
            ".img",
            ".jpg",
            ".hdr",
            ".bmp",
            ".adf",
        ]:
            self.ui.fgdc_enttypl.setText(shortname)

            num_bands = spatial_utils.get_band_count(fname)
            if num_bands == 1:
                self.ui.fgdc_enttypd.setPlainText(
                    "Raster geospatial data file.")
            else:
                self.ui.fgdc_enttypd.setPlainText(
                    "{} band raster geospatial data file.".format(num_bands)
                )

            # Retrieve raster attribute values.
            df = get_raster_attribute_table(fname)
            self.attributes.load_df(df)

            # Set defaults for required Raster attributes (OID, Value, Count).
            oid_attr = self.attributes.get_attr("OID")
            if oid_attr is not None:
                oid_attr.populate_domain_content(3)
                oid_attr.ui.fgdc_attrdef.setPlainText(
                    "Internal object identifier."
                )
                oid_attr.domain.ui.fgdc_udom.setPlainText(
                    "Sequential unique whole numbers that are "
                    "automatically generated."
                )
                oid_attr.regularsize_me()
                oid_attr.supersize_me()
            value_attr = self.attributes.get_attr("Value")
            if value_attr is not None:
                value_attr.populate_domain_content(1)
                value_attr.ui.fgdc_attrdef.setPlainText(
                    "Unique numeric values contained in each raster cell."
                )
            count_attr = self.attributes.get_attr("Count")
            if count_attr is not None:
                count_attr.populate_domain_content(1)
                count_attr.ui.fgdc_attrdef.setPlainText(
                    "Number of raster cells with this value."
                )

        # --- Pickle File Handling ---
        elif ext.lower() == ".p":
            p = pickle.load(open(fname, "rb"), encoding="bytes")

            if self.original_xml is not None:
                # Reload original XML content if available.
                original_content = xml_utils.XMLNode(self.original_xml)
                self.from_xml(self.original_xml)
            else:
                self.ui.fgdc_enttypl.setText("{}".format(shortname[:-2]))
                self.ui.fgdc_enttypd.setPlainText("Geospatial Dataset")
                self.attributes.load_pickle(p)

        # --- Text File Handling ---
        elif ext.lower() == ".txt":
            if sheet_name is None:
                # Prompt user for the delimiter
                delimiters = {
                    "comma": ",",
                    "tab": "\t",
                    "pipe": "|",
                    "colon": ":",
                }

                delimiter_str, ok = QInputDialog.getItem(
                    self,
                    "Select text delimiter",
                    "Pick the delimiter used in this file",
                    delimiters.keys(),
                    0,
                    False,
                )

                delimiter = delimiters[delimiter_str]

            if ok and delimiter:
                try:
                    self.clear_widget()
                    self.ui.fgdc_enttypl.setText(shortname)
                    self.ui.fgdc_enttypd.setPlainText(
                        "{} delimited text file.".format(delimiter_str)
                    )

                    df = data_io.read_data(fname, delimiter=delimiter)
                    self.attributes.load_df(df)
                except BaseException as e:
                    msg = "Cannot read txt file %s:\n%s." % (
                        fname,
                        traceback.format_exc(),
                    )
                    QMessageBox.warning(self, "File load problem", msg)

        # --- LAS/LAZ (Lidar) File Handling ---
        elif ext.lower() in [".las", ".laz"]:
            self.clear_widget()
            self.ui.fgdc_enttypl.setText(shortname)
            self.ui.fgdc_enttypd.setPlainText(
                "{} lidar data file.".format(ext)
            )

            # Open data.
            df = data_io.read_data(fname)
            self.attributes.load_df(df)

        # --- Unsupported File Format ---
        else:
            msg = (
                "Can only read '.csv', '.txt', '.shp', '.las.', "
                "raster files, and Excel files here"
            )
            QMessageBox.warning(self, "Unsupported file format", msg)

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears the text fields and calls the child attribute widget's
            clear method.

        Notes:
            None
        """

        self.ui.fgdc_enttypl.setText("")
        self.ui.fgdc_enttypd.setPlainText("")

        # Clear all attributes from the child widget.
        self.attributes.clear_children()

    def has_content(self):
        """
        Description:
            Checks for valid content in this widget.

        Passed arguments:
            None

        Returned objects:
            bool: True if any required field or attributes exist.

        Workflow:
            Checks the Entity Type Label, Entity Definition, and the
            count of attributes.

        Notes:
            None
        """

        has_content = False

        if self.ui.fgdc_enttypl.text():
            has_content = True
        if self.ui.fgdc_enttypd.toPlainText():
            has_content = True

        # Check if the attributes widget has any attributes loaded.
        if len(self.attributes.attrs) > 0:
            has_content = True

        return has_content

    def to_xml(self):
        """
        Description:
            Encapsulates the Entity Type information and all attributes
            into a single "detailed" XML element tag.

        Passed arguments:
            None

        Returned objects:
            detailed (xml.etree.ElementTree.Element): Detailed
                description element tag in XML tree.

        Workflow:
            1. Creates the <detailed> parent node.
            2. Creates and appends the <enttyp> node (containing
               label, definition, and source).
            3. Appends all <attr> nodes from the child "Attributes"
               widget directly to the <detailed> node.

        Notes:
            Assumes "xml_utils.xml_node" is available.
        """

        # Create the parent 'detailed' XML node
        detailed = xml_utils.xml_node("detailed")

        # Create the <enttyp> container node.
        enttyp = xml_utils.xml_node("enttyp", parent_node=detailed)

        # Create the <enttypl> container node.
        enttypl = xml_utils.xml_node(
            "enttypl", text=self.ui.fgdc_enttypl.text(),
            parent_node=enttyp
        )

        # Create the <enttypd> container node.
        enttypd = xml_utils.xml_node(
            "enttypd", text=self.ui.fgdc_enttypd.toPlainText(),
            parent_node=enttyp
        )

        # Create the <enttypds> container node.
        enttypds = xml_utils.xml_node(
            "enttypds", text=self.ui.fgdc_enttypds.text(),
            parent_node=enttyp
        )

        # Get the attribute XML elements from the child widget.
        attr = self.attributes.to_xml()

        # Append each <attr> element directly to <detailed>.
        for a in attr.xpath("attr"):
            detailed.append(a)
        return detailed

    def from_xml(self, detailed):
        """
        Description:
            Parse the XML code into the relevant detailed description
            elements.

        Passed arguments:
            detailed (xml.etree.ElementTree.Element): The XML element
                containing the detailed description.

        Returned objects:
            None

        Workflow:
            1. Check for the "detailed" tag.
            2. Uses "utils.populate_widget" to fill simple fields.
            3. Delegates parsing of <attr> elements to the child
               "Attributes" widget.

        Notes:
            None
        """

        try:
            if detailed.tag == "detailed":
                self.original_xml = detailed

                # Populate simple fields (label, definition, source).
                utils.populate_widget(self, detailed)

                # Delegate the complex attribute parsing to the child.
                self.attributes.from_xml(detailed)
            else:
                print("The tag is not a detailed")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Detailed, "detailed testing")
