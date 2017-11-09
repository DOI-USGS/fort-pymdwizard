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
    import codecs
    file = codecs.open(fname, "w", "utf-8")
    file.write(node_to_string(element))
    file.close()


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
        node_dict[tag] = node.text
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


def search_xpath(node, xpath, only_first=True):
    """

    Parameters
    ----------
    node : lxml node

    xpath : string
        xpath.search

    only_first : boolean
        flag to indicate return type
        True == only return first element found or None if none found
        False == return list of matches found or [] if none found

    Returns
    -------
    list of lxml nodes
    """

    if type(node) == etree._Element or \
            type(node) == etree._ElementTree:
        matches = node.xpath(xpath)
        if len(matches) == 0:
            if only_first:
                return None
            else:
                return []
        elif len(matches) == 1 and only_first:
            return matches[0]
        elif len(matches) >= 1 and not only_first:
            return matches
        else:
            return matches[0]
    else:
        if only_first:
            return None
        else:
            return []



def get_text_content(node, xpath=''):
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
    if node is None:
        return None

    if xpath:
        nodes = node.xpath(xpath)
    else:
        nodes = [node, ]

    if nodes:
        result = nodes[0].text
        if result is None:
            return ''
        else:
            return result
    else:
        return ''


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
    return etree.tostring(node, pretty_print=True, with_tail=False,
                          encoding='UTF-8', xml_declaration=True).decode()


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
    try:
        return etree.parse(fname)
    except:
        msg = "Error encounterd opening the selected file"
        msg += "\n Please make sure file exists and is valid FGDC XML"



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
    if str(text):
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

###############################################################################
# Experimental xml convenience classes
###############################################################################

class XMLRecord(object):
    def __init__(self, contents):
        try:
            if os.path.exists(contents[:255]):
                self.fname = contents
                #they passed us a file path
                self.record = etree.parse(self.fname)
                self._root = self.record.getroot()
            else:
                self.fname = None
                self._root = string_to_node(contents)
                self.record = etree.ElementTree(self._root)
        except etree.XMLSyntaxError:
            self.fname = None
            self.record = etree.fromstring(contents)
            self._root = self.record.getroot()

        self.tag = self._root.tag
        self.__dict__[self._root.tag] = XMLNode(self.record.getroot())
        self._contents = self.__dict__[self._root.tag]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__[self.tag].__str__()

    def serialize(self):
        return self.__str__()

    def save(self, fname=''):
        if not fname:
            fname = self.fname

        with open(fname, "w") as text_file:
            text_file.write(self.__str__())

    def validate(self, schema='fgdc', as_dataframe=True):
        from pymdwizard.core import fgdc_utils

        return fgdc_utils.validate_xml(self._contents.to_xml(), xsl_fname=schema,
                                as_dataframe=as_dataframe)


