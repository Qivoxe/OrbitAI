import numpy as np
from scipy.optimize import curve_fit
import logging

logger = logging.getLogger(__name__)


def trapezoidal_transit(phase, depth, duration, ingress_fraction, baseline):
    flux        = np.ones_like(phase) * baseline
    ingress_dur = duration * ingress_fraction / 2
    flat_dur    = duration * (1 - ingress_fraction) / 2

    for i, p in enumerate(phase):
        ap = abs(p)
        if ap < flat_dur:
            flux[i] = baseline - depth
        elif ap < flat_dur + ingress_dur:
            flux[i] = baseline - depth * (1 - (ap - flat_dur) / ingress_dur)
    return flux


def measure_depth(time, flux, period, transit_time, bls_duration):
    phase   = ((time - transit_time) % period) / period
    phase[phase > 0.5] -= 1.0
    sort_idx = np.argsort(phase)
    phase_s  = phase[sort_idx]
    flux_s   = flux[sort_idx]

    duration_phase = bls_duration / period
    mask           = np.abs(phase_s) < duration_phase * 2.5

    if mask.sum() < 10:
        depth = max(1.0 - np.min(flux_s), 0)
        return {"depth": depth, "depth_err": depth*0.2, "depth_ppm": depth*1e6,
                "depth_err_ppm": depth*0.2*1e6, "duration_phase": duration_phase,
                "duration_hrs": duration_phase*period*24, "ingress_fraction": 0.3,
                "baseline": 1.0, "fit_quality": "poor", "snr": 0}

    phase_fit = phase_s[mask]
    flux_fit  = flux_s[mask]
    p0        = [1.0 - np.min(flux_fit), duration_phase, 0.3,
                 np.median(flux_fit[np.abs(phase_fit) > duration_phase/2])]
    bounds    = ([0, duration_phase*0.3, 0.05, 0.95],
                 [0.5, duration_phase*3.0, 0.8, 1.05])

    try:
        popt, pcov  = curve_fit(trapezoidal_transit, phase_fit, flux_fit,
                                p0=p0, bounds=bounds, maxfev=5000)
        perr        = np.sqrt(np.diag(pcov))
        residuals   = flux_fit - trapezoidal_transit(phase_fit, *popt)
        scatter     = np.std(residuals)
        return {"depth": popt[0], "depth_err": perr[0],
                "depth_ppm": popt[0]*1e6, "depth_err_ppm": perr[0]*1e6,
                "duration_phase": popt[1], "duration_hrs": popt[1]*period*24,
                "ingress_fraction": popt[2], "baseline": popt[3],
                "fit_quality": "good", "snr": popt[0]/scatter if scatter > 0 else 0}
    except Exception as e:
        logger.warning(f"Fit failed: {e}")
        depth = max(1.0 - np.min(flux_fit), 0)
        return {"depth": depth, "depth_err": depth*0.2,
                "depth_ppm": depth*1e6, "depth_err_ppm": depth*0.2*1e6,
                "duration_phase": duration_phase, "duration_hrs": duration_phase*period*24,
                "ingress_fraction": 0.3, "baseline": 1.0,
                "fit_quality": "fallback", "snr": 0}