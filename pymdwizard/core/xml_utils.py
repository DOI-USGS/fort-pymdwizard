#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a variety of xml processing functions.


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
# built in Python imports
import os
import collections
import warnings

# external library imports
from lxml import etree

try:
    import pandas as pd
except ImportError:
    warnings.warn('Pandas library not installed, dataframes disabled')
    pd = None


def xml_document_loader(xml_locator):
    """

    Parameters
    ----------
    xml_locator : str or lxml element or lxml document
                if str can be one of:
                    file path and name to an xml document
                    string representation of an xml document
                    TODO: add option for url that resolves to an xml document
                lxml element or document

    Returns
    -------
        lxml element
    """

    if isinstance(xml_locator, str):
        if os.path.exists(xml_locator):
            return fname_to_node(xml_locator)
        else:
            return string_to_node(xml_locator)

    else:
        return xml_locator


def save_to_file(element, fname):
    """
    Save the provided element as the filename provided
    Parameters
    ----------
    element : lxml element
    fname : str

    Returns
    -------
    None
    """
    with open(fname, "w") as text_file:
        text_file.write(node_to_string(element))


def node_to_dict(node, add_fgdc=True):
    """

    Parameters
    ----------
    node : lxml element

    Returns
    -------
        dictionary contain a key value pair for each child item in the node
        where the key is the item's tag and the value is the item's text
    """
    node_dict = collections.OrderedDict()

    if len(node.getchildren()) == 0:
        tag = _parse_tag(node.tag)
        if add_fgdc:
            tag = 'fgdc_' + tag
        node_dict[tag] =  node.text
    else:
        for child in node.getchildren():
            tag = _parse_tag(child.tag)
            if add_fgdc:
                tag = 'fgdc_' + tag
            if len(child.getchildren()) > 0:
                content = node_to_dict(child, add_fgdc=add_fgdc)
            else:
                content = child.text
            node_dict[tag] = content
    return node_dict


def _parse_tag(tag):
    """
    strips namespace declaration from xml tag string

    Parameters
    ----------
    tag : str

    Returns
    -------
    formatted tag

    """
    return tag[tag.find("}")+1:]


def element_to_list(results):
    """
    Returns the results(etree) formatted into a list of dictionaries.
    This is useful for flat data structures, e.g. homogeneous results that
    could be thought of and converted to a dataframe.

    Parameters
    ----------
    results : list of lxml nodes
        This list would could be returned from an xpath query for example

    Returns
    -------
    List of dictionaries. Each dictionary in this list is the result of
    the _node_to_dict function
    """
    return [node_to_dict(item, add_fgdc=False) for item in results]


def search_xpath(node, xpath):
    """

    Parameters
    ----------
    node : lxml node

    xpath : xpath.search

    Returns
    -------
    list of lxml nodes
    """
    return node.xpath(xpath)


def get_text_content(node, xpath):
    """
    return the text from a specific node

    Parameters
    ----------
    node : lxml node

    xpath : xpath.search

    Returns
    -------
    str
    None if that xpath is not found in the node
    """
    nodes = node.xpath(xpath)
    if nodes:
        return nodes[0].text
    else:
        return None


def element_to_df(results):
    """
    Returns the results (etree) formatted into a pandas dataframe.
    This only intended to be used on flat data structures, e.g. a list of
    homogeneous elements.
    For nested or hierarchical data structures this result will be awkward.

    Parameters
    ----------
    results : list of lxml nodes
        This list would could be returned from an xpath query for example

    Returns
    -------
    pandas dataframe
    """
    results_list = element_to_list(results)
    return pd.DataFrame.from_dict(results_list)


def node_to_string(node):
    """

    Parameters
    ----------
    node : lxml note

    Returns
    -------

    str :
    Pretty string representation of node
    """
    return etree.tostring(node, pretty_print=True).decode()


def fname_to_node(fname):
    """

    Parameters
    ----------
    fname : str
            full file and path to the the file to load
    Returns
    -------
    lxml node
    """
    return etree.parse(fname)


def string_to_node(str_node):
    """
    covert an string representation of a node into an lxml node

    Parameters
    ----------
    str_node : str
               string representation of an XML element

    Returns
    -------
    lxml node
    """
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    element = etree.fromstring(str_node, parser=parser)
    return element


def xml_node(tag, text='', parent_node=None, index=-1):
    """
    convenience function for creating an xml node

    Parameters
    ----------
    tag : str
          The tag (e.g. fgdc short name) to be assigned to the node
    text : str, optional
          The text contents of the node.
    parent_node : lxml element, optional
          the node created by this function will be
          appended to this nodes children
    index : int, optional
          The positional index to insert the node at. (zero based)
          If none specified will append node to end of existing children.

    Returns
    -------
        the lxml node created by the function.
    """

    node = etree.Element(tag)
    if text:
        node.text = str(text)

    if parent_node is not None:
        if index == -1:
            parent_node.append(node)
        else:
            parent_node.insert(index, node)

    return node


def clear_children(element):
    """
    Removes all child elements from the element passed
    Parameters
    ----------
    xml_node : lxml element

    Returns
    -------
    None
    """
    for child in element.getchildren():
        element.remove(child)



