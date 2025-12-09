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
from copy import deepcopy

# Non-standard python libraries.
try:
    from PyQt5.QtWidgets import QHBoxLayout
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_IdInfo
    from pymdwizard.gui.PointOfContact import ContactInfoPointOfContact
    from pymdwizard.gui.Taxonomy import Taxonomy
    from pymdwizard.gui.Keywords import Keywords
    from pymdwizard.gui.accconst import Accconst
    from pymdwizard.gui.useconst import Useconst
    from pymdwizard.gui.Status import Status
    from pymdwizard.gui.timeperd import Timeperd
    from pymdwizard.gui.citeinfo import Citeinfo
    from pymdwizard.gui.datacred import Datacred
    from pymdwizard.gui.descript import Descript
    from pymdwizard.gui.supplinf import SupplInf
    from pymdwizard.gui.native import Native
    from pymdwizard.gui.purpose import Purpose
    from pymdwizard.gui.crossref_list import Crossref_list
except ImportError as err:
    raise ImportError(err, __file__)


class IdInfo(WizardWidget):
    """
    Description:
        A widget for managing the entire FGDC "Identification Information"
        ("idinfo") metadata section. This acts as a container for many
        other essential widgets like citation, keywords, and contacts.
        Inherits from WizardWidget.

    Passed arguments:
        root_widget (QWidget, optional): The root metadata widget
            container (e.g., the main application window).
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes and builds all necessary child widgets (citation,
           status, timeperd, etc.).
        2. Arranges these child widgets into a two-column layout.
        3. Provides methods for schema switching (e.g., hiding taxonomy
           for non-BDP schemas).

    Notes:
        The children() method is overridden to include the separate
        "spdom" (Spatial Domain) widget for validation purposes.
    """
    # Class attributes.
    drag_label = "Identification Information <idinfo>"
    acceptable_tags = ["idinfo"]

    # Assumed UI class for instantiation.
    ui_class = UI_IdInfo.Ui_fgdc_idinfo

    def __init__(self, root_widget=None, parent=None):
        # Initialize the parent class.
        super(self.__class__, self).__init__(parent=parent)
        self.schema = "bdp"
        self.root_widget = root_widget

        # Store reference to the scroll area.
        self.scroll_area = self.ui.idinfo_scroll_area

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, creates all child widgets, and inserts
            them into the two-column layout using "insertWidget" or
            "insertLayout" to control display order.

        Notes:
            Widgets are inserted in reverse visual order (bottom to top
            of the layout) for easier code readability when using the
            "insertWidget" method.
        """

        self.ui = self.ui_class()
        self.ui.setupUi(self)

        self.setup_dragdrop(self)

        # Initialize all child widgets for point of contact.
        self.ptcontac = ContactInfoPointOfContact(parent=self)
        self.taxonomy = Taxonomy(parent=self)
        self.keywords = Keywords(parent=self)
        self.accconst = Accconst(parent=self)
        self.useconst = Useconst(parent=self)
        self.status = Status(parent=self)
        self.timeperd = Timeperd(parent=self)
        self.citation = Citeinfo(parent=self)

        # Hide DOI import button for now.
        self.citation.ui.btn_import_doi.hide()

        # Initialize other information, such as data credit, abstract, purpose,
        # supplemental, and native environment.
        self.datacredit = Datacred(parent=self)
        self.descript = Descript(parent=self)
        self.purpose = Purpose(parent=self)
        self.supplinf = SupplInf(parent=self)
        self.native = Native(parent=self)

        # --- Layout Arrangement ---
        # Add citation widget directly to its container.
        self.ui.fgdc_citation.layout().addWidget(self.citation)

        # Combine status and timeperd into a horizontal box.
        time_hbox = QHBoxLayout()
        time_hbox.addWidget(self.status)
        time_hbox.addWidget(self.timeperd)

        # Insert widgets into the left column (bottom to top).
        self.ui.two_column_left.layout().insertWidget(0, self.native)
        self.ui.two_column_left.layout().insertLayout(0, time_hbox)
        self.ui.two_column_left.layout().insertWidget(0, self.datacredit)
        self.ui.two_column_left.layout().insertWidget(0, self.taxonomy)
        self.ui.two_column_left.layout().insertWidget(0, self.ptcontac)
        self.ui.two_column_left.layout().insertWidget(0, self.useconst)
        self.ui.two_column_left.layout().insertWidget(0, self.accconst)

        # Insert widgets into the right column (bottom to top).
        self.ui.two_column_right.layout().insertWidget(0, self.supplinf)
        self.ui.two_column_right.layout().insertWidget(0, self.keywords)
        self.ui.two_column_right.layout().insertWidget(0, self.purpose)
        self.ui.two_column_right.layout().insertWidget(0, self.descript)

        # Add the cross-reference list to its container.
        self.crossref_list = Crossref_list()
        self.ui.help_crossref.layout().addWidget(self.crossref_list)

    def children(self):
        """
        Description:
            Overrides the base method to include child widgets that are
            not strictly part of the IDInfo widget's layout, but whose
            content should be managed/validated by the root widget.

        Passed arguments:
            None

        Returned objects:
            list: List of child QWidgets.

        Workflow:
            Returns the base list of children plus the Spatial Domain
            (spdom) widget from the root widget.

        Notes:
            None
        """

        return super().children() + [
            self.root_widget.spatial_tab.spdom
        ]

    def switch_schema(self, schema):
        """
        Description:
            Hides or shows sections based on the active metadata schema.

        Passed arguments:
            schema (str): The current metadata schema name.

        Returned objects:
            None

        Workflow:
            If schema is "bdp", show the "Taxonomy" widget; otherwise,
            hide it.

        Notes:
            None
        """

        self.schema = schema
        if schema == "bdp":
            self.taxonomy.show()
        else:
            self.taxonomy.hide()

    def clear_widget(self):
        """
        Description:
            Clears all content from the IDInfo widget and associated
            widgets like Spatial Domain.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Clears the Spatial Domain and Taxonomy widgets, and then
            calls the base "WizardWidget.clear_widget" method.

        Notes:
            None
        """

        # Clear the Spatial Domain widget (managed separately).
        self.root_widget.spatial_tab.spdom.clear_widget()

        # Clear and hide the taxonomy (set radio button to no).
        self.taxonomy.clear_widget()
        self.taxonomy.ui.rbtn_no.setChecked(True)

        # Clear all other managed widgets.
        WizardWidget.clear_widget(self)

    def to_xml(self):
        """
        Description:
            Encapsulates the identification information into a single
            "idinfo" XML element tag.

        Passed arguments:
            None

        Returned objects:
            idinfo_node (ElementTree.Element): Identification
                information element tag in XML tree.

        Workflow:
            1. Creates the <idinfo> parent node.
            2. Appends XML nodes generated by each child widget.
            3. Conditionally includes elements like <spdom>,
               <taxonomy>, and legacy/retained elements ("browse",
               "secinfo", "tool").

        Notes:
            Assumes all child widgets have a to_xml() method.
        """

        # Create the parent "idinfo" XML node.
        idinfo_node = xml_utils.xml_node("idinfo")

        # --- CITATION ---
        citation_node = xml_utils.xml_node("citation",
                                           parent_node=idinfo_node)
        citeinfo_node = self.citation.to_xml()
        citation_node.append(citeinfo_node)
        idinfo_node.append(citation_node)

        # --- DESCRIPT (abstract, purpose, supplinf) ---
        descript_node = xml_utils.xml_node("descript",
                                           parent_node=idinfo_node)
        descript_node.append(self.descript.to_xml())
        descript_node.append(self.purpose.to_xml())
        supplinf_node = self.supplinf.to_xml()
        if supplinf_node.text is not None:
            descript_node.append(supplinf_node)
        idinfo_node.append(descript_node)

        # --- TIMEPERD and STATUS ---
        idinfo_node.append(self.timeperd.to_xml())
        idinfo_node.append(self.status.to_xml())

        # --- SPATIAL DOMAIN (if used) ---
        if self.root_widget.use_spatial:
            spdom_node = self.root_widget.spatial_tab.spdom.to_xml()
            idinfo_node.append(spdom_node)

        # --- KEYWORDS ---
        idinfo_node.append(self.keywords.to_xml())

        # --- TAXONOMY (if schema=bdp and has content) ---
        if self.schema == "bdp" and self.taxonomy.has_content():
            idinfo_node.append(self.taxonomy.to_xml())

        # --- CONSTRAINTS ---
        idinfo_node.append(self.accconst.to_xml())
        idinfo_node.append(self.useconst.to_xml())

        # --- POINT OF CONTACT (if has content) ---
        if self.ptcontac.has_content():
            idinfo_node.append(self.ptcontac.to_xml())

        # --- PRESERVATION OF ORIGINAL TAGS (browse, secinfo, tool) ---

        # <browse>
        if self.original_xml is not None:
            browse = xml_utils.search_xpath(self.original_xml, "browse")
            if browse is not None:
                browse.tail = None
                idinfo_node.append(deepcopy(browse))

        # <datacred> (if has text)
        datacredit_node = self.datacredit.to_xml()
        if datacredit_node.text:
            idinfo_node.append(datacredit_node)

        # <secinfo>
        if self.original_xml is not None:
            secinfo = xml_utils.search_xpath(self.original_xml,
                                             "secinfo")
            if secinfo is not None:
                secinfo.tail = None
                idinfo_node.append(deepcopy(secinfo))

        # <native> (if has content)
        if self.native.has_content():
            idinfo_node.append(self.native.to_xml())

        # <crossref> list
        if self.crossref_list.has_content():
            for crossref in self.crossref_list.get_children():
                idinfo_node.append(crossref.to_xml())

        # <tool> list
        if self.original_xml is not None:
            tools = xml_utils.search_xpath(
                self.original_xml, "tool", only_first=False
            )
            for tool in tools:
                tool.tail = None
                idinfo_node.append(deepcopy(tool))

        return idinfo_node

    def from_xml(self, xml_idinfo):
        """
        Description:
            Parses the XML code into the relevant identification
            information elements by calling the "from_xml" method on each
            child widget.

        Passed arguments:
            xml_idinfo (ElementTree.Element): The XML element
                containing the identification information.

        Returned objects:
            None

        Workflow:
            Uses "xml_utils.search_xpath" to find the correct child
            node for each widget and passes it to the child's "from_xml"
            method.

        Notes:
            None
        """

        self.original_xml = xml_idinfo

        # --- CITATION ---
        citation = xml_utils.search_xpath(xml_idinfo, "citation")
        if citation is not None:
            self.citation.from_xml(citation)

        # --- DESCRIPT (abstract, purpose, supplinf) ---
        abstract = xml_utils.search_xpath(xml_idinfo,
                                          "descript/abstract")
        if abstract is not None:
            self.descript.from_xml(abstract)

        purpose = xml_utils.search_xpath(xml_idinfo,
                                         "descript/purpose")
        if purpose is not None:
            self.purpose.from_xml(purpose)

        supplinf = xml_utils.search_xpath(xml_idinfo,
                                          "descript/supplinf")
        if supplinf is not None:
            self.supplinf.from_xml(supplinf)

        # --- TIMEPERD and STATUS ---
        timeperd = xml_utils.search_xpath(xml_idinfo, "timeperd")
        if timeperd is not None:
            self.timeperd.from_xml(timeperd)

        status = xml_utils.search_xpath(xml_idinfo, "status")
        if status is not None:
            self.status.from_xml(status)

        # --- SPATIAL DOMAIN ---
        spdom = xml_utils.search_xpath(xml_idinfo, "spdom")
        if spdom is not None:
            self.root_widget.spatial_tab.spdom.from_xml(spdom)

        # --- KEYWORDS and TAXONOMY ---
        keywords = xml_utils.search_xpath(xml_idinfo, "keywords")
        if keywords is not None:
            self.keywords.from_xml(keywords)

        taxonomy = xml_utils.search_xpath(xml_idinfo, "taxonomy")
        if taxonomy is not None:
            self.taxonomy.from_xml(taxonomy)

        # --- CONSTRAINTS ---
        accconst = xml_utils.search_xpath(xml_idinfo, "accconst")
        if accconst is not None:
            self.accconst.from_xml(accconst)

        useconst = xml_utils.search_xpath(xml_idinfo, "useconst")
        if useconst is not None:
            self.useconst.from_xml(useconst)

        # --- CONTACT and CREDIT ---
        ptcontac = xml_utils.search_xpath(xml_idinfo, "ptcontac")
        if ptcontac is not None:
            self.ptcontac.from_xml(ptcontac)

        datacred = xml_utils.search_xpath(xml_idinfo, "datacred")
        if datacred is not None:
            self.datacredit.from_xml(datacred)

        # --- NATIVE and CROSSREF ---
        native = xml_utils.search_xpath(xml_idinfo, "native")
        if native is not None:
            self.native.from_xml(native)

        crossref = xml_utils.search_xpath(xml_idinfo, "crossref")
        # crossref list can only be populated by passing the parent node
        if crossref is not None:
            self.crossref_list.from_xml(xml_idinfo)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(IdInfo, "IdInfo testing")
