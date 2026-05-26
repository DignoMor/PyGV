# PyGV Module Draft: `pygv.viewer`

- Status: approved
- Last updated: 2026-05-19

## Purpose

`pygv.viewer` defines `GenomeViewer`, the orchestration layer that composes tracks, manages figure layout, and triggers rendering over a genomic interval.

## Public Surface

- `GenomeViewer.__init__(...)`: configure global plotting defaults (font, spacing, tick behavior, alternate color map).
- `add_track(track)`: register a single track in render order.
- `add_tracks(tracks)`: register multiple tracks in render order.
- `remove_track(track)`: remove an existing registered track.
- `show_tracks()`: return registered track metadata `(name, type, object)`.
- `add_group_autoscale(track_idx)` / `add_group_autoscale_by_name(track_name)`: link numerical tracks to share y-scaling.
- `reset_group_autoscale()`: clear autoscale group settings.
- `set_highlight_regions(starts, ends, ...)`: apply highlight spans to all registered tracks.
- `set_global_highlight_region(start, end, ...)`: draw a figure-level highlight region after plotting.
- `plot(chromosome, start, end, ...)`: run validation, preparation hooks, drawing, and layout.
- `save(path, **kwargs)`: save current figure (adds PDF metadata when output is `.pdf`).

## Behavioral Contract

- Tracks render in registration order.
- `plot(...)` fails fast when no tracks are registered.
- Every track receives pre-draw and post-draw hooks around drawing.
- Figure height is inferred from track heights when `fig_height` is not provided.
- Group autoscaling only applies to numerical tracks.
- Global highlight requires a previously plotted region.

## Inputs and Error Expectations

- Genomic interval is passed as `chromosome`, `start`, `end` and reused across all registered tracks.
- Invalid setup states (for example, plotting with zero tracks) raise runtime errors.
- Unsupported autoscale references emit runtime warnings rather than failing hard.

## Dependencies

- Matplotlib for figure/axes lifecycle.
- NumPy for track height and scaling operations.
- `pygv.tracks` contracts (`_pre_plot_hook`, `_draw_track`, `_post_plot_hook`).

## Internal Methods (Contracted)

`GenomeViewer` has internal orchestration methods that define the cross-module rendering lifecycle:

- `GenomeViewer._validate_tracks(self)`
  - Must fail fast before plotting when no tracks are registered.
- `GenomeViewer._prepare_tracks(self, chromosome, start, end)`
  - Calls each track's `_pre_plot_hook(...)` with viewer context.
  - Passes shared viewer overrides (for example, `inward_ticks`) through hook kwargs.
- `GenomeViewer._draw_tracks(self, axs, chromosome, start, end, **kwargs)`
  - Calls each track's `_draw_track(...)` and then `_post_plot_hook(...)` in registration order.
  - Provides `n_ticks` and plotting kwargs to track hooks.
- `GenomeViewer._adjust_layout(self, fig, axs, force_tight_layout)`
  - Final layout phase after track drawing; applies spacing, y-label alignment, and autoscale groups.
- `GenomeViewer._apply_group_autoscale(self)`
  - Aligns y-limits/ticks across grouped numerical tracks using rendered axis state.

Expected lifecycle order for `plot(...)` is:
`_validate_tracks -> _prepare_tracks -> _create_figure_and_axes -> _draw_tracks -> _adjust_layout`.

Other private helpers are implementation details and intentionally excluded from this contract.

## API Reference

- Class: `GenomeViewer`
- Constructor:
  - `GenomeViewer.__init__(font_name=None, font_size=None, alternative_color_map=None, hspace=0.2, inward_ticks=None, n_ticks=None)`
- Track registration/introspection:
  - `add_track(self, track: pygv.tracks.track.Track) -> None`
  - `add_tracks(self, tracks)`
  - `remove_track(self, track)`
  - `show_tracks(self)`
- Autoscale controls:
  - `add_group_autoscale(self, track_idx: Union[tuple[int, ...], list[int]])`
  - `add_group_autoscale_by_name(self, track_name: Union[tuple[str, ...], list[str]])`
  - `reset_group_autoscale(self)`
- Highlight controls:
  - `set_highlight_regions(self, starts: Union[list, tuple], ends: Union[list, tuple], colors=(), alpha_vals=())`
  - `set_global_highlight_region(self, start: int, end: int, color="yellow", alpha=0.3)`
- Render/output:
  - `plot(self, chromosome, start, end, fig_width=8, height_scale_factor=1, force_tight_layout=None, fig_height=None, **kwargs)`
  - `save(self, *args, **kwargs)`
