import numpy as np
import pickle
import os
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

logger = logging.getLogger(__name__)

LABELS = {
    0: "PLANET CANDIDATE",
    1: "ECLIPSING BINARY",
    2: "BLEND",
    3: "NOISE / OTHER"
}


def extract_features(bls_result, cleaned_result):
    period       = bls_result["period"]
    depth        = bls_result["depth"]
    duration     = bls_result["duration"]
    snr          = bls_result["snr"]
    scatter_ppm  = cleaned_result["scatter_ppm"]
    depth_ppm    = depth * 1e6
    duration_hrs = duration * 24
    depth_ratio  = depth_ppm / scatter_ppm if scatter_ppm > 0 else 0
    duty_cycle   = duration / period

    return np.array([period, depth_ppm, duration_hrs, snr,
                     depth_ratio, duty_cycle, scatter_ppm])


def generate_training_data():
    np.random.seed(42)
    n = 300
    X, y = [], []

    for _ in range(n):
        period       = np.random.uniform(0.5, 30)
        depth_ppm    = np.random.uniform(100, 5000)
        duration_hrs = np.random.uniform(1.0, 8.0)
        scatter_ppm  = np.random.uniform(200, 2000)
        snr          = max(depth_ppm / scatter_ppm * np.sqrt(np.random.uniform(3, 20)) + np.random.normal(0, 2), 0)
        X.append([period, depth_ppm, duration_hrs, snr, depth_ppm/scatter_ppm, (duration_hrs/24)/period, scatter_ppm])
        y.append(0)

    for _ in range(n):
        period       = np.random.uniform(0.3, 15)
        depth_ppm    = np.random.uniform(5000, 100000)
        duration_hrs = np.random.uniform(0.5, 6.0)
        scatter_ppm  = np.random.uniform(200, 2000)
        snr          = max(depth_ppm / scatter_ppm * np.sqrt(np.random.uniform(5, 30)) + np.random.normal(0, 5), 0)
        X.append([period, depth_ppm, duration_hrs, snr, depth_ppm/scatter_ppm, (duration_hrs/24)/period, scatter_ppm])
        y.append(1)

    for _ in range(n):
        period       = np.random.uniform(1, 20)
        depth_ppm    = np.random.uniform(500, 8000)
        duration_hrs = np.random.uniform(2.0, 12.0)
        scatter_ppm  = np.random.uniform(500, 3000)
        snr          = np.random.uniform(3, 25)
        X.append([period, depth_ppm, duration_hrs, snr, depth_ppm/scatter_ppm*np.random.uniform(0.3,0.8), (duration_hrs/24)/period, scatter_ppm])
        y.append(2)

    for _ in range(n):
        period       = np.random.uniform(0.5, 14)
        depth_ppm    = np.random.uniform(50, 3000)
        duration_hrs = np.random.uniform(0.5, 5.0)
        scatter_ppm  = np.random.uniform(1000, 5000)
        snr          = np.random.uniform(0, 7)
        X.append([period, depth_ppm, duration_hrs, snr, depth_ppm/scatter_ppm*np.random.uniform(0.1,0.5), (duration_hrs/24)/period, scatter_ppm])
        y.append(3)

    return np.array(X), np.array(y)


def train_classifier(X=None, y=None, save_path="backend/src/models"):
    if X is None or y is None:
        X, y = generate_training_data()

    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    clf = RandomForestClassifier(n_estimators=200, max_depth=10,
                                  min_samples_leaf=5, random_state=42,
                                  class_weight="balanced")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=list(LABELS.values())))

    os.makedirs(save_path, exist_ok=True)
    with open(f"{save_path}/classifier.pkl", "wb") as f:
        pickle.dump(clf, f)
    with open(f"{save_path}/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    return clf, scaler


def classify_signal(bls_result, cleaned_result, model_path="backend/src/models"):
    clf_path    = f"{model_path}/classifier.pkl"
    scaler_path = f"{model_path}/scaler.pkl"

    if not os.path.exists(clf_path):
        clf, scaler = train_classifier()
    else:
        with open(clf_path, "rb") as f:  clf = pickle.load(f)
        with open(scaler_path, "rb") as f: scaler = pickle.load(f)

    features        = extract_features(bls_result, cleaned_result)
    features_scaled = scaler.transform(features.reshape(1, -1))
    label_idx       = clf.predict(features_scaled)[0]
    probabilities   = clf.predict_proba(features_scaled)[0]
    confidence      = probabilities[label_idx] * 100

    return {
        "label":         LABELS[label_idx],
        "label_idx":     int(label_idx),
        "confidence":    confidence,
        "probabilities": {LABELS[i]: round(float(p)*100, 1) for i, p in enumerate(probabilities)}
    }