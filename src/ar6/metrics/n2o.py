"""
Module for calculating metrics from N2O.

Author: Bill Collins (UK)
Adapted by Chris Smith
"""

import numpy as np
from .constants import M_ATMOS, M_AIR, M_N2O
from fair.forcing.ghg import meinshausen
from fair.defaults.thermal import q, d


# TODO: make better variable names
def n2o_analytical(H, co2=409.85, ch4=1866.3275, n2o=332.091, n2o_ra=0.07, n2o_o3=5.5e-4, f_n2o_ch4=-1.7, ch4_ra=-0.14, ch4_o3=1.4e-4, ch4_h2o=0.00004, d=d, q=q, alpha_n2o=109):
    """Calculates metrics for a 1 ppb N2O perturbation.
    
    Inputs:
    -------
    H : float or `np.ndarray`
        time horizon(s) of interest
    co2 : float, optional
        baseline concentrations of CO2, ppmv
    ch4: float, optional
        baseline concentrations of CH4, ppbv
    n2o : float, optional
        baseline concentrations of N2O, ppbv
    n2o_ra : float, optional
        tropospheric rapid adjustment enhancement of N2O forcing
    n2o_o3 : float, optional
        radiative efficiency increase of N2O emissions due to O3 formation, W m-2 (ppb N2O)-1
    f_n2o_ch4 : float, optional
        feedback change in methane lifetime due to N2O emissions, (ppb CH4) (ppb N2O)-1
    ch4_ra : float, optional
        tropospheric rapid adjustment enhancement of CH4 forcing
    ch4_o3 : float, optional
        radiative efficiency increase of CH4 emissions due to O3 formation, W m-2 (ppb CH4)-1
    ch4_h2o : float, optional
        radiative efficiency increase of CH4 emissions due to stratospheric H2O formation, W m-2 (ppb CH4)-1 
    d : `np.ndarray`, optional
        2-element array of fast and slow timescales to climate warming impulse response function
    q : `np.ndarray`, optional
        2-element array of fast and slow contributions to climate warming impulse response function
    alpha_n2o : float
        perturbation lifetime of N2O, years
    
    Returns:
    --------
    (rf, agwp, agtp, iagtp) : tuple of float or `np.ndarray`
        rf : Effective radiative forcing from a 1 ppbv increase in CH4
        agwp : Absolute global warming potential of CH4, W m-2 yr kg-1
        agtp : Absolute global temperature change potential of CH4, K kg-1
        iagtp : Integrated absolute global temperature change potential, K kg-1
    """
    re_n2o = meinshausen(np.array([co2, ch4, n2o+1]), np.array([co2, ch4, n2o]), scale_F2x=False)[2] * (1+n2o_ra) + n2o_o3
    re_ch4 = meinshausen(np.array([co2, ch4+1, n2o]), np.array([co2, ch4, n2o]), scale_F2x=False)[1] * (1+ch4_ra) + ch4_o3+ch4_h2o
    ppb2kg = 1e-9*(M_N2O/M_AIR)*M_ATMOS
# Add in a component for the destruction of methane from AR5 8.SM.11.3.3
    A = (re_n2o+f_n2o_ch4*re_ch4)/ppb2kg

    agtp = H*0.
    iagtp = H*0.
    rf = H*0.
    agwp = H*0.
    rf = rf+A*np.exp(-H/alpha_n2o)
    agwp = agwp+A*alpha_n2o*(1-np.exp(-H/alpha_n2o))
    for j in np.arange(2):
        agtp = agtp+A*alpha_n2o*q[j]*(np.exp(-H/alpha_n2o) -
                                                  np.exp(-H/d[j])) /\
                                             (alpha_n2o-d[j])
        iagtp = iagtp+A*alpha_n2o*q[j] * \
            (alpha_n2o*(1-np.exp(-H/(alpha_n2o))) -
             d[j]*(1-np.exp(-H/d[j]))) / \
            (alpha_n2o-d[j])

    return rf, agwp, agtp, iagtp
