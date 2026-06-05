"""Unittests for core.doi_utils"""


from pymdwizard.core import doi_utils


def test_datacite():
    doi = "10.3133/fs20263002"
    citeinfo = doi_utils.get_doi_citation(doi)
    # Verify that title and geoform are populated (don't check exact text as it may change)
    assert citeinfo.title.text is not None
    assert len(citeinfo.title.text) > 0
    assert citeinfo.geoform.text in ["dataset", "publication", "document"]


def test_crossref():
    doi = "https://doi.org/10.1007/s10530-018-1696-1"
    assert (
        doi_utils.get_doi_citation(doi).title.text
        == "Managing an invasive corallimorph at Palmyra Atoll National Wildlife Refuge, Line Islands, Central Pacific"
    )


def test_clean_doi():
    https_doi = "https://doi.org/10.1007/s10530-018-1696-1"
    http_doi = "http://dx.doi.org/10.1007/s10530-018-1696-1"
    doi_doi = "doi.org/10.1007/s10530-018-1696-1"
    just_doi = "10.1007/s10530-018-1696-1"

    assert doi_utils.clean_doi(https_doi) == doi_utils.clean_doi(just_doi)
    assert doi_utils.clean_doi(http_doi) == doi_utils.clean_doi(just_doi)
    assert doi_utils.clean_doi(doi_doi) == doi_utils.clean_doi(just_doi)
