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
    from pymdwizard.core import xml_utils
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.ui_files import UI_vertdef
except ImportError as err:
    raise ImportError(err, __file__)


class Vertdef(WizardWidget):  #

    drag_label = "Time Period information <vertdef>"
    acceptable_tags = ["vertdef", "altsys", "depthsys"]

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_vertdef.Ui_Form()
        self.ui.setupUi(self)
        self.setup_dragdrop(self)

        self.altres_list = RepeatingElement(
            widget_kwargs={
                "label": "Altitude Resolution",
                "line_name": "fgdc_altres",
                "required": True,
            },
            add_text="+",
            remove_text="-",
        )
        self.altres_list.add_another()
        self.ui.altsys_contents.layout().insertWidget(1, self.altres_list)

        self.depthres_list = RepeatingElement(
            widget_kwargs={
                "label": "Depth Resolution",
                "line_name": "fgdc_depthres",
                "required": True,
            },
            add_text="+",
            remove_text="-",
        )
        self.depthres_list.add_another()
        self.ui.depthsys_contents.layout().insertWidget(1, self.depthres_list)

    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions
        Returns
        -------
        None
        """
        # self.ui.radio_single.toggled.connect(self.switch_primary)
        self.ui.rbtn_yes.toggled.connect(self.include_vertdef_change)
        self.ui.rbtn_yes_alt.toggled.connect(self.include_alt_change)
        self.ui.rbtn_yes_depth.toggled.connect(self.include_depth_change)

    def has_content(self):
        """
        Returns if the widget contains legitimate content that should be
        written out to xml

        By default this is always true but should be implement in each
        subclass with logic to check based on contents

        Returns
        -------
        bool : True if there is content, False if no
        """
        return self.ui.rbtn_yes.isChecked()

    def include_vertdef_change(self, b):
        """
        Extended vertical definition section.

        Parameters
        ----------
        b: qt event

        Returns
        -------
        None
        """
        if b:
            self.ui.content_layout.show()
        else:
            self.ui.content_layout.hide()

        def include_vertdef_change(self, b):
            """
            Extended vertical definition section.

            Parameters
            ----------
            b: qt event

            Returns
            -------
            None
            """

        if b:
            self.ui.content_layout.show()
        else:
            self.ui.content_layout.hide()

    def include_alt_change(self, b):
        """
        Extended vertical definition section.

        Parameters
        ----------
        b: qt event

        Returns
        -------
        None
        """
        if b:
            self.ui.altsys_contents.show()
        else:
            self.ui.altsys_contents.hide()

    def include_depth_change(self, b):
        """
        Extended vertical definition section.

        Parameters
        ----------
        b: qt event

        Returns
        -------
        None
        """
        if b:
            self.ui.depthsys_contents.show()
        else:
            self.ui.depthsys_contents.hide()

    def clear_widget(self):
        WizardWidget.clear_widget(self)
        self.ui.rbtn_no.setChecked(True)
        self.ui.rbtn_no_alt.setChecked(True)
        self.ui.rbtn_no_depth.setChecked(True)

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeinfo element tag in xml tree
        """

        if self.ui.rbtn_yes.isChecked():
            vertdef = xml_utils.xml_node("vertdef")

            if self.ui.rbtn_yes_alt.isChecked():
                altsys = xml_utils.xml_node("altsys", parent_node=vertdef)
                altdatum = xml_utils.xml_node(
                    "altdatum",
                    text=self.ui.fgdc_altdatum.currentText(),
                    parent_node=altsys,
                )
                for widget in self.altres_list.get_widgets():
                    altres = xml_utils.xml_node(
                        "altres", widget.added_line.toPlainText(), parent_node=altsys
                    )
                altunits = xml_utils.xml_node(
                    "altunits",
                    text=self.ui.fgdc_altunits.currentText(),
                    parent_node=altsys,
                )
                altenc = xml_utils.xml_node(
                    "altenc", text=self.ui.fgdc_altenc.currentText(), parent_node=altsys
                )

            if self.ui.rbtn_yes_depth.isChecked():
                depth = xml_utils.xml_node("depthsys", parent_node=vertdef)
                depthdn = xml_utils.xml_node(
                    "depthdn",
                    text=self.ui.fgdc_depthdn.currentText(),
                    parent_node=depth,
                )
                for widget in self.depthres_list.get_widgets():
                    depthres = xml_utils.xml_node(
                        "depthres", widget.added_line.toPlainText(), parent_node=depth
                    )
                depthdu = xml_utils.xml_node(
                    "depthdu",
                    text=self.ui.fgdc_depthdu.currentText(),
                    parent_node=depth,
                )
                depthem = xml_utils.xml_node(
                    "depthem",
                    text=self.ui.fgdc_depthem.currentText(),
                    parent_node=depth,
                )

            return vertdef
        else:
            return None

    def from_xml(self, vertdef):
        """
        parses the xml code into the relevant timeinfo elements
        Parameters
        ----------
        metadata_date - the xml element timeinfo and its contents
        Returns
        -------
        None
        """
        self.clear_widget()
        try:
            if vertdef.tag == "vertdef":
                self.ui.rbtn_yes.setChecked(True)
                if vertdef.xpath("altsys"):
                    self.ui.rbtn_yes_alt.setChecked(True)
                    self.altres_list.clear_widgets(add_another=False)
                    for altres in vertdef.xpath("altsys/altres"):
                        altres_widget = self.altres_list.add_another()
                        altres_widget.added_line.setPlainText(altres.text)
                    if len(vertdef.xpath("altsys/altres")) == 0:
                        self.altres_list.add_another()
                else:
                    self.ui.rbtn_no_alt.setChecked(True)

                if vertdef.xpath("depthsys"):
                    self.ui.rbtn_yes_depth.setChecked(True)
                    self.depthres_list.clear_widgets(add_another=False)
                    for depthres in vertdef.xpath("depthsys/depthres"):
                        depthres_widget = self.depthres_list.add_another()
                        depthres_widget.added_line.setPlainText(depthres.text)
                    if len(vertdef.xpath("depthsys/depthres")) == 0:
                        self.depthres_list.add_another()

                else:
                    self.ui.rbtn_no_depth.setChecked(True)

                utils.populate_widget(self, vertdef)

            else:
                print("The tag is not a vertdef")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Vertdef, "Vertdef testing")
