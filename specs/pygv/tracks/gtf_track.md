# PyGV Module Draft: `pygv.tracks.gtf_track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines GTF-backed annotation tracks for transcript and gene visualization.

## Public Class

- `GtfTrack`

## Behavioral Contract

- Accepts indexed local or remote-compatible GTF sources.
- Parses transcript/gene/exon features into renderable records for lane placement.
- Supports optional `filters` callable to include/exclude records before plotting.
- Supports gene-aware view behavior (`show_genes`) and transcript labeling options.
- Supports annotation label formatting via user-provided formatter callable.

## Rendering Contract

- Transcripts/genes are drawn as interval features with optional exon block display.
- Exon segments are associated with parent transcript records when available.
- Record ordering should remain stable and reproducible for the same inputs.

## Error Expectations

- Missing/inaccessible GTF sources should fail during initialization.
- Unsupported parse paths (for example, unimplemented parser backend) should fail explicitly.
- Empty interval hits should produce empty render output without crashing.
