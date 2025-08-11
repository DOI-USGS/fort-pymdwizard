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
    from PyQt5.QtWidgets import QWidget
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.ui_files import UI_edom
except ImportError as err:
    raise ImportError(err, __file__)


class Edom(QWidget):  #

    drag_label = "Enumerated Domain <edom>"
    acceptable_tags = ["edom"]

    def __init__(self, xml=None, parent=None, item=None):
        QWidget.__init__(self, parent=parent)
        self.item = item
        self.build_ui()

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_edom.Ui_fgdc_attrdomv()
        self.ui.setupUi(self)
        self.ui.fgdc_edomvd.item = self.item
        self.ui.fgdc_edomvd.heightMin = 25
        self.ui.fgdc_edomvd.heightMax = 150
        self.ui.fgdc_edomvd.sizeChange()

        defsource = utils.get_setting("defsource", "Producer defined")
        self.ui.fgdc_edomvds.setText(defsource)

    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'timeperd'
        Parameters
        ----------
        e : qt event
        Returns
        -------
        """
        e.ignore()

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        edom = xml_utils.xml_node("edom")
        edomv = xml_utils.xml_node(
            "edomv", text=self.ui.fgdc_edomv.text(), parent_node=edom
        )
        edomvd = xml_utils.xml_node(
            "edomvd", text=self.ui.fgdc_edomvd.toPlainText(), parent_node=edom
        )
        edomvds = xml_utils.xml_node(
            "edomvds", text=self.ui.fgdc_edomvds.text(), parent_node=edom
        )

        return edom

    def from_xml(self, edom):
        """
        parses the xml code into the relevant timeperd elements
        Parameters
        ----------
        metadata_date - the xml element timeperd and its contents
        Returns
        -------
        None
        """
        try:
            if edom.tag == "edom":
                self.ui.fgdc_edomvds.setText("")
                utils.populate_widget(self, edom)
            else:
                print("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Edom, "edom testing")
