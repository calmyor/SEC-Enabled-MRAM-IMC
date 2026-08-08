# Data release policy

No measured raw dataset is committed in the initial public release.

The working collection contains many NPZ/NPY files, duplicates, fixed-filename analyses, machine-specific metadata, and individual files tens of megabytes in size. Before any measured dataset is published, it must be:

1. deduplicated without discarding distinct runs;
2. de-identified and screened for paths, serial identifiers, addresses, or credentials;
3. described by a versioned schema with units and dimensions;
4. linked to board/chip/overlay/software aliases and calibration provenance;
5. assigned a redistribution license;
6. checksummed in a manifest;
7. exercised by an end-to-end public analysis; and
8. deposited in a versioned archival service, with only a small sample kept in Git.

`schema.json` is the proposed public record shape. It is a release template, not a claim that historical captures already satisfy it.

## Minimum sample release

A useful Git-hosted sample should contain:

- at least two ADC columns;
- all reachable codes for one small or representative protocol slice;
- multiple distinct states per code and repeated captures per state;
- a separate calibration population;
- SEC-off and SEC-on records under matched configuration;
- expected summary values and tolerances; and
- the exact command that regenerates calibration and SNDR.

Full data should use stable opaque chip/board/instrument aliases. Keep the identifying alias map under controlled access.
