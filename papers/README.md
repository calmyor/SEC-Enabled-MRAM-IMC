# Papers and research sequence

The publication sequence follows the same causal path as the repository:

| Stage | Publication | Contribution to the chain |
|---|---|---|
| Behavioral limits | ISCAS 2022 | Frames how array nonidealities limit resistive-crossbar compute accuracy |
| Measured prototype | ESSCIRC 2023 | Introduces the 22 nm MRAM macro, OCCS, SEC, and headline silicon results |
| Complete account | JSSC 2025 | Connects the parasitic-aware model, fixed-point architecture, macro, measurement protocol, and application result |

## Modeling foundation: ISCAS 2022

S. K. Roy *et al.*, “Fundamental Limits on the Computational Accuracy of Resistive Crossbar-Based In-Memory Architectures,” *ISCAS 2022*.

- DOI: <https://doi.org/10.1109/ISCAS48785.2022.9937336>

This paper supplies the modeling lineage for understanding signal attenuation
and computational accuracy before the MRAM prototype introduces SEC.

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
