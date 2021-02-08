
import numpy as np
import metric_constants as const
from co2_forcing_AR6 import co2_forcing_AR6


def co2_analytical_AR6(H):
    re = co2_forcing_AR6(const.co2+1., const.co2, const.n2o)*(1+const.co2_ra)

    ppm2kg = 1E-6*(const.m_co2/const.m_air)*const.m_atm
    A = re/ppm2kg  # W/m2/kg

    delT = H*0.
    idelT = H*0.
    rf = H*0.
    agwp = H*0.
    for j in np.arange(2):
        if (j == 0):
            rf = rf+A*const.a[0]
            agwp = agwp+A*const.a[0]*H
        delT = delT+A*const.a[0]*const.c[j]*(1-np.exp(-H/const.d[j]))
        idelT = idelT+A*const.a[0]*const.c[j]*(H-const.d[j] *
                                               (1-np.exp(-H/const.d[j])))
        for i in np.arange(1, 4):
            if (j == 0):
                rf = rf+A*const.a[i]*np.exp(-H/const.alpha_co2[i])
                agwp = agwp+A*const.a[i]*const.alpha_co2[i] *\
                    (1-np.exp(-H/const.alpha_co2[i]))
            delT = delT+A*const.a[i]*const.alpha_co2[i]*const.c[j] *\
                (np.exp(-H/const.alpha_co2[i]) -
                 np.exp(-H/const.d[j]))/(const.alpha_co2[i]-const.d[j])
            idelT = idelT+A*const.a[i]*const.alpha_co2[i]*const.c[j] * \
                (const.alpha_co2[i]*(1-np.exp(-H/const.alpha_co2[i])) -
                 const.d[j]*(1-np.exp(-H/const.d[j]))) / \
                (const.alpha_co2[i]-const.d[j])

    return rf, agwp, delT, idelT
