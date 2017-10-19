#TODO add input handlers for all the types of data we want to handle
import os

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
import geopandas as gpd
import fiona

def read_csv(filepath, delimiter=','):
    """
    converts a csv, specified by filename, into a pandas dataframe

    Parameters
    ----------
    filepath : string
            Full filepath to the csv to return

    Returns
    -------
    pandas dataframe
    """
    try:
        df = pd.read_csv(filepath, parse_dates=True, delimiter=delimiter)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, parse_dates=True, encoding='utf8', delimiter=delimiter)
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, parse_dates=True, encoding = "ISO-8859-1", delimiter=delimiter)
    return df


def read_shp(filepath):
    df = gpd.read_file(filepath)
    c = fiona.open(filepath)
    col_names = list(c.schema['properties'].keys())

    df = df[[c for c in df.columns if c != 'geometry']]
    df.insert(0, 'Shape', c.schema['geometry'])
    df.insert(0, 'FID', range(df.shape[0]))
    return df


#  taken from http://code.activestate.com/recipes/362715-dbf-reader-and-writer/
def dbfreader(f):
    """Returns an iterator over records in a Xbase DBF file.
    The first row returned contains the field names.
    The second row contains field specs: (type, size, decimal places).
    Subsequent rows contain the data records.
    If a record is marked as deleted, it is skipped.
    File should be opened for binary reads.
    """
    #  See DBF format spec at:
    #     http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT

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


def read_dbf(filepath):
    f = open(filepath, 'rb')
    vat = list(dbfreader(f))
    return pd.DataFrame(vat[2:], columns=[c.decode("utf-8") for c in vat[0]])


def get_sheet_names(filepath):
    import xlrd as xl
    workbook = xl.open_workbook(filepath)
    return workbook.sheet_names()


def read_excel(filepath, sheet_name):
    df = pd.read_excel(filepath, sheet_name)
    return df


def read_data(filepath, sheet_name='', delimiter=','):
    if filepath.lower().endswith(".csv"):
        return read_csv(filepath)
    elif filepath.lower().endswith(".txt"):
        return read_csv(filepath, delimiter)
    elif filepath.lower().endswith(".shp"):
        return read_shp(filepath)
    elif sheet_name:
        return read_excel(filepath, sheet_name)
