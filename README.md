# tvbox-cfg

自用 TVBox / 影视仓 / FongMi 配置仓库。内容采集自 GitHub 上 star 排名靠前的 TVBox 相关项目，
经过**实探测活**后整理成可直接填写的配置地址，并提供多仓聚合配置。

> 采集与整理时间：**2026-10-19**（点播源于 2026-09-30 整理；直播源于 2026-10-19 重新核对上游、实测播放协议与可达性并刷新。上游接口随时可能失效，建议定期跑一次探活脚本）

---

## 一、直接可用的配置地址

### 多仓聚合（推荐，一次加载全部点播源）

| 用途 | 地址 |
| --- | --- |
| jsDelivr CDN 版（国内直连推荐） | `https://cdn.jsdelivr.net/gh/ouyushan/tvbox-cfg@main/config/multi.json` |
| jsDelivr Fastly 版 | `https://fastly.jsdelivr.net/gh/ouyushan/tvbox-cfg@main/config/multi.json` |
| 裸地址版 | `https://raw.githubusercontent.com/ouyushan/tvbox-cfg/main/config/multi.json` |
| 裸地址 + gh-proxy | `https://gh-proxy.com/https://raw.githubusercontent.com/ouyushan/tvbox-cfg/main/config/multi.json` |

### 直播源配置

| 用途 | 地址 |
| --- | --- |
| jsDelivr CDN 版 | `https://cdn.jsdelivr.net/gh/ouyushan/tvbox-cfg@main/config/live.json` |
| 裸地址版 | `https://raw.githubusercontent.com/ouyushan/tvbox-cfg/main/config/live.json` |

### 用法

1. 打开 TVBox / 影视仓 / FongMi 等客户端 → **设置** → **配置地址**
2. 粘贴上面任意一个 `multi.json` 地址 → 保存，等待加载完成
3. 直播源单独在 **直播** 入口或再填一条 `live.json`（部分客户端支持在配置里同时带 lives）

> jsDelivr 有缓存（约 12 小时），改完仓库想立刻生效，加缓存刷新：
> <https://purge.jsdelivr.net/gh/ouyushan/tvbox-cfg@main/config/multi.json>

---

## 二、目录结构

```
tvbox-cfg/
├── config/                 # 生成产物：TVBox 可直接填写的配置
│   ├── multi.json          # 多仓聚合（jsDelivr 镜像版）
│   ├── multi-raw.json      # 多仓聚合（裸地址版）
│   └── live.json           # 直播源 lives 配置
├── sources/                # 源数据（单一事实来源，手改这里）
│   ├── vod.json            # 点播配置源清单
│   ├── live.json           # 直播源清单
│   ├── mirrors.json        # GitHub 加速镜像
│   └── upstream.json       # 上游仓库 star 排名
├── scripts/
│   ├── build.py            # sources → config 生成
│   └── check.py            # 批量探活，回写 status
├── docs/
│   └── STATUS.md           # 探活报告（CI 生成）
└── .github/workflows/
    └── check.yml           # 每 6 小时自动探活
```

改完 `sources/*.json` 后执行：

```bash
python scripts/build.py      # 重新生成 config/
python scripts/check.py --status   # 探活 + 生成 docs/STATUS.md
```

---

## 三、点播配置源清单（已探活）

