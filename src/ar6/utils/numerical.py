"""
Module for numerical methods.
"""

import numpy as np

def significance(x, digits):
    """Expresses a number to a given precision.

    Inputs:
    -------
    x : float
        number to round
    digits : int
        number of significant figures to express result in

    Returns:
    --------
    float
        `x` rounded to `digits` significant figures.
    """
    return (np.round(x, digits - (1 + int(np.floor(np.log10(np.abs(x)))))))
