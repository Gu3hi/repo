"""Build the bilingual website and native Sileo depiction from shared history."""
from pathlib import Path
from html import escape as e
import json

ROOT=Path(__file__).resolve().parent
SITE=ROOT/'docs'
BASE='https://gu3hi.github.io/repo/'
ADD='sileo://source/'+BASE
history=json.loads((ROOT/'content/quart17-history.json').read_text(encoding='utf-8'))
assert history and len({r['version'] for r in history})==len(history)
zh='Quart17 在 iOS 17 上实现 iOS 27 的小时间样式，并为越狱设备提供可定制的锁屏音乐播放器、专辑封面、通知排版与缩放，以及下拉清理手势。'
en='Quart17 brings the iOS 27-style compact Lock Screen clock to iOS 17, alongside a customizable music player, album artwork, notification layouts and scaling, and pull-to-clear gestures for jailbroken devices.'
features=[('锁屏音乐播放器','Lock Screen player','播放控制、封面位置与缩放，支持封面进度交互。','Playback controls, artwork positioning and scaling, with artwork-based seeking.'),('通知排版与缩放','Notification layout','调整通知卡片尺寸，让锁屏列表更清晰。','Adjust notification card sizes for a cleaner Lock Screen list.'),('下拉清理手势','Pull to clear','通过手势清理通知，并在设置中调整选项。','Clear notifications with a gesture and customize behavior in Settings.'),('配合 Aura','Works with Aura','当前拆分版的玻璃效果由 Aura 提供；Quart17 保留播放器与通知功能。','Aura provides glass rendering in the current split edition; Quart17 handles player and notification features.')]
features.insert(0,('iOS 27 小时间','iOS 27-style compact clock','在 iOS 17 上实现 iOS 27 的锁屏小时间样式。','Bring the iOS 27-style compact Lock Screen clock to iOS 17.'))

def duo(a,b):return f'<p>{e(a)}</p><p class="en" lang="en">{e(b)}</p>'
def shell(title,body,relative='',page='depictions/quart17/'):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#05080b"><meta name="theme-color" media="(prefers-color-scheme: light)" content="#f3f6f4"><meta name="description" content="Gushi Repo · Jailbreak tweaks for iOS · 中文 / English">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="Gushi Repo · Jailbreak tweaks for iOS"><meta property="og:url" content="{BASE if not relative else BASE+page}"><meta property="og:image" content="{BASE}CydiaIcon.png"><meta name="twitter:card" content="summary">
<title>{e(title)}</title><link rel="icon" href="{relative}CydiaIcon.png"><link rel="stylesheet" href="{relative}assets/style.css?v=20261024-large"><script src="{relative}assets/site.js" defer></script></head>
<body><header class="top" id="top"><div class="bar"><a class="brand" href="{relative or './'}"><img src="{relative}CydiaIcon.png" width="34" height="34" alt="Gushi 头像"><span>Gushi<b>Repo</b></span></a><nav><a class="navlink" href="https://x.com/put_story" target="_blank" rel="noopener">X ↗</a><a class="navlink" href="https://github.com/Gu3hi/repo" target="_blank" rel="noopener">GitHub ↗</a></nav></div></header>
{body}
<footer class="foot"><div class="bigword" aria-hidden="true">GUSHI REPO</div><div class="footline"><span>Gushi Repo · Put_Story</span><a href="https://x.com/put_story" target="_blank" rel="noopener">X @put_story ↗</a><a href="https://github.com/Gu3hi/Quart17" target="_blank" rel="noopener">Quart17 on GitHub ↗</a></div></footer></body></html>'''
def buttons(*extra):
    return f'<div class="actions"><a class="button primary" href="{ADD}"><span class="bl">在 Sileo 中添加<i lang="en">Add to Sileo</i></span><span class="arr">→</span></a>{"".join(extra)}</div>'
def device(relative):
    return f'''<div class="heroart reveal" style="--d:.22s"><div class="glow"></div><div class="float"><div class="pair tilt">
