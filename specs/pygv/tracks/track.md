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

## Error Expectations

- Invalid interval/data transformation configuration should raise package-defined errors where available.
- Unsupported statistics/transforms should fail with explicit messages rather than silent fallback.
