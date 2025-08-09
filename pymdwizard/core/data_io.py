#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module for reading data from various formats into a Pandas dataframe


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import struct
import datetime
import decimal

# Non-standard python libraries.
try:
    import pandas as pd
    import numpy as np
    import geopandas as gpd
    import fiona
    import laspy
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import utils
except ImportError as err:
    raise ImportError(err, __file__)


def read_csv(fname, delimiter=","):
    """
    Description:
        Converts a CSV, specified by filename, into a pandas DataFrame.

    Args:
        fname (str): Full path to the CSV file to read.
        delimiter (str, optional): The character used to delimit the data in
            the file. Defaults to comma.

    Returns:
        df (pandas.DataFrame): A pandas DataFrame containing the CSV data.
    """

    # Get the maximum number of rows to read from settings
    max_rows = int(utils.get_setting("maxrows", 1000000))

    # Read the CSV file into a DataFrame.
    try:
        # Attempt to read the CSV file with default encoding.
        df = pd.read_csv(
            fname,
            parse_dates=True,
            delimiter=delimiter,
            nrows=max_rows,
            na_filter=False,
            comment="#",
        )
    except UnicodeDecodeError:
        try:
            # If default encoding fails, try reading with UTF-8 encoding.
            df = pd.read_csv(
                fname,
                parse_dates=True,
                encoding="utf8",
                delimiter=delimiter,
                nrows=max_rows,
                na_filter=False,
                comment="#",
            )
        except UnicodeDecodeError:
            # If UTF-8 encoding fails, try reading with ISO-8859-1 encoding.
            df = pd.read_csv(
                fname,
                parse_dates=True,
                encoding="ISO-8859-1",
                delimiter=delimiter,
                nrows=max_rows,
                na_filter=False,
                comment="#",
            )

    return df


def read_shp(fname):
    """
    Description:
        Returns a pandas DataFrame of the attributes in a shapefile's DBF,
        specified as a file path/name.

    Args:
        fname (str): Full path to the shapefile to read.

    Returns:
        df (pandas.DataFrame): A pandas DataFrame containing the attributes.
    """

    # Read the shapefile into a GeoDataFrame.
    df = gpd.read_file(fname)

    # Open the shapefile to access its schema.
    c = fiona.open(fname)

    # List the attribute names (keys) in the shapefile's schema.
    list(c.schema["properties"].keys())

    # Exclude the 'geometry' column from the DataFrame.
    df = df[[c for c in df.columns if c != "geometry"]]

    # Insert the geometry type at the beginning of the DataFrame.
    df.insert(0, "Shape", c.schema["geometry"])

    # Add a 'FID' column if it doesn't exist.
    if not "FID" in df.columns:
        df.insert(0, "FID", range(df.shape[0]))

    return df


def dbfreader(f):
    """
    Description:
        Returns an iterator over records in an Xbase DBF file.
        The first row returned contains the field names.

        The second row contains field specs: (type, size, decimal places).
        Subsequent rows contain the data records.

        If a record is marked as deleted, it is skipped.
        The file should be opened for binary reads.

    Args:
        f: A file object opened for binary reading.

    Returns:
        An iterator yielding records from the DBF file.

    Notes:
        originally taken from:
            http://code.activestate.com/recipes/362715-dbf-reader-and-writer/

        See DBF format spec at:
            http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT
    """

    # Unpack the header to get the number of records and header length.
    numrec, lenheader = struct.unpack("<xxxxLH22x", f.read(32))
    numfields = (lenheader - 33) // 32

    # Read field specifications
    fields = []
    for fieldno in range(numfields):
        name, typ, size, deci = struct.unpack("<11sc4xBB14x", f.read(32))
        name = bytes(name)
        name = name.replace(b"\0", b"")  # eliminate NULL from str
        fields.append((name, typ, size, deci))

    # Yield field names and field specifications
    yield [field[0] for field in fields]
    yield [tuple(field[1:]) for field in fields]

    terminator = f.read(1)
    assert terminator == b"\r"

    # Add the deletion flag as the first field.
    fields.insert(0, ("DeletionFlag", "C", 1, 0))
    fmt = "".join(["%ds" % fieldinfo[2] for fieldinfo in fields])
    fmtsiz = struct.calcsize(fmt)

    # Process each record.
    for i in range(numrec):
        record = struct.unpack(fmt, f.read(fmtsiz))
        if record[0] != b" ":
            continue  #  deleted record
        result = []
        for (name, typ, size, deci), value in zip(fields, record):
            value = bytes(value)
            if name == "DeletionFlag":
                continue

            # Process the value based on its type.
            if typ == b"N":
                value = value.replace(b"\0", b"").lstrip()
                if value == "":
                    value = 0
                elif deci:
                    value = decimal.Decimal(value)
                else:
                    value = int(value)
            if typ == b"C":
                value = value.decode("utf-8")
            elif typ == b"D":
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif typ == b"L":
                value = (
                    (value in b"YyTt" and b"T") or (value in b"NnFf" and b"F")
                    or b"?")
            elif typ == b"F":
                value = float(value)
            result.append(value)
        yield result


