from pathlib import Path
import bz2, gzip, hashlib, sys
from urllib.request import urlopen
from update_repo import control_from_deb, fields

site = Path(__file__).resolve().parent / 'docs'
names = ['Packages', 'Packages.gz', 'Packages.bz2', 'Release', 'index.html']
local = {name: (site / name).read_bytes() for name in names}
data = local
if len(sys.argv) > 1:
    base = sys.argv[1].rstrip('/') + '/'
    data = {name: urlopen(base + name, timeout=20).read() for name in names}
    assert data == local, 'Remote files differ from this checkout'
release = fields(data['Release'].decode())
# Sileo RepoManager requires Components even for flat repositories.
assert all(key in release and release[key].strip() for key in ('Origin', 'Label', 'Architectures', 'Components'))
indexed = set()
for paragraph in data['Packages'].decode().strip().split('\n\n'):
    if not paragraph:
        continue
    info = {key: value.strip() for key, value in fields(paragraph).items()}
    path = (site / info['Filename']).resolve()
    assert path.is_relative_to(site.resolve()) and path.suffix == '.deb'
    assert info['Filename'] not in indexed
    indexed.add(info['Filename'])
    package = path.read_bytes()
    if len(sys.argv) > 1:
        package = urlopen(base + info['Filename'], timeout=30).read()
        assert package == path.read_bytes()
    assert len(package) == int(info['Size'])
    for key, algorithm in [('MD5sum', 'md5'), ('SHA256', 'sha256'), ('SHA512', 'sha512')]:
        assert hashlib.new(algorithm, package).hexdigest() == info[key]
    actual = fields(control_from_deb(package))
    for key in ('Package', 'Version', 'Architecture'):
        assert actual[key].strip() == info[key]
    assert info['Architecture'] in release['Architectures'].split()
assert indexed == {p.relative_to(site).as_posix() for p in site.rglob('*.deb')}
assert gzip.decompress(data['Packages.gz']) == data['Packages']
assert bz2.decompress(data['Packages.bz2']) == data['Packages']
algorithm = None
checked = 0
for line in data['Release'].decode().splitlines():
    if not line.startswith(' '):
        algorithm = {'MD5Sum:': 'md5', 'SHA256:': 'sha256', 'SHA512:': 'sha512'}.get(line)
    elif algorithm:
        digest, size, name = line.split()
        assert name in data and int(size) == len(data[name]), name
        assert hashlib.new(algorithm, data[name]).hexdigest() == digest, name
        checked += 1
assert checked == 9
print(f'PASS: {len(indexed)} packages; Sileo required fields, package metadata, compressed indexes and checksums verified' + ('; live HTTPS files match' if len(sys.argv)>1 else ''))
