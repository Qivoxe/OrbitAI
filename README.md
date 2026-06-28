# 🪐 PlanetX

 AI-Driven Detection of Exoplanets from Noisy Astronomical Light Curves

**ISRO × Hack2Skill Hackathon — Problem Statement #07**
 Built on NASA TESS (Transiting Exoplanet Survey Satellite) data via MAST Archive

---

## What is PlanetX?

PlanetX is an end-to-end automated pipeline that downloads real stellar brightness data from NASA's TESS satellite, searches for the characteristic dimming caused by a planet passing in front of its star, classifies the signal type using machine learning, and estimates the planet's orbital parameters — all from a single command or through a web dashboard.

**Validated on WASP-126b** — a confirmed hot Jupiter. PlanetX recovered its orbital period to within 0.013% of the published value.

---

## Project Architecture

```
PlanetX/
│
├── backend/                          ← Python ML Pipeline + FastAPI
│   │
│   ├── api/
│   │   └── main.py                   ← FastAPI REST API (all endpoints)
│   │
│   ├── src/
│   │   ├── ingestion/
│   │   │   └── load_data.py          ← TESS data download (SPOC only)
│   │   │
│   │   ├── preprocessing/
│   │   │   └── clean_lightcurve.py   ← Outlier removal, normalize, detrend
│   │   │
│   │   ├── detection/
│   │   │   ├── transit_detector.py   ← BLS periodogram + SNR
│   │   │   └── signal_classifier.py  ← Random Forest (97% accuracy)
│   │   │
│   │   ├── fitting/
│   │   │   ├── period_estimator.py   ← Period refinement via minimization
│   │   │   ├── depth_calculator.py   ← Trapezoidal transit model fitting
│   │   │   └── transit_duration.py   ← Duration measurement + validation
│   │   │
│   │   ├── visualization/
│   │   │   └── plot_lightcurve.py    ← 4-panel diagnostic figure
│   │   │
│   │   └── models/
│   │       ├── classifier.pkl        ← Trained Random Forest model
│   │       └── scaler.pkl            ← Feature scaler
│   │
│   ├── outputs/                      ← Generated figures + JSON results
│   ├── data/
│   │   └── raw/                      ← TIC catalog files
│   │
│   ├── main.py                       ← CLI pipeline runner
│   ├── requirements.txt
│   └── venv/                         ← Python virtual environment
│
├── frontend/                         ← Next.js Web Dashboard
│   │
│   ├── app/
│   │   ├── page.tsx                  ← Landing page
│   │   ├── Dashboard/
│   │   │   └── page.tsx              ← Main analysis page
│   │   ├── Analyze/
│   │   │   └── page.tsx              ← Analyze page
│   │   ├── Results/
│   │   │   └── page.tsx              ← Batch results table
│   │   └── Docs/
│   │       └── page.tsx              ← Documentation
│   │
│   ├── components/
│   │   ├── Navbar.tsx                ← Navigation bar
│   │   ├── Hero.tsx                  ← Landing hero section
│   │   ├── Footer.tsx                ← Footer
│   │   ├── Pipeline.tsx              ← Pipeline stages component
│   │   └── SpaceBackground.tsx       ← Animated star field
│   │
│   ├── public/                       ← Static assets
│   ├── package.json
│   └── next.config.ts
│
├── main.py                           ← Root pipeline runner
├── README.md
└── .gitignore
```

---

## Pipeline Architecture

```
NASA MAST Archive
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│                    PlanetX Pipeline                      │
│                                                         │
│  Stage 1 │ load_data.py          → Download TESS FITS  │
│     ↓                                                   │
│  Stage 2 │ clean_lightcurve.py   → Clean & Detrend     │
│     ↓                                                   │
│  Stage 3 │ transit_detector.py   → BLS Detection       │
│     ↓                                                   │
│  Stage 4 │ signal_classifier.py  → ML Classification   │
│     ↓                                                   │
│  Stage 5 │ fitting/              → Parameter Estimation │
│     ↓                                                   │
│  Stage 6 │ plot_lightcurve.py    → 4-Panel Figure      │
└─────────────────────────────────────────────────────────┘
       │
       ▼
  FastAPI (port 8000)
       │
       ▼
  Next.js Dashboard (port 3000)
```

---

## Signal Classes

| Class | Description | Key Features |
|-------|-------------|--------------|
| 🪐 Planet Candidate | Transiting exoplanet | Depth 100–5,000 ppm, flat bottom, SNR > 7 |
| ⭐ Eclipsing Binary | Two stars eclipsing | Depth > 10,000 ppm, V-shaped, secondary eclipse |
| 🌫 Blend | Background contamination | Inconsistent depth, long duration, high scatter |
| 📡 Noise / Other | No real signal | SNR < 5, depth near noise floor |

