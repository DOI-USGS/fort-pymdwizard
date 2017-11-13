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

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import spatial_utils
from pymdwizard.core import fgdc_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_mapproj


class MapProj(WizardWidget):

    drag_label = "Map Projection <mapproj>"
    acceptable_tags = ['mapproj']

    ui_class = UI_mapproj.Ui_Form

    def build_ui(self):
        self.shortname = ''

        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = self.ui_class()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

    def clear_widget(self):
        layout = self.ui.mapproj_contents.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def load_projection(self, shortname):

        self.clear_widget()
        self.shortname = shortname
        self.projection = spatial_utils.lookup_shortname(shortname)

        annotation_lookup = fgdc_utils.get_fgdc_lookup()

        annotation_lookup['stdparll_2'] = {'long_name':'Standard Parallel',
                                      'annotation':annotation_lookup['stdparll']['annotation']}

        self.clear_widget()
        layout = self.ui.mapproj_contents.layout()

        for param in self.projection['elements']:
            try:
                long_name = annotation_lookup[param]['long_name']
                annotation = annotation_lookup[param]['annotation']
            except:
                long_name = param
                annotation = 'Unknown'

            label = QLabel(long_name)
            label.setToolTip(annotation)
            label.help_text = annotation
            lineedit = QLineEdit('...')
            lineedit.setObjectName('fgdc_' + param)
            lineedit.setToolTip(annotation)
            layout.addRow(label, lineedit)

    def to_xml(self):
        if self.shortname:
            proj_root = xml_utils.xml_node(self.shortname)

            for param in self.projection['elements']:
                widget = self.findChild(QLineEdit, "fgdc_"+param)
                if param == 'stdparll_2':
                    param = 'stdparll'
                if widget is not None:
                    xml_utils.xml_node(param, text=widget.text(), parent_node=proj_root)
                else:
                    xml_utils.xml_node(param, text='', parent_node=proj_root)
            return proj_root
        else:
            return None

    def from_xml(self, mapproj_node):
        self.clear_widget()

        shortname = mapproj_node.tag
        self.load_projection(shortname)

        for item in mapproj_node.getchildren():
            tag = item.tag
            item_widget = self.findChild(QLineEdit, "fgdc_"+tag)
            utils.set_text(item_widget, item.text)


        stdparll = mapproj_node.xpath('stdparll')
        try:
            stdparll_widget = self.findChildren(QLineEdit, "fgdc_stdparll")[0]
            utils.set_text(stdparll_widget, stdparll[0].text)
            stdparl_2_widget = self.findChildren(QLineEdit, "fgdc_stdparll_2")[0]
            utils.set_text(stdparl_2_widget, stdparll[1].text)
        except:
            pass


if __name__ == "__main__":
    utils.launch_widget(MapProj, "spref testing")
