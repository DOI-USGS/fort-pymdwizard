#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module contains methods for querying the ITIS webservice
and formatting the results into XML formatted FGDC taxonomy sections.

Attributes
----------
ITIS_BASE_URL : str
    ITIS service base url


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import collections
import requests
import warnings

# Non-standard python libraries.
try:
    import pandas as pd
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (xml_utils, utils)
except ImportError as err:
    raise ImportError(err, __file__)

# Global variables of URLs to access the Integrated Taxonomic Information System
# (ITIS) for handling taxonomic names.
# IMPT: These are not https (does not work)
ITIS_BASE_URL = "http://www.itis.gov/ITISWebService/services/ITISService/"
NS21 = {"ax21": "http://data.itis_service.itis.usgs.gov/xsd"}
NS23 = {"ax23": "http://metadata.itis_service.itis.usgs.gov/xsd"}

# GLOBAL Dictionary defining kingdoms.
KINGDON_LOOKUP = {
    "Animalia": 202423,
    "Chromista": 630578,
    "Protozoa": 630577,
    "Fungi": 555705,
    "Bacteria": 50,
    "Plantae": 202422,
    "Archaea": 935939,
    None: None,
}


def search_by_common_name(common_name, as_dataframe=True, **kwargs):
    """
    Description:
        Returns a list of items from the ITIS searchByCommonName function.
        The resulting pandas DataFrame or list of dictionaries contains
        the tsn, as well as common names.

    Args:
        common_name (str): The string to match on for the search.
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.

    Returns:
        pandas.DataFrame or list: A DataFrame or list of dictionaries
            containing common names and tsns.
    """

    # Construct the search URL and retrieve XML results from ITIS.
    results = _get_xml(
        ITIS_BASE_URL + "searchByCommonName",
        payload={"srchKey": common_name}
    )

    # Extract common names using XPath.
    common_names = results.xpath("//ax21:commonNames", namespaces=NS21)

    # Return results as a DataFrame if requested and pandas is available.
    if as_dataframe and pd:
        return xml_utils.element_to_df(common_names)
    else:
        # Otherwise return the results as a list of dictionaries.
        return xml_utils.element_to_list(common_names)


def search_by_scientific_name(scientific_name, as_dataframe=True, **kwargs):
    """
    Description:
        Returns a list of items from the ITIS searchByScientificName function.
        The resulting pandas DataFrame or list of dictionaries contains the
        tsn, as well as scientific names.

    Args:
        scientific_name (str): The string to match on for the search.
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.

    Returns:
        pandas.DataFrame or list: A DataFrame or list of dictionaries containing
            scientific names and tsns.
    """

    # Construct the search URL and retrieve XML results from ITIS.
    results = _get_xml(
        ITIS_BASE_URL + "searchByScientificName",
        payload={"srchKey": scientific_name}
    )

    # Extract scientific names using XPath.
    scientific_names = results.xpath("//ax21:scientificNames", namespaces=NS21)

    # Return results as a DataFrame if requested and pandas is available.
    if as_dataframe and pd:
        return xml_utils.element_to_df(scientific_names)
    else:
        # Otherwise return the results as a list of dictionaries.
        return xml_utils.element_to_list(scientific_names)


def get_full_hierarchy_from_tsn(tsn, as_dataframe=True, include_children=True,
                                **kwargs):
    """
    Description:
        Returns a list of items from the ITIS getFullHierarchyFromTSN function.
        The resulting pandas DataFrame or list of dictionaries contains the
        tsn, as well as common names.

    Args:
        tsn (int): The ITIS taxonomic serial number to query.
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.
        include_children (bool): Flag to optionally return the child taxonomies
            of the given taxon.

    Returns:
        pandas.DataFrame or list: A DataFrame or list of dictionaries
            containing common names and tsns.
    """

    # Fetch the XML results from ITIS based on the provided tsn.
    results = _get_xml(
        ITIS_BASE_URL + "getFullHierarchyFromTSN",
        payload={"tsn": tsn}
    )

    # Extract the hierarchy from the results using XPath.
    hierarchy = results.xpath("//ax21:hierarchyList", namespaces=NS21)

    if as_dataframe and pd:
        # Convert the XML hierarchy to a pandas DataFrame
        df = xml_utils.element_to_df(hierarchy)

        # If children are not included, filter the DataFrame.
        if not include_children:
            try:
                df = df[df.parentTsn != str(tsn)]
            except KeyError:
                pass
        return df
    else:
        # Convert the XML hierarchy to a list of dictionaries.
        d = xml_utils.element_to_list(hierarchy)

        # If children are not included, filter the list.
        if not include_children:
            d = [r for r in d if r["parentTsn"] != str(tsn)]
        return d


