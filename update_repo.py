"""Regenerate the flat APT index from the DEBs deliberately placed in docs/debs."""
from pathlib import Path
import bz2, gzip, hashlib, io, tarfile
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = Path(__file__).resolve().parent / 'docs'

def control_from_deb(data):
    assert data[:8] == b'!<arch>\n', 'Invalid DEB archive'
    offset = 8
    while offset < len(data):
        header = data[offset:offset + 60]
        assert len(header) == 60 and header[58:] == b'`\n'
        size = int(header[48:58]); start = offset + 60
        assert 0 <= size <= len(data) - start
        name = header[:16].decode('ascii').strip().rstrip('/')
        if name.startswith('control.tar'):
            with tarfile.open(fileobj=io.BytesIO(data[start:start + size])) as archive:
                members = [m for m in archive if m.name in ('control', './control')]
                assert len(members) == 1 and members[0].isfile() and members[0].size < 1048576
                text = archive.extractfile(members[0]).read().decode('utf-8').strip()
                assert '\n\n' not in text
                return text
        offset = start + size + size % 2
    raise ValueError('Missing control archive')

def fields(text):
    return dict(line.split(':', 1) for line in text.splitlines() if line and not line[0].isspace())

def main():
    entries = []; identities = set()
    for path in sorted((ROOT / 'debs').glob('*.deb')):
        data = path.read_bytes(); control = control_from_deb(data); info = fields(control)
        identity = tuple(info[key].strip() for key in ('Package', 'Version', 'Architecture'))
        assert identity not in identities, f'Duplicate package: {identity}'
        identities.add(identity)
        assert not any(k in info for k in ('Filename', 'Size', 'MD5sum', 'SHA256', 'SHA512'))
        entry = control
        if identity[0] == 'com.gushi.quart17':
            entry += '\nIcon: https://gu3hi.github.io/repo/assets/quart17.png'
            entry += '\nDepiction: https://gu3hi.github.io/repo/depictions/quart17/'
            entry += '\nSileoDepiction: https://gu3hi.github.io/repo/depictions/quart17/sileo.json'
        if identity[0] == 'com.gushi.aura':
            entry += '\nIcon: https://gu3hi.github.io/repo/assets/aura.png'
            entry += '\nDepiction: https://gu3hi.github.io/repo/depictions/aura/'
            entry += '\nSileoDepiction: https://gu3hi.github.io/repo/depictions/aura/sileo.json'
        if identity[0] == 'com.gushi.vela':
            entry += '\nIcon: https://gu3hi.github.io/repo/assets/vela.png'
            entry += '\nDepiction: https://gu3hi.github.io/repo/depictions/vela/'
            entry += '\nSileoDepiction: https://gu3hi.github.io/repo/depictions/vela/sileo.json'
        entry += f'\nFilename: {path.relative_to(ROOT).as_posix()}\nSize: {len(data)}\n'
        for key, algorithm in [('MD5sum', 'md5'), ('SHA256', 'sha256'), ('SHA512', 'sha512')]:
            entry += f'{key}: {hashlib.new(algorithm, data).hexdigest()}\n'
        entries.append(entry)
    packages = ('\n'.join(entries) + ('\n' if entries else '')).encode()
    payloads = {'Packages': packages, 'Packages.gz': gzip.compress(packages, mtime=0), 'Packages.bz2': bz2.compress(packages)}
    release = ['Origin: Gushi Repo', 'Label: Gushi Repo', 'Suite: stable', 'Version: 1.0',
               'Codename: gushi', 'Architectures: iphoneos-arm iphoneos-arm64 iphoneos-arm64e',
               'Components: main', 'Description: Gushi jailbreak repository',
               'Icon: https://gu3hi.github.io/repo/CydiaIcon.png',
               'Date: ' + format_datetime(datetime.now(timezone.utc), usegmt=True)]
    for label, algorithm in [('MD5Sum', 'md5'), ('SHA256', 'sha256'), ('SHA512', 'sha512')]:
        release.append(label + ':')
        for name, data in payloads.items():
            release.append(f' {hashlib.new(algorithm, data).hexdigest()} {len(data)} {name}')
    for name, data in payloads.items():
        (ROOT / name).write_bytes(data)
    (ROOT / 'Release').write_text('\n'.join(release) + '\n', encoding='utf-8', newline='\n')
    print(f'Indexed {len(entries)} packages')

if __name__ == '__main__':
    main()
