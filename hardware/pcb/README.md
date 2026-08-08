# TO3 test PCB: public engineering guide

## Evidence and boundary

The project archive contains a final one-page TO3 schematic record, QFN64 bonding documents, BOM workbooks, a board rendering, and physical setup/chip photographs. The editable KiCad files found during audit correspond to an older TO2/QFN80 design and reference older fabrication/model paths. They are **not** published or described as the final TO3 source.

A future open board release needs one coherent revision containing schematic, PCB, stackup, fabrication outputs, drill data, BOM, placement, assembly drawing, 3D models with licenses, ERC/DRC summaries, and a board-to-chip/lot manifest.

## Board design principles

### Package and pin traceability

- Fix the QFN64 pin-one convention and die/package orientation in every view.
- Map every package pin to a named net, no-connect, or reserved purpose.
- Trace chip pad → bond wire → package pin → PCB net → connector pin → FPGA pin.
- Keep one versioned source for voltage domain, direction, reset state, and safe state.

### Power integrity and safety

- Record nominal, allowed, and absolute-maximum values for every rail/reference.
- Define ramp order, discharge/shutdown order, and conservative first-power current limits.
- Size and place bulk/high-frequency decoupling by rail and expected load step.
- Preserve low-impedance return paths across planes/connectors.
- Provide measurement points that do not force unsafe probing or excessive loading.
- Ensure the unconfigured FPGA and disconnected instruments leave chip pins safe.

### Digital/analog signal integrity

- Verify FPGA bank voltages and level compatibility before routing.
- Control clock/scan edge quality and return-current continuity.
- Keep sensitive references and current-sense paths away from high-toggle interfaces.
- Review connector crosstalk, stubs, series damping, and simultaneous switching.
- Document pull-up/down ownership so board, FPGA, and chip cannot contend at reset.

## Bring-up record template

Every run should bind:

```text
board_revision:
assembly_variant:
chip_id / lot_id:
package_orientation_verified:
rework_log:
overlay_sha256:
pin_map_revision:
host_software_commit:
instrument_inventory:
rail_setpoints_and_limits:
measured_quiescent_currents:
ambient_and_timestamp:
operator_or_automation_id:
```

Do not publish personal identifiers or instrument serial numbers in a public dataset; use controlled aliases with an internal mapping.

## Bring-up ladder

1. Visual inspection, orientation, polarity, solder/rework review.
2. Unpowered rail-to-ground and rail-to-rail screening.
3. Continuity checks from connector to representative package pins.
4. Power with FPGA I/O safe and conservative current limits.
5. Verify rail values, sequence, and steady-state current.
6. Exercise reset and slow static GPIO.
7. Run scan-chain loopback/all-pin checks.
8. Read/write one controlled row and verify reset persistence behavior.
9. Capture raw ADC low/high and a known MVM vector.
10. Proceed to calibration, SEC, and statistical sweeps only after prior invariants pass.

## Missing public artifacts

- final editable TO3 KiCad source and fabrication bundle;
- sanitized pin/rail map;
- supplier-neutral BOM with order/PII removed;
- explicit power-up/current-limit/safe-shutdown procedure;
- expected voltage/current checkpoints;
- board revision ↔ chip/lot ↔ rework map; and
- symptom-to-cause fault table.

Their absence is recorded so readers do not mistake a photograph and schematic PDF for a complete reproducible PCB release.
