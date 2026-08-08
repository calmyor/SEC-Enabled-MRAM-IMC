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

The network experiment maps **only the final fully connected layer** to measured hardware. SEC learns hardware correction factors; it is not neural-network training. See [Measurements](measurements/README.md) for the protocol and interpretation boundary.

## Research chain

1. A behavioral model exposes MTJ variation, BL/SL parasitics, read noise, binary column weighting, and ADC quantization.
2. Location-dependent attenuation is represented by αᵢⱼ.
3. SEC learns a shared per-row input factor γᵢ and uses per-column normalization θⱼ, targeting θⱼγᵢαᵢⱼ ≈ 1.
4. Quantization studies select a 7-bit inference scale and 14-bit update accumulator.
5. Offset-compensated current sensing (OCCS) reduces readout mismatch and PVT sensitivity.
6. The macro is fabricated, packaged in QFN64, and exercised through Python → PYNQ-Z2 → custom PCB → chip.
7. Per-column MMSE calibration and 30 states/code × 10 repeats estimate compute SNDR.

Read the detailed [behavioral-model guide](design/behavioral-model/README.md), [SEC/OCCS architecture guide](design/sec-architecture/README.md), [tapeout process guide](tapeout/process-guide/README.md), [PCB guide](hardware/pcb/README.md), and [PYNQ guide](hardware/pynq/README.md).

## What is executable here

The public, standard-library-only Python package implements:

- independent per-column affine MMSE calibration;
- deterministic code-conditioned state/repetition requests;
- probability-weighted compute-SNDR;
- binomial probabilities for signed ±1 dot-product codes; and
- an explicitly synthetic multiplicative-correction illustration.

It **does not** communicate with the chip or reproduce proprietary controller RTL, PYNQ firmware, analog behavior, or measured data.

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
hardware/                PCB and PYNQ engineering/release boundaries
tapeout/process-guide/   sanitized mixed-signal tapeout workflow
data/                    public schema and example-data policy
papers/                  citations and conference-to-journal evolution
provenance/              artifact availability and release decisions
```

## Artifact boundary

The private working collection is not published wholesale. It interleaves legitimate research artifacts with foundry-confidential configuration/validator material, export paperwork, invoices, shipping records, vendor packages, obsolete board revisions, machine-specific identifiers, raw data, and code without a confirmed redistribution license.

| Tier | Meaning | Examples |
|---|---|---|
| Public source | Reviewed and licensed for this repository | Website, method package, tests, new engineering guides |
| Sanitized derivative | New or reviewed public representation | Selected paper figures, board visual, process checklists |
| Hardware-dependent | Real artifact whose execution requires unavailable/specific hardware | Historical overlay/notebook workflow, described but not distributed here |
| Restricted / unavailable | Confidential, identifying, incomplete, or unlicensed | PDK, GDS/netlists, rule reports, waivers, invoices, raw lab archive |

The collection does not contain a complete reproducible FPGA build (custom RTL/XDC/build Tcl are missing) or an open RTL-to-GDS/signoff flow. This repository makes neither claim. See [ARTIFACTS.md](provenance/ARTIFACTS.md).

## Primary papers

- S. K. Roy *et al.*, “Compute SNR-boosted 22 nm MRAM-based in-memory computing macro using statistical error compensation,” **ESSCIRC 2023**, pp. 25–28. <https://doi.org/10.1109/ESSCIRC59616.2023.10268688>
- S. K. Roy *et al.*, “Compute SNDR-boosted 22-nm MRAM-based in-memory computing macro using statistical error compensation,” **IEEE Journal of Solid-State Circuits**, vol. 60, no. 3, pp. 1092–1102, Mar. 2025 (published online 2024). <https://doi.org/10.1109/JSSC.2024.3442013>

The source collection does not contain an ISCA paper for this macro. ISSCC papers appear as prior art. An earlier ISCAS 2022 paper belongs to the modeling lineage but is not one of the two primary prototype publications.

## License and attribution

Original code is available under the [MIT License](LICENSE). Paper figures, photographs, board imagery, paper text, and third-party marks are governed by the terms described in [NOTICE.md](NOTICE.md) and are not relicensed by the MIT grant.

Please use [CITATION.cff](CITATION.cff) and the paper citations above when building on this work.
