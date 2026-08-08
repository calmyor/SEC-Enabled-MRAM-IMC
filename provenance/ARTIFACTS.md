# Artifact roles and provenance map

This map tells readers which artifact to use for each step of the engineering
story. It separates runnable methods, reviewed engineering records, execution
snapshots, publisher records, and technology-controlled implementation evidence
so that each result carries a clear interpretation.

## Artifact map

| Area | Evidence anchor | Repository role | Action it supports |
|---|---|---|---|
| JxCDC parallel-bar analysis | Publisher DOI; model-to-silicon comparison | Analytical companion and citation link | Follow the behavioral/SNDR framework validated against the 22 nm prototype |
| ESSCIRC prototype | Publisher paper; manuscript source and figures in the working record | DOI/citation and reviewed visuals | Read the macro, OCCS/SEC idea, and headline measured result |
| JSSC extension | Publisher paper; manuscript source and figure PDFs in the working record | DOI/citation and reviewed visuals | Follow the complete model–architecture–measurement account |
| Behavioral model | Equations, model/testbench history, and circuit-correlation scripts | Design guide, experiment sequence, and validation invariants | Isolate αᵢⱼ-producing mechanisms and correlate controlled vectors |
| SEC method | α/γ/θ equations, convergence studies, and fixed-point architecture | Architecture guide and synthetic learner | Inspect shared-factor compensation and fixed-point choices |
| Measurement analysis | Calibration/SNDR scripts and acquisition history | Tested standard-library implementation | Generate requests, calibrate each column, group by code, and compute weighted SNDR |
| Measured data | Raw capture arrays and derived analysis in the controlled research record | Public schema and paper-level reported values | Bind a future curated dataset to run, chip, board, overlay, and analysis identities |
| Final TO3 board | Final schematic record, QFN64 bond documents, BOM workbooks, rendering, and setup photographs | Reviewed visual and PCB engineering guide | Trace package pins and execute the bring-up ladder |
| TO2 board history | Editable TO2/QFN80 KiCad revision and older fabrication references | Explicit historical-revision label | Prevent TO2 source from being mixed with the measured TO3 setup |
| PYNQ execution stack | PYNQ-Z2/XC7Z020 metadata, bit/HWH snapshots, notebooks, and pin configuration | Control-path and overlay-identity guide | Identify an executed overlay and migrate transactions into a testable framework |
| Overlay regeneration | Custom HDL, XDC, Vivado project/build Tcl, image, and package lock form one complete unit | Release checklist in the PYNQ guide | Regenerate a bit/HWH pair with matching self-test evidence |
| ASIC implementation | Foundry configuration/validator records, reports, release paperwork, and intermediate summaries | Technology-neutral tapeout gates and exit-evidence ledger | Tie model correlation and signoff to one release-candidate digest |
| Packaging | QFN64 bonding records, package information, and chip photographs | Package/pin trace in PCB and tapeout guides | Carry die orientation and signal identity into the board |

## Recorded artifact state

This is the single inventory view for the audited working record; the topical
guides can therefore concentrate on engineering use.

| Area | Recorded state | Complete public handoff unit |
|---|---|---|
| Behavioral model | Working model/testbench and circuit-correlation scripts include collaborator and process-derived context | Reviewed source license, parameter provenance, environment, fixtures, tests, and figure-regeneration command |
| TO3 PCB | Final schematic record, QFN64 bonding documents, BOM workbooks, rendering, and photographs; the editable files located in audit are the older TO2/QFN80 revision | Matching editable TO3/QFN64 design, fabrication/assembly bundle, pin/rail map, and bring-up manifest |
| PYNQ overlay | Historical bit/HWH pairs, notebooks, target/tool/clock metadata, and pin-configuration record | Matching HDL, XDC, Vivado project/build Tcl, exact image/package lock, digests, and self-tests |
| Raw measurements | Capture arrays and derived outputs remain in the controlled research record | Curated dataset, schema, run manifests, aliases, deduplication, license, and archive digest |
| ASIC release | Foundry configuration/validator material, detailed reports, intermediate summaries, and release paperwork | Licensed source/IP, RTL and analog source, final database/netlists, build/signoff environment, ledgers, and release digest |

## Artifact roles

- **Runnable source:** code that installs and executes here with deterministic
  examples and unit tests.
- **Reviewed public record:** an engineering guide, schema, or visual prepared
  for this repository.
- **Publisher record:** the canonical publication linked by DOI and IEEE Xplore.
- **Execution snapshot:** binaries, notebooks, configuration, and observations
  that identify a historical hardware run.
- **Controlled implementation record:** foundry, raw-lab, identifying, licensed,
  or collaborator-owned material retained under its project controls.

These roles describe custody and use. The evidence labels below describe what a
technical statement means.

## Evidence labels

| Label | Interpretation |
|---|---|
| **Silicon measurement** | Observed through the fabricated chip, package, board, FPGA, and acquisition path |
| **Circuit simulation / Monte Carlo** | Produced by transistor-level or statistical circuit simulation |
| **Behavioral model** | Produced by the parasitic-aware numerical abstraction |
| **Projection** | Estimated for an alternative implementation, such as SRAM-backed SEC storage |
| **Synthetic** | Generated by the public toy model to expose a method or invariant |
| **Engineering process record** | Supports a design, signoff, packaging, or bring-up decision rather than a performance number |

## Reproduction paths

### Analysis path

```bash
python3 -m pip install -e .
python3 examples/protocol_demo.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

This path exercises deterministic protocol requests, independent column
calibration, signed-code probabilities, probability-weighted SNDR, and the
synthetic SEC illustration.

### Design interpretation path

Read `design/behavioral-model/` to identify the structured attenuation, then
`design/sec-architecture/` to see how γ and θ compensate it and how OCCS
stabilizes the readout. The fixed-point choices connect that mechanism to the
fabricated macro.

### Hardware transaction path

Use `hardware/pcb/` for package/pin traceability and the safe bring-up ladder.
Use `hardware/pynq/` for overlay identity, startup self-test, transaction
framing, and append-only acquisition. Together they define the route from an
experiment specification to a raw response record.

### Release path

Use `tapeout/process-guide/` to move from interface freeze through model
correlation, block closure, signoff, immutable handoff, and post-silicon
readiness. Every gate ends with evidence tied to the same release-candidate
digest.
