#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module contains utility functions for interacting with XML FGDC records


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import json
from dateutil import parser
from collections import OrderedDict

# Non-standard python libraries.
try:
    import defusedxml.lxml as lxml
    import pandas as pd
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (xml_utils, utils)
except ImportError as err:
    raise ImportError(err, __file__)

# Global variables defining XML Schema Definition file for metadata standards.
FGDC_XSD_NAME = "FGDC/fgdc-std-001-1998-annotated.xsd"
BDP_XSD_NAME = "FGDC/BDPfgdc-std-001-1998-annotated.xsd"


def validate_xml(xml, xsl_fname="fgdc", as_dataframe=False):
    """
    Description:
        Validates an XML document against a specified XML schema.

    Args:
        xml (lxml document, filename, or string): containing XML representation.
        xsl_fname (str, optional): Can be one of:
            - 'fgdc': Uses standard FGDC schema
            - 'bdp': Uses Biological Data Profile schema
            - Full file path to another local schema.
            Defaults to 'fgdc'.
        as_dataframe (bool): Specifies return format (list of tuples or
            DataFrame).

    Returns:
        list of tuples or pandas DataFrame
            Each tuple contains (xpath, error message, line number)
            or the results in DataFrame format.
    """

    # Map schema name to resource path.
    if xsl_fname.lower() == "fgdc":
        xsl_fname = utils.get_resource_path(FGDC_XSD_NAME)
    elif xsl_fname.lower() == "bdp":
        xsl_fname = utils.get_resource_path(BDP_XSD_NAME)
    else:
        xsl_fname = xsl_fname

    # Load schema and XML document.
    xmlschema = xml_utils.load_schema(xsl_fname)
    xml_doc = xml_utils.xml_document_loader(xml)
    xml_str = xml_utils.node_to_string(xml_doc)

    # Create a tree node from the XML string.
    tree_node = xml_utils.string_to_node(xml_str.encode("utf-8"))
    lxml._etree._ElementTree(tree_node)

    # Initiate list objects to store results.
    errors = []
    srcciteas = []

    # Validate source citation abbreviations.
    src_xpath = "dataqual/lineage/srcinfo/srccitea"
    src_nodes = tree_node.xpath(src_xpath)
    for i, src in enumerate(src_nodes):
        srcciteas.append(src.text)
        if src.text is None:
            if len(src_nodes) == 1:
                errors.append(
                    ("metadata/" + src_xpath,
                     "source citation abbreviation cannot be empty",
                     1,
                    )
                )
            else:
                xpath = "metadata/dataqual/lineage/srcinfo[{}]/srccitea"
                errors.append(
                    (xpath.format(i + 1),
                     "source citation abbreviation cannot be empty",
                     1,
                    )
                )

    # Validate source products.
    procstep_xpath = "dataqual/lineage/procstep"
    procstep_nodes = tree_node.xpath(procstep_xpath)
    for proc_i, proc in enumerate(procstep_nodes):
        srcprod_nodes = proc.xpath("srcprod")
        for srcprod_i, srcprod in enumerate(srcprod_nodes):
            srcciteas.append(srcprod.text)
            if srcprod.text is None:
                error_xpath = procstep_xpath
                if len(procstep_nodes) > 1:
                    error_xpath += "[{}]".format(proc_i + 1)
                error_xpath += "/srcprod"
                if len(srcprod_nodes) > 1:
                    error_xpath += "[{}]".format(proc_i + 1)
                errors.append(
                    ("metadata/" + error_xpath,
                     "source produced abbreviation cannot be empty",
                     1,
                    )
                )

    # Validate sources used.
    srcused_xpath = "dataqual/lineage/procstep/srcused"
    srcused_nodes = tree_node.xpath(srcused_xpath)
    for i, src in enumerate(srcused_nodes):
        if src.text not in srcciteas:
            if len(srcused_nodes) == 1:
                errors.append(
                    ("metadata/" + srcused_xpath,
                     "Source Used Citation Abbreviation {} "
                     "not found in Source inputs "
                     "used".format(src.text),
                     1,
                    )
                )
            else:
                xpath = "metadata/dataqual/lineage/procstep[{}]/srcused"
                errors.append(
                    (xpath.format(i + 1),
                     "Source Used Citation Abbreviation {} "
                     "not found in Source inputs "
                     "used".format(src.text),
                     1,
                    )
                )

    # Validate the XML against the schema and errors.
    if xmlschema.validate(tree_node) and not errors:
        return []

    # Line lookup for error messages.
    line_lookup = dict(
        [(e.sourceline, tree_node.getroottree().getpath(e))
         for e in tree_node.xpath(".//*")
        ]
    )
    sourceline = tree_node.sourceline
    line_lookup[sourceline] = tree_node.getroottree().getpath(tree_node)

    fgdc_lookup = get_fgdc_lookup()

    # Collect and clean schema validation errors.
    for error in xmlschema.error_log:
        error_msg = clean_error_message(error.message, fgdc_lookup)
        try:
            errors.append((line_lookup[error.line][1:], error_msg, error.line))
        except KeyError:
            errors.append(("Unknown", error_msg, error.line))

    # Remove duplicate errors while maintaining order.
    errors = list(OrderedDict.fromkeys(errors))

    # Return results based on requested format.
    if as_dataframe:
        cols = ["xpath", "message", "line number"]
        return pd.DataFrame.from_records(errors, columns=cols)
    else:
        return errors


