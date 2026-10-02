#!/usr/bin/env python3
"""Refresh official store rosters and prepare Google Maps coordinate checks."""

from __future__ import annotations

import json
import math
import re
from copy import deepcopy
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data" if (ROOT.parent / "data").exists() else ROOT
CSV_PATH = (DATA_DIR / "taiwan_home_stores_status.csv") if (DATA_DIR / "taiwan_home_stores_status.csv").exists() else (ROOT / "taiwan_home_stores_status.csv")
JSON_PATH = (DATA_DIR / "taiwan_home_stores_status.json") if (DATA_DIR / "taiwan_home_stores_status.json").exists() else (ROOT / "taiwan_home_stores_status.json")
QUERY_PATH = ROOT / "store_audit_queries.json"
COUNT_PATH = ROOT / "store_count_audit.csv"
AS_OF = date.today().isoformat()

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json,text/html"}
ACTIVE = "營業中"
PAUSED = "暫停營業"


def norm(value: str) -> str:
    value = str(value or "").replace("臺", "台").lower()
    for token in (
        "宜得利", "無印良品", "特力屋", "hola", "hoi!", "hoi！", "好好生活",
        "mr. living", "mr.living", "居家先生", "宜家家居", "ikea", "旗艦店",
        "品牌館", "社區店", "門市", "店",
    ):
        value = value.replace(token, "")
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]", "", value)


def clean_address(value: str) -> str:
    value = str(value or "").replace("臺", "台").replace("Ｆ", "F")
    value = re.sub(r"[（(].*?[）)]", "", value)
    value = re.sub(r"(?:B?\d+F|B?\d+樓|地下\d+樓).*$", "", value, flags=re.I)
    return re.sub(r"\s+", "", value).strip("，, ")


def city_of(address: str) -> str:
    m = re.match(r"(台北市|新北市|桃園市|台中市|台南市|高雄市|新竹市|嘉義市|基隆市|[^市縣]{2,3}[縣市])", address.replace("臺", "台"))
    return m.group(1) if m else ""


def district_of(address: str) -> str:
    m = re.search(r"([\u4e00-\u9fff]{1,4}(?:區|鄉|鎮|市))", address.replace("臺", "台")[3:])
    return m.group(1) if m else city_of(address)


def region_of(city: str) -> str:
    if city in {"台北市", "新北市", "桃園市", "新竹市", "新竹縣", "基隆市", "宜蘭縣", "苗栗縣"}:
        return "北部"
    if city in {"台中市", "彰化縣", "南投縣", "雲林縣"}:
        return "中部"
    if city in {"嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣", "澎湖縣", "金門縣"}:
        return "南部"
    return "東部"


def canonical_store_format(row: dict) -> str:
    """Return one mutually-exclusive, user-facing physical store format."""
    role = str(row.get("location_role") or "")
    role_map = {
        "子品牌門市": "子品牌門市",
        "店中店／專櫃": "店中店／專櫃",
        "訂購取貨中心": "訂購取貨中心",
        "期間限定門市": "期間限定門市",
    }
    if role in role_map:
        return role_map[role]
    if row.get("brand") == "MR. LIVING 居家先生" and "高雄巨蛋" in str(row.get("store_name") or ""):
        return "大型獨棟／街邊門市"

    text = " ".join(str(row.get(k) or "") for k in
                    ("store_name", "store_type", "channel_format", "address")).lower()
    if "deco home" in text:
        return "子品牌門市"
    if any(k in text for k in ("訂購取貨", "取貨中心", "pup")):
        return "訂購取貨中心"
    if any(k in text for k in ("期間限定", "快閃", "pop up", "popup")):
        return "期間限定門市"
    mass_retail = ("愛買", "大全聯", "大潤發", "萬家福", "家樂福", "大買家", "全聯", "台糖", "量販店中店", "超市複合")
    if any(k in text for k in mass_retail):
        return "量販店中店"
    if "專櫃" in str(row.get("store_name") or "") or "店中店" in str(row.get("store_type") or ""):
        return "店中店／專櫃"
    if "社區" in text or "都會社區型" in text or "城市型小型" in text:
        return "都會／社區門市"

    mall = ("百貨", "購物中心", "outlet", "mall", "廣場", "夢時代", "漢神", "漢神巨蛋", "大立", "遠東", "遠百",
            "三越", "sogo", "微風", "京站", "中友", "金典", "南紡", "lalaport", "mop", "三井", "耐斯",
            "秀泰", "新時代", "義享", "環球", "global", "新月", "大魯閣", "skm", "裕隆城", "dream plaza")
    if any(k in text for k in mall):
        return "百貨／購物中心門市"
    return "大型獨棟／街邊門市"


