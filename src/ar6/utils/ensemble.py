"""
Functions for calculating ensemble weightings.
"""

import numpy as np
from .statistics import rmse

def knutti_score(obs, mod, sigma_D=None):
    """Returns a score based on how well models match observations.

    The calculation is based on:
        Knutti et al., A climate model projection weighting scheme accounting for 
        performance and interdependence, Geophys. Res. Lett., 
        https://doi.org/10.1002/2016GL072012, 2017.

    This calculation does not downweight similar models unlike the original Knutti
    paper.

    Inputs
    ------
    obs : np.ndarray
        array of observations of shape (n_obs)
    mod : np.ndarray
        array of model results of shape (n_obs, n_models)
    sigma_D : float or None
        radius of model quality. If not specified use RMSE

    Returns
    -------
    ks : np.ndarray
        array of model scores of shape (n_models)
    """
    samples = mod.shape[1]
    rm_d = np.ones(samples) * np.nan

    for i in range(samples):
        rm_d[i] = rmse(obs, mod[:, i])

    if sigma_D==None:
        sigma_D = np.nanmin(rm_d)
    ks_raw = np.exp(-rm_d**2/sigma_D**2) 

    ks_raw[np.isnan(ks_raw)] = 0
    ks = ks_raw/np.sum(ks_raw)
    return ks


# TODO: is this different to above?
def simple_weight(obs, mod, sigma_D):
    """Applies Gaussian distance weighting with no RMSE step.

    Inputs
    ------
    obs : np.ndarray
        array of observations of shape (n_obs)
    mod : np.ndarray
        array of model results of shape (n_obs, n_models)
    sigma_D : float or None
        radius of model quality. If not specified use RMSE

    Returns
    -------
    ks : np.ndarray
        array of model scores of shape (n_models)
    """

    ks_raw = np.exp(-(mod-obs)**2/sigma_D**2)
    ks_raw[np.isnan(ks_raw)] = 0
    ks = ks_raw/np.sum(ks_raw)
    return ks
