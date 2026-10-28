from pathlib import Path
import bz2, gzip, hashlib, sys, json
from html.parser import HTMLParser
from datetime import datetime
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen
from update_repo import control_from_deb, fields, download_url

site = Path(__file__).resolve().parent / 'docs'
names = ['Packages', 'Packages.gz', 'Packages.bz2', 'Release', 'index.html']
names += ['CydiaIcon.png', 'assets/quart17.png', 'assets/quart17-lock-1.jpg', 'assets/quart17-lock-2.jpg', 'assets/style.css', 'assets/site.js', 'depictions/quart17/index.html', 'depictions/quart17/sileo.json']
names += ['assets/aura.png']
names += ['depictions/aura/index.html', 'depictions/aura/sileo.json']
names += ['assets/home.css', 'assets/Geist.woff2', 'assets/Geist-OFL.txt']
names += ['assets/vela.png','depictions/vela/index.html','depictions/vela/sileo.json']
names += ['assets/downloads.mjs']
names += ['assets/vela-promo.mp4','assets/vela-promo-poster.jpg']
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
vela_architectures=set()
aura_current_architectures=set()
for paragraph in data['Packages'].decode().strip().split('\n\n'):
    if not paragraph:
        continue
    info = {key: value.strip() for key, value in fields(paragraph).items()}
    path = (site / 'debs' / unquote(urlsplit(info['Filename']).path.rsplit('/', 1)[-1])).resolve()
    assert path.is_relative_to(site.resolve()) and path.suffix == '.deb'
    assert info['Filename'] == download_url(path.name), 'APT downloads must use the counted Release asset'
    assert path.relative_to(site).as_posix() not in indexed
    indexed.add(path.relative_to(site).as_posix())
    package = path.read_bytes()
    if len(sys.argv) > 1:
        package = urlopen(info['Filename'], timeout=60).read()
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
        assert info['Version'] in ('1.2.23', '1.2.40')
        if info['Version'] == '1.2.40':
            aura_current_architectures.add(info['Architecture'])
        assert info['Icon'] == 'https://gu3hi.github.io/repo/assets/aura.png'
        assert info['Depiction'] == 'https://gu3hi.github.io/repo/depictions/aura/'
        assert info['SileoDepiction'] == 'https://gu3hi.github.io/repo/depictions/aura/sileo.json'
    if info['Package'] == 'com.gushi.vela':
        assert info['Version']=='0.4.20', 'Only the current Vela release is published'
        vela_architectures.add(info['Architecture'])
        assert info['Icon']=='https://gu3hi.github.io/repo/assets/vela.png'
        assert info['Depiction']=='https://gu3hi.github.io/repo/depictions/vela/'
        assert info['SileoDepiction']=='https://gu3hi.github.io/repo/depictions/vela/sileo.json'
    assert info['Architecture'] in release['Architectures'].split()
assert indexed == {p.relative_to(site).as_posix() for p in site.rglob('*.deb')}
assert aura_current_architectures == {'iphoneos-arm64', 'iphoneos-arm64e'}
snapshot=json.loads(urlopen(base+'assets/downloads.json',timeout=20).read() if len(sys.argv)>1 else (site/'assets/downloads.json').read_bytes())
assert datetime.fromisoformat(snapshot['updated_at']).tzinfo is not None
assert {a['name'] for a in snapshot['assets']}=={Path(p).name for p in indexed}
assert len(snapshot['assets'])==len(indexed)
assert all(type(a['download_count']) is int and a['download_count']>=0 for a in snapshot['assets'])
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
assert data['assets/Geist.woff2'].startswith(b'wOF2')
home = data['index.html'].decode()
assert 'assets/home.css' in home and 'class="home-page"' in home
assert home.count('data-preview=') == 2 and home.count('aria-pressed="true"') == 1
assert all(f'id="{anchor}"' in home for anchor in ('main', 'packages', 'install', 'device-preview'))
assert '预发布 / Prerelease' in home and 'Post-install device validation is pending.' in home
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.counters=[]
    def handle_starttag(self, tag, attrs):
        self.links.extend(v for k,v in attrs if k in ('href','src') and v)
        self.counters.extend(v.split() for k,v in attrs if k=='data-download-files')