<img src="{relative}assets/quart17-lock-1.jpg" width="680" height="1311" alt="Quart17 锁屏播放器实机效果" decoding="async">
</div></div></div>'''
marquee=''.join(f'<span>{s}</span><b>·</b>' for s in ['GUSHI REPO','JAILBREAK TWEAKS','MAKE YOUR PHONE LOOK BETTER','让你的手机界面看起来更好','QUART17 2.7.112','ROOTLESS / ROOTHIDE','中文 · ENGLISH'])
home=f'''<main>
<section class="hero">
<div class="herotext">
<p class="eyebrow reveal">GUSHI · JAILBREAK REPOSITORY</p>
<h1 class="reveal" style="--d:.06s">Make your <br>phone look <br><em>better.</em></h1>
<p class="hero-subtitle reveal" style="--d:.09s">让你的锁屏，更像你。</p>
<div class="actions reveal" style="--d:.12s">
<a class="button primary" href="{ADD}"><span class="bl">在 Sileo 中添加<i lang="en">Add to Sileo</i></span><span class="arr">→</span></a><a class="button ghost" href="depictions/quart17/">探索 Quart17 <span class="arr">↗</span></a></div>
<button class="addr copy reveal" style="--d:.18s" type="button" data-copy="{BASE}" aria-label="复制源地址 · Copy repository URL">{BASE}<i aria-hidden="true">点击复制 · Tap to copy</i></button>
<p class="hint reveal" style="--d:.24s">在 iPhone 上打开 Sileo 添加，或复制地址手动添加。<br><span lang="en">Open in Sileo on iPhone, or copy the source URL.</span></p>
</div>
{device('')}
</section>
<div class="marquee" aria-hidden="true"><div class="mtrack"><div class="mg">{marquee}</div><div class="mg">{marquee}</div></div></div>
<section class="featured" id="packages">
<div class="seclabel reveal"><b>01</b><span>FEATURED PACKAGE · 精选插件</span></div>
<article class="package reveal" style="--d:.08s"><img class="appicon" src="assets/quart17.png" width="96" height="96" alt="Quart17 图标" loading="lazy" decoding="async"><div>
<div class="ptag">AVAILABLE · 2.7.112</div><h2>Quart17</h2>{duo(zh,en)}
<div class="tags"><span>Rootless</span><span>RootHide</span><span>中文 / English</span></div>
<a class="textlink" href="depictions/quart17/">功能介绍与完整更新记录 / Features &amp; changelog <i class="ta">→</i></a>
</div></article>
<article class="package reveal"><img class="appicon" src="assets/aura.png" width="96" height="96" alt="Aura 图标" loading="lazy" decoding="async"><div>
<div class="ptag">PRERELEASE · 1.2.23</div><h2>Aura</h2>{duo('为控制中心、Dock、文件夹与应用组件带来玻璃效果，可与 Quart17 配合使用。','Glass effects for Control Center, the Dock, folders and app components. Works alongside Quart17.')}
<div class="tags"><span>Rootless</span><span>RootHide</span><span>预发布 / Prerelease</span></div>
<a class="textlink" href="depictions/aura/">功能介绍与更新记录 / Features &amp; changelog <i class="ta">→</i></a>
<p class="hint">{e('1.2.23 入场时机修订包；安装后真机验收尚未完成。')}<br><span lang="en">Corrected alert presentation build. Post-install device validation is pending.</span></p>
</div></article>
<aside class="note reveal" style="--d:.14s"><h3>架构提示 <i lang="en">Pick your jailbreak</i></h3>{duo('仅发布匹配越狱环境的安装包；不要仅凭设备处理器型号选择架构。','Choose the package for your jailbreak environment, not just your device’s processor.')}</aside>
</section>
</main>'''
cards=''.join(f'<article class="reveal" style="--d:{i*.06:.2f}s"><em class="fnum">0{i+1}</em><h3>{e(a)}<i lang="en">{e(b)}</i></h3>{duo(c,d)}</article>' for i,(a,b,c,d) in enumerate(features))
entries=[]
for i,row in enumerate(history):
    assert row['kind'] in ('commit','release','release-reference','local')
    source=f'<a href="{e(row["source"],quote=True)}">原始记录 / Source ↗</a>' if row['source'] else '<span>本地版本记录 / Local version record</span>'
    entries.append(f'<details {"open" if i==0 else ""}><summary><b>{e(row["version"])}</b><time>{e(row["date"])}</time><i class="chev" aria-hidden="true">＋</i></summary><div class="acc"><div class="entry">{duo(row["zh"],row["en"])}<div class="source">{source}</div></div></div></details>')
downloads=''.join(f'<a class="button ghost" href="../../debs/com.gushi.quart17_2.7.112_{arch}.deb"><span class="bl">{label} · 2.7.112<i lang="en">Download</i></span><span class="arr">↓</span></a>' for arch,label in [('iphoneos-arm64','Rootless'),('iphoneos-arm64e','RootHide')])
body=f'''<main>
<section class="dhero">
<a class="back" href="../../">← Gushi Repo</a>
<div class="titleline reveal"><img class="appicon" src="../../assets/quart17.png" width="104" height="104" alt="Quart17 图标"><div><p class="eyebrow">LOCK SCREEN, REIMAGINED</p><h1>Quart17</h1><div class="tags"><span>2.7.112</span><span>Put_Story</span><span>iOS 17</span></div></div></div>
<div class="lede reveal" style="--d:.08s">{duo(zh,en)}</div>
<div class="reveal" style="--d:.14s">{buttons(*downloads)}</div>
<nav class="section-nav" aria-label="详情导航"><a href="#features">功能 / Features</a><a href="#screenshots">实机效果 / Gallery</a><a href="#changelog">更新记录 / Changelog</a></nav>
</section>
<section id="features"><div class="seclabel reveal"><b>01</b><span>FEATURES · 功能</span></div><div class="grid">{cards}</div></section>
<section id="screenshots"><div class="seclabel reveal"><b>02</b><span>ON DEVICE · 实机效果</span></div><div class="shots reveal" style="--d:.06s"><figure><img src="../../assets/quart17-lock-1.jpg" width="680" height="1311" alt="Quart17 锁屏播放器实机效果" loading="lazy" decoding="async"><figcaption>锁屏播放器 · <i lang="en">Lock Screen player</i></figcaption></figure></div></section>
<section class="note install reveal"><h3>安装说明 <i lang="en">Installation</i></h3>{duo('本版要求 iOS 17。RootHide 经用户真机测试确认；rootless 已构建验包，尚未真机测试。Rootless 与 RootHide 安装包不可混用。安装后进入「设置 → Quart17」配置。','This release requires iOS 17. RootHide testing was confirmed by the user; rootless has been built and inspected but has not been device-tested. Use the package matching Rootless or RootHide, then configure Settings → Quart17.')}<p class="hint">玻璃效果可另装 <a href="https://github.com/Gu3hi/Aura-Releases/releases" target="_blank" rel="noopener">Aura</a>。旧版历史中的玻璃功能不代表当前 Quart17 内置这些功能。<br><span lang="en">Install Aura separately for glass effects. Historical glass features listed below are not bundled with the current Quart17 edition.</span></p></section>
<section id="changelog"><div class="seclabel reveal"><b>03</b><span>CHANGELOG · 历史更新</span></div>
<p class="hint reveal" style="--d:.06s">按 GitHub 发布说明、版本提交及本地构建记录整理；日期优先采用发布时间。未记录的改动不作推测。<br><span lang="en">Based on release notes, version commits and local build records; release dates are preferred when available. Undocumented changes are not inferred.</span></p>
<div class="count reveal" style="--d:.1s"><b>{len(history)}</b><span>条记录 / <i lang="en">entries</i></span><button class="toggleall" type="button" aria-expanded="false">展开全部 · Expand all</button></div>
{''.join(entries)}</section>
</main>'''
detail=SITE/'depictions/quart17';detail.mkdir(parents=True,exist_ok=True)
(SITE/'index.html').write_text(shell('Gushi Repo · Quart17',home),encoding='utf-8',newline='\n')
(detail/'index.html').write_text(shell('Quart17 · 介绍与历史更新 / Features & Changelog',body,'../../'),encoding='utf-8',newline='\n')
def markdown(text):return {'class':'DepictionMarkdownView','markdown':text,'useRawFormat':False}
def tab(name,text):return {'class':'DepictionStackView','tabname':name,'views':[markdown(text)]}
zh_intro=f'# Quart17 · 2.7.112\n\n{zh}\n\n'+'\n\n'.join(f'### {a}\n{c}' for a,b,c,d in features)+'\n\n### 安装\n本版要求 iOS 17。RootHide 经用户真机测试确认；rootless 尚未真机测试。请按环境选择 Rootless / RootHide。安装后前往「设置 → Quart17」。玻璃效果由独立的 Aura 提供。'
en_intro=f'# Quart17 · 2.7.112\n\n{en}\n\n'+'\n\n'.join(f'### {b}\n{d}' for a,b,c,d in features)+'\n\n### Installation\nThis release requires iOS 17. RootHide testing was confirmed by the user; rootless device testing remains pending. Choose Rootless or RootHide for your environment, then configure Settings → Quart17. Glass rendering is provided separately by Aura.'
log='Historical glass features later moved to Aura. / 历史玻璃功能后续已迁移至 Aura。\n\n'+'\n\n'.join(f'## {r["version"]} · {r["date"]}\n\n{r["zh"]}\n\n{r["en"]}\n\n'+(f'[原始记录 / Source]({r["source"]})' if r['source'] else '本地版本记录 / Local version record') for r in history)
depiction={'class':'DepictionTabView','minVersion':'0.3','tintColor':'#2859D8','tabs':[tab('中文',zh_intro),tab('English',en_intro),tab('更新 / History',log)]}
(detail/'sileo.json').write_text(json.dumps(depiction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(f'Built bilingual pages and Sileo depiction with {len(history)} history entries')

aura_history=json.loads((ROOT/'content/aura-history.json').read_text(encoding='utf-8'))
assert len({r['version'] for r in aura_history})==len(aura_history)
aura_zh='Aura 为 iOS 16–17 越狱设备的系统界面与应用组件带来可调节的玻璃效果，可与 Quart17 配合使用。'
aura_en='Aura brings customizable glass effects to system surfaces and app components on jailbroken iOS 16–17 devices, and works alongside Quart17.'
aura_features=[
    ('通知与锁屏','Notifications & Lock Screen','通知卡片、横幅与锁屏通知玻璃，可调圆角、底色和边缘高光；支持 Quart17 播放器玻璃。','Glass for notification cards, banners, Lock Screen notifications and the Quart17 player, with adjustable corners, tint and edge highlights.'),
    ('控制中心与桌面','Control Center & Home Screen','控制中心模块、Dock、文件夹、桌面搜索胶囊、App 资源库搜索框与音量条玻璃。','Glass for Control Center modules, the Dock, folders, Home Screen search, App Library search and the volume HUD.'),
    ('弹窗与菜单','Popups & menus','系统弹窗、快捷菜单与弹出按钮玻璃，支持通知与弹窗强制深色。','Glass for system popups, context menus and pop-up buttons, with forced dark appearance options for notifications and popups.'),
    ('按 App 配置组件','Per-app components','独立开关 Tab 栏、标准按钮、搜索框玻璃与导航栏渐进模糊，也可去除分割线。','Per-app controls for tab bar, standard button and search bar glass, progressive navigation bar blur and separator removal.'),
    ('高光与动态效果','Highlights & motion','陀螺仪高光随手机倾斜改变光源方向；锁屏上滑边缘圆角与折射属于实验功能。','Gyroscope-driven highlights respond to device tilt. Lock Screen swipe-up edge rounding and refraction are experimental.'),
    ('预设与偏好备份','Presets & preference backup','支持应用作者预设、复制与导入偏好。使用设备绑定激活码，激活后可离线使用。','Apply the author preset and copy or import preferences. Uses device-bound activation and works offline after activation.')
]
aura_install_zh='安装与越狱环境匹配的一个包：Rootless 为 iphoneos-arm64，RootHide 为 iphoneos-arm64e。安装后前往「设置 → Aura」配置。Aura 使用设备绑定激活；安装包下载不代表已激活。'
aura_install_en='Install one package matching your jailbreak: iphoneos-arm64 for Rootless, or iphoneos-arm64e for RootHide. Configure Settings → Aura after installation. Aura uses device-bound activation; downloading the package does not activate it.'
aura_status_zh='当前上架 1.2.23 同版本修订包，仍为预发布版。安装后真机验收尚未完成，Rootless 未实机测试。'
aura_status_en='The repository hosts the revised 1.2.23 packages. This remains a prerelease; post-install device validation is pending, and Rootless has not been tested on a physical device.'
aura_cards=''.join(f'<article><em class="fnum">0{i+1}</em><h3>{e(a)}<i lang="en">{e(b)}</i></h3>{duo(c,d)}</article>' for i,(a,b,c,d) in enumerate(aura_features))
aura_entries=''.join(f'<details {"open" if i==0 else ""}><summary><b>{e(r["version"])}</b><time>{e(r["date"])}</time><i class="chev" aria-hidden="true">＋</i></summary><div class="entry">{duo(r["zh"],r["en"])}<p class="source"><a href="{e(r["source"])}">原始发布说明 / Release notes ↗</a></p></div></details>' for i,r in enumerate(aura_history))
aura_downloads=''.join(f'<a class="button ghost" href="../../debs/com.gushi.aura_1.2.23_{arch}.deb"><span class="bl">{label} · 1.2.23<i lang="en">Download</i></span><span class="arr">↓</span></a>' for arch,label in [('iphoneos-arm64','Rootless'),('iphoneos-arm64e','RootHide')])
aura_body=f'''<main><section class="dhero"><a class="back" href="../../">← Gushi Repo</a>
<div class="titleline"><img class="appicon" src="../../assets/aura.png" width="104" height="104" alt="Aura 图标"><div><p class="eyebrow">GLASS, YOUR WAY</p><h1>Aura</h1><div class="tags"><span>1.2.23</span><span>iOS 16–17</span><span>预发布 / Prerelease</span></div></div></div>
<div class="lede">{duo(aura_zh,aura_en)}</div>{buttons(*aura_downloads)}
<nav class="section-nav" aria-label="详情导航"><a href="#features">功能 / Features</a><a href="#installation">安装 / Installation</a><a href="#changelog">更新记录 / Changelog</a></nav></section>
<section id="features"><div class="seclabel"><b>01</b><span>FEATURES · 功能</span></div><div class="grid">{aura_cards}</div></section>
<section id="installation" class="note install"><h3>安装与激活 <i lang="en">Installation &amp; activation</i></h3>{duo(aura_install_zh,aura_install_en)}<div class="hint">{duo(aura_status_zh,aura_status_en)}</div><a class="textlink" href="https://github.com/Gu3hi/Aura-Releases/releases">发布与支持 / Releases &amp; support ↗</a></section>
<section id="changelog"><div class="seclabel"><b>02</b><span>CHANGELOG · 历史更新</span></div>{duo('以下整理了目前可核实的两条 GitHub 公开发布记录，包含 1.2.23 的同版本修订说明。更早或中间版本缺少独立发布说明，未推测其改动。','The two verifiable public GitHub releases are listed below, including the same-version revision of 1.2.23. Earlier and intermediate versions without standalone release notes are not reconstructed.')}<div class="count"><b>{len(aura_history)}</b><span>公开发布 / Public releases</span><button class="toggleall" type="button" aria-expanded="false">展开全部 · Expand all</button></div>{aura_entries}</section></main>'''
aura_dir=SITE/'depictions/aura';aura_dir.mkdir(parents=True,exist_ok=True)
(aura_dir/'index.html').write_text(shell('Aura · 介绍与历史更新 / Features & Changelog',aura_body,'../../','depictions/aura/'),encoding='utf-8',newline='\n')
aura_zh_md='# Aura · 1.2.23\n\n'+aura_zh+'\n\n'+'\n\n'.join(f'### {a}\n{c}' for a,b,c,d in aura_features)+'\n\n### 安装与激活\n'+aura_install_zh+'\n\n'+aura_status_zh
aura_en_md='# Aura · 1.2.23\n\n'+aura_en+'\n\n'+'\n\n'.join(f'### {b}\n{d}' for a,b,c,d in aura_features)+'\n\n### Installation & activation\n'+aura_install_en+'\n\n'+aura_status_en
aura_log='Only verifiable public releases are listed. / 仅收录可核实的公开发布记录。\n\n'+'\n\n'.join(f'## {r["version"]} · {r["date"]}\n\n{r["zh"]}\n\n{r["en"]}\n\n[发布说明 / Release notes]({r["source"]})' for r in aura_history)
(aura_dir/'sileo.json').write_text(json.dumps({'class':'DepictionTabView','minVersion':'0.3','tintColor':'#2859D8','tabs':[tab('中文',aura_zh_md),tab('English',aura_en_md),tab('更新 / History',aura_log)]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(f'Built Aura bilingual pages and Sileo depiction with {len(aura_history)} public release records')
