"""GWASTrack reader behavior for indexed and pandas BED6+ sources."""

import os
import subprocess
import sys
import warnings
from pathlib import Path

import pysam
import pytest

from pygv.tracks.gwas_track import GWASTrack


def _write_indexed_bed(tmp_path, name, text):
    source = tmp_path / f"{name}.bed"
    source.write_text(text)
    compressed = str(source) + ".gz"
    pysam.tabix_compress(str(source), compressed, force=True)
    pysam.tabix_index(compressed, preset="bed", force=True)
    return compressed


def _track(tmp_path, name, text, reader):
    if reader == "indexed":
        return GWASTrack(_write_indexed_bed(tmp_path, name, text))
    path = tmp_path / f"{name}.bed"
    path.write_text(text)
    return GWASTrack(str(path))


def _assert_empty(result):
    xvals, yvals, records = result
    assert len(xvals) == len(yvals) == len(records) == 0


@pytest.mark.parametrize("reader", ["indexed", "pandas"])
def test_readers_keep_half_open_interval(tmp_path, reader):
    track = _track(
        tmp_path,
        "bounds",
        "chr1\t10\t11\ta\t0.01\t+\nchr1\t20\t21\tb\t0.1\t+\n",
        reader,
    )

    xvals, yvals, records = track._get("chr1", 10, 20)
    assert list(xvals) == [10]
    assert yvals[0] == pytest.approx(2.0)
    assert records[0]["score"] == 0.01

    xvals, yvals, records = track._get("chr1", 20, 21)
    assert list(xvals) == [20]
    assert yvals[0] == pytest.approx(1.0)
    assert records[0]["name"] == "b"

    _assert_empty(track._get("chr1", 11, 20))


@pytest.mark.parametrize("reader", ["indexed", "pandas"])
def test_missing_contig_returns_empty(tmp_path, reader):
    track = _track(
        tmp_path,
        "present",
        "chr1\t10\t11\ta\t0.01\t+\n",
        reader,
    )
    _assert_empty(track._get("chr2", 0, 100))


@pytest.mark.parametrize("reader", ["indexed", "pandas"])
def test_valid_empty_interval_returns_empty(tmp_path, reader):
    track = _track(
        tmp_path,
        "present",
        "chr1\t10\t11\ta\t0.01\t+\n",
        reader,
    )
    _assert_empty(track._get("chr1", 0, 10))


@pytest.mark.parametrize("reader", ["indexed", "pandas"])
@pytest.mark.parametrize(
    ("row", "message"),
    [
        ("chr1\t10\t11\trs1\t1.5\t+\n", "p-values in"),
        ("chr1\t10\t11\trs1\t-0.2\t+\n", "p-values in"),
        ("chr1\t10\t15\trs1\t0.2\t+\n", "end - start"),
        ("chr1\t10\t11\trs1\tNA\t+\n", "numeric"),
    ],
)
def test_in_interval_records_fail_validation(tmp_path, reader, row, message):
    track = _track(tmp_path, "invalid", row, reader)
    with pytest.raises(ValueError, match=message):
        track._get("chr1", 0, 20)


def test_indexed_reader_rejects_short_bed_row(tmp_path):
    track = _track(tmp_path, "short", "chr1\t10\t11\trs1\t0.2\n", "indexed")
    with pytest.raises(ValueError, match="BED6"):
        track._get("chr1", 0, 20)


@pytest.mark.parametrize(
    "row",
    [
        "chr1\txx\t11\trs1\t0.2\t+\n",
        "chr1\t10\tNA\trs1\t0.2\t+\n",
    ],
)
def test_pandas_reader_rejects_nonnumeric_coordinates(tmp_path, row):
    track = _track(tmp_path, "coords", row, "pandas")
    with pytest.raises(ValueError, match="numeric"):
        track._get("chr1", 0, 20)


@pytest.mark.parametrize("reader", ["indexed", "pandas"])
def test_record_outside_interval_is_not_validated(tmp_path, reader):
    track = _track(
        tmp_path,
        "outside",
        "chr1\t8\t30\trs1\t1.5\t+\n",
        reader,
    )
    _assert_empty(track._get("chr1", 10, 20))


@pytest.mark.parametrize("reader", ["indexed", "pandas"])
def test_zero_p_value_is_skipped_with_one_warning(tmp_path, reader):
    track = _track(
        tmp_path,
        "zeros",
        "chr1\t10\t11\ta\t0\t+\nchr1\t12\t13\tb\t0\t+\nchr1\t14\t15\tc\t0.01\t+\n",
        reader,
    )

    with pytest.warns(RuntimeWarning, match="p-value == 0") as caught:
        xvals, yvals, records = track._get("chr1", 0, 100)
    assert len(caught) == 1
    assert list(xvals) == [14]
    assert yvals[0] == pytest.approx(2.0)
    assert [record["name"] for record in records] == ["c"]

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        track._get("chr1", 0, 100)


def test_gwas_gallery_example_runs():
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run(
        [sys.executable, str(root / "examples" / "plot_gwas.py")],
        cwd=root / "doc_source",
        env=env,
        check=True,
    )
