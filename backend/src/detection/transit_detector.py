import numpy as np
from astropy.timeseries import BoxLeastSquares
from astropy import units as u
import logging

logger = logging.getLogger(__name__)


def run_bls(time, flux, flux_err=None):
    model    = BoxLeastSquares(time * u.day, flux, dy=flux_err)
    baseline = time[-1] - time[0]
    min_period = 0.5
    max_period = baseline / 2.0
    durations  = np.linspace(0.02, 0.15, 10) * u.day

    periodogram = model.autopower(
        durations,
        minimum_period=min_period * u.day,
        maximum_period=max_period * u.day,
        frequency_factor=5.0
    )

    best_idx       = np.argmax(periodogram.power)
    best_period    = periodogram.period[best_idx].value
    best_power     = periodogram.power[best_idx]
    best_duration  = periodogram.duration[best_idx].value
    best_transit_time = periodogram.transit_time[best_idx].value

    stats     = model.compute_stats(
        best_period * u.day,
        best_duration * u.day,
        best_transit_time * u.day
    )

    depth     = stats['depth'][0]
    scatter   = np.std(flux)
    snr       = depth / (scatter / np.sqrt(len(flux))) if scatter > 0 else 0

    logger.info(f"BLS: period={best_period:.4f}d depth={depth*1e6:.1f}ppm snr={snr:.1f}")

    return {
        "period":       best_period,
        "duration":     best_duration,
        "transit_time": best_transit_time,
        "depth":        depth,
        "depth_err":    stats['depth'][1],
        "snr":          snr,
        "bls_power":    float(best_power),
        "periodogram":  periodogram
    }


def assess_signal_quality(bls_result):
    snr      = bls_result["snr"]
    depth    = bls_result["depth"]
    duration = bls_result["duration"]
    period   = bls_result["period"]
    score    = 0
    flags    = []

    if snr >= 7:       score += 40
    elif snr >= 5:     score += 20; flags.append("Low SNR")
    else:              flags.append("Very low SNR")

    if depth > 100e-6:    score += 20
    elif depth > 50e-6:   score += 10; flags.append("Shallow depth")
    else:                 flags.append("Depth near noise floor")

    if 1.0 <= duration * 24 <= 16.0:   score += 20
    else:                               flags.append(f"Unusual duration: {duration*24:.1f}h")

    if period >= 1.0:   score += 20
    else:               flags.append("Very short period")

    confidence = "HIGH" if score >= 80 else "MEDIUM" if score >= 50 else "LOW"
    return {"confidence": confidence, "score": score, "flags": flags}


def fold_lightcurve(time, flux, period, transit_time):
    phase = ((time - transit_time) % period) / period
    phase[phase > 0.5] -= 1.0
    sort_idx = np.argsort(phase)
    return phase[sort_idx], flux[sort_idx]