"""
Module for ozone forcing functions
"""

import numpy as np
from ..constants.gases import cl_atoms, br_atoms, fracrel

def eesc(x, specie, anomaly=True):
    """Equivalent effective stratospheric chlorine for ozone depleting compounds.

    Inputs
    ------
    x : obj:`numpy.array`
        Time series of halogenated gas concentrations (parts per trillion)
    specie : string
        Name of the compound, used for looking up properties
    anomaly : bool
        Calculate EESC relative to the first entry in x. If False, return absolute

    Returns
    -------
    res : obj:`numpy.array`
        Time series of EESC, in parts per trillion
    """
    if anomaly:
        x0 = x[0]
    else:
        x0 = 0

    return (
        (
            cl_atoms[specie] * (x-x0) * fracrel[specie]/fracrel['CFC11']
        ) + 45 *
        (
            br_atoms[specie] * (x-x0) * fracrel[specie]/fracrel['CFC11']
        )
    ) * fracrel['CFC11']
