"""Unittests for core.data_io"""


import pytest

import pymdwizard


def test_parse_init():
    # Parse the version from the pymdwizard module.
    with open('pymdwizard/__init__.py') as f:
        for line in f:
            if line.find("__version__") >= 0:
                version = line.split("=")[1].strip()
                version = version.strip('"')
                version = version.strip("'")
    assert type(str(version)) == str
    assert type(pymdwizard.__version__) == str