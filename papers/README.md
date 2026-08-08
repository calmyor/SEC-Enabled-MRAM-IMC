# Papers and research relationship

The three publications expose complementary parts of the same model-to-measurement argument:

| Stage | Publication | Contribution to the chain |
|---|---|---|
| Measured prototype | ESSCIRC 2023 | Introduces the 22 nm MRAM macro, OCCS, SEC, and headline silicon results |
| Parallel-bar analysis | JxCDC 2024 | Develops the behavioral/SNDR framework and validates it against the measured prototype |
| Complete account | JSSC 2025 | Connects the parasitic-aware model, fixed-point architecture, macro, measurement protocol, and application result |

The relationship is **JxCDC parallel-bar model ↔ ESSCIRC measured prototype → JSSC complete SEC account**. This is a conceptual map, not a claim about publication order.

## Parallel-bar analytical companion: JxCDC 2024

S. K. Roy and N. R. Shanbhag, “Energy-Accuracy Trade-Offs for Resistive In-Memory Computing Architectures,” *IEEE Journal on Exploratory Solid-State Computational Devices and Circuits*, vol. 10, pp. 22–30, 2024.

- DOI: <https://doi.org/10.1109/JXCDC.2024.3381888>

This paper models the differential resistive parallel-bar signal path across
device variation, BL/SL parasitics, current-mirror mismatch, and ADC noise. It
validates the model against the measured 22 nm MRAM prototype: at `N=64`, a
6-bit ADC, and a 20 mV reference, the reported compute SNDR is 5.17 dB from the
model and 5.15 dB from silicon. The JSSC work then carries the structured array
attenuation into the SEC/OCCS architecture.

## ESSCIRC 2023

S. K. Roy, H.-M. Ou, M. G. Ahmed, P. Deaville, B. Zhang, N. Verma, P. K. Hanumolu, and N. R. Shanbhag, “Compute SNR-boosted 22 nm MRAM-based in-memory computing macro using statistical error compensation,” *ESSCIRC 2023—IEEE 49th European Solid State Circuits Conference*, pp. 25–28, 2023.

- DOI: <https://doi.org/10.1109/ESSCIRC59616.2023.10268688>
- IEEE Xplore: <https://ieeexplore.ieee.org/document/10268688>

The conference paper introduces the macro, OCCS and SEC approach, measured 2.7–6 dB SNR improvement, 5× iso-SNR energy trade-off, and CIFAR-10 final-layer result.

## JSSC journal extension

S. K. Roy, H.-M. Ou, M. G. Ahmed, P. Deaville, B. Zhang, N. Verma, P. K. Hanumolu, and N. R. Shanbhag, “Compute SNDR-boosted 22-nm MRAM-based in-memory computing macro using statistical error compensation,” *IEEE Journal of Solid-State Circuits*, vol. 60, no. 3, pp. 1092–1102, Mar. 2025 (published online 2024).

- DOI: <https://doi.org/10.1109/JSSC.2024.3442013>
- IEEE Xplore: <https://ieeexplore.ieee.org/document/10642976>

The journal paper expands:

- the OCCS circuit operation and simulated mismatch/PVT evidence;
- the parasitic-aware behavioral model;
- the α/γ/θ SEC formulation;
- fixed-point convergence and architecture;
- complete macro organization;
- per-column affine MMSE calibration;
- code-conditioned, probability-weighted compute SNDR;
- measured column variation and energy/SNDR trade-offs; and
- the final-layer ResNet-20 mapping and confidence interval.

## Reading map and evidence labels

- The conference paper uses **SNR**; the journal extension uses **SNDR** to include distortion.
- In this work, SEC expands to **statistical error compensation**.
- SEC training learns hardware correction factors while network weights remain fixed.
- The physical array is 1T1R. A differential 2T2R logical representation implements signed weights.
- **Application mapping:** the CIFAR-10 result maps the final fully connected layer; the preceding ResNet-20 layers run in software.
- **Projection:** SRAM-based SEC storage gives a 3.7% estimated area overhead.
- **Silicon implementation:** the fabricated register-based SEC processor gives 12.2% area overhead.
- **Circuit simulation / Monte Carlo:** OCCS gives 3.8%–8.4% bitline-voltage variation and approximately 17% sensor overhead.
- **Silicon measurement:** SNDR, energy, column variation, and final-layer accuracy values come from the fabricated test path described in the JSSC paper.

## Canonical records

The DOI and IEEE Xplore links above are the citation anchors for the published
papers. The repository's design guides, runnable methods, and reviewed visuals
are reading companions that trace each equation and number to its role in the
model → architecture → silicon → measurement sequence.
