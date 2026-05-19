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

## Error Expectations

- Inconsistent region span vs. logo matrix length should raise `ValueError`.
- Inaccessible signal or fasta resources should fail early.
- Invalid matrix shapes should fail with actionable messages.
