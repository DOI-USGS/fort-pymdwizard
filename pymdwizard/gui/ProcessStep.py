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
    from PyQt5.QtWidgets import (QLineEdit, QVBoxLayout, QPlainTextEdit)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_ProcessStep
    from pymdwizard.gui.fgdc_date import FGDCDate
    from pymdwizard.gui.repeating_element import RepeatingElement
    from pymdwizard.gui.proccont import ProcessContact
except ImportError as err:
    raise ImportError(err, __file__)


class ProcessStep(WizardWidget):  #
    """
    Description:
        A widget corresponding to the FGDC <procstep> tag, which
        describes a single operation or event in the lineage of the
        data set.

    Passed arguments:
        None (Inherited from WizardWidget)

    Returned objects:
        None

    Workflow:
        1. Embeds widgets for process date, process contact, and repeating
           lists for sources used and sources produced.
        2. Handles XML serialization/deserialization for the entire
           `<procstep>` structure.

    Notes:
        Inherits from "WizardWidget". The "proccont" widget is controlled
        by a radio button within the embedded "ProcessContact" widget.
    """

    # Class attributes.
    drag_label = "Process Step <procstep>"
    acceptable_tags = ["procstep"]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's graphical user interface,
            initializing child widgets and repeating elements.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes UI, sets up drag-and-drop, creates child widgets
            ("FGDCDate", "ProcessContact"), and initializes repeating lists
            ("srcused_list", "srcprod_list").

        Notes:
            None
        """

        self.ui = UI_ProcessStep.Ui_Form()
        self.ui.setupUi(self)

        # Ensure the description field has a minimum height.
        self.ui.fgdc_procdesc.heightMin = 150
        self.setup_dragdrop(self)

        # Initialize process date widget.
        self.single_date = FGDCDate(
            show_format=False,
            required=True,
            label="",
            fgdc_name="fgdc_procdate",
        )

        # Initialize process contact widget.
        self.proccont = ProcessContact()

        # Place child widgets into the UI layouts.
        self.ui.fgdc_procdate.setLayout(QVBoxLayout())
        self.ui.fgdc_procdate.layout().insertWidget(0, self.single_date)
        self.ui.widget_proccont.layout().insertWidget(0, self.proccont)

        # Initialize RepeatingElement for Source Used (srcused).
        self.srcused_list = RepeatingElement(
            add_text="Add another",
            remove_text="Remove last",
            widget_kwargs={"label": "Source used",
                           "line_name": "fgdc_srcused"},
        )
        self.srcused_list.add_another()
        self.ui.srcused_groupbox.layout().addWidget(self.srcused_list)

        # Initialize RepeatingElement for Source Produced (srcprod).
        self.srcprod_list = RepeatingElement(
            add_text="Add another",
            remove_text="Remove last",
            widget_kwargs={"label": "Source produced:",
                           "line_name": "fgdc_srcprod"},
        )
        self.srcprod_list.add_another()
        self.ui.srcprod_groupbox.layout().addWidget(self.srcprod_list)

        self.clear_widget()

    def clear_widget(self):
        """
        Description:
            Clears the widget's content and sets the process contact
            radio button to 'No'.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Calls the parent "clear_widget" and sets the "proccont"
            radio button.

        Notes:
            None
        """

        # Call the base class clear method.
        super(self.__class__, self).clear_widget()

        # Ensure the contact is disabled by default.
        self.proccont.ui.rbtn_no.setChecked(True)

    def to_xml(self):
        """
        Description:
            Converts the widget's content into an FGDC <procstep> XML
            element.

        Passed arguments:
            None

        Returned objects:
            procstep (lxml.etree._Element): The <procstep> element.

        Workflow:
            1. Creates <procstep>.
            2. Appends <procdesc> text.
            3. Appends <srcused> elements from the repeating list.
            4. Appends <procdate> from the date widget.
            5. Appends <srcprod> elements from the repeating list.
            6. Appends <proccont> if the contact is enabled.

        Notes:
            Uses "findChild" to retrieve text from internal widgets.
        """

        # Create the root <procstep> node.
        procstep = xml_utils.xml_node(tag="procstep")

        # Process Description (<procdesc>)
        procdesc = xml_utils.xml_node(tag="procdesc")
        procdesc_widget = self.findChild(QPlainTextEdit,
                                         "fgdc_procdesc")
        procdesc.text = procdesc_widget.toPlainText()
        procstep.append(procdesc)

        # Sources Used (<srcused>).
        for srcused in self.srcused_list.get_widgets():
            if srcused.text():
                xml_utils.xml_node("srcused", text=srcused.text(),
                                   parent_node=procstep)

        # Process Date (<procdate>).
        procdate = xml_utils.xml_node(tag="procdate")
        date_var = self.single_date.findChild(QLineEdit,
                                              "fgdc_procdate").text()
        procdate.text = date_var
        procstep.append(procdate)

        # Sources Produced (<srcprod>).
        for srcprod in self.srcprod_list.get_widgets():
            if srcprod.text():
                xml_utils.xml_node("srcprod", text=srcprod.text(),
                                   parent_node=procstep)

        # Process Contact (<proccont>).
        if self.proccont.ui.rbtn_yes.isChecked():
            proccont = self.proccont.to_xml()
            procstep.append(proccont)

        return procstep

    def from_xml(self, xml_processstep):
        """
        Description:
            Parses an FGDC <procstep> XML element and populates the
            widget fields and lists.

        Passed arguments:
            xml_processstep (lxml.etree._Element): The XML node to load.

        Returned objects:
            None

        Workflow:
            1. Checks the tag.
            2. Populates simple fields using a utility function.
            3. Loads process date and process contact (setting radio buttons).
            4. Loads repeating lists ("srcused" and "srcprod"), handling
               clearing/adding widgets as necessary.

        Notes:
            Fails silently on "KeyError".
        """

        try:
            if xml_processstep.tag == "procstep":
                # Populate simple text fields.
                utils.populate_widget(self, xml_processstep)

                # Load process date.
                if xml_processstep.xpath("procdate"):
                    date_text = xml_processstep.xpath("procdate")[0].text
                    self.single_date.set_date(date_text)

                # Load process contact.
                if xml_processstep.xpath("proccont"):
                    self.proccont.ui.rbtn_yes.setChecked(True)
                    cntinfo_node = xml_processstep.xpath("proccont/cntinfo")[0]
                    self.proccont.from_xml(cntinfo_node)
                else:
                    self.proccont.ui.rbtn_no.setChecked(True)
                    pass

                # Load Sources Used (srcused).
                srcuseds = xml_processstep.findall("srcused")
                if srcuseds:
                    self.srcused_list.clear_widgets(add_another=False)
                    for srcused in srcuseds:
                        srcused_widget = self.srcused_list.add_another()
                        srcused_widget.setText(srcused.text)
                else:
                    self.srcused_list.clear_widgets(add_another=True)

                # Load Sources Produced (srcprod).
                srcprods = xml_processstep.findall("srcprod")
                if srcprods:
                    self.srcprod_list.clear_widgets(add_another=False)
                    for srcprod in srcprods:
                        srcprod_widget = self.srcprod_list.add_another()
                        srcprod_widget.setText(srcprod.text)
                else:
                    self.srcprod_list.clear_widgets(add_another=True)
            else:
                print("The tag is not procstep")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(ProcessStep, "Process Step testing")
