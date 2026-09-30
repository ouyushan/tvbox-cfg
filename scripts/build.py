#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由 sources/*.json 生成 TVBox 可直接填写的配置文件。

输出：
  config/multi.json      多仓聚合（jsDelivr CDN 版，国内直连推荐）
  config/multi-raw.json  多仓聚合（raw.githubusercontent 裸地址版）
  config/live.json       纯直播配置（lives 数组）

用法：
  python scripts/build.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "sources")
CONFIG = os.path.join(ROOT, "config")


def load(name):
    with open(os.path.join(SOURCES, name), "r", encoding="utf-8") as f:
        return json.load(f)


def dump(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("generated:", os.path.relpath(path, ROOT))


def pick_url(src, prefer_cdn=True):
    mirrors = src.get("mirrors") or []
    if not prefer_cdn:
        return src["url"]
    for m in mirrors:
        if "jsdelivr" in m:
            return m
    return src["url"]


def build_multi(prefer_cdn):
    data = load("vod.json")
    urls = []
    for i, s in enumerate(data["sources"], 1):
        if s.get("status") == "dead":
            continue
        if s.get("note"):  # 索引型仓库不给 TVBox 直接加载
            continue
        urls.append({"url": pick_url(s, prefer_cdn), "name": "%d-%s" % (i, s["name"])})
    return {"urls": urls}


def build_live():
    data = load("live.json")
    lives = []
    for s in data["sources"]:
        if s.get("status") == "dead":
            continue
        lives.append(
            {
                "name": s["name"],
                "type": 0,
                "url": pick_url(s, True),
                "playerType": 1,
            }
        )
    return {"lives": lives}


def main():
    dump(os.path.join(CONFIG, "multi.json"), build_multi(True))
    dump(os.path.join(CONFIG, "multi-raw.json"), build_multi(False))
    dump(os.path.join(CONFIG, "live.json"), build_live())
    return 0


if __name__ == "__main__":
    sys.exit(main())
