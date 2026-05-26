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

## Internal Methods (Contracted)

The following internal hooks are contracted for lifecycle/extension behavior:

- `_GenericNumericalBamTrack._get(self, chromosome, start, end)`
  - Data retrieval contract for BAM-derived numerical tracks (`CoverageTrack`, `StrandSpecificCoverageTrack`).
  - Must return interval-aligned numerical data consumed by draw hooks.
- `_GenericBamTrack._get(self, chromosome, start, end)`
  - Data retrieval contract for read-level BAM tracks (`CollapsedReadTrack`, `SplicedReadTrack`, `ReadArcTrack`).
- `SplicedReadTrack._pre_plot_hook(self, chromosome, start, end, **kwargs)`
  - Pre-computes lane packing/registries used by rendering.
- `CollapsedReadTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
- `SplicedReadTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
- `ReadArcTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Render contracts called by `GenomeViewer` after pre-plot preparation.
  - Implementations must honor requested intervals and viewer-managed axis lifecycle.

Non-contracted private helpers (for example, low-level color assignment and local parsing utilities) are implementation details and intentionally excluded.

## Error Expectations

- Missing index files should raise explicit data-integrity errors.
- Invalid coloring modes/unsupported options should fail loudly where validation exists.
- Empty windows should render as empty track outputs rather than hard failure.

## API Reference

- Classes: `CoverageTrack`, `CollapsedReadTrack`, `SplicedReadTrack`, `StrandSpecificCoverageTrack`, `ReadArcTrack`

### Class: `CoverageTrack`

- Constructor (inherited from `_GenericNumericalBamTrack`):
  - `__init__(self, track, filters=None, **kwargs)`

### Class: `CollapsedReadTrack`

- Constructor:
  - `CollapsedReadTrack.__init__(self, track, **kwargs)`

### Class: `SplicedReadTrack`

- Constructor:
  - `SplicedReadTrack.__init__(self, track, **kwargs)`

### Class: `StrandSpecificCoverageTrack`

- Constructor (inherited from `_GenericNumericalBamTrack`):
  - `__init__(self, track, filters=None, **kwargs)`

### Class: `ReadArcTrack`

- Constructor (inherited from `_GenericBamTrack`):
  - `__init__(self, track, filters=None, **kwargs)`
