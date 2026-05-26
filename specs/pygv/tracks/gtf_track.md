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

## Internal Methods (Contracted)

- `GtfTrack._get(self, chromosome, start, end)`
  - Internal data-fetch entrypoint selected at initialization (`_pysam_parser` today; pandas parser path is intentionally unimplemented).
- `GtfTrack._pre_plot_hook(self, chromosome, start, end, **kwargs)`
  - Builds transcript/gene lane registries and derives effective track height before drawing.
- `GtfTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders transcript backbones/exons/labels from prepared lane registries.

Parser-private details and record-shaping internals not listed above are implementation details and intentionally excluded.

## Error Expectations

- Missing/inaccessible GTF sources should fail during initialization.
- Unsupported parse paths (for example, unimplemented parser backend) should fail explicitly.
- Empty interval hits should produce empty render output without crashing.

## API Reference

- Class: `GtfTrack`

### Class: `GtfTrack`

- Constructor:
  - `GtfTrack.__init__(self, track, filters=None, show_genes=False, annotation_formatter=None, **kwargs)`
- Public properties with validation:
  - `filters`
  - `show_transcript_id`
