from pathlib import Path
import bz2, gzip, hashlib, sys, json
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen
from update_repo import control_from_deb, fields

site = Path(__file__).resolve().parent / 'docs'
names = ['Packages', 'Packages.gz', 'Packages.bz2', 'Release', 'index.html']
names += ['CydiaIcon.png', 'assets/quart17.png', 'assets/quart17-lock-1.jpg', 'assets/quart17-lock-2.jpg', 'assets/style.css', 'assets/site.js', 'depictions/quart17/index.html', 'depictions/quart17/sileo.json']
names += ['assets/aura.png']
names += ['depictions/aura/index.html', 'depictions/aura/sileo.json']
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
    if info['Package'] == 'com.gushi.quart17':
        for key, target in [('Icon','assets/quart17.png'), ('Depiction','depictions/quart17/'), ('SileoDepiction','depictions/quart17/sileo.json')]:
            assert info[key] == 'https://gu3hi.github.io/repo/' + target
    if info['Package'] == 'com.gushi.aura':
        assert info['Version'] == '1.2.23'
        assert info['Icon'] == 'https://gu3hi.github.io/repo/assets/aura.png'
        assert info['Depiction'] == 'https://gu3hi.github.io/repo/depictions/aura/'
        assert info['SileoDepiction'] == 'https://gu3hi.github.io/repo/depictions/aura/sileo.json'
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
assert data['CydiaIcon.png'].startswith(b'\x89PNG\r\n\x1a\n')
assert data['assets/quart17.png'].startswith(b'\x89PNG\r\n\x1a\n')
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        self.links.extend(v for k,v in attrs if k in ('href','src') and v)
for name in ('index.html','depictions/quart17/index.html','depictions/aura/index.html'):
    parser=Links(); parser.feed(data[name].decode())
    assert 'sileo://source/https://gu3hi.github.io/repo/' in parser.links
    for link in parser.links:
        parts=urlsplit(link)
        if parts.scheme or not parts.path:
            continue
        path=((site/name).parent/unquote(parts.path)).resolve()
        assert path.is_relative_to(site.resolve()) and path.exists(), (name,link)
depiction=json.loads(data['depictions/quart17/sileo.json'])
assert depiction['class']=='DepictionTabView'
assert [t['tabname'] for t in depiction['tabs']]==['中文','English','更新 / History']
for tab in depiction['tabs']:
    assert tab['class']=='DepictionStackView'
    assert all(v['class']=='DepictionMarkdownView' and v['markdown'] for v in tab['views'])
history=json.loads((site.parent/'content/quart17-history.json').read_text(encoding='utf-8'))
assert len({row['version'] for row in history})==len(history)
for row in history:
    assert row['zh'] and row['en']
    assert row['version'] in data['depictions/quart17/index.html'].decode()
    assert '## '+row['version']+' ·' in depiction['tabs'][2]['views'][0]['markdown']
print(f'PASS: icons, local links, Sileo deep links and native depiction; {len(history)} bilingual history entries')
aura=json.loads(data['depictions/aura/sileo.json'])
assert aura['class']=='DepictionTabView'
assert [t['tabname'] for t in aura['tabs']]==['中文','English','更新 / History']
aura_history=json.loads((site.parent/'content/aura-history.json').read_text(encoding='utf-8'))
assert len({r['version'] for r in aura_history})==len(aura_history)
for t in aura['tabs']:
    assert t['class']=='DepictionStackView' and t['views'][0]['class']=='DepictionMarkdownView'
    assert t['views'][0]['markdown']
for r in aura_history:
    assert r['zh'] and r['en'] and r['source'].startswith('https://github.com/Gu3hi/Aura-Releases/releases/tag/')
    assert r['zh'] in data['depictions/aura/index.html'].decode()
    assert r['en'] in aura['tabs'][2]['views'][0]['markdown']
print(f'PASS: Aura bilingual introduction, native depiction and {len(aura_history)} public release records')
print(f'PASS: {len(indexed)} packages; Sileo required fields, package metadata, compressed indexes and checksums verified' + ('; live HTTPS files match' if len(sys.argv)>1 else ''))
