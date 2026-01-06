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
files name.


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import sip

# Non-standard python libraries.
try:
    import numpy as np
    from PyQt5.QtWidgets import (QMessageBox, QWidget, QMenu, QComboBox,
                                 QLineEdit, QPlainTextEdit)
    from PyQt5.QtCore import (QPropertyAnimation, QSize)
    from PyQt5.QtGui import QIcon
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils, data_io)
    from pymdwizard.gui.wiz_widget import WizardWidget
    from pymdwizard.gui.ui_files import UI_attr
    from pymdwizard.gui import (udom, rdom, codesetd, edom_list, edom)
    from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
except ImportError as err:
    raise ImportError(err, __file__)

default_def_source = utils.get_setting("defsource", "Producer Defined")


class Attr(WizardWidget):
    """
    Description:
        A widget to handle the contents of the FGDC "attr" (Attribute)
        tag, allowing the user to select and configure different
        attribute domains (Enumerated, Range, Codeset, Unrepresentable).

    Passed arguments:
        parent (QWidget, optional): The parent widget.

    Returned objects:
        None

    Workflow:
        1. Initializes domain content and No Data tracking.
        2. Builds a dynamic UI that can switch between domain types.
        3. Supports context-menu actions (Copy, Paste, Insert, Delete).
        4. Provides introspection logic to guess the best domain type.

    Notes:
        Inherits from `WizardWidget`. Uses `QPropertyAnimation` for
        expanding/collapsing the attribute detail view.
    """

    # Class attributes.
    drag_label = "Attribute <attr>"
    acceptable_tags = ["attr"]

    def __init__(self, parent=None):
        # This changes to true when this attribute is being viewed/edited.
        self.active = False
        self.ef = 0

        self.nodata = None
        # (nodata checked, last nodata node)
        self.nodata_content = (False, None)

        WizardWidget.__init__(self, parent=parent)

        # In-memory record of contents selected for each domain type.
        self._previous_index = -1
        cbo = self.ui.comboBox
        self._domain_content = dict.fromkeys(range(cbo.count()), None)

        self.parent_ui = parent
        self.series = None

        # Hide No Data section initially.
        self.ui.nodata_section.hide()

        # Setup highlighter for the definition text area.
        self.highlighter = Highlighter(self.ui.fgdc_attrdef.document())

        # List of common No Data strings for sniffing
        self.nodata_matches = [
            "#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN",
            "-nan", "1.#IND", "1.#QNAN", "N/A", "NA", "NULL", "NaN",
            "n/a", "nan", "null", -9999, "-9999", "", "Nan",
            "<< empty cell >>",
        ]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's GUI.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Initializes the UI class and sets up the layout.
            2. Installs event filters for certain widgets.
            3. Connects signals (combobox change, radio button toggle).
            4. Overrides mouse press events for activation.

        Notes:
            Sets the default definition source text.
        """

        self.ui = UI_attr.Ui_attribute_widget()
        self.ui.setupUi(self)

        # Install event filters.
        self.ui.fgdc_attrdef.setMouseTracking(True)
        self.ui.fgdc_attrdefs.installEventFilter(self)
        self.ui.attrdomv_contents.installEventFilter(self)
        self.ui.place_holder.installEventFilter(self)

        # Setup drag and drop.
        self.setup_dragdrop(self)

        # Connect combobox change signal.
        self.ui.comboBox.currentIndexChanged.connect(self.change_domain)

        # Override mouse press events for activation.
        self.ui.fgdc_attr.mousePressEvent = self.mousePressEvent
        self.ui.fgdc_attrlabl.mousePressEvent = self.attrlabl_press
        self.ui.fgdc_attrdef.mousePressEvent = self.attrdef_press
        self.ui.fgdc_attrdefs.mousePressEvent = self.attrdefs_press
        self.ui.comboBox.mousePressEvent = self.combo_press

        # Connect No Data radio button toggle.
        self.ui.rbtn_nodata_yes.toggled.connect(self.include_nodata_change)

        # Hide the detailed No Data content section.
        self.ui.nodata_content.hide()

        # Set default radio button state.
        self.ui.rbtn_nodata_no.setChecked(True)

        # Set initial domain to Unrepresentable (index 3).
        self.ui.comboBox.setCurrentIndex(3)

        # Set the default definition source.
        self.ui.fgdc_attrdefs.setText(default_def_source)

    def include_nodata_change(self, b):
        """
        Description:
            Handles the event when the user toggles the No Data presence
            selection, showing or hiding the configuration section.

        Passed arguments:
            b (bool): True if the "Yes" radio button is checked.

        Returned objects:
            None

        Workflow:
            Shows the "nodata_section" if "b" is True, otherwise hides it.

        Notes:
            None
        """

        if b:
            self.ui.nodata_section.show()
        else:
            self.ui.nodata_section.hide()

    def mousePressEvent(self, event):
        """
        Description:
            Overrides the base mouse press event to activate the widget.

        Passed arguments:
            event (QMouseEvent): The mouse event object.

        Returned objects:
            None

        Workflow:
            Calls `self.activate()`.

        Notes:
            None
        """

        self.activate()

    def attrlabl_press(self, event):
        """
        Description:
            Overrides mouse press for "fgdc_attrlabl" to activate
            and pass the event to the QLineEdit.

        Passed arguments:
            event (QMouseEvent): The mouse event object.

        Returned objects:
            bool: Result of the QLineEdit's mousePressEvent.

        Workflow:
            Calls "self.activate()" then the base "QLineEdit" handler.

        Notes:
            None
        """

        self.activate()
        return QLineEdit.mousePressEvent(self.ui.fgdc_attrlabl, event)

    def attrdef_press(self, event):
        """
        Description:
            Overrides mouse press for "fgdc_attrdef" to activate
            and pass the event to the QPlainTextEdit.

        Passed arguments:
            event (QMouseEvent): The mouse event object.

        Returned objects:
            bool: Result of the QPlainTextEdit's mousePressEvent.

        Workflow:
            Calls "self.activate()" then the base `QPlainTextEdit` handler.

        Notes:
            None
        """

        self.activate()
        return QPlainTextEdit.mousePressEvent(self.ui.fgdc_attrdef, event)

    def attrdefs_press(self, event):
        """
        Description:
            Overrides mouse press for "fgdc_attrdefs" to activate
            and pass the event to the QLineEdit.

        Passed arguments:
            event (QMouseEvent): The mouse event object.

        Returned objects:
            bool: Result of the QLineEdit's mousePressEvent.

        Workflow:
            Calls "self.activate()" then the base "LineEdit" handler.

        Notes:
            None
        """

        self.activate()
        return QLineEdit.mousePressEvent(self.ui.fgdc_attrdefs, event)

    def combo_press(self, event):
        """
        Description:
            Overrides mouse press for the domain "comboBox" to activate
            and pass the event to the QComboBox.

        Passed arguments:
            event (QMouseEvent): The mouse event object.

        Returned objects:
            bool: Result of the QComboBox's mousePressEvent.

        Workflow:
            Calls "self.activate()" then the base "QComboBox" handler.

        Notes:
            None
        """

        self.activate()
        return QComboBox.mousePressEvent(self.ui.comboBox, event)

    def clear_domain(self):
        """
        Description:
            Removes the current domain widget from the layout.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Iterates through the children of "attrdomv_contents" and
            calls deleteLater() on any "QWidget" child.

        Notes:
            Used when switching domain types.
        """

        # Delete any existing domain widget in the container.
        for child in self.ui.attrdomv_contents.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def clear_nodata(self):
        """
        Description:
            Removes the No Data enumerated domain widget if it exists.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Attempts to call deleteLater() on "self.nodata_edom".

        Notes:
            Fails silently if the widget is not present.
        """

        try:
            # Delete the No Data enumeration widget.
            self.nodata_edom.deleteLater()
        except AttributeError:
            # Widget may not have been created yet.
            pass

    def set_series(self, series):
        """
        Description:
            Stores the associated pandas Series object with this attribute.

        Passed arguments:
            series (pandas.Series): The data column corresponding to
                this attribute.

        Returned objects:
            None

        Workflow:
            Assigns the passed series to "self.series".

        Notes:
            None
        """

        self.series = series

    def guess_domain(self):
        """
        Description:
            Guesses the appropriate FGDC domain type index based on the
            associated data series content.

        Passed arguments:
            None

        Returned objects:
            int: The index of the best matching domain:
                0: Enumerated
                1: Range
                3: Unrepresentable

        Workflow:
            1. Cleans the series of any detected No Data values.
            2. If numeric, guesses Range (1).
            3. If unique count < 20, guesses Enumerated (0).
            4. Otherwise, defaults to Unrepresentable (3).

        Notes:
            Defaults to Unrepresentable if no series is present.
        """

        # Given a series of data take a guess as to which
        # domain type is appropriate

        # If no series is present, default to Unrepresentable.
        if self.series is None:
            return 3

        # Clean series of No Data values before introspection.
        if self.series is not None:
            if self.nodata is not None:
                clean_series = data_io.clean_nodata(self.series, self.nodata)
            else:
                clean_series = self.series

            # Guess Range if the data type is numeric.
            uniques = clean_series.unique()
            if np.issubdtype(clean_series.dtype, np.number):
                return 1  # range

            # Guess Enumerated if there are few unique values.
            elif len(uniques) < 20:
                return 0  # enumerated

            # Otherwise, default to Unrepresentable.
            else:
                return 3  # unrepresentable

    def store_current_content(self):
        """
        Description:
            Saves the current domain and No Data content into internal
            memory dictionaries ("_domain_content" and "nodata_content").

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Converts the currently active domain widget (self.domain)
               to XML and stores it under its corresponding combobox index.
            2. Converts the No Data domain widget (self.nodata_edom) to
               XML and stores it in self.nodata_content.

        Notes:
            Uses sip.isdeleted to check for invalid Qt objects.
        """

        # Save the current primary domain content.
        if self.domain is not None and not sip.isdeleted(self.domain):
            cur_xml = self.domain.to_xml()
            if cur_xml.tag == "udom":
                self._domain_content[3] = cur_xml
            elif cur_xml.tag == "codesetd":
                self._domain_content[2] = cur_xml
            elif cur_xml.tag == "rdom":
                self._domain_content[1] = cur_xml
            elif cur_xml.tag == "attr":
                self._domain_content[0] = cur_xml

        # Save the current No Data domain content.
        if (self.ui.rbtn_nodata_yes.isChecked()
                and not sip.isdeleted(self.nodata_edom)
        ):
            self.nodata_content = (True, self.nodata_edom.to_xml())
        else:
            self.nodata_content = (False, None)

    def populate_domain_content(self, which="guess"):
        """
        Description:
            Fills the attribute domain section with a new domain widget,
            either by guessing the type or forcing a specific type.

        Passed arguments:
            which (str or int): "guess" to introspect the series, or an
                integer index to force a domain type (0-3).

        Returned objects:
            None

        Workflow:
            1. Clears existing domain widget.
            2. Determines the domain index (0-3).
            3. Creates the appropriate domain widget (self.domain).
            4. Populates the new widget either from stored content or by
               introspecting the data series.
            5. Displays warnings for excessive unique values or range domain
               use on text fields.

        Notes:
            None
        """

        self.clear_domain()

        if which == "guess":
            self.sniff_nodata()
            index = self.guess_domain()
        else:
            index = which

        # Set the combobox to the new index.
        self.ui.comboBox.setCurrentIndex(index)

        # Instantiate the correct domain widget.
        if index == 0:  # Enumerated
            self.domain = edom_list.EdomList(parent=self)
        elif index == 1:  # Range
            self.domain = rdom.Rdom(parent=self)
        elif index == 2:  # Codeset
            self.domain = codesetd.Codesetd(parent=self)
        else:  # Unrepresentable
            self.domain = udom.Udom(parent=self)

        # Populate the domain widget.
        if self._domain_content[index] is not None:
            # Use previously stored content if available.
            self.domain.from_xml(self._domain_content[index])
        elif self.series is not None and index == 0:
            # Introspect data series if no content is stored.
            clean_series = data_io.clean_nodata(self.series, self.nodata)
            uniques = clean_series.unique()

            if len(uniques) > 100:
                # Warning for too many unique values.
                msg = (
                    "There are more than 100 unique values in this "
                    "field. This tool cannot smoothly display that "
                    "many entries. Typically an enumerated domain is "
                    "not used with that many unique entries."
                    "\n\nOnly the first one hundred are displayed "
                    "below! You will likely want to change the "
                    "domain to one of the other options."
                )
                QMessageBox.warning(
                    self, "Too many unique entries", msg
                )
                self.domain.populate_from_list(uniques[:101])
            else:
                self.domain.populate_from_list(uniques)
        elif self.series is not None and index == 1:
            clean_series = data_io.clean_nodata(self.series, self.nodata)
            try:
                # Set min/max from series.
                self.domain.ui.fgdc_rdommin.setText(str(clean_series.min()))
            except:
                self.domain.ui.fgdc_rdommin.setText("")
            try:
                self.domain.ui.fgdc_rdommax.setText(str(clean_series.max()))
            except:
                self.domain.ui.fgdc_rdommax.setText("")

            if not np.issubdtype(clean_series.dtype, np.number):
                # Warning for range domain on text fields.
                msg = (
                    "Caution! The contents of this column are stored in the"
                    ' data source as "text".  The use of a range domain '
                    "type on text columns might give unexpected results, "
                    "especially for columns that contain date information."
                )
                msgbox = QMessageBox(
                    QMessageBox.Warning, "Range domain on text field",
                    msg
                )
                utils.set_window_icon(msgbox)
                msgbox.exec_()

        # Add the new domain widget to the layout.
        self.ui.attrdomv_contents.layout().addWidget(self.domain)

    def change_domain(self):
        """
        Description:
            Handles the combobox change event by storing the current
            domain content and loading the new domain content.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Checks if the widget is currently active (expanded).
            2. Stores the existing domain content.
            3. Clears the domain layout.
            4. Populates the new domain content.

        Notes:
            None
        """

        if self.active:
            # Save the content of the domain currently being viewed.
            self.store_current_content()

            # Remove the old domain widget.
            self.clear_domain()

            # Load the new domain content.
            self.populate_domain_content(
                self.ui.comboBox.currentIndex()
            )

    def supersize_me(self):
        """
        Description:
            Expands this attribute widget to show its detailed domain
            and No Data content.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Sets self.active = True.
            2. Starts a "QPropertyAnimation" to increase the minimum size.
            3. Shows the content sections and hides the placeholder.
            4. Populates the domain content and initializes the No Data
               domain section.

        Notes:
            Initializes the "nodata_edom" widget.
        """

        if not self.active:
            self.active = True

            # Animation to expand the widget horizontally.
            self.animation = QPropertyAnimation(self, b"minimumSize")
            self.animation.setDuration(200)
            self.animation.setEndValue(QSize(345, self.height()))
            self.animation.start()

            # Show the domain content and hide the placeholder.
            self.ui.attrdomv_contents.show()
            self.ui.place_holder.hide()
            cbo = self.ui.comboBox

            # Populate the domain content for the current index.
            self.populate_domain_content(cbo.currentIndex())

            # Handle No Data content section.
            self.ui.nodata_content.show()
            self.nodata_edom = edom.Edom()

            # Set radio button based on stored state.
            self.ui.rbtn_nodata_yes.setChecked(self.nodata_content[0])

            # Load stored No Data XML if available.
            if self.nodata_content[1] is not None:
                self.nodata_edom.from_xml(self.nodata_content[1])

            # Connect signal to update self.nodata on text change.
            self.nodata_edom.ui.fgdc_edomv.textChanged.connect(
                self.nodata_changed)

            # Add No Data widget to its section.
            self.ui.nodata_section.layout().addWidget(self.nodata_edom)

    def regularsize_me(self):
        """
        Description:
            Collapses this attribute widget to hide its detailed domain
            and No Data content.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Sets self.active = False.
            2. Stores the current domain content.
            3. Starts a "QPropertyAnimation" to shrink the minimum size.
            4. Hides the content sections and clears domain/nodata widgets.

        Notes:
            None
        """

        if self.active:
            # Save current content before collapsing.
            self.store_current_content()

            # Animation to collapse the widget horizontally.
            self.animation = QPropertyAnimation(self, b"minimumSize")
            self.animation.setDuration(200)
            self.animation.setEndValue(QSize(100, self.height()))
            self.animation.start()

            # Hide and clear dynamic widgets.
            self.ui.nodata_content.hide()
            self.clear_domain()
            self.clear_nodata()
            self.ui.place_holder.show()

        self.active = False

    def activate(self):
        """
        Description:
            Minimizes all sibling attributes in the parent list and
            expands this attribute.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            If inactive, tells the parent UI to minimize all other
            children, then calls supersize_me().

        Notes:
            None
        """

        if self.active:
            # Already expanded, do nothing.
            pass
        else:
            if self.parent_ui is not None:
                # Minimize all sibling attributes.
                self.parent_ui.minimize_children()

            # Expand this attribute.
            self.supersize_me()

    def nodata_changed(self):
        """
        Description:
            Updates the internal self.nodata value when the No Data
            text field changes, and cleans the primary domain.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Sets self.nodata from the "nodata_edom" text.
            2. Handles the special case of "<< empty cell >>".
            3. Calls "clean_domain_nodata" to update the primary domain
               content.

        Notes:
            None
        """

        # Update the No Data value from the widget.
        self.nodata = self.nodata_edom.ui.fgdc_edomv.text()
        if self.nodata == "<< empty cell >>":
            self.nodata = ""

        # Update the primary domain's stored content.
        self.clean_domain_nodata()

    def clean_domain_nodata(self):
        """
        Description:
            Forces an update of the primary domain's stored content
            (XML format) in "_domain_content".

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Saves the current domain's XML back into the memory cache.

        Notes:
            Only performs the save if the domain widget exists and is
            not deleted.
        """

        if self.domain is not None and not sip.isdeleted(self.domain):
            cur_xml = self.domain.to_xml()
            if cur_xml.tag == "rdom":
                self._domain_content[1] = cur_xml
            elif cur_xml.tag == "attr":
                # For enumerated domains which use the <attr> tag.
                edoms = self.domain.edoms
                self._domain_content[0] = cur_xml

    def sniff_nodata(self):
        """
        Description:
            Introspects the associated data series to automatically detect
            if a common "No Data" value is present.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            1. Iterates through a list of common No Data strings.
            2. If a match is found in the series, sets self.nodata.
            3. Updates self.nodata_content tuple (checked state and XML)
               to reflect the sniffed value.

        Notes:
            None
        """

        uniques = self.series.unique()

        self.nodata = None

        # Check if any common No Data string is in the unique values.
        for nd in self.nodata_matches:
            if nd in list(uniques):
                self.nodata = nd

        if self.nodata is None:
            # No No Data value found.
            self.nodata_content = (False, self.nodata_content[1])
        else:
            # No Data value found, create the XML representation.
            temp_edom = edom.Edom()
            if self.nodata == "":
                temp_edom.ui.fgdc_edomv.setText("<< empty cell >>")
            else:
                temp_edom.ui.fgdc_edomv.setText(str(self.nodata))

            temp_edom.ui.fgdc_edomvd.setPlainText("No Data")
            self.nodata_content = (True, temp_edom.to_xml())
            temp_edom.deleteLater()

    def contextMenuEvent(self, event):
        """
        Description:
            Handles the right-click event by displaying a context menu
            with actions like Copy, Paste, Insert, Delete, and Help.

        Passed arguments:
            event (QContextMenuEvent): The context menu event object.

        Returned objects:
            None

        Workflow:
            1. Determines the widget clicked.
            2. Creates and populates the menu.
            3. Executes the menu and handles the selected action.

        Notes:
            Relies on the parent UI for Insert/Delete actions.
        """

        self.in_context = True

        # Determine which child widget was clicked.
        clicked_widget = self.childAt(event.pos())

        # Add actions to context menu.
        menu = QMenu(self)
        copy_action = menu.addAction(QIcon("copy.png"), "&Copy")
        copy_action.setStatusTip("Copy to the Clipboard")

        paste_action = menu.addAction(QIcon("paste.png"), "&Paste")
        paste_action.setStatusTip("Paste from the Clipboard")

        menu.addSeparator()
        insert_before = menu.addAction(
            QIcon("paste.png"), "Insert before"
        )
        insert_before.setStatusTip(
            "insert an empty attribute (column) " "before this one"
        )

        insert_after = menu.addAction(
            QIcon("paste.png"), "Insert After"
        )
        insert_after.setStatusTip(
            "insert an empty attribute (column) after" " this one"
        )

        delete_action = menu.addAction(QIcon("delete.png"), "&Delete")
        delete_action.setStatusTip("Delete this atttribute (column)")

        # Add Help action if the clicked widget has help text.
        if hasattr(clicked_widget, "help_text") and clicked_widget.help_text:
            menu.addSeparator()
            help_action = menu.addAction("Help")
        else:
            help_action = None

        menu.addSeparator()
        clear_action = menu.addAction("Clear content")

        # Execute the menu.
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == copy_action:
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
        elif action == insert_before:
            self.parent_ui.insert_before(self)
        elif action == insert_after:
            self.parent_ui.insert_after(self)
        elif action == delete_action:
            self.parent_ui.delete_attr(self)
        elif help_action is not None and action == help_action:
            msg = QMessageBox(self)
            # msg.setTextFormat(Qt.RichText)
            msg.setText(clicked_widget.help_text)
            msg.setWindowTitle("Help")
            msg.show()
        self.in_context = False

    def to_xml(self):
        """
        Description:
            Returns an FGDC XML element (<attr>) representing the
            current contents of this attribute widget.

        Passed arguments:
            None

        Returned objects:
            attr (lxml.etree._Element): The XML node for the attribute.

        Workflow:
            1. Gets the current domain content (either from the active
               widget or the stored memory).
            2. Builds the <attrdomv> structure based on the domain type.
            3. Creates and attaches the <attrlabl>, <attrdef>, and
               <attrdefs> nodes.
            4. Attaches the No Data domain if configured.

        Notes:
            None
        """

        cur_index = self.ui.comboBox.currentIndex()

        # Get the domain XML content.
        if self.active:
            # Store content from the active widget before serializing.
            self.store_current_content()
            domain = self.domain.to_xml()
        elif self._domain_content[cur_index] is not None:
            # Use stored content if not active.
            domain = self._domain_content[cur_index]
        else:
            # Populate content and get XML if neither is available.
            self.populate_domain_content(cur_index)
            domain = self.domain.to_xml()

        # Build the <attr> node structure.
        if self.ui.comboBox.currentIndex() == 0:
            # Enumerated domain uses <attr> as its root tag.
            attr = xml_utils.XMLNode(domain)

            # Remove redundant attrlabl/attrdef/attrdefs children
            # (they are re-added below).
            attr.clear_children(tag="attrlabl")
            attr.clear_children(tag="attrdef")
            attr.clear_children(tag="attrdefs")
            attr = attr.to_xml()
        else:
            # Other domains use <attrdomv> wrapper.
            attr = xml_utils.xml_node("attr")
            attrdomv = xml_utils.xml_node("attrdomv", parent_node=attr)
            attrdomv.append(domain)

        # Add the common attribute elements (<attrlabl>, etc.).
        xml_utils.xml_node(
            "attrlabl",
            text=self.ui.fgdc_attrlabl.text(),
            parent_node=attr,
            index=0,
        )
        xml_utils.xml_node(
            "attrdef",
            text=self.ui.fgdc_attrdef.toPlainText(),
            parent_node=attr,
            index=1,
        )
        xml_utils.xml_node(
            "attrdefs",
            text=self.ui.fgdc_attrdefs.text(),
            parent_node=attr,
            index=2,
        )

        # Add the No Data domain if it exists.
        if self.nodata_content[0]:
            attrdomv = xml_utils.xml_node(
                "attrdomv", parent_node=attr, index=3
            )
            attrdomv.append(self.nodata_content[1])

        return attr

    def from_xml(self, attr):
        """
        Description:
            Populates the widget with a representation of the passed
            attribute XML element.

        Passed arguments:
            attr (lxml.etree._Element): The XML node for the attribute.

        Returned objects:
            None

        Workflow:
            1. Populates common fields ("attrlabl", "attrdef", etc.).
            2. Identifies and extracts the No Data domain if present.
            3. Checks for multiple domain types and warns the user if found.
            4. Sets the combobox index and stores the primary domain XML
               in "_domain_content".

        Notes:
            The code has special logic to identify and remove the No Data
            domain from the main list of domains.
        """

        try:
            self.clear_widget()
            if attr.tag == "attr":
                # Populate common widgets.
                utils.populate_widget(self, attr)
                attr_node = xml_utils.XMLNode(attr)

                # Get all <attrdomv> children.
                attrdomvs = attr_node.xpath("attrdomv", as_list=True)

                # List of domain tags (<edom>, <rdom>, etc.).
                attr_domains = [a.children[0].tag for a in attrdomvs]

                # --- No Data Domain Detection and Extraction ---
                for attrdomv in attrdomvs:
                    domain_tag = attrdomv.children[0].tag
                    edomv_text = attrdomv.children[0].children[0].text
                    edomvd_text = attrdomv.children[0].children[1].text
                    is_nodata_def = edomvd_text.lower() in [
                        "nodata", "no data"
                    ]

                    # Check for edom containing a known No Data value,
                    # or explicitly defined as No Data, or if it's the
                    # *only* edom when there are multiple domains total.
                    if (
                            domain_tag == "edom"
                            and (edomv_text in self.nodata_matches
                                 or is_nodata_def)
                    ) or (
                            domain_tag == "edom"
                            and len(attr_domains) > 1
                            and attr_domains.count("edom") == 1
                    ):
                        self.ui.rbtn_nodata_yes.setChecked(True)
                        self.nodata_content = (
                            1,
                            attrdomv.children[0].to_xml(),
                        )
                        # Remove the No Data domain from the list
                        attrdomvs.remove(attrdomv)
                        attr_domains.remove("edom")
                        # Also remove it from the XML tree
                        try:
                            edomv = attr.xpath(
                                f"attrdomv/edom/edomv[text()='{edomv_text}']"
                            )[0]
                            nd_attrdomv = edomv.getparent().getparent()
                            nd_attrdomv.getparent().remove(nd_attrdomv)
                        except Exception:
                            pass
                        break

                # --- Primary Domain Detection and Assignment ---
                if len(set(attr_domains)) > 1:
                    # Warning for multiple domain types.
                    msg = (
                        "Multiple domain types found in the "
                        f"attribute/column '{self.ui.fgdc_attrlabl.text()}'."
                        "\n i.e. more than one of Enumerated, Range, "
                        "Codeset, and Unrepresentable was used to "
                        "describe a single column.\n\n"
                        "While this is valid in the FGDC schema the "
                        "MetadataWizard is not designed to handle this."
                        "\n\nOnly the first of these domains will be "
                        "displayed and retained in the output saved "
                        "from this tool."
                        "\n\nIf having this structure is important please "
                        "use a different tool for editing this section."
                    )
                    msgbox = QMessageBox(
                        QMessageBox.Warning, "Too many domain types",
                        msg
                    )
                    utils.set_window_icon(msgbox)
                    msgbox.exec_()

                # Set combobox index and store primary domain XML
                if len(attrdomvs) == 0:
                    self.ui.comboBox.setCurrentIndex(3)  # Unrepresentable
                elif attr_domains[0] == "edom":
                    self.ui.comboBox.setCurrentIndex(0)  # Enumerated
                    self._domain_content[0] = attr
                elif attr_domains[0] == "udom":
                    self.ui.comboBox.setCurrentIndex(3)  # Unrepresentable
                    self._domain_content[3] = attr.xpath(
                        "attrdomv/udom"
                    )[0]
                elif attr_domains[0] == "rdom":
                    self.ui.comboBox.setCurrentIndex(1)  # Range
                    self._domain_content[1] = attr.xpath(
                        "attrdomv/rdom"
                    )[0]
                elif attr_domains[0] == "codesetd":
                    self.ui.comboBox.setCurrentIndex(2)  # Codeset
                    self._domain_content[2] = attr.xpath(
                        "attrdomv/codesetd"
                    )[0]
                else:
                    self.ui.comboBox.setCurrentIndex(3)  # Default
            else:
                print("The tag is not attr")
        except KeyError:
            pass


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(Attr, "attr testing")
