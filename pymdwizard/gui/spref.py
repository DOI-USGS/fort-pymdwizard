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
    from PyQt5.QtWidgets import (QLineEdit, QLabel, QComboBox)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, spatial_utils, fgdc_utils)
    from pymdwizard.core.xml_utils import xml_node
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_spref
    from pymdwizard.gui.mapproj import MapProj
    from pymdwizard.gui.vertdef import Vertdef
except ImportError as err:
    raise ImportError(err, __file__)


class SpRef(WizardWidget):
    """
    Description:
        A widget corresponding to the FGDC <spref> tag, managing
        all components of the **Spatial Reference** system definition:
        horizontal system (geographic, planar, or local) and vertical
        system.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds widgets for projection parameters ("MapProj") and
           vertical definition ("Vertdef").
        2. Uses stacked widgets and radio buttons to manage the
           mutually exclusive horizontal system definitions.
        3. Dynamically loads and displays required parameters for
           Map Projections and Grid Systems.

    Notes:
        Inherits from "WizardWidget". The "to_xml" and "from_xml"
        methods handle the complex nesting of "<horizsys>" and
        "<vertdef>".
    """

    # Class attributes.
    drag_label = "Spatial Reference <spref>"
    acceptable_tags = ["spref"]

    # Assign the UI class.
    ui_class = UI_spref.Ui_fgdc_spref

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            embedding child widgets and populating dropdowns.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up drag-and-drop, populates map
            projection and grid system lists, embeds "MapProj" and
            "Vertdef" widgets, and sets initial state.

        Notes:
            None
        """

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        # Enable drag and drop functionality.
        self.setup_dragdrop(self, enable=True)

        # Populate Map Projection dropdown list.
        self.ui.fgdc_mapprojn.addItems(spatial_utils.PROJECTION_LOOKUP.keys())

        # Embed MapProj widget for Projection (mapproj).
        self.mapproj = MapProj()
        self.ui.fgdc_mapproj.layout().addWidget(self.mapproj)

        # Embed MapProj widget for Grid System (gridsys).
        self.grid_mapproj = MapProj()
        self.ui.fgdc_gridsys.layout().addWidget(self.grid_mapproj)

        # Populate Grid System dropdown list.
        self.ui.fgdc_gridsysn.addItems(spatial_utils.GRIDSYS_LOOKUP.keys())

        # Embed Vertical Definition widget.
        self.vertdef = Vertdef()
        self.vertdef.ui.rbtn_no.setChecked(True)

        # Add vertdef to the main widget layout.
        self.layout().addWidget(self.vertdef)

        # Clear fields and reset state.
        self.clear_widget()

        # Set a default projection for a better starting view.
        self.ui.fgdc_mapprojn.setCurrentText("Transverse Mercator")

    def connect_events(self):
        """
        Description:
            Connects UI signals to the corresponding handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects radio buttons for visibility and system type
            switching, and comboboxes for dynamic loading of projection/
            grid system parameters.

        Notes:
            None
        """

        # Connect "Yes" radio button to show/hide content.
        self.ui.rbtn_yes.toggled.connect(self.spref_used_change)

        # Connect horizontal system definition radio buttons.
        self.ui.btn_geographic.toggled.connect(self.system_def_changed)
        self.ui.btn_local.toggled.connect(self.system_def_changed)
        # Note: btn_planar is connected via btn_geographic/local toggle

        # Connect planar subgroup radio buttons.
        self.ui.btngrp_planar.buttonClicked.connect(self.planar_changed)

        # Connect projection dropdown to load parameter fields.
        self.ui.fgdc_mapprojn.currentIndexChanged.connect(self.load_projection)
        self.load_projection()

        # Connect grid system dropdown to load parameter fields.
        self.ui.fgdc_gridsysn.currentIndexChanged.connect(self.load_gridsys)
        self.load_gridsys()

        # Connect horizontal datum dropdown to load ellipse parameters.
        self.ui.fgdc_horizdn.currentIndexChanged.connect(self.load_datum)
        self.load_datum()

    def clear_widget(self):
        """
        Description:
            Clears all content from this widget and resets UI state.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls base class clear, resets system definition to
            Geographic, sets "No" radio button, and hides content.

        Notes:
            None
        """

        WizardWidget.clear_widget(self)

        # Reset to Geographic definition.
        self.ui.btn_geographic.setChecked(True)

        # Reset usage radio button.
        self.ui.rbtn_no.setChecked(True)

        # Hide content.
        self.spref_used_change(False)

    def spref_used_change(self, b):
        """
        Description:
            Shows or hides the horizontal system content widget based
            on the "Yes" radio button state.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Calls horiz_layout.show() or horiz_layout.hide().

        Notes:
            None
        """

        if b:
            # Show the horizontal spatial reference content.
            self.ui.horiz_layout.show()
        else:
            # Hide the horizontal spatial reference content.
            self.ui.horiz_layout.hide()

    def has_content(self):
        """
        Description:
            Checks if the widget contains content that should be
            written to XML.

        Passed arguments:
            None

        Returned objects:
            bool: True if the "Yes" radio button is checked, False otherwise.

        Workflow:
            Returns the state of the "Yes" radio button.

        Notes:
            None
        """

        return self.ui.rbtn_yes.isChecked()

    def system_def_changed(self):
        """
        Description:
            Switches the main stacked widget to show fields for Geographic,
            Planar, or Local horizontal systems.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets stack index based on the checked radio button.

        Notes:
            Index 0: Geographic, Index 1: Planar, Index 2: Local.
        """

        self.sender().objectName()

        if self.ui.btn_geographic.isChecked():
            # Show Geographic fields.
            self.ui.stack_definition.setCurrentIndex(0)
        elif self.ui.btn_planar.isChecked():
            # Show Planar fields.
            self.ui.stack_definition.setCurrentIndex(1)
        else:
            # Show Local fields.
            self.ui.stack_definition.setCurrentIndex(2)

    def planar_changed(self):
        """
        Description:
            Switches the planar stacked widget to show fields for
            Map Projection, Grid System, or Local Planar.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets planar stack index based on the checked planar radio
            button.

        Notes:
            Index 0: Projection, Index 1: Grid System, Index 2: Local.
        """

        if self.ui.btn_localp.isChecked():
            index = 2
        elif self.ui.btn_projection.isChecked():
            index = 0
        else:
            index = 1
        self.ui.stack_planar.setCurrentIndex(index)

    def load_projection(self):
        """
        Description:
            Loads the appropriate "MapProj" child widget parameters based
            on the selected Map Projection name.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Retrieves projection shortname from "spatial_utils" lookup
            and passes it to self.mapproj.load_projection.

        Notes:
            None
        """

        projection_name = self.ui.fgdc_mapprojn.currentText()
        try:
            projection = spatial_utils.PROJECTION_LOOKUP[projection_name]

            # Load the necessary MapProj fields.
            self.mapproj.load_projection(projection["shortname"])
        except:
            pass

    def load_gridsys(self):
        """
        Description:
            Dynamically generates form fields for the selected Grid
            System and updates the embedded "MapProj" for the grid's
            projection.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Clears existing grid parameter fields.
            2. Iterates over required elements from the "GRIDSYS_LOOKUP".
            3. Creates a "QLabel" and a "QLineEdit" for each parameter.
            4. Loads the grid system's underlying projection into
               self.grid_mapproj.

        Notes:
            None
        """

        gridsys_name = self.ui.fgdc_gridsysn.currentText()
        projection = spatial_utils.GRIDSYS_LOOKUP[gridsys_name]
        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        layout = self.ui.gridsys_contents.layout()

        # Clear existing dynamic fields.
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Create new fields for the selected Grid System.
        for param in projection["elements"]:
            try:
                # Look up long name and annotation.
                long_name = annotation_lookup[param]["long_name"]
                annotation = annotation_lookup[param]["annotation"]
            except:
                long_name = param
                annotation = "Unknown"

            # Create and setup QLabel.
            label = QLabel(long_name)
            label.setToolTip(annotation)
            label.help_text = annotation

            # Create and setup QLineEdit.
            lineedit = QLineEdit("...")
            lineedit.setObjectName("fgdc_" + param)
            lineedit.setToolTip(annotation)

            # Add to the form layout.
            layout.addRow(label, lineedit)

        # Update the grid system's underlying projection widget.
        gridsys_proj = spatial_utils.PROJECTION_LOOKUP[projection["projection"]]
        self.grid_mapproj.load_projection(gridsys_proj["shortname"])

    def load_datum(self):
        """
        Description:
            Populates the horizontal datum's ellipsoid parameters
            (ellips, semiaxis, denflat) based on the selected datum name.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Retrieves datum parameters from "spatial_utils" lookup and
            sets text/current text for the corresponding UI fields.

        Notes:
            None
        """

        datum_names = spatial_utils.DATUM_LOOKUP.keys()
        datum_name = self.ui.fgdc_horizdn.currentText()
        if datum_name in datum_names:
            datum_params = spatial_utils.DATUM_LOOKUP[datum_name]

            # Set ellipsoid and axis parameters.
            self.ui.fgdc_ellips.setCurrentText(datum_params["ellips"])
            self.ui.fgdc_semiaxis.setText(datum_params["semiaxis"])
            self.ui.fgdc_denflat.setText(datum_params["denflat"])

    def has_content(self):
        """ Currently, no used.""" # ????????????????????????????????????????????????????????????????

        return self.ui.rbtn_yes.isChecked()

    def to_xml(self):
        """
        Description:
            Converts the spatial reference content into an FGDC
            <spref> XML element, including horizontal and vertical
            system definitions.

        Passed arguments:
            None

        Returned objects:
            spref_node (lxml.etree._Element): The complete <spref>
                element tag.

        Workflow:
            1. Creates <spref> and <horizsys>.
            2. Builds one of <geograph>, <planar>, or <local>
               based on selection.
            3. Builds <geodetic> if horizontal datum is provided.
            4. Appends <vertdef> if content exists.

        Notes:
            None
        """

        # Create the root <spref> node.
        spref_node = xml_node("spref")
        horizsys = xml_node("horizsys", parent_node=spref_node)

        # --- GEOGRAPHIC System ---
        if self.ui.btn_geographic.isChecked():
            geograph = xml_node("geograph", parent_node=horizsys)

            # Extract Geographic Resolution and Unit.
            latres_str = self.findChild(QLineEdit, "fgdc_latres").text()
            xml_node("latres", latres_str, geograph)
            longres_str = self.findChild(QLineEdit,
                                         "fgdc_longres").text()
            xml_node("longres", longres_str, geograph)
            geogunit_str = self.findChild(QComboBox,
                                          "fgdc_geogunit").currentText()
            xml_node("geogunit", geogunit_str, geograph)

        # --- PLANAR System ---
        elif self.ui.btn_planar.isChecked():
            planar = xml_node("planar", parent_node=horizsys)

            if self.ui.btn_projection.isChecked():
                # Map Projection.
                mapproj = xml_node("mapproj", parent_node=planar)
                projection_name = self.ui.fgdc_mapprojn.currentText()
                xml_node("mapprojn", text=projection_name,
                         parent_node=mapproj)
                proj = self.mapproj.to_xml()
                mapproj.append(proj)
            elif self.ui.btn_grid.isChecked():
                # Grid System.
                gridsys = xml_node("gridsys", parent_node=planar)
                gridsys_name = self.ui.fgdc_gridsysn.currentText()
                gridsys_info = spatial_utils.GRIDSYS_LOOKUP[gridsys_name]

                xml_node("gridsysn", text=gridsys_name,
                         parent_node=gridsys)

                # Create specific grid system node (e.g., <utm>).
                root_node = xml_node(gridsys_info["shortname"],
                                     parent_node=gridsys)

                # Add dynamic grid system parameters.
                for item in gridsys_info["elements"]:
                    widget = self.findChild(QLineEdit,
                                            "fgdc_" + item).text()
                    xml_node(item, text=widget, parent_node=root_node)

                # Append grid system's underlying projection parameters.
                proj = self.grid_mapproj.to_xml()
                root_node.append(proj)
            else:
                # Local Planar.
                localp = xml_node("localp", parent_node=planar)
                localpd_str = self.ui.fgdc_localpd.text()
                xml_node("localpd", localpd_str, parent_node=localp)
                localpgi_str = self.ui.fgdc_localpgi.text()
                xml_node("localpgi", localpgi_str, parent_node=localp)

            # Planar Coordinate Information (<planci>)
            planci = xml_node("planci", parent_node=planar)
            xml_node(
                "plance",
                text=self.ui.fgdc_plance.currentText(),
                parent_node=planci,
            )
            coordrep = xml_node("coordrep", parent_node=planci)
            xml_node("absres", text=self.ui.fgdc_absres.text(),
                     parent_node=coordrep)
            xml_node("ordres", text=self.ui.fgdc_ordres.text(),
                     parent_node=coordrep)
            xml_node(
                "plandu", text=self.ui.fgdc_plandu.currentText(),
                parent_node=planci
            )

        # --- LOCAL System ---
        else:
            local = xml_node("local", parent_node=horizsys)
            xml_node("localdes", text=self.ui.fgdc_localdes.text(),
                     parent_node=local)
            xml_node("localgeo", text=self.ui.fgdc_localgeo.text(),
                     parent_node=local)

        # --- GEODETIC Model (applies to Geographic and Planar) ---
        if self.findChild(QComboBox, "fgdc_horizdn").currentText():
            geodetic = xml_node("geodetic", parent_node=horizsys)
            horizdn_str = self.findChild(QComboBox, "fgdc_horizdn").currentText()
            xml_node("horizdn", horizdn_str, geodetic)
            ellips_str = self.findChild(QComboBox, "fgdc_ellips").currentText()
            xml_node("ellips", ellips_str, geodetic)
            semiaxis_str = self.findChild(QLineEdit, "fgdc_semiaxis").text()
            xml_node("semiaxis", semiaxis_str, geodetic)
            denflat_str = self.findChild(QLineEdit, "fgdc_denflat").text()
            xml_node("denflat", denflat_str, geodetic)

        # --- VERTICAL Definition ---
        if self.vertdef.has_content():
            spref_node.append(self.vertdef.to_xml())

        return spref_node

    def from_xml(self, spref_node):
        """
        Description:
            Parses an FGDC <spref> XML element and populates the
            widget's fields for horizontal and vertical definitions.

        Passed arguments:
            spref_node (lxml.etree._Element): The <spref> XML element.

        Returned objects:
            None

        Workflow:
            1. Clears content and sets "Yes" radio button.
            2. Checks for <geograph>, <local>, and <planar>.
            3. Populates horizontal definition and coordinate units.
            4. Populates <geodetic> model.
            5. Passes <vertdef> to the child widget.

        Notes:
            Uses "xml_utils.search_xpath" and "utils.populate_widget_element".
        """

        self.clear_widget()
        if spref_node.tag == "spref":
            self.original_xml = spref_node

            self.ui.rbtn_yes.setChecked(True)

            # --- GEOGRAPHIC System ---
            geograph = xml_utils.search_xpath(spref_node,
                                              "horizsys/geograph")
            if geograph is not None:
                self.ui.btn_planar.setChecked(True)
                self.ui.btn_geographic.setChecked(True)

                utils.populate_widget_element(self.ui.fgdc_latres, geograph,
                                              "latres")
                utils.populate_widget_element(self.ui.fgdc_longres, geograph,
                                              "longres")
                utils.populate_widget_element(
                    self.ui.fgdc_geogunit, geograph, "geogunit"
                )

            # --- LOCAL System (Horizontal) ---
            local = xml_utils.search_xpath(spref_node, "horizsys/local")
            if local is not None:
                self.ui.btn_planar.setChecked(True)
                self.ui.btn_local.setChecked(True)

                utils.populate_widget_element(self.ui.fgdc_localdes, local,
                                              "localdes")
                utils.populate_widget_element(self.ui.fgdc_localgeo, local,
                                              "localgeo")

            # --- PLANAR System ---
            planar = xml_utils.search_xpath(spref_node,
                                            "horizsys/planar")
            if planar is not None:
                self.ui.btn_grid.setChecked(True)
                self.ui.btn_planar.setChecked(True)

                # Map Projection within Planar.
                mapproj = xml_utils.search_xpath(planar, "mapproj")
                if mapproj is not None:
                    self.ui.btn_projection.setChecked(True)

                    utils.populate_widget_element(
                        self.ui.fgdc_mapprojn, mapproj, "mapprojn"
                    )
                    mapproj_children = mapproj.getchildren()

                    # Pass projection parameters to MapProj widget.
                    if len(mapproj_children) > 1:
                        self.mapproj.from_xml(mapproj_children[1])

                # Grid System within Planar.
                gridsys = xml_utils.search_xpath(planar, "gridsys")
                if gridsys is not None:
                    self.ui.btn_grid.setChecked(True)
                    xml_utils.search_xpath(gridsys, "gridsysn")
                    utils.populate_widget_element(
                        self.ui.fgdc_gridsysn, gridsys, "gridsysn"
                    )

                    gridsys_children = gridsys.getchildren()
                    if len(gridsys_children) > 1:
                        # Get the <gridsysn> tag's children.
                        gridsys_contents = gridsys.getchildren()[1]
                    else:
                        gridsys_contents = []
                    for item in gridsys_contents.getchildren():
                        tag = item.tag

                        # Check if tag is a known projection parameter.
                        if spatial_utils.lookup_shortname(tag) is not None:
                            self.grid_mapproj.from_xml(item)

                        # Check for nested mapproj.
                        elif tag == "mapproj":
                            mapprojn = xml_utils.search_xpath(item,
                                                              "mapprojn")
                            if mapprojn.text in spatial_utils.PROJECTION_LOOKUP:
                                self.grid_mapproj.from_xml(item.getchildren()[1])
                        else:
                            # Populate dynamic grid parameters.
                            item_widget = self.findChild(QLineEdit,
                                                         "fgdc_" + tag)
                            utils.set_text(item_widget, item.text)

                    grid_proj = gridsys.xpath("proj")

                # Local Planar within Planar.
                localp = xml_utils.search_xpath(planar, "localp")
                if localp:
                    self.ui.btn_localp.setChecked(True)
                    utils.populate_widget_element(
                        self.ui.fgdc_localpd, localp, "localpd"
                    )
                    utils.populate_widget_element(
                        self.ui.fgdc_localpgi, localp, "localpgi"
                    )

                # Planar Coordinate Information (<planci>).
                utils.populate_widget_element(
                    self.ui.fgdc_plance, planar, "planci/plance"
                )
                utils.populate_widget_element(
                    self.ui.fgdc_plandu, planar, "planci/plandu"
                )
                utils.populate_widget_element(
                    self.ui.fgdc_absres, planar, "planci/coordrep/absres"
                )
                utils.populate_widget_element(
                    self.ui.fgdc_ordres, planar, "planci/coordrep/ordres"
                )

                self.planar_changed()

            # --- GEODETIC Model (Datum/Ellipsoid) ---
            geodetic = xml_utils.search_xpath(spref_node,
                                              "horizsys/geodetic")
            if geodetic is not None:
                utils.populate_widget_element(self.ui.fgdc_horizdn, geodetic,
                                              "horizdn")
                utils.populate_widget_element(self.ui.fgdc_ellips, geodetic,
                                              "ellips")
                utils.populate_widget_element(
                    self.ui.fgdc_semiaxis, geodetic, "semiaxis"
                )
                utils.populate_widget_element(self.ui.fgdc_denflat, geodetic,
                                              "denflat")

            # --- VERTICAL Definition ---
            vertdef = xml_utils.search_xpath(spref_node, "vertdef")
            if vertdef is not None:
                self.vertdef.from_xml(vertdef)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SpRef, "spref testing")
