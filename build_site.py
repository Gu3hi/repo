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
zh='Quart17 为越狱设备提供可定制的锁屏音乐播放器、专辑封面、通知排版与缩放，以及下拉清理手势。'
en='Quart17 brings a customizable Lock Screen music player, album artwork, notification layouts and scaling, and pull-to-clear gestures to jailbroken devices.'
features=[('锁屏音乐播放器','Lock Screen player','播放控制、封面位置与缩放，支持封面进度交互。','Playback controls, artwork positioning and scaling, with artwork-based seeking.'),('通知排版与缩放','Notification layout','调整通知卡片尺寸，让锁屏列表更清晰。','Adjust notification card sizes for a cleaner Lock Screen list.'),('下拉清理手势','Pull to clear','通过手势清理通知，并在设置中调整选项。','Clear notifications with a gesture and customize behavior in Settings.'),('配合 Aura','Works with Aura','当前拆分版的玻璃效果由 Aura 提供；Quart17 保留播放器与通知功能。','Aura provides glass rendering in the current split edition; Quart17 handles player and notification features.')]
def duo(a,b):return f'<p>{e(a)}</p><p class="en" lang="en">{e(b)}</p>'
def shell(title,body,relative=''):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light"><meta name="theme-color" content="#05080b"><meta name="description" content="Gushi Repo · Jailbreak tweaks for iOS · 中文 / English">
<title>{e(title)}</title><link rel="icon" href="{relative}CydiaIcon.png"><link rel="stylesheet" href="{relative}assets/style.css"><script src="{relative}assets/site.js" defer></script></head>
<body><header class="top" id="top"><div class="bar"><a class="brand" href="{relative or './'}"><img src="{relative}CydiaIcon.png" width="34" height="34" alt="Gushi 头像"><span>Gushi<b>Repo</b></span></a><nav><a class="navlink" href="https://github.com/Gu3hi/repo" target="_blank" rel="noopener">GitHub ↗</a><a class="navcta" href="{ADD}">Sileo<i lang="en">Add</i></a></nav></div></header>
{body}
<footer class="foot"><div class="bigword" aria-hidden="true">GUSHI REPO</div><div class="footline"><span>Gushi Repo · Put_Story</span><span class="footnote" lang="en">Crafted tweaks for iOS</span><a href="https://github.com/Gu3hi/Quart17" target="_blank" rel="noopener">Quart17 on GitHub ↗</a></div></footer></body></html>'''
def buttons(*extra):
    return f'<div class="actions"><a class="button primary" href="{ADD}"><span class="bl">在 Sileo 中添加<i lang="en">Add to Sileo</i></span><span class="arr">→</span></a>{"".join(extra)}</div>'
copybtn=f'<button class="button ghost copy" type="button" data-copy="{BASE}">复制源地址<i lang="en">Copy URL</i></button>'
def device(relative):
    return f'''<div class="heroart reveal" style="--d:.22s" aria-hidden="true"><div class="glow"></div><div class="float"><div class="device"><div class="screen">
