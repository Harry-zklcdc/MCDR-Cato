# MCDR-Cato

## MCDR 插件

使服务器启动时, 自动使用 `cato` 进行端口映射, 并支持生成 `HMCL` 联机码

Cato 的介绍可以看[这里](https://noin.cn/71.html)

# 简单介绍

>你是否在为开服而烦恼?
>
>你是否为服务器不能端口映射而苦恼?
>
>你是否为服务器使用流量转发映射软件而为延迟感到担忧?
>
>来吧, Cato 欢迎你的使用!
>
>Cato, 全新一代 P2P 传输工具
>
>让你的延迟急速降低
>
>并配合 HMCL 使用, 让你无感 P2P 连接

# 特性:

* Cato 官方支持
* 无感 P2P 连接
* HMCl 多人游戏支持
* Cato 崩溃/临时 ID 到期自动重启
* API 接口获取 Cato 连接 ID、HMCL 联机码
* Cato Token 动态更换
* 游戏内获取 Cato 连接 ID、HMCL 联机码

# TODO

* PCL2 联机支持 (坐等龙猫更新 Cato 版 PCL(在催了.jpg))
* BakaXL 联机支持 (坐等 TT 支持联机(在催了.jpg))

# 食用方法

1. 下载插件后, 放至 [`MCDR`](https://github.com/Fallen-Breath/MCDReforged) 的 `plugins` 文件夹

2. 下载适合你系统版本的 Cato 本体, 放至 [`MCDR`](https://github.com/Fallen-Breath/MCDReforged) 的 `plugins` 文件夹, 下载地址在[这里](https://noin.cn/71.html)

3. 启动服务器

### OK, 你已完成插件安装

## API 接口

| API 接口             | 功能              |
| -------------------- | ----------------- |
| http://ip:26666/     | 查看 Cato 状态    |
| http://ip:26666/id   | 查看 Cato 连接 ID |
| http://ip:26666/code | 查看 HMCL 联机码  |

## 指令

| 指令                 | 功能                                                         |
| -------------------- | ------------------------------------------------------------ |
| !!cato id            | 查看 Cato 连接 ID                                            |
| !!cato code          | 查看 HMCL 联机码                                             |
| !!cato token <token> | <token> 可以填静态 Token（需要到[这里](https://noin.cn/)申请）, 也可以填 `new`, 即为临时 ID |

### ※PS: 临时 ID 有效期为三个小时, 三个小时需获取新的临时 ID, 本插件支持自动重启 Cato 以获取新的临时 ID

# 配置文件说明

### 配置文件位置: config/cato/config.json

| 配置项 | 注释                                                       |
| ------ | ---------------------------------------------------------- |
| token  | Cato 静态 Token, 可填 `new`/不填 获取临时 ID, 默认值`None` |
| name   | HMCl 中房间名, 默认值为 `A Minecraft Server`               |
| port   | 服务器的端口, 默认值为 `25565`                             |

