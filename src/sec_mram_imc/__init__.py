"""Measurement-method helpers for the SEC-enabled MRAM IMC project.

The package implements deterministic protocol sampling, per-column affine
calibration, signed-code probabilities, compute SNDR, and a synthetic SEC
illustration.
"""

from .measurement import (
    AffineCalibration,
    MeasurementRequest,
    SndrResult,
    code_conditioned_sndr,
    fit_affine_calibration,
    fit_column_calibrations,
    sample_measurement_protocol,
    signed_dot_product_code_probabilities,
)
from .synthetic_sec import (
    SYNTHETIC_DEMO_LABEL,
    SyntheticSecFit,
    apply_synthetic_correction,
    learn_synthetic_correction_factors,
)

__all__ = [
    "AffineCalibration",
    "MeasurementRequest",
    "SYNTHETIC_DEMO_LABEL",
    "SndrResult",
    "SyntheticSecFit",
    "apply_synthetic_correction",
    "code_conditioned_sndr",
    "fit_affine_calibration",
    "fit_column_calibrations",
    "learn_synthetic_correction_factors",
    "sample_measurement_protocol",
    "signed_dot_product_code_probabilities",
]
