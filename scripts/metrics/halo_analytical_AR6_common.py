import numpy as np
import metric_constants as const


def halo_analytical_AR6(H, alpha, re, mass):
    ppb2kg = 1e-9*(mass/const.m_air)*const.m_atm
    A = re/ppb2kg*(1+const.halo_ra)

    delT = H*0.
    idelT = H*0.
    rf = H*0.
    agwp = H*0.
    rf = rf+A*np.exp(-H/alpha)
    agwp = agwp+A*alpha*(1-np.exp(-H/alpha))
    for j in np.arange(2):
        delT = delT+A*alpha*const.c[j]*(np.exp(-H/alpha) -
                                        np.exp(-H/const.d[j])) /\
                                   (alpha-const.d[j])
        idelT = idelT+A*alpha*const.c[j] * \
            (alpha*(1-np.exp(-H/(alpha)))-const.d[j] *
             (1-np.exp(-H/const.d[j]))) / \
            (alpha-const.d[j])
    return rf, agwp, delT, idelT
