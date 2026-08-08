"""A synthetic correction-factor learner for inspecting SEC mechanics.

The deterministic batch-gradient example shows how shared multiplicative
factors learn systematic row attenuation before fixed-point hardware mapping.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


SYNTHETIC_DEMO_LABEL = (
    "Synthetic method demo: deterministic protocol data and an illustrative "
    "multiplicative correction-factor learner."
)


@dataclass(frozen=True)
class SyntheticSecFit:
    """Result of the educational batch-gradient correction fit."""

    factors: tuple[float, ...]
    initial_mse: float
    final_mse: float
    epochs: int
    learning_rate: float

    def predict(self, observed_contributions: Sequence[float]) -> float:
        return apply_synthetic_correction(observed_contributions, self.factors)


def _validated_matrix(
    observed_contributions: Sequence[Sequence[float]],
) -> tuple[tuple[float, ...], ...]:
    if not observed_contributions:
        raise ValueError("observed_contributions must not be empty")
    rows = tuple(tuple(float(value) for value in row) for row in observed_contributions)
    width = len(rows[0])
    if width == 0:
        raise ValueError("observed_contributions must have at least one feature")
    if any(len(row) != width for row in rows):
        raise ValueError("all contribution rows must have the same width")
    if not all(math.isfinite(value) for row in rows for value in row):
        raise ValueError("observed_contributions must contain only finite values")
    return rows


def apply_synthetic_correction(
    observed_contributions: Sequence[float],
    factors: Sequence[float],
) -> float:
    """Apply illustrative row factors and sum the corrected contributions."""

    contributions = tuple(float(value) for value in observed_contributions)
    weights = tuple(float(value) for value in factors)
    if len(contributions) != len(weights):
        raise ValueError("observed_contributions and factors must have the same length")
    if not contributions:
        raise ValueError("at least one contribution is required")
    if not all(math.isfinite(value) for value in contributions + weights):
        raise ValueError("contributions and factors must be finite")
    return math.fsum(value * factor for value, factor in zip(contributions, weights))


def _mse(
    rows: Sequence[Sequence[float]],
    targets: Sequence[float],
    factors: Sequence[float],
) -> float:
    return math.fsum(
        (apply_synthetic_correction(row, factors) - target) ** 2
        for row, target in zip(rows, targets)
    ) / len(rows)


def learn_synthetic_correction_factors(
    observed_contributions: Sequence[Sequence[float]],
    ideal_outputs: Sequence[float],
    *,
    epochs: int = 400,
    learning_rate: float = 0.5,
    l2_to_unity: float = 0.0,
    minimum_factor: float = 0.0,
    maximum_factor: float = 4.0,
) -> SyntheticSecFit:
    """Learn shared multiplicative factors in a synthetic batch-gradient demo.

    Each input row contains already-observed row contributions. Prediction is
    ``sum(gamma[i] * contribution[i])``. The gradient step is normalized by
    aggregate feature energy to remain stable across small demo dimensions.

    This public routine intentionally omits hardware registers, fixed-point
    formats, update scheduling, and board communication. It must not be treated
    as the fabricated controller's implementation.
    """

    rows = _validated_matrix(observed_contributions)
    targets = tuple(float(value) for value in ideal_outputs)
    if len(rows) != len(targets):
        raise ValueError("observed_contributions and ideal_outputs must align")
    if not targets or not all(math.isfinite(value) for value in targets):
        raise ValueError("ideal_outputs must contain finite values")
    if epochs <= 0:
        raise ValueError("epochs must be positive")
    if learning_rate <= 0.0 or not math.isfinite(learning_rate):
        raise ValueError("learning_rate must be finite and positive")
    if l2_to_unity < 0.0 or not math.isfinite(l2_to_unity):
        raise ValueError("l2_to_unity must be finite and nonnegative")
    if minimum_factor > maximum_factor:
        raise ValueError("minimum_factor must not exceed maximum_factor")

    width = len(rows[0])
    factors = [1.0] * width
    initial_mse = _mse(rows, targets, factors)
    sample_count = len(rows)
    feature_energy = math.fsum(
        math.fsum(row[index] ** 2 for row in rows) / sample_count
        for index in range(width)
    )
    normalized_step = learning_rate / max(1.0, feature_energy)

    for _ in range(epochs):
        errors = [
            math.fsum(factor * value for factor, value in zip(factors, row)) - target
            for row, target in zip(rows, targets)
        ]
        gradients = [
            2.0
            * math.fsum(error * row[index] for error, row in zip(errors, rows))
            / sample_count
            + 2.0 * l2_to_unity * (factors[index] - 1.0)
            for index in range(width)
        ]
        factors = [
            min(maximum_factor, max(minimum_factor, factor - normalized_step * gradient))
            for factor, gradient in zip(factors, gradients)
        ]

    final_factors = tuple(factors)
    return SyntheticSecFit(
        final_factors,
        initial_mse,
        _mse(rows, targets, final_factors),
        epochs,
        learning_rate,
    )
