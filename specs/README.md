# Specs Directory

This directory is the source of truth for planned and approved product and engineering work in PyGV.

Use these docs to define behavior before implementation and to keep changes reviewable.

## Structure

- `architecture.md`: system boundaries, core components, and design constraints.
- `pygv/`: markdown docs for the pygv package. Match the structure of the 
  `pygv/` code directory.
  - `pygv/viewer.md`: documentation for the `GenomeViewer` class.
  - `pygv/tracks/`: documentation for the track classes.
  - `pygv/utils.md`: documentation for the utility functions.

## API Reference

- Top-level package spec index: `specs/README.md`
- System architecture spec: `specs/architecture.md`
- Module-level package specs: `specs/pygv/*.md`
- Track module specs: `specs/pygv/tracks/*.md`

### Spec Entry Points

- `specs/architecture.md`
  - Defines package-wide orchestration and control flow.
  - Primary API entrypoint: `pygv.viewer.GenomeViewer`.
- `specs/pygv/viewer.md`
  - Class-focused reference for viewer lifecycle methods (`add_*`, `plot`, `save`).
- `specs/pygv/utils.md`
  - Function reference for shared validation helper `check_accessibility(...)`.
- `specs/pygv/tracks/README.md`
  - Index of track-family modules and their public classes.
  - Companion internal-hook contracts are documented only for stable lifecycle/extension points.

### Module-to-API Map

- Viewer orchestration
  - Module: `pygv.viewer`
  - Key class: `GenomeViewer`
  - Key methods:
    - `add_track(self, track: pygv.tracks.track.Track) -> None`
    - `add_tracks(self, tracks)`
    - `remove_track(self, track)`
    - `plot(self, chromosome, start, end, fig_width=8, height_scale_factor=1, force_tight_layout=None, fig_height=None, **kwargs)`
    - `save(self, *args, **kwargs)`
- Shared utilities
  - Module: `pygv.utils`
  - Key function: `check_accessibility(file_path: str, allow_remote: bool = False, raise_except: bool = True)`
- Track contracts
  - Module: `pygv.tracks.track`
  - Key classes: `Track`, `AnnotationTrack`, `NumericalTrack`, `DynamicValueTrack`
  - Public methods:
    - `Track.set_highlight_regions(self, starts, ends, colors=(), alpha_vals=())`
    - `Track.add_highlight_region(self, start, end)`
    - `Track.remove_highlight(self)`
- Format-specific tracks
  - Modules: `pygv.tracks.bed_track`, `pygv.tracks.bigbed_track`, `pygv.tracks.bigwig_track`, `pygv.tracks.bam_track`, `pygv.tracks.gtf_track`, `pygv.tracks.logo_track`
  - Exported classes: `BedTrack`, `BedPETrack`, `ConnectionArcTrack`, `UCSCMutationTrack`, `BigBed6Track`, `BigWigTrack`, `OverlayingTrack`, `PairedStrandSpecificTrack`, `PairedStrandSpecificTracks`, `PairedStrandlessTrack`, `CoverageTrack`, `CollapsedReadTrack`, `SplicedReadTrack`, `StrandSpecificCoverageTrack`, `ReadArcTrack`, `GtfTrack`, `LogoTrack`, `DynseqTrack`

