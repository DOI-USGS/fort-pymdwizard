#!/usr/bin/python
# -*- coding: utf8 -*-

"""Tests for the validator North/South ordering check.

Covers the read-only North/South bounding-coordinate ordering check in
``pymdwizard.core.fgdc_utils.validate_xml()``. The FGDC schema constrains each
latitude's range but not the ordering relationship between ``northbc`` and
``southbc``, so an inverted record (``northbc < southbc``) passes schema
validation while being logically invalid. ``validate_xml`` appends one
``(xpath, message, line)`` error per inverted ``idinfo/spdom/bounding`` element.

These are pure-core tests (no PyQt). The repository does not use a
property-testing library (hypothesis is not a dependency), so the randomized
tests follow the existing plain-pytest convention using the standard-library
``random`` module with a fixed seed for reproducibility and many iterations.

Tests craft minimal metadata documents and filter the returned errors to the
North/South ordering message only, so unrelated schema errors from a minimal
document do not affect the assertions.
"""


import random

from lxml import etree

from pymdwizard.core import fgdc_utils


# The exact message substring the validator appends for an inverted N/S pair.
NS_MESSAGE_SUBSTR = (
    "North Bounding Coordinate must be greater than or "
    "equal to the South Bounding Coordinate"
)

# Iteration count for the randomized checks.
ITERATIONS = 150

# Fixed seed keeps failures reproducible while still exercising the input space.
SEED = 20240601

# Full inclusive latitude range for both North and South coordinates.
LAT_MIN = -90.0
LAT_MAX = 90.0


# ---------------------------------------------------------------------------
# Helpers for building minimal metadata documents and filtering N/S errors.
# ---------------------------------------------------------------------------

def _bounding_block(west="-100.0", east="-90.0", north=None, south=None):
    """Return the XML text for one bounding block, omitting None lat/lon."""
    parts = ["    <bounding>"]
    if west is not None:
        parts.append("      <westbc>{}</westbc>".format(west))
    if east is not None:
        parts.append("      <eastbc>{}</eastbc>".format(east))
    if north is not None:
        parts.append("      <northbc>{}</northbc>".format(north))
    if south is not None:
        parts.append("      <southbc>{}</southbc>".format(south))
    parts.append("    </bounding>")
    return "\n".join(parts)


def _make_metadata(boundings):
    """Build a minimal metadata document string with the given bounding blocks.

    ``boundings`` is an iterable of pre-rendered bounding-block strings. The
    surrounding structure is intentionally minimal; tests only assert on the
    North/South ordering error, so other schema errors are irrelevant.
    """
    bounding_xml = "\n".join(boundings)
    return (
        "<metadata>\n"
        "  <idinfo>\n"
        "    <spdom>\n"
        "{}\n"
        "    </spdom>\n"
        "  </idinfo>\n"
        "</metadata>\n"
    ).format(bounding_xml)


def _ns_errors(xml_str):
    """Run validate_xml on the string and return only the N/S ordering errors."""
    errors = fgdc_utils.validate_xml(xml_str)
    return [e for e in errors if NS_MESSAGE_SUBSTR in e[1]]


def _random_latitude(rng):
    """Return a random latitude across the full -90..90 inclusive range."""
    return rng.uniform(LAT_MIN, LAT_MAX)


# ---------------------------------------------------------------------------
# Validator flags inverted records at the bounding location.
# ---------------------------------------------------------------------------

def test_prop5_inverted_records_flagged_once_at_bounding_location():
    """Numeric northbc < southbc yields exactly one N/S error at the bounding
    location, across the full latitude range including negatives."""
    rng = random.Random(SEED)
    saw_negative = False
    for _ in range(ITERATIONS):
        a = _random_latitude(rng)
        b = _random_latitude(rng)
        # Force a strictly inverted pair: north < south.
        low, high = (a, b) if a < b else (b, a)
        if a == b:
            # Nudge to guarantee strict inversion.
            high = low + 0.5
        north, south = low, high
        if north < 0 or south < 0:
            saw_negative = True

        xml_str = _make_metadata([_bounding_block(north=north, south=south)])
        ns_errors = _ns_errors(xml_str)

        assert len(ns_errors) == 1, (
            "expected exactly one N/S error for north=%r south=%r, got %r"
            % (north, south, ns_errors)
        )
        xpath = ns_errors[0][0]
        assert "idinfo/spdom/bounding" in xpath, (
            "N/S error xpath does not reference the bounding location: %r"
            % (xpath,)
        )
    # Sanity: the randomized run exercised Southern-Hemisphere latitudes.
    assert saw_negative


