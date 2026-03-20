#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a variety of xml processing functions.

NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import os
import collections
import warnings
from pathlib import Path
import unicodedata
import codecs

# Non-standard python libraries.
try:
    from defusedxml import lxml
    from lxml import etree as etree
    import pandas as pd
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (fgdc_utils, utils)
except ImportError as err:
    raise ImportError(err, __file__)


def xml_document_loader(xml_locator):
    """
    Description:
        Loads an XML document from a file path, string, or as an lxml element.

    Args:
        xml_locator (str, lxml.Element, or lxml.Document): Can be a file path
            to an XML document, a string representation of an XML document,
            or an lxml element or document.
            TODO: add option for url that resolves to an xml document

    Returns:
        lxml.Element: The parsed lxml element from the XML input.
    """

    # Check if the xml_locator is a string.
    if isinstance(xml_locator, str):
        # If it is a file path and the file exists, load it.
        if os.path.exists(xml_locator):
            return fname_to_node(xml_locator)
        else:
            # Otherwise, treat it as a string representation of XML.
            return string_to_node(xml_locator)

    # If xml_locator is not a string, return it directly (assumed to be an
    # lxml element/document).
    return xml_locator


def save_to_file(element, fname):
    """
    Description:
        Saves the provided lxml element to a file with the specified name.

    Args:
        element (lxml.Element): The element to save to the file.
        fname (str): The filename where the element should be saved.

    Returns:
        None
    """

    # Open the file in write mode with UTF-8 encoding.
    with codecs.open(fname, "w", "utf-8") as file:
        # Convert the lxml element to a string and write to the file.
        file.write(node_to_string(element))
        # lxml.etree.tostring(element, encoding="unicode")


def node_to_dict(node, add_fgdc=True):
    """
    Description:
        Converts an lxml element node into a dictionary.

    Args:
        node (lxml.Element): The lxml element to convert.
        add_fgdc (bool): If True, prepend 'fgdc_' to the front of all tags.

    Returns:
        dict: A dictionary containing key-value pairs for each child item
            in the node, where the key is the item's tag and the value
            is the item's text.
    """

    # Create an ordered dictionary to maintain the order of elements.
    node_dict = collections.OrderedDict()

    # If the node has no children, process the current node.
    if len(node) == 0:
        tag = parse_tag(node.tag)
        if add_fgdc:
            tag = "fgdc_" + tag
        node_dict[tag] = node.text
    else:
        # Process each child node.
        for child in node:
            try:
                tag = parse_tag(child.tag)
                if add_fgdc:
                    tag = "fgdc_" + tag

                # Recursively convert child node to dictionary if it has
                # children.
                if len(child) > 0:
                    content = node_to_dict(child, add_fgdc=add_fgdc)
                else:
                    content = child.text

                # Add the tag and content to the dictionary.
                node_dict[tag] = content
            except AttributeError:
                # Ignore comments or processing instructions.
                pass

    return node_dict


def parse_tag(tag):
    """
    Description:
        Strips the namespace declaration from an XML tag string.

    Args:
        tag (str): The XML tag string potentially containing a namespace.

    Returns:
        str: The formatted tag without the namespace.
    """

    # Check if the tag contains a namespace and strip it out.
    return tag[tag.find("}") + 1 :]


def element_to_list(results):
    """
    Description:
        Converts a list of lxml nodes into a list of dictionaries.

    Args:
        results (list of lxml.Element): A list of lxml nodes, typically the
            result of an XPath query.

    Returns:
        list of dict: Each dictionary in the list represents a node, formatted
            by the node_to_dict function.
    """

    # Use a list comprehension to convert each node to a dictionary.
    return [node_to_dict(item, add_fgdc=False) for item in results]


def search_xpath(node, xpath, only_first=True):
    """
    Description:
        Searches for elements in an lxml node using an XPath expression.

    Args:
        node (lxml.Element or lxml.ElementTree): The node to search within.
        xpath (str): The XPath expression to evaluate against the node.
        only_first (bool):
            If True, return only the first element found or None if none found.
            If False, return a list of matches found, or an empty list if none.

    Returns:
        lxml.Element, or list of lxml.Elements:
            The first matched element if only_first is True,
            otherwise a list of matched elements.
    """

    # Check if node is of an acceptable type.
    if isinstance(node, (etree._Element, etree._ElementTree)):
        # Execute the XPath query.
        matches = node.xpath(xpath)

        # Return based on the number of matches and the only_first flag.
        if not matches:
            return None if only_first else []
        if only_first:
            return matches[0]  # Return the first match
        return matches  # Return all matches

    # Return None or empty list if the node type is invalid.
    return None if only_first else []


