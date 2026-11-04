"""Unittests for core.data_io"""



import shutil

import pytest
from lxml import etree

from pymdwizard.core import xml_utils

POLARBEARS_FIXTURE = "tests/data/USGS_ASC_PolarBears_FGDC.xml"

xml_str = """<cntinfo>
  <cntperp>
    <cntper>Colin Talbert</cntper>
    <cntorg>U.S. Geological Survey, Southwest Region</cntorg>
  </cntperp>
  <cntpos>Ecologist</cntpos>
  <cntaddr>
    <addrtype>Mailing</addrtype>
    <address>2150 Centre Avenue Bldg C</address>
    <city>Fort Collins</city>
    <state>CO</state>
    <postal>80526</postal>
  </cntaddr>
</cntinfo>
"""

parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")
element = etree.fromstring(xml_str, parser=parser)


def test_node_to_dict():
    result = xml_utils.node_to_dict(element)
    assert result["fgdc_cntperp"]["fgdc_cntper"] == "Colin Talbert"


@pytest.mark.skip(reason="ScienceBase integration has been removed from the GUI")
def test_url_read():
    url = "https://www.sciencebase.gov/catalog/file/get/57d8779de4b090824ff9acfb?f=__disk__e1%2F7c%2Fa7%2Fe17ca734bf9ffd9ae0abeaaf0da208d457f72b3c&allowOpen=true"
    md = xml_utils.XMLRecord(url)
    assert md.metadata.idinfo.citation.citeinfo.geoform.text == "Raster Digital Data Set"


def test_open_save(tmp_path):
    # Operate on a copy in tmp_path so the committed fixture is never mutated
    # (save() reserializes the whole file, which otherwise dirties the tree).
    fname = str(tmp_path / "record.xml")
    shutil.copy(POLARBEARS_FIXTURE, fname)

    md = xml_utils.XMLRecord(fname)
    assert md.metadata.idinfo.citation.citeinfo.geoform.text == "Tabular Digital Data"
    md.metadata.idinfo.citation.citeinfo.geoform.text = "testing"
    md.save()

    # Re-open the saved copy and confirm the edit round-tripped to disk.
    md = xml_utils.XMLRecord(fname)
    new_geoform = md.metadata.idinfo.citation.citeinfo.geoform.text

    assert new_geoform == "testing"


def test_find_replace():
    # Read-only test: replace_string mutates the in-memory tree but never
    # calls save(), so reading directly from the fixture is safe.
    fname = POLARBEARS_FIXTURE
    md = xml_utils.XMLRecord(fname)
    assert len(md.metadata.find_string("asc", ignorecase=True)) == 7
    assert len(md.metadata.find_string("asc", ignorecase=False)) == 0
    assert len(md.metadata.find_string("ASC")) == 7

    assert md.metadata.replace_string("Polar Bear", "Honey Badger", deep=False) == 0
    assert md.metadata.replace_string("Polar Bear", "Honey Badger") == 4
    assert "Honey Badger" in md.metadata.idinfo.citation.citeinfo.title.text
    assert (
        md.metadata.idinfo.descript.abstract.replace_string("polar", "big white") == 4
    )
    assert md.metadata.idinfo.descript.abstract.text.count("polar") == 0

    md = xml_utils.XMLRecord(fname)
    assert (
        md.metadata.idinfo.descript.abstract.replace_string(
            "polar", "big white", maxreplace=2
        )
        == 2
    )
    assert md.metadata.idinfo.descript.abstract.text.count("polar") == 2


# ---------------------------------------------------------------------------
# content_diff: detects leaf content present in the original but dropped from
# the produced tree (used to warn about content the GUI form cannot represent).
# ---------------------------------------------------------------------------


def _node(xml_string):
    """Parse an XML string into an lxml element for the diff tests."""
    return xml_utils.string_to_node(xml_string)


def test_content_diff_identical_is_empty():
    tree = _node(
        "<metadata><idinfo><descript>"
        "<abstract>Hello</abstract></descript></idinfo></metadata>"
    )
    assert xml_utils.content_diff(tree, tree) == []


def test_content_diff_detects_dropped_section():
    original = _node(
        "<metadata>"
        "<idinfo><descript><abstract>Hello</abstract></descript></idinfo>"
        "<spdoinfo><direct>Vector</direct></spdoinfo>"
        "</metadata>"
    )
    # Produced tree lost the entire spdoinfo section.
    produced = _node(
        "<metadata>"
        "<idinfo><descript><abstract>Hello</abstract></descript></idinfo>"
        "</metadata>"
    )

    dropped = dict(xml_utils.content_diff(original, produced))
    assert dropped == {"metadata/spdoinfo/direct": ["Vector"]}


