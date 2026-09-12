# Third-party notices

PyGV is distributed under GPL-3.0-or-later (see [`LICENSE`](LICENSE)). This file
records the third-party components and data that PyGV bundles, reproduces, or
depends on, together with the notices required by their terms.

Complying with GPL-3.0-or-later does not remove the obligations attached to the
third-party material listed below. When redistributing PyGV, keep this file and
the referenced license texts with the distribution.

## Bundled source code

### Logomaker

The sequence-logo implementation under `pygv/tracks/logomaker/` is derived from
[Logomaker](https://github.com/jbkinney/logomaker) by Ammar Tareen and Justin B.
Kinney and is redistributed under the MIT License. The full text is preserved at
[`pygv/tracks/logomaker/LICENSE`](pygv/tracks/logomaker/LICENSE) and is included
in built wheels. The same MIT terms apply to that subdirectory and override the
project-wide GPL-3.0-or-later terms for those files only.

## Example data

The example scripts in `examples/` load the files in `examples/data/`. These
files are canonical in this repository and are consumed by the generated
documentation gallery; they are not copied into the documentation repository.

| File | Source | Terms |
| --- | --- | --- |
| `K562_DNase_ENCFF530BKH.chr1.bw` | ENCODE, K562 DNase-seq (experiment ENCSR000EOT, file ENCFF530BKH) | ENCODE data are freely available; cite the ENCODE Consortium and the originating experiment |
| `K562_DNase_hg38_ENCFF413AHU.chr19.bigWig` | ENCODE, K562 DNase-seq (file ENCFF413AHU) | As above |
| `K562_H3K27ac_ENCFF779QTH.chr19.bigWig` | ENCODE, K562 H3K27ac ChIP-seq (file ENCFF779QTH) | As above |
| `K562_GROcap_hg38_mn.chr1.bw`, `K562_GROcap_hg38_pl.chr1.bw` | ENCODE, K562 GRO-cap (Kruesi et al.) | As above |
| `gencodeV24.sub.bed.gz` | GENCODE release 24, derived from Ensembl annotation | GENCODE/Ensembl data are freely available; cite the GENCODE Consortium |
| `AD_Bellenguez_2022.GWAS.TREM2_loci.bed6poly` | Bellenguez et al., *Nature Genetics* (2022), Alzheimer's disease GWAS summary statistics, TREM2 locus | Redistribution and reuse are governed by the terms of the originating publication and data provider; confirm these terms before redistribution |
| `s03.chr22.bam`, `s03.chr22.bam.bai` | Small demonstration alignment | Bundled for illustration |
| `demo.bedpe.gz`, `demo.bedpe.gz.tbi` | Small demonstration interaction file | Bundled for illustration |
| `test.bigBed` | Small demonstration bigBed file | Bundled for illustration |
| `saliency.csv` | Small demonstration numerical signal | Bundled for illustration |

The ENCODE, GENCODE, and GWAS datasets are included solely to make the examples
runnable. Their inclusion does not relicense them. If you redistribute PyGV or
its documentation, verify that each dataset's own terms permit redistribution
and retain the corresponding attribution.

## Build and documentation dependencies

The documentation and gallery are built with third-party Python packages that
are installed as dependencies and are not vendored here. Notable ones include
Sphinx (BSD-2-Clause), MyST-Parser (MIT), the PyData Sphinx Theme
(BSD-3-Clause), Sphinx-Gallery (BSD-3-Clause), and Matplotlib (Matplotlib
license, PSF-based). Their license texts ship with the installed distributions.
