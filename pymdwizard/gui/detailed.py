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
file's name.


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

import os
import pickle

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import QSettings

from pymdwizard.core import utils
from pymdwizard.core import xml_utils
from pymdwizard.core import data_io
from pymdwizard.core import spatial_utils
from pymdwizard.core.spatial_utils import get_raster_attribute_table

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_detailed
from pymdwizard.gui import attributes


class Detailed(WizardWidget):  #

    drag_label = "Detailed Description <detailed>"
    acceptable_tags = ['detailed']

    def __init__(self, remove_function=None, parent=None):
        self.EA = parent
        WizardWidget.__init__(self, parent=parent)
        if remove_function is None:
            self.ui.btn_remove.hide()
        else:
            self.ui.btn_remove.clicked.connect(remove_function)

    def build_ui(self):
        """
        Build and modify this widget's GUI
        Returns
        -------
        None
        """
        self.ui = UI_detailed.Ui_fgdc_detailed()
        self.ui.setupUi(self)
        self.ui.displayed_widget.hide()

        self.attributes = attributes.Attributes(parent=self)
        self.ui.attribute_frame.layout().addWidget(self.attributes)

        self.setup_dragdrop(self)

        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.fgdc_enttypl.textChanged.connect(self.update_tooltip)

    def browse(self):
        settings = QSettings('USGS', 'pymdwizard')
        last_data_fname = settings.value('lastDataFname', '')
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        filter = "data files (*.csv *.txt *.shp *.xls *.xlsm *.xlsx "
        filter += "*.tif *.grd *.png *.img *.jpg *.hdr *.bmp *.adf)"

        fname = QFileDialog.getOpenFileName(self, fname, dname,
                                            filter=filter)
        if fname[0]:
            settings.setValue('lastDataFname', fname[0])
            try:
                self.populate_from_fname(fname[0])
            except BaseException as e:
                import traceback
                msg = "Could not extract data from file %s:\n%s." % (fname, traceback.format_exc())
                QMessageBox.warning(self, "Data file error", msg)

    def update_tooltip(self):
        try:
            cur_text = self.ui.fgdc_enttypl.text()
            cur_index = self.EA.ui.fgdc_eainfo.currentIndex()
            self.EA.ui.fgdc_eainfo.setTabToolTip(cur_index, cur_text)
        except:
            pass

    def update_displayed_label(self):
        pass

    def populate_from_fname(self, fname):
        if fname.endswith('$'):
            fname, sheet_name = os.path.split(fname)
            sheet_name = sheet_name[:-1]
            ok = True
        else:
            sheet_name = None

        shortname = os.path.split(fname)[1]
        ext = os.path.splitext(shortname)[1]

        self.ui.fgdc_enttypds.setText('Producer defined')
        if ext.lower() == '.csv':
            try:
                self.clear_widget()
                self.ui.fgdc_enttypl.setText(shortname)
                self.ui.fgdc_enttypd.setPlainText('Comma Separated Value (CSV) file containing data.')

                df = data_io.read_data(fname)

                if df.shape[0] == data_io.MAX_ROWS:
                    msg = "This CSV file contains more than" \
                          " {:,} rows!".format(data_io.MAX_ROWS)
                    msg += "\n\n Due to speed and memory constraints, " \
                           "\ndata from rows past\nthe first {:,} rows" \
                           "".format(data_io.MAX_ROWS)
                    msg += "\nwere not used " \
                           "to populate this section.".format(data_io.MAX_ROWS)
                    msg += '\n\nCheck that the values displayed are ' \
                           'complete \nand appropriate for the entire record.'
                    QMessageBox.warning(self, "Large File Warning", msg)

                self.attributes.load_df(df)
            except BaseException as e:
                import traceback
                msg = "Cannot read csv %s:\n%s." % (fname, traceback.format_exc())
                QMessageBox.warning(self, "Recent Files", msg)

        elif ext.lower() == '.shp':
            self.clear_widget()
            self.ui.fgdc_enttypl.setText(shortname + ' Attribute Table')
            self.ui.fgdc_enttypd.setPlainText('Table containing attribute information associated with the data set.')

            df = data_io.read_data(fname)
            self.attributes.load_df(df)

            fid_attr = self.attributes.get_attr('FID')
            if fid_attr is not None:
                fid_attr.populate_domain_content(3)
                fid_attr.ui.fgdc_attrdef.setPlainText('Internal feature number.')
                utils.set_text(fid_attr.ui.fgdc_attrdefs, 'ESRI')
                fid_attr.domain.ui.fgdc_udom.setPlainText("Sequential unique whole numbers that are automatically generated.")
                fid_attr.regularsize_me()
                fid_attr.supersize_me()
            shape_attr = self.attributes.get_attr('Shape')
            if shape_attr is not None:
                shape_attr.populate_domain_content(3)
                shape_attr.ui.fgdc_attrdef.setPlainText('Feature geometry.')
                utils.set_text(shape_attr.ui.fgdc_attrdefs, 'ESRI')
                shape_attr.domain.ui.fgdc_udom.setPlainText("Coordinates defining the features.")
                shape_attr.store_current_content()
                shape_attr.supersize_me()
                shape_attr.regularsize_me()

        elif ext.lower() in ['.xlsm', '.xlsx', '.xls']:
            if sheet_name is None:
                sheets = data_io.get_sheet_names(fname)

                sheet_name, ok = QInputDialog.getItem(self, "select sheet dialog",
                                    "Pick one of the sheets from this workbook",
                                                      sheets, 0, False)
            if ok and sheet_name:
                self.clear_widget()
                self.ui.fgdc_enttypl.setText('{} ({})'.format(shortname, sheet_name))
                self.ui.fgdc_enttypd.setPlainText('Excel Worksheet')

                df = data_io.read_excel(fname, sheet_name)
                self.attributes.load_df(df)
        elif ext.lower() in ['.tif', '.grd', '.png', '.img', '.jpg', '.hdr',
                             '.bmp', '.adf']:
            self.ui.fgdc_enttypl.setText(shortname)

            num_bands = spatial_utils.get_band_count(fname)
            if num_bands == 1:
                self.ui.fgdc_enttypd.setPlainText('Raster geospatial data file.')
            else:
                self.ui.fgdc_enttypd.setPlainText('{} band raster geospatial data file.'.format(num_bands))

            df = get_raster_attribute_table(fname)
            self.attributes.load_df(df)
            oid_attr = self.attributes.get_attr('OID')
            if oid_attr is not None:
                oid_attr.populate_domain_content(3)
                oid_attr.ui.fgdc_attrdef.setPlainText('Internal object identifier.')
                oid_attr.domain.ui.fgdc_udom.setPlainText('Sequential unique whole numbers that are automatically generated.')
                oid_attr.regularsize_me()
                oid_attr.supersize_me()
            value_attr = self.attributes.get_attr('Value')
            if value_attr is not None:
                value_attr.populate_domain_content(1)
                value_attr.ui.fgdc_attrdef.setPlainText('Unique numeric values contained in each raster cell.')
            count_attr = self.attributes.get_attr('Count')
            if count_attr is not None:
                count_attr.populate_domain_content(1)
                count_attr.ui.fgdc_attrdef.setPlainText('Number of raster cells with this value.')

        elif ext.lower() == ".p":
            p = pickle.load(open(fname, "rb"), encoding='bytes')

            if self.original_xml is not None:
                original_content = xml_utils.XMLNode(self.original_xml)
                self.from_xml(self.original_xml)
            else:
                self.ui.fgdc_enttypl.setText('{}'.format(shortname[:-2]))
                self.ui.fgdc_enttypd.setPlainText('Geospatial Dataset')
                self.attributes.load_pickle(p)
        elif ext.lower() == '.txt':
            if sheet_name is None:
                delimiters = {'comma': ',', 'tab': '\t',
                              'pipe': '|', 'colon': ':'}

                delimiter_str, ok = QInputDialog.getItem(self, "Select text delimiter",
                                                      "Pick the delimiter used in this file",
                                                      delimiters.keys(), 0, False)

                delimiter = delimiters[delimiter_str]

            if ok and delimiter:
                try:
                    self.clear_widget()
                    self.ui.fgdc_enttypl.setText(shortname)
                    self.ui.fgdc_enttypd.setPlainText('{} delimited text file.'.format(delimiter_str))

                    df = data_io.read_data(fname, delimiter=delimiter)
                    self.attributes.load_df(df)
                except BaseException as e:
                    import traceback
                    msg = "Cannot read txt file %s:\n%s." % (fname, traceback.format_exc())
                    QMessageBox.warning(self, "File load problem", msg)
        else:
            msg = "Can only read '.csv', '.txt', '.shp', raster files, and Excel files here"
            QMessageBox.warning(self, "Unsupported file format", msg)

    def clear_widget(self):
        """
        Clears all content from this widget

        Returns
        -------
        None
        """
        self.ui.fgdc_enttypl.setText('')
        self.ui.fgdc_enttypd.setPlainText('')
        self.attributes.clear_children()

    def has_content(self):
        """
        Checks for valid content in this widget

        Returns
        -------
        Boolean
        """
        has_content = False

        if self.ui.fgdc_enttypl.text():
            has_content = True
        if self.ui.fgdc_enttypd.toPlainText():
            has_content = True

        if len(self.attributes.attrs) > 0:
            has_content = True

        return has_content

    def to_xml(self):
        """
        encapsulates the QTabWidget text for Metadata Time in an element tag
        Returns
        -------
        timeperd element tag in xml tree
        """
        detailed = xml_utils.xml_node('detailed')
        enttyp = xml_utils.xml_node('enttyp', parent_node=detailed)
        enttypl = xml_utils.xml_node('enttypl', text=self.ui.fgdc_enttypl.text(), parent_node=enttyp)
        enttypd = xml_utils.xml_node('enttypd', text=self.ui.fgdc_enttypd.toPlainText(), parent_node=enttyp)
        enttypds = xml_utils.xml_node('enttypds', text=self.ui.fgdc_enttypds.text(), parent_node=enttyp)

        attr = self.attributes.to_xml()
        for a in attr.xpath('attr'):
            detailed.append(a)
        return detailed

    def from_xml(self, detailed):
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
                utils.populate_widget(self, detailed)
                self.attributes.from_xml(detailed)
            else:
                print ("The tag is not a detailed")
        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(Detailed,
                        "detailed testing")

