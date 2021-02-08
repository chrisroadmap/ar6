import numpy as np


def ch4_forcing_AR6(ch4, ch4_0, n2o_bar):

    a3 = -1.3e-6  # W/m2/ppb
    b3 = -8.2e-6  # W/m2/ppb
    ch4_bar = (ch4_0+ch4)/2.
    ch4_forcing_etminan = (a3*ch4_bar + b3*n2o_bar + 0.043) * \
        (np.sqrt(ch4)-np.sqrt(ch4_0))
    return ch4_forcing_etminan
