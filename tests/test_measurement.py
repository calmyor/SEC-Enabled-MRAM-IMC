from __future__ import annotations

from collections import Counter
import math
import unittest

from sec_mram_imc import (
    code_conditioned_sndr,
    fit_affine_calibration,
    fit_column_calibrations,
    sample_measurement_protocol,
    signed_dot_product_code_probabilities,
)


class CalibrationTests(unittest.TestCase):
    def test_affine_fit_recovers_reference_map(self) -> None:
        references = (-2.0, -1.0, 0.0, 1.0, 2.0)
        measured = tuple(2.5 * value - 0.75 for value in references)
        calibration = fit_affine_calibration(measured, references)

        self.assertAlmostEqual(calibration.gain, 0.4)
        self.assertAlmostEqual(calibration.offset, 0.3)
        self.assertLess(calibration.residual_mse, 1e-24)
        self.assertEqual(calibration.apply_many(measured), references)

    def test_independent_column_calibration(self) -> None:
        references = (-1.0, 0.0, 1.0)
        calibrations = fit_column_calibrations(
            {
                "a": (-1.5, 0.5, 2.5),
                "b": (-3.0, -1.0, 1.0),
            },
            references,
        )
        self.assertAlmostEqual(calibrations["a"].apply(2.5), 1.0)
        self.assertAlmostEqual(calibrations["b"].apply(-3.0), -1.0)


class ProtocolTests(unittest.TestCase):
    def test_default_protocol_is_seeded_and_has_300_requests_per_code(self) -> None:
        states = {
            0: tuple(f"zero-{index}" for index in range(40)),
            1: tuple(f"one-{index}" for index in range(40)),
        }
        first = sample_measurement_protocol(states, seed=7)
        second = sample_measurement_protocol(states, seed=7)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 600)
        self.assertEqual(Counter(request.code for request in first), {0: 300, 1: 300})
        selected = {
            code: {request.state for request in first if request.code == code}
            for code in states
        }
        self.assertEqual({code: len(values) for code, values in selected.items()}, {0: 30, 1: 30})
        self.assertTrue(all(0 <= request.repeat_index < 10 for request in first))

    def test_protocol_rejects_too_few_unique_states(self) -> None:
        with self.assertRaisesRegex(ValueError, "unique states"):
            sample_measurement_protocol({0: ("a", "a")}, states_per_code=2)


class SndrTests(unittest.TestCase):
    def test_default_uses_empirical_code_probabilities(self) -> None:
        result = code_conditioned_sndr(
            (-1.0, -1.0, -1.0, 1.0),
            (-2.0, -1.0, -1.0, 3.0),
        )

        self.assertEqual(result.code_probabilities, {-1.0: 0.75, 1.0: 0.25})
        self.assertAlmostEqual(result.signal_power, 0.75)
        self.assertAlmostEqual(result.per_code_mse[-1.0], 1.0 / 3.0)
        self.assertAlmostEqual(result.per_code_mse[1.0], 4.0)
        self.assertAlmostEqual(result.error_power, 1.25)
        self.assertAlmostEqual(result.db, 10.0 * math.log10(0.75 / 1.25))

    def test_explicit_weights_are_normalized_and_control_sndr(self) -> None:
        result = code_conditioned_sndr(
            (-1.0, -1.0, -1.0, 1.0),
            (-2.0, -1.0, -1.0, 3.0),
            code_probabilities={-1.0: 1.0, 1.0: 1.0},
        )

        self.assertEqual(result.code_probabilities, {-1.0: 0.5, 1.0: 0.5})
        self.assertAlmostEqual(result.signal_power, 1.0)
        self.assertAlmostEqual(result.error_power, (1.0 / 3.0 + 4.0) / 2.0)

    def test_signed_dot_product_distribution_matches_binomial(self) -> None:
        distribution = signed_dot_product_code_probabilities(4)

        self.assertEqual(tuple(distribution), (-4, -2, 0, 2, 4))
        expected = {-4: 1 / 16, -2: 4 / 16, 0: 6 / 16, 2: 4 / 16, 4: 1 / 16}
        for code, probability in expected.items():
            self.assertAlmostEqual(distribution[code], probability)
        mean = math.fsum(code * probability for code, probability in distribution.items())
        variance = math.fsum(
            probability * (code - mean) ** 2
            for code, probability in distribution.items()
        )
        self.assertAlmostEqual(variance, 4.0)

    def test_zero_error_has_infinite_sndr(self) -> None:
        result = code_conditioned_sndr((-1.0, 1.0), (-1.0, 1.0))
        self.assertTrue(math.isinf(result.db))


if __name__ == "__main__":
    unittest.main()
