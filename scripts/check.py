#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量探活 sources/*.json 里的所有地址，回写 status / last_checked，并生成 docs/STATUS.md。

用法：
  python scripts/check.py            # 只探活并更新 json
  python scripts/check.py --status   # 额外生成 docs/STATUS.md

退出码恒为 0，方便放进 CI 定时任务。
"""

import concurrent.futures
import datetime
import json
import os
import ssl
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "sources")
DOCS = os.path.join(ROOT, "docs")

ssl._create_default_https_context = ssl._create_unverified_context
UA = {"User-Agent": "Mozilla/5.0 (compatible; tvbox-cfg-healthcheck)"}


RETRY = 3
CONCURRENCY = 6


def _once(url):
    req = urllib.request.Request(url, headers=UA)
    resp = urllib.request.urlopen(req, timeout=30)
    body = resp.read()
    return "ok", "%d / %d B" % (resp.status, len(body))


def probe(url):
    """探活，失败重试 RETRY 次（线性退避），避免并发过高导致的误判。"""
    last = ""
    for i in range(RETRY):
        try:
            return _once(url)
        except Exception as e:  # noqa: BLE001
            last = str(e)[:70]
            if i < RETRY - 1:
                time.sleep(2 * (i + 1))
    return "dead", last


def collect():
    """返回 [(json_path, data, source_item)]"""
    items = []
    for fn in sorted(os.listdir(SOURCES)):
        if not fn.endswith(".json") or fn == "mirrors.json":
            continue
        p = os.path.join(SOURCES, fn)
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        for s in data.get("sources", []):
            items.append((p, data, s))
    return items


def main():
    today = datetime.date.today().isoformat()
    items = collect()

    targets = []
    for _p, _d, s in items:
        targets.append(s["url"])
        targets.extend(s.get("mirrors") or [])

    print("probing %d urls ..." % len(targets))
    result = {}
    with concurrent.futures.ThreadPoolExecutor(CONCURRENCY) as ex:
        for url, (st, detail) in zip(targets, ex.map(probe, targets)):
            result[url] = (st, detail)

    # 回写
    for p, data, s in items:
        st, _ = result[s["url"]]
        s["status"] = st
        s["last_checked"] = today

    for p in {p for p, _, _ in items}:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(
                [d for pp, d, _ in items if pp == p][-1], f, ensure_ascii=False, indent=2
            )
            f.write("\n")

    if "--status" in sys.argv:
        lines = ["# 配置源健康状态", "", "生成时间：%s" % today, ""]
        for p, data, s in items:
            lines.append("## %s" % s["name"])
            lines.append("- 主地址：`%s` → **%s**" % (s["url"], result[s["url"]][0]))
            for m in s.get("mirrors") or []:
                if m in result:
                    lines.append("- 镜像：`%s` → %s" % (m, result[m][0]))
            lines.append("")
        os.makedirs(DOCS, exist_ok=True)
        with open(os.path.join(DOCS, "STATUS.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("generated: docs/STATUS.md")

    dead = [u for u, (st, _) in result.items() if st == "dead"]
    print("ok: %d, dead: %d" % (len(result) - len(dead), len(dead)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