def test_content_diff_reports_specific_lost_repeat():
    # Three keywords in, two out: the diff should name the one lost value,
    # not merely report that a keyword went missing.
    original = _node(
        "<metadata><idinfo><keywords><theme>"
        "<themekey>alpha</themekey>"
        "<themekey>beta</themekey>"
        "<themekey>gamma</themekey>"
        "</theme></keywords></idinfo></metadata>"
    )
    produced = _node(
        "<metadata><idinfo><keywords><theme>"
        "<themekey>alpha</themekey>"
        "<themekey>beta</themekey>"
        "</theme></keywords></idinfo></metadata>"
    )

    dropped = dict(xml_utils.content_diff(original, produced))
    assert dropped == {
        "metadata/idinfo/keywords/theme/themekey": ["gamma"]
    }


def test_content_diff_detects_dropped_attribute():
    original = _node("<metadata><customext units='meters'>99</customext></metadata>")
    produced = _node("<metadata><customext>99</customext></metadata>")

    dropped = dict(xml_utils.content_diff(original, produced))
    assert dropped == {"metadata/customext/@units": ["meters"]}


def test_content_diff_ignores_additions_and_reordering():
    original = _node(
        "<metadata>"
        "<idinfo><descript><abstract>A</abstract><purpose>P</purpose>"
        "</descript></idinfo></metadata>"
    )
    # Same content, reordered, plus an extra element the form added.
    produced = _node(
        "<metadata>"
        "<idinfo><descript><purpose>P</purpose><abstract>A</abstract>"
        "</descript></idinfo><metainfo><metstdn>FGDC</metstdn></metainfo>"
        "</metadata>"
    )

    # Nothing from the original is missing, so no drops are reported even
    # though order changed and content was added.
    assert xml_utils.content_diff(original, produced) == []


def test_content_diff_accepts_element_trees():
    # content_diff should accept ElementTree inputs (what fname_to_node
    # returns), not only Elements.
    original = etree.ElementTree(
        _node("<metadata><spdoinfo><direct>Vector</direct></spdoinfo></metadata>")
    )
    produced = etree.ElementTree(_node("<metadata></metadata>"))

    dropped = dict(xml_utils.content_diff(original, produced))
    assert dropped == {"metadata/spdoinfo/direct": ["Vector"]}


# ---------------------------------------------------------------------------
# content_changes: separates content that is gone ("dropped") from content
# the form kept in a different form ("rewritten"), so genuine losses can be
# shown first and normalizations treated as a lesser matter.
# ---------------------------------------------------------------------------


def test_content_changes_identical_is_empty():
    tree = _node("<metadata><metainfo><metstdn>FGDC</metstdn></metainfo></metadata>")
    assert xml_utils.content_changes(tree, tree) == ([], [])


def test_content_changes_replaced_value_is_rewritten_not_dropped():
    # The metadata standard name is rewritten to its canonical wording by the
    # form: nothing is lost, so it must not be reported as dropped.
    original = _node(
        "<metadata><metainfo><metstdn>FGDC Biological Data Profile of the "
        "CSDGM</metstdn></metainfo></metadata>"
    )
    produced = _node(
        "<metadata><metainfo><metstdn>FGDC Biological Data Profile of the "
        "Content Standard for Digital Geospatial Metadata</metstdn>"
        "</metainfo></metadata>"
    )

    dropped, rewritten = xml_utils.content_changes(original, produced)

    assert dropped == []
    assert rewritten == [
        (
            "metadata/metainfo/metstdn",
            [
                (
                    "FGDC Biological Data Profile of the CSDGM",
                    "FGDC Biological Data Profile of the Content Standard "
                    "for Digital Geospatial Metadata",
                )
            ],
        )
    ]


def test_content_changes_missing_value_is_dropped():
    original = _node(
        "<metadata><customext units='meters'>99</customext></metadata>"
    )
    produced = _node("<metadata></metadata>")

    dropped, rewritten = xml_utils.content_changes(original, produced)

    assert rewritten == []
    assert dict(dropped) == {
        "metadata/customext": ["99"],
        "metadata/customext/@units": ["meters"],
    }


def test_content_changes_splits_a_mixed_path():
    # Two keywords in, one different keyword out: one is rewritten (paired in
    # order), the unpaired one is dropped.
    original = _node(
        "<metadata><theme><themekey>a</themekey><themekey>b</themekey>"
        "</theme></metadata>"
    )
    produced = _node(
        "<metadata><theme><themekey>c</themekey></theme></metadata>"
    )

    dropped, rewritten = xml_utils.content_changes(original, produced)

    assert rewritten == [("metadata/theme/themekey", [("a", "c")])]
    assert dropped == [("metadata/theme/themekey", ["b"])]


def test_content_diff_still_reports_replaced_values_as_missing():
    # content_diff keeps its original contract: any original value without an
    # equal counterpart is "missing", whether or not something replaced it.
    original = _node("<metadata><a>old</a></metadata>")
    produced = _node("<metadata><a>new</a></metadata>")

    assert xml_utils.content_diff(original, produced) == [
        ("metadata/a", ["old"])
    ]
