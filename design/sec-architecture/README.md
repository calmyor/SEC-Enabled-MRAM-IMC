# SEC and OCCS architecture

## Statistical error compensation

SEC factors the dominant parasitic distortion into values practical to learn and store:

```text
calibrated_output_j = theta_j * sum_i gamma_i * alpha_ij * w_ij * x_i
target: theta_j * gamma_i * alpha_ij ≈ 1 statistically
```

- `alpha_ij`: effective attenuation for row `i`, column `j`.
- `gamma_i`: learned input-side correction shared across ADC columns.
- `theta_j`: output-side normalization for ADC column `j`.

A full correction matrix would scale with rows × columns. Sharing `gamma_i` across columns makes the storage and multiply path proportional primarily to row count, while `theta_j` absorbs column gain.

## Learning and inference roles

### Learning/calibration phase

1. Apply controlled training patterns with known target output.
2. Measure the calibrated column response.
3. Form an error relative to the ideal target.
4. Update row factors through the hardware-defined stochastic-gradient path.
5. Clip/quantize state using the same fixed-point rules as the implemented datapath.
6. Stop on the defined iteration or convergence rule and freeze the factors.

This phase learns correction state for the hardware. It does **not** update neural-network weights.

### Inference phase

1. Retrieve the frozen 7-bit row factor.
2. Scale the corresponding input contribution.
3. Execute the 1-bit-input × 4-bit-weight MRAM dot product.
4. Convert through the 6-bit ADC path.
5. Apply per-column calibration/normalization for analysis.

Multibit activations are processed bit-serially.

## Fixed-point choices

| Quantity | Reported implementation | Reason |
|---|---:|---|
| Inference scale `gamma` | 7 bit | Preserves correction quality with bounded multiplier/storage cost |
| Update accumulator | 14 bit | Retains smaller learning increments and convergence range |
| Learning rate `mu` | Power of two | Implements scaling with a shift |
| ADC output | 6 bit | Balances conversion overhead with analog-noise/distortion limits |

The widths come from floating- versus fixed-point convergence studies. They are not generic optimum values for every eNVM array.

## Offset-compensated current sensing (OCCS)

SEC addresses structured array nonlinearity; OCCS reduces a different error source: static readout mismatch and PVT sensitivity.

- A resistor is used for level shifting in place of the prior transistor implementation.
- An auto-zero phase captures static offset.
- An evaluation phase senses the array current after compensation.
- The bitline operating point is held more consistently across columns.

The paper reports 3.8%–8.4% bitline-voltage variation and about 17% sensor area overhead from Monte Carlo **simulation**. These are not fabricated-macro measurements.

## Integrated macro organization

- 512 × 512 physical 1T1R MRAM array (32 kB).
- Differential 2T2R logical representation for signed weights.
- Four binary-weighted physical columns per ADC column.
- 128 parallel ADC columns.
- 6-bit SAR ADC and local sequencing.
- SEC processor with 12.2% fabricated area overhead.

The paper projects that replacing register-heavy SEC storage with SRAM could reduce overhead to 3.7%; that number is a projection, not measured silicon.

## Verification checklist

- Golden α/γ/θ vectors shared among behavioral, fixed-point, RTL, and analysis models.
- Explicit saturation, rounding, sign extension, reset, update order, and overflow behavior.
- OCCS auto-zero/evaluate timing checked against array/ADC sequencing.
- Training and inference memories/registers protected from unintended overlap.
- Power-of-two learning-rate shift verified for negative values and rounding.
- Scan/register access can observe SEC state and bypass correction.
- SEC-off and SEC-on modes use the same measurement/calibration population.
- Simulated, measured, and projected results remain labeled separately.
