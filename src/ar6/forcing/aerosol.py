"""
Module for aerosol forcing functions
"""

import numpy as np

def aerocom_n(x, bc, oc, so2, nh3):
    """ERFari linear in emissions including nitrate

    Inputs
    ------
    x : obj:`numpy.array`
        Time series of aerosol emissions
    bc : float
        Radiative efficiency of black carbon, W m**-2 (TgC yr**-1)**-1
    oc : float
        Radiative efficiency of organic carbon, W m**-2 (TgC yr**-1)**-1
    so2 : float
        Radiative efficiency of sulfate (expressed as SO2 emissions),
        W m**-2 (TgSO2 yr**-1)**-1
    nh3 : float
        Radiative efficiency of nitrate (expressed as NH3 emissions),
        W m**-2 (TgSO2 yr**-1)**-1

    Returns
    -------
    res : obj:`numpy.array`
        Time series of ERFari
    """
    return bc*x[0] + oc*x[1] + so2*x[2] + nh3*x[3]


def ghan(x, beta, n0, n1):
    """ERFaci logarithmic in emissions excluding nitrate.

    Named after Steve Ghan, whose 2013 simple emissions emulator is extremely useful,
    (https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/jgrd.50567),
    and can be emulated again using this very simple formula.

    Inputs
    ------
    x : obj:`numpy.array`
        Time series of aerosol emissions
    beta : float
        Scale factor linking forcing to time series
    n0 : float
        Shape factor for SO2 emissions, W m**-2 (TgSO2 yr**-1)**-1
    n1 : float
        Shape factor for BC+OC emissions, W m**-2 (TgC yr**-1)**-1

    Returns
    -------
    res : obj:`numpy.array`
        Time series of ERFaci
    """
    return -beta*np.log(1 + x[0]/n0 + x[1]/n1)


def shindell(x, beta, n0, n1, n2):
    """ERFaci logarithmic in emissions including nitrate.

    Why is this named after Drew? Possibly due to the AR5 ACCMIP paper, though he was
    not involved in this formulation!

    Inputs
    ------
    x : obj:`numpy.array`
        Time series of aerosol emissions
    beta : float
        Scale factor linking forcing to time series
    n0 : float
        Shape factor for SO2 emissions, W m**-2 (TgSO2 yr**-1)**-1
    n1 : float
        Shape factor for BC+OC emissions, W m**-2 (TgC yr**-1)**-1
    n2 : float
        Shape factor for NH3 emissions, W m**-2 (TgSO2 yr**-1)**-1

    Returns
    -------
    res : obj:`numpy.array`
        Time series of ERFaci
    """
    return -beta*np.log(1 + x[0]/n0 + x[1]/n1 + x[2]/n2)
