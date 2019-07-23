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
Module contains utility functions for interacting with XML FGDC records


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

import json
from dateutil import parser

import defusedxml.lxml as lxml

import pandas as pd

from pymdwizard.core import xml_utils
from pymdwizard.core import utils

from collections import OrderedDict

FGDC_XSD_NAME = "FGDC/fgdc-std-001-1998-annotated.xsd"
BDP_XSD_NAME = "FGDC/BDPfgdc-std-001-1998-annotated.xsd"


def validate_xml(xml, xsl_fname="fgdc", as_dataframe=False):
    """

    Parameters
    ----------
    xml : lxml document
                or
          filename
                or
          string containing xml representation

    xsl_fname : str (optional)
                can be one of:
                'fgdc' - uses the standard fgdc schema
                        ../resources/FGDC/fgdc-std-001-1998-annotated.xsd
                'bdp' = use the Biological Data profile schema,
                        ../resources/FGDC/BDPfgdc-std-001-1998-annotated.xsd
                full file path to another local schema.

                if not specified defaults to 'fgdc'
    as_dataframe : bool
                used to specify return format (list of tuples or dataframe)

    Returns
    -------
        list of tuples
        (xpath, error message, line number)
        or
        pandas dataframe
    """

    if xsl_fname.lower() == "fgdc":
        xsl_fname = utils.get_resource_path(FGDC_XSD_NAME)
    elif xsl_fname.lower() == "bdp":
        xsl_fname = utils.get_resource_path(BDP_XSD_NAME)
    else:
        xsl_fname = xsl_fname

    xmlschema = xml_utils.load_schema(xsl_fname)
    xml_doc = xml_utils.xml_document_loader(xml)
    xml_str = xml_utils.node_to_string(xml_doc)

    tree_node = xml_utils.string_to_node(xml_str.encode("utf-8"))
    lxml._etree._ElementTree(tree_node)

    errors = []
    srcciteas = []

    src_xpath = "dataqual/lineage/srcinfo/srccitea"
    src_nodes = tree_node.xpath(src_xpath)
    for i, src in enumerate(src_nodes):
        srcciteas.append(src.text)
        if src.text is None:
            if len(src_nodes) == 1:
                errors.append(
                    (
                        "metadata/" + src_xpath,
                        "source citation abbreviation cannot be empty",
                        1,
                    )
                )
            else:
                xpath = "metadata/dataqual/lineage/srcinfo[{}]/srccitea"
                errors.append(
                    (
                        xpath.format(i + 1),
                        "source citation abbreviation cannot be empty",
                        1,
                    )
                )
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
                    (
                        "metadata/" + error_xpath,
                        "source produced abbreviation cannot be empty",
                        1,
                    )
                )

    srcused_xpath = "dataqual/lineage/procstep/srcused"
    srcused_nodes = tree_node.xpath(srcused_xpath)
    for i, src in enumerate(srcused_nodes):
        if src.text not in srcciteas:
            if len(srcused_nodes) == 1:
                errors.append(
                    (
                        "metadata/" + srcused_xpath,
                        "Source Used Citation Abbreviation {} "
                        "not found in Source inputs "
                        "used".format(src.text),
                        1,
                    )
                )
            else:
                xpath = "metadata/dataqual/lineage/procstep[{}]/srcused"
                errors.append(
                    (
                        xpath.format(i + 1),
                        "Source Used Citation Abbreviation {} "
                        "not found in Source inputs "
                        "used".format(src.text),
                        1,
                    )
                )

    if xmlschema.validate(tree_node) and not errors:
        return []

    line_lookup = dict(
        [
            (e.sourceline, tree_node.getroottree().getpath(e))
            for e in tree_node.xpath(".//*")
        ]
    )
    sourceline = tree_node.sourceline
    line_lookup[sourceline] = tree_node.getroottree().getpath(tree_node)

    fgdc_lookup = get_fgdc_lookup()

    for error in xmlschema.error_log:
        error_msg = clean_error_message(error.message, fgdc_lookup)
        try:
            errors.append((line_lookup[error.line][1:], error_msg, error.line))
        except KeyError:
            errors.append(("Unknown", error_msg, error.line))

    errors = list(OrderedDict.fromkeys(errors))

    if as_dataframe:
        cols = ["xpath", "message", "line number"]
        return pd.DataFrame.from_records(errors, columns=cols)
    else:
        return errors


def get_fgdc_lookup():
    """
    Loads the local resource, 'bdp_lookup' into a json object

    Returns
    -------
        json fgdc item lookup
    """
    annotation_lookup_fname = utils.get_resource_path("FGDC/bdp_lookup")
    try:
        with open(annotation_lookup_fname, encoding="utf-8") as data_file:
            annotation_lookup = json.loads(data_file.read())
    except TypeError:
        with open(annotation_lookup_fname) as data_file:
            annotation_lookup = json.loads(data_file.read())

    return annotation_lookup


def clean_error_message(message, fgdc_lookup=None):
    """
    Returns a cleaned up, more informative translation
    of a raw xml schema error message.
    Empty or missing elements are described in plain English

    Parameters
    ----------
    message : str
              The raw message we will be cleaning up

    Returns
    -------
        str : cleaned up error message
    """
    parts = message.split()
    if "Missing child element" in message:
        clean_message = "The {} is missing the expected element(s) '{}'"
        clean_message.format(parts[1][:-1], parts[-2])
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
    Convert a Python date object into an FGDC string format YYYYMMDD

    Parameters
    ----------
    date_input : str or datetime
            if str provided must be in format that dateutil's parser can handle
    Returns
    -------
        str : date formated in FGDC YYYYMMDD format
    """

    if type(date_input) == str:
        date_input = parser.parse(date_input)

    return date_input.strftime("%Y%m%d")
