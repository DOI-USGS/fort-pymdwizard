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
files name.


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

import numpy as np

import sip

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_attr
from pymdwizard.gui import udom
from pymdwizard.gui import rdom
from pymdwizard.gui import codesetd
from pymdwizard.gui import edom_list
from pymdwizard.gui import edom
from pymdwizard.gui.ui_files.spellinghighlighter import Highlighter
from pymdwizard.core import data_io

default_def_source = utils.get_setting('defsource', 'Producer Defined')

class Attr(WizardWidget):

    drag_label = "Attribute <attr>"
    acceptable_tags = ['attr']

    def __init__(self, parent=None):
        # This changes to true when this attribute is being viewed/edited
        self.active = False
        self.ef = 0

        self.nodata = None
        self.nodata_content = (False, None) # nodata checked, last nodata node

        WizardWidget.__init__(self, parent=parent)

        # an in memory record of all  the contents that were selected
        self._previous_index = -1
        cbo = self.ui.comboBox
        self._domain_content = dict.fromkeys(range(cbo.count()), None)

        self.parent_ui = parent
        self.series = None
        self.ui.nodata_section.hide()
        self.highlighter = Highlighter(self.ui.fgdc_attrdef.document())

        self.nodata_matches = ['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN',
                               '-nan', '1.#IND', '1.#QNAN', 'N/A', 'NA', 'NULL', 'NaN',
                               'n/a', 'nan', 'null', -9999, '-9999', '', 'Nan', '<< empty cell >>']

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_attr.Ui_attribute_widget()
        self.ui.setupUi(self)

        # self.ui.fgdc_attrdef.installEventFilter(self)
        self.ui.fgdc_attrdef.setMouseTracking(True)
        self.ui.fgdc_attrdefs.installEventFilter(self)
        self.ui.attrdomv_contents.installEventFilter(self)
        self.ui.place_holder.installEventFilter(self)

        self.setup_dragdrop(self)
        self.ui.comboBox.currentIndexChanged.connect(self.change_domain)
        self.ui.fgdc_attr.mousePressEvent = self.mousePressEvent
        self.ui.fgdc_attrlabl.mousePressEvent = self.attrlabl_press
        self.ui.fgdc_attrdef.mousePressEvent = self.attrdef_press
        self.ui.fgdc_attrdefs.mousePressEvent = self.attrdefs_press
        self.ui.comboBox.mousePressEvent = self.combo_press
        self.ui.rbtn_nodata_yes.toggled.connect(self.include_nodata_change)

        self.domain = None
        self.ui.nodata_content.hide()
        self.ui.rbtn_nodata_no.setChecked(True)
        self.ui.comboBox.setCurrentIndex(3)

        self.ui.fgdc_attrdefs.setText(default_def_source)

    def include_nodata_change(self, b):
        """
            The user has changed the nodata present selection

            Parameters
            ----------
            b: qt event

            Returns
            -------
            None
            """
        if b:
            self.ui.nodata_section.show()
            # self.nodata
            # self.nodata_edom.show()
        else:
            self.ui.nodata_section.hide()
            # self.nodata = None

    def mousePressEvent(self, event):
        self.activate()

    def attrlabl_press(self, event):
        self.activate()
        return QLineEdit.mousePressEvent(self.ui.fgdc_attrlabl, event)

    def attrdef_press(self, event):
        self.activate()
        return QPlainTextEdit.mousePressEvent(self.ui.fgdc_attrdef, event)

    def attrdefs_press(self, event):
        self.activate()
        return QLineEdit.mousePressEvent(self.ui.fgdc_attrdefs, event)

    def combo_press(self, event):
        self.activate()
        return QComboBox.mousePressEvent(self.ui.comboBox, event)

    def clear_domain(self):
        for child in self.ui.attrdomv_contents.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def clear_nodata(self):
        try:
            self.nodata_edom.deleteLater()
        except:
            pass


    def set_series(self, series):
        """
        store a series with this attri
        Parameters
        ----------
        series : pandas series

        Returns
        -------
        None
        """
        self.series = series

    def guess_domain(self):
        """
        return the index of the domain the associated series is thought to
        best match.

        if there are less than twenty unique items in the series the guess
        is enumerated
        if it's numeric the guess is range.
        else it's unrepresentable

        Returns
        -------
        int : index of the domain the associated series is
            thought to best match
        """
        # given a series of data take a guess as to which
        # domain type is appropriate

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

        # without a series to introspect we're going to default to udom
        return 3  # unrepresentable

    def store_current_content(self):
        """
        Save the current contents (xml format) into our domain contents dict

        Returns
        -------
        None
        """
        if self.domain is not None and not sip.isdeleted(self.domain):
            cur_xml = self.domain.to_xml()
            if cur_xml.tag == 'udom':
                self._domain_content[3] = cur_xml
            elif cur_xml.tag == 'codesetd':
                self._domain_content[2] = cur_xml
            elif cur_xml.tag == 'rdom':
                self._domain_content[1] = cur_xml
            elif cur_xml.tag == 'attr':
                self._domain_content[0] = cur_xml

        if self.ui.rbtn_nodata_yes.isChecked() and \
           not sip.isdeleted(self.nodata_edom):
            self.nodata_content = (True, self.nodata_edom.to_xml())
        else:
            self.nodata_content = (False, None)


    def populate_domain_content(self, which='guess'):
        """
        Fill out this widget with the content from it's associated series

        Parameters
        ----------
        which : str, optional, one of 'guess' or the index to force
            if guess introspect the series associated with this attribute
            and make a best guess as to which domain to use.

        Returns
        -------
        None
        """
        self.clear_domain()

        if which == 'guess':
            self.sniff_nodata()
            index = self.guess_domain()
        else:
            index = which

        self.ui.comboBox.setCurrentIndex(index)

        if index == 0:
            self.domain = edom_list.EdomList(parent=self)
        elif index == 1:
            self.domain = rdom.Rdom(parent=self)
        elif index == 2:
            self.domain = codesetd.Codesetd(parent=self)
        else:
            self.domain = udom.Udom(parent=self)

        if self._domain_content[index] is not None:
            # This domain has been used before, display previous content
            self.domain.from_xml(self._domain_content[index])
        elif self.series is not None and index == 0:
            clean_series = data_io.clean_nodata(self.series, self.nodata)
            uniques = clean_series.unique()

            if len(uniques) > 100:
                msg = "There are more than 100 unique values in this field."
                msg += "\n This tool cannot smoothly display that many " \
                       "entries. "
                msg += "\nTypically an enumerated domain is not used with " \
                       "that many unique entries."
                msg += "\n\nOnly the first one hundred are displayed below!"
                msg += "\nYou will likely want to change the domain to one " \
                       "of the other options."
                QMessageBox.warning(self, "Too many unique entries", msg)
                self.domain.populate_from_list(uniques[:101])
            else:
                self.domain.populate_from_list(uniques)
        elif self.series is not None and index == 1:
            clean_series = data_io.clean_nodata(self.series, self.nodata)
            try:
                self.domain.ui.fgdc_rdommin.setText(str(clean_series.min()))
            except:
                self.domain.ui.fgdc_rdommin.setText('')
            try:
                self.domain.ui.fgdc_rdommax.setText(str(clean_series.max()))
            except:
                self.domain.ui.fgdc_rdommax.setText('')

            if not np.issubdtype(clean_series.dtype, np.number):
                msg = 'Caution! The contents of this column are stored in the' \
                      ' data source as "text".  The use of a range domain ' \
                      'type on text columns might give unexpected results, ' \
                      'especially for columns that contain date information.'
                msgbox = QMessageBox(QMessageBox.Warning, "Range domain on text field",
                                     msg)
                utils.set_window_icon(msgbox)
                msgbox.exec_()
        self.ui.attrdomv_contents.layout().addWidget(self.domain)

    def change_domain(self):
        """
        When changing the domain we must first store the current contents
        in our internal contents dictionary before loading the next.

        Returns
        -------
        None
        """
        if self.active:
            self.store_current_content()
            self.clear_domain()

            self.populate_domain_content(self.ui.comboBox.currentIndex())

    def supersize_me(self):
        """
        Expand this attribute and display it's contents

        Returns
        -------
        None
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

            self.nodata_edom.ui.fgdc_edomv.textChanged.connect(self.nodata_changed)
            self.ui.nodata_section.layout().addWidget(self.nodata_edom)

    def regularsize_me(self):
        """
        Collapse this attribute and hide it's content

        Returns
        -------
        None
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
        When an attribute is activated minimize all the other attributes
        in the parent attribute list

        Returns
        -------
        None
        """
        if self.active:
            #we're already big so do nothing
            pass
        else:
            if self.parent_ui is not None:
                self.parent_ui.minimize_children()
            self.supersize_me()

    def nodata_changed(self):
        """remove """
        self.nodata = self.nodata_edom.ui.fgdc_edomv.text()
        if self.nodata == "<< empty cell >>":
            self.nodata = ""
        self.clean_domain_nodata()

    def clean_domain_nodata(self):
        if self.domain is not None and not sip.isdeleted(self.domain):
            cur_xml = self.domain.to_xml()
            if cur_xml.tag == 'rdom':
                self._domain_content[1] = cur_xml
            elif cur_xml.tag == 'attr':
                edoms = self.domain.edoms
                self._domain_content[0] = cur_xml

    def sniff_nodata(self):
        uniques = self.series.unique()

        self.nodata = None
        for nd in self.nodata_matches:
            if nd in list(uniques):
                self.nodata = nd

        if self.nodata is None:
            self.nodata_content = (False, self.nodata_content[1])
        else:
            temp_edom = edom.Edom()
            if self.nodata == '':
                temp_edom.ui.fgdc_edomv.setText('<< empty cell >>')
            else:
                temp_edom.ui.fgdc_edomv.setText(str(self.nodata))

            temp_edom.ui.fgdc_edomvd.setPlainText('No Data')
            self.nodata_content = (True, temp_edom.to_xml())
            temp_edom.deleteLater()

    def contextMenuEvent(self, event):

        self.in_context = True
        clicked_widget = self.childAt(event.pos())


        menu = QMenu(self)
        copy_action = menu.addAction(QIcon('copy.png'), '&Copy')
        copy_action.setStatusTip('Copy to the Clipboard')

        paste_action = menu.addAction(QIcon('paste.png'), '&Paste')
        paste_action.setStatusTip('Paste from the Clipboard')

        menu.addSeparator()
        insert_before = menu.addAction(QIcon('paste.png'), 'Insert before')
        insert_before.setStatusTip('insert an empty attribute (column) '
                                   'before this one')

        insert_after = menu.addAction(QIcon('paste.png'), 'Insert After')
        insert_after.setStatusTip('insert an empty attribute (column) after'
                                  ' this one')

        delete_action = menu.addAction(QIcon('delete.png'), '&Delete')
        delete_action.setStatusTip('Delete this atttribute (column)')

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
        return an XML element with the contents of this widget,
        augmented with any original content not displayed on the widget
        if applicable.

        Returns
        -------
        XML Element
        """
        cur_index = self.ui.comboBox.currentIndex()

        if self.active:
            domain = self.domain.to_xml()
        elif self._domain_content[cur_index] is not None:
            domain = self._domain_content[cur_index]
        else:
            self.populate_domain_content(cur_index)
            domain = self.domain.to_xml()

        if self.ui.comboBox.currentIndex() == 0:
            attr = xml_utils.XMLNode(domain)
            attr.clear_children(tag='attrlabl')
            attr.clear_children(tag='attrdef')
            attr.clear_children(tag='attrdefs')
            attr = attr.to_xml()
        else:
            attr = xml_utils.xml_node('attr')
            attrdomv = xml_utils.xml_node('attrdomv', parent_node=attr)
            attrdomv.append(domain)

        attrlabl = xml_utils.xml_node('attrlabl',
                                      text=self.ui.fgdc_attrlabl.text(),
                                      parent_node=attr, index=0)
        attrdef = xml_utils.xml_node('attrdef',
                                     text=self.ui.fgdc_attrdef.toPlainText(),
                                     parent_node=attr, index=1)
        attrdefs = xml_utils.xml_node('attrdefs',
                                      text=self.ui.fgdc_attrdefs.text(),
                                      parent_node=attr, index=2)

        if self.nodata_content[0]:
            attrdomv = xml_utils.xml_node('attrdomv', parent_node=attr,
                                          index=3)
            attrdomv.append(self.nodata_content[1])

        return attr

    def from_xml(self, attr):
        """
        Populate widget with a representation of the passed XML element

        Parameters
        ----------
        attr : XML Element

        Returns
        -------
        None
        """
        try:
            self.clear_widget()
            if attr.tag == 'attr':

                utils.populate_widget(self, attr)
                attr_node = xml_utils.XMLNode(attr)
                attrdomvs = attr_node.xpath('attrdomv', as_list=True)
                attr_domains = [a.children[0].tag for a in attrdomvs]

                # pull out the first no data attribute domain
                for attrdomv in attrdomvs:
                    if attrdomv.children[0].tag == 'edom' and \
                            (attrdomv.children[0].children[0].text in self.nodata_matches or \
                            attrdomv.children[0].children[1].text.lower() in ['nodata', 'no data']
                            or (attr_domains.count('edom')==1) and len(attr_domains) > 1):
                        self.ui.rbtn_nodata_yes.setChecked(True)
                        self.nodata_content = (1, attrdomv.children[0].to_xml())
                        attrdomvs.remove(attrdomv)
                        attr_domains.remove('edom')
                        try:
                            edomv = attr.xpath("attrdomv/edom/edomv[text()='{}']".format(attrdomv.children[0].children[0].text))[0]
                            nd_attrdomv = edomv.getparent().getparent()
                            nd_attrdomv.getparent().remove(nd_attrdomv)
                        except:
                            pass
                        break

                if len(set(attr_domains)) > 1:
                    # multiple domain types present in this attr
                    msg = "Multiple domain types found in the attribute/column '{}'."
                    msg += "\ni.e. more than one of Enumerated, Range, "
                    msg += "Codeset, and Unrepresentable was used to "
                    msg += "was used to describe a single column.\n\n"
                    msg += "While this is valid in the FGDC schema the "
                    msg += "MetadataWizard is not designed to handle this."
                    msg += "\n\nOnly the first of these domains will be displayed "
                    msg += "and retained in the output saved from this tool."
                    msg += "\n\nIf having this structure is import please use"
                    msg += " a different tool for editing this section."
                    msg = msg.format(self.ui.fgdc_attrlabl.text())
                    msgbox = QMessageBox(QMessageBox.Warning, "Too many domain types",
                                         msg)
                    utils.set_window_icon(msgbox)
                    msgbox.exec_()

                if len(attrdomvs) == 0:
                    self.ui.comboBox.setCurrentIndex(3)
                elif attr_domains[0] == 'edom':
                    self.ui.comboBox.setCurrentIndex(0)
                    self._domain_content[0] = attr
                elif attr_domains[0] == 'udom':
                    self.ui.comboBox.setCurrentIndex(3)
                    self._domain_content[3] = attr.xpath('attrdomv/udom')[0]
                elif attr_domains[0] == 'rdom':
                    self.ui.comboBox.setCurrentIndex(1)
                    self._domain_content[1] = attr.xpath('attrdomv/rdom')[0]
                elif attr_domains[0] == 'codesetd':
                    self.ui.comboBox.setCurrentIndex(2)
                    self._domain_content[2] = attr.xpath('attrdomv/codesetd')[0]
                else:
                    self.ui.comboBox.setCurrentIndex(3)
            else:
                print("The tag is not attr")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Attr,
                        "attr testing")
