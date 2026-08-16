#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
harvest-vquest.py
Check the current IMGT V-QUEST reference directory release
and download the whole species/loci tree if it's a new release.
"""

import gzip
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime

__email__ = 'aretasgasp@gmail.com'
__version__ = '0.1.0'
__author__ = 'Aretas Gaspariunas'

release_dir = '../releases/'
old_releases = sorted(os.listdir(release_dir))
old_releases = [x for x in old_releases if not x.startswith('.')]
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
    wget_dir = 'www.imgt.org/'

    today = datetime.today().date().isoformat()
    out_dir = release_dir + '_'.join([today, 'VQUEST', current_release]) + '/'
    wget_cmd = (
        "wget --recursive --no-clobber --page-requisites --convert-links "
        "--domains www.imgt.org --no-parent "
        "https://www.imgt.org/download/V-QUEST/IMGT_V-QUEST_reference_directory/"
    )
    subprocess.call(wget_cmd, shell=True)
    shutil.move(wget_dir + 'download/V-QUEST/IMGT_V-QUEST_reference_directory/', out_dir)

    shutil.rmtree(wget_dir)

    # Autoindex sort links (e.g. index.html?C=N;O=D) get saved as literal files
    # by wget — strip them recursively.
    for root, _dirs, files in os.walk(out_dir):
        for fname in files:
            if '=' in fname:
                os.remove(os.path.join(root, fname))

    # Record the release string so the archive is self-describing without
    # relying on the directory name alone.
    with open(out_dir + 'RELEASE', 'w') as fh:
        fh.write(current_release + '\n')

    # Gzip FASTA files to keep the repo compact (~7x compression),
    # matching the genedb-releases convention.
    for root, _dirs, files in os.walk(out_dir):
        for fname in files:
            if '.fasta' not in fname or fname.endswith('.gz'):
                continue
            src_path = os.path.join(root, fname)
            with open(src_path, 'rb') as src, gzip.open(src_path + '.gz', 'wb', compresslevel=9) as dst:
                shutil.copyfileobj(src, dst)
            os.remove(src_path)
