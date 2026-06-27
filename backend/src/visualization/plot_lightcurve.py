import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import logging

logger = logging.getLogger(__name__)

STYLE = {
    "bg":      "#0d1117",
    "panel":   "#161b22",
    "accent":  "#58a6ff",
    "green":   "#3fb950",
    "red":     "#f85149",
    "yellow":  "#d29922",
    "text":    "#e6edf3",
    "subtext": "#8b949e",
}


def apply_style():
    plt.rcParams.update({
        "figure.facecolor": STYLE["bg"],
        "axes.facecolor":   STYLE["panel"],
        "axes.edgecolor":   STYLE["subtext"],
        "axes.labelcolor":  STYLE["text"],
        "xtick.color":      STYLE["subtext"],
        "ytick.color":      STYLE["subtext"],
        "text.color":       STYLE["text"],
        "grid.color":       "#21262d",
        "grid.linestyle":   "--",
        "grid.alpha":       0.5,
        "font.family":      "monospace",
        "font.size":        10,
    })


def plot_full_report(time, flux_raw, cleaned, bls_result, classification, tic_id, save_path="backend/outputs"):
    apply_style()
    os.makedirs(save_path, exist_ok=True)

    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(STYLE["bg"])

    conf_color = (STYLE["green"] if classification["confidence"] > 70
                  else STYLE["yellow"] if classification["confidence"] > 40
                  else STYLE["red"])

    fig.suptitle(
        f"PlanetX — TIC {tic_id}   |   {classification['label']}   ({classification['confidence']:.1f}% confidence)",
        fontsize=14, fontweight="bold", color=conf_color, y=0.98
    )

    gs  = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.3, top=0.93, bottom=0.07, left=0.07, right=0.97)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    c_time = cleaned["time"]
    c_flux = cleaned["flux"]

    ax1.plot(time, flux_raw, ".", color=STYLE["subtext"], markersize=1, alpha=0.6, rasterized=True)
    ax1.set_xlabel("Time (BTJD days)")
    ax1.set_ylabel("Normalized Flux")
    ax1.set_title("Raw Light Curve", color=STYLE["accent"])
    ax1.grid(True)

    ax2.plot(c_time, c_flux, ".", color=STYLE["accent"], markersize=1, alpha=0.7, rasterized=True)
    for gap_idx in cleaned["gap_indices"]:
        if gap_idx < len(c_time):
            ax2.axvline(c_time[gap_idx], color=STYLE["yellow"], alpha=0.5, linewidth=1, linestyle="--")
    ax2.axhline(1.0, color=STYLE["subtext"], linewidth=0.5, linestyle="--")
    ax2.set_xlabel("Time (BTJD days)")
    ax2.set_ylabel("Detrended Flux")
    ax2.set_title("Cleaned & Detrended", color=STYLE["accent"])
    ax2.grid(True)
    ax2.annotate(f"Scatter: {cleaned['scatter_ppm']:.0f} ppm", xy=(0.02, 0.05),
                 xycoords="axes fraction", color=STYLE["subtext"], fontsize=8)

    periodogram = bls_result["periodogram"]
    periods     = periodogram.period.value
    power       = periodogram.power
    ax3.plot(periods, power, color=STYLE["accent"], linewidth=0.8, alpha=0.9)
    ax3.axvline(bls_result["period"], color=STYLE["green"], linewidth=1.5, linestyle="--", alpha=0.8)
    ax3.annotate(f"P = {bls_result['period']:.3f} d", xy=(bls_result["period"], max(power)*0.85),
                 color=STYLE["green"], fontsize=9, xytext=(10, 0), textcoords="offset points")
    ax3.set_xlabel("Period (days)")
    ax3.set_ylabel("BLS Power")
    ax3.set_title("BLS Periodogram", color=STYLE["accent"])
    ax3.grid(True)

    period       = bls_result["period"]
    transit_time = bls_result["transit_time"]
    phase        = ((c_time - transit_time) % period) / period
    phase[phase > 0.5] -= 1.0
    sort_idx      = np.argsort(phase)
    phase_sorted  = phase[sort_idx]
    flux_sorted   = c_flux[sort_idx]

    ax4.plot(phase_sorted, flux_sorted, ".", color=STYLE["subtext"], markersize=1.5, alpha=0.4, rasterized=True)

    n_bins      = 100
    bins        = np.linspace(-0.5, 0.5, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_flux    = []
    for i in range(n_bins):
        mask = (phase_sorted >= bins[i]) & (phase_sorted < bins[i+1])
        bin_flux.append(np.median(flux_sorted[mask]) if mask.sum() > 0 else np.nan)

    bin_flux = np.array(bin_flux)
    valid    = ~np.isnan(bin_flux)
    ax4.plot(bin_centers[valid], bin_flux[valid], color=STYLE["green"], linewidth=2, zorder=5)

    duration_phase = bls_result["duration"] / period
    ax4.axvspan(-duration_phase/2, duration_phase/2, color=STYLE["red"], alpha=0.15)
    ax4.axhline(1.0, color=STYLE["subtext"], linewidth=0.5, linestyle="--")
    ax4.set_xlabel(f"Phase (Period = {period:.3f} days)")
    ax4.set_ylabel("Detrended Flux")
    ax4.set_title("Phase-Folded Light Curve", color=STYLE["accent"])
    ax4.grid(True)

    stats_text = (f"Depth : {bls_result['depth']*1e6:.0f} ppm\n"
                  f"Dur   : {bls_result['duration']*24:.2f} hr\n"
                  f"SNR   : {bls_result['snr']:.1f}")
    ax4.annotate(stats_text, xy=(0.02, 0.05), xycoords="axes fraction",
                 color=STYLE["text"], fontsize=8,
                 bbox=dict(boxstyle="round", facecolor=STYLE["bg"], alpha=0.8, edgecolor=STYLE["subtext"]))

    outpath = os.path.join(save_path, f"planetx_TIC{tic_id}.png")
    plt.savefig(outpath, dpi=150, bbox_inches="tight", facecolor=STYLE["bg"])
    plt.close()
    logger.info(f"Saved: {outpath}")
    return outpath