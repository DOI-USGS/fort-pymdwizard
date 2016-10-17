"""Unittests for core.data_io"""


import pytest

import pandas as pd

from pymdwizard.core.data_io import read_csv


def test_read_csv():
    filepath = "tests/data/iris.csv"
    df = read_csv(filepath)
    assert df.shape == (150, 5)
    assert list(df.columns) == [u'sepal_length', u'sepal_width',
                                u'petal_length', u'petal_width',
                                u'species']