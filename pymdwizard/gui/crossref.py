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
    from pymdwizard.gui.citeinfo import Citeinfo
except ImportError as err:
    raise ImportError(err, __file__)


class Crossref(Citeinfo):
    """
    Description:
        A widget for managing the FGDC "cross reference" ("crossref")
        metadata element. Inherits from the Citeinfo widget but customizes
        its appearance and XML structure.

    Passed arguments:
        None (Inherits from Citeinfo's __init__)

    Returned objects:
        None

    Workflow:
        Overrides "Citeinfo.build_ui" to hide larger work fields and
        rename labels, then wraps the resulting "citeinfo" XML in a
        "crossref" tag during export.

    Notes:
        The "connect_events" method is redundant as it mirrors the
        parent's connection logic but is kept for explicit definition.
    """

    # Class attributes.
    drag_label = "Cross Reference <crossref>"
    acceptable_tags = ["crossref", "citeinfo"]

    def build_ui(self,):
        """
        Description:
            Build and modify this widget's GUI, overriding the parent's
            method to customize labels and hide unwanted elements.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the parent's "build_ui", sets the object name, hides
            larger work elements, and renames various labels to be
            contextually appropriate for a cross-reference.

        Notes:
            None
        """

        # Call the parent's UI build method.
        Citeinfo.build_ui(self)

        # Set specific object name for this widget instance.
        self.setObjectName("fgdc_crossref")

        # Hide the larger work citation section.
        self.ui.fgdc_lworkcit.hide()

        # Rename the primary title label.
        self.ui.lbl_dataset_title.setText("Crossref Title")

        # Hide internal labels (likely from parent Citeinfo).
        self.ui.label_34.hide()
        self.ui.label_38.hide()

        # Rename other specific labels.
        self.ui.label_47.setText("Author/Originator")
        self.ui.label_53.setText("Format")

        # Set a default geoform value.
        self.ui.fgdc_geoform.setCurrentText("publication")
        self.ui.label_51.setText("Online Link to the Publication")
        self.ui.label_53.setText(
            "Can you provide more publication information?"
        )
        self.ui.label_43.setText("Is this publication part of a series?")

    def connect_events(self):
        """
        Description:
            Connect the appropriate GUI components with the corresponding
            functions. (Redundant as parent handles this, but explicitly
            redefined here.)

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects radio button toggles to visibility change functions
            and the DOI button to the import function.

        Notes:
            Mirrors the parent class "Citeinfo.connect_events".
        """

        # Connect radio buttons to visibility handlers.
        self.ui.radio_lworkyes.toggled.connect(self.include_lworkext_change)
        self.ui.radio_seriesyes.toggled.connect(self.include_seriesext_change)
        self.ui.radio_pubinfoyes.toggled.connect(self.include_pubext_change)

        # Connect the DOI import button.
        self.ui.btn_import_doi.clicked.connect(self.get_doi_citation)

    def to_xml(self):
        """
        Description:
            Encapsulates the citation information in a "crossref" tag.

        Passed arguments:
            None

        Returned objects:
            crossref (xml.etree.ElementTree.Element): Cross reference
                element tag in XML tree.

        Workflow:
            Calls the parent "Citeinfo.to_xml" to get the "citeinfo"
            node, creates a "crossref" node, and appends "citeinfo" as
            its child.

        Notes:
            None
        """

        # Get the "citeinfo" element from the parent method.
        citeinfo = super().to_xml()

        # Create the parent "crossref" XML node.
        crossref = xml_utils.xml_node("crossref")

        # Append the "citeinfo" node as a child.
        crossref.append(citeinfo)

        return crossref

    def from_xml(self, citeinfo):
        """
        Description:
            Parse the XML code into the relevant citation elements.

        Passed arguments:
            xml_element (xml.etree.ElementTree.Element): The XML element
                containing citation ("citation", "crossref", or
                "citeinfo") details.

        Returned objects:
            None

        Workflow:
            1. Unwraps the "citeinfo" node if it is nested within
               "citation" or "crossref" tags.
            2. Calls the parent "Citeinfo.from_xml" to populate the UI.

        Notes:
            The parameter name was updated from "citeinfo" to
            "xml_element" for clarity since it might be a wrapper tag.
        """

        self.original_xml = citeinfo
        self.clear_widget()

        try:
            # Unwrap "citeinfo" if it is wrapped in "citation".
            if citeinfo.tag == "citation":
                citeinfo = citeinfo.xpath("citeinfo")[0]

            # Unwrap "citeinfo" if it is wrapped in "crossref".
            if citeinfo.tag == "crossref":
                citeinfo = citeinfo.xpath("citeinfo")[0]
            # Use the element directly if it's "citeinfo".
            elif citeinfo.tag != "citeinfo":
                print("The tag is not 'citation' or 'citeinfo'")
                return

            # Call the parent's implementation to populate UI fields.
            Citeinfo.from_xml(self, citeinfo)

        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Crossref, "Crossref testing")
