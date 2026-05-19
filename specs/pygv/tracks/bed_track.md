# PyGV Module Draft: `pygv.tracks.bed_track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines BED-backed annotation tracks for visualizing interval features and pair/connection relationships.

## Public Classes

- `BedTrack`
- `BedPETrack`
- `ConnectionArcTrack`

## Behavioral Contract

- Supports BED-style inputs, with parser strategy depending on available indexing and local tooling.
- Determines feature lane placement to avoid visual overlap in expanded mode.
- Supports collapsed mode for denser summaries when overlap is high.
- Optional properties (feature name display, block rendering, thickness) should only affect presentation, not interval selection.

## Format Contract

- Accepts common BED variants with progressive optional columns.
- Uses available fields to enable richer rendering (for example, blocks, thick segments, item RGB).
- Missing optional BED fields should degrade gracefully to simpler rendering behavior.

## Filtering and Styling

- Feature-level filters should allow users to narrow visible annotations.
- Defaults should provide legible neutral styling when explicit colors are absent.

## Error Expectations

- Missing local files must fail during setup.
- Invalid `show_mode` values should fail validation.
- Empty interval hits should produce an empty rendering state without crashing.
