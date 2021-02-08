
import numpy as np


a = np.array([0.2173, 0.2240, 0.2824, 0.2763])  # Joos et al. 2013
alpha_co2 = np.array([0.,   394.4, 36.54, 4.304])   # Joos et al. 2013
alpha_ch4 = 11.7 # Vaishali
alpha_n2o = 109.  # AR6 SOD

co2_0 = 278.
ch4_0 = 722
n2o_0 = 270.
co2 = 405.  # 2017 FOD
ch4 = 1850.  # 2017 FOD
n2o = 330.  # 2017 FOD
co2 = 407.38 
ch4 = 1858.6  # 2018 SOD
n2o = 331.19  # 2018 SOD
ch4 = 1866. # 2019 FGD
co2 = 410. # 2019 FGD
n2o = 332. # 2019 FGD


c = 0.885*np.array([0.587, 0.413])  # in K/(W/m2) Geoffroy et al. 2013
d = np.array([4.1, 249.])
# Tropospheric rapid adjustments
co2_ra = 0.05  # section 7.3.2
ch4_ra = -0.14  # section 7.3.2
n2o_ra = 0.07   # section 7.3.2
cfc_ra = 0.12 # section 7.3.2
halo_ra = 0.     # section 7.3.2

# Fractional uncertainties
err_co2 = 0.12
err_ch4 = 0.2
err_n2o = 0.16

#
m_atm = 5.1352E18
m_air = 28.97E-3
m_co2 = 44.01E-3
m_c = 12.0E-3
m_ch4 = 16.043E-3
m_n2o = 44.0E-3

f_ch4_o3 = 0.29 # Thornhill
f_ch4_h2o = 0.1 # Thornhill
f_n2o_o3 = 0.15 # Thornhill
f_n2o_ch4 = -1.6 # Thornhill