def get_text_content(node, xpath=""):
    """
    Description:
        Retrieves the text content from a specific node.

    Args:
        node (lxml.Element): The node from which to retrieve text content.

        xpath (str): An optional XPath expression to find specific sub-nodes.

    Returns:
        str: The text content of the first matching node or an empty string
            if the node is not found or contains no text.
    """

    # Return None if the provided node is None.
    if node is None:
        return None

    # Use the provided XPath to find nodes; use the node itself if no xpath is
    # given.
    nodes = node.xpath(xpath) if xpath else [node]

    # Check if any nodes were found
    if nodes:
        # Get the text content of the first node.
        result = nodes[0].text

        # Return empty string if result is None.
        return result if result is not None else ""

    # Return empty string if no nodes were found.
    return ""


def remove_control_characters(s):
    """
    Description:
        Removes control characters from the input string, keeping
        newline and tab characters.

    Args:
        s (str): The input string from which control characters will be removed.

    Returns:
        str: The cleaned string with control characters removed, except
            for newlines and tabs.
    """

    # Convert the input to a string (in case it is not already).
    s = str(s)

    # Use a generator expression to filter out control characters.
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C" or ch in ['\n', '\t']
    )


def element_to_df(results):
    """
    Description:
        Converts a list of lxml nodes into a pandas DataFrame.

    Args:
        results (list of lxml.Element): A list of lxml nodes, typically the
            result of an XPath query.

    Returns:
        pandas.DataFrame: A DataFrame containing the structured data from the
            lxml nodes. This is intended for flat data structures where each
            node represents a homogeneous element. For nested or hierarchical
            data structures, the result may be awkward.
    """

    # Convert the lxml nodes to a list of dictionaries.
    results_list = element_to_list(results)

    # Create and return a DataFrame from the list of dictionaries.
    return pd.DataFrame.from_dict(results_list)


def node_to_string(node, encoding=True):
    """
    Description:
        Converts an lxml node or tree to a pretty-printed string.

    Args:
        node (lxml.Element or lxml.ElementTree): The node or tree to convert to
            a string.

        encoding (bool, optional): If True, include an XML declaration in the
            output.

    Returns:
        str: A pretty string representation of the XML node or tree.
    """

    # Convert the node to an ElementTree if it is not already one.
    if not isinstance(node, etree._ElementTree):
        tree = etree.ElementTree(node)
    else:
        tree = node

    # Convert the ElementTree to a string with specified formatting options.
    return lxml.tostring(
        tree,
        pretty_print=True,  # Format with indentation
        with_tail=False,     # Do not include tail text
        encoding="UTF-8",   # Use UTF-8 encoding
        xml_declaration=encoding,  # Include XML declaration if specified
    ).decode("utf-8")  # Decode bytes to string


def fname_to_node(fname):
    """
    Description:
        Parses the contents of a local file into an lxml node object.

    Args:
        fname (str): The full file path to the XML file to load.

    Returns:
        lxml.Element: The root node of the parsed XML document.
    """

    # Parse the XML file and return the resulting lxml node object.
    return etree.parse(fname)


def string_to_node(str_node):
    """
    Description:
        Converts a string representation of an XML element into an lxml node.

    Args:
        str_node (str): The string representation of an XML element.

    Returns:
        lxml.Element: The parsed lxml node object created from the string.
    """

    # Create an XML parser with specified settings.
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")

    # Parse the string to create an lxml element.
    element = etree.fromstring(str_node, parser=parser)

    return element


def xml_node(tag, text="", parent_node=None, index=-1, comment=False):
    """
    Description:
        Creates an XML node with the specified tag and optional text.

    Args:
        tag (str): The tag to be assigned to the node (e.g., 'fgdcShortName').
        text (str, optional): The text contents of the node.
        parent_node (lxml.Element, optional): The parent node to which the
            created node will be appended.
        index (int, optional): The positional index to insert the node at
            (zero-based). If not specified, the node will be appended to the
            end.
        comment (bool, optional): If True, create a comment node instead of an
            element node.

    Returns:
        lxml.Element: The created lxml node or comment.
    """

    # Create a comment node if specified, otherwise create a regular element.
    node = etree.Comment() if comment else etree.Element(tag)

    # Set the text content of the node, removing control characters if present.
    if text:
        node.text = u"{}".format(remove_control_characters(text))

    # Append or insert the created node to the parent node if provided.
    if parent_node is not None:
        if index == -1:
            # Append the node to the end of the parent's children.
            parent_node.append(node)
        else:
            # Insert the node at the specified index.
            parent_node.insert(index, node)

    return node


