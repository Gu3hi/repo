# Gushi Repo

越狱源地址：**https://gu3hi.github.io/repo/**

当前上架 Quart17 2.7.112：Rootless（iphoneos-arm64）和 RootHide（iphoneos-arm64e）。不包含插件源码。

源头像：`docs/CydiaIcon.png`（GitHub 账号头像）；Quart17 图标：`docs/assets/quart17.png`（项目现有图标）。
网站提供 `sileo://source/https://gu3hi.github.io/repo/` 添加按钮及手动添加地址。
Quart17 的 HTML 介绍和原生 Sileo 详情均由 `build_site.py` 生成；索引中的 Icon、Depiction 和 SileoDepiction 指向对应资源。

中英文历史数据保存在 `content/quart17-history.json`，覆盖已找到的 28 条版本记录；每条注明发布/提交来源或本地记录，未知改动明确标记。旧版本的玻璃功能不作为当前版本能力宣传。
编辑历史或页面生成逻辑后依次运行 `python build_site.py`、`python update_repo.py`、`python verify.py` 再提交。安装包本体不因详情更新而改变。

GitHub Pages 从 `main` 分支的 `docs/` 发布。该目录包含平面 APT 源的
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
