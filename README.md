# SEC-Enabled 22 nm MRAM In-Memory Computing

[![Pages](https://github.com/calmyor/SEC-Enabled-MRAM-IMC/actions/workflows/pages.yml/badge.svg)](https://github.com/calmyor/SEC-Enabled-MRAM-IMC/actions/workflows/pages.yml)
[![Validate](https://github.com/calmyor/SEC-Enabled-MRAM-IMC/actions/workflows/validate.yml/badge.svg)](https://github.com/calmyor/SEC-Enabled-MRAM-IMC/actions/workflows/validate.yml)

This repository documents the engineering path behind a measured **22 nm MRAM in-memory-computing (IMC) macro with statistical error compensation (SEC)**: behavioral modeling, SEC/OCCS co-design, fixed-point architecture, mixed-signal tapeout considerations, PCB and PYNQ-Z2 testing, code-conditioned compute-SNDR measurement, and the ESSCIRC/JSSC publication record.

**Project website:** <https://calmyor.github.io/SEC-Enabled-MRAM-IMC/>

## Headline measured results

| Item | Reported value |
|---|---:|
| Process and supply | Commercial 22 nm FD-SOI, 0.8 V |
| Physical MRAM array | 512 × 512 1T1R cells (32 kB) |
| ADC columns | 128, 6-bit SAR |
| Dot-product modes | N = 64 and 128 |
| SEC-enabled compute-SNDR improvement | 2.7–6 dB across evaluated operating points |
| Energy trade-off | 5× reduction per 1-bit operation at iso-SNDR |
| SEC overhead | 12.2% fabricated area; 0.8% energy at N=64 and 1.8% at N=128 |
| CIFAR-10 / ResNet-20 final-layer mapping | 74.8% ±5% to 82.0% ±5% at 90% confidence |

The network experiment maps the **final fully connected layer** to measured hardware while the preceding ResNet-20 layers run in software. SEC learns hardware correction factors with the network weights fixed. See [Measurements](measurements/README.md) for the sampling, calibration, and confidence protocol.

## Engineering chain

1. **Expose the signal limit.** A behavioral model combines MTJ variation, BL/SL parasitics, read noise, binary column weighting, and ADC quantization.
2. **Capture its spatial structure.** Location-dependent attenuation is represented by αᵢⱼ.
3. **Compensate economically.** SEC learns a shared per-row input factor γᵢ and uses per-column normalization θⱼ, targeting θⱼγᵢαᵢⱼ ≈ 1.
4. **Map the algorithm to hardware.** Quantization studies select a 7-bit inference scale, 14-bit update accumulator, and power-of-two learning rate.
5. **Stabilize the sensor.** Offset-compensated current sensing (OCCS) reduces readout mismatch and PVT sensitivity before conversion.
6. **Realize and exercise the macro.** The 22 nm chip is packaged in QFN64 and connected through Python → PYNQ-Z2 → custom PCB → chip.
7. **Measure by ideal code.** Independent per-column MMSE calibration and 30 states/code × 10 repeats estimate probability-weighted compute SNDR.

Read the detailed [behavioral-model guide](design/behavioral-model/README.md), [SEC/OCCS architecture guide](design/sec-architecture/README.md), [tapeout process guide](tapeout/process-guide/README.md), [PCB guide](hardware/pcb/README.md), and [PYNQ guide](hardware/pynq/README.md).

## Runnable analysis path

The standard-library-only Python package follows the measurement record from calibration through the paper's SNDR metric:

- independent per-column affine MMSE calibration;
- deterministic code-conditioned state/repetition requests;
- probability-weighted compute-SNDR;
- binomial probabilities for signed ±1 dot-product codes; and
- a synthetic multiplicative-correction illustration for inspecting the SEC mechanism.

The hardware transaction path is specified separately in the [PYNQ control guide](hardware/pynq/README.md), while this package keeps the numerical methods deterministic and directly testable.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 examples/protocol_demo.py
```

Run the tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Build and validate the static website:

```bash
node scripts/build-site.mjs
node scripts/validate-site.mjs
```

## Repository structure

```text
website/                 editable site source and reviewed visual assets
docs/                    generated GitHub Pages output
src/sec_mram_imc/        public analysis-method package
examples/                deterministic synthetic demonstration
tests/                   unit tests
measurements/            protocol and interpretation guide
design/                  behavioral-model and SEC/OCCS design principles
hardware/                PCB and PYNQ engineering records
tapeout/process-guide/   mixed-signal tapeout workflow and exit evidence
data/                    public schema and example-data policy
papers/                  citations and conference-to-journal evolution
provenance/              artifact roles, evidence classes, and handoff paths
```

## Evidence map

Every result is paired with the artifact type that supports it:

| Evidence class | What it answers | Repository entry point |
|---|---|---|
| Silicon measurement | What the fabricated macro and system produced | [Measurement method](measurements/README.md) and primary papers |
| Circuit simulation / Monte Carlo | How OCCS behaves across modeled mismatch and PVT | [SEC/OCCS architecture](design/sec-architecture/README.md) |
| Behavioral model | Why location-dependent attenuation emerges and how SEC responds | [Behavioral-model guide](design/behavioral-model/README.md) |
| Projection | How an alternative SRAM-backed SEC implementation changes area | [SEC/OCCS architecture](design/sec-architecture/README.md) |
| Synthetic example | How to run and inspect the public numerical methods | `examples/protocol_demo.py` and `tests/` |
| Engineering record | How the chip, board, FPGA, and tapeout stages connect | `tapeout/` and `hardware/` guides |

The complete artifact-by-artifact handoff is in [ARTIFACTS.md](provenance/ARTIFACTS.md).

## Publication sequence

- S. K. Roy *et al.*, “Fundamental Limits on the Computational Accuracy of Resistive Crossbar-Based In-Memory Architectures,” **ISCAS 2022**. This establishes the modeling foundation for signal-loss analysis. <https://doi.org/10.1109/ISCAS48785.2022.9937336>

- S. K. Roy *et al.*, “Compute SNR-boosted 22 nm MRAM-based in-memory computing macro using statistical error compensation,” **ESSCIRC 2023**, pp. 25–28. <https://doi.org/10.1109/ESSCIRC59616.2023.10268688>
- S. K. Roy *et al.*, “Compute SNDR-boosted 22-nm MRAM-based in-memory computing macro using statistical error compensation,” **IEEE Journal of Solid-State Circuits**, vol. 60, no. 3, pp. 1092–1102, Mar. 2025 (published online 2024). <https://doi.org/10.1109/JSSC.2024.3442013>

The sequence runs from behavioral limits (ISCAS), to the measured prototype and core SEC result (ESSCIRC), to the complete model–architecture–measurement account (JSSC).

## License and attribution

Original code is available under the [MIT License](LICENSE). Paper figures, photographs, board imagery, paper text, and third-party marks are governed by the terms described in [NOTICE.md](NOTICE.md) and are not relicensed by the MIT grant.

Please use [CITATION.cff](CITATION.cff) and the paper citations above when building on this work.
