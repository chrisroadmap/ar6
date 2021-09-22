"""
Module for calculating metrics from generic halogens.

Author: Bill Collins (UK)
Adapted by Chris Smith
"""

import numpy as np
from .constants import M_ATMOS, M_AIR
from fair.defaults.thermal import q, d


def halogen_analytical(H, alpha, re, mass, d=d, q=q, halogen_ra=0):
    """Calculates metrics for a 1 ppt perturbation from halogenated gas.
    
    Inputs:
    -------
    H : float or `np.ndarray`
        time horizon(s) of interest
    alpha : float
        atmospheric lifetime, years
    re : float
        radiative efficiency, W m-2 ppb-1
    mass : float
        molecular mass, kg mol-1
    d : `np.ndarray`, optional
        2-element array of fast and slow timescales to climate warming impulse response function
    q : `np.ndarray`, optional
        2-element array of fast and slow contributions to climate warming impulse response function
    halogen_ra : float, optional
        tropospheric rapid adjustment enhancement of halogen forcing
    
    Returns:
    --------
    (rf, agwp, agtp, iagtp) : tuple of float or `np.ndarray`
        rf : Effective radiative forcing from a 1 ppbv increase in CH4
        agwp : Absolute global warming potential of CH4, W m-2 yr kg-1
        agtp : Absolute global temperature change potential of CH4, K kg-1
        iagtp : Integrated absolute global temperature change potential, K kg-1
    """
    ppb2kg = 1e-9*(mass/M_AIR)*M_ATMOS
    A = re/ppb2kg*(1+halogen_ra)

    agtp = H*0.
    iagtp = H*0.
    rf = H*0.
    agwp = H*0.
    rf = rf+A*np.exp(-H/alpha)
    agwp = agwp+A*alpha*(1-np.exp(-H/alpha))
    for j in np.arange(2):
        agtp = agtp+A*alpha*q[j]*(np.exp(-H/alpha) -
                                        np.exp(-H/d[j])) /\
                                   (alpha-d[j])
        iagtp = iagtp+A*alpha*q[j] * \
            (alpha*(1-np.exp(-H/(alpha)))-d[j] *
             (1-np.exp(-H/d[j]))) / \
            (alpha-d[j])
    return rf, agwp, agtp, iagtp