def test_prop5_multiple_boundings_flags_each_inverted_with_index():
    """When multiple bounding blocks exist, each inverted one is flagged with an
    indexed xpath."""
    rng = random.Random(SEED + 10)
    for _ in range(ITERATIONS):
        # First bounding inverted, second ordered.
        n1 = _random_latitude(rng)
        s1 = n1 + rng.uniform(0.1, 10.0)  # strictly inverted (north < south)
        if s1 > LAT_MAX:
            s1 = LAT_MAX
            n1 = s1 - rng.uniform(0.1, 10.0)
        boundings = [
            _bounding_block(north=n1, south=s1),
            _bounding_block(north="50.0", south="10.0"),
        ]
        xml_str = _make_metadata(boundings)
        ns_errors = _ns_errors(xml_str)

        assert len(ns_errors) == 1, (
            "expected one N/S error for two boundings (first inverted), got %r"
            % (ns_errors,)
        )
        xpath = ns_errors[0][0]
        assert "idinfo/spdom/bounding" in xpath
        assert "[1]" in xpath, (
            "expected indexed xpath for multiple boundings, got %r" % (xpath,)
        )


# ---------------------------------------------------------------------------
# Validator raises no false North/South error.
# ---------------------------------------------------------------------------

def test_prop6_ordered_records_produce_no_ns_error():
    """northbc >= southbc (including equal and negatives) yields no N/S error."""
    rng = random.Random(SEED + 1)
    saw_equal = False
    saw_negative = False
    for _ in range(ITERATIONS):
        a = _random_latitude(rng)
        b = _random_latitude(rng)
        # Force an ordered pair: north >= south.
        north, south = (a, b) if a >= b else (b, a)
        # Occasionally test the equal boundary.
        if rng.random() < 0.2:
            south = north
            saw_equal = True
        if north < 0 or south < 0:
            saw_negative = True

        xml_str = _make_metadata([_bounding_block(north=north, south=south)])
        ns_errors = _ns_errors(xml_str)

        assert ns_errors == [], (
            "unexpected N/S error for ordered pair north=%r south=%r: %r"
            % (north, south, ns_errors)
        )
    assert saw_equal and saw_negative


def test_prop6_absent_or_nonnumeric_latitudes_produce_no_ns_error():
    """Absent, empty, or non-numeric latitudes yield no N/S error."""
    rng = random.Random(SEED + 2)
    # Candidate values that should never trigger the numeric N/S comparison.
    non_numeric = ["", "abc", "N/A", "--", "1.2.3", " ", "north"]
    for _ in range(ITERATIONS):
        choice = rng.randint(0, 4)
        if choice == 0:
            # Both latitudes absent.
            block = _bounding_block(north=None, south=None)
        elif choice == 1:
            # North absent, south numeric.
            block = _bounding_block(north=None, south=str(_random_latitude(rng)))
        elif choice == 2:
            # South absent, north numeric.
            block = _bounding_block(north=str(_random_latitude(rng)), south=None)
        elif choice == 3:
            # North non-numeric, south numeric.
            block = _bounding_block(
                north=rng.choice(non_numeric),
                south=str(_random_latitude(rng)),
            )
        else:
            # Both non-numeric.
            block = _bounding_block(
                north=rng.choice(non_numeric),
                south=rng.choice(non_numeric),
            )

        xml_str = _make_metadata([block])
        ns_errors = _ns_errors(xml_str)

        assert ns_errors == [], (
            "unexpected N/S error for absent/non-numeric block %r: %r"
            % (block, ns_errors)
        )


# ---------------------------------------------------------------------------
# Validator North/South check is read-only.
# ---------------------------------------------------------------------------

def _canonical(xml_str):
    """Return a canonical (C14N) serialization of the given XML string."""
    node = etree.fromstring(xml_str.encode("utf-8"))
    return etree.tostring(node, method="c14n")


def test_prop7_validate_xml_does_not_mutate_input():
    """The canonical serialization is identical before and after validate_xml,
    for inverted, ordered, and non-numeric documents alike."""
    rng = random.Random(SEED + 3)
    for _ in range(ITERATIONS):
        a = _random_latitude(rng)
        b = _random_latitude(rng)
        kind = rng.randint(0, 2)
        if kind == 0:
            # Inverted.
            north, south = min(a, b), max(a, b)
            if north == south:
                south = north + 0.5
            block = _bounding_block(north=north, south=south)
        elif kind == 1:
            # Ordered.
            north, south = max(a, b), min(a, b)
            block = _bounding_block(north=north, south=south)
        else:
            # Non-numeric.
            block = _bounding_block(north="abc", south=str(a))

        xml_str = _make_metadata([block])
        before = _canonical(xml_str)

        # validate_xml parses its own tree from the string; the source
        # document representation must remain unchanged (read-only).
        fgdc_utils.validate_xml(xml_str)

        after = _canonical(xml_str)
        assert before == after, (
            "validate_xml altered the document representation for block %r"
            % (block,)
        )