def get_common_names_tsn(tsn, as_dataframe=True, **kwargs):
    """
    Description:
        Retrieves common names associated with the given ITIS TSN.

    Args:
        tsn (int): The ITIS taxonomic serial number to query.
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.

    Returns:
        pandas.DataFrame or list: A DataFrame or list of dictionaries
            containing common names and tsns.
    """

    # Fetch the XML results from ITIS using the provided TSN.
    results = _get_xml(
        ITIS_BASE_URL + "getCommonNamesFromTSN",
        payload={"tsn": tsn}
    )

    # Extract common names using XPath.
    common_names = results.xpath("//ax21:commonNames", namespaces=NS21)

    # Check if the results should be returned as a DataFrame.
    if as_dataframe and pd:
        return xml_utils.element_to_df(common_names)
    else:
        return xml_utils.element_to_list(common_names)


def get_rank_names(as_dataframe=True, **kwargs):
    """
    Description:
        Provides a list of all unique rank names contained in the database
        along with their kingdom and rank ID values.

    Args:
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.
        kwargs (dict): Additional keyword arguments for extensibility.

    Returns:
        pandas.DataFrame or list: A DataFrame containing rank names and their
            associated values or a list of dictionaries if as_dataframe is
            False.
    """

    # Fetch the XML results from ITIS for rank names.
    results = _get_xml(ITIS_BASE_URL + "getRankNames", payload={})

    # Extract rank names using XPath.
    rank_names = results.xpath("//ax23:rankNames", namespaces=NS23)

    # Return results as a DataFrame if requested and pandas is available.
    if as_dataframe and pd:
        return xml_utils.element_to_df(rank_names)
    else:
        # Otherwise return the results as a list of dictionaries.
        return xml_utils.element_to_list(rank_names)


def get_currency_from_tsn(tsn, as_dataframe=True, **kwargs):
    """
    Description:
        Retrieves currency information associated with a given ITIS TSN.

    Args:
        tsn (int): The ITIS taxonomic serial number to query.
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.

    Returns:
        pandas.DataFrame or list: A DataFrame or list of dictionaries containing
            currency information associated with the TSN.
    """

    # Fetch the XML results from ITIS using the provided TSN.
    results = _get_xml(
        ITIS_BASE_URL + "getCurrencyFromTSN",
        payload={"tsn": tsn}
    )

    # Return results as a DataFrame if requested and pandas is available.
    if as_dataframe and pd:
        return xml_utils.element_to_df(results)
    else:
        # Otherwise return the results as a list of dictionaries.
        return xml_utils.element_to_list(results)


def get_full_record_from_tsn(tsn, as_dataframe=False, **kwargs):
    """
    Description:
        Retrieves a full record associated with a given ITIS TSN.

    Args:
        tsn (int): The ITIS taxonomic serial number to query.
        as_dataframe (bool): If True, return a pandas DataFrame; if False,
            return a list of dictionaries.

    Returns:
        pandas.DataFrame or dict: A DataFrame or dictionary containing the full
            record data associated with the TSN.
    """

    # Fetch the XML results from ITIS using the provided TSN.
    results = _get_xml(
        ITIS_BASE_URL + "getFullRecordFromTSN",
        payload={"tsn": tsn}
    ).getchildren()[0]  # Get the first child of the results.

    if as_dataframe:
        # Create an OrderedDict to hold DataFrames for each child.
        dfs = collections.OrderedDict()

        # Iterate over each child element and convert to DataFrame.
        for child in results.getchildren():
            df = xml_utils.element_to_df([child]).dropna()
            dfs[xml_utils.parse_tag(child.tag)] = df  # Use tag as key

        return dfs
    else:
        # Convert the results to a dictionary without FGDC added.
        return xml_utils.node_to_dict(results, add_fgdc=False)


