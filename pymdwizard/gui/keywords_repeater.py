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
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.ui_files import UI_keywords_repeater
except ImportError as err:
    raise ImportError(err, __file__)


class KeywordsRepeater(WizardWidget):
    """
    Description:
        A reusable widget that manages a list of repeatable keyword
        elements associated with a single thesaurus or source.
        Inherits from WizardWidget.

    Passed arguments:
        thesaurus_label (str): Label for the thesaurus/source input field.
        keywords_label (str): Label for the individual keyword input lines.
        line_name (str): Object name for the keyword input line widgets.
        spellings (bool): If True, enables spelling/autocomplete features
            on the keyword input line.
        parent (QWidget, optional): Parent widget.

    Returned objects:
        None

    Workflow:
        1. Stores initialization parameters.
        2. Builds a UI that includes a thesaurus field and a
           "RepeatingElement" container for the keywords.
        3. Allows dynamic addition of keyword input lines.

    Notes:
        None
    """

    # Class attribute, often overridden by parent container.
    drag_label = "NA <NA>"

    def __init__(
        self,
        thesaurus_label="Thesaurus",
        keywords_label="Keywords:",
        line_name="kw",
        spellings=True,
        parent=None,
    ):
        # Store initialization parameters.
        self.thesaurus_label = thesaurus_label
        self.keywords_label = keywords_label
        self.line_name = line_name
        self.keywords = None
        self.spellings = spellings

        # Initialize the parent WizardWidget class.
        WizardWidget.__init__(self, parent=parent)

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Instantiates the UI, sets up drag-and-drop, creates the
            "RepeatingElement" for keywords, and inserts it into the
            layout.

        Notes:
            None
        """

        # Instantiate and setup the UI.
        self.ui = UI_keywords_repeater.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        # Set the thesaurus label text.
        self.ui.thesaurus_label = self.thesaurus_label

        # Arguments to be passed to each individual keyword widget.
        widget_kwargs = {
            "label": self.keywords_label,
            "line_name": self.line_name,
            "required": True,
            "spellings": self.spellings,
        }

        # Create the RepeatingElement container for keywords.
        self.keywords = RepeatingElement(
            add_text="Add keyword",
            remove_text="Remove last",
            widget_kwargs=widget_kwargs,
        )

        # Remove any default style from the italic label.
        self.keywords.ui.italic_label.setStyleSheet("")

        # Add the first keyword input line.
        self.keywords.add_another()

        # Insert the RepeatingElement into the keywords layout.
        self.ui.keywords_layout.insertWidget(0, self.keywords)

    def lock(self):
        """
        Description:
            Locks the widget fields, preventing editing of the thesaurus
            field and disabling the "Add keyword" button.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Sets the thesaurus field to read-only and disables the add
            button in the repeating element.

        Notes:
            None
        """

        # Set thesaurus field to read-only.
        self.ui.fgdc_themekt.setReadOnly(True)

        # Disable the "Add keyword" button.
        self.keywords.ui.addAnother.setEnabled(False)

    def get_keywords(self):
        """
        Description:
            Retrieves the text content of all individual keyword widgets.

        Passed arguments:
            None

        Returned objects:
            list: List of strings, where each string is a keyword.

        Workflow:
            Iterates through the list of keyword widgets and returns
            their text content.

        Notes:
            None
        """

        # List comprehension to extract text from each keyword widget.
        return [kw.text() for kw in self.keywords.get_widgets()]

    def add_another(self, locked=False):
        """
        Description:
            Adds another keyword input line to the list.

        Passed arguments:
            locked (bool): If True, the newly added input line will be
                set to read-only.

        Returned objects:
            QWidget: The newly created keyword input widget.

        Workflow:
            Calls the repeating element's add method, sets the object
            name, and optionally sets the input line to read-only.

        Notes:
            None
        """

        # Add a new keyword widget.
        widget = self.keywords.add_another()

        # Set object name for XML/utility purposes.
        widget.setObjectName(self.line_name)

        # Set read-only status based on "locked" parameter.
        widget.added_line.setReadOnly(locked)

        return widget

    def get_widgets(self):
        return self.keywords.get_widgets()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(KeywordsRepeater, " testing")
