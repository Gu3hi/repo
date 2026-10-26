"""Publish a small public snapshot using gh's existing authenticated API session."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess

def main():
    release=json.loads(subprocess.check_output(['gh','api','repos/Gu3hi/repo/releases/tags/packages']))
    assets=[dict(name=a['name'],download_count=a['download_count']) for a in release['assets'] if a['name'].endswith('.deb')]
    expected={p.name for p in (Path(__file__).resolve().parent/'docs/debs').glob('*.deb')}
    assert {a['name'] for a in assets}==expected and len(assets)==len(expected), 'Release assets do not match published packages'
    assert all(type(a['download_count']) is int and a['download_count']>=0 for a in assets)
    snapshot=dict(updated_at=datetime.now(timezone.utc).isoformat(),assets=assets)
    (Path(__file__).resolve().parent/'docs/assets/downloads.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'Refreshed download snapshot for {len(assets)} packages')

if __name__=='__main__':
    main()
