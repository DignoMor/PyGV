# PyGV Module Draft: `pygv.tracks.bigwig_track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines numerical signal tracks that read BigWig files and render line/bar-style signals across genomic intervals.

## Public Classes

- `BigWigTrack`
- `OverlayingTrack`
- `PairedStrandSpecificTrack`
- `PairedStrandSpecificTracks` (alias/compatibility class)
- `PairedStrandlessTrack`

## Behavioral Contract

- Accept local paths and remote URLs (when accessible).
- Extract values across `[start, end)` and align x-coordinates to genomic positions.
- Support configurable plotting modes (`line`, `bar`) for standard BigWig tracks.
- Apply optional value transforms/scaling/statistic binning before rendering.
- Preserve deterministic ordering of overlaid tracks and their labels/colors.

## Visualization Contract

- Filled area/line behavior should match selected plot type.
- Overlay tracks should maintain stable legend labeling when enabled.
- Strand-specific variants should clearly distinguish signal channels by configuration and color.

## Internal Methods (Contracted)

- `BigWigTrack._get(self, chromosome, start, end, nan_as_zero=True)`
  - Interval data-fetch contract for BigWig-backed numerical rendering.
  - Applies configured NaN handling, transforms, scaling, and optional bin-stat aggregation.
- `BigWigTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders using configured `plot_type` (`line`/`bar`) from `_get(...)` output.
- `OverlayingTrack._get(self, chromosome, start, end)`
- `OverlayingTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Contract for multi-source overlay ordering and per-track label/color rendering.
- `PairedStrandSpecificTrack._get(self, chromosome, start, end, nan_as_zero=True)`
- `PairedStrandSpecificTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Contract for paired positive/negative channel extraction and mirrored rendering.
- `PairedStrandlessTrack._get(self, chromosome, start, end, nan_as_zero=True)`
  - Contract for strand-collapsed paired signal aggregation prior to inherited rendering.

Non-contracted local helpers and rendering micro-optimizations are implementation details and intentionally excluded.

## Error and Data Handling

- Inaccessible tracks must fail during initialization.
- Missing values may be normalized (`nan -> 0`) depending on rendering path.
- Region requests that return empty data should render gracefully without crashing.

## API Reference

- Classes: `BigWigTrack`, `OverlayingTrack`, `PairedStrandSpecificTrack`, `PairedStrandSpecificTracks`, `PairedStrandlessTrack`

### Class: `BigWigTrack`

- Constructor:
  - `BigWigTrack.__init__(self, track: str, plot_type: str = "line", **kwargs)`

### Class: `OverlayingTrack`

- Constructor:
  - `OverlayingTrack.__init__(self, tracks, labels, palette="Set1", colors=None, legend=True, legend_kws=None, **kwargs)`

### Class: `PairedStrandSpecificTrack`

- Constructor:
  - `PairedStrandSpecificTrack.__init__(self, pl_track, mn_track, draw_y_independently=True, plot_type: str = "line", **kwargs)`

### Class: `PairedStrandSpecificTracks`

- Alias class:
  - `class PairedStrandSpecificTracks(PairedStrandSpecificTrack)`
  - Inherits `PairedStrandSpecificTrack.__init__(self, pl_track, mn_track, draw_y_independently=True, plot_type: str = "line", **kwargs)`

### Class: `PairedStrandlessTrack`

- Constructor:
  - `PairedStrandlessTrack.__init__(self, pl_track, mn_track, plot_type: str = "line", **kwargs)`
