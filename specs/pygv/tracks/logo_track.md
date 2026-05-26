# PyGV Module Draft: `pygv.tracks.logo_track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines sequence-logo-style tracks for nucleotide/protein motif visualization and dynseq-style rendering.

## Public Classes

- `LogoTrack`
- `DynseqTrack`

## Behavioral Contract

- `LogoTrack` renders a logo matrix supplied by user-assigned values.
- Matrix length must match plotting interval span.
- Supports configurable color schemes, font, stack order, and below-baseline behavior.
- `DynseqTrack` derives logo values from track signals and sequence context (fasta) for per-position glyph rendering.

## Data Contract

- Value inputs can be NumPy arrays or DataFrames, with expected character columns.
- Sequence-backed dynseq rendering requires valid sequence source compatibility with requested interval.

## Internal Methods (Contracted)

- `LogoTrack._get(self, chromosome, start, end)`
  - Validates interval-length alignment against assigned logo values and returns interval coordinates with matrix data.
- `LogoTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders logo glyphs from `_get(...)` output after standard numerical/base track setup.
- `DynseqTrack._get(self, chromosome, start, end)`
  - Cross-module contract that combines BigWig interval values with FASTA sequence to produce per-position logo matrices.
- `DynseqTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders dynseq logos from derived matrices while honoring viewer lifecycle.

Non-contracted private helpers and low-level matrix construction details are implementation details and intentionally excluded.

## Error Expectations

- Inconsistent region span vs. logo matrix length should raise `ValueError`.
- Inaccessible signal or fasta resources should fail early.
- Invalid matrix shapes should fail with actionable messages.

## API Reference

- Classes: `LogoTrack`, `DynseqTrack`

### Class: `LogoTrack`

- Constructor:
  - `LogoTrack.__init__(self, track: str = "", **kwargs)`
- Public property:
  - `values`

### Class: `DynseqTrack`

- Constructor:
  - `DynseqTrack.__init__(self, track: str = "", seq_fasta: str = "", is_nucleotide: bool = True, **kwargs)`
