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

from pymdwizard.core import utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.ui_files import UI_keywords_repeater


class KeywordsRepeater(WizardWidget):

    drag_label = "NA <NA>"

    def __init__(
        self,
        thesaurus_label="Thesaurus",
        keywords_label="Keywords:",
        line_name="kw",
        spellings=True,
        parent=None,
    ):
        self.thesaurus_label = thesaurus_label
        self.keywords_label = keywords_label
        self.line_name = line_name
        self.keywords = None
        self.spellings = spellings

        WizardWidget.__init__(self, parent=parent)

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_keywords_repeater.Ui_Form()

        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.ui.thesaurus_label = self.thesaurus_label

        widget_kwargs = {
            "label": self.keywords_label,
            "line_name": self.line_name,
            "required": True,
            "spellings": self.spellings,
        }

        self.keywords = RepeatingElement(
            add_text="Add keyword",
            remove_text="Remove last",
            widget_kwargs=widget_kwargs,
        )
        self.keywords.ui.italic_label.setStyleSheet("")

        self.keywords.add_another()

        self.ui.keywords_layout.insertWidget(0, self.keywords)

    def lock(self):
        self.ui.fgdc_themekt.setReadOnly(True)
        self.keywords.ui.addAnother.setEnabled(False)

    def get_keywords(self):
        return [kw.text() for kw in self.keywords.get_widgets()]

    def add_another(self, locked=False):
        widget = self.keywords.add_another()
        widget.setObjectName(self.line_name)
        widget.added_line.setReadOnly(locked)
        return widget

    def get_widgets(self):
        return self.keywords.get_widgets()


if __name__ == "__main__":
    utils.launch_widget(KeywordsRepeater, " testing")
