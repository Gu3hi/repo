# Gushi Repo

越狱源地址：**https://gu3hi.github.io/repo/**

当前为有意创建的空源：没有安装包，也没有插件源码。

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
本版本还会断言索引为空且没有 DEB，防止意外上架。

以后上架时，应先明确包的发行版本及 rootless/RootHide 架构，再生成索引和 Release 校验和。
当前操作不构建、发布或安装任何插件。

部署配置参考：[GitHub Pages API](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site)。
