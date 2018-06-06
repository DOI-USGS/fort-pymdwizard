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
Module contains methods for querying the ITIS webservice
and formatting the results into XML formatted FGDC taxonomy sections.

Attributes
----------
ITIS_BASE_URL : str
    ITIS service base url


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

import collections
import requests
import warnings

try:
    import pandas as pd
except ImportError:
    warnings.warn('Pandas library not installed, dataframes disabled')
    pd = None

# internal package imports
from pymdwizard.core import xml_utils
from pymdwizard.core import utils

ITIS_BASE_URL = 'http://www.itis.gov/ITISWebService/services/ITISService/'
NS21 = {'ax21': 'http://data.itis_service.itis.usgs.gov/xsd'}
NS23 = {'ax23': 'http://metadata.itis_service.itis.usgs.gov/xsd'}

kingdom_lookup = {'Animalia': 202423,
                 'Chromista': 630578,
                 'Protozoa': 630577,
                 'Fungi': 555705,
                 'Bacteria': 50,
                 'Plantae': 202422,
                 'Archaea': 935939,
                 None: None}


def search_by_common_name(common_name, as_dataframe=True, **kwargs):
    """
        Returns a list of items from the ITIS searchByCommonName function.
        The resulting pandas dataframe or list of dictionaries contains
         the tsn, as well as common name

    Parameters
    ----------
    common_name : str
        The string to match on

    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    Returns
    -------
        pandas dataframe or list of dictionaries with common names and tsns
    """
    results = _get_xml(ITIS_BASE_URL + 'searchByCommonName',
                       payload={'srchKey': common_name})
    common_names = results.xpath('//ax21:commonNames', namespaces=NS21)
    if as_dataframe and pd:
        return xml_utils.element_to_df(common_names)
    else:
        return xml_utils.element_to_list(common_names)


def search_by_scientific_name(scientific_name, as_dataframe=True, **kwargs):
    """
        Returns a list of items from the ITIS searchByCommonName function.
        The resulting pandas dataframe or list of dictionaries contains
         the tsn, as well as common name

    Parameters
    ----------
    scientific_name : str
        The string to match on

    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    Returns
    -------
        pandas dataframe or list of dictionaries with scientific_names and tsns
    """
    results = _get_xml(ITIS_BASE_URL + 'searchByScientificName',
                       payload={'srchKey': scientific_name})
    scientific_names = results.xpath('//ax21:scientificNames', namespaces=NS21)
    if as_dataframe and pd:
        return xml_utils.element_to_df(scientific_names)
    else:
        return xml_utils.element_to_list(scientific_names)


def get_full_hierarchy_from_tsn(tsn, as_dataframe=True, include_children=True,
                                **kwargs):
    """
        Returns a list of items from the ITIS getFullHierarchyFromTSN function.
        The resulting pandas dataframe or list of dictionaries contains
         the tsn, as well as common name

    Parameters
    ----------
    tsn : int
        The ITIS taxonomic serial number to query

    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    include_children : bool
        flag to optionally return the child taxonomies of the given taxon

    Returns
    -------
        pandas dataframe or list of dictionaries with common names and tsns
    """
    results = _get_xml(ITIS_BASE_URL + 'getFullHierarchyFromTSN',
                       payload={'tsn': tsn})
    hierarchy = results.xpath('//ax21:hierarchyList', namespaces=NS21)
    if as_dataframe and pd:
        df = xml_utils.element_to_df(hierarchy)
        if not include_children:
            try:
                df = df[df.parentTsn!=str(tsn)]
            except:
                pass
        return df
    else:
        d = xml_utils.element_to_list(hierarchy)
        if not include_children:
            d = [r for r in d if r['parentTsn'] != str(tsn)]
        return d


def get_common_names_tsn(tsn, as_dataframe=True, **kwargs):
    """
        Returns a list of items from the ITIS getFullHierarchyFromTSN function.
        The resulting pandas dataframe or list of dictionaries contains
         the tsn, as well as common name

    Parameters
    ----------
    tsn : int
        The ITIS taxonomic serial number to query

    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    Returns
    -------
        pandas dataframe or list of dictionaries with common names and tsns
    """
    results = _get_xml(ITIS_BASE_URL + 'getCommonNamesFromTSN',
                       payload={'tsn': tsn})
    commmon_names = results.xpath('//ax21:commonNames', namespaces=NS21)
    if as_dataframe and pd:
        return xml_utils.element_to_df(commmon_names)
    else:
        return xml_utils.element_to_list(commmon_names)


def get_rank_names(as_dataframe=True, **kwargs):
    """
    Provides a list of all the unique rank names contained in the database and
    their kingdom and rank ID values.

    Parameters
    ----------
    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    kwargs

    Returns
    -------

    """
    results = _get_xml(ITIS_BASE_URL + 'getRankNames',
                       payload={})

    rank_names = results.xpath('//ax23:rankNames', namespaces=NS23)
    if as_dataframe and pd:
        return xml_utils.element_to_df(rank_names)
    else:
        return xml_utils.element_to_list(rank_names)


