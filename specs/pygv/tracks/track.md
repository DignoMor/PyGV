# PyGV Module Draft: `pygv.tracks.track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines base track abstractions and shared behavior for all PyGV track implementations.

## Public Classes

- `Track`: generic plotting track with style and axis lifecycle helpers.
- `AnnotationTrack`: base class for feature-style tracks (intervals/annotations).
- `NumericalTrack`: base class for value-over-position tracks.
- `DynamicValueTrack`: numerical track variant that can derive values from callable/data at render time.

## Shared Contract (`Track`)

- Tracks expose core style knobs: name, color, edge color, alpha, line width, font controls, and track height.
- Tracks support highlight region overlays via track-level APIs.
- Track instances attach to a Matplotlib axis during drawing.
- Height must be positive; invalid height should fail.

## Annotation Track Contract

- Feature data is prepared before drawing.
- Lane packing behavior controls collision/overlap rendering.
- Optional feature labels and padding affect readability, not genomic coordinate semantics.

## Numerical Track Contract

- Numerical tracks render genomic coordinate vectors against one or more value arrays.
- Optional transforms/scaling/statistics are applied deterministically before plotting.
- Axis scaling and y-label formatting are controlled by track configuration.

## Integration Contract with `GenomeViewer`

- Track implementations are expected to support:
  - `_pre_plot_hook(chromosome, start, end, ...)`
  - `_draw_track(chromosome, start, end, ax, index, ...)`
  - `_post_plot_hook(chromosome, start, end, ax, index, ...)`
- Hooks must behave idempotently for repeated plotting over different intervals in the same viewer object.

## Internal Methods (Contracted)

These internal methods are part of the viewer/track lifecycle contract and are safe for developers to anchor on when extending tracks:

- `Track._pre_plot_hook(self, chromosome, start, end, **kwargs)`
  - Called by `GenomeViewer` before drawing.
  - Must be side-effect safe for repeated renders and may consume viewer-provided options (for example, `inward_ticks`).
- `Track._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Called by `GenomeViewer` to bind the axis and draw track content.
  - Implementations must honor the requested `[start, end)` window and draw on `ax`.
- `Track._post_plot_hook(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Called after drawing; used for post-render overlays and final axis adjustments.
- `NumericalTrack._get(self, chromosome, start, end)`
  - Required subclass hook for fetching/deriving x/y arrays before rendering.
  - Returned coordinates/values must align to the requested interval.
- `NumericalTrack._post_plot_hook(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Extends base post-hook behavior with numerical y-range, scale, and overflow handling.
  - Numerical subclasses overriding this hook should preserve base behavior.

Non-contracted private helpers and stateful internals (for example, local utility functions and temporary caches) are implementation details and intentionally excluded.

## Error Expectations

- Invalid interval/data transformation configuration should raise package-defined errors where available.
- Unsupported statistics/transforms should fail with explicit messages rather than silent fallback.

## API Reference

- Classes: `Track`, `AnnotationTrack`, `NumericalTrack`, `DynamicValueTrack`

### Class: `Track`

- Constructor:
  - `Track.__init__(self, **kwargs: Any)`
- Public methods:
  - `set_highlight_regions(self, starts, ends, colors=(), alpha_vals=())`
  - `add_highlight_region(self, start, end)`
  - `remove_highlight(self)`

### Class: `AnnotationTrack`

- Constructor:
  - `AnnotationTrack.__init__(self, track, **kwargs)`

### Class: `NumericalTrack`

- Constructor:
  - `NumericalTrack.__init__(self, **kwargs)`
- Public methods:
  - `reset_min_val(self)`
  - `reset_max_val(self)`

### Class: `DynamicValueTrack`

- Constructor:
  - `DynamicValueTrack.__init__(self, track: str = "", **kwargs)`
