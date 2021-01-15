"""
Gas properties
"""

# Number of bromine atoms
br_atoms = {
    'CCl4': 0,
    'CFC11': 0,
    'CFC113': 0,
    'CFC114': 0,
    'CFC115': 0,
    'CFC12': 0,
    'CH2Cl2': 0,
    'CH3Br': 1,
    'CH3CCl3': 0,
    'CH3Cl': 0,
    'CHCl3': 0,
    'HCFC141b': 0,
    'HCFC142b': 0,
    'HCFC22': 0,
    'Halon1211': 1,
    'Halon1301': 1,
    'Halon2402': 2,
}

# Number of chlorine atoms
cl_atoms = {
    'CCl4': 4,
    'CFC11': 3,
    'CFC113': 3,
    'CFC114': 2,
    'CFC115': 1,
    'CFC12': 2,
    'CH2Cl2': 2,
    'CH3Br': 0,
    'CH3CCl3': 3,
    'CH3Cl': 1,
    'CHCl3': 3,
    'HCFC141b': 2,
    'HCFC142b': 1,
    'HCFC22': 1,
    'Halon1211': 0,
    'Halon1301': 0,
    'Halon2402': 0,
}

# Fractional release (for ozone depletion)
# References:
# Daniel, J. and Velders, G.: A focus on information and options for 
#   policymakers, in: Scientific Assessment of Ozone Depletion, WMO, 2011
# Newman et al., 2007: A new formulation of equivalent effective stratospheric
#   chlorine (EESC)
fracrel = {
    'CCl4': 0.56,
    'CFC11': 0.47,
    'CFC113': 0.29,
    'CFC114': 0.12,
    'CFC115': 0.04,
    'CFC12': 0.23,
    'CH2Cl2': 0, # no literature value available
    'CH3Br': 0.60,
    'CH3CCl3': 0.67,
    'CH3Cl': 0.44,
    'CHCl3': 0, # no literature value available
    'HCFC141b': 0.34,
    'HCFC142b': 0.17,
    'HCFC22': 0.13,
    'Halon1211': 0.62,
    'Halon1301': 0.28,
    'Halon2402': 0.65,
}

# Conversion between GHG names in GHG spreadsheet and RCMIP.
ghg_to_rcmip_names={
    'HFC-125':      'HFC125',
    'HFC-134a':     'HFC134a',
    'HFC-143a':     'HFC143a',
    'HFC-152a':     'HFC152a',
    'HFC-227ea':    'HFC227ea',
    'HFC-23':       'HFC23',
    'HFC-236fa':    'HFC236fa',
    'HFC-245fa':    'HFC245fa',
    'HFC-32':       'HFC32',
    'HFC-365mfc':   'HFC365mfc',
    'HFC-43-10mee': 'HFC4310mee',
    'NF3':          'NF3',
    'C2F6':         'C2F6',
    'C3F8':         'C3F8',
    'n-C4F10':      'C4F10',
    'n-C5F12':      'C5F12',
    'n-C6F14':      'C6F14',
    'i-C6F14':      None,
    'C7F16':        'C7F16',
    'C8F18':        'C8F18',
    'CF4':          'CF4',
    'c-C4F8':       'cC4F8',
    'SF6':          'SF6',
    'SO2F2':        'SO2F2',
    'CCl4':         'CCl4',
    'CFC-11':       'CFC11',
    'CFC-112':      'CFC112',  
    'CFC-112a':     None,  
    'CFC-113':      'CFC113',
    'CFC-113a':     None,  
    'CFC-114':      'CFC114',
    'CFC-114a':     None, 
    'CFC-115':      'CFC115',
    'CFC-12':       'CFC12',
    'CFC-13':       None,
    'CH2Cl2':       'CH2Cl2',
    'CH3Br':        'CH3Br',
    'CH3CCl3':      'CH3CCl3',
    'CH3Cl':        'CH3Cl',
    'CHCl3':        'CHCl3',
    'HCFC-124':     None,
    'HCFC-133a':    None,
    'HCFC-141b':    'HCFC141b',
    'HCFC-142b':    'HCFC142b',
    'HCFC-22':      'HCFC22',
    'HCFC-31':      None,
    'Halon-1211':   'Halon1211',
    'Halon-1301':   'Halon1301',
    'Halon-2402':   'Halon2402',
}

rcmip_to_ghg_names = {v: k for k, v in ghg_to_rcmip_names.items()}
