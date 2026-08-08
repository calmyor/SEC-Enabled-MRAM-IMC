# Parasitic-aware behavioral model

## Purpose

The behavioral model is the bridge from transistor/circuit behavior to the SEC architecture. It answers:

- how much each activated MRAM row contributes after BL/SL voltage loss;
- how MTJ variation, read noise, and ADC quantization combine;
- how error changes with dot-product dimension and activation location;
- whether a low-dimensional correction can compensate the dominant structure; and
- which fixed-point widths preserve the learning trajectory.

Its output is a compact description of the dominant structured error: a spatial attenuation field that the on-chip correction can learn economically.

## Signal path represented

| Layer | Public model concept | Design question |
|---|---|---|
| Device | Parallel/antiparallel conductance and MTJ variability | How wide is the physical state distribution? |
| Array | BL/SL series resistance and row location | How does contribution change with physical position? |
| Weight formation | Differential signed representation and binary column weighting | How do physical columns compose one logical 4-bit weight? |
| Readout | Sensor noise and column gain/offset | Is the useful current step resolvable? |
| Conversion | 6-bit ADC range, clipping, and quantization | Is added precision useful or analog-noise limited? |
| SEC | Shared row scaling and column normalization | How much structured error can be removed economically? |

For a signed dot product, the nonideal output can be abstracted as

```text
y_j = sum_i alpha_ij * w_ij * x_i + readout/quantization error
```

where `alpha_ij` is an effective, location-dependent attenuation term inferred from behavior. SEC approximates this field with shared row factors and per-column normalization instead of storing a rows × columns correction matrix.

## Why location matters

At `N=128`, the paper gives an 80 µS state step in a nominal 20 mS column, only 0.4%. BL/SL drops therefore create a meaningful fraction of the signal. Two activation vectors with the same ideal dot product can distribute current differently along the array and produce different measured outputs. The effect is particularly visible near zero output, where relative distortion can be large.

## Recommended experiment sequence

1. **Ideal arithmetic:** verify sign convention, bit significance, differential mapping, and reachable codes.
2. **ADC only:** add clipping and quantization; sweep range and precision.
3. **Device variation only:** use fixed seeds and separate within-device from across-device effects.
4. **Read noise only:** repeat identical states to expose temporal variation.
5. **BL resistance only:** compare near/far and randomized row patterns at equal ideal code.
6. **SL resistance only:** repeat the controlled pattern comparison.
7. **Combined array:** sweep dimension, current/bias, clock, and code.
8. **Circuit correlation:** compare controlled behavioral vectors against circuit-simulation CSV exports.
9. **SEC floating point:** establish attainable correction and convergence.
10. **SEC fixed point:** sweep clipping, rounding, widths, learning rate, and seeds.

Change one nonideality at a time before relying on the combined result. Preserve the vector, seed, configuration, and output for every correlation run.

## Validation invariants

- Zero parasitics/noise/variation must reduce to the ideal dot product within the declared ADC behavior.
- Swapping differential logical weights must obey the defined sign convention.
- Increasing BL/SL resistance must not silently improve the ideal-to-analog mapping.
- Repeated identical states vary only through enabled temporal sources.
- Different states with equal ideal code remain distinguishable in the raw record.
- Clipping is counted as distortion, not discarded as an outlier.
- Fixed-point update order and saturation match the hardware specification cycle by cycle.
- Every plotted aggregate can be regenerated from stored numeric outputs.

## Reproduction package

The public behavioral-model layer is organized around the equations, controlled
experiment sequence, and validation invariants above. The runnable package adds
calibration, code probabilities, SNDR, and a synthetic SEC illustration. A
calibrated model release binds the same structure to:

- versioned device, interconnect, sensor, and ADC parameters with provenance;
- a declared environment and random seeds;
- ideal-limit and edge-case unit tests;
- small circuit-correlation fixtures;
- floating- and fixed-point SEC traces; and
- a command that regenerates each model figure from stored numeric output.

Use the evidence label **behavioral model** for calibrated model sweeps and
**synthetic** for the public toy parameters. Measured-silicon values retain the
separate **silicon measurement** label.