def google_coords(url: str):
    m = re.search(r"!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)", url or "")
    if not m:
        m = re.search(r"/@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", url or "")
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)


def official_nitori():
    html = requests.get("https://www.nitori-net.tw/store", headers=HEADERS, timeout=45).text
    soup = BeautifulSoup(html, "html.parser")
    graph = json.loads(soup.find("script", type="application/ld+json").string)["@graph"]
    return [
        {"name": item["name"], "address": item["address"]["streetAddress"], "status": ACTIVE,
         "source": "https://www.nitori-net.tw/store"}
        for item in graph if item.get("@type") == "LocalBusiness"
    ]


def official_tr_api(host: str, brand: str):
    url = host + "/rest/v2/trplus/pos/search"
    data = requests.get(url, headers=HEADERS, timeout=45).json()["data"]["pos"]
    rows = []
    for item in data:
        status = PAUSED if "暫停營業" in item["posName"] else ACTIVE
        lat, lng = google_coords(item.get("googleMapUrl", ""))
        rows.append({
            "name": re.sub(r"\s*[【(（].*?暫停營業.*?[】)）]\s*", "", item["posName"]).strip(),
            "address": item["posAddress"], "status": status, "lat": lat, "lng": lng,
            "google_url": item.get("googleMapUrl", ""), "source": url,
        })
    return rows


def official_hoi():
    url = ("https://www.hoihome.tw/webapi/LocationV2/GetLocationList"
           "?lat=23.7&lng=120.9&startIndex=0&maxCount=100&shopId=40000")
    data = requests.get(url, headers=HEADERS, timeout=45).json()["Data"]["List"]
    return [
        {"name": x["Name"], "address": x["Address"], "status": ACTIVE,
         "lat": x.get("Latitude"), "lng": x.get("Longitude"), "source": url}
        for x in data
    ]


def best_existing(existing, brand: str, item: dict):
    pool = [x for x in existing if x["brand"] == brand and x["status"] == ACTIVE]
    ca = clean_address(item["address"])
    by_address = [x for x in pool if clean_address(x["address"]) == ca]
    if by_address:
        return max(by_address, key=lambda x: SequenceMatcher(None, norm(item["name"]), norm(x["store_name"])).ratio())
    if not pool:
        return None
    scored = [(SequenceMatcher(None, norm(item["name"]), norm(x["store_name"])).ratio(), x) for x in pool]
    score, match = max(scored, key=lambda z: z[0])
    return match if score >= 0.65 else None


def make_row(existing, brand: str, item: dict):
    old = best_existing(existing, brand, item)
    row = deepcopy(old) if old else {k: "" for k in existing[0].keys()}
    prefix = {"宜得利": "宜得利 ", "特力屋": "特力屋 ", "HOLA": "HOLA ", "hoi! 好好生活": "hoi! "}[brand]
    name = item["name"] if item["name"].lower().startswith(prefix.strip().lower()) else prefix + item["name"]
    address = item["address"].replace("臺", "台")
    city = city_of(address)
    row.update({
        "brand": brand, "store_name": name, "address": address, "city": city,
        "district": district_of(address), "region": region_of(city), "status": item["status"],
        "status_category": "現行營運中" if item["status"] == ACTIVE else "暫停營業",
        "opened_date": "官方在線門市", "note": f"{AS_OF} 官方門市清單核對",
        "clean_address": clean_address(address), "clean_name": name,
        "clean_query": f"{name} {address}", "geocode_score": 100 if item.get("google_url") else "",
    })
    if item.get("lat") is not None and item.get("lng") is not None:
        row["lat"], row["lng"] = item["lat"], item["lng"]
    return row


