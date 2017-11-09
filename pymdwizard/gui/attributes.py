#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/
PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a Metadata Date <timeperd> section
SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None
U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.
Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.
Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

import pandas as pd

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QIcon
from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_attributes
from pymdwizard.gui import attr

class Attributes(WizardWidget):  #

    drag_label = "Attributes <attr>"
    acceptable_tags = ['attr']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_attributes.Ui_Form()  # .Ui_USGSContactInfoWidgetMain()
        self.ui.setupUi(self)

        self.main_layout = self.ui.scrollAreaWidgetContents.layout()

        self.attrs = []
        self.displayed_min = 0
        self.displayed_max = 9

        self.minimize_children()

    def load_df(self, df):
        self.clear_children()

        i = 0
        for col_label in df.columns:
            col = df[col_label]
            attr_i = attr.Attr(parent=self)
            attr_i.ui.fgdc_attrlabl.setText(str(col_label))

            attr_i.set_series(col)
            attr_i.ui.comboBox.setCurrentIndex(attr_i.guess_domain())
            self.append_attr(attr_i)

        self.attrs[0].supersize_me()

    def append_attr(self, attr):
        self.attrs.append(attr)
        self.main_layout.insertWidget(len(self.main_layout) - 1, attr)

    def load_pickle(self, contents):
        self.clear_children()

        if self.original_xml is not None:
            self._from_xml(self.original_xml)
        else:

            for col_label in contents.keys():
                attr_i = attr.Attr(parent=self)
                attr_i.ui.fgdc_attrlabl.setText(col_label)

                if contents[col_label][b'type'] == 'String':
                    s = pd.Series(contents[col_label][b'contents'])
                    attr_i.set_series(s)
                    attr_i.guess_domain()
                elif contents[col_label][b'type'] in ['Integer', 'Single', 'SmallInteger', 'Double', 'Date']:
                    s = pd.Series(contents[col_label][b'contents'])
                    attr_i.set_series(s)
                    attr_i.ui.comboBox.setCurrentIndex(1)
                else:
                    attr_i.populate_domain_content(3)
                    unrep = contents[col_label][b'contents']

                    utils.set_text(attr_i.ui.fgdc_attrdef, unrep[0].decode("utf-8"))
                    utils.set_text(attr_i.domain.ui.fgdc_udom, unrep[1].decode("utf-8"))
                    utils.set_text(attr_i.ui.fgdc_attrdefs, unrep[2].decode("utf-8"))
                    attr_i.store_current_content()
                    attr_i.supersize_me()
                    attr_i.regularsize_me()
                self.append_attr(attr_i)

            try:
                self.attrs[0].supersize_me()
            except IndexError:
                pass

    def clear_children(self):
        for attribute in self.attrs:
            attribute.deleteLater()
        self.attrs = []

    def get_attr(self, which):
        for attr in self.attrs:
            if attr.ui.fgdc_attrlabl.text() == which:
                return attr
        return None

    def insert_before(self, this_attr):
        new_attrs = []
        for i, attribute in enumerate(self.attrs):
            if attribute == this_attr:
                new_attr = attr.Attr(parent=self)
                self.main_layout.insertWidget(i, new_attr)
                new_attrs.append(new_attr)
            new_attrs.append(attribute)
        self.attrs = new_attrs

    def insert_after(self, this_attr):
        new_attrs = []
        for i, attribute in enumerate(self.attrs):
            new_attrs.append(attribute)
            if attribute == this_attr:
                new_attr = attr.Attr(parent=self)
                self.main_layout.insertWidget(i+1, new_attr)
                new_attrs.append(new_attr)
        self.attrs = new_attrs

    def delete_attr(self, this_attr):
        keep_attrs = []
        for attribute in self.attrs:
            if attribute == this_attr:
                attribute.deleteLater()
            else:
                keep_attrs.append(attribute)
        self.attrs = keep_attrs

    def minimize_children(self):
        for attr_widget in self.attrs:
            if attr_widget.active:
                attr_widget.regularsize_me()
                attr_widget.ui.fgdc_attrlabl.setCursorPosition(0)

    def contextMenuEvent(self, event):
        self.in_context = True
        clicked_widget = self.childAt(event.pos())

        menu = QMenu(self)
        copy_action = menu.addAction(QIcon('copy.png'), '&Copy')
        copy_action.setStatusTip('Copy to the Clipboard')

        paste_action = menu.addAction(QIcon('paste.png'), '&Paste')
        paste_action.setStatusTip('Paste from the Clipboard')

        menu.addSeparator()
        add_attr = menu.addAction(QIcon('paste.png'), 'Add attribute (column)')
        add_attr.setStatusTip('Add attribute')

        if hasattr(clicked_widget, 'help_text') and clicked_widget.help_text:
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
            elif clicked_widget.objectName() == 'idinfo_button':
                self.idinfo.copy_mime()
            elif clicked_widget.objectName() == 'dataquality_button':
                self.dataqual.copy_mime()
            elif clicked_widget.objectName() == 'eainfo_button':
                self.eainfo.copy_mime()
            elif clicked_widget.objectName() == 'distinfo_button':
                self.distinfo.copy_mime()
            elif clicked_widget.objectName() == 'metainfo_button':
                self.metainfo.copy_mime()
            else:
                self.copy_mime()
        elif action == paste_action:
            self.paste_mime()
        elif action == clear_action:
            if clicked_widget is None:
                self.clear_widget()
            elif clicked_widget.objectName() == 'idinfo_button':
                self.idinfo.clear_widget()
            elif clicked_widget.objectName() == 'dataquality_button':
                self.dataqual.clear_widget()
            elif clicked_widget.objectName() == 'eainfo_button':
                self.eainfo.clear_widget()
            elif clicked_widget.objectName() == 'distinfo_button':
                self.distinfo.clear_widget()
            elif clicked_widget.objectName() == 'metainfo_button':
                self.metainfo.clear_widget()
            else:
                self.clear_widget()
        elif action == add_attr:
            new_attr = attr.Attr(parent=self)
            self.append_attr(new_attr)
            self.minimize_children()
            new_attr.supersize_me()
        elif help_action is not None and action == help_action:
            msg = QMessageBox(self)
            # msg.setTextFormat(Qt.RichText)
            msg.setText(clicked_widget.help_text)
            msg.setWindowTitle("Help")
            msg.show()
        self.in_context = False


    def dragEnterEvent(self, e):
        """
        Attributes never accept drops
        Parameters
        ----------
        e : qt eventr
        Returns
        -------
        """
        e.ignore()


    def _to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        detailed = xml_utils.xml_node('detailed')
        for a in self.attrs:
            detailed.append(a._to_xml())

        return detailed

    def _from_xml(self, detailed):
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
            if detailed.tag == 'detailed':
                self.original_xml = detailed
                self.clear_children()
                for attr_node in detailed.xpath('attr'):
                    attr_widget = attr.Attr(parent=self)
                    attr_widget._from_xml(attr_node)

                    self.attrs.append(attr_widget)
                    self.main_layout.insertWidget(len(self.main_layout) - 1, attr_widget)

                self.minimize_children()
                self.attrs[0].supersize_me()
            else:
                print ("The tag is not udom")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Attributes,
                        "attr_list testing")
