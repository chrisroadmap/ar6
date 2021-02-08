"""
Module with general constants used throughout the processing chain.
"""

import scipy.stats as st

NINETY_TO_ONESIGMA = st.norm.ppf(0.95)
