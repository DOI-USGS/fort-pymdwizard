#TODO add input handlers for all the types of data we want to handle
import os

import pandas as pd
import geopandas as gpd
import fiona

def read_csv(filepath):
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
        df = pd.read_csv(filepath, parse_dates=True)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, parse_dates=True, encoding='utf8')
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, parse_dates=True, encoding = "ISO-8859-1")
    return df


def read_shp(filepath):
    df = gpd.read_file(filepath)
    c = fiona.open(filepath)
    col_names = list(c.schema['properties'].keys())
    df = df[[c for c in df.columns if c != 'geometry']]
    return df[col_names]


def get_sheet_names(filepath):
    import xlrd as xl
    workbook = xl.open_workbook(filepath)
    return workbook.sheet_names()


def read_excel(filepath, sheet_name):
    df = pd.read_excel(filepath, sheet_name)
    return df


def read_data(filepath, sheet_name=''):
    if filepath.lower().endswith(".csv"):
        return read_csv(filepath)
    elif filepath.lower().endswith(".shp"):
        return read_shp(filepath)
    elif sheet_name:
        return read_excel(filepath, sheet_name)