def main():
    existing = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    official = {
        "宜得利": official_nitori(),
        "特力屋": official_tr_api("https://cdn.trplus.com.tw", "特力屋"),
        # HOLA's endpoint also publishes La-Z-Boy counters.  They are valid POIs,
        # but not HOLA stores and must never be re-imported into the HOLA count.
        "HOLA": [x for x in official_tr_api("https://www.hola.com.tw", "HOLA")
                 if "la-z-boy" not in x["name"].lower()],
        "hoi! 好好生活": official_hoi(),
    }

    # Brands with authoritative roster counts already represented by the active rows.
    for brand in ("無印良品", "IKEA", "MR. LIVING 居家先生"):
        official[brand] = [
            {"name": x["store_name"], "address": x["address"], "status": ACTIVE,
             "source": {"無印良品": "https://www.muji.tw/tw/", "IKEA": "https://www.ikea.com.tw/zh/store/index",
                        "MR. LIVING 居家先生": "https://www.mrliving.com.tw/store-locations"}[brand]}
            for x in existing if x["brand"] == brand and x["status"] == ACTIVE
        ]

    refreshed = []
    refreshed_brands = set(official)
    # Retain explicitly historical and explicitly excluded records, but replace
    # all other current/paused rosters.
    for row in existing:
        if (row["brand"] not in refreshed_brands or row["status"] not in {ACTIVE, PAUSED}
                or row.get("dashboard_excluded")):
            refreshed.append(row)
    for brand, items in official.items():
        if brand in {"無印良品", "IKEA", "MR. LIVING 居家先生"}:
            refreshed.extend(deepcopy(x) for x in existing if x["brand"] == brand and x["status"] == ACTIVE)
        else:
            refreshed.extend(make_row(existing, brand, item) for item in items)

    for i, row in enumerate(refreshed, 1):
        row["n"] = i
        row["is_co_location"] = False
        if row.get("brand") in {"宜得利", "無印良品", "IKEA", "特力屋", "HOLA", "hoi! 好好生活", "MR. LIVING 居家先生"}:
            row["store_format"] = canonical_store_format(row)
    for row in refreshed:
        row["is_co_location"] = sum(
            math.hypot(float(row["lat"]) - float(other["lat"]), float(row["lng"]) - float(other["lng"])) < 0.00035
            for other in refreshed if row.get("lat") not in (None, "") and other.get("lat") not in (None, "")
        ) > 1

    JSON_PATH.write_text(json.dumps(refreshed, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame(refreshed).to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

    counts = []
    for brand, items in official.items():
        old_count = sum(x["brand"] == brand and x["status"] == ACTIVE for x in existing)
        active_count = sum(x["status"] == ACTIVE for x in items)
        paused_count = sum(x["status"] == PAUSED for x in items)
        counts.append({"brand": brand, "before_active": old_count, "official_active": active_count,
                       "official_paused": paused_count, "difference": active_count - old_count,
                       "source": items[0]["source"] if items else "", "checked_at": AS_OF})
    pd.DataFrame(counts).to_csv(COUNT_PATH, index=False, encoding="utf-8-sig")

    queries = []
    for row in refreshed:
        if row["status"] != ACTIVE:
            continue
        # TR APIs already expose their exact Google Maps place URLs and coordinates.
        item = next((x for x in official.get(row["brand"], [])
                     if clean_address(x["address"]) == clean_address(row["address"])), None)
        queries.append({"n": row["n"], "brand": row["brand"], "store_name": row["store_name"],
                        "address": row["address"], "query": f'{row["store_name"]} {row["address"]}',
                        "official_google_url": (item or {}).get("google_url", "")})
    QUERY_PATH.write_text(json.dumps(queries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(pd.DataFrame(counts).to_string(index=False))
    print(f"Wrote {len(refreshed)} records and {len(queries)} Google Maps checks")


if __name__ == "__main__":
    main()
