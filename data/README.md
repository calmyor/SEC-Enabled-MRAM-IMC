# Data packaging

`schema.json` defines the run-record shape shared by compact samples and full
measurement captures. It keeps ideal code, state, repeat, ADC column,
configuration, calibration, SEC state, and provenance in one structured record.

## Full capture release checklist

A measured dataset is prepared by:

1. deduplicated without discarding distinct runs;
2. de-identified and screened for paths, serial identifiers, addresses, or credentials;
3. described by a versioned schema with units and dimensions;
4. linked to board/chip/overlay/software aliases and calibration provenance;
5. assigned a redistribution license;
6. checksummed in a manifest;
7. exercised by an end-to-end public analysis; and
8. depositing the complete capture in a versioned archival service and keeping a compact end-to-end sample in Git.

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
