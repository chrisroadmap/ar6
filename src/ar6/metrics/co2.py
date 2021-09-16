"""
Module for calculating metrics from CO2, usually as a baseline to compare other gases.

Author: Bill Collins (UK)
Adapted by Chris Smith
"""

import numpy as np
from .constants import M_ATMOS, M_AIR, M_CO2
from fair.forcing.ghg import meinshausen
from fair.defaults.thermal import q, d
from fair.defaults.carbon import a, tau as alpha_co2


# TODO: make better variable names
def co2_analytical(H, co2=409.85, n2o=332.091, co2_ra=0.05, d=d, q=q, a=a, alpha_co2=alpha_co2):
    """Calculates baseline metrics for a 1 ppm CO2 perturbation.
    
    Inputs:
    -------
    H : float or `np.ndarray`
        time horizon(s) of interest
    co2 : float, optional
        baseline concentrations of CO2, ppmv
    n2o : float, optional
        baseline concentrations of N2O, ppbv
    co2_ra : float, optional
        tropospheric rapid adjustment enhancement of CO2 forcing, expressed as a decimal
    d : `np.ndarray`, optional
        2-element array of fast and slow timescales to climate warming impulse response function
    q : `np.ndarray`, optional
        2-element array of fast and slow contributions to climate warming impulse response function
    a : `np.ndarray`, optional
        4-element array of partition fractions of CO2 atmospheric boxes, slow to fast
    alpha_co2 : `np.ndarray`, optional
        4-element array of time constants of CO2 atmospheric boxes, slow to fast
    
    Returns:
    --------
    (rf, agwp, agtp, iagtp) : tuple of float or `np.ndarray`
        rf : Effective radiative forcing from a 1 ppmv increase in CO2
        agwp : Absolute global warming potential of CO2, W m-2 yr kg-1
        agtp : Absolute global temperature change potential of CO2, K kg-1
        iagtp : Integrated absolute global temperature change potential, K kg-1
    """
    # the CH4 concentration does not affect CO2 forcing, so we hardcode an approximate 2019 value
    re = meinshausen(np.array([co2+1, 1866.3, n2o]), np.array([co2, 1866.3, n2o]), scale_F2x=False)[0] * (1+co2_ra)

    ppm2kg = 1E-6*(M_CO2/M_AIR)*M_ATMOS
    A = re/ppm2kg  # W/m2/kg

    agtp = H*0.
    iagtp = H*0.
    rf = H*0.
    agwp = H*0.
    for j in np.arange(2):
        if (j == 0):
            rf = rf+A*a[0]
            agwp = agwp+A*a[0]*H
        agtp = agtp+A*a[0]*q[j]*(1-np.exp(-H/d[j]))
        iagtp = iagtp+A*a[0]*q[j]*(H-d[j] * (1-np.exp(-H/d[j])))

        for i in np.arange(1, 4):
            if (j == 0):
                rf = rf+A*a[i]*np.exp(-H/alpha_co2[i])
                agwp = agwp+A*a[i]*alpha_co2[i] *\
                    (1-np.exp(-H/alpha_co2[i]))
            agtp = agtp+A*a[i]*alpha_co2[i]*q[j] *\
                (np.exp(-H/alpha_co2[i]) -
                 np.exp(-H/d[j]))/(alpha_co2[i]-d[j])
            iagtp = iagtp+A*a[i]*alpha_co2[i]*q[j] * \
                (alpha_co2[i]*(1-np.exp(-H/alpha_co2[i])) -
                 d[j]*(1-np.exp(-H/d[j]))) / \
                (alpha_co2[i]-d[j])

    return rf, agwp, agtp, iagtp
