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
Module contains functions for retrieving information about a DOI
from Datacite and Crossref
Returns information in an FGDC citeinfo xml format


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
from urllib.parse import urlparse

try:
    from habanero import cn
except ImportError:
    habanero = None

from pymdwizard.core.xml_utils import XMLNode
from pymdwizard.core import utils


def clean_doi(doi):
    """
    Cleans doi to match expected string format.
    Removes leading 'https://'  and 'doi.org/' from the string

    Parameters
    ----------
    doi : str
        A string containing a DOI

    Returns
    -------
        DOI string with extraneous characters removed
    """
    if doi.startswith("https://doi.org/"):
        return doi.replace("https://doi.org/", "")
    elif doi.startswith("doi.org/"):
        return doi.replace("doi.org/", "")
    elif doi.startswith("http://dx.doi.org"):
        return doi.replace("http://dx.doi.org/", "")
    elif doi.startswith("doi: "):
        return doi.replace("doi: ", "")
    elif doi.startswith("doi:"):
        return doi.replace("doi:", "")
    else:
        return doi


def get_doi_citation_crossref(doi):
    """
    get

    Parameters
    ----------
    doi : str
        DOI in the format "https://doi.org/10.1109/5.771073"
                    or    "doi:10.5066/F70R9MFW"
                    or    "http://dx.doi.org/10.1109/5.771073"

    Returns
    -------
        dict with publication information pulled from crossref site
    """

    cite_data = json.loads(cn.content_negotiation(ids=doi,
                                                  format="citeproc-json"))

    cite_data["geoform"] = "publication"
    if "publisher-location" in cite_data:
        cite_data["pubplace"] = cite_data["publisher-location"]
    else:
        cite_data["pubplace"] = "n/a"

    return cite_data


def get_doi_citation_datacite(doi):
    """

    Parameters
    ----------
    doi : str
        DOI in the format "https://doi.org/10.1109/5.771073"
                    or    "doi:10.5066/F70R9MFW"
                    or    "http://dx.doi.org/10.1109/5.771073"

    Returns
    -------
        dict with information pulled from datacite site
    """
    endpoint = "https://api.datacite.org/works"
    response = utils.requests_pem_get(endpoint + "/" + doi)
    cite_data = json.loads(response.text)["data"]["attributes"]

    if "container-title" not in cite_data:
        cite_data["container-title"] = cite_data.pop("container_title")
    if "data-center-id" not in cite_data:
        cite_data["data-center-id"] = cite_data.pop("data_center_id")

    cite_data["publisher"] = cite_data["container-title"]
    cite_data["URL"] = "https://doi.org/{}".format(cite_data["doi"])
    if "data-center-id" in cite_data and "usgs" in cite_data["data-center-id"]:
        cite_data["container-title"] = None
        cite_data["pubplace"] = "n/a"
        cite_data["geoform"] = "dataset"
    else:
        cite_data["geoform"] = "publication"
        cite_data["pubplace"] = "n/a"
    return cite_data


