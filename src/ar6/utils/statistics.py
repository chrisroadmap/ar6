"""
Helpful functions oft used for stats
"""

import numpy as np
import wquantiles


def rmse(obs, mod):
    """Calculate root mean squared error of a time series.

    Inputs
    ------
    obs : np.ndarray
        array of observations
    mod : np.ndarray
        array of modelled values

    Returns
    -------
    rmse : float
        root mean squared error
    """
    return np.sqrt(np.sum((obs-mod)**2)/len(obs))


def weighted_percentile(a, w, q):
    if isinstance(q, (list, tuple, np.ndarray)):
        result = []
        for iq in q:
            result.append(wquantiles.quantile(a, w, iq))
    else:
        result = wquantiles.quantile(a, w, q)
    return result

