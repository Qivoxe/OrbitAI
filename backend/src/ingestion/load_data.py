import lightkurve as lk
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)


def search_and_download(tic_id: int, sector: int = None, exptime: str = "short"):
    search_result = lk.search_lightcurve(
        f"TIC {tic_id}",
        mission="TESS",
        sector=sector,
        exptime=exptime,
        author="SPOC"
    )

    if len(search_result) == 0:
        search_result = lk.search_lightcurve(
            f"TIC {tic_id}",
            mission="TESS",
            author="SPOC"
        )

    if len(search_result) == 0:
        logger.warning(f"No data found for TIC {tic_id}")
        return None

    lc = search_result[0].download()

    if lc is None:
        return None

    logger.info(f"Downloaded {len(lc.time)} points for TIC {tic_id}")
    return lc


def load_from_file(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return lk.read(filepath)


def extract_arrays(lc):
    lc_clean = lc.remove_nans()
    time     = np.array(lc_clean.time.value)
    flux     = np.array(lc_clean.flux.value)
    flux_err = np.array(lc_clean.flux_err.value)
    return time, flux, flux_err