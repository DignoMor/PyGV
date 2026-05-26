---
status: approved
last_updated: 2026-05-19
---

# Architecture Spec: PyGV

## System Context

PyGV is a Python package built on Matplotlib and genomics IO libraries (`pysam`, `pybigwig`, `pyfaidx`) to render genomic tracks over genomic coordinates.

## High-Level Components

- `pygv/`: the main package directory.
    - `GenomeViewer`: orchestrates track registration, layout, and rendering.
    - Track classes (`pygv/tracks/*`): format-specific logic for loading and plotting data.
    - Shared utilities (`pygv/utils.py`, track base classes): coordinate transforms and common helpers.
- `doc_source/`: the source directory for the documentation.
- `examples/`: the directory for the example notebooks that are used to generate the documentation.

## Key Architectural Constraints

- Viewer should be agnostic to specific track file formats.
- Track-specific IO and rendering should stay encapsulated in each track implementation.
- Rendering relies on Matplotlib primitives and figure lifecycle.

## Data and Control Flow

1. User creates `GenomeViewer` and one or more track instances.
2. User configures tracks (filters, styling, labels, and behavior options).
3. `GenomeViewer.plot()` defines genomic interval and plotting canvas.
4. Each track fetches data for interval and renders to allocated axes area.
5. Figure is displayed or saved via Matplotlib.

### Internal Lifecycle Contract (Viewer <-> Track)

For extension work, the internal lifecycle contract is:

1. `GenomeViewer._validate_tracks(self)`
2. `GenomeViewer._prepare_tracks(self, chromosome, start, end)` -> each track's `_pre_plot_hook(...)`
3. `GenomeViewer._draw_tracks(self, axs, chromosome, start, end, **kwargs)` -> each track's `_draw_track(...)` then `_post_plot_hook(...)`
4. `GenomeViewer._adjust_layout(self, fig, axs, force_tight_layout)` (includes `_apply_group_autoscale()` when configured)

Track subclasses should treat `_pre_plot_hook`, `_draw_track`, and `_post_plot_hook` as the contracted integration points with the viewer. For numerical tracks, `_get(self, chromosome, start, end)` is the contracted data-fetch hook used by concrete renderers.
Private helpers outside these named hooks are intentionally treated as implementation details and are not architectural contracts.

## API Reference

- `pygv.viewer.GenomeViewer`: orchestration entrypoint for plotting workflows.
- `pygv.tracks.*`: format-specific track APIs and plotting contracts.
- `pygv.utils.check_accessibility(file_path: str, allow_remote: bool = False, raise_except: bool = True)`: shared path/URL accessibility validator.

### Architectural API Map

- Orchestration layer: `pygv.viewer`
  - Entry class: `GenomeViewer`
  - Core lifecycle methods:
    - `__init__(font_name=None, font_size=None, alternative_color_map=None, hspace=0.2, inward_ticks=None, n_ticks=None)`
    - `add_track(self, track: pygv.tracks.track.Track) -> None`
    - `add_tracks(self, tracks)`
    - `plot(self, chromosome, start, end, fig_width=8, height_scale_factor=1, force_tight_layout=None, fig_height=None, **kwargs)`
    - `save(self, *args, **kwargs)`
  - Control helpers:
    - `add_group_autoscale(self, track_idx: Union[tuple[int, ...], list[int]])`
    - `add_group_autoscale_by_name(self, track_name: Union[tuple[str, ...], list[str]])`
    - `reset_group_autoscale(self)`
    - `set_highlight_regions(self, starts: Union[list, tuple], ends: Union[list, tuple], colors=(), alpha_vals=())`
    - `set_global_highlight_region(self, start: int, end: int, color="yellow", alpha=0.3)`
- Track abstraction layer: `pygv.tracks.track`
  - Base classes: `Track`, `AnnotationTrack`, `NumericalTrack`, `DynamicValueTrack`
  - Core public methods:
    - `Track.set_highlight_regions(self, starts, ends, colors=(), alpha_vals=())`
    - `Track.add_highlight_region(self, start, end)`
    - `Track.remove_highlight(self)`
    - `NumericalTrack.reset_min_val(self)`
    - `NumericalTrack.reset_max_val(self)`
- Format implementations: `pygv.tracks.*`
  - Numerical signal: `bigwig_track`
  - Alignments/coverage: `bam_track`
  - Interval/feature annotations: `bed_track`, `bigbed_track`, `gtf_track`
  - Sequence logos: `logo_track`
- Shared validation: `pygv.utils`
  - `check_accessibility(file_path: str, allow_remote: bool = False, raise_except: bool = True)`

### API Control-Flow Entry Points

1. Instantiate `GenomeViewer.__init__(font_name=None, font_size=None, alternative_color_map=None, hspace=0.2, inward_ticks=None, n_ticks=None)` and one or more track classes.
2. Register tracks via `add_track(self, track: pygv.tracks.track.Track) -> None` or `add_tracks(self, tracks)`.
3. Execute `plot(self, chromosome, start, end, fig_width=8, height_scale_factor=1, force_tight_layout=None, fig_height=None, **kwargs)`.
4. Persist output with `save(self, *args, **kwargs)` after render.

### Validation and Error Surfaces

- Viewer-level invalid state (for example, no tracks at plot time) raises runtime errors.
- Track-level validation handles format-specific failures (missing indexes, unsupported modes, bad inputs).
- Path/URL accessibility checks are centralized via `check_accessibility(...)`.

