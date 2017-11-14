"""Unittests for taxonomy module"""


import pytest

import pandas as pd

import pymdwizard
from pymdwizard.core import taxonomy


def test_search_common_name():
    df = taxonomy.search_by_common_name("brown bear")
    assert list(df.columns) == ['commonName', 'language', 'tsn']

    results = taxonomy.search_by_common_name("brown bear", as_dataframe=False)
    assert list(results[0].keys()) == ['commonName', 'language', 'tsn']

    taxonomy.pd = None
    results = taxonomy.search_by_common_name("brown bear", as_dataframe=True)
    assert list(results[0].keys()) == ['commonName', 'language', 'tsn']
    taxonomy.pd = pd


def test_search_scientific_name():
    df = taxonomy.search_by_scientific_name("gulo gulo")
    assert list(df.columns) == ['tsn', 'author', 'combinedName', 'kingdom',
                                'unitInd1', 'unitInd2', 'unitInd3', 'unitInd4',
                                'unitName1', 'unitName2', 'unitName3',
                                'unitName4']

    results = taxonomy.search_by_scientific_name("gulo gulo",
                                                        as_dataframe=False)
    assert list(results[0].keys()) == ['tsn', 'author', 'combinedName',
                                       'kingdom', 'unitInd1', 'unitInd2',
                                       'unitInd3', 'unitInd4', 'unitName1',
                                       'unitName2', 'unitName3', 'unitName4']


def test_full_hierarchy_from_tsn():
    df = taxonomy.get_full_hierarchy_from_tsn(180694)
    assert list(df.columns) == ['tsn', 'author', 'parentName', 'parentTsn',
                                'rankName', 'taxonName']

    results = taxonomy.get_full_hierarchy_from_tsn(180694, as_dataframe=False)
    assert results[0]['taxonName'] == 'Animalia'

    no_species = taxonomy.get_full_hierarchy_from_tsn(180694,
                                                      as_dataframe=False,
                                                      include_children=False)
    assert no_species[-1]['rankName'] == 'Genus'

    has_species = taxonomy.get_full_hierarchy_from_tsn(180694,
                                                       as_dataframe=False,
                                                       include_children=True)
    assert has_species[-1]['rankName'] == 'Species'

    df = taxonomy.get_full_hierarchy_from_tsn(180694, include_children=False)
    assert df[df.rankName == 'Species'].empty

    df = taxonomy.get_full_hierarchy_from_tsn(180694, include_children=True)
    assert not df[df.rankName == 'Species'].empty


def test_get_common_names_tsn():
    df = taxonomy.get_common_names_tsn(202385)
    assert list(df.columns) == ['commonName', 'language', 'tsn']

    results = taxonomy.get_common_names_tsn(202385, as_dataframe=False)
    assert list(results[0].keys()) == ['commonName', 'language', 'tsn']


def test_to_lower():
    lower = taxonomy._to_lower(['Hello', 'WORLD'])
    assert lower == ['hello', 'world']


def test_gen_fgdc_taxonomy():
    fgdc_taxonomy = taxonomy.gen_fgdc_taxoncl(tsns=[180694])
    assert fgdc_taxonomy.tag == 'taxoncl'
    assert fgdc_taxonomy.getchildren()[1].text == 'Animalia'

    # Add a plant, so that the top level is Domain==Eukaryota
    fgdc_taxonomy = taxonomy.gen_fgdc_taxoncl(tsns=[180694, 183437])
    assert fgdc_taxonomy.getchildren()[1].text == 'Eukaryota'

    # Add a bacteria, so that the top level is Domain==Life
    fgdc_taxonomy = taxonomy.gen_fgdc_taxoncl(tsns=[180694, 183437, 951930])
    assert fgdc_taxonomy.getchildren()[1].text == 'Life'

    fgdc_taxonomy = taxonomy.gen_taxonomy_section(keywords=['test', 'test2'],
                                                  tsns=[180694, 183437])
    assert fgdc_taxonomy.tag == 'taxonomy'