def get_fgdc_lookup():
    """
    Description:
        Loads the local resource 'bdp_lookup' into a JSON object.

    Returns:
        dict: FGDC item lookup as a JSON object.
    """

    # Get the file path for the FGDC 'bdp_lookup' resource.
    annotation_lookup_fname = utils.get_resource_path("FGDC/bdp_lookup")

    # Load the JSON data from the specified file.
    try:
        with open(annotation_lookup_fname, encoding="utf-8") as data_file:
            annotation_lookup = json.loads(data_file.read())
    except TypeError:
        with open(annotation_lookup_fname) as data_file:
            annotation_lookup = json.loads(data_file.read())

    return annotation_lookup


def clean_error_message(message, fgdc_lookup=None):
    """
    Description:
        Returns a cleaned up, more informative translation of
        a raw XML schema error message. Empty or missing elements
        are described in plain English.

    Args:
        message (str): The raw message we will be cleaning up.
        fgdc_lookup ():  ???????????????????????????????????????????????

    Returns:
        str: Cleaned up error message.
    """

    # Split string.
    parts = message.split()

    # Check for missing child element errors.
    if "Missing child element" in message:
        clean_message = "The {} is missing the expected element(s) '{}'"
        clean_message.format(parts[1][:-1], parts[-2])
    # Check for validation pattern errors
    elif (
        r"' is not accepted by the pattern '\s*\S(.|\n|\r)*'" in message
        or "'' is not a valid value of the atomic type" in message
    ):
        shortname = parts[1][:-1].replace("'", "")
        try:
            longname = fgdc_lookup[shortname]["long_name"]
        except (KeyError, TypeError):
            longname = None

        if longname is None:
            name = shortname
        else:
            name = "{} ({})".format(longname, shortname)

        clean_message = "The value for {} cannot be empty"
        clean_message = clean_message.format(name)
    else:
        clean_message = message

    return clean_message


def format_date(date_input):
    """
    Description:
        Convert a Python date object into an FGDC string format YYYYMMDD.

    Args:
        date_input (str or datetime): If str provided, it must be in a format
            that dateutil's parser can handle.

    Returns:
        str: Date formatted in FGDC YYYYMMDD format.
    """

    # Check if the input is a string and parse it to a datetime object.
    if type(date_input) == str:
        date_input = parser.parse(date_input)

    return date_input.strftime("%Y%m%d")


def add_doi(xml_record, doi_url):
    """
    Description:
        Adds a DOI to an existing XML record by replacing the 'onlink' if it
        matches the default or by adding an additional 'onlink'. Also replaces
        or adds a network resource name to the distribution section.

    Args:
        xml_record (xml_utils.XMLRecord): The XML record to which the DOI will
            be added.
        doi_url (str): Digital Object Identifier (DOI) as a URL.

    Returns:
        xml_utils.XMLRecord: The updated XML record.
    """

    # Initialize a flag to track whether the DOI link has been added or updated.
    onlink_added = False
    citeinfo = xml_record.metadata.idinfo.citation.citeinfo

    # Iterate through existing onlink elements.
    for onlink in citeinfo.xpath('onlink'):
        if onlink.text == doi_url:
            onlink_added = True
        elif onlink.text == 'https://doi.org/10.5066/xxxxxxxx':
            onlink.text = doi_url
            onlink_added = True

    # Add a new onlink if it wasn't added or replaced.
    if not onlink_added:
        new_onlink = xml_utils.XMLNode(tag='onlink', text=doi_url)
        if not citeinfo.xpath('lworkcit'):
            citeinfo.add_child(new_onlink)
        else:
            # insert the new onlink before the larger work citation
            citeinfo.add_child(new_onlink, index=-2)

    # Attempt to add or update the network resource in the distribution section.
    try:
        network_resource = xml_record.metadata.distinfo.stdorder.digform. \
            digtopt.onlinopt.computer.networka.networkr
        network_resource.text = doi_url
    except AttributeError:
        # Create the structure if it doesn't exist
        stdorder_str = (
            "<stdorder><digform><digtinfo>"
            "<formname>Digital Data</formname></digtinfo>"
            "<digtopt><onlinopt><computer>"
            "<networka><networkr></networkr></networka>"
            "</computer></onlinopt></digtopt></digform>"
            "<fees>None</fees></stdorder>"
        )
        stdorder_node = xml_utils.XMLNode(
            stdorder_str, parent_node=xml_record.metadata.distinfo)
        stdorder_node.digform.digtopt.onlinopt.computer.networka.networkr. \
            text = doi_url

    return xml_record
