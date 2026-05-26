# PyGV Module Draft: `pygv.tracks.gwas_track`

- Status: draft
- Last updated: 2026-05-26

## Purpose

Defines SNP-oriented GWAS marker tracks that render p-value-derived signal over genomic position.

## Public Classes

- `GWASTrack`

## Behavioral Contract

- Input is BED6+ (`bed6plus`); column 5 (`score`) is interpreted as raw p-value.
- X-coordinate uses BED `start`; records are SNP-oriented (`end - start == 1` expected).
- Columns 7+ are ignored by this track contract.
- Y-values are computed from p-values through user-configurable `y_transform`.
- Processing and rendering are interval-scoped: only records within the requested plot interval are fetched/used.
- Significance lines are provided as raw p-values and transformed internally through `y_transform` before plotting.
- Marker color and marker size accept either scalar values or callables for per-record styling.

## Data and Styling Contract

- Default visual styling follows existing PyGV track conventions when optional style inputs are omitted.
- `marker_size` supports scalar numeric input or callable mapping record context to size.
- `color` supports scalar color input or callable mapping record context to color.
- `y_transform` defaults to a deterministic track-provided transform when unset.

## Internal Methods (Contracted)

- `GWASTrack._get(self, chromosome, start, end)`
  - Fetches/filters interval-local BED records and returns x/y-ready marker data.
  - Applies SNP semantic checks and ignores non-required trailing columns.
- `GWASTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders interval-local markers using transformed y-values and resolved style inputs.
  - Draws significance reference lines from transformed threshold values.

Non-contracted helper utilities, parser micro-optimizations, and local rendering internals are implementation details and intentionally excluded.

## Error Expectations

- Non-SNP BED rows (where `end - start != 1`) should fail SNP-semantic validation.
- Non-positive or invalid p-values should fail validation, except p-value `== 0` rows:
  - p-value `== 0` rows are skipped with a warning and do not abort rendering.
- Empty interval matches must render as empty output without crashing.

## Performance Expectations

- Interval-only data access is required; do not process records outside requested `[start, end)`.
- Down-sampling is not part of this track contract; all in-interval SNP markers are rendered.

## API Reference

- Classes: `GWASTrack`

### Class: `GWASTrack`

- Constructor:
  - `GWASTrack.__init__(self, track: str, y_transform=None, marker_size=8.0, color="grey", significance_lines=None, significance_line_kws=None, **kwargs)`
- Constructor argument contract:
  - `marker_size`: scalar numeric value or callable.
  - `color`: scalar color value or callable.
  - `significance_lines`: iterable of raw p-values.
