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
    from PyQt5.QtWidgets import QPlainTextEdit
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_abstract
except ImportError as err:
    raise ImportError(err, __file__)


class Abstract(WizardWidget):
    drag_label = "Abstract <abstract>"
    acceptable_tags = ["abstract"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Args:
            None

        Returns:
            None
        """

        self.ui = UI_abstract.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)


    def get_children(self, widget):
        """
        Description:
            Return a list of widget's children.

        Args:
            widget (QWidget): The widget whose children are to be returned.

        Returns:
            widget (list): List of children widgets
        """

        children = []
        children.append(self.ui.fgdc_abstract)

        parent = self.parent()
        while not parent.objectName() == "fgdc_idinfo":
            parent = parent.parent()
        children.append(parent.supplinf.ui.fgdc_supplinf)
        children.append(parent.purpose.ui.fgdc_purpose)

        return children


    def to_xml(self):
        """
        Description:
            Encapsulate the QPlainTextEdit text in an element tag.

        Args:
            None

        Returns:
            abstract (xml.etree.ElementTree.Element): Abstract element tag in
                XML tree
        """

        abstract = xml_utils.xml_node(
            "abstract", text=self.ui.fgdc_abstract.toPlainText()
        )

        return abstract


    def from_xml(self, abstract):
        """
        Description:
            Parse the XML code into the relevant abstract elements.

        Args:
            abstract (xml.etree.ElementTree.Element): The XML element
                containing the abstract.

        Returns:
            None
        """

        try:
            if abstract.tag == "abstract":
                try:
                    abstract_text = abstract.text
                    abstract_box = self.findChild(QPlainTextEdit,
                                                  "fgdc_abstract")
                    abstract_box.setPlainText(abstract_text)
                except:
                    pass
            else:
                print("The tag is not abstract.")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    utils.launch_widget(Abstract, "Abstract testing")
