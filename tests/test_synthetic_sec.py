from __future__ import annotations

from itertools import product
import unittest

from sec_mram_imc import (
    PUBLIC_SAFETY_NOTICE,
    learn_synthetic_correction_factors,
)


class SyntheticSecTests(unittest.TestCase):
    def test_fit_learns_inverse_row_attenuation(self) -> None:
        attenuation = (0.55, 0.70, 0.82, 0.91)
        states = tuple(product((-1.0, 1.0), repeat=len(attenuation)))
        observed = tuple(
            tuple(scale * value for scale, value in zip(attenuation, state))
            for state in states
        )
        targets = tuple(sum(state) for state in states)

        fit = learn_synthetic_correction_factors(observed, targets, epochs=300)

        self.assertIn("Synthetic method demo only", PUBLIC_SAFETY_NOTICE)
        self.assertLess(fit.final_mse, fit.initial_mse * 1e-6)
        for learned, scale in zip(fit.factors, attenuation):
            self.assertAlmostEqual(learned, 1.0 / scale, places=5)


if __name__ == "__main__":
    unittest.main()

