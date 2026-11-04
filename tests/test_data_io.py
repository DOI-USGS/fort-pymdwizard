"""Unittests for core.data_io"""




import pymdwizard


def test_read_csv():
    fname = "tests/data/iris.csv"
    df = pymdwizard.core.data_io.read_csv(fname)
    assert df.shape == (150, 5)
    assert list(df.columns) == [
        u"sepal_length",
        u"sepal_width",
        u"petal_length",
        u"petal_width",
        u"species",
    ]


# ---------------------------------------------------------------------------
# File Geodatabase (.gdb); gdb_path is a fixture in conftest.py
# ---------------------------------------------------------------------------


def test_get_gdb_layer_names(gdb_path):
    layers = pymdwizard.core.data_io.get_gdb_layer_names(gdb_path)
    assert sorted(layers) == ["roads", "wells"]


def test_get_gdb_oid_column(gdb_path):
    oid = pymdwizard.core.data_io.get_gdb_oid_column(gdb_path, "wells")
    assert oid == "OBJECTID"


def test_read_gdb_named_layer(gdb_path):
    df = pymdwizard.core.data_io.read_gdb(gdb_path, layer="wells")
    # Object ID first, then Shape, then the attribute fields; no geometry
    # column and no generated FID.
    assert list(df.columns) == ["OBJECTID", "Shape", "name", "depth"]
    assert df["OBJECTID"].tolist() == [1, 2, 3]
    assert set(df["Shape"]) == {"Point"}
    assert df["name"].tolist() == ["A", "B", "C"]
    assert df["depth"].tolist() == [10, 20, 30]


def test_read_gdb_first_layer_by_default(gdb_path):
    first = pymdwizard.core.data_io.get_gdb_layer_names(gdb_path)[0]
    df = pymdwizard.core.data_io.read_gdb(gdb_path)
    expected = pymdwizard.core.data_io.read_gdb(gdb_path, layer=first)
    assert df.equals(expected)


def test_read_data_dispatches_gdb(gdb_path):
    df = pymdwizard.core.data_io.read_data(gdb_path)
    assert df.columns[0] == "OBJECTID"
    assert df.columns[1] == "Shape"
