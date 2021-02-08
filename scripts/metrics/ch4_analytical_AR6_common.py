import numpy as np
import metric_constants as const
from ch4_forcing_AR6 import ch4_forcing_AR6


def ch4_analytical_AR6(H):
    re = ch4_forcing_AR6(const.ch4+1., const.ch4, const.n2o) *\
             (1+const.ch4_ra)
    print("ra =", const.ch4_ra)
    ppb2kg = 1e-9*(const.m_ch4/const.m_air)*const.m_atm
    A = (1.+const.f_ch4_o3+const.f_ch4_h2o)*re/ppb2kg

    delT = H*0.
    idelT = H*0.
    rf = H*0.
    agwp = H*0.

    rf = rf+A*np.exp(-H/(const.alpha_ch4))
    agwp = agwp+A*const.alpha_ch4*(1-np.exp(-H/const.alpha_ch4))
    for j in np.arange(2):
        delT = delT+A*const.alpha_ch4*const.c[j] *\
            (np.exp(-H/(const.alpha_ch4)) -
             np.exp(-H/const.d[j]))/(const.alpha_ch4-const.d[j])
        idelT = idelT+A*const.alpha_ch4*const.c[j] * \
            (const.alpha_ch4*(1-np.exp(-H/(const.alpha_ch4))) -
             const.d[j]*(1-np.exp(-H/const.d[j]))) / \
            (const.alpha_ch4-const.d[j])
    return rf, agwp, delT, idelT