def _get_xml(url, payload, **kwargs):
    """
    Description:
        Fetches XML data from a specified URL with given parameters.

    Args:
        url (str): The endpoint URL to send the request to.
        payload (dict): Parameters to include in the request.
        kwargs (dict): Additional arguments to pass to the request function.

    Returns:
        lxml.etree.Element: The parsed XML node obtained from the response
            content.
    """

    tries = 0  # Initialize the attempt counter
    while tries < 5:  # Try up to 5 times to fetch the XML.
        try:
            # Make GET request with parameters.
            out = utils.requests_pem_get(url, params=payload)
            out.raise_for_status()  # Raise an error for bad responses
            tt = xml_utils.string_to_node(out.content)  # Parse response

            return tt  # Return the parsed XML node
        except:
            # Increment the attempt counter on exception.
            tries += 1

    # Final attempt outside the loop if previous attempts failed.
    out = utils.requests_pem_get(url, params=payload)
    out.raise_for_status()  # Raise an error for bad responses
    tt = xml_utils.string_to_node(out.content)  # Parse response

    return tt  # Return the parsed XML node
    
    
def _to_lower(items):
    """
    Description:
        Converts a list of strings into a list of lower case strings.

    Args:
        items (list): A list of strings to be converted to lower case.

    Returns:
        list: A list of strings, all converted to lower case.
    """

    # Use a list comprehension to convert each string to lower case.
    return [item.lower() for item in items]  # Return the new list


