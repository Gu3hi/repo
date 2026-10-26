# Gushi Repo

越狱源地址：**https://gu3hi.github.io/repo/**

当前上架 Vela 0.4.19、Quart17 2.7.112 与 Aura 1.2.23，均提供 Rootless / RootHide 安装包。Vela 仅发布本次 0.4.19 双包，配色、主题与基础面板直接使用，无需激活；完整功能范围见 `content/vela.json`。

Quart17 2.7.112：Rootless（iphoneos-arm64）和 RootHide（iphoneos-arm64e）。不包含插件源码。

源头像：`docs/CydiaIcon.png`（GitHub 账号头像）；Quart17 图标：`docs/assets/quart17.png`（项目现有图标）。
网站提供 `sileo://source/https://gu3hi.github.io/repo/` 添加按钮及手动添加地址。
Quart17 的 HTML 介绍和原生 Sileo 详情均由 `build_site.py` 生成；索引中的 Icon、Depiction 和 SileoDepiction 指向对应资源。

中英文历史数据保存在 `content/quart17-history.json`，覆盖已找到的 29 条版本记录；每条注明发布/提交来源或本地记录，未知改动明确标记。旧版本的玻璃功能不作为当前版本能力宣传。
编辑历史或页面生成逻辑后依次运行 `python build_site.py`、`python update_repo.py`、`python verify.py` 再提交。安装包本体不因详情更新而改变。

GitHub Pages 通过 `.github/workflows/pages.yml` 从 `main` 分支的 `docs/` 发布。推送、手动触发及每小时定时任务均会刷新下载快照并部署；GitHub 调度可能延迟。该目录包含平面 APT 源的
`Release`、`Packages`、`Packages.gz`、`Packages.bz2` 和介绍页面。

手动添加上述地址即可。APT sources.list 的对应条目为：

```text
deb https://gu3hi.github.io/repo/ ./
```

当前 Release 未做 GPG 签名；强制签名验证的客户端需要另行配置签名信任。
不得把私钥、访问令牌或其他项目的私有源码上传到此仓库。

本地校验：`python verify.py`。部署后校验：`python verify.py https://gu3hi.github.io/repo/`。
校验会比较线上文件和本地文件、压缩索引与原始索引、Release 中的大小及校验和。
校验还检查 Sileo 必需的 Components/Architectures 字段、DEB 内版本/架构、包的大小及哈希、是否有遗漏或重复索引。

以后上架时，先明确发行版本及 rootless/RootHide 架构，将授权发布的 DEB 放入 `docs/debs/`，运行 `python update_repo.py` 和 `python verify.py`，提交并推送。发布后运行线上校验。
索引脚本只读取安装包元数据，不执行包内脚本，也不重新打包或安装插件。

2026-10-24：修复 Release 缺失 Components 导致 Sileo 报 “Could not parse release file” 的问题，并发布 Quart17 两种架构的现有 2.7.103 安装包。

2026-10-26：发布 Quart17 2.7.112 RootHide/rootless 双包，并更新中英文介绍与历史。本版最低系统为 iOS 17；RootHide 经用户真机测试确认，rootless 已构建验包但尚未真机测试。

部署配置参考：[GitHub Pages API](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site)。

## 网站首页

首页由 `build_site.py` 生成，独立样式位于 `docs/assets/home.css`。实机视图切换使用仓库中现有的两张截图；不改变安装包与原生 Sileo 描述。Geist 字体随站点本地提供，许可证见 `docs/assets/Geist-OFL.txt`。

本地预览：python -m http.server 8766 --bind 127.0.0.1 --directory docs，打开 http://127.0.0.1:8766/。修改后运行 python build_site.py 和 python verify.py。

2026-10-26：新增 Vela 0.4.19 RootHide/rootless 双包。中英文介绍、功能范围、安装方式、验证状态与本次更新由 `content/vela.json` 生成，同步网站首页和原生 Sileo 描述。未追加 Vela 历史版本安装包。

## 下载次数

首页显示各插件已上架包的合计下载次数，详情页按版本与 RootHide / Rootless 展开。计数由 GitHub Actions 使用内置令牌读取本仓库 `packages` Release 资产的 GitHub `download_count`，生成 `docs/assets/downloads.json` 同源快照，约每小时刷新；详情页显示统计时间，自 2026-10-26 启用，不追补此前的下载。网页按钮和 APT `Filename` 均指向 Release 资产，因此刷新源后的 Sileo 下载也走同一地址。

统计的是 Release 下载次数，包含重复下载、升级和校验下载，不代表安装成功、独立设备或活跃用户。旧的 Pages 直链继续可用，但不纳入新计数。网页不直接请求 GitHub 公共 API，避免访客共享配额导致限流。快照无法读取时显示“暂不可用”，不影响下载安装；生成失败时不覆盖上一次已部署页面，更新时间保留供判断新鲜度。页面不包含 GitHub 令牌，也不给插件加入安装上报。

以后发布新包时，先将同名 DEB 上传到本仓库 `packages` Release，确认资产与 `docs/debs/` 原件的 SHA256 一致，再运行 `python build_site.py`、`python update_repo.py`、`python refresh_downloads.py`（使用本机已登录的 gh）、`python verify.py`。推送 Pages 后运行 `python verify.py https://gu3hi.github.io/repo/`。保持已发布资产不变；删除再上传会重置该资产计数，修订包应使用新版本。计数逻辑自检：`node --test tests/downloads.test.mjs`。


## Vela 宣传片

首页 Vela 卡片、Vela HTML 安装详情及 Sileo 中英文原生详情均包含最新 12 秒普通 / 玻璃真机演示。原成片 H264/AAC 保留，未重画或重新压缩；网页使用 `preload="none"`、封面及点击播放，不自动加载全片或播放声音。影片是外观演示，功能范围与兼容性以当前文字说明为准。

资源：`docs/assets/vela-promo.mp4` 与 `docs/assets/vela-promo-poster.jpg`。Sileo 使用原生 `DepictionVideoView`，显示播放控件且不自动播放；网页另外提供单独播放链接。生成和校验命令与上文一致。
