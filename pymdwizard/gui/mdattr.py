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

def qwidget_is_valid(widget) -> bool:
    """
    Return True if 'widget' is a live Qt object we can safely touch.
    PyQt raises RuntimeError if the wrapped C/C++ object has been deleted.
    """
    if widget is None:
        return False
    try:
        _ = widget.objectName()
        return True
    except RuntimeError:
        return False

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
    drag_label = "Attribute &lt;attr&gt;"
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
            "&lt;&lt; empty cell &gt;&gt;",
        ]

    def build_ui(self):
        """
        Description:
            Builds and modifies this widget's GUI.
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
        """Show/Hide the No Data config section."""
        if b:
            self.ui.nodata_section.show()
        else:
            self.ui.nodata_section.hide()

    def mousePressEvent(self, event):
        """Activate the widget on click."""
        self.activate()

    def attrlabl_press(self, event):
        """Activate + pass the event to QLineEdit."""
        self.activate()
        return QLineEdit.mousePressEvent(self.ui.fgdc_attrlabl, event)

    def attrdef_press(self, event):
        """Activate + pass the event to QPlainTextEdit."""
        self.activate()
        return QPlainTextEdit.mousePressEvent(self.ui.fgdc_attrdef, event)

    def attrdefs_press(self, event):
        """Activate + pass the event to QLineEdit."""
        self.activate()
        return QLineEdit.mousePressEvent(self.ui.fgdc_attrdefs, event)

    def combo_press(self, event):
        """Activate + pass the event to QComboBox."""
        self.activate()
        return QComboBox.mousePressEvent(self.ui.comboBox, event)

    def clear_domain(self):
        """Remove current domain widget from layout."""
        for child in self.ui.attrdomv_contents.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def clear_nodata(self):
        """Remove No Data enumerated domain widget if present."""
        try:
            self.nodata_edom.deleteLater()
        except AttributeError:
            pass

    def set_series(self, series):
        """Associate a pandas Series with this attribute."""
        self.series = series

    def guess_domain(self):
        """
        Guess the appropriate FGDC domain type index based on the data series.
        Returns:
            0: Enumerated, 1: Range, 3: Unrepresentable
        """

        if self.series is None:
            return 3

        if self.series is not None:
            if self.nodata is not None:
                clean_series = data_io.clean_nodata(self.series, self.nodata)
            else:
                clean_series = self.series

            uniques = clean_series.unique()
            if np.issubdtype(clean_series.dtype, np.number):
                return 1  # range
            elif len(uniques) < 20:
                return 0  # enumerated
            else:
                return 3  # unrepresentable

    def store_current_content(self):
        """
        Saves current domain and No Data content into memory caches.
        (SIP-free: uses qwidget_is_valid)
        """

        # Save the current primary domain content.
        if self.domain is not None and qwidget_is_valid(self.domain):
            cur_xml = self.domain.to_xml()
            if cur_xml.tag == "udom":
                self._domain_content[3] = cur_xml
            elif cur_xml.tag == "codesetd":
                self._domain_content[2] = cur_xml
            elif cur_xml.tag == "rdom":
                self._domain_content[1] = cur_xml
            elif cur_xml.tag == "attr":
                self._domain_content[0] = cur_xml

        # Save the current No Data domain content (if widget exists & checked).
        nodata_widget = getattr(self, "nodata_edom", None)
        if (self.ui.rbtn_nodata_yes.isChecked()
                and qwidget_is_valid(nodata_widget)):
            try:
                self.nodata_content = (True, nodata_widget.to_xml())
            except RuntimeError:
                self.nodata_content = (False, None)
        else:
            self.nodata_content = (False, None)

    def populate_domain_content(self, which="guess"):
        """
        Fills the attribute domain section with a new domain widget.
        """

        self.clear_domain()

        if which == "guess":
            self.sniff_nodata()
            index = self.guess_domain()
        else:
            index = which

        self.ui.comboBox.setCurrentIndex(index)

        if index == 0:      # Enumerated
            self.domain = edom_list.EdomList(parent=self)
        elif index == 1:    # Range
            self.domain = rdom.Rdom(parent=self)
        elif index == 2:    # Codeset
            self.domain = codesetd.Codesetd(parent=self)
        else:               # Unrepresentable
            self.domain = udom.Udom(parent=self)

        if self._domain_content[index] is not None:
            self.domain.from_xml(self._domain_content[index])
        elif self.series is not None and index == 0:
            clean_series = data_io.clean_nodata(self.series, self.nodata)
            uniques = clean_series.unique()

            if len(uniques) > 100:
                msg = (
                    "There are more than 100 unique values in this "
                    "field. This tool cannot smoothly display that "
                    "many entries. Typically an enumerated domain is "
                    "not used with that many unique entries."
                    "\n\nOnly the first one hundred are displayed "
                    "below! You will likely want to change the "
                    "domain to one of the other options."
                )
                QMessageBox.warning(self, "Too many unique entries", msg)
                self.domain.populate_from_list(uniques[:101])
            else:
                self.domain.populate_from_list(uniques)
        elif self.series is not None and index == 1:
            clean_series = data_io.clean_nodata(self.series, self.nodata)
            try:
                self.domain.ui.fgdc_rdommin.setText(str(clean_series.min()))
            except Exception:
                self.domain.ui.fgdc_rdommin.setText("")
            try:
                self.domain.ui.fgdc_rdommax.setText(str(clean_series.max()))
            except Exception:
                self.domain.ui.fgdc_rdommax.setText("")

            if not np.issubdtype(clean_series.dtype, np.number):
                msg = (
                    "Caution! The contents of this column are stored in the"
                    ' data source as "text".  The use of a range domain '
                    "type on text columns might give unexpected results, "
                    "especially for columns that contain date information."
                )
                msgbox = QMessageBox(
                    QMessageBox.Warning, "Range domain on text field", msg
                )
                utils.set_window_icon(msgbox)
                msgbox.exec_()

        self.ui.attrdomv_contents.layout().addWidget(self.domain)

    def change_domain(self):
        """Handle combobox change → store, clear, repopulate."""
        if self.active:
            self.store_current_content()
            self.clear_domain()
            self.populate_domain_content(self.ui.comboBox.currentIndex())

    def supersize_me(self):
        """
        Expand this attribute to show domain and No Data content.
        """

        if not self.active:
            self.active = True

            self.animation = QPropertyAnimation(self, b"minimumSize")
            self.animation.setDuration(200)
            self.animation.setEndValue(QSize(345, self.height()))
            self.animation.start()

            self.ui.attrdomv_contents.show()
            self.ui.place_holder.hide()
            cbo = self.ui.comboBox

            self.populate_domain_content(cbo.currentIndex())

            self.ui.nodata_content.show()
            self.nodata_edom = edom.Edom()

            self.ui.rbtn_nodata_yes.setChecked(self.nodata_content[0])

            if self.nodata_content[1] is not None:
                self.nodata_edom.from_xml(self.nodata_content[1])

            self.nodata_edom.ui.fgdc_edomv.textChanged.connect(
                self.nodata_changed)

            self.ui.nodata_section.layout().addWidget(self.nodata_edom)

    def regularsize_me(self):
        """
        Collapse this attribute and hide detailed content.
        """

        if self.active:
            self.store_current_content()

            self.animation = QPropertyAnimation(self, b"minimumSize")
            self.animation.setDuration(200)
            self.animation.setEndValue(QSize(100, self.height()))
            self.animation.start()

            self.ui.nodata_content.hide()
            self.clear_domain()
            self.clear_nodata()
            self.ui.place_holder.show()

        self.active = False

    def activate(self):
        """
        Minimize siblings and expand this attribute.
        """

        if self.active:
            pass
        else:
            if self.parent_ui is not None:
                self.parent_ui.minimize_children()
            self.supersize_me()

    def nodata_changed(self):
        """
        Update self.nodata from the No Data widget and refresh domain cache.
        """

        self.nodata = self.nodata_edom.ui.fgdc_edomv.text()
        if self.nodata == "&lt;&lt; empty cell &gt;&gt;":
            self.nodata = ""

        self.clean_domain_nodata()

    def clean_domain_nodata(self):
        """
        Force update of the primary domain's stored XML in _domain_content.
        (SIP-free: uses qwidget_is_valid)
        """

        if self.domain is not None and qwidget_is_valid(self.domain):
            try:
                cur_xml = self.domain.to_xml()
            except RuntimeError:
                return

            if cur_xml.tag == "rdom":
                self._domain_content[1] = cur_xml
            elif cur_xml.tag == "attr":
                # For enumerated domains which use the <attr> tag.
                edoms = getattr(self.domain, "edoms", None)  # retained from original
                self._domain_content[0] = cur_xml

    def sniff_nodata(self):
        """
        Detect common No Data values in the series and prefill the No Data domain.
        """

        uniques = self.series.unique()
        self.nodata = None

        for nd in self.nodata_matches:
            if nd in list(uniques):
                self.nodata = nd

        if self.nodata is None:
            self.nodata_content = (False, self.nodata_content[1])
        else:
            temp_edom = edom.Edom()
            if self.nodata == "":
                temp_edom.ui.fgdc_edomv.setText("&lt;&lt; empty cell &gt;&gt;")
            else:
                temp_edom.ui.fgdc_edomv.setText(str(self.nodata))

            temp_edom.ui.fgdc_edomvd.setPlainText("No Data")
            self.nodata_content = (True, temp_edom.to_xml())
            temp_edom.deleteLater()

    def contextMenuEvent(self, event):
        """
        Right-click context menu for Copy/Paste/Insert/Delete/Help.
        """

        self.in_context = True
        clicked_widget = self.childAt(event.pos())

        menu = QMenu(self)
        copy_action = menu.addAction(QIcon("copy.png"), "&Copy")
        copy_action.setStatusTip("Copy to the Clipboard")

        paste_action = menu.addAction(QIcon("paste.png"), "&Paste")
        paste_action.setStatusTip("Paste from the Clipboard")

        menu.addSeparator()
        insert_before = menu.addAction(QIcon("paste.png"), "Insert before")
        insert_before.setStatusTip("insert an empty attribute (column) before this one")

        insert_after = menu.addAction(QIcon("paste.png"), "Insert After")
        insert_after.setStatusTip("insert an empty attribute (column) after this one")

        delete_action = menu.addAction(QIcon("delete.png"), "&Delete")
        delete_action.setStatusTip("Delete this atttribute (column)")

        if hasattr(clicked_widget, "help_text") and clicked_widget.help_text:
            menu.addSeparator()
            help_action = menu.addAction("Help")
        else:
            help_action = None

        menu.addSeparator()
        clear_action = menu.addAction("Clear content")

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
            msg.setText(clicked_widget.help_text)
            msg.setWindowTitle("Help")
            msg.show()
        self.in_context = False

    def to_xml(self):
        """
        Return an FGDC <attr> XML element representing this attribute.
        """

        cur_index = self.ui.comboBox.currentIndex()

        # Get the domain XML content.
        if self.active:
            self.store_current_content()
            domain = self.domain.to_xml()
        elif self._domain_content[cur_index] is not None:
            domain = self._domain_content[cur_index]
        else:
            self.populate_domain_content(cur_index)
            domain = self.domain.to_xml()

        # Build the <attr> node structure.
        if self.ui.comboBox.currentIndex() == 0:
            # Enumerated domain uses <attr> as its root tag.
            attr = xml_utils.XMLNode(domain)
            attr.clear_children(tag="attrlabl")
            attr.clear_children(tag="attrdef")
            attr.clear_children(tag="attrdefs")
            attr = attr.to_xml()
        else:
            attr = xml_utils.xml_node("attr")
            attrdomv = xml_utils.xml_node("attrdomv", parent_node=attr)
            attrdomv.append(domain)

        # Add common elements
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

        # No Data domain
        if self.nodata_content[0]:
            attrdomv = xml_utils.xml_node(
                "attrdomv", parent_node=attr, index=3
            )
            attrdomv.append(self.nodata_content[1])

        return attr

    def from_xml(self, attr):
        """
        Populate the widget from an <attr> XML element.
        """

        try:
            self.clear_widget()
            if attr.tag == "attr":
                utils.populate_widget(self, attr)
                attr_node = xml_utils.XMLNode(attr)

                attrdomvs = attr_node.xpath("attrdomv", as_list=True)
                attr_domains = [a.children[0].tag for a in attrdomvs]

                # --- No Data Domain Detection and Extraction ---
                for attrdomv in attrdomvs:
                    domain_tag = attrdomv.children[0].tag
                    edomv_text = attrdomv.children[0].children[0].text
                    edomvd_text = attrdomv.children[0].children[1].text
                    is_nodata_def = edomvd_text.lower() in ["nodata", "no data"]

                    if (
                        domain_tag == "edom"
                        and (edomv_text in self.nodata_matches or is_nodata_def)
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
                        attrdomvs.remove(attrdomv)
                        attr_domains.remove("edom")
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
                        QMessageBox.Warning, "Too many domain types", msg
                    )
                    utils.set_window_icon(msgbox)
                    msgbox.exec_()

                if len(attrdomvs) == 0:
                    self.ui.comboBox.setCurrentIndex(3)  # Unrepresentable
                elif attr_domains[0] == "edom":
                    self.ui.comboBox.setCurrentIndex(0)  # Enumerated
                    self._domain_content[0] = attr
                elif attr_domains[0] == "udom":
                    self.ui.comboBox.setCurrentIndex(3)  # Unrepresentable
                    self._domain_content[3] = attr.xpath("attrdomv/udom")[0]
                elif attr_domains[0] == "rdom":
                    self.ui.comboBox.setCurrentIndex(1)  # Range
                    self._domain_content[1] = attr.xpath("attrdomv/rdom")[0]
                elif attr_domains[0] == "codesetd":
                    self.ui.comboBox.setCurrentIndex(2)  # Codeset
                    self._domain_content[2] = attr.xpath("attrdomv/codesetd")[0]
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
    utils.launch_widget(Attr, "attr testing")
