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
    from pymdwizard.core import utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_descript
    from pymdwizard.gui.abstract import Abstract
except ImportError as err:
    raise ImportError(err, __file__)


class Descript(WizardWidget):
    """
    Description:
        A widget container for the FGDC "description" section, specifically
        handling the "abstract" element. This widget acts as a simple
        wrapper for the "Abstract" child widget.
        Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Initializes the UI and embeds an instance of the "Abstract"
        widget. It delegates all XML serialization and parsing tasks to
        the child "Abstract" widget.

    Notes:
        None
    """

    # Class attributes.
    drag_label = "Abstract <abstract>"
    acceptable_tags = ["abstract"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the main UI, sets the object name, and creates
            and embeds the child "Abstract" widget.

        Notes:
            None
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_descript.Ui_fgdc_descript()

        # Set up the instantiated UI.
        self.ui.setupUi(self)

        # Set specific object name for this widget instance.
        self.setObjectName("fgdc_descript")

        # Instantiate the child widget for the abstract content.
        self.abstract = Abstract()

        # Add the abstract widget to the main layout.
        self.ui.verticalLayout.addWidget(self.abstract)

    def to_xml(self):
        """
        Description:
            Returns the XML representation of the abstract content by
            delegating to the child "Abstract" widget.

        Passed arguments:
            None

        Returned objects:
            abstract (xml.etree.ElementTree.Element): The abstract
                element tag in the XML tree.

        Workflow:
            Calls the "to_xml" method of the embedded "Abstract" widget.

        Notes:
            None
        """

        # Delegate XML creation to the child widget.
        return self.abstract.to_xml()

    def from_xml(self, abstract):
        """
        Description:
            Parse the XML code into the relevant abstract elements by
            delegating to the child "Abstract" widget.

        Passed arguments:
            abstract (xml.etree.ElementTree.Element): The XML element
                containing the abstract content.

        Returned objects:
            None

        Workflow:
            Calls the "from_xml" method of the embedded "Abstract" widget
            to populate the UI fields.

        Notes:
            The original docstring mentioned "access_constraints" which
            was replaced with "abstract" for relevance.
        """

        # Delegate XML parsing to the child widget.
        self.abstract.from_xml(abstract)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Descript, "Abstract testing")
