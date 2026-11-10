"""Unittests for core.data_io"""


import pytest
from pymdwizard.core import spatial_utils



def test_shp():
    fname = "tests/data/projections/wgs84.shp"
    layer = spatial_utils.get_layer(fname)
    assert layer.GetName() == "wgs84"

    extent = spatial_utils.get_extent(layer)
    assert extent == (-113.7224033, -113.5972322, 39.1362139, 39.3367364)

    geo_extent = spatial_utils.get_geographic_extent(layer)
    # Note: GDAL coordinate order changed in recent versions (north/south swapped)
    assert geo_extent == (-113.7224033, -113.5972322, 39.3367364, 39.1362139)

    fname2 = r"tests/data/projections/World_Azimuthal_Equidistant.shp"
    layer2 = spatial_utils.get_layer(fname2)

    extent = spatial_utils.get_extent(layer2)
    assert extent == (
        -9000045.450707654,
        -8967080.560731161,
        7983954.351019523,
        8011829.313610071,
    )

    geo_extent = spatial_utils.get_geographic_extent(layer2)
    # Use pytest.approx for floating-point comparison (GDAL version differences)
    # Note: GDAL coordinate order changed - north/south swapped
    assert geo_extent == pytest.approx((
        -113.87509809270827,
        -113.39545637692781,
        39.337014808573535,
        39.13579145480427,
    ))


# ===========================================================================
# North/South ordering helper tests
#
# Unit tests for the North/South ordering helpers in core.spatial_utils.
# Covers ``ns_is_inverted`` and ``ns_ordered`` for inverted, ordered, equal,
# non-numeric, empty-string, and None inputs, including a negative-latitude
# (Southern-Hemisphere) inverted case.
# ===========================================================================

import random


# ---------------------------------------------------------------------------
# ns_is_inverted
# ---------------------------------------------------------------------------

def test_ns_is_inverted_true_when_north_below_south():
    # north < south -> inverted
    assert spatial_utils.ns_is_inverted(34.95, 41.25) is True


def test_ns_is_inverted_false_when_ordered():
    # north > south -> not inverted
    assert spatial_utils.ns_is_inverted(41.25, 34.95) is False


def test_ns_is_inverted_false_when_equal():
    # north == south -> not inverted (>= is satisfied)
    assert spatial_utils.ns_is_inverted(10.0, 10.0) is False


def test_ns_is_inverted_accepts_numeric_strings():
    # Values arrive from QLineEdit as strings; they must be cast and compared.
    assert spatial_utils.ns_is_inverted("34.95", "41.25") is True
    assert spatial_utils.ns_is_inverted("41.25", "34.95") is False


def test_ns_is_inverted_negative_latitudes_inverted():
    # Southern-Hemisphere inverted case: north=-10 < south=-5 -> inverted.
    assert spatial_utils.ns_is_inverted(-10, -5) is True


def test_ns_is_inverted_negative_latitudes_ordered():
    # north=-5 >= south=-10 -> not inverted.
    assert spatial_utils.ns_is_inverted(-5, -10) is False


def test_ns_is_inverted_false_for_non_numeric():
    assert spatial_utils.ns_is_inverted("abc", 10) is False
    assert spatial_utils.ns_is_inverted(10, "xyz") is False


def test_ns_is_inverted_false_for_empty_string():
    assert spatial_utils.ns_is_inverted("", "10") is False
    assert spatial_utils.ns_is_inverted("10", "") is False


def test_ns_is_inverted_false_for_none():
    assert spatial_utils.ns_is_inverted(None, 10) is False
    assert spatial_utils.ns_is_inverted(10, None) is False
    assert spatial_utils.ns_is_inverted(None, None) is False


# ---------------------------------------------------------------------------
# ns_ordered
# ---------------------------------------------------------------------------

def test_ns_ordered_swaps_when_inverted():
    # Inverted pair is reordered so the larger latitude comes first.
    assert spatial_utils.ns_ordered(34.95, 41.25) == (41.25, 34.95)


def test_ns_ordered_identity_when_ordered():
    # Already ordered pair is returned unchanged.
    assert spatial_utils.ns_ordered(41.25, 34.95) == (41.25, 34.95)


def test_ns_ordered_identity_when_equal():
    # Equal values are returned unchanged.
    assert spatial_utils.ns_ordered(10.0, 10.0) == (10.0, 10.0)


def test_ns_ordered_negative_latitudes_inverted():
    # Southern-Hemisphere inverted case: north=-10, south=-5 -> (-5, -10).
    assert spatial_utils.ns_ordered(-10, -5) == (-5, -10)


def test_ns_ordered_negative_latitudes_ordered():
    # north=-5 >= south=-10 -> unchanged identity.
    assert spatial_utils.ns_ordered(-5, -10) == (-5, -10)