def get_currency_from_tsn(tsn, as_dataframe=True, **kwargs):
    """
        Returns a list of items from the ITIS getFullHierarchyFromTSN function.
        The resulting pandas dataframe or list of dictionaries contains
         the tsn, as well as common name

    Parameters
    ----------
    tsn : int
        The ITIS taxonomic serial number to query

    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    Returns
    -------
        pandas dataframe or list of dictionaries with common names and tsns
    """
    results = _get_xml(ITIS_BASE_URL + 'getCurrencyFromTSN',
                       payload={'tsn': tsn})
    if as_dataframe and pd:
        return xml_utils.element_to_df(results)
    else:
        return xml_utils.element_to_list(results)


def get_full_record_from_tsn(tsn, as_dataframe=False, **kwargs):
    """
        Returns a list of items from the ITIS getFullHierarchyFromTSN function.
        The resulting pandas dataframe or list of dictionaries contains
         the tsn, as well as common name

    Parameters
    ----------
    tsn : int
        The ITIS taxonomic serial number to query

    as_dataframe : bool
        if True return pandas dataframe, if False return list of dictionaries

    Returns
    -------
        pandas dataframe or list of dictionaries with common names and tsns
    """

    results = _get_xml(ITIS_BASE_URL + 'getFullRecordFromTSN',
                       payload={'tsn': tsn}).getchildren()[0]
    if as_dataframe:
        dfs = collections.OrderedDict()
        for child in results.getchildren():
            df = xml_utils.element_to_df([child]).dropna()
            dfs[xml_utils.parse_tag(child.tag)] = df
        return dfs
    else:
        return xml_utils.node_to_dict(results, add_fgdc=False)


def _get_xml(url, payload, **kwargs):
    out = utils.requests_pem_get(url, params=payload)
    out.raise_for_status()
    tt = xml_utils.string_to_node(out.content)
    return tt


def _to_lower(items):
    """
        Converts a list of strings into a list of lower case strings.

    Parameters
    ----------
    items : list
        A list of strings.

    Returns
    -------
        The list of items all converted to lower case.
    """
    return [item.lower() for item in items]


class Taxon(object):
    """ object to hold a representation of a single taxonomic item.
        Allows for a nested hierarchical model by specifying optional
        children Taxons, and a single parent Taxon"""


    def __init__(self, taxon_name=None, taxon_value=None,
                 tsn=None, children=None, parent=None):
        """

        Parameters
        ----------
        taxon_name : str
            The taxonomic level name ('species', 'genus', 'family', etc)
        taxon_value : str
            The value of this specific taxonomic level ('homo', 'sapiens', etc)
        tsn : int
            The ITIS taxonomic serial number

        children : list of taxon objects
            This list contains the child or children Taxon objects of this
            object
        parent : taxon object
            The Taxon representing the parent Taxon object of this object
        """
        self.taxon_name = taxon_name
        self.taxon_value = taxon_value
        self.tsn = tsn

        self.populate_ranknames()

        if not taxon_name and not taxon_value and tsn:
            self.load_from_tsn()

        if children:
            self.children = children
        else:
            self.children = []
        self.parent = parent
        self.indent = "  "*int(int(self._indent_lookup[taxon_name]) / 10)

    def populate_ranknames(self):
        try:
            self._rank_names = get_rank_names()

            self._rank_names.drop_duplicates(inplace=True)
            del(self._rank_names['kingdomName'])
            self._rank_names['rankId'] = pd.to_numeric(self._rank_names['rankId'])
            self. _rank_names = self._rank_names.append(pd.DataFrame([{"rankName": "Life", "rankId":1}]))
            self._rank_names = self._rank_names.append(pd.DataFrame([{"rankName": "Domain", "rankId":5}]))

            self._indent_lookup = dict(zip(self._rank_names.rankName, self._rank_names.rankId))
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            self._rank_names = {}
            self._indent_lookup = {}

    def __eq__(self, other):
        return self.taxon_name == other.taxon_name and \
                                self.taxon_value == other.taxonname and \
                                self.tsn == other.tsn

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = self.indent+"{}:{} (tsn={})\n".format(self.taxon_name,
                                                       self.taxon_value,
                                                       self.tsn)
        if self.children:
            string += "".join([str(c) for c in self.children])
        return string

    def add_child(self, child):
        """

        Parameters
        ----------
        child : Taxon
                Adds a child Taxon to the list of children of this object
        Returns
        -------
            None
        """
        child.parent = self
        #         child.indent = "  "+self.indent
        self.children.append(child)

    def find_child_by_tsn(self, tsn):
        """

        Parameters
        ----------
        tsn : int

        Returns
        -------
            If no match is found returns None
            else returns taxon object which matches the given tsn
        """
        if str(self.tsn) == str(tsn):
            return self
        else:
            for child in self.children:
                match = child.find_child_by_tsn(tsn)
                if match:
                    return match
        return None

    def load_from_tsn(self):
        merge_taxons([self.tsn])


