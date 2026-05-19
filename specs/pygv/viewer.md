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
