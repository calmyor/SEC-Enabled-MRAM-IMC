# PYNQ-Z2 control path and overlay identity

## Executed setup record

Available metadata identifies:

- PYNQ-Z2 / XC7Z020 target;
- Vivado 2022.2;
- a 100 MHz design;
- AXI DMA; and
- custom all-pin test logic.

Historical notebooks cover all-pin/scan-chain checks, read/write access, MVM and ADC capture, SEC runs, and final-layer network evaluation. Together, the target metadata, bit/HWH snapshots, notebooks, and pin-configuration record identify the executed control stack.

**Execution snapshot.** The target, Vivado version,
clock, bit/HWH pairs, and notebook sequence capture the historical execution
path. The matching custom HDL, XDC, Vivado build project/Tcl, exact PYNQ image,
and Python package lock form the source-regeneration layer.

## Overlay identity record

Bind every executable overlay to:

- bitstream and HWH SHA-256 digests;
- PYNQ-Z2 / XC7Z020 target and the PYNQ image version;
- Vivado version, configured clocks, and IP/register signature;
- register-map and pin-map revision;
- compatible host-software commit and Python package lock; and
- all-pin, DMA-loopback, and known-command self-test results.

Source regeneration adds the matching custom HDL, XDC constraints, Vivado
project/build Tcl, and one command that produces the identified bit/HWH pair.
This separates two useful records: the exact overlay that executed an
experiment and the recipe that regenerates it.

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

## Notebook-to-framework path

Move the historical notebook sequence into explicit layers so each experiment can be replayed, tested, and audited:

- device/instrument drivers;
- pure protocol plans;
- configuration schemas;
- append-only acquisition;
- calibration/analysis;
- hardware smoke tests; and
- synthetic unit tests.

The package in `src/sec_mram_imc/` implements the hardware-independent analysis
layer: calibration, sampling requests, code probabilities, and SNDR. A transport
adapter can consume the same request plan, append raw responses, and hand the
resulting record to these pure functions.
