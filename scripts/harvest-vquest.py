#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
harvest-vquest.py
Check the current IMGT V-QUEST reference directory release
and download the whole species/loci tree if it's a new release.
"""

import gzip
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

release_dir = Path('../releases')
old_releases = sorted(p.name for p in release_dir.iterdir() if not p.name.startswith('.'))
last_release = old_releases[-1].split('_')[-1] if old_releases else ''

print("Last banked release detected:\t" + (last_release or '(none)'))

release_notes_url = "https://www.imgt.org/vquest/refseqh.html"
release_re = re.compile(r"release\s+([0-9]{6}-[0-9]+)", re.IGNORECASE)

try:
    with urllib.request.urlopen(release_notes_url) as in_url:
        release_notes_html = in_url.read().decode('utf-8', errors='replace')
except urllib.error.URLError as err:
    print(err.reason)
    sys.exit()

m = release_re.search(release_notes_html)
if not m:
    print("Could not parse V-QUEST release string from " + release_notes_url)
    sys.exit()
current_release = m.group(1)

print("Currently available release:\t" + current_release)

if current_release != last_release:
    print("Newer release detected: downloading")
    wget_dir = Path('www.imgt.org')

    today = datetime.today().date().isoformat()
    out_dir = release_dir / '_'.join([today, 'VQUEST', current_release])
    wget_cmd = (
        "wget --recursive --no-clobber --page-requisites --convert-links "
        "--domains www.imgt.org --no-parent "
        "https://www.imgt.org/download/V-QUEST/IMGT_V-QUEST_reference_directory/"
    )
    subprocess.call(wget_cmd, shell=True)
    shutil.move(wget_dir / 'download/V-QUEST/IMGT_V-QUEST_reference_directory', out_dir)

    shutil.rmtree(wget_dir)

    # Autoindex sort links (e.g. index.html?C=N;O=D) get saved as literal files
    # by wget — strip them recursively.
    for path in list(out_dir.rglob('*')):
        if path.is_file() and '=' in path.name:
            path.unlink()

    # Record the release string so the archive is self-describing without
    # relying on the directory name alone.
    (out_dir / 'RELEASE').write_text(current_release + '\n')

    # Gzip FASTA files to keep the repo compact (~7x compression),
    # matching the genedb-releases convention.
    for src_path in list(out_dir.rglob('*')):
        if not src_path.is_file() or '.fasta' not in src_path.name or src_path.suffix == '.gz':
            continue
        # mtime=0 and an empty header filename make the output byte-identical
        # for unchanged inputs, so git dedupes them across releases.
        gz_path = src_path.with_name(src_path.name + '.gz')
        with src_path.open('rb') as src, gz_path.open('wb') as raw, \
                gzip.GzipFile(filename='', fileobj=raw, mode='wb', compresslevel=9, mtime=0) as dst:
            shutil.copyfileobj(src, dst)
        src_path.unlink()