def test_ns_ordered_preserves_multiset_when_swapping():
    north, south = 12.0, 47.0
    result = spatial_utils.ns_ordered(north, south)
    assert sorted(result) == sorted((north, south))
    assert result[0] >= result[1]


def test_ns_ordered_identity_for_non_numeric():
    # Non-castable inputs are returned unchanged, preserving value and type.
    assert spatial_utils.ns_ordered("abc", 10) == ("abc", 10)
    assert spatial_utils.ns_ordered(10, "xyz") == (10, "xyz")


def test_ns_ordered_identity_for_empty_string():
    assert spatial_utils.ns_ordered("", "10") == ("", "10")
    assert spatial_utils.ns_ordered("10", "") == ("10", "")


def test_ns_ordered_identity_for_none():
    assert spatial_utils.ns_ordered(None, 10) == (None, 10)
    assert spatial_utils.ns_ordered(10, None) == (10, None)
    assert spatial_utils.ns_ordered(None, None) == (None, None)


# ===========================================================================
# North/South ordering randomized tests
#
# Randomized coverage for ``ns_ordered`` (backed by ``ns_is_inverted``) across
# the full -90..90 latitude range. The repository does not use a
# property-testing library (e.g. hypothesis is not a dependency), so these tests
# follow the existing plain-pytest convention using the standard-library
# ``random`` module with a fixed seed for reproducibility and many iterations.
# ===========================================================================

# Iteration count for the randomized checks.
NS_ITERATIONS = 200

# Fixed seed keeps failures reproducible while still exercising the input space.
NS_SEED = 20240601

# Full inclusive latitude range for both North and South coordinates.
NS_LAT_MIN = -90.0
NS_LAT_MAX = 90.0


def ns_random_latitude(rng):
    """Return a random latitude across the full -90..90 inclusive range."""
    return rng.uniform(NS_LAT_MIN, NS_LAT_MAX)


# ---------------------------------------------------------------------------
# ns_ordered swaps only when inverted and always preserves the pair
# ---------------------------------------------------------------------------

def test_prop1_ns_ordered_output_is_ordered():
    """For any latitude pair, ns_ordered output has first >= second."""
    rng = random.Random(NS_SEED)
    for _ in range(NS_ITERATIONS):
        north = ns_random_latitude(rng)
        south = ns_random_latitude(rng)
        first, second = spatial_utils.ns_ordered(north, south)
        assert first >= second, (
            "ns_ordered output not ordered for north=%r south=%r -> (%r, %r)"
            % (north, south, first, second)
        )


def test_prop1_ns_ordered_preserves_pair_multiset():
    """For any latitude pair, ns_ordered preserves the multiset {north, south}."""
    rng = random.Random(NS_SEED + 1)
    for _ in range(NS_ITERATIONS):
        north = ns_random_latitude(rng)
        south = ns_random_latitude(rng)
        result = spatial_utils.ns_ordered(north, south)
        assert sorted(result) == sorted((north, south)), (
            "ns_ordered did not preserve the pair for north=%r south=%r -> %r"
            % (north, south, result)
        )


def test_prop1_ns_ordered_identity_when_already_ordered():
    """When north >= south, ns_ordered returns the input unchanged."""
    rng = random.Random(NS_SEED + 2)
    checked = 0
    for _ in range(NS_ITERATIONS):
        a = ns_random_latitude(rng)
        b = ns_random_latitude(rng)
        # Force an already-ordered pair (north >= south).
        north, south = (a, b) if a >= b else (b, a)
        result = spatial_utils.ns_ordered(north, south)
        assert result == (north, south), (
            "ns_ordered mutated an already-ordered pair north=%r south=%r -> %r"
            % (north, south, result)
        )
        checked += 1
    assert checked == NS_ITERATIONS


def test_prop1_ns_ordered_swaps_iff_inverted():
    """ns_ordered swaps exactly when the input is inverted, else identity."""
    rng = random.Random(NS_SEED + 3)
    saw_inverted = False
    saw_ordered = False
    for _ in range(NS_ITERATIONS):
        north = ns_random_latitude(rng)
        south = ns_random_latitude(rng)
        result = spatial_utils.ns_ordered(north, south)
        if north < south:
            saw_inverted = True
            assert result == (south, north), (
                "inverted pair not swapped north=%r south=%r -> %r"
                % (north, south, result)
            )
        else:
            saw_ordered = True
            assert result == (north, south), (
                "ordered pair changed north=%r south=%r -> %r"
                % (north, south, result)
            )
    # Sanity: the randomized run exercised both branches.
    assert saw_inverted and saw_ordered
