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
from fair.defaults.carbon import a, tau as alpha_co2


def co2_analytical(H, co2=409.85, ch4=1866.3275, n2o=332.091, co2_ra=0.05, d=d, q=q, a=a, alpha_co2=alpha_co2):
    # TODO: Add docstring
    re = meinshausen(np.array([co2+1, ch4, n2o]), np.array([co2, ch4, n2o]), scale_F2x=False)[0] * (1+co2_ra)

    ppm2kg = 1E-6*(molwt.CO2/molwt.AIR)*M_ATMOS
    A = re/ppm2kg  # W/m2/kg

    delT = H*0.
    idelT = H*0.
    rf = H*0.
    agwp = H*0.
    for j in np.arange(2):
        if (j == 0):
            rf = rf+A*a[0]
            agwp = agwp+A*a[0]*H
        delT = delT+A*a[0]*q[j]*(1-np.exp(-H/d[j]))
        idelT = idelT+A*a[0]*q[j]*(H-d[j] * (1-np.exp(-H/d[j])))
        for i in np.arange(1, 4):
            if (j == 0):
                rf = rf+A*a[i]*np.exp(-H/alpha_co2[i])
                agwp = agwp+A*a[i]*alpha_co2[i] *\
                    (1-np.exp(-H/alpha_co2[i]))
            delT = delT+A*a[i]*alpha_co2[i]*q[j] *\
                (np.exp(-H/alpha_co2[i]) -
                 np.exp(-H/d[j]))/(alpha_co2[i]-d[j])
            idelT = idelT+A*a[i]*alpha_co2[i]*q[j] * \
                (alpha_co2[i]*(1-np.exp(-H/alpha_co2[i])) -
                 d[j]*(1-np.exp(-H/d[j]))) / \
                (alpha_co2[i]-d[j])

    return rf, agwp, delT, idelT