for name in ('index.html','depictions/quart17/index.html','depictions/aura/index.html','depictions/vela/index.html'):
    parser=Links(); parser.feed(data[name].decode())
    assert 'sileo://source/https://gu3hi.github.io/repo/' in parser.links
    assert any('assets/downloads.mjs?' in link for link in parser.links)
    expected={p.name for p in (site/'debs').glob('*.deb') if name=='index.html' or p.name.startswith('com.gushi.'+name.split('/')[1]+'_')}
    assert parser.counters and set().union(*(set(group) for group in parser.counters))==expected
    assert all(len(group)==len(set(group)) for group in parser.counters)
    if name!='index.html':
        downloads=[unquote(urlsplit(link).path.rsplit('/',1)[-1]) for link in parser.links if '/releases/download/packages/' in link]
        assert len(downloads)==2 and set(downloads)<=expected
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
    assert r['zh'] and r['en'] and (r['source'].startswith('https://github.com/Gu3hi/Aura-Releases/releases/tag/') or r['source'] == 'https://github.com/Gu3hi/repo/releases/tag/packages')
    assert r['zh'] in data['depictions/aura/index.html'].decode()
    assert r['en'] in aura['tabs'][2]['views'][0]['markdown']
print(f'PASS: Aura bilingual introduction, native depiction and {len(aura_history)} public release records')
print(f'PASS: {len(indexed)} packages; Sileo required fields, package metadata, compressed indexes and checksums verified' + ('; live HTTPS files match' if len(sys.argv)>1 else ''))

assert vela_architectures=={'iphoneos-arm64','iphoneos-arm64e'}
vela=json.loads(data['depictions/vela/sileo.json'])
assert vela['class']=='DepictionTabView'
assert [t['tabname'] for t in vela['tabs']]==['中文','English','更新 / History']
content=json.loads((site.parent/'content/vela.json').read_text(encoding='utf-8'))
assert content['version']=='0.4.20' and content['features']
for i,lang in enumerate(('zh','en')):
    video=vela['tabs'][i]['views'][0]
    assert video['class']=='DepictionVideoView' and video['URL']=='https://gu3hi.github.io/repo/assets/vela-promo.mp4'
    assert video['showPlaybackControls'] is True and video['autoplay'] is False
    md=vela['tabs'][i]['views'][1]['markdown']
    for key in (lang,'scope_'+lang,'install_'+lang,'status_'+lang):
        assert content[key] in md and content[key] in data['depictions/vela/index.html'].decode()
assert '### 功能范围' in vela['tabs'][0]['views'][1]['markdown']
assert 'Vela Studio' in vela['tabs'][0]['views'][1]['markdown']
assert vela['tabs'][2]['views'][0]['markdown'].count('## ')==1
assert content['release_zh'] in vela['tabs'][2]['views'][0]['markdown']
assert content['release_en'] in vela['tabs'][2]['views'][0]['markdown']
assert 'depictions/vela/' in home and 'assets/vela.png' in home
assert not any(x in data['depictions/vela/index.html'].decode() for x in ['15 元','Put_Story（添加','VL1'])
print('PASS: Vela 0.4.20 only; dual packages, bilingual features/scope, current release and Sileo depiction')
assert hashlib.sha256(data['assets/vela-promo.mp4']).hexdigest()=='338b662caaf6ed48e8cbb4b43dc4722d82541812e44477bc98bc7813a978315e'
for page in ('index.html','depictions/vela/index.html'):
    html=data[page].decode()
    assert html.count('<video ')==1 and 'controls playsinline preload="none"' in html
    assert 'assets/vela-promo.mp4' in html and 'assets/vela-promo-poster.jpg' in html
print('PASS: final native-footage promo on homepage, Vela detail and both Sileo language tabs')
