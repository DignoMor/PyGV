# PyGV Module Draft: `pygv.tracks.bigbed_track`

- Status: approved
- Last updated: 2026-05-19

## Purpose

Defines BigBed-based annotation tracks, including a mutation lollipop-style specialization.

## Public Classes

- `UCSCMutationTrack`
- `BigBed6Track`

## Behavioral Contract

- Accepts local or remote BigBed sources.
- Validates that provided files are BigBed-formatted before rendering.
- `BigBed6Track` maps returned records into BED6-compatible fields for annotation display.
- `UCSCMutationTrack` renders mutation markers/lollipops with optional highlighting and color gradients.

## Filtering and Labels

- Mutation track supports filter fields for targeted mutation emphasis.
- BigBed6 track supports attribute-based filtering over known BED6 fields.
- Over-fielded records should be truncated with warnings rather than hard failure.

## Internal Methods (Contracted)

- `UCSCMutationTrack._get(self, chromosome, start, end)`
  - Fetches BigBed entries for the interval and returns raw mutation rows for renderer consumption.
- `UCSCMutationTrack._draw_track(self, chromosome, start, end, ax, index=1, **kwargs)`
  - Renders lollipop markers/segments from interval entries and applies configured highlight/filter behavior.
- `BigBed6Track._get(self, chromosome, start, end)`
  - Fetches BigBed records and normalizes/truncates rows to BED6-compatible fields.
  - Must return sorted interval records for deterministic downstream rendering via inherited `BedTrack` hooks.

Non-contracted private helpers and commented/experimental draw paths are implementation details and intentionally excluded.

## Error Expectations

- Non-BigBed files should raise value errors.
- Empty intervals should render as no features/mutations.
- Optional labeling dependencies should degrade gracefully if unavailable.

## API Reference

- Classes: `UCSCMutationTrack`, `BigBed6Track`

### Class: `BigBed6Track`

- Constructor:
  - `BigBed6Track.__init__(self, track, **kwargs)`
- Public methods:
  - `get_filters(self)`
  - `set_filters(self, key, value)`

### Class: `UCSCMutationTrack`

- Constructor:
  - `UCSCMutationTrack.__init__(self, track, **kwargs)`
- Public methods:
  - `get_filters(self)`
  - `set_filters(self, key, value)`
