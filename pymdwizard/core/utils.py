"""Various utility and misc functions used in this project.

Attributes
----------

"""
from lxml import etree
import requests

from PyQt4 import QtGui
from PyQt4 import QtCore

from pymdwizard.core import xml_utils

USGS_AD_URL = "http://geo-nsdi.er.usgs.gov/contact-xml.php?email={}"


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


def populate_widget(widget, data_dict):
    """
    uses the

    Parameters
    ----------
    widget : QtGui:QWidget
            This widget has QLineEdits with names that correspond to the keys
            in the dictionary.
    data_dict : dict
            A dictionary containing key that correspond to line edits and
            values that will be inserted as text.  This dictionary will be
            flattened if it contains a nested hierarchy.
    Returns
        None
    -------

    """
    for key, value in data_dict.items():
        if isinstance(value, dict):
            populate_widget(widget, value)
        else:
            try:
                line_edit = widget.findChild(QtGui.QLineEdit, key)
                line_edit.setText(value)
            except:
                pass
