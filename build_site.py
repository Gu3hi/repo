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
<meta name="color-scheme" content="dark light"><meta name="description" content="Gushi Repo · Quart17 · Lock Screen player and notifications">
<title>{e(title)}</title><link rel="icon" href="{relative}CydiaIcon.png"><link rel="stylesheet" href="{relative}assets/style.css"></head>
<body><div class="wrap"><header><a class="brand" href="{relative or './'}"><img src="{relative}CydiaIcon.png" width="36" height="36" alt="Gushi 头像">Gushi Repo</a><a href="https://github.com/Gu3hi/repo">GitHub ↗</a></header>
{body}<footer><span>Gushi Repo · Put_Story</span><a href="https://github.com/Gu3hi/Quart17">Quart17 on GitHub ↗</a></footer></div></body></html>'''
buttons=f'<div class="actions"><a class="button primary" href="{ADD}">在 Sileo 中添加 <span lang="en">Add to Sileo ↗</span></a><a class="button" href="{BASE}">软件源地址 / Repository URL</a></div>'
home=f'''<main><section class="hero"><div class="eyebrow">GUSHI · JAILBREAK REPOSITORY</div><h1>让锁屏更像你。<span lang="en">Make your Lock Screen yours.</span></h1>
{duo('播放器、通知和细节，从这里开始。','A home for player, notification and interface tweaks.')}{buttons}
<div class="address"><span>源地址 / Source URL</span><code>{BASE}</code></div><p class="hint">请在安装了 Sileo 的 iPhone 上打开。若未唤起 App，可在软件源页面手动添加上方地址。<br><span lang="en">Open on an iPhone with Sileo installed, or add the URL manually in Sources.</span></p></section>
<section class="package"><img class="appicon" src="assets/quart17.png" width="88" height="88" alt="Quart17 图标"><div><div class="eyebrow">AVAILABLE NOW · 2.7.103</div><h2>Quart17</h2>{duo(zh,en)}<div class="tags"><span>Rootless</span><span>RootHide</span><span>中文 / English</span></div><a class="textlink" href="depictions/quart17/">功能介绍与完整更新记录 / Features & changelog →</a></div></section>
<section class="note">仅发布匹配越狱环境的安装包；不要仅凭设备处理器型号选择架构。<br><span lang="en">Choose the package for your jailbreak environment, not just your device’s processor.</span></section></main>'''
(SITE/'index.html').write_text(shell('Gushi Repo · Quart17',home),encoding='utf-8',newline='\n')
cards=''.join(f'<article><h3>{e(a)}</h3><div class="en" lang="en">{e(b)}</div>{duo(c,d)}</article>' for a,b,c,d in features)
entries=[]
for i,row in enumerate(history):
    assert row['kind'] in ('commit','release','release-reference','local')
    source=f'<a href="{e(row["source"],quote=True)}">原始记录 / Source ↗</a>' if row['source'] else '<span>本地版本记录 / Local version record</span>'
    entries.append(f'<details {"open" if i==0 else ""}><summary><strong>{e(row["version"])}</strong><time>{e(row["date"])}</time></summary><div class="entry">{duo(row["zh"],row["en"])}<div class="source">{source}</div></div></details>')
downloads=''.join(f'<a class="button" href="../../debs/com.gushi.quart17_2.7.103_{arch}.deb">{label} · 2.7.103 ↓</a>' for arch,label in [('iphoneos-arm64','Rootless'),('iphoneos-arm64e','RootHide')])
body=f'''<main><section class="detailhero"><a class="back" href="../../">← Gushi Repo</a><div class="titleline"><img class="appicon" src="../../assets/quart17.png" width="96" height="96" alt="Quart17 图标"><div><div class="eyebrow">LOCK SCREEN, REIMAGINED</div><h1>Quart17</h1><div class="tags"><span>2.7.103</span><span>Put_Story</span></div></div></div>{duo(zh,en)}{buttons}</section>
<section><h2>功能 / Features</h2><div class="grid">{cards}</div></section>
<section class="note"><h3>安装说明 / Installation</h3>{duo('面向 iOS 16–17 越狱环境；2.7.103 包含 iOS 16 播放器识别兼容调整。Rootless 与 RootHide 安装包不可混用。安装后进入「设置 → Quart17」配置。','For jailbroken iOS 16–17 devices. Version 2.7.103 includes an iOS 16 player-detection compatibility adjustment. Use the package matching Rootless or RootHide, then configure Settings → Quart17.')}
<div class="actions">{downloads}</div><p class="hint">玻璃效果可另装 <a href="https://github.com/Gu3hi/Aura-Releases/releases">Aura</a>。旧版历史中的玻璃功能不代表当前 Quart17 内置这些功能。<br><span lang="en">Install Aura separately for glass effects. Historical glass features listed below are not bundled with the current Quart17 edition.</span></p></section>
<section id="changelog"><div class="sectionhead"><h2>历史更新 <span lang="en">Changelog</span></h2><span>{len(history)} 条记录 / entries</span></div><p class="hint">按 GitHub 发布说明、版本提交及本地构建记录整理；日期优先采用发布时间。未记录的改动不作推测。<br><span lang="en">Based on release notes, version commits and local build records; release dates are preferred when available. Undocumented changes are not inferred.</span></p>{''.join(entries)}</section></main>'''
detail=SITE/'depictions/quart17';detail.mkdir(parents=True,exist_ok=True)
(detail/'index.html').write_text(shell('Quart17 · 介绍与历史更新 / Features & Changelog',body,'../../'),encoding='utf-8',newline='\n')
def markdown(text):return {'class':'DepictionMarkdownView','markdown':text,'useRawFormat':False}
def tab(name,text):return {'class':'DepictionStackView','tabname':name,'views':[markdown(text)]}
zh_intro=f'# Quart17 · 2.7.103\n\n{zh}\n\n'+'\n\n'.join(f'### {a}\n{c}' for a,b,c,d in features)+'\n\n### 安装\niOS 16–17 越狱环境。请按环境选择 Rootless / RootHide。安装后前往「设置 → Quart17」。玻璃效果由独立的 Aura 提供。'
en_intro=f'# Quart17 · 2.7.103\n\n{en}\n\n'+'\n\n'.join(f'### {b}\n{d}' for a,b,c,d in features)+'\n\n### Installation\nFor jailbroken iOS 16–17. Choose Rootless or RootHide for your environment, then configure Settings → Quart17. Glass rendering is provided separately by Aura.'
log='Historical glass features later moved to Aura. / 历史玻璃功能后续已迁移至 Aura。\n\n'+'\n\n'.join(f'## {r["version"]} · {r["date"]}\n\n{r["zh"]}\n\n{r["en"]}\n\n'+(f'[原始记录 / Source]({r["source"]})' if r['source'] else '本地版本记录 / Local version record') for r in history)
depiction={'class':'DepictionTabView','minVersion':'0.3','tintColor':'#168D82','tabs':[tab('中文',zh_intro),tab('English',en_intro),tab('更新 / History',log)]}
(detail/'sileo.json').write_text(json.dumps(depiction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(f'Built bilingual pages and Sileo depiction with {len(history)} history entries')
