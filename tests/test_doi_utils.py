"""Unittests for core.doi_utils

get_doi_citation tries CrossRef first, then falls back to DataCite. The offline
tests mock those two boundary functions and assert the XML the transform builds.
Live end-to-end checks are marked @pytest.mark.network.
"""

import pytest

from pymdwizard.core import doi_utils


# ---------------------------------------------------------------------------
# clean_doi - pure logic, no network
# ---------------------------------------------------------------------------

def test_clean_doi():
    https_doi = "https://doi.org/10.1007/s10530-018-1696-1"
    http_doi = "http://dx.doi.org/10.1007/s10530-018-1696-1"
    doi_doi = "doi.org/10.1007/s10530-018-1696-1"
    just_doi = "10.1007/s10530-018-1696-1"

    assert doi_utils.clean_doi(https_doi) == doi_utils.clean_doi(just_doi)
    assert doi_utils.clean_doi(http_doi) == doi_utils.clean_doi(just_doi)
    assert doi_utils.clean_doi(doi_doi) == doi_utils.clean_doi(just_doi)


# ---------------------------------------------------------------------------
# get_doi_citation - mocked CrossRef / DataCite (offline)
# ---------------------------------------------------------------------------

# Minimal citeproc-json style dict as returned by get_doi_citation_crossref.
_FAKE_CROSSREF = {
    "author": [{"literal": "Jane Doe"}, {"given": "John", "family": "Roe"}],
    "published": "2018",
    "title": "Managing an invasive corallimorph at Palmyra Atoll",
    "geoform": "publication",
    "pubplace": "n/a",
    "publisher": "Springer",
    "URL": "https://doi.org/10.1007/s10530-018-1696-1",
}

# Minimal dict as returned by get_doi_citation_datacite (USGS dataset).
_FAKE_DATACITE = {
    "author": [{"literal": "USGS Author"}],
    "published": "2020",
    "title": "Polar bear locations",
    "geoform": "dataset",
    "pubplace": "n/a",
    "publisher": "U.S. Geological Survey",
    "URL": "https://doi.org/10.5066/xyz",
}


def test_get_doi_citation_crossref_mocked(mocker):
    """When CrossRef succeeds, its data drives the citeinfo output."""
    mocker.patch.object(
        doi_utils, "get_doi_citation_crossref", return_value=dict(_FAKE_CROSSREF)
    )

    citeinfo = doi_utils.get_doi_citation("10.1007/s10530-018-1696-1")

    assert citeinfo.title.text == \
        "Managing an invasive corallimorph at Palmyra Atoll"
    assert citeinfo.geoform.text == "publication"
    # First author present as an origin node.
    origins = [n.text for n in citeinfo.xpath("origin")]
    assert "Jane Doe" in origins
    # given/family author is assembled into a literal name.
    assert "John Roe" in origins


def test_get_doi_citation_datacite_fallback_mocked(mocker):
    """When CrossRef raises, get_doi_citation falls back to DataCite."""
    mocker.patch.object(
        doi_utils,
        "get_doi_citation_crossref",
        side_effect=ValueError("crossref miss"),
    )
    mocker.patch.object(
        doi_utils, "get_doi_citation_datacite", return_value=dict(_FAKE_DATACITE)
    )

    citeinfo = doi_utils.get_doi_citation("10.5066/xyz")

    assert citeinfo.title.text == "Polar bear locations"
    assert citeinfo.geoform.text == "dataset"


def test_get_doi_citation_both_fail_returns_none(mocker):
    """If both providers fail, get_doi_citation returns None rather than raise."""
    mocker.patch.object(
        doi_utils,
        "get_doi_citation_crossref",
        side_effect=ValueError("crossref miss"),
    )
    mocker.patch.object(
        doi_utils,
        "get_doi_citation_datacite",
        side_effect=ValueError("datacite miss"),
    )

    assert doi_utils.get_doi_citation("10.9999/nope") is None


# ---------------------------------------------------------------------------
# Live integration checks (network)
# ---------------------------------------------------------------------------

@pytest.mark.network
def test_datacite_live():
    doi = "10.3133/fs20263002"
    citeinfo = doi_utils.get_doi_citation(doi)
    assert citeinfo.title.text is not None
    assert len(citeinfo.title.text) > 0
    assert citeinfo.geoform.text in ["dataset", "publication", "document"]


@pytest.mark.network
def test_crossref_live():
    doi = "https://doi.org/10.1007/s10530-018-1696-1"
    citeinfo = doi_utils.get_doi_citation(doi)
    assert citeinfo.title.text == (
        "Managing an invasive corallimorph at Palmyra Atoll National "
        "Wildlife Refuge, Line Islands, Central Pacific"
    )
