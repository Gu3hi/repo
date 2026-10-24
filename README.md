# Gushi Repo

越狱源地址：**https://gu3hi.github.io/repo/**

当前上架 Quart17 2.7.103：Rootless（iphoneos-arm64）和 RootHide（iphoneos-arm64e）。不包含插件源码。

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

部署配置参考：[GitHub Pages API](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site)。
