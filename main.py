import argparse
import logging
import os
import sys
import json
import time as timer
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ingestion.load_data import search_and_download, extract_arrays
from src.preprocessing.clean_lightcurve import clean_lightcurve
from src.detection.transit_detector import run_bls, assess_signal_quality
from src.detection.signal_classifier import classify_signal, train_classifier
from src.fitting.period_estimator import refine_period
from src.fitting.depth_calculator import measure_depth
from src.fitting.transit_duration import validate_duration
from src.visualization.plot_lightcurve import plot_full_report

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("PlanetX")
logger.setLevel(logging.INFO)


def run_pipeline(tic_id: int, save_outputs=True):
    start = timer.time()
    logger.info(f"Processing TIC {tic_id}")

    try:
        lc = search_and_download(tic_id)
        if lc is None: return None
        time, flux, flux_err = extract_arrays(lc)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return None

    try:
        cleaned = clean_lightcurve(time, flux, flux_err)
    except Exception as e:
        logger.error(f"Cleaning failed: {e}")
        return None

    try:
        bls_result = run_bls(cleaned["time"], cleaned["flux"], cleaned["flux_err"])
        quality    = assess_signal_quality(bls_result)
    except Exception as e:
        logger.error(f"BLS failed: {e}")
        return None

    try:
        classification = classify_signal(bls_result, cleaned)
    except Exception as e:
        classification = {"label": "UNKNOWN", "confidence": 0.0, "probabilities": {}}

    try:
        refined_period, period_err = refine_period(cleaned["time"], cleaned["flux"], bls_result["period"])
        depth_result               = measure_depth(cleaned["time"], cleaned["flux"], refined_period,
                                                   bls_result["transit_time"], bls_result["duration"])
        duration_val               = validate_duration(depth_result["duration_hrs"], refined_period)
    except Exception as e:
        refined_period = bls_result["period"]
        period_err     = 0.0
        depth_result   = {"depth_ppm": bls_result["depth"]*1e6, "depth_err_ppm": 0,
                          "duration_hrs": bls_result["duration"]*24, "fit_quality": "fallback"}
        duration_val   = {"flag": "UNKNOWN", "interpretation": "Fitting unavailable"}

    radius_ratio = np.sqrt(bls_result["depth"]) if bls_result["depth"] > 0 else 0
    figure_path  = None

    if save_outputs:
        try:
            flux_norm   = flux / np.median(flux)
            figure_path = plot_full_report(time, flux_norm, cleaned, bls_result,
                                           classification, tic_id, save_path="backend/outputs")
        except Exception as e:
            logger.error(f"Visualization failed: {e}")

    result = {
        "tic_id":         tic_id,
        "classification": classification["label"],
        "confidence":     classification["confidence"],
        "probabilities":  classification["probabilities"],
        "parameters": {
            "period_days":      round(refined_period, 5),
            "depth_ppm":        round(depth_result["depth_ppm"], 2),
            "duration_hrs":     round(depth_result["duration_hrs"], 3),
            "snr":              round(bls_result["snr"], 2),
            "scatter_ppm":      round(cleaned["scatter_ppm"], 2),
            "radius_ratio":     round(float(radius_ratio), 5),
        },
        "quality":        quality,
        "figure_path":    figure_path,
        "elapsed_sec":    round(timer.time() - start, 2)
    }

    if save_outputs:
        os.makedirs("backend/outputs", exist_ok=True)
        with open(f"backend/outputs/result_TIC{tic_id}.json", "w") as f:
            json.dump(result, f, indent=2, default=str)

    return result


def print_summary(results):
    valid = [r for r in results if r]
    print(f"\n{'='*65}")
    print(f"  PLANETX SUMMARY — {len(valid)}/{len(results)} stars processed")
    print(f"{'='*65}")
    print(f"  {'TIC ID':<14} {'Classification':<22} {'Conf%':<8} {'Period(d)':<12} {'SNR'}")
    print(f"  {'-'*60}")
    counts = {}
    for r in valid:
        label = r["classification"]
        counts[label] = counts.get(label, 0) + 1
        print(f"  {r['tic_id']:<14} {label:<22} {r['confidence']:<8.1f} "
              f"{r['parameters']['period_days']:<12.4f} {r['parameters']['snr']:.1f}")
    print(f"\n  Breakdown:")
    for label, count in sorted(counts.items()):
        print(f"    {label:<22}: {count}  {'█'*count}")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PlanetX — Exoplanet Detection Pipeline")
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tic",     type=int)
    group.add_argument("--ticlist", type=str)
    group.add_argument("--demo",    action="store_true")
    parser.add_argument("--limit",  type=int, default=20)
    args = parser.parse_args()

    train_classifier()

    if args.demo:
        tics = [25155310, 207141131, 318937509]
        results = [run_pipeline(t) for t in tics]
        print_summary(results)

    elif args.tic:
        result = run_pipeline(args.tic)
        if result: print_summary([result])

    elif args.ticlist:
        with open(args.ticlist) as f:
            tics = [int(l.strip()) for l in f if l.strip().isdigit()][:args.limit]
        results = [run_pipeline(t) for t in tics]
        print_summary(results)
