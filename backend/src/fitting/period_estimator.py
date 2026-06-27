import numpy as np
from scipy.optimize import minimize_scalar
import logging

logger = logging.getLogger(__name__)


def refine_period(time, flux, bls_period, search_fraction=0.1):
    p_min = bls_period * (1 - search_fraction)
    p_max = bls_period * (1 + search_fraction)

    def fold_scatter(period):
        if period <= 0:
            return 1e10
        phase      = ((time - time[0]) % period) / period
        flux_sorted = flux[np.argsort(phase)]
        return np.std(np.diff(flux_sorted))

    result         = minimize_scalar(fold_scatter, bounds=(p_min, p_max),
                                     method='bounded', options={'xatol': 1e-6})
    refined_period = result.x
    baseline       = time[-1] - time[0]
    n_transits     = baseline / refined_period
    period_err     = refined_period / (baseline * np.sqrt(max(n_transits, 1)))

    logger.info(f"Refined period: {refined_period:.6f} ± {period_err:.6f} days")
    return refined_period, period_err