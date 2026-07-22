#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

PURPOSE
------------------------------------------------------------------------------
Module for looking up USGS controlled vocabulary (thesaurus) names and
terms via the USGS Thesaurus web service. Shared by the ThesaurusSearch GUI
dialog and by core FGDC validation (fgdc_utils.validate_xml), which is why
this logic lives in pymdwizard.core rather than pymdwizard.gui -- core
modules must not depend on PyQt5.


NOTES
------------------------------------------------------------------------------
Details: https://apps.usgs.gov/thesaurus/service-thesaurus.html
"""

# Standard python libraries.
from urllib.parse import quote

# Custom import/libraries.
try:
    from pymdwizard.core import utils
except ImportError as err:
    raise ImportError(err, __file__)

# Base URL for the USGS Thesaurus web service.
THESAURUS_BASE_URL = "https://apps.usgs.gov/thesaurus/"

# Thesaurus names that indicate free text rather than a controlled vocabulary.
FREE_TEXT_THESAURI = {"none"}


def is_free_text(thesaurus_name):
    """
    Description:
        Determines whether a thesaurus name represents free text (no
        controlled vocabulary) rather than a reference to a registered
        thesaurus.

    Args:
        thesaurus_name (str): The contents of a <themekt> or <placekt>
            element.

    Returns:
        bool: True if the name is empty or "None" (case-insensitive),
            False otherwise.
    """

    if thesaurus_name is None:
        return True

    return thesaurus_name.strip().lower() in FREE_TEXT_THESAURI


def get_thesauri_lookup():
    """
    Description:
        Fetches the list of all available thesauri from the USGS Thesaurus
        web service.

    Args:
        None

    Returns:
        dict or None: A mapping of thesaurus name (str) to thesaurus code
            (int), or None if the service could not be reached.
    """

    url = THESAURUS_BASE_URL + "thesaurus.php?format=json"

    try:
        result = utils.requests_pem_get(url).json()
    except Exception:
        return None

    try:
        return {i["name"]: i["thcode"] for i in result["vocabulary"]}
    except (KeyError, TypeError):
        return None


def _term_is_known(thcode, keyword):
    """
    Description:
        Checks whether a single keyword is a preferred or non-preferred
        term in the given thesaurus, using the same exact-match term
        lookup endpoint as ThesaurusSearch.show_details().

    Args:
        thcode (int or str): The thesaurus code to check against.
        keyword (str): The term to look up.

    Returns:
        bool or None: True if the term (or a non-preferred alias of it)
            is recognized by the thesaurus, False if it is not, or None
            if the lookup could not be completed (e.g. the service is
            unreachable).
    """

    url = THESAURUS_BASE_URL + "term.php?thcode={}&text={}"
    url = url.format(thcode, quote(keyword))

    try:
        details = utils.requests_pem_get(url).json()
    except Exception:
        return None

    if not details:
        return False

    if isinstance(details, dict):
        details = [details]

    keyword_lower = keyword.lower()
    try:
        for detail in details:
            term = detail["term"]
            if term["name"].lower() == keyword_lower:
                return True
            for alt in detail.get("uf", []):
                if alt["name"].lower() == keyword_lower:
                    return True
    except (KeyError, TypeError):
        return None

    return False


def find_invalid_keywords(thesaurus_name, keywords, lookup=None):
    """
    Description:
        Checks a list of keywords against a named USGS controlled
        vocabulary and returns the ones that are not recognized terms in
        that thesaurus.

    Args:
        thesaurus_name (str): The contents of a <themekt> or <placekt>
            element. If this is free text (see is_free_text), no check is
            performed.
        keywords (list of str): The <themekey>/<placekey> values to check.
        lookup (dict, optional): A pre-fetched thesaurus name -> thcode
            mapping (see get_thesauri_lookup). Fetched automatically if
            not provided.

    Returns:
        list of str or None:
            - [] if the thesaurus is free text or every keyword is a
              recognized term.
            - A list of the keywords that are not recognized terms in the
              named thesaurus.
            - None if the check could not be performed (thesaurus name
              not found, or the service is unreachable) -- distinct from
              [] so callers can choose to skip reporting rather than
              imply "all valid".
    """

    if is_free_text(thesaurus_name):
        return []

    if lookup is None:
        lookup = get_thesauri_lookup()

    if lookup is None or thesaurus_name not in lookup:
        return None

    thcode = lookup[thesaurus_name]

    invalid = []
    for kw in keywords:
        if not kw:
            continue
        is_known = _term_is_known(thcode, kw)
        if is_known is None:
            return None
        if not is_known:
            invalid.append(kw)

    return invalid
