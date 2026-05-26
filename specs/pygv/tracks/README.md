# PyGV Module Drafts: `pygv.tracks`

- Status: approved
- Last updated: 2026-05-19

## Scope

This directory mirrors user-facing modules under `pygv/tracks/` and captures draft behavioral contracts for each track family.

Each module spec may also include an `Internal Methods (Contracted)` section for lifecycle hooks and extension points that developers should anchor on. Private helpers not called out there are intentionally treated as implementation details.

## Modules

- `track.md`: base contracts for `Track`, `AnnotationTrack`, `NumericalTrack`, and `DynamicValueTrack`.
- `bigwig_track.md`: signal tracks backed by BigWig sources.
- `bam_track.md`: read-level and coverage tracks backed by BAM.
- `bed_track.md`: interval/annotation tracks backed by BED variants.
- `bigbed_track.md`: BigBed-based annotation and mutation tracks.
- `gtf_track.md`: transcript/gene annotation track from GTF.
- `logo_track.md`: sequence logo and dynseq-style tracks.

## API Reference

- Exported classes (`pygv.tracks.__all__`):
  - Base: `Track`, `AnnotationTrack`, `NumericalTrack`, `DynamicValueTrack`
  - BAM: `CoverageTrack`, `CollapsedReadTrack`, `SplicedReadTrack`, `StrandSpecificCoverageTrack`, `ReadArcTrack`
  - BED: `BedTrack`, `BedPETrack`, `ConnectionArcTrack`
  - BigBed: `UCSCMutationTrack`, `BigBed6Track`
  - BigWig: `BigWigTrack`, `OverlayingTrack`, `PairedStrandSpecificTrack`, `PairedStrandSpecificTracks`, `PairedStrandlessTrack`
  - GTF/logo: `GtfTrack`, `LogoTrack`, `DynseqTrack`

### Constructor Signatures by Module

- `pygv.tracks.track`
  - `Track.__init__(self, **kwargs: Any)`
  - `AnnotationTrack.__init__(self, track, **kwargs)`
  - `NumericalTrack.__init__(self, **kwargs)`
  - `DynamicValueTrack.__init__(self, track: str = "", **kwargs)`
- `pygv.tracks.bigwig_track`
  - `BigWigTrack.__init__(self, track: str, plot_type: str = "line", **kwargs)`
  - `OverlayingTrack.__init__(self, tracks, labels, palette="Set1", colors=None, legend=True, legend_kws=None, **kwargs)`
  - `PairedStrandSpecificTrack.__init__(self, pl_track, mn_track, draw_y_independently=True, plot_type: str = "line", **kwargs)`
  - `PairedStrandlessTrack.__init__(self, pl_track, mn_track, plot_type: str = "line", **kwargs)`
- `pygv.tracks.bam_track`
  - `CoverageTrack.__init__(self, track, filters=None, **kwargs)` (inherited)
  - `CollapsedReadTrack.__init__(self, track, **kwargs)`
  - `SplicedReadTrack.__init__(self, track, **kwargs)`
  - `StrandSpecificCoverageTrack.__init__(self, track, filters=None, **kwargs)` (inherited)
  - `ReadArcTrack.__init__(self, track, filters=None, **kwargs)` (inherited)
- `pygv.tracks.bed_track`
  - `BedTrack.__init__(self, track, **kwargs: Any)`
  - `BedPETrack.__init__(self, track, **kwargs: Any)`
  - `ConnectionArcTrack.__init__(self, track, **kwargs)`
- `pygv.tracks.bigbed_track`
  - `UCSCMutationTrack.__init__(self, track, **kwargs)`
  - `BigBed6Track.__init__(self, track, **kwargs)`
- `pygv.tracks.gtf_track` / `pygv.tracks.logo_track`
  - `GtfTrack.__init__(self, track, filters=None, show_genes=False, annotation_formatter=None, **kwargs)`
  - `LogoTrack.__init__(self, track: str = "", **kwargs)`
  - `DynseqTrack.__init__(self, track: str = "", seq_fasta: str = "", is_nucleotide: bool = True, **kwargs)`
