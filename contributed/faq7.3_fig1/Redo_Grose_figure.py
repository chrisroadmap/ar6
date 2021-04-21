import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import os.path

df = pd.read_excel (r'ecs_for_faq.xlsx')
dt = pd.read_excel (r'tcr_for_faq.xlsx')

nCMIP5 = df[df['project'] == "CMIP5"]['dataset'].size
nCMIP6 = df[df['project'] == "CMIP6"]['dataset'].size

iCMIP5 = df['project'] == "CMIP5"
iCMIP6 = df['project'] == "CMIP6"

nTCR = dt[dt['project'] == "CMIP6"]['dataset'].size

# CMIP5:
for i in np.arange(nCMIP5):
    model = df[df['project'] == "CMIP5"]['dataset'][i]
    filename = "CMIP5_means/dtas_"+model+".nc"
    if os.path.isfile(filename):
        f     = Dataset(filename, "r")
        df['dT'][i] = f.variables['tas'][0,0,0].data
#        g     = Dataset("CMIP5_means/tas_"+model+"_rcp85.nc")
#        h     = Dataset("CMIP5_means/tas_"+model+"_piControl.nc")
#        plt.figure()
#        plt.plot(g.variables['time'][:].data, g.variables['tas'][:,0,0].data)
#        plt.plot(h.variables['time'][:].data, h.variables['tas'][:,0,0].data)
#        plt.savefig('check_'+model+'.png', dpi=300)

    
# CMIP6:
for i in np.arange(nCMIP5,nCMIP5+nCMIP6):
    model = df[df['project'] == "CMIP6"]['dataset'][i]
    filename = "CMIP6_means/dtas_"+model+".nc"
    if os.path.isfile(filename):
        f     = Dataset(filename, "r")
        df['dT'][i] = f.variables['tas'][0,0,0].data
#        g     = Dataset("CMIP6_means/tas_"+model+"_ssp585.nc")
#        h     = Dataset("CMIP6_means/tas_"+model+"_piControl.nc")
#        plt.figure()
#        plt.plot(g.variables['time'][:].data, g.variables['tas'][:,0,0].data)
#        plt.plot(h.variables['time'][:].data, h.variables['tas'][:,0,0].data)
#        plt.savefig('check_'+model+'.png', dpi=300)

# TCR from CMIP6:
for i in np.arange(0,nTCR):
    model = dt['dataset'][i]
    filename = "CMIP6_means/dtas_"+model+".nc"
    if os.path.isfile(filename):
        f     = Dataset(filename, "r")
        dt['dT'][i] = f.variables['tas'][0,0,0].data
        
fig, axes = plt.subplots(figsize=(5,5))

# Chapter 4: SSP5-8.5 warming in 2081-2100 relative to 1995-2014 is very likely 2.6-4.7C
# Chapter 2, Box 2.3: warming in 1995-2014 relative to 1850-1900 was 0.84C (0.70-0.98)

assessed_mean = 0.84 + (2.6+4.7)/2
assessed_vlr  = (0.14**2 + 1.05**2)**0.5

x1=1.2
axes.plot((x1, x1),(assessed_mean - assessed_vlr, assessed_mean + assessed_vlr), color='gray', lw=3)

y1=2
axes.plot((2, 5),(y1,y1), color='gray', lw=3)
#axes.plot((3, 3),(y1-0.2, y1+0.2), color='gray', lw=3)

# Numbers from emulator: 3.04638277, 6.46582885
#rect = plt.Rectangle((2, 3.04638277), 3, 6.46582885-3.04638277, facecolor="lightgray", zorder=0)
#axes.add_patch(rect)

h5 = axes.scatter(df['ECS'][iCMIP5], df['dT'][iCMIP5], color='red', label='CMIP5, RCP8.5')
h6 = axes.scatter(df['ECS'][iCMIP6], df['dT'][iCMIP6], color='blue', label='CMIP6, SSP5-8.5')

#axes.text(1,1,'Preliminary figure',color='red', fontsize=20)

plt.legend(handles=[h5, h6], frameon=False, fontsize=10, loc='upper left')

plt.ylabel(r'Global warming in 2081-2100 ($^\circ$C)')
plt.xlabel(r'Equilibrium Climate Sensitivity ($^\circ$C)')

axes.set_ylim(0,8)
axes.set_xlim(0,6)

plt.tight_layout()
plt.savefig('ECS_vs_RCP85_SSP5-85.png', dpi=600)
plt.close()

# TCR figure

fig, axes = plt.subplots(figsize=(5,5))
axes.scatter(dt['TCR'][:], dt['dT'][:], color='blue', label='CMIP6, SSP5-8.5')
axes.plot((x1, x1),(assessed_mean - assessed_vlr, assessed_mean + assessed_vlr), color='gray', lw=3)
axes.plot((1.2, 2.4),(y1,y1), color='gray', lw=3)

plt.ylabel(r'Global warming in 2081-2100 ($^\circ$C)')
plt.xlabel(r'Transient Climate Response ($^\circ$C)')

axes.set_ylim(0,8)
axes.set_xlim(0,6)

plt.tight_layout()
plt.savefig('TCR_vs_SSP5-85.png', dpi=600)
plt.close()

#Schlund, M., Lauer, A., Gentine, P., Sherwood, S. C., and Eyring, V.: Emergent constraints on Equilibrium Climate Sensitivity in CMIP5: do they hold for CMIP6?, Earth Syst. Dynam. Discuss., https://doi.org/10.5194/esd-2020-49, in review, 2020.
