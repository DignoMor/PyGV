from warnings import warn

import numpy as np
import pandas as pd

from pygv.utils import check_accessibility

from .track import NumericalTrack


class GWASTrack(NumericalTrack):
    """
    SNP-based GWAS marker track from BED6+.

    Examples
    --------

    .. plot:: ../examples/plot_gwas.py
    """

    _BED_COLUMNS = ("contig", "start", "end", "name", "score", "strand")

    def __init__(
        self,
        track: str,
        y_transform=None,
        marker_size=8.0,
        color="grey",
        significance_lines=None,
        significance_line_kws=None,
        **kwargs,
    ):
        if callable(color):
            kwargs.setdefault("color", "grey")
        else:
            kwargs.setdefault("color", color)
        super(GWASTrack, self).__init__(**kwargs)
        check_accessibility(track, allow_remote=False)

        self.track = track
        self._marker_size = marker_size
        self._record_color = color
        self._warned_zero_rows = False
        self.significance_lines = list(significance_lines or [])
        self.significance_line_kws = (
            significance_line_kws if isinstance(significance_line_kws, dict) else {}
        )
        if y_transform is None:
            self._y_transform = lambda pvals: -np.log10(pvals)
        elif callable(y_transform):
            self._y_transform = y_transform
        else:
            raise ValueError("y_transform must be None or a callable object.")

        self._use_pysam = False
        self._bed_obj = None
        self._setup_reader()

    def _setup_reader(self):
        use_pysam = False
        if self.track.endswith(".gz"):
            try:
                import pysam

                if check_accessibility(self.track + ".tbi", raise_except=False):
                    self._bed_obj = pysam.TabixFile(self.track)
                    use_pysam = True
            except ImportError:
                use_pysam = False

        if not use_pysam:
            self._bed_obj = pd.read_csv(
                self.track,
                sep="\t",
                header=None,
                comment="#",
                usecols=[0, 1, 2, 3, 4, 5],
                names=self._BED_COLUMNS,
            )
            self._bed_obj["start"] = pd.to_numeric(
                self._bed_obj["start"], errors="coerce"
            )
            self._bed_obj["end"] = pd.to_numeric(self._bed_obj["end"], errors="coerce")
            self._bed_obj["score"] = pd.to_numeric(
                self._bed_obj["score"], errors="coerce"
            )
        self._use_pysam = use_pysam

    def _validate_and_collect(self, row, records, xvals, pvals):
        start = row["start"]
        end = row["end"]
        pval = row["score"]

        if pd.isna(start) or pd.isna(end) or pd.isna(pval):
            raise ValueError("GWASTrack requires numeric BED start/end/score fields.")

        start = int(start)
        end = int(end)
        pval = float(pval)

        if end - start != 1:
            raise ValueError(
                "GWASTrack requires SNP BED rows where end - start == 1."
            )

        if pval == 0:
            if not self._warned_zero_rows:
                warn("Skipping GWAS variants with p-value == 0.", RuntimeWarning)
                self._warned_zero_rows = True
            return
        if pval < 0 or pval > 1:
            raise ValueError("GWASTrack requires p-values in (0, 1].")

        records.append(
            {
                "contig": row["contig"],
                "start": start,
                "end": end,
                "name": row["name"],
                "score": pval,
                "strand": row["strand"],
            }
        )
        xvals.append(start)
        pvals.append(pval)

    def _apply_y_transform(self, pvals):
        arr = np.asarray(pvals, dtype=float)
        if arr.size == 0:
            return arr
        try:
            transformed = np.asarray(self._y_transform(arr), dtype=float)
            if transformed.shape != arr.shape:
                raise ValueError
        except Exception:
            transformed = np.asarray(
                [float(self._y_transform(float(pv))) for pv in arr], dtype=float
            )

        if transformed.shape != arr.shape or not np.all(np.isfinite(transformed)):
            raise ValueError("GWASTrack y_transform must return finite numeric values.")
        return transformed

    def _get(self, chromosome, start, end):
        records = []
        xvals = []
        pvals = []

        if self._use_pysam:
            try:
                for row in self._bed_obj.fetch(chromosome, start, end):
                    fields = row.split("\t")
                    if len(fields) < 6:
                        raise ValueError("GWASTrack requires BED6+ input.")
                    parsed = {
                        "contig": fields[0],
                        "start": fields[1],
                        "end": fields[2],
                        "name": fields[3],
                        "score": fields[4],
                        "strand": fields[5],
                    }
                    pos = int(parsed["start"])
                    if start <= pos < end:
                        self._validate_and_collect(parsed, records, xvals, pvals)
            except ValueError:
                return np.asarray([], dtype=int), np.asarray([], dtype=float), []
        else:
            sub = self._bed_obj.loc[
                np.logical_and(
                    self._bed_obj["contig"] == chromosome,
                    np.logical_and(
                        self._bed_obj["start"] >= start, self._bed_obj["start"] < end
                    ),
                ),
                :,
            ]
            for row in sub.itertuples(index=False):
                parsed = dict(zip(self._BED_COLUMNS, row))
                self._validate_and_collect(parsed, records, xvals, pvals)

        yvals = self._apply_y_transform(pvals)
        return np.asarray(xvals, dtype=int), yvals, records

    def _resolve_style_value(self, style_value, records):
        if callable(style_value):
            return [style_value(record) for record in records]
        return style_value

    def _draw_significance_lines(self):
        if len(self.significance_lines) == 0:
            return

        raw_pvals = []
        for pval in self.significance_lines:
            pval = float(pval)
            if pval <= 0 or pval > 1:
                raise ValueError("significance_lines must contain p-values in (0, 1].")
            raw_pvals.append(pval)

        transformed = self._apply_y_transform(raw_pvals)
        line_kws = {
            "color": self.edge_color,
            "linewidth": self.line_width,
            "linestyle": "--",
            "alpha": self.alpha,
        }
        line_kws.update(self.significance_line_kws)
        for yval in transformed:
            self._ax.axhline(float(yval), **line_kws)

    def _draw_track(self, chromosome, start, end, ax, index=1, **kwargs):
        super(GWASTrack, self)._draw_track(
            chromosome=chromosome, start=start, end=end, ax=ax, index=index, **kwargs
        )
        xvals, yvals, records = self._get(chromosome, start, end)
        if xvals.size == 0:
            self._draw_significance_lines()
            return

        colors = self._resolve_style_value(self._record_color, records)
        sizes = self._resolve_style_value(self._marker_size, records)
        self._ax.scatter(
            xvals,
            yvals,
            c=colors,
            s=sizes,
            alpha=self.alpha,
            linewidths=0,
            rasterized=True,
        )
        self._draw_significance_lines()
