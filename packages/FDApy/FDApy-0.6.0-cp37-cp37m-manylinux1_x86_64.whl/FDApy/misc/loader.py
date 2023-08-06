#!/usr/bin/python3.7
# -*-coding:utf8 -*

"""
Module for the definition of different loaders for FunctionalData types.

This modules is used to defined different loaders to load common data files
(such as csv, ts, ...) into an object of the class DenseFunctionalData,
IrregularFunctionalData or MultivariateFunctionalData.
"""
import numpy as np
import pandas as pd

from FDApy.representation.functional_data import (DenseFunctionalData,
                                                  IrregularFunctionalData)


###############################################################################
# Loader for csv
def read_csv(filepath, **kwargs):
    """Read a comma-separated values (csv) file into Functional Data.

    Build a DenseFunctionalData or IrregularFunctionalData object upon a csv
    file passed as parameter.

    Notes
    -----
    It is assumed that the data are unidimensional. And so, it will not be
    checked.

    Parameters
    ----------
    filepath: str
        Any valid string path is acceptable.
    **kwargs:
        Keywords arguments to passed to the pd.read_csv function.

    Return
    ------
    obj: DenseFunctionalData or IrregularFunctionalData
        The loaded csv file.

    """
    data = pd.read_csv(filepath, **kwargs)

    try:
        all_argvals = data.columns.astype(np.int64)
    except TypeError:
        all_argvals = np.arange(0, len(data.columns))

    if not data.isna().values.any():
        obj = read_csv_dense(data, all_argvals)
    else:
        obj = read_csv_irregular(data, all_argvals)
    return obj


def read_csv_dense(data, argvals):
    """Load a csv file into a DenseFunctionalData object.

    Parameters
    ----------
    data: pd.DataFrame
        Input dataframe
    argvals: np.ndarray
        An array of argvals

    Returns
    -------
    obj: DenseFunctionalData
        The loaded csv file

    """
    argvals = {'input_dim_0': argvals}
    values = np.array(data)
    return DenseFunctionalData(argvals, values)


def read_csv_irregular(data, argvals):
    """Load a csv file into an IrregularFunctionalData object.

    Parameters
    ----------
    data: pd.DataFrame
        Input dataframe
    argvals: np.ndarray
        An array of argvals

    Returns
    -------
    obj: IrregularFunctionalData
        The loaded csv file

    """
    argvals = {'input_dim_0': {idx: np.array(argvals[~np.isnan(row)])
                               for idx, row in enumerate(data.values)}}
    values = {idx: row[~np.isnan(row)] for idx, row in enumerate(data.values)}
    return IrregularFunctionalData(argvals, values)
