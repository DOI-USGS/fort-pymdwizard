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
    from PyQt5.QtWidgets import QLineEdit
    from PyQt5.QtWidgets import QLabel
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.core import spatial_utils
    from pymdwizard.core import fgdc_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_mapproj
except ImportError as err:
    raise ImportError(err, __file__)


class MapProj(WizardWidget):

    drag_label = "Map Projection <mapproj>"
    acceptable_tags = ["mapproj"]

    ui_class = UI_mapproj.Ui_Form

    def build_ui(self):
        self.shortname = ""

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

        annotation_lookup["stdparll_2"] = {
            "long_name": "Standard Parallel",
            "annotation": annotation_lookup["stdparll"]["annotation"],
        }

        self.clear_widget()
        layout = self.ui.mapproj_contents.layout()

        for param in self.projection["elements"]:
            try:
                long_name = annotation_lookup[param]["long_name"]
                annotation = annotation_lookup[param]["annotation"]
            except:
                long_name = param
                annotation = "Unknown"

            label = QLabel(long_name)
            label.setToolTip(annotation)
            label.help_text = annotation
            lineedit = QLineEdit("...")
            lineedit.setObjectName("fgdc_" + param)
            lineedit.setToolTip(annotation)
            layout.addRow(label, lineedit)

    def to_xml(self):
        if self.shortname:
            proj_root = xml_utils.xml_node(self.shortname)

            for param in self.projection["elements"]:
                widget = self.findChild(QLineEdit, "fgdc_" + param)
                if param == "stdparll_2":
                    param = "stdparll"
                if widget is not None:
                    xml_utils.xml_node(param, text=widget.text(), parent_node=proj_root)
                else:
                    xml_utils.xml_node(param, text="", parent_node=proj_root)
            return proj_root
        else:
            return None

    def from_xml(self, mapproj_node):
        self.clear_widget()

        shortname = mapproj_node.tag
        self.load_projection(shortname)

        for item in mapproj_node.getchildren():
            tag = item.tag
            item_widget = self.findChild(QLineEdit, "fgdc_" + tag)
            utils.set_text(item_widget, item.text)

        stdparll = mapproj_node.xpath("stdparll")
        try:
            stdparll_widget = self.findChildren(QLineEdit, "fgdc_stdparll")[0]
            utils.set_text(stdparll_widget, stdparll[0].text)
            stdparl_2_widget = self.findChildren(QLineEdit, "fgdc_stdparll_2")[0]
            utils.set_text(stdparl_2_widget, stdparll[1].text)
        except:
            pass


if __name__ == "__main__":
    utils.launch_widget(MapProj, "spref testing")
