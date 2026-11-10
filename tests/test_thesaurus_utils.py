# -*- coding: utf8 -*-
"""Unit tests for core.thesaurus_utils (controlled-vocabulary keyword check).

The 2.2.1 feature validates theme/place keywords against their named USGS
thesaurus. All web access funnels through utils.requests_pem_get, so these
tests mock that single boundary (via a fake response with a .json() method)
and exercise the logic and its three-state return contract:

    []   -> free text, known-broken thesaurus, or every keyword recognized
    [..] -> the unrecognized keywords
    None -> check could not be performed (unknown thesaurus / service down)

None being distinct from [] matters: callers skip reporting on None rather
than falsely implying "all valid" when the service is unreachable.
"""

import pytest

from pymdwizard.core import thesaurus_utils


class _FakeResponse:
    """Minimal stand-in for a requests.Response with a .json() payload."""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def _patch_get(mocker, side_effect=None, return_value=None):
    """Patch the single network primitive used by thesaurus_utils."""
    return mocker.patch.object(
        thesaurus_utils.utils,
        "requests_pem_get",
        side_effect=side_effect,
        return_value=return_value,
    )


# A representative thesaurus.php payload and the lookup it produces.
_VOCAB_PAYLOAD = {
    "vocabulary": [
        {"name": "USGS Thesaurus", "thcode": 2},
        {"name": "Common geographic areas", "thcode": 4},
    ]
}
_LOOKUP = {"USGS Thesaurus": 2, "Common geographic areas": 4}


# ---------------------------------------------------------------------------
# is_free_text
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value", [None, "None", "none", "NONE", "  None  "])
def test_is_free_text_true(value):
    """None and the literal 'None' (any case, surrounding whitespace) are
    treated as free text."""
    assert thesaurus_utils.is_free_text(value) is True


@pytest.mark.parametrize(
    "value", ["USGS Thesaurus", "Common geographic areas", "", "   "]
)
def test_is_free_text_false(value):
    """Real thesaurus names are not free text. Note an empty/whitespace name
    is NOT free text either -- it falls through to the lookup (where it will
    not be found, yielding None = 'cannot check' rather than an error)."""
    assert thesaurus_utils.is_free_text(value) is False


# ---------------------------------------------------------------------------
# get_thesauri_lookup
# ---------------------------------------------------------------------------

def test_get_thesauri_lookup_parses_vocabulary(mocker):
    _patch_get(mocker, return_value=_FakeResponse(_VOCAB_PAYLOAD))
    assert thesaurus_utils.get_thesauri_lookup() == _LOOKUP


def test_get_thesauri_lookup_service_error_returns_none(mocker):
    _patch_get(mocker, side_effect=Exception("boom"))
    assert thesaurus_utils.get_thesauri_lookup() is None


def test_get_thesauri_lookup_unexpected_shape_returns_none(mocker):
    _patch_get(mocker, return_value=_FakeResponse({"unexpected": True}))
    assert thesaurus_utils.get_thesauri_lookup() is None


# ---------------------------------------------------------------------------
# _term_is_known
# ---------------------------------------------------------------------------

def test_term_is_known_matches_preferred_term(mocker):
    _patch_get(mocker, return_value=_FakeResponse([{"term": {"name": "Biology"}}]))
    # Match is case-insensitive against the preferred term name.
    assert thesaurus_utils._term_is_known(2, "biology") is True


def test_term_is_known_matches_non_preferred_alias(mocker):
    payload = [{"term": {"name": "Hydrology"}, "uf": [{"name": "water science"}]}]
    _patch_get(mocker, return_value=_FakeResponse(payload))
    # The keyword matches a "used-for" (uf) alias, not the preferred term.
    assert thesaurus_utils._term_is_known(2, "Water Science") is True


def test_term_is_known_no_match_returns_false(mocker):
    _patch_get(mocker, return_value=_FakeResponse([{"term": {"name": "Biology"}}]))
    assert thesaurus_utils._term_is_known(2, "notarealterm") is False


def test_term_is_known_empty_response_returns_false(mocker):
    _patch_get(mocker, return_value=_FakeResponse([]))
    assert thesaurus_utils._term_is_known(2, "anything") is False


def test_term_is_known_service_error_returns_none(mocker):
    _patch_get(mocker, side_effect=Exception("boom"))
    assert thesaurus_utils._term_is_known(2, "biology") is None


# ---------------------------------------------------------------------------
# find_invalid_keywords - the three-state contract
# ---------------------------------------------------------------------------

def test_find_invalid_free_text_returns_empty(mocker):
    """Free-text thesaurus -> no check, no network call."""
    spy = _patch_get(mocker)
    assert thesaurus_utils.find_invalid_keywords("None", ["anything"]) == []
    spy.assert_not_called()


def test_find_invalid_unknown_thesaurus_returns_none():
    """Thesaurus name not in the lookup -> None (cannot check)."""
    result = thesaurus_utils.find_invalid_keywords(
        "Not A Real Thesaurus", ["biology"], lookup=_LOOKUP
    )
    assert result is None


def test_find_invalid_broken_thesaurus_returns_empty():
    """Known-broken thcode is skipped (returns [] rather than hitting the
    broken endpoint)."""
    broken_code = next(iter(thesaurus_utils.BROKEN_THESAURUS_THCODES))
    lookup = {"Broken Thesaurus": broken_code}
    result = thesaurus_utils.find_invalid_keywords(
        "Broken Thesaurus", ["anything"], lookup=lookup
    )
    assert result == []


def test_find_invalid_all_valid_returns_empty(mocker):
    """Every keyword recognized -> []."""
    mocker.patch.object(thesaurus_utils, "_term_is_known", return_value=True)
    result = thesaurus_utils.find_invalid_keywords(
        "USGS Thesaurus", ["biology", "hydrology"], lookup=_LOOKUP
    )
    assert result == []


def test_find_invalid_reports_unrecognized_keywords(mocker):
    """Unrecognized keywords are returned; recognized ones are not."""
    def fake_known(thcode, kw):
        return kw == "biology"

    mocker.patch.object(
        thesaurus_utils, "_term_is_known", side_effect=fake_known
    )
    result = thesaurus_utils.find_invalid_keywords(
        "USGS Thesaurus", ["biology", "notarealterm", "alsofake"], lookup=_LOOKUP
    )
    assert result == ["notarealterm", "alsofake"]


def test_find_invalid_service_failure_midcheck_returns_none(mocker):
    """If a single term lookup fails (None), the whole check aborts to None
    rather than reporting a partial/misleading result."""
    mocker.patch.object(thesaurus_utils, "_term_is_known", return_value=None)
    result = thesaurus_utils.find_invalid_keywords(
        "USGS Thesaurus", ["biology"], lookup=_LOOKUP
    )
    assert result is None


def test_find_invalid_skips_empty_keywords(mocker):
    """Empty/None keyword values are skipped, not treated as invalid."""
    mocker.patch.object(thesaurus_utils, "_term_is_known", return_value=True)
    result = thesaurus_utils.find_invalid_keywords(
        "USGS Thesaurus", ["biology", "", None], lookup=_LOOKUP
    )
    assert result == []
