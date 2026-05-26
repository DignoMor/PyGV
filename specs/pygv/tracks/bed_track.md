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

## Internal Methods (Contracted)

The following internal methods are stable hook contracts for track lifecycle behavior:

- `BedTrack._pre_plot_hook(self, chromosome, start, end, **kwargs)`
  - Builds lane registries for overlap/collapse behavior.
  - Must run before draw to keep lane placement deterministic.
- `BedTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Consumes precomputed lane registries and renders interval blocks/arrows/labels.
- `BedPETrack._pre_plot_hook(self, chromosome, start, end, **kwargs)`
  - Prepares pair-anchor structures used by arc rendering.
- `BedPETrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders interactions and optional arc orientation handling.
- `ConnectionArcTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Uses interval records to draw directional arc annotations.

Non-contracted private helpers and parser internals are implementation details and intentionally excluded.

## Error Expectations

- Missing local files must fail during setup.
- Invalid `show_mode` values should fail validation.
- Empty interval hits should produce an empty rendering state without crashing.

## API Reference

- Classes: `BedTrack`, `BedPETrack`, `ConnectionArcTrack`

### Class: `BedTrack`

- Constructor:
  - `BedTrack.__init__(self, track, **kwargs: Any)`
- Public properties with validation:
  - `plot_thickness`
  - `show_mode`
  - `block_line_width`

### Class: `BedPETrack`

- Constructor:
  - `BedPETrack.__init__(self, track, **kwargs: Any)`

### Class: `ConnectionArcTrack`

- Constructor:
  - `ConnectionArcTrack.__init__(self, track, **kwargs)`
