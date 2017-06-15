#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Contains a variety of miscellaneous functions used in the the metadata wizard


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
import sys
import os
import datetime
import traceback
import pkg_resources

from lxml import etree
import requests

import pandas as pd

from PyQt5.QtWidgets import QLineEdit, QTextEdit, QTextBrowser, QPlainTextEdit
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap, QIcon

from pymdwizard.core import xml_utils

USGS_AD_URL = "https://geo-nsdi.er.usgs.gov/contact-xml.php?email={}"


def get_usgs_contact_info(ad_username, as_dictionary=True):
    """

    Parameters
    ----------
    ad_username : str
                  The active directory username to return the
                  contact information for
    as_dictionary : bool
                    specify return format as nested dictionary or lxml element
    Returns
    -------
        None if ad_username is not found
        FGDC Contact Section as dictionary or lxml element
    """

    result = requests.get(USGS_AD_URL.format(ad_username))
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    element = etree.fromstring(result.content, parser=parser)

    if as_dictionary:
        return xml_utils.node_to_dict(element)
    else:
        return element


def get_orcid(ad_username):
    """

    Parameters
    ----------
    ad_username : the AD user name to search for

    Returns
    -------
    str : the orcid as a string, if not found returns None

    """
    try:
        return get_usgs_contact_info(ad_username)['fgdc_cntperp']['fgdc_orcid']
    except:
        return None


def populate_widget(widget, contents):
    """
    uses the

    Parameters
    ----------
    widget : QtGui:QWidget
            This widget has QLineEdits with names that correspond to the keys
            in the dictionary.
    contents : dict
            A dictionary containing key that correspond to line edits and
            values that will be inserted as text.  This dictionary will be
            flattened if it contains a nested hierarchy.
    Returns
    -------
    None

    """
    if not isinstance(contents, dict):
        contents = xml_utils.node_to_dict(contents)

    for key, value in contents.items():
        if isinstance(value, dict):
            populate_widget(widget, value)
        else:
            try:
                child_widget = getattr(widget.ui, key)
            except AttributeError:
                try:
                    child_widget = getattr(widget, key)
                except AttributeError:
                    child_widget = None

            set_text(child_widget, value)


def set_text(widget, text):
    """
    set the text of a widget regardless of it's base type

    Parameters
    ----------
    widget : QtGui:QWidget
            This widget is a QlineEdit or QPlainText edit
    text : str
            The text that will be inserted
    Returns
    -------
    None

    """
    if isinstance(widget, QLineEdit):
        widget.setText(text)
        widget.setCursorPosition(0)

    if isinstance(widget, QPlainTextEdit):
        widget.setPlainText(text)

    if isinstance(widget, QTextBrowser):
        widget.setText(text)

    if isinstance(widget, QComboBox):
        index = widget.findText(text, Qt.MatchFixedString)
        if index >= 0:
            widget.setCurrentIndex(index)
        else:
            widget.setEditText(text)


def populate_widget_element(widget, element, xpath):
    """
    if the xpath is present in the element
    set the text or plainText of it to the first result of that xpath's text

    Parameters
    ----------
    widget : pyqt widget, lineEdit or plainTextEdit
    element : lxml element
    xpath : str
            xpath to the child element in the element

    Returns
    -------
        None
    """
    if element.xpath(xpath):
        first_child = element.xpath(xpath)[0]
        set_text(widget, first_child.text)


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def launch_widget(Widget, title="", **kwargs):
    """
    run a widget within it's own application
    Parameters
    ----------
    widget : QWidget
    title : str
            The title to use for the application

    Returns
    -------
    None
    """

    try:
        app = QApplication([])
        app.title = title
        widget = Widget(**kwargs)
        widget.setWindowTitle(title)
        widget.show()
        sys.exit(app.exec_())
    except:
        e = sys.exc_info()[0]
        print('problem encountered', e)
        print(traceback.format_exc())


def get_resource_path(fname):
    """

    Parameters
    ----------
    fname : str
            filename that you would like to find

    Returns
    -------
            the full file path to the resource specified
    """
    return pkg_resources.resource_filename('pymdwizard',
                                           'resources/{}'.format(fname))
