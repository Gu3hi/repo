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
    is_home=not relative
    home_style='<link rel="stylesheet" href="assets/home.css?v=20261026">' if is_home else ''
    home_nav='<a class="navlink" href="#packages">插件</a><a class="navlink" href="#install">安装指南</a>' if is_home else ''
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#000000"><meta name="theme-color" media="(prefers-color-scheme: light)" content="#f5f5f3"><meta name="description" content="Gushi Repo · Jailbreak tweaks for iOS · 中文 / English">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="Gushi Repo · Jailbreak tweaks for iOS"><meta property="og:url" content="{BASE if not relative else BASE+page}"><meta property="og:image" content="{BASE}CydiaIcon.png"><meta name="twitter:card" content="summary">
<title>{e(title)}</title><link rel="icon" href="{relative}CydiaIcon.png"><link rel="stylesheet" href="{relative}assets/style.css?v=20261026-source">{home_style}<script src="{relative}assets/site.js?v=20261026" defer></script></head>
<body class="{'home-page' if is_home else 'detail-page'}"><a class="skip-link" href="#main">跳至内容 · Skip to content</a><header class="top" id="top"><div class="bar"><a class="brand" href="{relative or './'}" aria-label="Gushi Repo 首页"><img src="{relative}CydiaIcon.png" width="34" height="34" alt=""><span>Gushi<b>Repo</b></span></a><nav aria-label="主导航">{home_nav}<a class="navlink social" href="https://x.com/put_story" target="_blank" rel="noopener">X ↗</a><a class="navlink" href="https://github.com/Gu3hi/repo" target="_blank" rel="noopener">GitHub ↗</a></nav></div></header>
{body}
<footer class="foot"><div class="bigword" aria-hidden="true">GUSHI REPO</div><div class="footline"><span>Gushi Repo · Put_Story</span><a href="https://x.com/put_story" target="_blank" rel="noopener">X @put_story ↗</a><a href="https://github.com/Gu3hi/Quart17" target="_blank" rel="noopener">Quart17 on GitHub ↗</a></div></footer></body></html>'''
def buttons(*extra):
    return f'<div class="actions"><a class="button primary" href="{ADD}"><span class="bl">在 Sileo 中添加<i lang="en">Add to Sileo</i></span><span class="arr">→</span></a>{"".join(extra)}</div>'
home=f'''<main id="main">
<section class="source-hero" aria-labelledby="hero-title">
<div class="hero-copy">
<p class="kicker reveal"><span class="status-dot" aria-hidden="true"></span> 独立开发，为你的 iPhone <span lang="en">Made by Put_Story</span></p>
<h1 id="hero-title" class="reveal" style="--d:.08s">熟悉的 iPhone。<br>更喜欢的样子。</h1>
<p class="hero-english reveal" lang="en" style="--d:.16s">Your iPhone. A little more you.</p>
<p class="hero-description reveal" style="--d:.24s">从锁屏的音乐，到界面的玻璃质感。<br>为越狱后的日常，添一点自己的风格。</p>
<div class="hero-actions reveal" style="--d:.32s"><a class="source-button" href="{ADD}">添加到 Sileo <span aria-hidden="true">↗</span></a><span class="action-caption" lang="en">Add the source.<br>Make it yours.</span></div>
<button class="source-copy copy reveal" style="--d:.4s" type="button" data-copy="{BASE}" aria-label="复制源地址 · Copy repository URL"><span>gu3hi.github.io/repo/</span><span class="copy-label">复制地址 <span aria-hidden="true">⧉</span></span></button>
<div class="hero-support reveal" style="--d:.48s"><span>Rootless / RootHide</span><span>中文 / English</span></div>
</div>
<figure class="device-stage reveal" style="--d:.24s">
<div class="device-meta"><span>Quart17</span><span>ON DEVICE / 实机效果</span></div>
<div class="device-view" id="device-preview"><img class="wallpaper-shot" aria-hidden="true" src="assets/quart17-lock-2.jpg" width="680" height="1311" alt="同一设备的壁纸视图" decoding="async"><img class="player-shot" src="assets/quart17-lock-1.jpg" width="680" height="1311" alt="Quart17 锁屏音乐播放器实机效果" decoding="async" fetchpriority="high"></div>
<figcaption><div class="view-switch" role="group" aria-label="切换实机视图 · Device preview"><button type="button" data-preview="player" aria-controls="device-preview" aria-pressed="true">音乐播放器</button><button type="button" data-preview="wallpaper" aria-controls="device-preview" aria-pressed="false">壁纸视图</button></div><span class="preview-note">点击，换个视角 <span aria-hidden="true">↗</span></span></figcaption>
</figure>
</section>
<section class="collection" id="packages" aria-labelledby="collection-title">
<div class="section-heading reveal"><div><p class="section-index">01 / THE COLLECTION</p><h2 id="collection-title">各有所长，一起刚好。</h2></div><p lang="en">Small details.<br>A different everyday.</p></div>
<div class="product-grid">
<article class="product-card vela-card reveal">
<div class="product-top"><img src="assets/vela.png" width="64" height="64" alt="Vela 图标" loading="lazy"><span class="version-label">0.4.19 <span>当前版本 / Current</span></span></div>
<h3>Vela</h3><p class="product-lead">常用控制，一次上滑。</p><p class="product-english" lang="en">Your everyday controls, one swipe away.</p>
<p class="product-description">连接、音乐、亮度与音量，集中在浮动面板中。横滑进入快捷指令页，自由配置配色、主题和玻璃外观。</p><p class="product-description en" lang="en">Connectivity, music, brightness and volume in one floating panel. Swipe to shortcuts and configure colors, themes and optional glass.</p>
<ul class="feature-list"><li>快捷指令两列四行 <span lang="en">Two columns, four visible rows</span></li><li>可重放的手势导览 <span lang="en">Replayable gesture tour</span></li><li>配色与主题无需激活 <span lang="en">Colors and themes, no activation</span></li></ul>
<div class="product-bottom"><span>iOS 16+ · Rootless · RootHide</span><a href="depictions/vela/" class="product-link" aria-label="查看 Vela 功能范围与安装说明">探索 Vela <span aria-hidden="true">↗</span></a></div>
</article>

