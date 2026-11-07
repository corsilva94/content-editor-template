"""Extract only the two manifest-listed starter assets into this checkout."""
from pathlib import Path
import sys,json,zipfile,shutil
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'media-manifest.json').read_text())
expected={item['path'] for item in manifest['files']}
with zipfile.ZipFile(sys.argv[1]) as archive:
    if set(archive.namelist())!=expected:
        raise SystemExit('Unexpected archive contents; nothing extracted.')
    for name in expected:
        destination=(root/name).resolve()
        if not destination.is_relative_to(root):raise SystemExit('Unsafe archive path.')
        destination.parent.mkdir(parents=True,exist_ok=True)
        with archive.open(name) as src,destination.open('wb') as dst:shutil.copyfileobj(src,dst)