class Taxon(object):
    """
    Object to hold a representation of a single taxonomic item. Allows for a
    nested hierarchical model by specifying optional children Taxons, and a
    single parent Taxon
    """

    def __init__(self, taxon_name=None, taxon_value=None, tsn=None,
                 children=None, parent=None):
        """
        Initializes a Taxon object with the provided parameters.

        Args:
            taxon_name (str): The taxonomic level name (e.g., 'species',
                'genus', etc.).
            taxon_value (str): The value of this specific taxonomic level
                (e.g., 'homo', 'sapiens', etc.).
            tsn (int): The ITIS taxonomic serial number.
            children (list of Taxon): A list containing child Taxon objects of
                this object.
            parent (Taxon): The parent Taxon object of this Taxon.
        """

        self.taxon_name = taxon_name
        self.taxon_value = taxon_value
        self.tsn = tsn

        # Populate rank names for this taxon.
        self.populate_ranknames()

        # Load taxon from TSN if no name/value provided.
        if not taxon_name and not taxon_value and tsn:
            self.load_from_tsn()

        # Initialize children.
        self.children = children if children else []

        self.parent = parent

        # Indent for display based on rank lookup.
        self.indent = "  " * int(int(self._indent_lookup[taxon_name]) / 10)

    def populate_ranknames(self):
        """
        Populates the rank names and their corresponding IDs from an API call.
        Handles connection errors appropriately.
        """

        try:
            # Retrieve and clean rank names.
            self._rank_names = get_rank_names()
            self._rank_names.drop_duplicates(inplace=True)
            del self._rank_names["kingdomName"]
            self._rank_names["rankId"] = \
                pd.to_numeric(self._rank_names["rankId"])

            # Create additional ranks DataFrame.
            additional_ranks = pd.DataFrame([
                {"rankName": "Life", "rankId": 1},
                {"rankName": "Domain", "rankId": 5}
            ])

            # Concatenate additional ranks to the existing DataFrame.
            self._rank_names = pd.concat(
                [self._rank_names, additional_ranks], ignore_index=True
            )

            # Create lookup dictionary for ranks.
            self._indent_lookup = dict(
                zip(self._rank_names.rankName, self._rank_names.rankId)
            )
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError):
            # Initialize as an empty DataFrame on error.
            self._rank_names = pd.DataFrame()
            self._indent_lookup = {}

    def __eq__(self, other):
        """Checks equality between two Taxon objects based on attributes."""

        return (
            self.taxon_name == other.taxon_name
            and self.taxon_value == other.taxonname
            and self.tsn == other.tsn
        )

    def __repr__(self):
        """Return the string representation of the Taxon object."""

        return self.__str__()

    def __str__(self):
        """Return a formatted string representation of the Taxon."""

        string = self.indent + "{}:{} (tsn={})\n".format(
            self.taxon_name, self.taxon_value, self.tsn
        )
        if self.children:
            string += "".join([str(c) for c in self.children])
        return string

    def add_child(self, child):
        """
        Description:
            Adds a child Taxon to the list of children of this Taxon.

        Args:
            child (Taxon): The child Taxon to be added to this Taxon.

        Returns: None
        """

        child.parent = self  # Set the parent for the child
        self.children.append(child)  # Append the child

    def find_child_by_tsn(self, tsn):
        """
        Finds a child Taxon by its TSN.

        Args:
            tsn (int): The TSN of the Taxon to find.

        Returns:
            Taxon or None: If no match is found, returns None;
                otherwise returns the matching Taxon object.
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
        """Loads the Taxon information based on its TSN."""

        merge_taxons([self.tsn])


def get_kingdom(hierarchy):
    """
    Description:
        Retrieves the kingdom name from a given taxonomy hierarchy.

    Args:
        hierarchy (DataFrame): A pandas DataFrame representing the taxonomy.

    Returns:
        str or None: The name of the kingdom if found; otherwise, None.
    """

    try:
        # Access the taxon name corresponding to the "Kingdom" rank.
        return str(hierarchy[hierarchy.rankName == "Kingdom"]["taxonName"][0])
    except IndexError:
        return None


def get_taxon_root(kingdoms):
    """
    Description:
        Determines the root taxon based on the provided kingdoms.

    Args:
        kingdoms (list): A list of kingdom names.

    Returns:
        Taxon: A Taxon object representing the root taxon.
    """

    # Define the set of eukaryotic kingdoms.
    eukaryota = ["Animalia", "Chromista", "Protozoa", "Fungi", "Plantae"]

    # Determine root properties based on the number of kingdoms.
    if len(kingdoms) == 0:
        root_name = "Life"
        root_value = "Life"
        tsn = None
    elif len(kingdoms) > 1:
        tsn = None
        # Check if all kingdoms are eukaryotic.
        if set(eukaryota).issuperset(set(kingdoms)):
            root_name = "Domain"
            root_value = "Eukaryota"
        else:
            root_name = "Life"
            root_value = "Life"
    else:
        root_name = "Kingdom"
        root_value = kingdoms[0]
        tsn = KINGDON_LOOKUP[root_value]  # Lookup TSN for the kingdom

    # Return Taxon object with the determined root properties.
    return Taxon(taxon_name=root_name, taxon_value=root_value, tsn=tsn)


def merge_taxons(tsns):
    """
    Description:
        Merges multiple taxonomic serial numbers (TSNs) into a single
        Taxon structure.

    Args:
        tsns (list): A list of taxonomic serial numbers.

    Returns:
        Taxon: A Taxon object that contains all content of the input
            Taxons merged into a single hierarchy.
    """

    # Initialize a list to store hierarchy data.
    hierarchies = []

    # Get the hierarchy for each TSN and store it.
    for tsn in tsns:
        accepted_tsn = get_accepted_tsn(tsn)
        hierarchy = get_full_hierarchy_from_tsn(
            accepted_tsn, include_children=False
        )  # Get the full hierarchy for the accepted TSN.
        hierarchies.append(hierarchy)

    # Retrieve unique kingdoms from the hierarchies.
    kingdoms = list(set([get_kingdom(h) for h in hierarchies]))

    # Get the root taxon based on identified kingdoms.
    root_taxon = get_taxon_root(kingdoms)

    # Iterate through each hierarchy and add taxons to the root.
    for hierarchy in hierarchies:
        for row in hierarchy.itertuples():
            # Check if the taxon already exists.
            existing_taxon = root_taxon.find_child_by_tsn(row.tsn)
            if not existing_taxon:  # If not found, create a new taxon
                child_taxon = Taxon(
                    taxon_name=row.rankName,
                    taxon_value=row.taxonName,
                    tsn=row.tsn
                )

                # Find the parent taxon and add the new child taxon.
                parent = root_taxon.find_child_by_tsn(row.parentTsn)
                parent.add_child(child_taxon)

    return root_taxon


def get_accepted_tsn(tsn):
    """
    Description:
        Runs a web service query to identify the accepted TSN for a given TSN.
        If anything goes wrong, the original TSN is returned.

    Args:
        tsn (str): A taxonomic serial number (ITIS identifier).

    Returns:
        str: The accepted TSN if found; otherwise, the original TSN.
    """

    try:
        # Fetch XML data and extract the accepted TSN using XPath.
        return (
            _get_xml(ITIS_BASE_URL + "getAcceptedNamesFromTSN",
                     payload={"tsn": tsn})
            .xpath("//ax21:acceptedTsn", namespaces=NS21)[0]
            .text
        )
    except:
        # Return the original TSN if an error occurs.
        return tsn


def gen_taxonomy_section(keywords, tsns, include_common_names=False):
    """
    Description:
        Generates a taxonomy section as an XML node using given keywords
        and taxonomic serial numbers (TSNs).

    Args:
        keywords (list): A list of keywords for the taxonomy section.
        tsns (list): A list of taxonomic serial numbers to include in the
            section.
        include_common_names (bool): Flag to determine if common names should
            be included in the output.

    Returns:
        lxml.etree.Element: An XML node representing the taxonomy section.
    """

    # Create the root taxonomy XML node and keywtax node.
    taxonomy = xml_utils.xml_node(tag="taxonomy")
    keywtax = xml_utils.xml_node(tag="keywtax")

    # Create a taxonkt node with default text "None".
    taxonkt = xml_utils.xml_node(tag="taxonkt", text="None",
                                 parent_node=keywtax)

    # Add each keyword as a taxonkey node.
    for keyword in keywords:
        xml_utils.xml_node(tag="taxonkey", text=keyword, parent_node=keywtax)

    # Append the keywtax node to the taxonomy node.
    taxonomy.append(keywtax)

    # Generate the FGDC taxoncl node using the provided TSNs.
    taxoncl = gen_fgdc_taxoncl(tsns, include_common_names, include_tsns=tsns)

    # Append the taxoncl node to the taxonomy node.
    taxonomy.append(taxoncl)

    return taxonomy


def gen_fgdc_taxoncl(tsns, include_common_names=False, include_tsns=[]):
    """
    Description:
        Generates FGDC taxonomy information for given taxonomic serial
        numbers (TSNs).

    Args:
        tsns (list): A list of taxonomic serial numbers to be merged.
        include_common_names (bool): If True, include common names in the
            output.
        include_tsns (list): Optional list of TSNs to include in the output.

    Returns:
        lxml.etree.Element: An XML node representing the FGDC taxonomy section.
    """

    # Merge the provided TSNs into a single taxon object.
    taxon = merge_taxons(tsns)

    # Generate the FGDC taxonomy section using the merged taxon.
    return _gen_fgdc_taxonomy_section(taxon, include_common_names, include_tsns)


def _gen_fgdc_taxonomy_section(taxon, include_common_names=False,
                               include_tsns=[]):
    """
    Description:
        Generates an FGDC taxonomy section as an XML node for the given
        taxon and its children.

    Args:
        taxon (object):
            An object representing a taxon with attributes for taxon name,
            value, TSN, and children.

        include_common_names (bool): If True, include common names for the
            taxon.

        include_tsns (list): A list of TSNs to include in the output.

    Returns:
        lxml.etree.Element: An XML node representing the taxonomic
            classification section.
    """

    # Create the main taxonomic classification node.
    taxonomicclassification = xml_utils.xml_node(tag="taxoncl")

    # Create and append the taxon rank name node.
    taxrankname = xml_utils.xml_node(tag="taxonrn")
    taxrankname.text = taxon.taxon_name
    taxonomicclassification.append(taxrankname)

    # Create and append the taxon rank value node.
    taxrankvalue = xml_utils.xml_node(tag="taxonrv")
    taxrankvalue.text = taxon.taxon_value
    taxonomicclassification.append(taxrankvalue)

    # Include common names if requested and a TSN is available.
    if include_common_names and taxon.tsn:
        try:
            # Retrieve common names associated with the TSN.
            df = get_common_names_tsn(taxon.tsn)
            if "language" in df.columns:
                # Append common names in English to the classification
                for common_name in df.query('language == "English"').commonName:
                    applicable_common_name = xml_utils.xml_node(tag="common")
                    applicable_common_name.text = common_name
                    taxonomicclassification.append(applicable_common_name)
        except (ValueError, IndexError):
            pass  # Ignore errors retrieving common names

    # Include TSN in the output if specified.
    if str(taxon.tsn) in include_tsns:
        tsn_common_name = xml_utils.xml_node(tag="common")
        tsn_common_name.text = "TSN: {}".format(taxon.tsn)
        taxonomicclassification.append(tsn_common_name)

    # Recursively generate sections for each child taxon.
    for child in taxon.children:
        child_node = _gen_fgdc_taxonomy_section(
            child, include_common_names, include_tsns=include_tsns
        )
        taxonomicclassification.append(child_node)

    return taxonomicclassification
