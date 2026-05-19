# PyGV Module Drafts: `pygv.tracks`

- Status: approved
- Last updated: 2026-05-19

## Scope

This directory mirrors user-facing modules under `pygv/tracks/` and captures draft behavioral contracts for each track family.

## Modules

- `track.md`: base contracts for `Track`, `AnnotationTrack`, `NumericalTrack`, and `DynamicValueTrack`.
- `bigwig_track.md`: signal tracks backed by BigWig sources.
- `bam_track.md`: read-level and coverage tracks backed by BAM.
- `bed_track.md`: interval/annotation tracks backed by BED variants.
- `bigbed_track.md`: BigBed-based annotation and mutation tracks.
- `gtf_track.md`: transcript/gene annotation track from GTF.
- `logo_track.md`: sequence logo and dynseq-style tracks.
