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

