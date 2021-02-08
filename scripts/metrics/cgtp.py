#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from co2_analytical_AR6_common import co2_analytical_AR6
from ch4_analytical_AR6_common import ch4_analytical_AR6
from halo_analytical_AR6_common import halo_analytical_AR6
#from ccycle_gasser import ccycle_gasser


alpha_cfc11 = 45.0
alpha_hfc32 = 5.2
alpha_n2o = 121.0

a = np.array([0.2173, 0.2240, 0.2824, 0.2763])  # Joos et al. 2013
# a = np.array([0.2173, 0.2240, 0.2824, 0.])  # Joos et al. 2013
alpha = np.array([0.,   394.4, 36.54, 4.304])   # Joos et al. 2013

dts = 0.1
c = np.array([0.631, 0.429])  # Boucher and Reddy 2008
d = np.array([8.4, 409.5])    # Boucher and Reddy 2008

lamb = np.sum(c)
M_hfc32 = 52.03  # GWP_review_molarmass.prn

H = np.arange(0, 100.+dts, dts)

#Hodnebrog 2020
re_hfc32 = 0.11144
alpha_hfc32 = 5.4
mass_hfc32 = 0.05203

rf_co2, agwp_co2, delT_co2, idelT_co2 = co2_analytical_AR6(H)
rf_ch4, agwp_ch4, delT_ch4, idelT_ch4 = ch4_analytical_AR6(H)
rf_hfc32, agwp_hfc32, delT_hfc32, idelT_hfc32 =\
            halo_analytical_AR6(H, alpha_hfc32, re_hfc32, mass_hfc32)
gwp_ch4 = agwp_ch4/agwp_co2


fig = plt.figure()
fig.add_subplot(2, 2, 1)
f1 = fig.add_subplot(2, 2, 1)
f1.plot(H[200:], idelT_ch4[200:]*1e12)
f1.plot(H[200:], 0.01*idelT_hfc32[200:]*1e12)
plt.xlabel('years')
plt.ylabel(r'$^\circ$C (Pg yr$^{-1}$)$^{-1}$')
plt.ylim(0., 2)
plt.title(r'$\Delta$T from emission step change')
f1 = fig.add_subplot(2, 2, 2)
f1.plot(H[200:], delT_co2[200:]*1e12)
plt.xlabel('years')
plt.ylabel(r'$^\circ$C Pg$^{-1}$')
plt.ylim(0, 1.1E-3)
plt.title(r'$\Delta$T from emission pulse')
f1 = fig.add_subplot(2, 2, 4)
f1.plot(H[200:], idelT_ch4[200:]/delT_co2[200:])
f1.plot(H[200:], 0.01*idelT_hfc32[200:]/delT_co2[200:])
plt.xlabel('years')
plt.ylabel(r'CGTP (yr)')
plt.ylim(0, 4000)
# plt.yticks([0, 1000, 2000, 3000, 4000])
plt.title(r'$\Delta$T ratio for step vs pulse emissions')
f1 = fig.add_subplot(2, 2, 3)
f1.plot(H[200:], delT_ch4[200:]/delT_co2[200:], label='CH$_4$')
f1.plot(H[200:], 0.01*delT_hfc32[200:]/delT_co2[200:], label='HFC-32/100')
plt.xlabel('years')
plt.ylim(0, 100)
plt.title(r'$\Delta$T ratio for pulse emissions')
plt.legend(prop={'size': 12})
plt.ylabel(r'GTP')
plt.tight_layout()
plt.show()
