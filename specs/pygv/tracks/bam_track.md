# PyGV Module Draft: `pygv.tracks.bam_track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines BAM-backed tracks for coverage, aligned-read, spliced-read, and arc-style visualization.

## Public Classes

- `CoverageTrack`
- `CollapsedReadTrack`
- `SplicedReadTrack`
- `StrandSpecificCoverageTrack`
- `ReadArcTrack`

## Behavioral Contract

- BAM path must exist and include a readable index before plotting.
- Tracks operate on requested genomic intervals and fetch only interval-relevant reads.
- Optional `filters` callables determine which reads are retained for rendering.
- Strand/color options and legend options must be deterministic from configuration.

## Rendering Contract

- Coverage-style tracks render aggregated numeric summaries.
- Read-level tracks render individual or packed read glyphs.
- Arc-style tracks render junction/link structures between genomic positions.
- Sampling/feature-lane options should trade detail for clarity/performance without breaking coordinate correctness.

## Error Expectations

- Missing index files should raise explicit data-integrity errors.
- Invalid coloring modes/unsupported options should fail loudly where validation exists.
- Empty windows should render as empty track outputs rather than hard failure.
