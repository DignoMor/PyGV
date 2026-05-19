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

## Error and Data Handling

- Inaccessible tracks must fail during initialization.
- Missing values may be normalized (`nan -> 0`) depending on rendering path.
- Region requests that return empty data should render gracefully without crashing.
