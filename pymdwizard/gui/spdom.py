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
import platform
from copy import deepcopy
import time

# Non-standard python libraries.
try:
    import pandas as pd
    from PyQt5.QtWidgets import (QMessageBox, QCompleter)
    from PyQt5.QtCore import (QStringListModel, QUrl, QDir,
                              QSettings, pyqtSlot)
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5 import QtCore
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, spatial_utils)
    from pymdwizard.core.xml_utils import xml_node
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_spdom
except ImportError as err:
    raise ImportError(err, __file__)

# Use the correct naming for the XML node function
# xml_node = xml_utils.xml_node


class Spdom(WizardWidget):
    """
    Description:
        Widget for handling the FGDC Spatial Domain <spdom> component,
        including boundary coordinates and a map interface (Leaflet via
        QWebEngineView).

    Passed arguments:
        root_widget (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes coordinate attributes and UI components.
        2. Loads spatial boundary data for auto-completion.
        3. Sets up map view and JavaScript channel for two-way
           communication.

    Notes:
        The "bnds_df" DataFrame is used for geographical name
        auto-completion and coordinate lookup.
    """

    # Class attributes.
    drag_label = "Spatial Domain <spdom>"
    acceptable_tags = ["spdom", "bounding"]
    ui_class = UI_spdom.Ui_fgdc_spdom

    def __init__(self, root_widget=None):
        # Initialize internal state variables for coordinates and validation.
        self.east = 180
        self.west = -180
        self.north = 90
        self.south = -90
        self.valid = True

        # Initialize the parent WizardWidget.
        super(self.__class__, self).__init__()
        self.schema = "bdp"
        self.root_widget = root_widget

        # Internal flags for controlling map and XML loading state.
        self.after_load = False
        self.in_xml_load = False
        self.has_rect = True

        # Setup QCompleter for geographical description field.
        self.completer = QCompleter()
        self.ui.fgdc_descgeog.setCompleter(self.completer)

        # Setup model for completer data.
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(0)

        # Load boundary coordinate data from CSV file.
        fname = utils.get_resource_path("spatial/BNDCoords.csv")
        self.bnds_df = pd.read_csv(fname)
        self.model.setStringList(self.bnds_df["Name"])

        # Connect completer events to coordinate update function.
        self.completer.popup().clicked.connect(self.on_completer_activated)
        self.completer.popup().selectionModel().selectionChanged.connect(
            self.on_completer_activated
        )
        # self.completer.popup().activated.connect(self.on_completer_activated)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI, setting up the map
            view and communication channel.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Sets up the main UI from the designer file.
            2. Determines the correct Leaflet map HTML file based on OS.
            3. Initializes QWebEngineView and QWebChannel for JS comms.
            4. Loads the map HTML file.
            5. Adds the map view to the layout.

        Notes:
            Handles QWebEngineView setup differences and sets up the
            "Spdom" object for JavaScript access.
        """

        # Instantiate and setup the UI.
        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Determine which map file to load based on OS.
        if platform.system() == "Darwin":
            map_fname = utils.get_resource_path("leaflet/map_mac.html")
        else:
            map_fname = utils.get_resource_path("leaflet/map.html")

        # Setup QWebEngineView and QWebChannel for JS interaction
        self.view = QWebEngineView()
        channel = QWebChannel()
        channel.registerObject("Spdom", self)
        self.view.page().setWebChannel(channel)

        # Load the local HTML map file
        local_url = QUrl.fromLocalFile(QDir.current().filePath(map_fname))
        self.view.setUrl(local_url)

        # Connect the map load finished signal.
        self.view.page().loadFinished.connect(self.on_map_load_finished)

        # Add the map view to the vertical layout
        self.ui.verticalLayout_3.addWidget(self.view)

        # Setup drag-drop functionality for this widget and all it's children.
        self.setup_dragdrop(self)
        self.raise_()

    def connect_events(self):
        """
        Description:
            Connect the coordinate input fields to the update function.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects "editingFinished" signal of all bounding coordinate
            fields to coord_updated.

        Notes:
            None
        """

        self.ui.fgdc_eastbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_westbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_northbc.editingFinished.connect(self.coord_updated)
        self.ui.fgdc_southbc.editingFinished.connect(self.coord_updated)

    def on_completer_activated(self, model_index):
        """
        Description:
            Updates the bounding coordinate fields when an item from the
            geographical description completer is selected.

        Passed arguments:
            model_index (QModelIndex): The index of the selected item.

        Returned objects:
            None

        Workflow:
            1. Extracts the selected geographical name.
            2. Looks up the corresponding coordinates in bnds_df.
            3. Populates the east, west, north, and south fields.
            4. Updates the map with the new rectangle.

        Notes:
            Handles both QModelIndex and QAction-like inputs.
        """

        try:
            # Extract the data from the model index.
            try:
                cur_descgeog = model_index.data()
            except AttributeError:
                cur_descgeog = model_index.indexes()[0].data()
        except:
            return

        # Look up the coordinates in the DataFrame and populate fields.
        try:
            if self.bnds_df["Name"].str.contains(cur_descgeog).any():
                df_row = self.bnds_df[self.bnds_df["Name"] == cur_descgeog]
                self.ui.fgdc_eastbc.setText(str(float(df_row["east"])))
                self.ui.fgdc_westbc.setText(str(float(df_row["west"])))
                self.ui.fgdc_northbc.setText(str(float(df_row["north"])))
                self.ui.fgdc_southbc.setText(str(float(df_row["south"])))
                self.add_rect()
                self.update_map()
        except:
            pass

    def complete_name(self):
        """
        Description:
            Triggers the "addRect" JavaScript function in the map view
            for auto-completion.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Executes addRect() via runJavaScript.

        Notes:
            None
        """

        # Execute the 'addRect' JS function.
        self.view.page().runJavaScript("addRect();", js_callback)

    def coord_updated(self):
        """
        Description:
            Validates bounding box coordinates after a field is edited
            and updates the map.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Validates input is numeric and within -180/180 or -90/90.
            2. Validates North > South relationship.
            3. Shows a warning if validation fails.
            4. Calls add_rect/remove_rect and update_map if valid.

        Notes:
            None
        """

        good_coords = self.all_good_coords()

        # Get the name and value of the sender widget.
        try:
            cur_name = self.sender().objectName()
            if "fgdc" not in cur_name:
                return
            cur_value = self.sender().text()
        except AttributeError:
            cur_name = ""
            cur_value = ""

        # Attempt to convert to float for validation.
        try:
            cur_value = float(cur_value)
        except ValueError:
            pass

        msg = ""
        # Validate input type and format.
        if not isinstance(cur_value, float) and cur_value != "":
            msg = "number entered must be numeric only"
        elif cur_value == "":
            msg = ""
        # Validate East/West ranges.
        elif cur_name in ["fgdc_westbc", "fgdc_eastbc"] and \
                not -180 <= cur_value <= 180:
            msg = ("East or West coordinate must be within -180 "
                   "and 180")
        # Validate North/South ranges.
        elif cur_name in ["fgdc_southbc", "fgdc_northbc"] and \
                not -90 <= cur_value <= 90:
            msg = ("North and South coordinates must be within -90 "
                   "and 90")
        # Validate North > South relationship (South field updated).
        elif cur_name == "fgdc_southbc":
            try:
                north = float(self.ui.fgdc_northbc.text())
                if north <= cur_value:
                    msg = ("North coordinate must be greater than "
                           "South coordinate")
            except ValueError:
                pass
        # Validate North > South relationship (North field updated).
        elif cur_name == "fgdc_northbc":
            try:
                south = float(self.ui.fgdc_southbc.text())
                if south >= cur_value:
                    msg = ("North coordinate must be greater than "
                           "South coordinate")
            except ValueError:
                pass

        # Show warning if any validation failed.
        if msg:
            QMessageBox.warning(self, "Problem bounding coordinates",
                                msg)

        # Update map if coordinates are generally valid.
        if good_coords:
            self.add_rect()
        else:
            self.remove_rect()
            return

        self.update_map()

    def update_map(self):
        """
        Description:
            Generates and executes JavaScript to update the bounding
            box coordinates on the Leaflet map and fit the map view.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Formats the current coordinates into a JavaScript string.
            2. Executes the JS to update map variables and fit the view.

        Notes:
            None
        """

        jstr = """east = {eastbc};
        west = {westbc};
        south = {southbc};
        north = {northbc};
        updateMap();
        fitMap();
        """.format(
            **{
                "eastbc": self.ui.fgdc_eastbc.text(),
                "westbc": self.ui.fgdc_westbc.text(),
                "northbc": self.ui.fgdc_northbc.text(),
                "southbc": self.ui.fgdc_southbc.text(),
            }
        )
        self.evaluate_js(jstr)

    def add_rect(self):
        """
        Description:
            Executes JavaScript to draw the bounding box rectangle on
            the map.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Executes addRect() via runJavaScript.

        Notes:
            None
        """

        jstr = """addRect();"""
        self.evaluate_js(jstr)

    def remove_rect(self):
        """
        Description:
            Removes the bounding box rectangle from the map if one
            currently exists.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Checks "self.has_rect" flag and executes removeRect() JS.

        Notes:
            Updates "self.has_rect" to False.
        """

        if self.has_rect:
            self.has_rect = False
            jstr = """removeRect();"""
            self.evaluate_js(jstr)

    def evaluate_js(self, jstr):
        """
        Description:
            Executes a JavaScript string in the QWebEngineView page.

        Passed arguments:
            jstr (str): The JavaScript code to execute.

        Returned objects:
            None

        Workflow:
            Attempts to execute jstr. If it fails, executes jstr with
            the js_callback function.

        Notes:
            None
        """

        try:
            self.view.page().runJavaScript(jstr)
        except:
            self.view.page().runJavaScript(jstr, js_callback)

    @pyqtSlot(float, float)
    def on_ne_move(self, lat, lng):
        """
        Description:
            Handles movement of the North-East map marker, updating the
            North and East coordinate fields.

        Passed arguments:
            lat (float): New latitude (North).
            lng (float): New longitude (East).

        Returned objects:
            None

        Workflow:
            Updates UI fields using spatial_utils.format_bounding.

        Notes:
            Only runs if "self.in_xml_load" is True.
        """

        if self.in_xml_load:
            n, e = lat, lng
            try:
                s = float(self.ui.fgdc_southbc.text())
                w = float(self.ui.fgdc_westbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_eastbc.setText(bounds[1])
                self.ui.fgdc_northbc.setText(bounds[2])
            except:
                pass

    @pyqtSlot(float, float)
    def on_nw_move(self, lat, lng):
        """
        Description:
            Handles movement of the North-West map marker, updating the
            North and West coordinate fields.

        Passed arguments:
            lat (float): New latitude (North).
            lng (float): New longitude (West).

        Returned objects:
            None

        Workflow:
            Updates UI fields using spatial_utils.format_bounding.

        Notes:
            Only runs if "self.in_xml_load" is True.
        """

        if self.in_xml_load:
            n, w = lat, lng
            try:
                s = float(self.ui.fgdc_southbc.text())
                e = float(self.ui.fgdc_eastbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_westbc.setText(bounds[0])
                self.ui.fgdc_northbc.setText(bounds[2])
            except:
                pass

    @pyqtSlot(float, float)
    def on_se_move(self, lat, lng):
        """
        Description:
            Handles movement of the South-East map marker, updating the
            South and East coordinate fields.

        Passed arguments:
            lat (float): New latitude (South).
            lng (float): New longitude (East).

        Returned objects:
            None

        Workflow:
            Updates UI fields using spatial_utils.format_bounding.

        Notes:
            Only runs if "self.in_xml_load" is True.
        """

        if self.in_xml_load:
            s, e = lat, lng
            try:
                n = float(self.ui.fgdc_northbc.text())
                w = float(self.ui.fgdc_westbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_eastbc.setText(bounds[1])
                self.ui.fgdc_southbc.setText(bounds[3])
            except:
                pass

    @pyqtSlot(float, float)
    def on_sw_move(self, lat, lng):
        """
        Description:
            Handles movement of the South-West map marker, updating the
            South and West coordinate fields.

        Passed arguments:
            lat (float): New latitude (South).
            lng (float): New longitude (West).

        Returned objects:
            None

        Workflow:
            Updates UI fields using spatial_utils.format_bounding.

        Notes:
            Only runs if "self.in_xml_load" is True.
        """

        if self.in_xml_load:
            s, w = lat, lng
            try:
                n = float(self.ui.fgdc_northbc.text())
                e = float(self.ui.fgdc_eastbc.text())
                bounds = spatial_utils.format_bounding((w, e, n, s))

                self.ui.fgdc_westbc.setText(bounds[0])
                self.ui.fgdc_southbc.setText(bounds[3])
            except:
                pass

    def switch_schema(self, schema):
        """
        Description:
            Switches the visibility of schema-dependent fields, such as
            the geographical description field for "bdp" schema.

        Passed arguments:
            schema (str): The name of the schema to switch to.

        Returned objects:
            None

        Workflow:
            Sets the visibility of description widgets based on the
            schema type.

        Notes:
            None
        """

        self.schema = schema
        if schema == "bdp":
            self.ui.fgdc_descgeog.show()
            self.ui.descgeog_label.show()
            self.ui.descgeog_star.show()
        else:
            self.ui.fgdc_descgeog.hide()
            self.ui.descgeog_label.hide()
            self.ui.descgeog_star.hide()

    def all_good_coords(self):
        """
        Description:
            Checks if all four bounding coordinates are valid (numeric,
            within bounds, and North > South).

        Passed arguments:
            None

        Returned objects:
            bool: True if all coordinates are valid, False otherwise.

        Workflow:
            Attempts to convert all four fields to float and performs
            boundary checks.

        Notes:
            None
        """

        try:
            if -180 > float(self.ui.fgdc_westbc.text()) > 180:
                return False
            if -180 > float(self.ui.fgdc_eastbc.text()) > 180:
                return False
            if -90 > float(self.ui.fgdc_southbc.text()) > 90:
                return False
            if -90 > float(self.ui.fgdc_northbc.text()) > 90:
                return False
            if (float(self.ui.fgdc_northbc.text()) <=
                    float(self.ui.fgdc_southbc.text())):
                return False
            return True
        except:
            return False

    def clear_widget(self):
        """
        Description:
            Clears the widget content and state.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the parent class's clear_widget method.

        Notes:
            The map update logic is handled elsewhere.
        """

        super(self.__class__, self).clear_widget()

    def on_map_load_finished(self, ok):
        """
        Description:
            Called when the QWebEngineView page finishes loading.

        Passed arguments:
            ok (bool): True if the page loaded successfully.

        Returned objects:
            None

        Workflow:
            If successful and not previously loaded, initializes the
            map with the current coordinates and opens a popup.
            Sets "self.after_load" to True.

        Notes:
            Avoids repeated map initialization.
        """

        if ok and not self.after_load:
            # Now the map's JS should be ready to receive commands.
            if self.all_good_coords():
                jstr = "sw_marker.openPopup();"
                self.evaluate_js(jstr)
                time.sleep(2)  # This should not be required but not working.
                self.add_rect()
                self.update_map()
            self.after_load = True

    def showEvent(self, e):
        """
        Description:
            When the widget is shown ensure the map is properly updated and
            centered.

        Passed arguments:
            e (QShowEvent): The show event object.

        Returned objects:
            None

        Workflow:
            If the map has initialized, calls update_map to ensure
            centering and correct rectangle display.

        Notes:
            The primary map setup is now in on_map_load_finished.
        """

        # If the map has already been initialized, ensure it is centered.
        if self.after_load:
            self.update_map()
        super().showEvent(e)

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an XML element tree
            node for the <spdom> tag.

        Passed arguments:
            None

        Returned objects:
            spdom (lxml.etree._Element): The spatial domain XML node.

        Workflow:
            1. Creates <spdom> and <bounding> nodes.
            2. Appends <descgeog> if schema is 'bdp'.
            3. Appends all four boundary coordinates to <bounding>.
            4. Transfers any existing <boundalt> or <dsgpoly> nodes
               from the original XML.

        Notes:
            None
        """

        # Create the root <spdom> node.
        spdom = xml_node("spdom")

        # Add <descgeog> only if schema is 'bdp'
        if self.schema == "bdp":
            xml_node(
                "descgeog", text=self.ui.fgdc_descgeog.text(),
                parent_node=spdom
            )

            # Create and populate the <bounding> node.
            bounding = xml_node("bounding", parent_node=spdom)
            xml_node(
                "westbc", text=self.ui.fgdc_westbc.text(),
                parent_node=bounding
            )
            xml_node(
                "eastbc", text=self.ui.fgdc_eastbc.text(),
                parent_node=bounding
            )
            xml_node(
                "northbc", text=self.ui.fgdc_northbc.text(),
                parent_node=bounding
            )
            xml_node(
                "southbc", text=self.ui.fgdc_southbc.text(),
                parent_node=bounding
            )

            # Retain optional child elements from original XML.
            if self.original_xml is not None:
                boundalt = xml_utils.search_xpath(self.original_xml,
                                                  "bounding/boundalt")
                if boundalt is not None:
                    spdom.append(deepcopy(boundalt))

                dsgpoly_list = xml_utils.search_xpath(
                    self.original_xml, "dsgpoly", only_first=False
                )
                for dsgpoly in dsgpoly_list:
                    spdom.append(deepcopy(dsgpoly))

        return spdom

    def from_xml(self, spdom):
        """
        Description:
            Populates the widget fields from an XML element tree node.

        Passed arguments:
            spdom (lxml.etree._Element): The spatial domain XML node.

        Returned objects:
            None

        Workflow:
            1. Clears the current widget content.
            2. Populates fields using utility functions.
            3. Checks coordinates and updates the map (add/remove rect).
            4. Sets "self.in_xml_load" to True.

        Notes:
            None
        """

        self.in_xml_load = False
        self.original_xml = spdom
        self.clear_widget()
        utils.populate_widget(self, spdom)

        contents = xml_utils.node_to_dict(spdom, add_fgdc=False)
        if "bounding" in contents:
            contents = contents["bounding"]

        # Check coordinates and update map bounding box.
        try:
            if self.all_good_coords():
                self.add_rect()
                self.update_map()
            else:
                self.remove_rect()
        except KeyError:
            self.remove_rect()
        self.in_xml_load = True


def js_callback(result):
    """
    Description:
        Callback function for JavaScript execution results.

    Passed arguments:
        result (str): The result returned from the JavaScript execution.

    Returned objects:
        None

    Workflow:
        Simply prints the result to the console.

    Notes:
        None
    """

    # Print the result returned from runJavaScript.
    print(result)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    w = utils.launch_widget(Spdom)
