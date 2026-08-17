# vquest releases
### v 0.1.0
#### Aretas Gaspariunas, 2026-08

This repo collates publicly available releases of the [IMGT V-QUEST reference directory](https://www.imgt.org/download/V-QUEST/IMGT_V-QUEST_reference_directory/) — IMGT's per-locus curated alignment reference used by their V-QUEST alignment tool. It covers taxa that IMGT/GENE-DB bulk export does not (e.g. Chondrichthyes shark IGHV, Teleostei). I am not affiliated with IMGT in any way; this exists so historical releases are recoverable, since V-QUEST only exposes the *current* release at any given time.

For the sibling GENE-DB archive, see [genedb-releases](https://github.com/JamieHeather/genedb-releases).

Releases live under `releases/`, named by date of access and IMGT release number (format `YYYYWW-N`, scraped from [refseqh.html](https://www.imgt.org/vquest/refseqh.html)):

```
releases/{YYYY-MM-DD}_VQUEST_{release}/
├── RELEASE
├── Homo_sapiens/
│   ├── IG/
│   │   ├── IGHV.fasta.gz
│   │   ├── IGHJ.fasta.gz
│   │   └── ...
│   └── TR/
│       └── ...
├── Mus_musculus/
│   └── ...
└── ...
```

FASTA files are stored gzipped (`.fasta.gz`) to keep the repo compact — the raw files compress ~7×. Decompress in place with `gunzip` or read directly in Python via `gzip.open(path, 'rt')`.

New releases are detected weekly by a GitHub Action (`.github/workflows/harvest-vquest.yml`) which runs `scripts/harvest-vquest.py`. The script mirrors the full V-QUEST reference tree via `wget --recursive`, so no hardcoded species or gene-prefix list is needed — every subdirectory IMGT publishes is captured automatically.

Because V-QUEST does not expose historical releases, this archive starts from the date of first automated harvest. Older releases cannot be backfilled.

### IMGT licensing information

As of 2026-07-01, IMGT data is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — commercial use is permitted with attribution. This is a meaningful change from the previous CC BY-NC-ND 4.0 license, which restricted use to academic and non-profit users. See [IMGT's terms of use](https://imgt.org/#termsofuse) for the full text.
