#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module for reading data from various formats into a Pandas dataframe


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

import struct
import datetime
import decimal
try:
    # Python 2
    from itertools import izip
except ImportError:
    # Python 3
    izip = zip

try:
    xrange
except NameError:
    xrange = range

import pandas as pd
try:
    import geopandas as gpd
    import fiona
except:
    gpd = None
    fiona = None


MAX_ROWS = 1000000

def read_csv(fname, delimiter=','):
    """
    converts a csv, specified by filename, into a pandas dataframe

    Parameters
    ----------
    fname : string
            Full fname to the csv to return
    delimiter : str, optional, defaults to comma
            the character used to delimit the data in a txt file

    Returns
    -------
    pandas dataframe
    """
    try:
        df = pd.read_csv(fname, parse_dates=True, delimiter=delimiter,
                         nrows=MAX_ROWS)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(fname, parse_dates=True, encoding='utf8',
                             delimiter=delimiter, nrows=MAX_ROWS)
        except UnicodeDecodeError:
            df = pd.read_csv(fname, parse_dates=True,
                             encoding="ISO-8859-1", delimiter=delimiter,
                             nrows=MAX_ROWS)

    return df


def read_shp(fname):
    """
    Returns a pandas dataframe of the attribute in a shapefile's dbf
     specified as a file path/name

    Parameters
    ----------
    fname : str
            file path/name to the shapefile being returned

    Returns
    -------
        pandas dataframe
    """
    df = gpd.read_file(fname)
    c = fiona.open(fname)
    list(c.schema['properties'].keys())

    df = df[[c for c in df.columns if c != 'geometry']]
    df.insert(0, 'Shape', c.schema['geometry'])
    df.insert(0, 'FID', range(df.shape[0]))
    return df


def dbfreader(f):
    """Returns an iterator over records in a Xbase DBF file.
    The first row returned contains the field names.
    The second row contains field specs: (type, size, decimal places).
    Subsequent rows contain the data records.
    If a record is marked as deleted, it is skipped.
    File should be opened for binary reads.

    originally taken from:
        http://code.activestate.com/recipes/362715-dbf-reader-and-writer/

    See DBF format spec at:
        http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT
    """

    numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))
    numfields = (lenheader - 33) // 32

    fields = []
    for fieldno in xrange(numfields):
        name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
        name = bytes(name)
        name = name.replace(b'\0', b'')  #  eliminate NULs from string
        fields.append((name, typ, size, deci))
    yield [field[0] for field in fields]
    yield [tuple(field[1:]) for field in fields]

    terminator = f.read(1)
    assert terminator == b'\r'

    fields.insert(0, ('DeletionFlag', 'C', 1, 0))
    fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in fields])
    fmtsiz = struct.calcsize(fmt)
    for i in xrange(numrec):
        record = struct.unpack(fmt, f.read(fmtsiz))
        if record[0] != b' ':
            continue  #  deleted record
        result = []
        for (name, typ, size, deci), value in izip(fields, record):
            value = bytes(value)
            if name == 'DeletionFlag':
                continue
            if typ == b"N":
                value = value.replace(b'\0', b'').lstrip()
                if value == '':
                    value = 0
                elif deci:
                    value = decimal.Decimal(value)
                else:
                    value = int(value)
            if typ == b"C":
                value = value.decode("utf-8")
            elif typ == b'D':
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif typ == b'L':
                value = (value in b'YyTt' and b'T') or \
                        (value in b'NnFf' and b'F') or b'?'
            elif typ == b'F':
                value = float(value)
            result.append(value)
        yield result


def read_dbf(fname):
    """
    Returns a pandas dataframe of the dbf
     specified as a file path/name

    Parameters
    ----------
    fname : str
            file path/name to the dbf being returned

    Returns
    -------
        pandas dataframe
    """
    f = open(fname, 'rb')
    vat = list(dbfreader(f))
    return pd.DataFrame(vat[2:], columns=[c.decode("utf-8") for c in vat[0]])


def get_sheet_names(fname):
    """
    Returns list of sheets in an Excel file

    Parameters
    ----------
    fname : str
            file path/name to the Excel file being returned

    Returns
    -------
    list of strings
    """
    import xlrd as xl
    workbook = xl.open_workbook(fname)
    return workbook.sheet_names()


def read_excel(fname, sheet_name):
    """
    Returns a pandas dataframe of an Excel file and sheet

    Parameters
    ----------
    fname : str
            file path/name to the Excel file
    sheet_name : str

    Returns
    -------
        pandas dataframe
    """
    df = pd.read_excel(fname, sheet_name)
    return df


def read_data(fname, sheet_name='', delimiter=','):
    """
    Returns pandas dataframe from a file (csv, txt, Excel, or shp)

    Parameters
    ----------
    fname : str
            file path/name to the Excel file
    sheet_name : str, optional
            sheet name
    delimiter : str, optional
            the character used to delimit the data in a txt file

    Returns
    -------
        pandas dataframe
    """
    if fname.lower().endswith(".csv"):
        return read_csv(fname)
    elif fname.lower().endswith(".txt"):
        return read_csv(fname, delimiter)
    elif fname.lower().endswith(".shp"):
        return read_shp(fname)
    elif sheet_name:
        return read_excel(fname, sheet_name)