---

## API Architecture

**Base URL:** `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/analyze` | Run full pipeline on a TIC ID |
| GET | `/result/{tic_id}` | Fetch cached result |
| GET | `/results` | List all processed stars |
| GET | `/stats` | Dashboard counters |
| DELETE | `/result/{tic_id}` | Delete cached result |

**Request:**
```json
POST /analyze
{
  "tic_id": 25155310
}
```

**Response:**
```json
{
  "tic_id": 25155310,
  "classification": "PLANET CANDIDATE",
  "confidence": 36.1,
  "probabilities": {
    "PLANET CANDIDATE": 36.1,
    "ECLIPSING BINARY": 20.8,
    "BLEND": 35.3,
    "NOISE / OTHER": 7.8
  },
  "parameters": {
    "period_days": 3.23793,
    "depth_ppm": 464.2,
    "duration_hrs": 0.76,
    "snr": 120.2,
    "scatter_ppm": 1325.8,
    "radius_ratio": 0.03243
  },
  "quality": {
    "confidence": "HIGH",
    "score": 80,
    "flags": ["Unusual duration: 1.0h"]
  },
  "figure_url": "/outputs/planetx_TIC25155310.png"
}
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Qivoxe/PlanetX.git
cd PlanetX
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the CLI Pipeline

```bash
# Single star
python main.py --tic 25155310

# Demo mode (3 known stars)
python main.py --demo

# From TIC ID list
python main.py --ticlist data/confirmed_tics.txt
```

### 4. Start the API

```bash
uvicorn api.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

### 5. Start the Frontend

```bash
cd ../frontend
npm install
npm run dev
```

Dashboard: `http://localhost:3000/Dashboard`

---

## Sample Results

| TIC ID | Classification | Period | Depth | SNR |
|--------|---------------|--------|-------|-----|
| 25155310 | 🪐 PLANET CANDIDATE | 3.289 days | 1052.9 ppm | 120.2 |
| 207141131 | 🪐 PLANET CANDIDATE | 4.137 days | 244.6 ppm | 77.9 |
| 149603524 | 🪐 PLANET CANDIDATE | 4.413 days | 3763.0 ppm | 493.5 |
| 318937509 | ⭐ ECLIPSING BINARY | 1.049 days | 17290.0 ppm | 103.6 |
| 100100827 | 🌫 BLEND | 0.942 days | 1495.6 ppm | 208.1 |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data | lightkurve 2.6 | TESS light curve download |
| Astronomy | astropy 8.0 | BLS periodogram, FITS I/O |
| Signal Processing | scipy | Detrending, curve fitting, optimization |
| ML | scikit-learn | Random Forest classifier |
| Numerics | numpy 2.x | Array operations |
| Visualization | matplotlib | 4-panel diagnostic figure |
| API | FastAPI + uvicorn | REST backend |
| Frontend | Next.js 16 + Tailwind | Web dashboard |
| Language | Python 3.14 | Runtime |

---

## Classifier Performance

```
                  precision    recall  f1-score   support

PLANET CANDIDATE       0.94      0.97      0.95        60
ECLIPSING BINARY       1.00      1.00      1.00        60
           BLEND       0.98      0.92      0.95        60
   NOISE / OTHER       0.97      1.00      0.98        60

        accuracy                           0.97       240
```

**Feature importances:**

| Feature | Importance |
|---------|-----------|
| depth_ratio | 24.4% |
| depth_ppm | 24.4% |
| snr | 20.8% |
| duration_hrs | 11.2% |
| scatter_ppm | 9.7% |
| period | 6.6% |
| duty_cycle | 2.9% |

---

## Known Limitations

- Savitzky-Golay detrending suppresses transits > 3 hours, causing depth underestimation
- Single 27-day TESS sector analyzed per star — longer periods not detectable
- Classifier trained on synthetic data — improves with curated labeled dataset
- No limb darkening in trapezoidal model (~10-15% depth uncertainty)
- SPOC-only products — faint stars in crowded fields skipped

---

## Team

Built for ISRO × Hack2Skill Hackathon — Problem Statement #07

| Name | Role |
|------|------|
| Shivam | Backend / ML Pipeline |
| Nancy | Frontend / UI |
| [Team Member 3] | Research / Report |

**GitHub:** https://github.com/Qivoxe/PlanetX

---

*PlanetX — Searching the universe, one light curve at a time. 🪐*
