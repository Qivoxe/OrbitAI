import numpy as np
import logging

logger = logging.getLogger(__name__)

R_SUN = 6.957e8
M_SUN = 1.989e30
G     = 6.674e-11


def estimate_duration_physical(period_days, stellar_radius_rsun=1.0, stellar_mass_msun=1.0, impact_param=0.0):
    period_sec = period_days * 86400
    Rs         = stellar_radius_rsun * R_SUN
    Ms         = stellar_mass_msun * M_SUN
    a          = (G * Ms * period_sec**2 / (4 * np.pi**2)) ** (1/3)
    sin_arg    = min(Rs * np.sqrt(1 - impact_param**2) / a, 1.0)
    return (period_sec / np.pi) * np.arcsin(sin_arg) / 3600


def validate_duration(measured_hrs, period_days, stellar_radius_rsun=1.0, stellar_mass_msun=1.0):
    expected_hrs = estimate_duration_physical(period_days, stellar_radius_rsun, stellar_mass_msun)
    ratio        = measured_hrs / expected_hrs if expected_hrs > 0 else 0

    if ratio < 0.3:       flag, interp = "SHORT",          "Too short — possible grazing transit or noise"
    elif ratio < 0.5:     flag, interp = "SLIGHTLY_SHORT", "Shorter than expected — high impact parameter"
    elif ratio <= 2.0:    flag, interp = "OK",             "Consistent with planetary transit"
    elif ratio <= 4.0:    flag, interp = "LONG",           "Longer than expected — possible blend or EB"
    else:                 flag, interp = "TOO_LONG",       "Much too long — likely eclipsing binary or artifact"

    return {"measured_hrs": measured_hrs, "expected_hrs": expected_hrs,
            "ratio": ratio, "flag": flag, "interpretation": interp}