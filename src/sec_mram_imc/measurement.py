"""Reference implementations of the public measurement-analysis methods.

All routines are deterministic for a fixed input and seed and use only the
Python standard library. They operate on exported numeric samples; they do not
communicate with the PYNQ board or the test chip.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Hashable, Mapping, Sequence


@dataclass(frozen=True)
class AffineCalibration:
    """Least-squares map from a measured ADC value to its reference value.

    ``apply(measured)`` evaluates ``gain * measured + offset``. ``residual_mse``
    is measured on the samples used to fit the calibration.
    """

    gain: float
    offset: float
    sample_count: int
    residual_mse: float

    def apply(self, measured: float) -> float:
        value = float(measured)
        if not math.isfinite(value):
            raise ValueError("measured value must be finite")
        return self.gain * value + self.offset

    def apply_many(self, measured: Sequence[float]) -> tuple[float, ...]:
        return tuple(self.apply(value) for value in measured)


@dataclass(frozen=True)
class MeasurementRequest:
    """One state/repetition requested by the code-conditioned protocol."""

    code: Hashable
    state: Hashable
    repeat_index: int


@dataclass(frozen=True)
class SndrResult:
    """Code-probability-weighted signal-to-noise-and-distortion summary."""

    db: float
    signal_power: float
    error_power: float
    per_code_mse: Mapping[float, float]
    samples_per_code: Mapping[float, int]
    code_probabilities: Mapping[float, float]


def _finite_values(values: Sequence[float], name: str) -> tuple[float, ...]:
    converted = tuple(float(value) for value in values)
    if not converted:
        raise ValueError(f"{name} must not be empty")
    if not all(math.isfinite(value) for value in converted):
        raise ValueError(f"{name} must contain only finite values")
    return converted


def fit_affine_calibration(
    measured: Sequence[float],
    references: Sequence[float],
) -> AffineCalibration:
    """Fit the MMSE affine map ``reference ~= gain * measured + offset``.

    At least two measured levels are required. A zero-variance measured vector
    cannot identify a gain and is rejected.
    """

    x = _finite_values(measured, "measured")
    y = _finite_values(references, "references")
    if len(x) != len(y):
        raise ValueError("measured and references must have the same length")
    if len(x) < 2:
        raise ValueError("at least two calibration samples are required")

    x_mean = math.fsum(x) / len(x)
    y_mean = math.fsum(y) / len(y)
    x_variance_sum = math.fsum((value - x_mean) ** 2 for value in x)
    if x_variance_sum <= 0.0:
        raise ValueError("measured calibration samples must span multiple levels")

    covariance_sum = math.fsum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x, y)
    )
    gain = covariance_sum / x_variance_sum
    offset = y_mean - gain * x_mean
    residual_mse = math.fsum(
        (gain * x_value + offset - y_value) ** 2
        for x_value, y_value in zip(x, y)
    ) / len(x)
    return AffineCalibration(gain, offset, len(x), residual_mse)


def fit_column_calibrations(
    measured_by_column: Mapping[Hashable, Sequence[float]],
    references: Sequence[float],
) -> dict[Hashable, AffineCalibration]:
    """Fit an independent gain and offset for every ADC column.

    The reference sequence is shared, and each column sequence must follow the
    same sample order. This mirrors the paper-level per-column calibration step
    without exposing any board-specific transport or register protocol.
    """

    if not measured_by_column:
        raise ValueError("measured_by_column must not be empty")
    return {
        column: fit_affine_calibration(samples, references)
        for column, samples in measured_by_column.items()
    }


def sample_measurement_protocol(
    states_by_code: Mapping[Hashable, Sequence[Hashable]],
    *,
    states_per_code: int = 30,
    repeats: int = 10,
    seed: int = 0,
    shuffle_requests: bool = True,
) -> tuple[MeasurementRequest, ...]:
    """Select states and expand them into repeated measurement requests.

    The paper protocol uses 30 randomly selected states for each ideal output
    code and measures every selected state 10 times. Defaults therefore create
    300 requests per code. Sampling is without replacement within each code.
    ``seed`` controls both selection and the optional final request shuffle.
    """

    if not states_by_code:
        raise ValueError("states_by_code must not be empty")
    if states_per_code <= 0:
        raise ValueError("states_per_code must be positive")
    if repeats <= 0:
        raise ValueError("repeats must be positive")

    rng = random.Random(seed)
    requests: list[MeasurementRequest] = []
    for code, candidates in states_by_code.items():
        try:
            unique_candidates = tuple(dict.fromkeys(candidates))
        except TypeError as exc:
            raise TypeError("measurement states must be hashable") from exc
        if len(unique_candidates) < states_per_code:
            raise ValueError(
                f"code {code!r} provides {len(unique_candidates)} unique states; "
                f"{states_per_code} are required"
            )
        selected = rng.sample(unique_candidates, states_per_code)
        for state in selected:
            for repeat_index in range(repeats):
                requests.append(MeasurementRequest(code, state, repeat_index))

    if shuffle_requests:
        rng.shuffle(requests)
    return tuple(requests)


def signed_dot_product_code_probabilities(
    dimension: int,
    *,
    positive_probability: float = 0.5,
) -> dict[int, float]:
    """Return the code distribution for a sum of signed +/-1 products.

    For ``dimension=N``, the supported codes are ``-N, -N+2, ..., N``. If an
    individual signed product is positive with probability ``p``, code
    ``c = 2k-N`` has probability ``comb(N, k) p**k (1-p)**(N-k)``. The paper's
    methodology uses the default ``p=0.5`` binomial distribution.
    """

    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension <= 0:
        raise ValueError("dimension must be a positive integer")
    probability = float(positive_probability)
    if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("positive_probability must be finite and within [0, 1]")

    distribution = {
        2 * positive_count - dimension: (
            math.comb(dimension, positive_count)
            * probability**positive_count
            * (1.0 - probability) ** (dimension - positive_count)
        )
        for positive_count in range(dimension + 1)
    }
    total = math.fsum(distribution.values())
    if total <= 0.0:
        raise ValueError("the requested distribution underflowed to zero")
    return {code: weight / total for code, weight in distribution.items()}


def code_conditioned_sndr(
    ideal_codes: Sequence[float],
    estimates: Sequence[float],
    *,
    code_probabilities: Mapping[float, float] | None = None,
) -> SndrResult:
    """Compute code-conditioned SNDR using explicit or empirical code weights.

    The denominator is ``sum(P(c) * MSE_code(c))`` and the numerator is the
    variance of the ideal code under the same normalized distribution ``P``.
    This matches the paper methodology when ``code_probabilities`` is supplied
    by :func:`signed_dot_product_code_probabilities`.

    If ``code_probabilities`` is omitted, the documented default is the
    empirical code frequency in ``ideal_codes``. Supplied values may be either
    probabilities or arbitrary nonnegative weights; they are normalized. Every
    positive-weight code must have measured samples. Equal-code weighting is
    available explicitly by passing the same positive weight for every code.
    """

    codes = _finite_values(ideal_codes, "ideal_codes")
    measured = _finite_values(estimates, "estimates")
    if len(codes) != len(measured):
        raise ValueError("ideal_codes and estimates must have the same length")

    squared_errors: dict[float, list[float]] = {}
    for code, estimate in zip(codes, measured):
        squared_errors.setdefault(code, []).append((estimate - code) ** 2)

    levels = tuple(squared_errors)
    if len(levels) < 2:
        raise ValueError("SNDR requires at least two distinct ideal code levels")

    per_code_mse = {
        code: math.fsum(errors) / len(errors)
        for code, errors in squared_errors.items()
    }
    samples_per_code = {code: len(errors) for code, errors in squared_errors.items()}
    if code_probabilities is None:
        total_samples = len(codes)
        probabilities = {
            code: count / total_samples
            for code, count in samples_per_code.items()
        }
    else:
        supplied: dict[float, float] = {}
        for code, weight in code_probabilities.items():
            numeric_code = float(code)
            numeric_weight = float(weight)
            if not math.isfinite(numeric_code):
                raise ValueError("code probability keys must be finite numeric codes")
            if not math.isfinite(numeric_weight) or numeric_weight < 0.0:
                raise ValueError("code probabilities must be finite and nonnegative")
            supplied[numeric_code] = numeric_weight
        unmeasured = [
            code
            for code, weight in supplied.items()
            if weight > 0.0 and code not in per_code_mse
        ]
        if unmeasured:
            raise ValueError(
                "positive-probability codes have no measurements: "
                + ", ".join(str(code) for code in sorted(unmeasured))
            )
        missing = [code for code in per_code_mse if code not in supplied]
        if missing:
            raise ValueError(
                "code_probabilities is missing measured codes: "
                + ", ".join(str(code) for code in sorted(missing))
            )
        total_weight = math.fsum(supplied.values())
        if total_weight <= 0.0:
            raise ValueError("code probabilities must have positive total weight")
        probabilities = {
            code: supplied[code] / total_weight
            for code in per_code_mse
        }

    weighted_mean = math.fsum(
        probabilities[code] * code for code in per_code_mse
    )
    signal_power = math.fsum(
        probabilities[code] * (code - weighted_mean) ** 2
        for code in per_code_mse
    )
    if signal_power <= 0.0:
        raise ValueError("weighted ideal code distribution must have nonzero signal power")
    error_power = math.fsum(
        probabilities[code] * mse for code, mse in per_code_mse.items()
    )
    db = math.inf if error_power == 0.0 else 10.0 * math.log10(signal_power / error_power)
    return SndrResult(
        db,
        signal_power,
        error_power,
        per_code_mse,
        samples_per_code,
        probabilities,
    )
