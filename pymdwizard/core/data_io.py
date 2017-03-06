#TODO add input handlers for all the types of data we want to handle
import os

import pandas as pd
import geopandas as gpd

from  osgeo import ogr, osr

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

    return pd.read_csv(filepath)


def read_shp(filepath):
    df = gpd.read_file(filepath)
    return df[[c for c in df.columns if c != 'geometry']]

def read_data(filepath):
    if filepath.lower().endswith(".csv"):
        return read_csv(filepath)
    elif filepath.lower().endswith(".shp"):
        return read_shp(filepath)