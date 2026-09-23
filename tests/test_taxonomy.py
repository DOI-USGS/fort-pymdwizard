"""Unittests for the taxonomy module

All ITIS web calls funnel through taxonomy._get_xml, which returns a parsed
lxml tree. The offline unit tests mock _get_xml with a small captured-shape XML
document and exercise the DataFrame/list shaping plus the pure-logic helpers.
The richer end-to-end assertions against the live ITIS service are preserved as
@pytest.mark.network tests.
"""

import pandas as pd
import pytest

from pymdwizard.core import taxonomy, xml_utils


# ---------------------------------------------------------------------------
# Offline: pure logic
# ---------------------------------------------------------------------------

def test_to_lower():
    assert taxonomy._to_lower(["Hello", "WORLD"]) == ["hello", "world"]


# ---------------------------------------------------------------------------
# Offline: mocked _get_xml for the search/shaping path
# ---------------------------------------------------------------------------

# ITIS wraps results in the ax21 namespace. A commonNames record carries
# commonName / language / tsn children.
_ITIS_NS = "http://data.itis_service.itis.usgs.gov/xsd"

_COMMON_NAMES_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<response xmlns:ax21="{_ITIS_NS}">
  <ax21:commonNames>
    <ax21:commonName>brown bear</ax21:commonName>
    <ax21:language>English</ax21:language>
    <ax21:tsn>180546</ax21:tsn>
  </ax21:commonNames>
  <ax21:commonNames>
    <ax21:commonName>grizzly bear</ax21:commonName>
    <ax21:language>English</ax21:language>
    <ax21:tsn>180546</ax21:tsn>
  </ax21:commonNames>
</response>
"""


def test_search_by_common_name_dataframe_mocked(mocker):
    """search_by_common_name shapes the ITIS commonNames records into a
    DataFrame with the documented columns. Network is mocked."""
    tree = xml_utils.string_to_node(_COMMON_NAMES_XML.encode("utf-8"))
    mocker.patch.object(taxonomy, "_get_xml", return_value=tree)

    df = taxonomy.search_by_common_name("brown bear")
    assert list(df.columns) == ["commonName", "language", "tsn"]
    assert "brown bear" in list(df.commonName)


def test_search_by_common_name_as_list_mocked(mocker):
    """as_dataframe=False returns a list of dicts with the same keys."""
    tree = xml_utils.string_to_node(_COMMON_NAMES_XML.encode("utf-8"))
    mocker.patch.object(taxonomy, "_get_xml", return_value=tree)

    results = taxonomy.search_by_common_name("brown bear", as_dataframe=False)
    assert list(results[0].keys()) == ["commonName", "language", "tsn"]
    assert results[0]["commonName"] == "brown bear"


# ---------------------------------------------------------------------------
# Live integration checks (network)
# ---------------------------------------------------------------------------

@pytest.mark.network
def test_search_common_name_live():
    df = taxonomy.search_by_common_name("brown bear")
    assert list(df.columns) == ["commonName", "language", "tsn"]

    results = taxonomy.search_by_common_name("brown bear", as_dataframe=False)
    assert list(results[0].keys()) == ["commonName", "language", "tsn"]

    taxonomy.pd = None
    results = taxonomy.search_by_common_name("brown bear", as_dataframe=True)
    assert list(results[0].keys()) == ["commonName", "language", "tsn"]
    taxonomy.pd = pd


@pytest.mark.network
def test_search_scientific_name_live():
    expected = [
        "tsn", "author", "combinedName", "kingdom",
        "unitInd1", "unitInd2", "unitInd3", "unitInd4",
        "unitName1", "unitName2", "unitName3", "unitName4",
    ]
    df = taxonomy.search_by_scientific_name("gulo gulo")
    assert list(df.columns) == expected

    results = taxonomy.search_by_scientific_name("gulo gulo", as_dataframe=False)
    assert list(results[0].keys()) == expected


@pytest.mark.network
def test_full_hierarchy_from_tsn_live():
    expected = [
        "tsn", "author", "parentName", "parentTsn", "rankName", "taxonName",
    ]
    df = taxonomy.get_full_hierarchy_from_tsn(180694)
    assert list(df.columns) == expected

    results = taxonomy.get_full_hierarchy_from_tsn(180694, as_dataframe=False)
    assert results[0]["taxonName"] == "Animalia"

    no_species = taxonomy.get_full_hierarchy_from_tsn(
        180694, as_dataframe=False, include_children=False
    )
    assert no_species[-1]["rankName"] == "Genus"

    has_species = taxonomy.get_full_hierarchy_from_tsn(
        180694, as_dataframe=False, include_children=True
    )
    assert has_species[-1]["rankName"] == "Species"

    df = taxonomy.get_full_hierarchy_from_tsn(180694, include_children=False)
    assert df[df.rankName == "Species"].empty

    df = taxonomy.get_full_hierarchy_from_tsn(180694, include_children=True)
    assert not df[df.rankName == "Species"].empty


@pytest.mark.network
def test_get_common_names_tsn_live():
    df = taxonomy.get_common_names_tsn(202385)
    assert list(df.columns) == ["commonName", "language", "tsn"]

    results = taxonomy.get_common_names_tsn(202385, as_dataframe=False)
    assert list(results[0].keys()) == ["commonName", "language", "tsn"]


@pytest.mark.network
def test_gen_fgdc_taxonomy_live():
    fgdc_taxonomy = taxonomy.gen_fgdc_taxoncl(tsns=[180694])
    assert fgdc_taxonomy.tag == "taxoncl"
    assert list(fgdc_taxonomy)[1].text == "Animalia"

    # Add a plant, so that the top level is Domain==Eukaryota.
    fgdc_taxonomy = taxonomy.gen_fgdc_taxoncl(tsns=[180694, 183437])
    assert list(fgdc_taxonomy)[1].text == "Eukaryota"

    # Add a bacteria, so that the top level is Domain==Life.
    fgdc_taxonomy = taxonomy.gen_fgdc_taxoncl(tsns=[180694, 183437, 951930])
    assert list(fgdc_taxonomy)[1].text == "Life"

    fgdc_taxonomy = taxonomy.gen_taxonomy_section(
        keywords=["test", "test2"], tsns=[180694, 183437]
    )
    assert fgdc_taxonomy.tag == "taxonomy"
