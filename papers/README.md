# Papers and research evolution

## ESSCIRC 2023

S. K. Roy, H.-M. Ou, M. G. Ahmed, P. Deaville, B. Zhang, N. Verma, P. K. Hanumolu, and N. R. Shanbhag, “Compute SNR-boosted 22 nm MRAM-based in-memory computing macro using statistical error compensation,” *ESSCIRC 2023—IEEE 49th European Solid State Circuits Conference*, pp. 25–28, 2023.

- DOI: <https://doi.org/10.1109/ESSCIRC59616.2023.10268688>
- IEEE Xplore: <https://ieeexplore.ieee.org/document/10268688>

The conference paper introduces the macro, OCCS and SEC approach, measured 2.7–6 dB SNR improvement, 5× iso-SNR energy trade-off, and bounded CIFAR-10 last-layer result.

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
- the final-layer ResNet-20 experiment and its limitations.

## Reading and terminology notes

- The conference paper uses **SNR**; the journal extension uses **SNDR** to include distortion.
- SEC means **statistical error compensation**, not single-error correction.
- SEC training learns hardware correction factors; it does not train network weights.
- The physical array is 1T1R. A differential 2T2R logical representation implements signed weights.
- The CIFAR-10 result maps only the last fully connected layer, not the full ResNet-20.
- The 3.7% SRAM-based SEC area is projected. The fabricated implementation is 12.2%.
- The 3.8%–8.4% OCCS variation and approximate 17% sensor overhead are simulated.
- “First work” language should be attributed to the authors unless independently reviewed.

## Venue clarification

The source collection supports ESSCIRC 2023 and the JSSC extension. It does not contain an ISCA paper for this macro; ISSCC papers appear as cited prior art.

The earlier modeling lineage includes “Fundamental Limits on the Computational Accuracy of Resistive Crossbar-Based In-Memory Architectures,” ISCAS 2022: <https://doi.org/10.1109/ISCAS48785.2022.9937336>.

## Local paper files

The audited working archive contains manuscript LaTeX and figure PDFs, but no verified public compiled paper PDF. This repository links the publisher records rather than distributing a locally compiled manuscript as the version of record.
