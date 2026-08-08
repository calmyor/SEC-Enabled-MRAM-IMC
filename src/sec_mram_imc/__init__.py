"""Public-safe measurement helpers for the SEC-enabled MRAM IMC project.

The package reconstructs paper-level analysis methods. It does not contain the
test-chip bitstream, foundry collateral, or the proprietary hardware controller.
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
    PUBLIC_SAFETY_NOTICE,
    SyntheticSecFit,
    apply_synthetic_correction,
    learn_synthetic_correction_factors,
)

__all__ = [
    "AffineCalibration",
    "MeasurementRequest",
    "PUBLIC_SAFETY_NOTICE",
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
