"""Unittests for core.data_io"""


import pytest

import pandas as pd

import pymdwizard


def test_search_common_name():
    df = pymdwizard.core.taxonomy.search_by_common_name("brown bear")
    assert list(df.columns) == ['commonName', 'language', 'tsn']

    results = pymdwizard.core.taxonomy.search_by_common_name("brown bear",
                                                            as_dataframe=False)
    assert list(results[0].keys()) == ['commonName', 'language', 'tsn']


def test_search_scientific_name():
    df = pymdwizard.core.taxonomy.search_by_scientific_name("gulo gulo")
    assert list(df.columns) == ['tsn', 'author', 'combinedName', 'kingdom',
                                'unitInd1', 'unitInd2', 'unitInd3', 'unitInd4',
                                'unitName1', 'unitName2', 'unitName3',
                                'unitName4']

    results = pymdwizard.core.search_by_scientific_name("gulo gulo",
                                                        as_dataframe=False)
    assert list(results[0].keys()) == ['tsn', 'author', 'combinedName',
                                       'kingdom', 'unitInd1', 'unitInd2',
                                       'unitInd3', 'unitInd4', 'unitName1',
                                       'unitName2', 'unitName3', 'unitName4']


def test_get_common_names_tsn():
    df = pymdwizard.core.taxonomy.get_common_names_tsn(202385)
    assert list(df.columns) == ['commonName', 'language', 'tsn']

    results = pymdwizard.core.taxonomy.get_common_names_tsn(202385,
                                                           as_dataframe=False)
    assert list(results[0].keys()) == ['commonName', 'language', 'tsn']