def load_xslt(fname):
    """
    Description:
        Loads an XSLT stylesheet from the specified file.

    Args:
        fname (str): The full path to the XSLT file to be loaded.

    Returns:
        lxml.XSLT: The loaded XSLT object.
    """

    # Load the XSLT file and convert it to an lxml node object.
    return etree.XSLT(fname_to_node(fname))


def load_schema(fname):
    """
    Description:
        Loads an XML schema from the specified file.

    Args:
        fname (str): The full path to the XML schema file to be loaded.

    Returns:
        lxml.XMLSchema: The loaded XML schema object.
    """

    # Load the schema file and convert it to an lxml node object.
    return etree.XMLSchema(fname_to_node(fname))


def clear_children(element):
    """
    Description:
        Removes all child elements from the given lxml element.

    Args:
        element (lxml.Element): The lxml element from which to remove all child
            elements.

    Returns:
        None
    """

    # Iterate over a list of child elements and remove each one.
    for child in element.getchildren():
        element.remove(child)


class XMLRecord(object):
    def __init__(self, contents):
        """
        Initializes the XMLRecord with provided contents.

        Contents must be one of the following:
            1) File path/name on the local filesystem that exists and can be
                read.
            2) String containing an XML Record.
            3) URL containing an XML record.

        Args:
            contents (str or lxml.Element): URL, file path, or XML string
                snippet.
        """

        try:
            contents_path = Path(contents)

            # Check if the path exists.
            try:
                exists = contents_path.exists()
            except (OSError, ValueError):
                exists = False

            if exists:
                # Process as a file path.
                self.fname = str(contents_path.absolute())
                self.record = etree.parse(self.fname)
                self._root = self.record.getroot()
            else:
                # Validate and retrieve content from the URL.
                try:
                    if utils.url_validator(contents):
                        contents = utils.requests_pem_get(contents).text
                except Exception:
                    pass

                self.fname = None

                # Strip BOM if present.
                if contents.startswith("ï»¿"):
                    contents = contents[3:]

                if isinstance(contents, str):
                    # Convert string contents to bytes.
                    contents = contents.encode("utf-8")

                self._root = string_to_node(contents)  # Convert string to node
                self.record = etree.ElementTree(self._root)

        except etree.XMLSyntaxError:
            # Handle invalid XML content.
            self.fname = None
            self.record = etree.fromstring(contents)
            self._root = self.record.getroot()

        self.tag = self._root.tag
        # Create an XMLNode from the root element.
        self.__dict__[self._root.tag] = XMLNode(self.record.getroot())
        self._contents = self.__dict__[self._root.tag]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__[self.tag].__str__()

    def serialize(self):
        """Serializes the XML node to a string representation."""
        return self.__str__()

    def save(self, fname=""):
        """
        Description:
            Saves the XML content to the specified file name. If no file name
            is provided, defaults to the original file name.

        Args:
            fname (str): The full path to the XML schema file to be loaded.

        Returns:
            None
        """

        if not fname:
            fname = self.fname
        save_to_file(self._contents.to_xml(), fname)

    def validate(self, schema="fgdc", as_dataframe=True):
        """
        Description:
            Validates the XML content against a specified schema.

        Args:
            schema (str, optional):
                Can be one of:
                    'fgdc' - uses the standard FGDC schema.
                    'bdp' - uses the Biological Data Profile schema.
                    Full file path to another local schema.
                Defaults to 'fgdc'.
            as_dataframe (bool): Specifies return format (list of tuples or
                DataFrame).

        Returns:
            list of tuples or pandas DataFrame (xpath, error message,
                line number)
        """

        return fgdc_utils.validate_xml(
            self._contents.to_xml(),
            xsl_fname=schema,
            as_dataframe=as_dataframe
        )