class XMLNode(object):
    def __init__(self, element=None, tag='', text='', parent_node=None, index=-1):
        self.text = text
        self.tag = tag
        self.children = []

        if type(element) == etree._Element:
            self.from_xml(element)
        elif tag:
            element = xml_node(tag=tag, text=text)
            self.from_xml(element)
        elif type(element) == str:
            self.from_str(element)

        if parent_node is not None:
            parent_node.add_child(self, index=index, deepcopy=False)

    def __repr__(self):
        return self.__str__()

    def __str__(self, level=0):
        if self.text:
            cur_node = xml_node(self.tag, self.text)
            result = "{}{}".format("  "*level, etree.tostring(cur_node, pretty_print=True).decode()).rstrip()
        else:
            result = "{}<{}>".format("  "*level, self.tag, self.tag)
            for child in self.children:
                if type(self.__dict__[child.tag]) == XMLNode:
                    child = self.__dict__[child.tag]
                result += '\n' + child.__str__(level=level+1)
            result += '\n{}</{}>'.format("  "*level, self.tag)
        return result

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.to_str() == other.to_str()
        return False

    def from_xml(self, element):
        self.element = element
        self.tag = element.tag
        self.add_attr(self.tag, self)
        try:
            self.text = element.text.strip()
        except:
            self.text = ''

        self.children = []
        for child_node in self.element.getchildren():
            child_object = XMLNode(child_node)
            self.children.append(child_object)
            self.add_attr(child_node.tag, child_object)

    def add_attr(self, tag, child_object):
        if tag in self.__dict__:
            cur_contents = self.__dict__[tag]
            if type(cur_contents) == list:
                cur_contents.append(child_object)
            else:
                self.__dict__[tag] = [cur_contents, child_object]
        else:
            self.__dict__[tag] = child_object

    def to_xml(self):
        str_element = self.to_str()
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        element = etree.fromstring(str_element, parser=parser)
        return element

    def from_str(self, str_element):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        element = etree.fromstring(str_element, parser=parser)
        self.from_xml(element)

    def to_str(self):
        return self.__str__()

    def search_xpath(self, xpath=''):
        if not xpath:
            return self

        xpath_items = xpath.split('/')
        if len(xpath_items) == 1:
            xpath_remainder = ''
        else:
            xpath_remainder = '/'.join(xpath_items[1:])
        first_item = xpath_items[0]
        try:
            tag, index = split_tag(first_item)
            results = self.__dict__[tag]
            if '[' in first_item:
                first_result = results[index]
                return first_result.search_xpath(xpath_remainder)
            else:
                if type(results) == list:
                    aggregator = []
                    for result in results:
                        node = result.search_xpath(xpath_remainder)
                        if node is not None:
                            aggregator.append(node)
                    return aggregator
                else:
                    return results.search_xpath(xpath_remainder)
        except:
            return []

    def xpath(self, xpath='', as_list=True, as_text=False):
        results = self.search_xpath(xpath)
        if as_list and not type(results) == list:
            results = [results]

        if as_text:
            results = [r.text for r in results if r]

        return results

    def xpath_march(self, xpath, as_list=True):
        """
        for a given xpath, return the most distant matching element
        iteratively searches an xpath until a match is found removing the last
        element each time

        Parameters
        ----------
        xpath
        as_list

        Returns
        -------

        """
        xpath_items = xpath.split('/')

        while xpath_items:
            result = self.xpath('/'.join(xpath_items))
            if result:
                return result
            xpath_items.pop()

        return []

    def clear_children(self, tag=None):
        if tag is not None:
            self.children = [c for c in self.children if c.tag != tag]
        else:
            self.children = []

    def replace_child(self, new_child, tag=None, deepcopy=True):
        """
        replaces the

        Parameters
        ----------
        tag : Str (optional)
            The child node tag that will be replaced.
            If not supplied the tag of the child node will be used.
        child : XMLNode

        Returns
        -------
        None
        """
        if tag is None:
            tag = new_child.tag
        for i, child in enumerate(self.children):
            if child.tag == tag:
                del self.children[i]
                self.add_child(new_child, i, deepcopy=deepcopy)

    def add_child(self, child, index=-1, deepcopy=True):
        if index == -1:
            index = len(self.children)
        if index < -1:
            index += 1

        if type(child) == etree._Element:
            node_str = node_to_string(child)
        else:
            node_str = child.to_str()
        child_copy = XMLNode(node_str)

        if deepcopy:
            self.children.insert(index, child_copy)
        else:
            self.children.insert(index, child)
        self.add_attr(child.tag, child)

    def copy(self):
        node_str = self.to_str()
        self_copy = XMLNode(node_str)
        return self_copy


def split_tag(tag):
    """
    parse an xml tag into the tag itself and the tag index
    Parameters
    ----------
    tag : str
        xml tag that might or might not have a [n] item

    Returns
    -------
    tuple: fgdc_tag, index
    """
    if '[' in tag:
        fgdc_tag, tag = tag.split('[')
        index = int(tag.split(']')[0])-1
    else:
        fgdc_tag = tag
        index = 0
    return fgdc_tag, index


