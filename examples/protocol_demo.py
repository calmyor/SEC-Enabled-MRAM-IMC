"""Run a deterministic, synthetic version of the public measurement flow."""

from __future__ import annotations

import random

from sec_mram_imc import (
    SYNTHETIC_DEMO_LABEL,
    code_conditioned_sndr,
    fit_column_calibrations,
    learn_synthetic_correction_factors,
    sample_measurement_protocol,
    signed_dot_product_code_probabilities,
)


def states_for_codes(
    codes: tuple[int, ...],
    *,
    width: int,
    count: int,
    seed: int,
) -> dict[
    int,
    tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
]:
    """Create unique (weight, activation) pairs with requested dot products."""

    rng = random.Random(seed)
    result: dict[int, tuple[tuple[int, ...], ...]] = {}
    for code in codes:
        positive_products = (width + code) // 2
        states: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
        while len(states) < count:
            positive_indices = set(rng.sample(range(width), positive_products))
            products = tuple(
                1 if index in positive_indices else -1
                for index in range(width)
            )
            weights = tuple(rng.choice((-1, 1)) for _ in range(width))
            activations = tuple(
                weight * product
                for weight, product in zip(weights, products)
            )
            states.add((weights, activations))
        result[code] = tuple(sorted(states))
    return result


def main() -> None:
    rng = random.Random(2025)
    width = 16
    attenuation = tuple(0.70 + 0.018 * index for index in range(width))

    training_states = [
        tuple(rng.choice((-1, 1)) for _ in range(width))
        for _ in range(800)
    ]
    training_contributions = [
        tuple(scale * value for scale, value in zip(attenuation, state))
        for state in training_states
    ]
    training_targets = [float(sum(state)) for state in training_states]
    sec_fit = learn_synthetic_correction_factors(
        training_contributions,
        training_targets,
        epochs=500,
    )

    code_probabilities = signed_dot_product_code_probabilities(width)
    states_by_code = states_for_codes(
        tuple(code_probabilities),
        width=width,
        count=45,
        seed=11,
    )
    requests = sample_measurement_protocol(
        states_by_code,
        states_per_code=30,
        repeats=10,
        seed=29,
    )

    front_ends = {
        "adc_column_07": (0.87, 0.35),
        "adc_column_51": (1.08, -0.22),
    }
    reference_levels = tuple(
        float(sum(rng.choice((-1, 1)) for _ in range(width)))
        for _ in range(800)
    )
    calibration_samples = {
        column: tuple(gain * level + offset for level in reference_levels)
        for column, (gain, offset) in front_ends.items()
    }
    calibrations = fit_column_calibrations(calibration_samples, reference_levels)

    codes = tuple(float(request.code) for request in requests)
    raw_sndr: dict[str, float] = {}
    sec_sndr: dict[str, float] = {}
    for column, (front_end_gain, front_end_offset) in front_ends.items():
        raw_estimates: list[float] = []
        corrected_estimates: list[float] = []
        for request in requests:
            weights, activations = request.state
            products = tuple(
                weight * activation
                for weight, activation in zip(weights, activations)
            )
            observed = tuple(
                scale * value
                for scale, value in zip(attenuation, products)
            )
            raw_analog = sum(observed)
            corrected_analog = sec_fit.predict(observed)
            raw_adc = front_end_gain * raw_analog + front_end_offset + rng.gauss(0.0, 0.08)
            sec_adc = front_end_gain * corrected_analog + front_end_offset + rng.gauss(0.0, 0.08)
            raw_estimates.append(calibrations[column].apply(raw_adc))
            corrected_estimates.append(calibrations[column].apply(sec_adc))
        raw_sndr[column] = code_conditioned_sndr(
            codes,
            raw_estimates,
            code_probabilities=code_probabilities,
        ).db
        sec_sndr[column] = code_conditioned_sndr(
            codes,
            corrected_estimates,
            code_probabilities=code_probabilities,
        ).db

    print(SYNTHETIC_DEMO_LABEL)
    print(f"Protocol requests: {len(requests)} ({len(requests) // len(states_by_code)} per code)")
    print(f"SNDR code model: signed +/-1 binomial distribution, N={width}, p=0.5")
    print(f"Synthetic learner MSE: {sec_fit.initial_mse:.5f} -> {sec_fit.final_mse:.5f}")
    for column in front_ends:
        print(
            f"{column}: calibrated raw SNDR={raw_sndr[column]:.2f} dB, "
            f"synthetic SEC SNDR={sec_sndr[column]:.2f} dB"
        )


if __name__ == "__main__":
    main()
