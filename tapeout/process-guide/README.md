# Mixed-signal tapeout process guide

This is a sanitized engineering guide, not a foundry recipe. Rule names, PDK/configuration data, validator material, release databases, personal paths, waiver details, and raw reports remain restricted.

## 1. Freeze interfaces and ownership

Before implementation closure, freeze:

- compute modes, dimensions, ADC and weight/input precision;
- SEC training/inference semantics and bypass;
- reset, clock, scan, register, and external timing;
- voltage domains, analog references, safe pin states, and power sequence;
- array/sensor/ADC/digital interface contracts;
- test modes and required observables;
- package/pad assumptions; and
- source/IP authorship, licensing, export, and public-release classification.

**Exit evidence:** signed specification, interface tables, golden vectors, IP/provenance ledger, and owned open issues.

## 2. Correlate models

Use shared vectors to correlate:

1. ideal mathematical dot product;
2. parasitic-aware behavioral model;
3. transistor/circuit simulation;
4. fixed-point SEC model;
5. RTL/gate implementation; and
6. post-layout/extracted behavior where applicable.

Record sign, scaling, bit ordering, rounding, clipping, reset, and update sequence. A numerical match without a shared convention is not correlation.

**Exit evidence:** versioned vector pack, tolerances, discrepancy ledger, and resolution for every out-of-tolerance class.

## 3. Verify mixed-signal blocks

For array, OCCS, ADC, references, and interfaces, separate:

- nominal functional sweeps;
- global PVT/corner sweeps;
- local mismatch Monte Carlo;
- temporal-noise analysis;
- startup and reset;
- extreme-code/headroom behavior;
- timing aperture and conversion decision margin; and
- extracted parasitic re-correlation.

**Exit evidence:** reviewed coverage matrix, model versions, seeds/sample count, worst cases, and owners for residual risk.

## 4. Close digital implementation and DFT

- Lint and CDC/RDC with intentional crossings documented.
- Synthesis constraints and equivalence.
- Clock/reset/test-mode definitions.
- Timing exceptions with path-level justification.
- Scan controllability/observability for each mode.
- Bit-accurate SEC saturation, sign, and shift behavior.
- Gate-level/reset/timing simulation where needed.
- Formal or exhaustive checks for protocol/state invariants where practical.

**Exit evidence:** constrained netlist, exception ledger, coverage and equivalence summaries, and test-mode vectors.

## 5. Co-design floorplan, power, and package

- Place the array, sensors, ADCs, references, and digital logic according to signal sensitivity and routing load.
- Isolate analog quiet regions from high-toggle clocks/buses.
- Plan domain-specific grids, decoupling, reference return, and package current paths.
- Analyze IR drop and electromigration under realistic simultaneous activity.
- Shield or space clocks, references, and high-impedance nodes.
- Reserve padframe/test access before late congestion.
- Feed extracted parasitics back to sensor and SEC assumptions.

**Exit evidence:** floorplan review, power-intent consistency, extraction correlation, package/pad feasibility, and owned remaining margins.

## 6. Physical verification and signoff ledger

Qualified flows commonly cover DRC, LVS, ERC, antenna, density/fill, timing, EM/IR, and final-stream integrity. The exact foundry flow remains private.

For each run retain:

```text
design_digest
database_timestamp
tool_and_rule_version
library_and_corner_version
configuration_digest
summary_counts
reviewer_and_review_time
exception_or_waiver_links
relationship_to_release_candidate
```

Nonzero summary counts require review; a successful tool exit does not prove clean signoff. A waiver needs the exact rule/geometry, intent, risk argument, narrow scope, approver, and revalidation after ECO/fill/regeneration.

**Exit evidence:** reviewed signoff ledger tied to the exact release-candidate digest.

## 7. Verify top level, padframe, and package

- Pad/ESD type and voltage domain.
- Clamp and domain-crossing behavior in all power states.
- Die orientation, pin one, bond-wire feasibility, no-connects.
- Schematic/netlist/bond-map/board naming consistency.
- Package parasitic and simultaneous-switching impact.
- Safe FPGA/board state before and during chip power-up.

**Exit evidence:** released QFN64 bond map, pad audit, package drawing, and pin-to-register traceability table.

## 8. Create an immutable handoff

- Generate the final database once from a documented candidate.
- Compute checksums and a byte/file manifest.
- Record layer map, qualified configuration, approved exceptions, and required forms.
- Transfer only through the approved secure mechanism.
- Verify the received digest and archive acknowledgement.
- Freeze the exact released artifact; later changes become a new candidate.

**Exit evidence:** immutable manifest, checksums, approval record, secure-transfer acknowledgement, and archived copy under access control.

## 9. Prepare post-silicon before parts arrive

- Final board/package revision and pin map.
- Conservative power-up/current-limit/shutdown procedure.
- Overlay/firmware/software digests and compatibility matrix.
- Scan, read/write, ADC, and known-MVM smoke vectors.
- Expected checkpoints and fault tree.
- Raw-data schema, run manifest, and calibration plan.
- Board/chip/lot aliasing and rework log.

**Exit evidence:** executable bring-up rehearsal using a mock/loopback path and a signed readiness checklist.

## Archive boundary from this project

The audited private tapeout folder contains confidential foundry configuration/validator material, export paperwork, detailed run paths/reports, and intermediate summaries. It does not establish an open source-to-GDS flow. No RTL, final GDS/OASIS, netlists, synthesis/P&R scripts, or complete LVS/PEX/signoff package suitable for public reproduction was found.

This guide therefore describes the engineering process without asserting that the internal archive is a clean, complete, or redistributable signoff bundle.