<article class="product-card quart-card reveal">
<div class="product-top"><img src="assets/quart17.png" width="64" height="64" alt="Quart17 图标" loading="lazy"><span class="version-label">2.7.112 <span>当前版本 / Current</span></span></div>
<h3>Quart17</h3><p class="product-lead">让锁屏，跟着你的节奏。</p><p class="product-english" lang="en">A Lock Screen that feels like you.</p>
<p class="product-description">小时间、音乐播放器、专辑封面与通知排版。<br>从一眼看见，到随手操控，都由你来调整。</p><p class="product-description en" lang="en">Compact clock, music controls, album artwork and notification layouts. Customize the details you see and use.</p>
<ul class="feature-list"><li>锁屏播放器 <span lang="en">Music player</span></li><li>通知布局与缩放 <span lang="en">Notification layout</span></li><li>下拉清理手势 <span lang="en">Pull to clear</span></li></ul>
<div class="product-bottom"><span>Rootless · RootHide</span><a href="depictions/quart17/" class="product-link" aria-label="探索 Quart17 功能与更新记录">探索 Quart17 <span aria-hidden="true">↗</span></a></div>
</article>
<article class="product-card aura-card reveal" style="--d:.09s">
<div class="product-top"><img src="assets/aura.png" width="64" height="64" alt="Aura 图标" loading="lazy"><span class="version-label">1.2.23 <span>预发布 / Prerelease</span></span></div>
<h3>Aura</h3><p class="product-lead">给日常界面，一点通透。</p><p class="product-english" lang="en">A softer view of the familiar.</p>
<p class="product-description">控制中心、Dock、文件夹与应用组件的玻璃效果。可独立配置，也可与 Quart17 配合使用。</p><p class="product-description en" lang="en">Glass effects for Control Center, the Dock, folders and app components. Configurable on its own, or alongside Quart17.</p>
<aside class="release-note"><span class="status-dot" aria-hidden="true"></span><div><strong>预发布说明</strong><p>1.2.23 入场时机修订包，安装后真机验收尚未完成。</p><p lang="en">Corrected alert presentation build. Post-install device validation is pending.</p></div></aside>
<div class="product-bottom"><span>Rootless · RootHide</span><a href="depictions/aura/" class="product-link" aria-label="探索 Aura 功能与更新记录">探索 Aura <span aria-hidden="true">↗</span></a></div>
</article>
</div>
</section>
<section class="manifesto" aria-label="设计理念"><p class="section-index">MADE FOR THE EVERYDAY</p><h2><span class="word-reveal">不必</span><span class="word-reveal" style="--word-delay:.08s">换一部</span><span class="word-reveal" style="--word-delay:.16s">手机。</span><br><span class="word-reveal" style="--word-delay:.24s">换一种，</span><span class="word-reveal" style="--word-delay:.32s">每天见面的</span><span class="word-reveal" style="--word-delay:.4s">方式。</span></h2><p lang="en">Keep the iPhone you know.<br>Make the everyday feel your own.</p></section>
<section class="installation" id="install" aria-labelledby="install-title">
<div class="section-heading reveal"><div><p class="section-index">02 / GET STARTED</p><h2 id="install-title">三步，开始定制。</h2></div><a class="source-button" href="{ADD}">添加到 Sileo <span aria-hidden="true">↗</span></a></div>
<div class="install-steps"><article class="reveal"><span class="step-number">01</span><h3>添加软件源</h3><p>在 iPhone 上点击添加；或复制下方地址，在 Sileo 的软件源中手动添加。</p><p class="en" lang="en">Open in Sileo on iPhone, or add the source URL manually.</p></article><article class="reveal" style="--d:.08s"><span class="step-number">02</span><h3>选对越狱环境</h3><p>Rootless 与 RootHide 安装包不可混用。按越狱环境选择，不按处理器型号选择。</p><p class="en" lang="en">Match your jailbreak environment. Rootless and RootHide packages are not interchangeable.</p></article><article class="reveal" style="--d:.16s"><span class="step-number">03</span><h3>调整成喜欢的样子</h3><p>安装后，进入「设置」中的插件页面配置。兼容性与版本说明请查看插件详情。</p><p class="en" lang="en">Configure the tweak in Settings. Check its detail page for compatibility and release notes.</p></article></div>
<div class="source-address reveal"><div><span>软件源地址 / Repository URL</span><p>{BASE}</p></div><button class="copy" type="button" data-copy="{BASE}">复制地址 / Copy <span aria-hidden="true">⧉</span></button></div>
</section>
<section class="source-faq" aria-labelledby="faq-title"><div class="section-heading reveal"><div><p class="section-index">03 / GOOD TO KNOW</p><h2 id="faq-title">安装前，了解这些。</h2></div></div>
<div class="faq-grid">
<details><summary>支持哪些 iOS 版本？ <span aria-hidden="true">＋</span></summary>{duo('Vela 的最低部署版本为 iOS 16；当前 Quart17 2.7.112 要求 iOS 17；Aura 面向 iOS 16–17 越狱环境。请查看各自详情页的兼容性与测试状态。','Vela has a minimum deployment target of iOS 16. Quart17 2.7.112 requires iOS 17. Aura targets jailbroken iOS 16–17. Check each detail page for compatibility and testing status.')}</details>
<details><summary>Rootless 和 RootHide 怎么选？ <span aria-hidden="true">＋</span></summary>{duo('Rootless 对应 iphoneos-arm64，RootHide 对应 iphoneos-arm64e。请按实际越狱环境选择，不要仅看处理器型号。','Use iphoneos-arm64 for Rootless and iphoneos-arm64e for RootHide. Choose by your jailbreak environment, not the processor.')}</details>
<details><summary>Quart17 自带玻璃效果吗？ <span aria-hidden="true">＋</span></summary>{duo('当前拆分版由 Aura 提供玻璃效果，Quart17 保留播放器与通知等功能。需要玻璃效果时请另行安装 Aura。','In the current split edition, Aura provides glass rendering. Install it separately alongside Quart17 for glass effects.')}</details>
<details><summary>Aura 当前是正式版吗？ <span aria-hidden="true">＋</span></summary>{duo('当前上架的 1.2.23 是预发布包，安装后真机验收尚未完成。请先阅读 Aura 详情页中的状态说明。','The listed 1.2.23 build is a prerelease. Post-install device validation is pending. Read the status notes before installing.')}</details>
<details><summary>在哪里查看完整更新记录？ <span aria-hidden="true">＋</span></summary><p>在 <a href="depictions/quart17/#changelog">Quart17 更新记录</a>、<a href="depictions/aura/#changelog">Aura 更新记录</a>与 <a href="depictions/vela/#changelog">Vela 本次更新</a>中查看中英文说明。</p><p class="en" lang="en">Each detail page includes bilingual release information.</p></details>
<details><summary>点击添加没有打开 Sileo？ <span aria-hidden="true">＋</span></summary>{duo('请在已安装 Sileo 的 iPhone 上打开本页。也可以复制软件源地址，在 Sileo 中手动添加。','Open this page on an iPhone with Sileo installed, or copy the repository URL and add it manually.')}</details>
</div></section>
</main>'''
cards=''.join(f'<article class="reveal" style="--d:{i*.06:.2f}s"><em class="fnum">0{i+1}</em><h3>{e(a)}<i lang="en">{e(b)}</i></h3>{duo(c,d)}</article>' for i,(a,b,c,d) in enumerate(features))
entries=[]
for i,row in enumerate(history):
    assert row['kind'] in ('commit','release','release-reference','local')
    source=f'<a href="{e(row["source"],quote=True)}">原始记录 / Source ↗</a>' if row['source'] else '<span>本地版本记录 / Local version record</span>'
    entries.append(f'<details {"open" if i==0 else ""}><summary><b>{e(row["version"])}</b><time>{e(row["date"])}</time><i class="chev" aria-hidden="true">＋</i></summary><div class="acc"><div class="entry">{duo(row["zh"],row["en"])}<div class="source">{source}</div></div></div></details>')
downloads=''.join(f'<a class="button ghost" href="../../debs/com.gushi.quart17_2.7.112_{arch}.deb"><span class="bl">{label} · 2.7.112<i lang="en">Download</i></span><span class="arr">↓</span></a>' for arch,label in [('iphoneos-arm64','Rootless'),('iphoneos-arm64e','RootHide')])
body=f'''<main id="main">
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
(SITE/'index.html').write_text(shell('Gushi Repo · 为你的 iPhone 添一点风格',home),encoding='utf-8',newline='\n')
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
aura_body=f'''<main id="main"><section class="dhero"><a class="back" href="../../">← Gushi Repo</a>
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

# Vela publishes only the requested current release.
vela=json.loads((ROOT/'content/vela.json').read_text(encoding='utf-8'))
vela_dir=SITE/'depictions/vela';vela_dir.mkdir(parents=True,exist_ok=True)
vela_cards=''.join(f'<article><em class="fnum">0{i+1}</em><h3>{e(a)}<i lang="en">{e(b)}</i></h3>{duo(c,d)}</article>' for i,(a,b,c,d) in enumerate(vela['features']))
vela_downloads=''.join(f'<a class="button ghost" href="../../debs/com.gushi.vela_{vela["version"]}_{arch}.deb"><span class="bl">{label} · {vela["version"]}<i lang="en">Download</i></span><span class="arr">↓</span></a>' for arch,label in [('iphoneos-arm64e','RootHide'),('iphoneos-arm64','Rootless')])
vela_body=f'''<main id="main"><section class="dhero"><a class="back" href="../../">← Gushi Repo</a>
<div class="titleline"><img class="appicon" src="../../assets/vela.png" width="104" height="104" alt="Vela 图标"><div><p class="eyebrow">EVERYDAY CONTROLS</p><h1>Vela</h1><div class="tags"><span>{e(vela['version'])}</span><span>iOS 16+</span><span>无需激活 / No activation</span></div></div></div>
<div class="lede">{duo(vela['zh'],vela['en'])}</div>{buttons(*vela_downloads)}
<nav class="section-nav" aria-label="详情导航"><a href="#features">功能 / Features</a><a href="#scope">功能范围 / Scope</a><a href="#installation">安装 / Installation</a><a href="#changelog">本次更新 / Release</a></nav></section>
<section id="features"><div class="seclabel"><b>01</b><span>FEATURES · 功能</span></div><div class="grid">{vela_cards}</div></section>
<section id="scope" class="note install"><h3>功能范围 <i lang="en">Scope</i></h3>{duo(vela['scope_zh'],vela['scope_en'])}</section>
<section id="installation" class="note install"><h3>安装与验证状态 <i lang="en">Installation and testing</i></h3>{duo(vela['install_zh'],vela['install_en'])}<div class="hint">{duo(vela['status_zh'],vela['status_en'])}</div></section>
<section id="changelog"><div class="seclabel"><b>02</b><span>RELEASE · 本次更新</span></div><h2>{e(vela['version'])} · {e(vela['date'])}</h2>{duo(vela['release_zh'],vela['release_en'])}</section></main>'''
(vela_dir/'index.html').write_text(shell('Vela · 浮动控制中心 / Floating Control Center',vela_body,'../../','depictions/vela/'),encoding='utf-8',newline='\n')
vela_zh='# Vela · '+vela['version']+'\n\n'+vela['zh']+'\n\n'+'\n\n'.join(f'### {a}\n{c}' for a,b,c,d in vela['features'])+'\n\n### 功能范围\n'+vela['scope_zh']+'\n\n### 安装\n'+vela['install_zh']+'\n\n'+vela['status_zh']
vela_en='# Vela · '+vela['version']+'\n\n'+vela['en']+'\n\n'+'\n\n'.join(f'### {b}\n{d}' for a,b,c,d in vela['features'])+'\n\n### Scope\n'+vela['scope_en']+'\n\n### Installation\n'+vela['install_en']+'\n\n'+vela['status_en']
vela_log=f"## {vela['version']} · {vela['date']}\n\n{vela['release_zh']}\n\n{vela['release_en']}"
(vela_dir/'sileo.json').write_text(json.dumps({'class':'DepictionTabView','minVersion':'0.3','tintColor':'#2859D8','tabs':[tab('中文',vela_zh),tab('English',vela_en),tab('更新 / History',vela_log)]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Built Vela 0.4.19 bilingual scope, installation, current release and Sileo depiction')
