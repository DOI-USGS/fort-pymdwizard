"""Unittests for core.data_io"""


import pytest

from pymdwizard.core import spatial_utils

import pymdwizard


def test_shp():
    fname = "tests/data/projections/wgs84.shp"
    layer = spatial_utils.get_layer(fname)
    assert layer.GetName() == 'wgs84'

    extent = spatial_utils.get_extent(layer)
    assert extent == (-113.7224033, -113.5972322, 39.1362139, 39.3367364)

    geo_extent = spatial_utils.get_geographic_extent(layer)
    assert geo_extent == (-113.7224033, -113.5972322, 39.1362139, 39.3367364)

    fname2 = r"tests/data/projections/World_Azimuthal_Equidistant.shp"
    layer2 = spatial_utils.get_layer(fname2)

    extent = spatial_utils.get_extent(layer2)
    assert extent == (-9000045.450707654, -8967080.560731161,
                      7983954.351019523, 8011829.313610071)

    geo_extent = spatial_utils.get_geographic_extent(layer2)
    assert geo_extent == (-113.87509809270827,
                          -113.39545637692781,
                          39.13579145480427,
                          39.337014808573535)