def get_doi_citation(doi):
    """

    Parameters
    ----------
    doi : str
        DOI in the format "https://doi.org/10.1109/5.771073"
                    or    "doi:10.5066/F70R9MFW"
                    or    "http://dx.doi.org/10.1109/5.771073"

    Returns
    -------
        xml node with citation information in FGDC schema, citeinfo format.
            or
        None if the DOI cannot be retrieved
    """

    doi = clean_doi(doi)
    try:
        cite_data = get_doi_citation_crossref(doi)
    except:
        try:
            cite_data = get_doi_citation_datacite(doi)
        except:
            return None

    citeinfo = XMLNode(tag="citeinfo")
    if "author" in cite_data:
        for author in cite_data["author"]:
            if "literal" not in author:
                author["literal"] = author["given"] + " " + author["family"]
            origin = XMLNode(tag="origin", parent_node=citeinfo, text=author["literal"])
    else:
        origin = XMLNode(tag="origin", parent_node=citeinfo, text="")

    pubdate_parts = None
    if "published-online" in cite_data:
        pubdate_parts = cite_data["published-online"]["date-parts"][0]
    elif "published-print" in cite_data:
        pubdate_parts = cite_data["published-print"]["date-parts"][0]
    elif "published" in cite_data:
        pubdate_parts = [cite_data["published"]]

    if pubdate_parts:
        pubdate_str = \
            "".join(["{:02d}".format(int(part)) for part in pubdate_parts])

    # Handle different publication dates in attempt to define a
    # complete YYYYMMDD for journals that are not including day.
    if len(pubdate_str) == 6:
        has_license = "license" in cite_data and cite_data["license"]
        if has_license:
            try:
                pubdate_parts = \
                    cite_data.get("license")[0].get("start").get("date-parts")[0]
                pubdate_str = "".join(
                    ["{:02d}".format(int(part)) for part in pubdate_parts])
            except AttributeError:
                pass

    # Handle different publication dates in attempt to define a
    # complete YYYYMMDD for USGS publications.
    if len(pubdate_str) == 4:
        has_created = \
            "created" in cite_data and cite_data["created"]["date-parts"]
        has_registered = \
            "registered" in cite_data and cite_data["registered"]
        if has_created:
            try:
                # USGS Series.
                pubdate_parts = cite_data.get("created").get("date-parts")[0]
                pubdate_str = "".join(
                    ["{:02d}".format(int(part)) for part in pubdate_parts])
            except AttributeError:
                pass
        if has_registered:
            try:
                # USGS data/software.
                pubdate_parts = cite_data.get("registered")
                pubdate_parts = pubdate_parts[:10].split("-")
                pubdate_str = "".join(
                    ["{:02d}".format(int(part)) for part in pubdate_parts])
            except AttributeError:
                pass

    pubdate = XMLNode(tag="pubdate", parent_node=citeinfo, text=pubdate_str)

    # USGS data/software products (pubplace and geoform).
    # Version--Edition unfortunately not tracked in data/software DOI.
    has_usgs_prod = \
        "data-center-id" in cite_data and cite_data["data-center-id"]
    if has_usgs_prod:
        data_cntr_id = cite_data["data-center-id"]
        data_type = cite_data["resource-type-subtype"]
        if data_cntr_id == "usgs.prod":
            try:
                usgs_url = cite_data["url"]
                parsed_url = urlparse(usgs_url)
                cite_data["pubplace"] = \
                    parsed_url.scheme + "://" + parsed_url.netloc
            except AttributeError:
                cite_data["pubplace"] = "UNKNOWN"

            if data_type == "Dataset":
                # User may want to change to vector, raster, etc.
                cite_data["geoform"] = data_type
            elif data_type == "Software":
                cite_data["geoform"] = "application/service"

    # USGS Series (pubplace, volume/issue)
    try:
        has_container = "container-title" in cite_data and cite_data[
            "container-title"]
        has_url = "URL" in cite_data and cite_data["URL"]
        has_altid = \
            "alternative-id" in cite_data and cite_data["alternative-id"]

        if has_container and has_url and has_altid:
            try:
                url_ref = cite_data.get("resource").get("primary").get("URL")

                if "https://pubs.usgs.gov/" in url_ref:
                    try:
                        # Series name; set below
                        series_name = cite_data["container-title"]
                    except AttributeError:
                        series_name = "ERROR"
                    try:
                        # DOI--Not using
                        url_doi = cite_data["URL"]
                    except AttributeError:
                        url_doi = "ERROR"
                    try:
                        # Pub place.
                        url_ref = \
                            cite_data.get("resource").get("primary").get("URL")
                        if "https://pubs.usgs.gov/" in url_ref:
                            cite_data["pubplace"] = "https://pubs.usgs.gov"
                        else:
                            cite_data["pubplace"] = url_ref
                    except AttributeError:
                        cite_data["pubplace"] = "ERROR"
                    try:
                        # USGS series volume/issue
                        altid = cite_data["alternative-id"][0]
                        cite_data["volume"] = altid
                    except AttributeError:
                        cite_data["volume"] = "ERROR"
            except AttributeError:
                pass
    except AttributeError:
        pass

    title = XMLNode(tag="title", parent_node=citeinfo, text=cite_data["title"])
    geoform = XMLNode(tag="geoform", parent_node=citeinfo, text=cite_data["geoform"])

    has_container = "container-title" in cite_data and cite_data["container-title"]
    has_volume = "volume" in cite_data and cite_data["volume"]
    has_issue = "issue" in cite_data and cite_data["issue"]

    if has_container and (has_volume or has_issue):
        serinfo = XMLNode(tag="serinfo", parent_node=citeinfo)
        sername = XMLNode(
            tag="sername",
            parent_node=citeinfo.serinfo,
            text=cite_data["container-title"],
        )

        if "volume" in cite_data and "issue" in cite_data:
            issue_str = "vol." + " " + str(cite_data["volume"]) + ", issue "
            issue_str += cite_data["issue"]
            issue = XMLNode(tag="issue", parent_node=citeinfo.serinfo, text=issue_str)
        elif "volume" in cite_data:
            issue_str = "vol." + " " + str(cite_data["volume"])
            XMLNode(tag="issue", parent_node=citeinfo.serinfo, text=issue_str)
        elif "issue" in cite_data:
            issue_str = "issue " + cite_data["issue"]
            XMLNode(tag="issue", parent_node=citeinfo.serinfo, text=issue_str)

    XMLNode(tag="pubinfo", parent_node=citeinfo)
    XMLNode(tag="pubplace", parent_node=citeinfo.pubinfo, text=cite_data["pubplace"])
    XMLNode(tag="publish", parent_node=citeinfo.pubinfo, text=cite_data["publisher"])

    if "page" in cite_data:
        othercit_str = "ppg. " + cite_data["page"]
        XMLNode(tag="othercit", parent_node=citeinfo, text=othercit_str)

    XMLNode(
        tag="onlink",
        parent_node=citeinfo,
        text=cite_data["URL"].replace("http://dx.doi.org", "https://doi.org"),
    )

    return citeinfo