| # | 名称 | 上游仓库 | 状态 |
| --- | --- | --- | --- |
| 1 | 饭太硬(fty) | [qist/tvbox](https://github.com/qist/tvbox) | ✅ |
| 2 | 饭太硬(极速 jsm) | [qist/tvbox](https://github.com/qist/tvbox) | ✅ |
| 3 | 潇洒 | [qist/tvbox](https://github.com/qist/tvbox) | ✅ |
| 4 | OK影视 | [2hacc/TVBox](https://github.com/2hacc/TVBox) | ✅ |
| 5 | 高天流云 | [gaotianliuyun/gao](https://github.com/gaotianliuyun/gao) | ✅ |
| 6 | 歧人知道(tvbox) | [qirenzhidao/tvbox18](https://github.com/qirenzhidao/tvbox18) | ✅ |
| 7 | 歧人知道(fan) | [qirenzhidao/tvbox18](https://github.com/qirenzhidao/tvbox18) | ✅ |
| 8 | 歧人知道(fongmi) | [qirenzhidao/tvbox18](https://github.com/qirenzhidao/tvbox18) | ✅ |
| 9 | 香雅情 XYQ | [xyq254245/xyqonlinerule](https://github.com/xyq254245/xyqonlinerule) | ✅ |
| 10 | 小帅 XC | [yoursmile66/TVBox](https://github.com/yoursmile66/TVBox) | ✅ |
| 11 | 月光宝盒 | [guot55/yg](https://github.com/guot55/yg) | ✅ |
| 12 | DXAW | [dxawi/0](https://github.com/dxawi/0) | ✅ |
| 13 | 猫影视 | [maoystv/6](https://github.com/maoystv/6) | ✅ |
| 14 | Txtv | [txtvv/txtv](https://github.com/txtvv/txtv) | ✅ |
| 15 | 一木多线路 | [xianyuyimu/TVBOX-](https://github.com/xianyuyimu/TVBOX-) | ✅ |
| 16 | 肥猫 frjbox | [kunkka1986/my.img](https://github.com/kunkka1986/my.img) | ✅ |
| 17 | hackyjso jzy | [hackyjso/box](https://github.com/hackyjso/box) | ✅ |
| 18 | noimank 多仓 | [noimank/tvbox](https://github.com/noimank/tvbox) | ✅ |
| 19 | CatVod 官方 Spider | [FongMi/CatVodSpider](https://github.com/FongMi/CatVodSpider) | ✅ |

完整地址（含镜像）见 [`sources/vod.json`](sources/vod.json)。

## 四、直播源清单

TVBox **支持多直播源**：`config/live.json` 的 `lives` 数组里每个条目就是一个独立直播源，
在客户端的直播页通过「换源 / 切源」菜单切换，多个源是叠加关系，不是互斥的。

| 名称 | 上游仓库 | 格式 | 适用网络 | 状态 |
| --- | --- | --- | --- | --- |
| iptv-api 聚合 | [Guovin/iptv-api](https://github.com/Guovin/iptv-api) | m3u | 通用（约 230 分组 / 1600+ 频道，含各省级频道） | ✅ |
| iptv-api 聚合(TXT) | [Guovin/iptv-api](https://github.com/Guovin/iptv-api) | txt | 通用（同上，平铺无分组） | ✅ |
| YueChan Live(GNTV) | [YueChan/Live](https://github.com/YueChan/Live) | m3u | 仅台湾网络（CloudFront 地域封锁，大陆 403） | ⚠️ |
| ngo5 IPTV(IPv4) | [ngo5/IPTV](https://github.com/ngo5/IPTV) | m3u | 仅中国移动宽带（PLTV 内网流） | ⚠️ |

### 使用方法（重要）

1. 打开客户端 → **设置** → **配置地址**，填
   `https://cdn.jsdelivr.net/gh/ouyushan/tvbox-cfg@main/config/live.json`
   （`live.json` 本身就是一份合法配置，只含 `lives`，可直接当配置地址填）
2. 进入 **直播** 页：
   - **切换直播源**：用顶部菜单 / 遥控器「源」按钮在 4 个源之间切换；
   - **切换频道分组**：频道列表顶部有分组下拉（或左右方向键），
     Guovin 源有约 230 个分组（央视频道、卫视频道、浙江/河南/江苏等各省级频道）。
3. ⚠️ **Guovin 源的第一个分组「🕘️更新时间」是上游自带的伪频道**
   （只有一条时间戳、无法播放），这不是故障——**切换到「📺央视频道」或其他分组即可正常收看**。

> 注1：原 `YueChan Live(Global)` 引用的 `Global.m3u` 已被上游删除，2026-10-16 改用 `GNTV.m3u` 替代。
> 注2：原 `YueChan Live(IPTV)` 已于 2026-10-19 移除——实测该列表 96/96 个频道全是 `rtp://` 组播地址，
> TVBox 系 App 播放器不支持 rtp 组播，仅在支持 IGMP 的路由器内网可用，对 App 用户等同失效。

## 五、上游仓库 star 排名（完整版）

见 [`sources/upstream.json`](sources/upstream.json)，收录 24 个仓库，覆盖：
直播源采集（Guovin/iptv-api、joevess/IPTV、HerbertHe/iptv-sources）、
点播配置（qist/tvbox、gaotianliuyun/gao、2hacc/TVBox、noimank/tvbox）、
客户端（j4Uq/TVBoxOSC、liu673cn/bug、kknifer7/FreeBox）、
爬虫框架（FongMi/CatVodSpider）、资源索引（laoma2053/awesome-zhuiju-free、Zhou-Li-Bin/Tvbox-QingNing）。

---

## 六、免责声明

- 本仓库**仅收集整理网络上公开的配置地址与开源仓库索引**，不存储、不分发任何影视内容，
  也不提供任何解析、破解或绕过版权保护的能力。
- 所有配置内容的所有权归各自上游仓库作者所有，请遵守上游项目的许可与使用条款。
- 请仅用于**个人学习与技术交流**，观看影视内容请使用合法授权渠道；因使用第三方接口
  产生的任何版权或法律风险由使用者自行承担。
- 若你是上游仓库作者且不希望被收录，请提 Issue，会在 24 小时内移除。