def test_prop7_shared_element_not_mutated_by_validate():
    """Passing a live lxml element to validate_xml leaves that element's
    canonical serialization unchanged (defensive read-only check)."""
    rng = random.Random(SEED + 4)
    for _ in range(ITERATIONS // 3):
        a = _random_latitude(rng)
        b = _random_latitude(rng)
        north, south = min(a, b), max(a, b)
        if north == south:
            south = north + 0.5
        xml_str = _make_metadata([_bounding_block(north=north, south=south)])
        node = etree.fromstring(xml_str.encode("utf-8"))

        before = etree.tostring(node, method="c14n")
        fgdc_utils.validate_xml(node)
        after = etree.tostring(node, method="c14n")

        assert before == after, (
            "validate_xml mutated the shared element for north=%r south=%r"
            % (north, south)
        )


# ---------------------------------------------------------------------------
# Unit tests for the validator check.
# ---------------------------------------------------------------------------

def test_unit_inverted_positive_reports_ns_error():
    """A crafted inverted-N/S bounding element reports the N/S error.

    Uses the motivating report values (North=34.95, South=41.25).
    """
    xml_str = _make_metadata([_bounding_block(north="34.95", south="41.25")])
    ns_errors = _ns_errors(xml_str)

    assert len(ns_errors) == 1
    xpath, message, line = ns_errors[0]
    assert "idinfo/spdom/bounding" in xpath
    assert NS_MESSAGE_SUBSTR in message


def test_unit_inverted_southern_hemisphere_reports_ns_error():
    """A negative-latitude (Southern-Hemisphere) inverted case is flagged.

    north=-50.0 < south=-10.0.
    """
    xml_str = _make_metadata([_bounding_block(north="-50.0", south="-10.0")])
    ns_errors = _ns_errors(xml_str)

    assert len(ns_errors) == 1
    assert "idinfo/spdom/bounding" in ns_errors[0][0]


def test_unit_ordered_reports_no_ns_error():
    """An ordered pair (north > south) reports no N/S error."""
    xml_str = _make_metadata([_bounding_block(north="41.25", south="34.95")])
    assert _ns_errors(xml_str) == []


def test_unit_equal_reports_no_ns_error():
    """Equal latitudes (north == south) report no N/S error."""
    xml_str = _make_metadata([_bounding_block(north="40.0", south="40.0")])
    assert _ns_errors(xml_str) == []


def test_unit_ordered_southern_hemisphere_reports_no_ns_error():
    """Ordered negative latitudes report no N/S error.

    north=-10.0 >= south=-50.0.
    """
    xml_str = _make_metadata([_bounding_block(north="-10.0", south="-50.0")])
    assert _ns_errors(xml_str) == []


def test_unit_missing_latitudes_reports_no_ns_error():
    """Absent northbc/southbc report no N/S error."""
    # Both missing.
    xml_str = _make_metadata([_bounding_block(north=None, south=None)])
    assert _ns_errors(xml_str) == []

    # North missing only.
    xml_str = _make_metadata([_bounding_block(north=None, south="10.0")])
    assert _ns_errors(xml_str) == []

    # South missing only.
    xml_str = _make_metadata([_bounding_block(north="10.0", south=None)])
    assert _ns_errors(xml_str) == []


def test_unit_nonnumeric_latitudes_reports_no_ns_error():
    """Non-numeric latitudes report no N/S error."""
    xml_str = _make_metadata([_bounding_block(north="abc", south="12.0")])
    assert _ns_errors(xml_str) == []

    xml_str = _make_metadata([_bounding_block(north="", south="")])
    assert _ns_errors(xml_str) == []


def test_unit_multiple_boundings_indexes_inverted_error():
    """With multiple boundings, only the inverted one is flagged, indexed."""
    boundings = [
        _bounding_block(north="41.25", south="34.95"),  # ordered
        _bounding_block(north="34.95", south="41.25"),  # inverted
    ]
    xml_str = _make_metadata(boundings)
    ns_errors = _ns_errors(xml_str)

    assert len(ns_errors) == 1
    xpath = ns_errors[0][0]
    assert "idinfo/spdom/bounding" in xpath
    assert "[2]" in xpath


# ===========================================================================
# Controlled-vocabulary keyword validation (2.2.1)
# ===========================================================================
#
# validate_xml checks theme/place keywords against their named USGS thesaurus
# and appends a "controlled vocabulary" error per keyword group containing
# unrecognized terms. These tests patch the thesaurus_utils boundary
# (get_thesauri_lookup + _term_is_known) so no network access occurs, and
# filter the returned errors to the controlled-vocabulary message.

from pymdwizard.core import thesaurus_utils

CV_MESSAGE_SUBSTR = "controlled vocabulary"

_CV_LOOKUP = {"USGS Thesaurus": 2, "Common geographic areas": 4}


def _keywords_metadata(themekt=None, themekeys=(), placekt=None, placekeys=()):
    """Build a minimal metadata document with theme and/or place keywords."""
    blocks = []
    if themekt is not None:
        theme = ["    <theme>", "      <themekt>{}</themekt>".format(themekt)]
        theme += ["      <themekey>{}</themekey>".format(k) for k in themekeys]
        theme.append("    </theme>")
        blocks.append("\n".join(theme))
    if placekt is not None:
        place = ["    <place>", "      <placekt>{}</placekt>".format(placekt)]
        place += ["      <placekey>{}</placekey>".format(k) for k in placekeys]
        place.append("    </place>")
        blocks.append("\n".join(place))
    keywords_xml = "\n".join(blocks)
    return (
        "<metadata>\n"
        "  <idinfo>\n"
        "    <keywords>\n"
        "{}\n"
        "    </keywords>\n"
        "  </idinfo>\n"
        "</metadata>\n"
    ).format(keywords_xml)


def _cv_errors(xml_str):
    """Run validate_xml and return only the controlled-vocabulary errors."""
    errors = fgdc_utils.validate_xml(xml_str)
    return [e for e in errors if CV_MESSAGE_SUBSTR in e[1]]


def test_cv_invalid_theme_keyword_reported(mocker):
    """An unrecognized theme keyword is reported against its thesaurus."""
    mocker.patch.object(
        thesaurus_utils, "get_thesauri_lookup", return_value=dict(_CV_LOOKUP)
    )
    mocker.patch.object(
        thesaurus_utils,
        "_term_is_known",
        side_effect=lambda thcode, kw: kw == "biology",
    )

    xml_str = _keywords_metadata(
        themekt="USGS Thesaurus", themekeys=["biology", "notarealterm"]
    )
    cv_errors = _cv_errors(xml_str)

    assert len(cv_errors) == 1
    xpath, message, _line = cv_errors[0]
    assert "idinfo/keywords/theme/themekt" in xpath
    assert "notarealterm" in message
    assert "USGS Thesaurus" in message
    # The recognized keyword is not reported.
    assert "biology" not in message


def test_cv_all_valid_keywords_no_error(mocker):
    """When every keyword is recognized, no controlled-vocabulary error."""
    mocker.patch.object(
        thesaurus_utils, "get_thesauri_lookup", return_value=dict(_CV_LOOKUP)
    )
    mocker.patch.object(thesaurus_utils, "_term_is_known", return_value=True)

    xml_str = _keywords_metadata(
        themekt="USGS Thesaurus", themekeys=["biology", "hydrology"]
    )
    assert _cv_errors(xml_str) == []


def test_cv_free_text_thesaurus_skipped(mocker):
    """A free-text themekt ('None') is skipped: no lookup, no error."""
    lookup = mocker.patch.object(thesaurus_utils, "get_thesauri_lookup")
    known = mocker.patch.object(thesaurus_utils, "_term_is_known")

    xml_str = _keywords_metadata(
        themekt="None", themekeys=["whatever", "anything"]
    )
    assert _cv_errors(xml_str) == []
    lookup.assert_not_called()
    known.assert_not_called()


def test_cv_service_unreachable_no_false_positive(mocker):
    """If the thesaurus service is unreachable (lookup None), no error is
    reported rather than falsely flagging keywords as invalid."""
    mocker.patch.object(
        thesaurus_utils, "get_thesauri_lookup", return_value=None
    )
    known = mocker.patch.object(thesaurus_utils, "_term_is_known")

    xml_str = _keywords_metadata(
        themekt="USGS Thesaurus", themekeys=["biology", "notarealterm"]
    )
    assert _cv_errors(xml_str) == []
    # With no lookup, per-term checks are never attempted.
    known.assert_not_called()


def test_cv_invalid_place_keyword_reported(mocker):
    """An unrecognized place keyword is reported against its thesaurus."""
    mocker.patch.object(
        thesaurus_utils, "get_thesauri_lookup", return_value=dict(_CV_LOOKUP)
    )
    mocker.patch.object(
        thesaurus_utils,
        "_term_is_known",
        side_effect=lambda thcode, kw: kw == "Colorado",
    )

    xml_str = _keywords_metadata(
        placekt="Common geographic areas",
        placekeys=["Colorado", "Notaplace"],
    )
    cv_errors = _cv_errors(xml_str)

    assert len(cv_errors) == 1
    xpath, message, _line = cv_errors[0]
    assert "idinfo/keywords/place/placekt" in xpath
    assert "Notaplace" in message