def set_window_icon(widget):
    icon = QIcon(get_resource_path('icons/Ducky.ico'))
    widget.setWindowIcon(icon)

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    options = {"striped": True, "stripesColor": "#fafafa", "na_values": "least",
               "tooltip_min_len": 21}

    def __init__(self, dataframe, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.setDataFrame(dataframe if dataframe is not None else pd.DataFrame())

    def setDataFrame(self, dataframe):
        self.df = dataframe
        #        self.df_full = self.df
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.df.values)

    def columnCount(self, parent=None):
        return self.df.columns.size

    def data(self, index, role=Qt.DisplayRole):

        row, col = index.row(), index.column()
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            ret = self.df.iat[row, col]
            if ret is not None and ret==ret: #convert to str except for None, NaN, NaT
                if isinstance(ret, float):
                    ret = "{:n}".format(ret)
                elif isinstance(ret, datetime.date):
                    #FIXME: show microseconds optionally
                    ret = ret.strftime(("%x", "%c")[isinstance(ret, datetime.datetime)])
                else: ret = str(ret)
                if role == Qt.ToolTipRole:
                    if len(ret)<self.options["tooltip_min_len"]: ret = ""
                return ret
        elif role == Qt.BackgroundRole:
            if self.options["striped"] and row%2:
                return QBrush(QColor(self.options["stripesColor"]))

        return None

    def dataframe(self):
        return self.df

    def reorder(self, oldIndex, newIndex, orientation):
        "Reorder columns / rows"
        horizontal = orientation==Qt.Horizontal
        cols = list(self.df.columns if horizontal else self.df.index)
        cols.insert(newIndex, cols.pop(oldIndex))
        self.df = self.df[cols] if horizontal else self.df.T[cols].T
        return True

    #    def filter(self, filt=None):
    #        self.df = self.df_full if filt is None else self.df[filt]
    #        self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole: return
        label = getattr(self.df, ("columns", "index")[orientation!=Qt.Horizontal])[section]
        #        return label if type(label) is tuple else label
        return ("\n", " | ")[orientation!=Qt.Horizontal].join(str(i) for i in label) if type(label) is tuple else str(label)

    def dataFrame(self):
        return self.df

    def sort(self, column, order):
        if len(self.df):
            asc = order==Qt.AscendingOrder
            na_pos = 'first' if (self.options["na_values"]=="least") == asc else 'last'
            self.df.sort_values(self.df.columns[column], ascending=asc,
                                inplace=True, na_position=na_pos)
            self.layoutChanged.emit()

def check_fname(fname):
    """
    Check that the given fname is in a directory that exists and the current
    users has write permission to.  If a file named fname already exists that
    it can be opened with write permission.

    Parameters
    ----------
    fname : str

    Returns
    -------
    str :
    one of:
    'good' if the fname is good on all criteria
    'missing directory' if the directory does not exist
    'not writable directory' if the user does not have write access
    'not writable file' if there is a lock on the file
    Boolean if the file is writable
    """

    dname = os.path.split(fname)[0]
    if not os.path.exists(dname):
        return 'missing directory'
    if not os.path.exists(fname):
        try:
            f = open(fname, "w")
            f.close()
            os.remove(fname)
            return 'good'
        except:
            return 'not writable directory'
    else:
        try:
            f = open(fname, "a")
            f.close()
            return 'good'
        except:
            return 'not writable file'


def get_install_dname(which='pymdwizard'):
    """
    get the full path to the installation directory
    Returns
    -------
    str : path and directory name of the directory pymdwizard is in
    """
    this_fname = os.path.realpath(__file__)
    pymdwizard_dname = os.path.dirname(os.path.dirname(os.path.dirname(this_fname)))
    root_dir = os.path.dirname(pymdwizard_dname)
    python_dname = os.path.join(root_dir, 'Python35_64')

    if which == 'root':
        return root_dir
    elif which == 'pymdwizard':
        return pymdwizard_dname
    elif which == 'python':
        return python_dname


