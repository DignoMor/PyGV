"""
==========
GWAS Track
==========

Create a :class:`~pygv.tracks.gwas_track.GWASTrack` with callable marker style inputs.
"""

import matplotlib.pyplot as plt
import numpy as np

from pygv.tracks.gwas_track import GWASTrack
from pygv.viewer import GenomeViewer

gv = GenomeViewer()

gwas_track = GWASTrack(
    "../examples/data/AD_Bellenguez_2022.GWAS.chr22.bed6poly",
    name="AD GWAS",
    max_val=28,
    y_transform=lambda pvalue: -1.0 * np.log10(pvalue),
    marker_size=lambda record: 12 if record["score"] < 1e-5 else 6,
    color=lambda record: "crimson" if record["score"] < 5e-8 else "grey",
    significance_lines=(5e-8, 1e-5),
    significance_line_kws={"color": "black", "linestyle": "--", "linewidth": 0.9},
)
gv.add_track(gwas_track)

# Plot 100 kb centered at the TREM2 TSS (chr6:41,163,186).
trem2_tss = 41163186
window_half_size = 50000
gv.plot(
    "chr6",
    trem2_tss - window_half_size,
    trem2_tss + window_half_size,
    fig_height=2.5,
)
plt.tight_layout()