def read_dbf(fname):
    """
    Description:
        Returns a pandas dataframe of the DBF specified as a file path/name.

    Args:
        fname (str): Full path to the DBF to read.

    Returns:
        pandas.DataFrame: DataFrame containing the records from the DBF file.
    """

    # Open the specified DBF file in binary read mode
    f = open(fname, "rb")
    vat = list(dbfreader(f))

    # Create a DataFrame:
    # - Use the third element of `vat` as data (rows)
    # - Use the first element of `vat` as column names
    return pd.DataFrame(vat[2:], columns=[c.decode("utf-8") for c in vat[0]])


def get_sheet_names(fname):
    """
    Description:
        Returns a list of sheet names in an Excel file.

    Args:
        fname (str): Full path to the Excel file.

    Returns:
        list (str): List of sheet names in the Excel file.

    """

    # Load the Excel file using pandas.
    workbook = pd.ExcelFile(fname)

    # Return the list of sheet names
    return workbook.sheet_names


def read_excel(fname, sheet_name):
    """
    Description:
        Returns a pandas DataFrame of an Excel file and sheet.

    Args:
        fname (str): Full path to the Excel file.
        sheet_name (str): Name of the sheet to read from the Excel file.

    Returns:
        pandas.DataFrame: DataFrame containing the data from the specified
            sheet.
    """

    # Check the file extension to determine the appropriate engine.
    if fname.endswith(".xlsx") or fname.endswith(".xlsm"):
        # Read the specified sheet using 'openpyxl' engine for newer formats.
        df = pd.read_excel(fname, sheet_name, engine='openpyxl')
    else:
        # Read the specified sheet using the default engine for older formats.
        df = pd.read_excel(fname, sheet_name)

    return df


def read_las(fname):
    """
    Description:
        Returns a pandas DataFrame of attributes from a LAS file.

    Args:
        fname (str): Full path to the LAS file.

    Returns:
        pandas.DataFrame: DataFrame containing point attributes from the LAS
            file.
    """

    # Get the maximum number of rows to read from the settings.
    max_rows = int(utils.get_setting("maxrows", 1000000))

    # Open the LAS file.
    las = laspy.open(fname)

    # Extract dimension names from the LAS header.
    dims = [dim.name for dim in las.header.point_format]

    # Read the first chunk of points from the LAS file.
    for points in las.chunk_iterator(max_rows):
        break

    # Create a dictionary to store point data arrays.
    point_data = {dim: np.array(points[dim]) for dim in dims}
    
    # Apply scaling and offsets to X, Y, Z dimensions.
    header = las.header
    point_data["X"] = point_data["X"] * header.x_scale + header.x_offset
    point_data["Y"] = point_data["Y"] * header.y_scale + header.y_offset
    point_data["Z"] = point_data["Z"] * header.z_scale + header.z_offset

    # Create a DataFrame from the point data dictionary.
    df = pd.DataFrame(point_data)

    return df


def read_data(fname, sheet_name="", delimiter=","):
    """
    Description:
        Returns a pandas DataFrame from a file (csv, txt, Excel, or shp).

    Args:
        fname (str): Full path to the file.
        sheet_name (str, optional): Name of the sheet to read from the file
        delimiter (str, optional): Delimiter to use in the file
            (default is an empty string).
        delimiter (str, optional): The character used to delimit the data in a
            txt file.

    Returns:
        pandas.DataFrame: DataFrame containing the data from the file.
    """

    # Check the file extension and call the respective read function.
    if fname.lower().endswith(".csv"):
        return read_csv(fname)
    elif fname.lower().endswith(".txt"):
        return read_csv(fname, delimiter)
    elif fname.lower().endswith(".shp"):
        return read_shp(fname)
    elif fname.lower().endswith(".las") or fname.lower().endswith(".laz"):
        return read_las(fname)
    elif sheet_name:
        return read_excel(fname, sheet_name)

    raise ValueError("Unsupported file format or no sheet name provided.")


def sniff_nodata(series):
    """
    Description:
        Attempt to guess the nodata value associated with a pandas Series.

    Args:
        series (pandas.Series): The series from which to identify the nodata
            value.

    Returns:
        str or None: The nodata placeholder found in the series, or None if
            not found.
    """

    # Get the unique values in the series.
    uniques = series.uniques()

    # List of known nodata values to check against
    nodata_values = [
        "#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN", "-nan",
        "1.#IND", "1.#QNAN", "N/A", "NA", "NULL", "NaN", "n/a", "nan",
        "null", -9999, "-9999", "", "Nan"
    ]

    # Loop through the known nodata values and see if any are present
    for nd in nodata_values:
        if nd in uniques:  # Check if the nodata value is in uniques
            return nd  # Return the first matched nodata value

    return None  # Return None if no nodata value is found


def clean_nodata(series, nodata=None):
    """
    Description:
        Given a series, remove the values that match the specified nodata
        value and convert it to an int or float if possible.

    Args:
        series (pandas.Series): The series from which to remove nodata values.
        nodata (string, int, or float, optional): The nodata placeholder to
            remove from the series.

    Returns:
        pandas.Series: A cleaned series with nodata values removed and
            converted if possible.
    """

    # Return the original series if no nodata value is specified.
    if nodata is None:
        return series

    # Filter out the values matching nodata.
    clean_series = series[series != nodata]

    # Attempt to convert the cleaned series to integer type.
    try:
        clean_series = clean_series.astype("int64")
    except ValueError:
        try:
            clean_series = clean_series.astype("float64")
        except ValueError:
            # Keep it as-is if conversion fails
            pass

    return clean_series
