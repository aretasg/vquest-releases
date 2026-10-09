# vquest releases

This repo collates publicly available releases of the [IMGT V-QUEST reference directory](https://www.imgt.org/download/V-QUEST/IMGT_V-QUEST_reference_directory/) — IMGT's per-locus curated alignment reference used by their V-QUEST alignment tool. It covers taxa that IMGT/GENE-DB bulk export does not (e.g. Chondrichthyes shark IGHV, Teleostei). I am not affiliated with IMGT in any way; this exists so historical releases are recoverable, since V-QUEST only exposes the *current* release at any given time.

For the sibling GENE-DB archive, see [genedb-releases](https://github.com/JamieHeather/genedb-releases).

A read-only mirror is available on Codeberg: [codeberg.org/aretasg/vquest-releases](https://codeberg.org/aretasg/vquest-releases).

## V-QUEST vs GENE-DB — when to use which

Both are IMGT germline references and their V/D/J sequences are byte-identical where they overlap (verified: 472/472 shared Human IGHV alleles match exactly at release 202631). They differ in scope and organisation:

| Aspect | GENE-DB | V-QUEST |
| --- | --- | --- |
| Shape | One bulk archive per release; multi-species, multi-locus fastas | Per-species → per-locus → per-gene fastas, pre-split |
| Region types | V/D/J plus constant regions (`CH1`, `CH2`, hinges, transmembrane, cytoplasmic), MHC (`G-ALPHA1-LIKE`), etc. | V/D/J only |
| Pseudogene coverage | Inframe + out-of-frame (`allP` variant) | Inframe only |
| Sequence formats | 5 variants: AA/nt × gapped/ungapped × inframe/all-P | nt-with-gaps only |
| Species coverage | ~40 species, plus extensive strain-level breakdown | 37 species |
| Per-release size | ~5 MB | ~2.5 MB |

**Reach for GENE-DB when you need:** constant regions or antibody structural sub-regions, MHC data, amino-acid sequences, out-of-frame pseudogenes, orphon genes (`IGHV/OR16-*`), strain-level resolution (BALB/c vs C57BL/6 vs …), or species V-QUEST doesn't cover (e.g. `Cercocebus atys`, `Papio anubis`, `Mesocricetus auratus`, additional *Mus* species).

**Reach for V-QUEST when you need:** Chondrichthyes (shark IGHV — VNAR work), Teleostei, cod (`Gadus morhua`), or catfish (`Ictalurus punctatus`) — the taxa GENE-DB genuinely lacks; or when you want files pre-scoped by species/locus/gene so you can just point at `Homo_sapiens/IG/IGHV.fasta.gz` with no header-filter step; or when you're producing outputs meant to align with IMGT's V-QUEST alignment tool.

**For mainstream mammalian V/D/J germline work, either works** — pick based on which format is easier for your pipeline.

## Layout

Releases live under `releases/`, named by date of access and IMGT release number (format `YYYYWW-N`, scraped from [refseqh.html](https://www.imgt.org/vquest/refseqh.html)):

```text
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

Fastas are stored gzipped (`.fasta.gz`) — the raw files compress ~7×. Decompress in place with `gunzip`, or read directly in Python via `gzip.open(path, 'rt')`.

## Updates

New releases are detected weekly by the [GitHub Action](.github/workflows/harvest-vquest.yml), which runs [`scripts/harvest-vquest.py`](scripts/harvest-vquest.py). The script mirrors the full V-QUEST reference tree via `wget --recursive`, so no hardcoded species or gene-prefix list is needed — every subdirectory IMGT publishes is captured automatically.

Because V-QUEST does not expose historical releases, this archive starts from the date of first automated harvest. Older releases cannot be backfilled.

GitHub is the source of truth. Every push to `main` (including harvest commits) is mirrored to [Codeberg](https://codeberg.org/aretasg/vquest-releases) by a [second Action](.github/workflows/mirror-codeberg.yml), which fails if the two copies diverge.

## Licensing

As of 2026-07-01, IMGT data is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — commercial use is permitted with attribution. This is a meaningful change from the previous CC BY-NC-ND 4.0 license, which restricted use to academic and non-profit users. See [IMGT's terms of use](https://imgt.org/#termsofuse) for the full text.
