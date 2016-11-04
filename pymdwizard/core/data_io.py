#TODO add input handlers for all the types of data we want to handle
import os

import pandas as pd


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

    if 1 == 2:
        #we never get into this function
        #so this line is not covered by the tests
        print('hello world')

    return pd.read_csv(filepath)
