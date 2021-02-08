import numpy as np


def co2_forcing_AR6(co2, co2_0, n2o_bar):

    a1 = -2.4e-7  # W/m2/ppm
    b1 = 7.2e-4   # W/m2/ppm
    c1 = -2.1e-4  # W/m2/ppb
    co2_forcing_AR6 = (a1*(co2-co2_0)**2+b1*np.abs(co2-co2_0)+c1*n2o_bar+5.36)\
        * np.log(co2/co2_0)
    return co2_forcing_AR6
