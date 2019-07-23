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
Module contains a variety of miscellaneous functions


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey (USGS).
Although the software has been subjected to rigorous review, 
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

import sys
import os
from os.path import dirname
import platform
import datetime
import traceback
import pkg_resources

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

import requests

import pandas as pd

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

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

    result = requests_pem_get(USGS_AD_URL.format(ad_username))
    element = xml_utils.string_to_node(result.content)

    try:
        if element.xpath("cntperp/cntper")[0].text == "GS ScienceBase":
            element.xpath("cntperp")[0].tag = "cntorgp"
    except:
        pass

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
        return get_usgs_contact_info(ad_username)["fgdc_cntperp"]["fgdc_orcid"]
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
        return widget
    except:
        e = sys.exc_info()[0]
        print("problem encountered", e)
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
    return pkg_resources.resource_filename("pymdwizard", "resources/{}".format(fname))


def set_window_icon(widget, remove_help=True):
    """
    Add our default ducky icon to a widget

    Parameters
    ----------
    widget : PyQt widget
    remove_help : Bool
                  Whether to show the help question mark icon.
    Returns
    -------
    None
    """
    icon = QIcon(get_resource_path("icons/Ducky.ico"))
    widget.setWindowIcon(icon)
    if remove_help:
        widget.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    options = {
        "striped": True,
        "stripesColor": "#fafafa",
        "na_values": "least",
        "tooltip_min_len": 21,
    }

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
            if (
                ret is not None and ret == ret
            ):  # convert to str except for None, NaN, NaT
                if isinstance(ret, float):
                    ret = "{:n}".format(ret)
                elif isinstance(ret, datetime.date):
                    # FIXME: show microseconds optionally
                    ret = ret.strftime(("%x", "%c")[isinstance(ret, datetime.datetime)])
                else:
                    ret = str(ret)
                if role == Qt.ToolTipRole:
                    if len(ret) < self.options["tooltip_min_len"]:
                        ret = ""
                return ret
        elif role == Qt.BackgroundRole:
            if self.options["striped"] and row % 2:
                return QBrush(QColor(self.options["stripesColor"]))

        return None

    def dataframe(self):
        return self.df

    def reorder(self, oldIndex, newIndex, orientation):
        "Reorder columns / rows"
        horizontal = orientation == Qt.Horizontal
        cols = list(self.df.columns if horizontal else self.df.index)
        cols.insert(newIndex, cols.pop(oldIndex))
        self.df = self.df[cols] if horizontal else self.df.T[cols].T
        return True

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return
        label = getattr(self.df, ("columns", "index")[orientation != Qt.Horizontal])[
            section
        ]
        #        return label if type(label) is tuple else label
        return (
            ("\n", " | ")[orientation != Qt.Horizontal].join(str(i) for i in label)
            if type(label) is tuple
            else str(label)
        )

    def dataFrame(self):
        return self.df

    def sort(self, column, order):
        if len(self.df):
            asc = order == Qt.AscendingOrder
            na_pos = (
                "first" if (self.options["na_values"] == "least") == asc else "last"
            )
            self.df.sort_values(
                self.df.columns[column], ascending=asc, inplace=True, na_position=na_pos
            )
            self.layoutChanged.emit()


def check_fname(fname):
    """
    Check that the given fname is in a directory that exists and the current
    users has write permission to.  If a file named fname already exists that
    it can be opened with write permission.

    Parameters
    ----------
    fname : str
            file path and name to check
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
        return "missing directory"
    if not os.path.exists(fname):
        try:
            f = open(fname, "w")
            f.close()
            os.remove(fname)
            return "good"
        except:
            return "not writable directory"
    else:
        try:
            f = open(fname, "a")
            f.close()
            return "good"
        except:
            return "not writable file"


def url_validator(url, qualifying=None):
    """
    Check whether a given string is in a valid url syntax

    Parameters
    ----------
    url : str
        The string to check for url syntax
    qualifying : list
        url attributes to check for as list of strings
        defaults to 'scheme' and 'netloc'

    Returns
    -------
        Bool
    """
    min_attributes = ("scheme", "netloc")
    qualifying = min_attributes if qualifying is None else qualifying
    token = urlparse(url)
    return all([getattr(token, qualifying_attr) for qualifying_attr in qualifying])


def get_install_dname(which="pymdwizard"):
    """
    get the full path to the installation directory

    Parameters
    ----------
    which : str, optional
            which subdirectory to return (
            one of: 'root', 'pymdwizard', or 'python'

    Returns
    -------
    str : path and directory name of the directory pymdwizard is in
    """
    this_fname = os.path.realpath(__file__)
    if platform.system() == "Darwin":
        # This is the path to the 'content' folder in the MetadataWizard.app
        pymdwizard_dname = os.path.abspath(
            os.path.join(dirname(this_fname), *[".."] * 7)
        )
        root_dir = pymdwizard_dname
        executable = sys.executable
        python_dname = os.path.split(executable)[0]
    else:
        pymdwizard_dname = dirname(dirname(dirname(this_fname)))
        root_dir = os.path.dirname(pymdwizard_dname)
        python_dname = os.path.join(root_dir, "Python35_64")
        if not os.path.exists(python_dname):
            python_dname = os.path.join(root_dir, "Python36_64")
        if not os.path.exists(python_dname):
            executable = sys.executable
            python_dname = os.path.split(executable)[0]

    if which == "root":
        return root_dir
    elif which == "pymdwizard":
        return pymdwizard_dname
    elif which == "python":
        return python_dname


def get_pem_fname():
    return os.path.join(
        get_install_dname("pymdwizard"), "pymdwizard", "resources", "DOIRootCA2.pem"
    )


def check_pem_file():
    """
    Convenience USGS only function that checks if the DOI PEM file is stored
    in the wincertstore and export a local copy for use in the application.

    Returns
    -------
    None
    """
    try:
        import wincertstore

        pem_fname = get_pem_fname()
        if not os.path.exists(pem_fname):
            for storename in ("CA", "ROOT"):
                with wincertstore.CertSystemStore(storename) as store:
                    for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
                        if "DOIRootCA2" in cert.get_name():
                            text_file = open(pem_fname, "w", encoding="ascii")
                            contents = cert.get_pem().encode().decode("ascii")
                            text_file.write(contents)
                            text_file.close()

        os.environ["PIP_CERT"] = pem_fname
        os.environ["SSL_CERT_FILE"] = pem_fname
        os.environ["GIT_SSL_CAINFO"] = pem_fname
        return pem_fname
    except:
        # this is an optional convenience function that will only work
        # on the Windows platform, for USGS users.
        # if anything goes wrong pass silently
        pass


def requests_pem_get(url, params={}):
    """
    Make a get requests.get call but use the local PEM fname if you hit an
    SSL error

    Parameters
    ----------
    url : str
          url to use
    params: dict
            parameters to pass on to the function

    Returns
    -------
        the results of the requests call
    """
    try:
        return requests.get(url, params=params)
    except requests.exceptions.SSLError:
        pem_fname = get_pem_fname()
        return requests.get(url, params=params, verify=pem_fname)


def get_setting(which, default=None):
    """
    return a pymdwizard application setting

    Parameters
    ----------
    which: str
            name of setting to return

    Returns
    -------
        setting in native format, string, integer, etc

    """
    settings = QSettings("USGS", "pymdwizard")
    if default is None:
        return settings.value(which)
    else:
        return settings.value(which, default)
