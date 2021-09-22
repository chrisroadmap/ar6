import numpy as np
from .co2 import co2_analytical
from .constants import M_ATMOS, M_CO2, M_C
from fair.defaults.thermal import q, d

def carbon_cycle_adjustment(H, agtp, co2=409.85, n2o=332.091, co2_ra=0.05, d=d, q=q):
    """Calculates adjustment to metrics based on carbon cycle feedback
    
    Inputs:
    -------
    H : `np.ndarray` of float
        reguarly spaced time horizons of interest, yr
    agtp : `np.ndarray` of float
        Unadjusted Absolute Global Temperature Change Potential evaluated at each time horizon of H
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

    Returns:
    --------
    (rf_cc, agwp_cc, agtp_cc) : tuple of `np.ndarray`
        rf_cc : Increase in effective radiative forcing due to carbon cycle adjustment
        agwp : Increase in absolute global warming potential due to carbon cycle adjustment, W m-2 yr kg-1
        agtp : Increase in absolute global temperature change potential due to carbon cycle adjustment, K kg-1
    """
    dts = H[1]
    rf_co2, agwp_co2, agtp_co2, iagtp_co2 = co2_analytical(H, co2=co2, n2o=n2o, co2_ra=co2_ra, d=d, q=q)

    agtp_cc = H*0.
    agwp_cc = H*0.
    rf_cc = H*0.
    F_CO2 = H*0.
    a = np.array([0.6368, 0.3322, 0.0310])  # Gasser et al. 2017
    alpha = np.array([2.376, 30.14, 490.1])

    gamma = 3.015*1E12  # kgCO2/yr/K  Gasser et al. 2017
    r_f = H*0.
    r_f[0] = np.sum(a)/dts
    for i in np.arange(0, 3):
        r_f = r_f-(a[i]/alpha[i])*np.exp(-H/alpha[i])

    for j in np.arange(H.size):
        for i in np.arange(j+1):
            F_CO2[j] = F_CO2[j]+agtp[i]*gamma*r_f[j-i]*dts
    for j in np.arange(H.size):
        for i in np.arange(j+1):
            rf_cc[j] = rf_cc[j]+F_CO2[i]*rf_co2[j-i]*dts * \
                (M_CO2/M_C)
            agwp_cc[j] = agwp_cc[j]+F_CO2[i]*agwp_co2[j-i]*dts * \
                (M_CO2/M_C)
            agtp_cc[j] = agtp_cc[j]+F_CO2[i]*agtp_co2[j-i]*dts * \
                (M_CO2/M_C)
    return rf_cc, agwp_cc, agtp_cc
