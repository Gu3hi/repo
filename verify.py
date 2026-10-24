from pathlib import Path
import bz2, gzip, hashlib, sys
from urllib.request import urlopen

site = Path(__file__).resolve().parent / 'docs'
names = ['Packages', 'Packages.gz', 'Packages.bz2', 'Release', 'index.html']
local = {name: (site / name).read_bytes() for name in names}
data = local
if len(sys.argv) > 1:
    base = sys.argv[1].rstrip('/') + '/'
    data = {name: urlopen(base + name, timeout=20).read() for name in names}
    assert data == local, 'Remote files differ from this checkout'
assert data['Packages'] == b'', 'This repository must remain empty until publication is authorized'
assert not list(site.rglob('*.deb')), 'Unexpected package in empty source'
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
print('PASS: empty source; compressed indexes and all 9 checksums verified' + ('; live HTTPS files match' if len(sys.argv)>1 else ''))
