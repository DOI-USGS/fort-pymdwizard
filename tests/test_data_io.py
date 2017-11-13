"""Unittests for core.data_io"""


import pytest

import pandas as pd

import pymdwizard


def test_read_csv():
    fname = "tests/data/iris.csv"
    df = pymdwizard.core.data_io.read_csv(fname)
    assert df.shape == (150, 5)
    assert list(df.columns) == [u'sepal_length', u'sepal_width',
                                u'petal_length', u'petal_width',
                                u'species']