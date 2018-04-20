#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

from pymdwizard.core import utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.repeating_element import RepeatingElement
from pymdwizard.gui.ui_files import UI_keywords_repeater


class KeywordsRepeater(WizardWidget):

    drag_label = "NA <NA>"

    def __init__(self, thesaurus_label='Thesaurus', keywords_label='Keywords:',
                 line_name='kw', spellings=True, parent=None):
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

        widget_kwargs = {'label': self.keywords_label,
                         'line_name': self.line_name,
                         'required': True,
                         'spellings': self.spellings}

        self.keywords = RepeatingElement(add_text='Add keyword',
                                         remove_text='Remove last',
                                         widget_kwargs=widget_kwargs)
        self.keywords.ui.italic_label.setStyleSheet('')

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
    utils.launch_widget(KeywordsRepeater,
                        " testing")
