#!/usr/bin/env python3
"""Copy the brand CSS, JSON and fonts into a composition so it can link brand/brand.css.

Usage (from the job folder):  python3 work/brand-kit/stage.py work/<video>/composition
The starter build.py already embeds the brand; this helper is for hand-built compositions.
"""
from pathlib import Path
import shutil
import sys

kit = Path(__file__).resolve().parent
job = kit.parents[1]
if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 work/brand-kit/stage.py work/<video>/<composition>')
target = Path(sys.argv[1]).resolve()
if not target.is_relative_to(job / 'work') or target == kit or target.is_relative_to(kit):
    raise SystemExit('Composition must be inside this job/work, outside the brand-kit folder.')
dest = target / 'brand'
if dest.is_symlink() or (dest / 'fonts').is_symlink():
    raise SystemExit('Refusing a symlinked asset destination.')
dest.mkdir(parents=True, exist_ok=True)
shutil.copy2(kit / 'brand.css', dest / 'brand.css')
shutil.copy2(kit / 'brand.json', dest / 'brand.json')
shutil.copytree(kit / 'fonts', dest / 'fonts', dirs_exist_ok=True)
print(f'Staged brand assets: {dest}')
print('Add <link rel="stylesheet" href="brand/brand.css"> and use the brand-* classes.')