def get_kingdom(heirarchy):
    try:
        return str(heirarchy[heirarchy.rankName == 'Kingdom']['taxonName'][0])
    except IndexError:
        return None


def get_taxon_root(kingdoms):
    eukaryota = ['Animalia', 'Chromista', 'Protozoa', 'Fungi', 'Plantae']
    if len(kingdoms) == 0:
        root_name = 'Life'
        root_value = 'Life'
        tsn = None
    elif len(kingdoms) > 1:
        tsn = None
        if set(eukaryota).issuperset(set(kingdoms)):
            root_name = 'Domain'
            root_value = 'Eukaryota'
        else:
            root_name = 'Life'
            root_value = 'Life'
    else:
        root_name = 'Kingdom'
        root_value = kingdoms[0]
        tsn = kingdom_lookup[root_value]

    return Taxon(taxon_name=root_name, taxon_value=root_value, tsn=tsn)


def merge_taxons(tsns):
    """

    Parameters
    ----------
    taxons : list of tsns

    Returns
    -------
        a Taxon that contains all of the content of all the input Taxons


    """
    heirarchies  = []
    for tsn in tsns:
        accepted_tsn = get_accepted_tsn(tsn)

        hierarchy = get_full_hierarchy_from_tsn(accepted_tsn,
                                                include_children=False)
        heirarchies.append(hierarchy)

    kingdoms = list(set([get_kingdom(h) for h in heirarchies]))

    root_taxon = get_taxon_root(kingdoms)

    for hierarchy in heirarchies:
        for row in hierarchy.itertuples():
            #see if taxonomy is alreay there
            existing_taxon = root_taxon.find_child_by_tsn(row.tsn)
            if not existing_taxon:
                child_taxon = Taxon(taxon_name=row.rankName,
                                    taxon_value=row.taxonName,
                                    tsn=row.tsn)
                parent = root_taxon.find_child_by_tsn(row.parentTsn)
                parent.add_child(child_taxon)

    return root_taxon


def get_accepted_tsn(tsn):
    """
    Runs a web service query to identify the accepted tsn for a given tsn.
    If anything goes wrong, the original tsn is returned.

    Parameters
    ----------
    tsn : str
          A taxonomic serial number (ITIS identifier)

    Returns
    -------
    str
    """
    try:
        return _get_xml(ITIS_BASE_URL + 'getAcceptedNamesFromTSN',
                        payload={'tsn': tsn}).xpath('//ax21:acceptedTsn',
                                                    namespaces=NS21)[0].text
    except:
        return tsn


def gen_taxonomy_section(keywords, tsns, include_common_names=False):
    taxonomy = xml_utils.xml_node(tag="taxonomy")
    keywtax = xml_utils.xml_node(tag="keywtax")
    taxonkt = xml_utils.xml_node(tag="taxonkt", text='None',
                                 parent_node=keywtax)


    for keyword in keywords:
        taxonkey = xml_utils.xml_node(tag="taxonkey", text=keyword,
                                      parent_node=keywtax)

    taxonomy.append(keywtax)

    taxoncl = gen_fgdc_taxoncl(tsns, include_common_names, include_tsns=tsns)
    taxonomy.append(taxoncl)
    return taxonomy


def gen_fgdc_taxoncl(tsns, include_common_names=False, include_tsns=[]):
    taxon = merge_taxons(tsns)
    return _gen_fgdc_taxonomy_section(taxon, include_common_names, include_tsns)


def _gen_fgdc_taxonomy_section(taxon, include_common_names=False,
                               include_tsns=[]):
    taxonomicclassification = xml_utils.xml_node(tag="taxoncl")
    taxrankname = xml_utils.xml_node(tag="taxonrn")
    taxrankname.text = taxon.taxon_name
    taxonomicclassification.append(taxrankname)

    taxrankvalue = xml_utils.xml_node(tag="taxonrv")
    taxrankvalue.text = taxon.taxon_value
    taxonomicclassification.append(taxrankvalue)

    if include_common_names and taxon.tsn:
        try:
            df = get_common_names_tsn(taxon.tsn)
            if 'language' in df.columns:
                for common_name in df.query('language == "English"').commonName:
                    applicable_common_name = xml_utils.xml_node(tag="common")
                    applicable_common_name.text = common_name
                    taxonomicclassification.append(applicable_common_name)
        except (ValueError, IndexError):
            pass

    if str(taxon.tsn) in include_tsns:
        tsn_common_name = xml_utils.xml_node(tag="common")
        tsn_common_name.text = "TSN: {}".format(taxon.tsn)
        taxonomicclassification.append(tsn_common_name)

    for child in taxon.children:
        child_node = _gen_fgdc_taxonomy_section(child, include_common_names,
                                                include_tsns=include_tsns)
        taxonomicclassification.append(child_node)

    return taxonomicclassification







