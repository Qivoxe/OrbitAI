import numpy as np
from scipy.signal import savgol_filter
import logging

logger = logging.getLogger(__name__)


def normalize_flux(flux, flux_err):
    median = np.median(flux)
    return flux / median, flux_err / median


def remove_outliers(time, flux, flux_err, sigma=5.0):
    median = np.median(flux)
    std    = np.std(flux)
    mask   = np.abs(flux - median) < sigma * std
    logger.info(f"Removed {np.sum(~mask)} outliers")
    return time[mask], flux[mask], flux_err[mask]


def detrend_flux(time, flux, window_length=101):
    if window_length % 2 == 0:
        window_length += 1
    trend     = savgol_filter(flux, window_length=window_length, polyorder=2)
    detrended = flux / trend
    logger.info(f"Detrended with Savitzky-Golay window={window_length}")
    return detrended, trend


def handle_gaps(time, flux, flux_err, gap_threshold=0.5):
    dt          = np.diff(time)
    gap_indices = np.where(dt > gap_threshold)[0]
    logger.info(f"Found {len(gap_indices)} gaps")
    return gap_indices.tolist()


def clean_lightcurve(time, flux, flux_err):
    time, flux, flux_err    = remove_outliers(time, flux, flux_err)
    flux, flux_err          = normalize_flux(flux, flux_err)
    flux_detrended, trend   = detrend_flux(time, flux)
    gap_indices             = handle_gaps(time, flux_detrended, flux_err)
    scatter                 = np.std(flux_detrended)

    return {
        "time":        time,
        "flux":        flux_detrended,
        "flux_err":    flux_err,
        "trend":       trend,
        "gap_indices": gap_indices,
        "scatter_ppm": scatter * 1e6,
        "n_points":    len(time)
    }