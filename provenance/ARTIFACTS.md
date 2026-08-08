# Artifact availability and provenance matrix

This matrix records what the audited working collection supports and what the public repository actually releases.

| Area | Evidence found | Public status | Reproduction statement |
|---|---|---|---|
| ESSCIRC manuscript | LaTeX source and figures | DOI/citation linked | Publisher paper is canonical |
| JSSC manuscript | LaTeX source and figure PDFs | Selected figures + DOI/citation | Publisher paper is canonical |
| Behavioral model | Python model/testbench/circuit-comparison scripts | Method documented; original code held | Requires license/parameter cleanup before source release |
| SEC method | Equations, simulations, fixed-point architecture | Design guide + synthetic illustration | Toy learner is not hardware implementation |
| Measurement analysis | Calibration/SNR scripts and raw arrays | Independently written tested methods | Paper weighting is supported; no measured dataset yet |
| Final TO3 board | Final schematic record, QFN64 bond docs, BOMs, photos | Sanitized visual + engineering guide | Final editable source/fab bundle not found |
| Older board source | TO2/QFN80 KiCad and old fabrication references | Excluded | Must not be labeled final TO3 |
| PYNQ overlay | Bit/HWH pairs and notebooks | Described, binaries held | Complete RTL/XDC/build flow not found |
| Pin map | Historical configuration record | Held pending sanitized review | Not a stable public interface |
| Raw measurements | NPZ/NPY captures and analysis outputs | Excluded pending curation | Needs schema, manifest, deduplication, license, archive |
| ASIC implementation | Foundry config/validator/reports/paperwork | Restricted | No open RTL-to-GDS/signoff flow found |
| Tapeout method | Working process record | Newly written sanitized guide | General method, not a qualified foundry recipe |
| Packaging | QFN64 bonding documents and chip photos | Sanitized photo; detailed files held | Public pin/bond map requires review |

## Labels used

- **Public source:** reviewed, licensed material committed to this repository.
- **Sanitized derivative:** newly authored/redrawn/reviewed content that removes restricted detail.
- **Hardware-dependent:** authentic execution artifact that needs specific unavailable hardware or incomplete build provenance.
- **Restricted / unavailable:** confidential, identifying, incomplete, or unlicensed material not released.

## Explicit non-claims

This repository does not provide:

- a reproducible ASIC implementation or signoff flow;
- the foundry PDK, rule deck, validator, waiver package, or final database;
- a rebuildable PYNQ overlay;
- a turnkey test-board fabrication package;
- a public raw measured-silicon dataset; or
- a full-network on-chip ResNet-20 implementation.

Changes to those statements require a reviewed artifact, ownership permission, versioned provenance, and an end-to-end validation record.
