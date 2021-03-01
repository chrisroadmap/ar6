"""
Module for calculating metrics from CO2, usually as a baseline to compare other gases.

Author: Bill Collins (UK)
Adapted by Chris Smith
"""

import numpy as np
from fair.constants import molwt
from fair.constants.general import M_ATMOS
from fair.forcing.ghg import meinshausen
from fair.defaults.thermal import q, d


def ch4_analytical(H, co2=409.85, ch4=1866.3275, n2o=332.091, ch4_ra=-0.14, f_ch4_o3=0.29, f_ch4_h2o=-0.1, d=d, q=q, alpha_ch4=11.8):
    re = meinshausen(np.array([co2, ch4+1, n2o]), np.array([co2, ch4, n2o]), scale_F2x=False)[1] * (1+ch4_ra)
    ppb2kg = 1e-9*(molwt.C/molwt.AIR)*M_ATMOS
    A = (1.+f_ch4_o3+f_ch4_h2o)*re/ppb2kg

    delT = H*0.
    idelT = H*0.
    rf = H*0.
    agwp = H*0.

    rf = rf+A*np.exp(-H/(alpha_ch4))
    agwp = agwp+A*alpha_ch4*(1-np.exp(-H/alpha_ch4))
    for j in np.arange(2):
        delT = delT+A*alpha_ch4*q[j] *\
            (np.exp(-H/(alpha_ch4)) -
             np.exp(-H/d[j]))/(alpha_ch4-d[j])
        idelT = idelT+A*alpha_ch4*q[j] * \
            (alpha_ch4*(1-np.exp(-H/(alpha_ch4))) -
             d[j]*(1-np.exp(-H/d[j]))) / \
            (alpha_ch4-d[j])
    return rf, agwp, delT, idelT