<div class="island"></div>
<div class="dt"><span class="dtime">9:41</span><span class="ddate" lang="en">Saturday, October 24</span></div>
<div class="player"><div class="art"><img src="{relative}assets/quart17.png" alt=""></div><div class="pmeta"><strong>Quart17</strong><span lang="en">Now Playing · 正在播放</span><div class="pb"><i></i></div></div><div class="pctl"><span>⏮</span><span class="pplay">⏯</span><span>⏭</span></div></div>
<div class="notif"><img src="{relative}assets/quart17.png" alt=""><div><strong>Quart17</strong><span>通知排版已更新 · <i lang="en">Layout updated</i></span></div><em lang="en">now</em></div>
</div></div></div></div>'''
marquee=''.join(f'<span>{s}</span><b>·</b>' for s in ['GUSHI REPO','JAILBREAK TWEAKS','让系统更像你 · MAKE IOS YOURS','QUART17 2.7.103','ROOTLESS / ROOTHIDE','中文 · ENGLISH'])
home=f'''<main>
<section class="hero">
<div class="herotext">
<p class="eyebrow reveal">GUSHI · JAILBREAK REPOSITORY</p>
<h1 class="reveal" style="--d:.06s">让系统更像你。<span lang="en">Make iOS yours.</span></h1>
<div class="lede reveal" style="--d:.12s">{duo('播放器、通知、界面细节——精选插件陆续上架。','Players, notifications and interface tweaks — more to come.')}</div>
<div class="actions reveal" style="--d:.18s">{''}
<a class="button primary" href="{ADD}"><span class="bl">在 Sileo 中添加<i lang="en">Add to Sileo</i></span><span class="arr">→</span></a>{copybtn}</div>
<div class="address reveal" style="--d:.24s"><code>{BASE}</code></div>
<p class="hint reveal" style="--d:.3s">请在安装了 Sileo 的 iPhone 上打开。若未唤起 App，可在软件源页面手动添加上方地址。<br><span lang="en">Open on an iPhone with Sileo installed, or add the URL manually in Sources.</span></p>
</div>
{device('')}
</section>
<div class="marquee" aria-hidden="true"><div class="mtrack"><div class="mg">{marquee}</div><div class="mg">{marquee}</div></div></div>
<section class="featured">
<div class="seclabel reveal"><b>01</b><span>FEATURED PACKAGE · 精选插件</span></div>
<article class="package reveal" style="--d:.08s"><img class="appicon" src="assets/quart17.png" width="96" height="96" alt="Quart17 图标"><div>
<div class="ptag">AVAILABLE · 2.7.103</div><h2>Quart17</h2>{duo(zh,en)}
<div class="tags"><span>Rootless</span><span>RootHide</span><span>中文 / English</span></div>
<a class="textlink" href="depictions/quart17/">功能介绍与完整更新记录 / Features &amp; changelog <i class="ta">→</i></a>
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
downloads=''.join(f'<a class="button ghost" href="../../debs/com.gushi.quart17_2.7.103_{arch}.deb"><span class="bl">{label} · 2.7.103<i lang="en">Download</i></span><span class="arr">↓</span></a>' for arch,label in [('iphoneos-arm64','Rootless'),('iphoneos-arm64e','RootHide')])
body=f'''<main>
<section class="dhero">
<a class="back" href="../../">← Gushi Repo</a>
<div class="titleline reveal"><img class="appicon" src="../../assets/quart17.png" width="104" height="104" alt="Quart17 图标"><div><p class="eyebrow">LOCK SCREEN, REIMAGINED</p><h1>Quart17</h1><div class="tags"><span>2.7.103</span><span>Put_Story</span><span>iOS 16–17</span></div></div></div>
<div class="lede reveal" style="--d:.08s">{duo(zh,en)}</div>
<div class="reveal" style="--d:.14s">{buttons(*downloads)}</div>
</section>
<section><div class="seclabel reveal"><b>01</b><span>FEATURES · 功能</span></div><div class="grid">{cards}</div></section>
<section class="note install reveal"><h3>安装说明 <i lang="en">Installation</i></h3>{duo('面向 iOS 16–17 越狱环境；2.7.103 包含 iOS 16 播放器识别兼容调整。Rootless 与 RootHide 安装包不可混用。安装后进入「设置 → Quart17」配置。','For jailbroken iOS 16–17 devices. Version 2.7.103 includes an iOS 16 player-detection compatibility adjustment. Use the package matching Rootless or RootHide, then configure Settings → Quart17.')}<p class="hint">玻璃效果可另装 <a href="https://github.com/Gu3hi/Aura-Releases/releases" target="_blank" rel="noopener">Aura</a>。旧版历史中的玻璃功能不代表当前 Quart17 内置这些功能。<br><span lang="en">Install Aura separately for glass effects. Historical glass features listed below are not bundled with the current Quart17 edition.</span></p></section>
<section id="changelog"><div class="seclabel reveal"><b>02</b><span>CHANGELOG · 历史更新</span></div>
<p class="hint reveal" style="--d:.06s">按 GitHub 发布说明、版本提交及本地构建记录整理；日期优先采用发布时间。未记录的改动不作推测。<br><span lang="en">Based on release notes, version commits and local build records; release dates are preferred when available. Undocumented changes are not inferred.</span></p>
<div class="count reveal" style="--d:.1s"><b>{len(history)}</b><span>条记录 / <i lang="en">entries</i></span></div>
{''.join(entries)}</section>
</main>'''
detail=SITE/'depictions/quart17';detail.mkdir(parents=True,exist_ok=True)
(SITE/'index.html').write_text(shell('Gushi Repo · Quart17',home),encoding='utf-8',newline='\n')
(detail/'index.html').write_text(shell('Quart17 · 介绍与历史更新 / Features & Changelog',body,'../../'),encoding='utf-8',newline='\n')
def markdown(text):return {'class':'DepictionMarkdownView','markdown':text,'useRawFormat':False}
def tab(name,text):return {'class':'DepictionStackView','tabname':name,'views':[markdown(text)]}
zh_intro=f'# Quart17 · 2.7.103\n\n{zh}\n\n'+'\n\n'.join(f'### {a}\n{c}' for a,b,c,d in features)+'\n\n### 安装\niOS 16–17 越狱环境。请按环境选择 Rootless / RootHide。安装后前往「设置 → Quart17」。玻璃效果由独立的 Aura 提供。'
en_intro=f'# Quart17 · 2.7.103\n\n{en}\n\n'+'\n\n'.join(f'### {b}\n{d}' for a,b,c,d in features)+'\n\n### Installation\nFor jailbroken iOS 16–17. Choose Rootless or RootHide for your environment, then configure Settings → Quart17. Glass rendering is provided separately by Aura.'
log='Historical glass features later moved to Aura. / 历史玻璃功能后续已迁移至 Aura。\n\n'+'\n\n'.join(f'## {r["version"]} · {r["date"]}\n\n{r["zh"]}\n\n{r["en"]}\n\n'+(f'[原始记录 / Source]({r["source"]})' if r['source'] else '本地版本记录 / Local version record') for r in history)
depiction={'class':'DepictionTabView','minVersion':'0.3','tintColor':'#7FF0D4','tabs':[tab('中文',zh_intro),tab('English',en_intro),tab('更新 / History',log)]}
(detail/'sileo.json').write_text(json.dumps(depiction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(f'Built bilingual pages and Sileo depiction with {len(history)} history entries')
