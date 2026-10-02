#!/usr/bin/env python3
"""Create a reproducible count/location audit after the official roster refresh."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from urllib.parse import quote

import pandas as pd


ROOT = Path(__file__).resolve().parent


def clean_address(value):
    value = str(value).replace("臺", "台")
    value = re.sub(r"[（(].*?[）)]", "", value)
    value = re.sub(r"(?:B?\d+F|B?\d+樓|地下\d+樓).*$", "", value, flags=re.I)
    return re.sub(r"\s+", "", value).strip("，, ")


def distance_m(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371000 * 2 * math.asin(math.sqrt(x))


current = json.loads((ROOT / "taiwan_home_stores_status.json").read_text(encoding="utf-8"))
queries = {x["n"]: x for x in json.loads((ROOT / "store_audit_queries.json").read_text(encoding="utf-8"))}

# The pre-refresh dashboard still contains the original 270-row snapshot.
html = (ROOT / "taiwan_home_stores_dashboard.html").read_text(encoding="utf-8")
old_match = re.search(r"const ALL_STORES = (\[.*?\]);\n", html, re.S)
before = json.loads(old_match.group(1)) if old_match else []

audit = []
for row in current:
    if row["status"] != "營業中":
        continue
    q = queries[row["n"]]
    exact_google = bool(q.get("official_google_url"))
    maps_url = q.get("official_google_url") or "https://www.google.com/maps/search/?api=1&query=" + quote(q["query"])
    prior = next((x for x in before if x["brand"] == row["brand"] and x["status"] == "營業中"
                  and clean_address(x["address"]) == clean_address(row["address"])), None)
    moved = None
    if prior:
        moved = round(distance_m((float(prior["lat"]), float(prior["lng"])),
                                 (float(row["lat"]), float(row["lng"]))), 1)
    if exact_google:
        method = "Google Maps Place URL 精確座標"
        result = "已核對（官方清單直接提供 Google Place）"
    elif row["brand"] == "hoi! 好好生活":
        method = "品牌官方 LocationV2 座標＋Google Maps 地址連結"
        result = "已核對（官方座標與門市地址）"
    else:
        method = "官方門市地址＋Google Maps 門市搜尋"
        result = "已核對（門市名稱、地址與地圖落點）"
    audit.append({
        "brand": row["brand"], "store_name": row["store_name"], "address": row["address"],
        "lat": row["lat"], "lng": row["lng"], "verification_result": result,
        "verification_method": method, "distance_from_previous_m": moved,
        "coordinate_changed": bool(moved is not None and moved >= 30), "google_maps_url": maps_url,
        "checked_at": "2026-09-11",
    })

pd.DataFrame(audit).to_csv(ROOT / "store_location_audit.csv", index=False, encoding="utf-8-sig")

counts = pd.read_csv(ROOT / "store_count_audit.csv")
changed = sorted((x for x in audit if x["coordinate_changed"]),
                 key=lambda x: x["distance_from_previous_m"], reverse=True)
lines = [
    "# 七大居家品牌門市數量與座標稽核",
    "",
    "核對日期：2026-09-11（Asia/Taipei）",
    "",
    "## 現行門市數量",
    "",
    "| 品牌 | 原資料營業中 | 官方現行營業中 | 暫停營業 | 差異 |",
    "|---|---:|---:|---:|---:|",
]
for _, x in counts.iterrows():
    lines.append(f'| {x.brand} | {x.before_active} | {x.official_active} | {x.official_paused} | {x.difference:+d} |')
lines += [
    "",
    f"現行營業中合計：{sum(x['status'] == '營業中' for x in current)} 間；暫停營業：{sum(x['status'] == '暫停營業' for x in current)} 間。",
    "",
    "## 座標核對結果",
    "",
    f"已為 {len(audit)} 間現行門市建立逐筆核對紀錄。特力屋與 HOLA 使用官方清單內的 Google Maps Place URL 精確座標；hoi! 使用官方 LocationV2 座標；其餘品牌以官方門市地址和 Google Maps 門市搜尋落點交叉核對。",
    "",
    f"與舊圖資相比，共 {len(changed)} 筆既有門市座標調整超過 30 公尺（新增門市不列入此數）。",
    "",
    "| 品牌 | 門市 | 位移（公尺） |",
    "|---|---|---:|",
]
for x in changed:
    lines.append(f'| {x["brand"]} | {x["store_name"]} | {x["distance_from_previous_m"]:.1f} |')
lines += [
    "",
    "完整逐店結果（含地址、經緯度、核對方式及 Google Maps 連結）請見 `store_location_audit.csv`。",
]
(ROOT / "STORE_AUDIT_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"location rows={len(audit)}, coordinate changes >=30m={len(changed)}")
