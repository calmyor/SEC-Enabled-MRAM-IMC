# PYNQ-Z2 control and overlay provenance

## Audited implementation record

Available metadata identifies:

- PYNQ-Z2 / XC7Z020 target;
- Vivado 2022.2;
- a 100 MHz design;
- AXI DMA; and
- custom all-pin test logic.

Historical notebooks cover all-pin/scan-chain checks, read/write access, MVM and ADC capture, SEC runs, and last-layer network evaluation. A separate pin-configuration record exists in the private working archive.

## Rebuildability boundary

The archive does not contain the complete custom HDL, XDC constraints, Vivado project, or build Tcl needed to regenerate the overlay. Exact PYNQ image and Python package versions are also incomplete. Therefore:

- a bit/HWH pair may only be released after ownership/security review;
- every released binary would need SHA-256, board target, tool version, clock, register signature, and compatible software version;
- historical notebooks are evidence of execution, not a supported public API; and
- this repository does not claim a reproducible open FPGA build.

## Recommended control architecture

```text
experiment specification
    ↓
protocol planner (scan/read/write/MVM/SEC)
    ↓
typed command and response framing
    ↓
PYNQ overlay + DMA/GPIO transport
    ↓
board pin/voltage boundary
    ↓
chip state machine and observable output
    ↓
append-only raw acquisition record
```

### Configuration

Move machine-specific paths and resources out of scripts. Validate a configuration with:

- overlay and HWH paths plus SHA-256;
- expected board/part and clock;
- register-map/pin-map revision;
- DMA word width, endianness, and buffer limit;
- board/chip aliases;
- instrument aliases and timeouts; and
- rail/current safety bounds.

### Transport

Each transaction should define opcode, payload length, sequence number, timeout, returned status, and recovery behavior. Reject stale/partial DMA results instead of silently reusing a buffer.

### Startup self-test

1. Confirm the PYNQ board and software image.
2. Verify bit/HWH digests and expected IP/register signature.
3. Check configured clocks.
4. Allocate and loop back a bounded DMA transfer.
5. Keep chip-facing outputs safe until rail/pin checks pass.
6. Run the all-pin or scan-loopback smoke vector.
7. Record the self-test result with the acquisition manifest.

## Notebook-to-framework migration

The historical notebooks and scripts include hard-coded serial/VISA endpoints, fixed filenames, implicit units, and analysis constants. A supported framework should separate:

- device/instrument drivers;
- pure protocol plans;
- configuration schemas;
- append-only acquisition;
- calibration/analysis;
- hardware smoke tests; and
- synthetic unit tests.

The public package in `src/sec_mram_imc/` implements only safe, hardware-independent analysis principles. It intentionally has no register map or chip transport.
