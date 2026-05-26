# PyGV Module Draft: `pygv.utils`

- Status: approved
- Last updated: 2026-05-19

## Purpose

`pygv.utils` contains reusable utility helpers shared across track and viewer modules.

## Public Surface

- `check_accessibility(file_path, allow_remote=False, raise_except=True) -> bool`

## Behavioral Contract

- Returns `True` when a local path exists.
- Returns `True` for `http/https/ftp` URLs only when `allow_remote=True`.
- Returns `False` for inaccessible paths when `raise_except=False`.
- Raises `ValueError` for inaccessible paths when `raise_except=True`.

## Usage in Package

- File-backed tracks use this helper to validate local or remote data sources before opening files.
- The helper is expected to be side-effect free (validation only).

## Constraints

- This utility checks path accessibility only; it does not validate file format or readability of file contents.
- Remote checks are prefix-based and do not include a live network probe.

## API Reference

- Function: `check_accessibility(file_path: str, allow_remote: bool = False, raise_except: bool = True)`

### Function: `check_accessibility(file_path: str, allow_remote: bool = False, raise_except: bool = True)`

- Behavior
  - Returns `True` for existing local paths.
  - Returns `True` for remote prefixes only when remote access is explicitly allowed.
  - Performs accessibility validation only; does not parse or inspect file contents.
- Validation/error notes
  - Inaccessible paths raise `ValueError` when `raise_except=True`.
  - Inaccessible paths return `False` when `raise_except=False`.
