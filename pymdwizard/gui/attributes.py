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
    import pandas as pd
    from PyQt5.QtWidgets import (QMessageBox, QMenu)
    from PyQt5.QtGui import QIcon
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_attributes
    from pymdwizard.gui import mdattr
except ImportError as err:
    raise ImportError(err, __file__)


class Attributes(WizardWidget):  #
    """
    Description:
        A widget for managing the FGDC "detailed" entity and attribute
        metadata section. Inherits from QgsWizardWidget.

    Passed arguments:
        None

    Returned objects:
        None

    Workflow:
        Manages the display, loading (from DataFrame or pickle), and
        manipulation of a list of attribute widgets. Handles XML
        conversion for the entire set.

    Notes:
        Relies on "mdattr.Attr" for individual attribute widgets.
    """

    # Class attributes.
    drag_label = "Attributes <attr>"
    acceptable_tags = ["attr"]

    def build_ui(self):
        """
        Description:
            Build and modify this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Initializes the UI, gets the layout for dynamically adding
            attribute widgets, and initializes display bounds.

        Notes:
            Assumes UI_attributes is available.
        """

        # Instantiate the UI elements from the designer file.
        self.ui = UI_attributes.Ui_Form()

        # Set up the instantiated UI
        self.ui.setupUi(self)

        # Get the layout of the scroll area content for dynamic widgets.
        self.main_layout = self.ui.scrollAreaWidgetContents.layout()

        # Initialize the list of attribute widgets.
        self.attrs = []

        # Initialize display boundaries (for pagination/expansion logic).
        self.displayed_min = 0
        self.displayed_max = 9

        # Minimize all children (if any were loaded).
        self.minimize_children()

    def load_df(self, df):
        """
        Description:
            Load attributes from a pandas DataFrame. Displays a warning
            for datasets with many columns.

        Passed arguments:
            df (pd.DataFrame): The DataFrame containing the data and
                column names.

        Returned objects:
            None

        Workflow:
            1. Check for excessive columns and warn the user.
            2. Clear existing attribute widgets.
            3. Iterate through columns, create an "mdattr.Attr" widget
               for each, set its label, sniff data, and guess the
               domain type.

        Notes:
            Relies on "mdattr.Attr", "QMessageBox", and "utils".
        """

        # Check if the number of columns exceeds a threshold.
        if len(df.columns) > 100:
            msgbox = QMessageBox(self)
            utils.set_window_icon(msgbox)
            msgbox.setIcon(QMessageBox.Question)

            # Construct the lengthy warning message (split for PEP 8)
            msg = "There are more than 100 columns in the dataset "
            msg += "you are trying to build an Entity and Attribute "
            msg += "section for!\n\n"
            msg += "The application can become sluggish or unresponsive "
            msg += "when loading and displaying that many columns.\n\n"
            msg += "Displaying more than 250 columns can cause the "
            msg += "application to crash.\n\n"
            msg += "Often datasets with that many columns are documented "
            msg += "with an overview instead of a detailed section, or "
            msg += "using an external data dictionary.\n\n"
            msg += "You have {} columns in this dataset.".format(
                len(df.columns)
            )
            msg += "\n\nAre you sure you want to continue?"

            msgbox.setText(msg)
            msgbox.setWindowTitle("Too Many Columns Warning")
            msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm = msgbox.exec_()

            if confirm == QMessageBox.No:
                return

        # Clear any existing attribute widgets.
        self.clear_children()

        # Iterate through column labels to create attribute widgets.
        for col_label in df.columns:
            col = df[col_label]

            # Create a new attribute widget.
            attr_i = mdattr.Attr(parent=self)

            # Set the attribute label (column name).
            attr_i.ui.fgdc_attrlabl.setText(str(col_label))

            # Set the data series, sniff for no-data values.
            attr_i.set_series(col)
            attr_i.sniff_nodata()

            # Guess the domain and set the combobox index.
            attr_i.ui.comboBox.setCurrentIndex(attr_i.guess_domain())

            # Add the new attribute widget to the list and layout.
            self.append_attr(attr_i)

        # Expand the first attribute widget for easy editing.
        self.attrs[0].supersize_me()

    def append_attr(self, attr):
        """
        Description:
            Append a new attribute widget to the internal list and the
            main layout.

        Passed arguments:
            attr (mdattr.Attr): The attribute widget to append.

        Returned objects:
            None

        Workflow:
            Adds the widget to the list and inserts it into the layout
            just before the final spacer/stretch item.

        Notes:
            None
        """

        # Add the widget to the internal list.
        self.attrs.append(attr)

        # Insert the widget into the layout before the final item (spacer).
        self.main_layout.insertWidget(len(self.main_layout) - 1, attr)

    def load_pickle(self, contents):
        """
        Description:
            Load attributes from a pickled dictionary containing column
            metadata and data samples.

        Passed arguments:
            contents (dict): The dictionary containing attribute data.

        Returned objects:
            None

        Workflow:
            1. Clear existing attributes.
            2. If original XML is present, parse from XML instead.
            3. Otherwise, iterate through pickle contents, create new
               widgets, populate based on data 'type' (String, Numeric,
               or Other), and append them.

        Notes:
            None
        """

        # Clear any existing attribute widgets.
        self.clear_children()

        # If original XML exists, load from that instead.
        if self.original_xml is not None:
            self.from_xml(self.original_xml)

        # Iterate through keys (column labels) in the pickle contents.
        for col_label in contents.keys():
            # Create a new attribute widget
            attr_i = mdattr.Attr(parent=self)
            attr_i.ui.fgdc_attrlabl.setText(col_label)

            col_data = contents[col_label]
            col_type = col_data[b"type"]

            # Handle String type attributes.
            if col_type == "String":
                s = pd.Series(col_data[b"contents"])
                attr_i.set_series(s)
                attr_i.guess_domain()

            # Handle Numeric/Date type attributes.
            elif col_type in [
                "Integer",
                "Single",
                "SmallInteger",
                "Double",
                "Date",
            ]:
                s = pd.Series(col_data[b"contents"])
                attr_i.set_series(s)
                # Set domain to Numeric/Time
                attr_i.ui.comboBox.setCurrentIndex(1)

            # Handle Unknown/Unrepresented type attributes.
            else:
                attr_i.populate_domain_content(3)
                unrep = col_data[b"contents"]

                # Populate definition, domain, and definition source.
                utils.set_text(
                    attr_i.ui.fgdc_attrdef, unrep[0].decode("utf-8")
                )
                utils.set_text(
                    attr_i.domain.ui.fgdc_udom, unrep[1].decode("utf-8")
                )
                utils.set_text(
                    attr_i.ui.fgdc_attrdefs, unrep[2].decode("utf-8")
                )

                # Ensure the new content is stored and the size is reset.
                attr_i.store_current_content()
                attr_i.supersize_me()
                attr_i.regularsize_me()

            # Add the new attribute widget.
            self.append_attr(attr_i)

            try:
                # Expand the first attribute widget if it exists.
                self.attrs[0].supersize_me()
            except IndexError:
                pass

    def clear_children(self):
        """
        Description:
            Delete all attribute widgets and clear the internal list.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Iterates through the list of widgets, calls "deleteLater()",
            and resets the list.

        Notes:
            None
        """

        # Iterate and schedule widgets for deletion.
        for attribute in self.attrs:
            attribute.deleteLater()

        # Reset the internal list.
        self.attrs = []

    def get_attr(self, which):
        """
        Description:
            Retrieve an attribute widget by its label (column name).

        Passed arguments:
            which (str): The label of the attribute to find.

        Returned objects:
            attr (mdattr.Attr | None): The matching attribute widget, or
                None if not found.

        Workflow:
            Iterates through the list and compares attribute labels.

        Notes:
            None
        """

        # Iterate through attributes to find a label match.
        for attr in self.attrs:
            if attr.ui.fgdc_attrlabl.text() == which:
                return attr

        return None

    def insert_before(self, this_attr):
        """
        Description:
            Insert a new, empty attribute widget immediately before the
            specified attribute.

        Passed arguments:
            this_attr (mdattr.Attr): The attribute widget to insert
                before.

        Returned objects:
            None

        Workflow:
            Creates a new list, inserts the new widget at the correct
            index in the layout and new list, and replaces the old list.

        Notes:
            None
        """

        # Initialize list.
        new_attrs = []

        # Find the index of the reference attribute.
        for i, attribute in enumerate(self.attrs):
            if attribute == this_attr:

                # Create and insert the new attribute widget.
                new_attr = mdattr.Attr(parent=self)
                self.main_layout.insertWidget(i, new_attr)
                new_attrs.append(new_attr)
            new_attrs.append(attribute)

        # Replace the list with the updated list.
        self.attrs = new_attrs

    def insert_after(self, this_attr):
        """
        Description:
            Insert a new, empty attribute widget immediately after the
            specified attribute.

        Passed arguments:
            this_attr (mdattr.Attr): The attribute widget to insert
                after.

        Returned objects:
            None

        Workflow:
            Creates a new list, inserts the new widget at the correct
            index in the layout and new list, and replaces the old list.

        Notes:
            None
        """

        # Initialize list.
        new_attrs = []

        # Find the index of the reference attribute.
        for i, attribute in enumerate(self.attrs):
            new_attrs.append(attribute)
            if attribute == this_attr:

                # Create and insert the new attribute widget.
                new_attr = mdattr.Attr(parent=self)
                self.main_layout.insertWidget(i + 1, new_attr)
                new_attrs.append(new_attr)

        # Replace the list with the updated list.
        self.attrs = new_attrs

    def delete_attr(self, this_attr):
        """
        Description:
            Delete the specified attribute widget from the UI and the
            internal list.

        Passed arguments:
            this_attr (mdattr.Attr): The attribute widget to delete.

        Returned objects:
            None

        Workflow:
            Iterates, schedules the matching widget for deletion, and
            builds a new list of attributes to keep.

        Notes:
            None
        """

        # Initialize list.
        keep_attrs = []

        for attribute in self.attrs:
            if attribute == this_attr:
                # Schedule the widget for deletion.
                attribute.deleteLater()
            else:
                # Keep the other widgets.
                keep_attrs.append(attribute)

        # Update the internal list.
        self.attrs = keep_attrs

    def minimize_children(self):
        """
        Description:
            Minimize (regular-size) all currently active attribute
            widgets and reset their cursor position.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Iterates through all attributes and calls "regularsize_me()"
            if they are active.

        Notes:
            Assumes "attr_widget.active" and "regularsize_me()" exist.
        """

        for attr_widget in self.attrs:
            if attr_widget.active:
                attr_widget.regularsize_me()
                attr_widget.ui.fgdc_attrlabl.setCursorPosition(0)

    def contextMenuEvent(self, event):
        """
        Description:
            Handles the right-click context menu for the widget.

        Passed arguments:
            event (QEvent): The mouse event object.

        Returned objects:
            None

        Workflow:
            1. Creates a context menu and defines copy, paste, add,
               help, and clear actions.
            2. Determines the clicked widget/button.
            3. Executes the selected action (copy/paste data, clear,
               add new attribute, or display help).

        Notes:
            This method is lengthy due to handling many different
            contextual actions for various parent/child widgets.
        """

        self.in_context = True

        # Find the widget clicked at the event position.
        clicked_widget = self.childAt(event.pos())

        # Create the context menu.
        menu = QMenu(self)

        # Define standard actions.
        copy_action = menu.addAction(QIcon("copy.png"), "&Copy")
        copy_action.setStatusTip("Copy to the Clipboard")

        paste_action = menu.addAction(QIcon("paste.png"), "&Paste")
        paste_action.setStatusTip("Paste from the Clipboard")

        menu.addSeparator()
        add_attr = menu.addAction(QIcon("paste.png"),
                                  "Add attribute (column)")
        add_attr.setStatusTip("Add attribute")

        # Add help action if the clicked widget has help text.
        if hasattr(clicked_widget, "help_text") and clicked_widget.help_text:
            menu.addSeparator()
            help_action = menu.addAction("Help")
        else:
            help_action = None

        menu.addSeparator()
        clear_action = menu.addAction("Clear content")

        # Execute the menu at the cursor position.
        action = menu.exec_(self.mapToGlobal(event.pos()))

        # Handle actions.
        if action == copy_action:
            # Copy content based on the clicked widget.
            if clicked_widget is None:
                pass
            elif clicked_widget.objectName() == "idinfo_button":
                self.idinfo.copy_mime()
            elif clicked_widget.objectName() == "dataquality_button":
                self.dataqual.copy_mime()
            elif clicked_widget.objectName() == "eainfo_button":
                self.eainfo.copy_mime()
            elif clicked_widget.objectName() == "distinfo_button":
                self.distinfo.copy_mime()
            elif clicked_widget.objectName() == "metainfo_button":
                self.metainfo.copy_mime()
            else:
                self.copy_mime()
        elif action == paste_action:
            self.paste_mime()
        elif action == clear_action:
            if clicked_widget is None:
                self.clear_widget()
            elif clicked_widget.objectName() == "idinfo_button":
                self.idinfo.clear_widget()
            elif clicked_widget.objectName() == "dataquality_button":
                self.dataqual.clear_widget()
            elif clicked_widget.objectName() == "eainfo_button":
                self.eainfo.clear_widget()
            elif clicked_widget.objectName() == "distinfo_button":
                self.distinfo.clear_widget()
            elif clicked_widget.objectName() == "metainfo_button":
                self.metainfo.clear_widget()
            else:
                self.clear_widget()
        elif action == add_attr:
            # Add a new attribute widget.
            new_attr = mdattr.Attr(parent=self)
            self.append_attr(new_attr)
            self.minimize_children()
            new_attr.supersize_me()
        elif help_action is not None and action == help_action:
            # Show help text for the clicked widget.
            msg = QMessageBox(self)
            # msg.setTextFormat(Qt.RichText)
            msg.setText(clicked_widget.help_text)
            msg.setWindowTitle("Help")
            msg.show()
        self.in_context = False

    def dragEnterEvent(self, e):
        """
        Description:
            Attributes never accept drops.

        Passed arguments:
            e (QEvent): The drag event object.

        Returned objects:
            None

        Workflow:
            Ignores the drag event, preventing a drop.

        Notes:
            None
        """

        # Attributes never accept drops.
        e.ignore()

    def to_xml(self):
        """
        Description:
            Encapsulate all attribute widgets' content into the parent
            "detailed" element tag.

        Passed arguments:
            None

        Returned objects:
            detailed (xml.etree.ElementTree.Element): The 'detailed'
                element tag in the XML tree, containing all 'attr'
                children.

        Workflow:
            Creates the "detailed" parent node and appends the XML
            representation of each attribute widget as a child.

        Notes:
            Assumes "xml_utils.xml_node" and "a.to_xml()" exist.
        """

        # Create the parent "detailed" XML node.
        detailed = xml_utils.xml_node("detailed")

        # Get XML for each attribute and append it to "detailed".
        for a in self.attrs:
            detailed.append(a.to_xml())

        return detailed

    def from_xml(self, detailed):
        """
        Description:
            Parse the XML code into the relevant attribute widgets.

        Passed arguments:
            detailed (xml.etree.ElementTree.Element): The XML element
                containing the 'detailed' entity and attribute section.

        Returned objects:
            None

        Workflow:
            1. Check tag is "detailed".
            2. Store the original XML.
            3. Clear existing widgets.
            4. Iterate through "attr" children, create an attribute
               widget for each, parse its XML, and add it to the UI.
            5. Minimize all widgets and expand the first one.

        Notes:
            Relies on "detailed.xpath()" and "mdattr.Attr.from_xml()".
        """

        try:
            # Check if the element tag matches the expected "detailed".
            if detailed.tag == "detailed":
                # Store the original element for later use.
                self.original_xml = detailed

                # Clear any existing widgets.
                self.clear_children()

                # Iterate through all "attr" nodes in the XML.
                for attr_node in detailed.xpath("attr"):
                    # Create a new attribute widget.
                    attr_widget = mdattr.Attr(parent=self)

                    # Load content from the XML node into the widget.
                    attr_widget.from_xml(attr_node)

                    # Add the widget to the list and layout.
                    self.attrs.append(attr_widget)
                    self.main_layout.insertWidget(
                        len(self.main_layout) - 1, attr_widget
                    )

                # Reset all widgets to regular size.
                self.minimize_children()
                try:
                    # Expand the first attribute widget if it exists.
                    self.attrs[0].supersize_me()
                except IndexError:
                    pass

            else:
                print("The tag is not udom")
        except KeyError:
            # Handle if the element is not found/accessible.
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Attributes, "attr_list testing")
