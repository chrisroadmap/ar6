"""
Module for calculating metrics from generic halogens.

Author: Bill Collins (UK)
Adapted by Chris Smith
"""

import numpy as np
from fair.constants import molwt
from fair.constants.general import M_ATMOS
from fair.defaults.thermal import q, d


def halogen_analytical(H, alpha, re, mass, halogen_ra=0):
    ppb2kg = 1e-9*(mass/molwt.AIR)*M_ATMOS
    A = re/ppb2kg*(1+halogen_ra)

    delT = H*0.
    idelT = H*0.
    rf = H*0.
    agwp = H*0.
    rf = rf+A*np.exp(-H/alpha)
    agwp = agwp+A*alpha*(1-np.exp(-H/alpha))
    for j in np.arange(2):
        delT = delT+A*alpha*q[j]*(np.exp(-H/alpha) -
                                        np.exp(-H/d[j])) /\
                                   (alpha-d[j])
        idelT = idelT+A*alpha*q[j] * \
            (alpha*(1-np.exp(-H/(alpha)))-d[j] *
             (1-np.exp(-H/d[j]))) / \
            (alpha-d[j])
    return rf, agwp, delT, idelT
