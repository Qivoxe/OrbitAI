from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os
import json
import glob
import numpy as np
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.load_data import search_and_download, extract_arrays
from src.preprocessing.clean_lightcurve import clean_lightcurve
from src.detection.transit_detector import run_bls, assess_signal_quality
from src.detection.signal_classifier import classify_signal, train_classifier
from src.fitting.period_estimator import refine_period
from src.fitting.depth_calculator import measure_depth
from src.fitting.transit_duration import validate_duration
from src.visualization.plot_lightcurve import plot_full_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PlanetX.API")

app = FastAPI(
    title="PlanetX API",
    description="AI-driven exoplanet transit detection from NASA TESS data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


class TICRequest(BaseModel):
    tic_id: int


@app.on_event("startup")
def startup_event():
    logger.info("PlanetX API starting — training classifier...")
    train_classifier()
    logger.info("PlanetX API ready.")


@app.get("/")
def root():
    return {
        "name":        "PlanetX",
        "status":      "running",
        "version":     "1.0.0",
        "description": "AI-driven exoplanet transit detection from NASA TESS data"
    }


@app.post("/analyze")
def analyze(req: TICRequest):
    logger.info(f"PlanetX analyzing TIC {req.tic_id}")

    try:
        lc = search_and_download(req.tic_id, sector=None)
        if lc is None:
            raise HTTPException(status_code=404, detail=f"No TESS data found for TIC {req.tic_id}")
        time, flux, flux_err = extract_arrays(lc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

    try:
        cleaned = clean_lightcurve(time, flux, flux_err)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")

    try:
        bls_result = run_bls(cleaned["time"], cleaned["flux"], cleaned["flux_err"])
        quality    = assess_signal_quality(bls_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transit detection failed: {str(e)}")

    try:
        classification = classify_signal(bls_result, cleaned)
    except Exception as e:
        logger.warning(f"Classification failed: {e}")
        classification = {"label": "UNKNOWN", "confidence": 0.0, "probabilities": {}}

    try:
        refined_period, period_err = refine_period(
            cleaned["time"], cleaned["flux"], bls_result["period"]
        )
        depth_result = measure_depth(
            cleaned["time"], cleaned["flux"],
            refined_period,
            bls_result["transit_time"],
            bls_result["duration"]
        )
        duration_val = validate_duration(depth_result["duration_hrs"], refined_period)
        radius_ratio = np.sqrt(bls_result["depth"]) if bls_result["depth"] > 0 else 0
    except Exception as e:
        logger.warning(f"Fitting failed: {e}")
        refined_period = bls_result["period"]
        period_err     = 0.0
        depth_result   = {
            "depth_ppm":     bls_result["depth"] * 1e6,
            "depth_err_ppm": 0.0,
            "duration_hrs":  bls_result["duration"] * 24,
            "fit_quality":   "fallback"
        }
        duration_val = {"flag": "UNKNOWN", "interpretation": "Fitting unavailable"}
        radius_ratio = np.sqrt(bls_result["depth"]) if bls_result["depth"] > 0 else 0

    figure_url = None
    try:
        flux_norm  = flux / np.median(flux)
        plot_full_report(
            time, flux_norm, cleaned,
            bls_result, classification,
            req.tic_id, save_path="outputs"
        )
        figure_url = f"/outputs/planetx_TIC{req.tic_id}.png"
    except Exception as e:
        logger.warning(f"Visualization failed: {e}")

    result = {
        "tic_id":         req.tic_id,
        "name":           "PlanetX",
        "classification": classification["label"],
        "confidence":     round(classification["confidence"], 2),
        "probabilities":  classification["probabilities"],
        "parameters": {
            "period_days":     round(refined_period, 5),
            "period_err_days": round(period_err, 6),
            "depth_ppm":       round(depth_result["depth_ppm"], 2),
            "depth_err_ppm":   round(depth_result["depth_err_ppm"], 2),
            "duration_hrs":    round(depth_result["duration_hrs"], 3),
            "snr":             round(bls_result["snr"], 2),
            "scatter_ppm":     round(cleaned["scatter_ppm"], 2),
            "radius_ratio":    round(float(radius_ratio), 5),
            "n_points":        cleaned["n_points"],
            "fit_quality":     depth_result["fit_quality"]
        },
        "quality": {
            "confidence": quality["confidence"],
            "score":      quality["score"],
            "flags":      quality["flags"]
        },
        "duration_validation": {
            "flag":           duration_val["flag"],
            "interpretation": duration_val["interpretation"]
        },
        "figure_url": figure_url
    }

    os.makedirs("outputs", exist_ok=True)
    with open(f"outputs/result_TIC{req.tic_id}.json", "w") as f:
        json.dump(result, f, indent=2, default=str)

    return result


@app.get("/result/{tic_id}")
def get_result(tic_id: int):
    path = f"outputs/result_TIC{tic_id}.json"
    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail=f"No cached result for TIC {tic_id}. Run /analyze first."
        )
    with open(path) as f:
        return json.load(f)


@app.get("/results")
def list_results():
    results = []
    for path in sorted(glob.glob("outputs/result_TIC*.json")):
        try:
            with open(path) as f:
                results.append(json.load(f))
        except Exception:
            continue
    return {"total": len(results), "results": results}


@app.get("/stats")
def get_stats():
    results = []
    for path in glob.glob("outputs/result_TIC*.json"):
        try:
            with open(path) as f:
                results.append(json.load(f))
        except Exception:
            continue

    counts = {}
    for r in results:
        label = r.get("classification", "UNKNOWN")
        counts[label] = counts.get(label, 0) + 1

    return {
        "name":                "PlanetX",
        "total_processed":     len(results),
        "planet_candidates":   counts.get("PLANET CANDIDATE", 0),
        "eclipsing_binaries":  counts.get("ECLIPSING BINARY", 0),
        "blends":              counts.get("BLEND", 0),
        "noise":               counts.get("NOISE / OTHER", 0),
        "classifier_accuracy": 97.0,
        "catalog_stars":       196801
    }


@app.delete("/result/{tic_id}")
def delete_result(tic_id: int):
    path     = f"outputs/result_TIC{tic_id}.json"
    fig_path = f"outputs/planetx_TIC{tic_id}.png"

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"No result for TIC {tic_id}")

    os.remove(path)
    if os.path.exists(fig_path):
        os.remove(fig_path)

    return {"status": "deleted", "tic_id": tic_id}