class XMLNode(object):
    """
    Class used to dynamically create an object containing the contents of an
    XML node, along with functions for manipulating and introspecting it.
    """

    def __init__(self, element=None, tag="", text="", parent_node=None,
                 index=-1):
        """
        Description:
            Initializes the XMLNode with provided parameters.

        Args:
            element (lxml.Element, optional): The XML element to initialize
                from.
            tag (str, optional): The string to use for the element tag.
            text (str): The text contents of the element.
            parent_node (XMLNode, optional): If provided, add this XMLNode to
                the parent node.
            index (int, optional): If provided, insert this XMLNode into the
                parent node at this position.
        """

        self.text = text
        self.tag = tag
        self.children = []

        # Initialize based on element or tag/text.
        if isinstance(element, etree._Element):
            self.from_xml(element)
        elif tag:
            element = xml_node(tag=tag, text=text)
            self.from_xml(element)
        elif type(element) == str:
            self.from_str(element)

        # Add this node to the parent node if provided.
        if parent_node is not None:
            parent_node.add_child(self, index=index, deepcopy=False)

    def __repr__(self):
        """Return a string representation of this object."""

        return self.__str__()

    def __str__(self, level=0):
        """
        Description:
            Pretty print the XMLNode contents.

        Args:
            level (int): Number of spaces to indent for pretty printing.

        Returns:
            str: Pretty string representation of this element.
        """

        if self.text:
            cur_node = xml_node(self.tag, self.text)
            result = "{}{}".format(
                "  " * level, lxml.tostring(cur_node,
                                            pretty_print=True).decode()
            )
            result = result.rstrip()
        else:
            result = "{}<{}>".format("  " * level, self.tag, self.tag)
            for child in self.children:
                if type(self.__dict__[child.tag]) == XMLNode:
                    child = self.__dict__[child.tag]
                result += "\n" + child.__str__(level=level + 1)
            result += "\n{}</{}>".format("  " * level, self.tag)

        return result

    def __eq__(self, other):
        """
        Description:
            Compare this XMLNode with another for equality.

        Args:
            other (XMLNode): The XMLNode to compare with.

        Returns:
            bool: True if equal, False otherwise.
        """

        if isinstance(other, self.__class__):
            return self.to_str() == other.to_str()

        return False

    def from_xml(self, element):
        """
        Description:
            Populate this XMLNode from an lxml.Element.

        Args:
            element (lxml.Element): The XML element to parse and initialize
                from.

        Returns:
            None
        """

        # Store the provided lxml.Element in the instance variable.
        self.element = element

        # Get the tag name from the element and assign it to the instance.
        self.tag = element.tag

        # Add this XMLNode to the attributes of the class using its tag.
        self.add_attr(self.tag, self)

        # Attempt to extract and clean the text from the element.
        try:
            self.text = element.text.strip()
        except:
            self.text = ""

        # Initialize an empty list to hold child XMLNodes.
        self.children = []

        # Iterate over all child elements of the current element.
        for child_node in self.element.getchildren():
            # Create an XMLNode from the current child element.
            child_object = XMLNode(child_node)

            # Append the newly created child XMLNode to the children list.
            self.children.append(child_object)

            # Add the child XMLNode to the attributes of this node using its
            # tag.
            self.add_attr(child_node.tag, child_object)

    def add_attr(self, tag, child_object):
        """
        Description:
            Add a child XMLNode to this object's attributes.

        Args:
            tag (str): The tag of the XMLNode.
            child_object (XMLNode): The XMLNode to add to this object.

        Returns:
            None
        """

        # Check if the tag already exists in the object's attributes.
        if tag in self.__dict__:
            # Fetch the current contents associated with the tag
            cur_contents = self.__dict__[tag]

            # If the current contents are already a list, append the new child.
            if isinstance(cur_contents, list):
                cur_contents.append(child_object)
            else:
                # If it is not a list, convert the current contents into a list
                # and add the new child XMLNode.
                self.__dict__[tag] = [cur_contents, child_object]
        else:
            # If the tag does not exist, directly add the new child object.
            self.__dict__[tag] = child_object

    def to_xml(self):
        """
        Description:
            Return lxml element version of this XMLNode.

        Returns:
            lxml.Element
        """

        # Convert the current XMLNode representation to a string.
        str_element = self.to_str()

        # Parse the string representation back into an lxml.Element.
        element = string_to_node(str_element)

        return element

    def from_str(self, str_element):
        """
        Description:
            Populate this XMLNode from a string representation.

        Args:
            str_element (str): XML element serialized as a string.

        Returns:
            None
        """

        # Create an XML parser with options to clean namespaces and recover
        # from errors.
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")

        # Parse the string representation of the XML element into an
        # lxml.Element.
        element = lxml.fromstring(str_element, parser=parser)

        # Populate this XMLNode using the parsed lxml.Element.
        self.from_xml(element)

    def to_str(self):
        """
        Description:
            Return a string representation of this XMLNode.

        Returns:
            str
        """

        return self.__str__()

    def search_xpath(self, xpath=""):
        """
        Description:
            Search for matching elements by parsing an XPath expression.

        Args:
            xpath (str): The XPath expression to search for.

        Returns:
            list: A list of matching elements or the first matching element.
        """

        # If no XPath expression is provided, return the current node.
        if not xpath:
            return self

        # Split the XPath expression into individual components.
        xpath_items = xpath.split("/")

        # Determine the remainder of the XPath expression after the first item.
        if len(xpath_items) == 1:
            xpath_remainder = ""  # No more items to process
        else:
            xpath_remainder = "/".join(xpath_items[1:])  # Join remaining items

        # Get the first item from the XPath expression.
        first_item = xpath_items[0]

        try:
            # Split the first XPath item into tag and index (if present).
            tag, index = split_tag(first_item)

            # Retrieve the matching results from the current object's
            # attributes.
            results = self.__dict__[tag]

            # If the first item contains an index, navigate to the specified
            # child.
            if "[" in first_item:
                first_result = results[index]  # Get the indexed child
                return first_result.search_xpath(
                    xpath_remainder)  # Recurse further

            # If the first item does not contain an index.
            else:
                # If the results are a list, aggregate results from each child
                if isinstance(results, list):
                    aggregator = []  # Prepare an empty list to collect matches
                    for result in results:
                        # Recursively search each child for the remaining XPath.
                        node = result.search_xpath(xpath_remainder)
                        if node is not None:
                            aggregator.append(node)  # Collect matching nodes
                    return aggregator  # Return all collected matches

                # If there is only one result, recursively search it.
                else:
                    return results.search_xpath(xpath_remainder)

        # If any errors occur during the search or navigation, return an empty
        # list.
        except:
            return []

    def xpath(self, xpath="", as_list=True, as_text=False):
        """
        Description:
            Convenience function for calling XPath searches.

        Args:
            xpath (str): The XPath to search.
            as_list (bool): Whether to return results as a list.
            as_text (bool): Whether to return the text of the first matching
                element.

        Returns:
            XMLNode, list of XMLNodes, or str
        """

        # Perform the XPath search using the provided XPath expression.
        results = self.search_xpath(xpath)

        # If results should be returned as a list and the result is not already
        # a list.
        if as_list and not isinstance(results, list):
            results = [results]  # Convert single result to a list

        # If as_text is True, extract the text from each matching XMLNode.
        if as_text:
            results = [r.text for r in results if
                       r]  # Filter out any None results

        # Return the final results, which can be an XMLNode, list of XMLNodes,
        # or str.
        return results

    def xpath_march(self, xpath, as_list=True):
        """
        Description:
            Iteratively search for the most distant matching element.

        Args:
            xpath (str): The XPath to search.
            as_list (bool): Whether to return as a list.

        Returns:
            list
        """

        # Split the provided XPath into its individual components.
        xpath_items = xpath.split("/")

        # Continue searching while there are still XPath components left.
        while xpath_items:
            # Join the current components to form the current XPath query.
            result = self.xpath("/".join(xpath_items), as_list=as_list)

            # If a match is found, return the matched result.
            if result:
                return result

            # Remove the last component of the XPath and try again.
            xpath_items.pop()

        # If no matches were found after iterating through all components,
        # return an empty list.
        return []

    def clear_children(self, tag=None):
        """
        Description:
            Remove children from this node.

        Args:
            tag (str, optional): The tag to look for and remove. Non-matching
                tags will be kept.

        Returns:
            None
        """

        # If a specific tag is provided.
        if tag is not None:
            # Filter the children list to keep only those children whose tag
            # does not match the specified tag.
            self.children = [c for c in self.children if c.tag != tag]
        else:
            # If no tag is specified, clear all children from this node.
            self.children = []

    def replace_child(self, new_child, tag=None, deepcopy=True):
        """
        Description:
            Replace a given child node.

        Args:
            tag (str, optional): The child node tag to replace.
            new_child (XMLNode): The child to swap into this object.
            deepcopy (bool): Whether to use the exact child object passed or a
                copy of it.

        Returns:
            None
        """

        # If no specific tag is provided, use the tag of the new child.
        if tag is None:
            tag = new_child.tag

        # Iterate over the list of children to find the child with the
        # specified tag.
        for i, child in enumerate(self.children):
            # Check if the current child's tag matches the specified tag.
            if child.tag == tag:
                # Remove the matched child from the children list.
                del self.children[i]

                # Add the new child in place of the removed child.
                self.add_child(new_child, i, deepcopy=deepcopy)

                # Exit loop after the replacement is done.
                break

    def find_string(self, string, ignorecase=False):
        """
        Description:
            Find all nodes containing a specific string.

        Args:
            string (str): The string to search for in the node text.
            ignorecase (bool): Flag to ignore case when searching.

        Returns:
            list: All XMLNodes with text elements containing the string.
        """

        # Initialize an empty list to collect found nodes.
        found = []

        # Check if the string is found in the current node's text, considering
        # case sensitivity.
        if ignorecase and string.lower() in self.text.lower():
            # Add current node if the string is found (case ignored).
            found.append(self)
        elif string in self.text:
            # Add current node if the string is found (case sensitive).
            found.append(self)

        # Recursively search in all child nodes
        for child in self.children:
            # Extend the found list with results from the child's search.
            found += child.find_string(string, ignorecase)

        # Return the list of all found XMLNodes.
        return found

    def replace_string(self, old, new, maxreplace=None, deep=True):
        """
        Replace occurrences of a string in the node text.

        Args:
            old (str): The string to find.
            new (str): The string to replace 'old' with.
            maxreplace (int, optional): Limit the number of replacements.
            deep (bool): Whether to apply replacement on all child nodes
                recursively.

        Returns:
            int: The number of occurrences found.
        """

        # Count the occurrences of the old string in the current node's text.
        count_found = self.text.count(old)

        # If no maximum limit is provided, replace all occurrences of the old
        # string.
        if maxreplace is None:
            self.text = self.text.replace(old, new)
        else:
            # Limit the number of replacements if count exceeds maxreplace.
            if count_found > maxreplace:
                count_found = maxreplace  # cap the count to maxreplace

            # Replace up to the maximum specified occurrences.
            self.text = self.text.replace(old, new, maxreplace)

        # If deep replacement is requested, apply it to all child nodes
        # recursively.
        if deep:
            for child in self.children:
                # Recursively replace strings in each child and accumulate the
                # count.
                count_found += child.replace_string(old, new, maxreplace, deep)

        # Return the total number of occurrences found and replaced.
        return count_found

    def add_child(self, child, index=-1, deepcopy=True):
        """
        Add a child element to this XMLNode.

        Args:
            child (XMLNode): The child element to be added.
            index (int, optional): The position to add the child element at.
            deepcopy (bool): Whether to use the exact child object or a copy of
                it.

        Returns:
            None
        """

        # If no index is provided, append the child at the end of the children
        # list.
        if index == -1:
            index = len(self.children)

        # Convert the child element to its string representation. Check if the
        # child is an lxml Element; if so, convert it accordingly.
        if isinstance(child, etree._Element):
            node_str = node_to_string(child, encoding=False)
        else:
            # Assume child is an XMLNode and convert it.
            node_str = child.to_str()

        # Create a new XMLNode from the string representation of the child.
        child_copy = XMLNode(node_str)

        # Insert the child copy or the original child based on deepcopy flag.
        if deepcopy:
            # If deepcopy is True, insert the copied child.
            self.children.insert(index, child_copy)
        else:
            # If deepcopy is False, insert the original child.
            self.children.insert(index, child)

        # Add the child as an attribute of the current node, indexed by its tag.
        self.add_attr(child.tag, child)


    def copy(self):
        """
        Description:
            Return a deep copy of this XMLNode.

        Returns:
            XMLNode
        """

        # Convert the current XMLNode to its string representation.
        node_str = self.to_str()

        # Create a new XMLNode using the string representation to ensure a deep
        # copy.
        self_copy = XMLNode(node_str)

        return self_copy


def split_tag(tag):
    """
    Description:
        Parses an XML tag to separate the tag name and its index.

    Args:
        tag (str): An XML tag that may include an index in the format [n].

    Returns:
        tuple: A tuple containing the tag name (str) and the index (int).
            The index is zero-based.
    """

    # Check if there's an index specified in the tag.
    if "[" in tag:
        # Split the tag and extract the index
        fgdc_tag, tag = tag.split("[")
        index = int(tag.split("]")[0]) - 1  # Convert to zero-based index
    else:
        fgdc_tag = tag  # If no index, use the full tag
        index = 0  # Default index is 0

    return fgdc_tag, index
