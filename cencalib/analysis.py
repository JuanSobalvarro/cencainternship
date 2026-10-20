from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PyAstronomy import pyTiming as pyt
from PyAstronomy.pyTiming import pyPDM


def get_tpf_parameters(tpf: Any) -> dict[str, float]:
    """Return the cadence-related FITS header values used in the investigation."""
    header = tpf.get_header(ext=1)
    return {
        "timedel": header["TIMEDEL"],
        "frametim": header["FRAMETIM"],
        "num_frm": header["NUM_FRM"],
        "int_time": header["INT_TIME"],
    }


def get_exposure_summary(
    tpf: Any, cosmic_ray_retention: float = 0.8
) -> dict[str, float]:
    """Calculate nominal cadence and effective exposure for one TESS cutout."""
    parameters = get_tpf_parameters(tpf)
    raw_integration = parameters["int_time"] * parameters["num_frm"]
    return {
        "cadence": parameters["frametim"] * parameters["num_frm"],
        "raw_integration": raw_integration,
        "effective_exposure": raw_integration * cosmic_ray_retention,
    }


def fft_lightcurve(
    flux: np.ndarray,
    time: np.ndarray,
    center: bool = False,
    min_period: float = 0.0,
    max_period: float = np.inf,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute the positive-frequency FFT used by the notebook plots."""
    flux = np.asarray(flux)
    time = np.asarray(time)
    if flux.size != time.size or flux.size < 2:
        raise ValueError("flux and time must have the same length and at least two samples.")
    if center:
        flux = flux - np.nanmean(flux)

    fft_flux = np.fft.fft(flux)
    frequencies = np.fft.fftfreq(len(fft_flux), d=np.median(np.diff(time)))
    magnitudes = np.abs(fft_flux) / len(fft_flux)
    frequencies = frequencies[: len(fft_flux) // 2]
    magnitudes = magnitudes[: len(fft_flux) // 2]

    valid = np.ones(frequencies.size, dtype=bool)
    if min_period > 0:
        valid &= frequencies <= 1.0 / min_period
    if max_period < np.inf:
        valid &= frequencies >= 1.0 / max_period
    return frequencies[valid], magnitudes[valid]


def plot_fft(
    frequencies: np.ndarray,
    magnitudes: np.ndarray,
    title: str,
    color: str,
    ax: plt.Axes,
) -> None:
    """Render one FFT using the notebook's existing plot styling."""
    ax.plot(frequencies, magnitudes, color=color)
    ax.set_title(f"{title} {np.max(frequencies):.2f}")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Magnitude")


def plot_significant_periods(periodogram: Any, name: str) -> None:
    """Plot a Lightkurve periodogram and annotate its five strongest periods."""
    significant_indices = np.argsort(periodogram.power.value)[-5:]
    periods = periodogram.period[significant_indices]
    powers = periodogram.power[significant_indices]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(periodogram.period.to_value("day"), periodogram.power.value)
    ax.set_title(f"{name} Periodogram")
    ax.set_xlabel("Period [days]")
    ax.set_ylabel("Power")

    for period, power in zip(periods, powers):
        period_days = period.to_value("day")
        power_value = power.value
        ax.scatter(period_days, power_value, s=50)
        ax.text(
            period_days,
            power_value,
            f"{period_days:.4f} d",
            fontsize=9,
            ha="right",
            va="bottom",
        )
    plt.show()


def fit_polynomial_trend(lc: Any, degree: int = 1) -> dict[str, np.ndarray]:
    """Fit and subtract a least-squares polynomial trend from a LightCurve."""
    if degree < 0:
        raise ValueError("degree must be non-negative.")
    time = np.asarray(lc.time.value)
    flux = np.asarray(lc.flux.value)
    coefficients = np.linalg.lstsq(
        np.vander(time, N=degree + 1, increasing=True), flux, rcond=None
    )[0]
    fitted_values = np.polynomial.Polynomial(coefficients[::-1])(time)
    return {
        "coefficients": coefficients,
        "fitted_values": fitted_values,
        "residuals": flux - fitted_values,
    }


def identify_linear_trend(lc: Any) -> dict[str, np.ndarray | float]:
    result = fit_polynomial_trend(lc, degree=1)
    return {
        "slope": result["coefficients"][1],
        "intercept": result["coefficients"][0],
        **result,
    }


def identify_cuadratic_trend(lc: Any) -> dict[str, np.ndarray]:
    return fit_polynomial_trend(lc, degree=2)


def identify_cubic_trend(lc: Any) -> dict[str, np.ndarray]:
    return fit_polynomial_trend(lc, degree=3)


def identify_polynomial_trend(lc: Any, degree: int = 1) -> dict[str, np.ndarray]:
    return fit_polynomial_trend(lc, degree=degree)


def _clean_series(time: np.ndarray, flux: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    time = np.asarray(time)
    flux = np.asarray(flux)
    good = np.isfinite(time) & np.isfinite(flux)
    time, flux = time[good], flux[good]
    if time.size < 3:
        raise ValueError("Not enough valid observations.")
    order = np.argsort(time)
    return time[order], flux[order]


def process_pdm(
    time: np.ndarray,
    flux: np.ndarray,
    min_period: float | None = None,
    max_period: float | None = None,
    n_bins: int = 10,
    samples_per_period: int = 10,
    oversampling: int = 10,
    covers: int = 3,
    n_candidates: int = 5,
    candidate_separation: float = 0.05,
    title: str = "Sh 2-71",
) -> dict[str, Any]:
    """Run PyAstronomy PDM and reproduce the notebook's three-panel diagnostic."""
    time, flux = _clean_series(time, flux)
    baseline = time.max() - time.min()
    sampling_duration = np.median(np.diff(time))
    min_period = (
        samples_per_period * sampling_duration if min_period is None else min_period
    )
    max_period = baseline / 2 if max_period is None else max_period
    if min_period <= 0 or max_period <= min_period:
        raise ValueError("max_period must be larger than a positive min_period.")

    df = 1.0 / (oversampling * baseline)
    scanner = pyPDM.Scanner(
        minVal=1.0 / max_period,
        maxVal=1.0 / min_period,
        dVal=df,
        mode="frequency",
    )
    frequency, theta = pyPDM.PyPDM(time, flux).pdmEquiBinCover(
        n_bins, covers, scanner
    )
    frequency, theta = np.asarray(frequency), np.asarray(theta)
    valid = np.isfinite(frequency) & np.isfinite(theta) & (frequency > 0)
    period, theta = 1.0 / frequency[valid], theta[valid]
    order = np.argsort(period)
    period, theta = period[order], theta[order]
    best_index = np.nanargmin(theta)
    local_minima = np.where(
        (theta[1:-1] < theta[:-2]) & (theta[1:-1] < theta[2:])
    )[0] + 1
    if best_index not in local_minima:
        local_minima = np.append(local_minima, best_index)
    selected: list[int] = []
    for index in local_minima[np.argsort(theta[local_minima])]:
        if all(
            abs(period[index] - period[previous]) / period[previous]
            >= candidate_separation
            for previous in selected
        ):
            selected.append(index)
        if len(selected) >= n_candidates:
            break

    best_period = period[best_index]
    phase = ((time - time.min()) / best_period) % 1
    cycle_number = np.floor((time - time.min()) / best_period).astype(int)
    fig, ax = plt.subplots(3, 1, figsize=(11, 13))
    ax[0].scatter(time, flux, s=4, alpha=0.7)
    ax[0].set(xlabel="Time [days]", ylabel="Flux", title=f"{title} - Original light curve")
    ax[0].grid(alpha=0.3)
    ax[1].plot(period, theta)
    for rank, index in enumerate(selected, start=1):
        ax[1].axvline(period[index], linestyle="--", alpha=0.6)
        ax[1].text(period[index], theta[index], f" {rank}", fontsize=9)
    ax[1].axvline(best_period, linestyle="--", linewidth=2, label=f"Best P = {best_period:.4f} d")
    ax[1].set(xlabel="Period [days]", ylabel="PDM Theta", title=f"PDM period search - {title}")
    ax[1].legend()
    ax[1].grid(alpha=0.3)
    scatter = ax[2].scatter(phase, flux, c=cycle_number, s=5, alpha=0.7)
    fig.colorbar(scatter, ax=ax[2], label="Cycle number")
    ax[2].set(xlabel="Phase", ylabel="Flux", title=f"{title} - Folded at P = {best_period:.4f} d")
    ax[2].grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    return {
        "best_period": best_period,
        "best_theta": theta[best_index],
        "cycles_observed": baseline / best_period,
        "period": period,
        "theta": theta,
        "candidate_periods": period[selected],
        "candidate_theta": theta[selected],
        "baseline": baseline,
        "sampling_duration": sampling_duration,
        "min_period": min_period,
        "max_period": max_period,
    }


def process_stringlength(
    lc: Any,
    min_period: float | None = None,
    max_period: float | None = None,
    samples_per_period: int = 10,
    oversampling: int = 10,
    title: str = "Sh 2-71",
) -> dict[str, Any]:
    """Run PyAstronomy string-length analysis and plot its best period."""
    time, flux = _clean_series(lc.time.value, lc.flux.value)
    baseline = time.max() - time.min()
    sampling_duration = np.median(np.diff(time))
    min_period = samples_per_period * sampling_duration if min_period is None else min_period
    max_period = baseline / 2 if max_period is None else max_period
    frequencies = np.arange(
        1.0 / max_period, 1.0 / min_period, 1.0 / (oversampling * baseline)
    )
    periods, string_length = pyt.stringlength_dat(
        time, flux, tps=np.sort(1.0 / frequencies), closed=True
    )
    periods, string_length = np.asarray(periods), np.asarray(string_length)
    index = np.nanargmin(string_length)
    best_period, best_length = periods[index], string_length[index]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(periods, string_length)
    ax.axvline(best_period, linestyle="--", label=f"P = {best_period:.4f} d")
    ax.set(xlabel="Period [days]", ylabel="String Length", title=f"String Length - {title}")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.show()
    return {
        "period": periods,
        "string_length": string_length,
        "best_period": best_period,
        "best_length": best_length,
        "baseline": baseline,
        "sampling_duration": sampling_duration,
        "min_period": min_period,
        "max_period": max_period,
    }