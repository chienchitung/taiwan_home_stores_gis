# -*- coding: utf-8 -*-
"""逐筆比對樂家康門市座標與 Google 地圖上的地點位置。

- 官方門市資料的 store_link 若是 Google 地圖地點連結（cid=…），讀取該地點的名稱、地址與座標；
- 其餘門市以「樂家康超市 ＋ 店名 ＋ 地址」在 Google 地圖搜尋，取第一筆地點。
- 檢查：Google 地點名稱是否為同一間店、與儀表板座標的距離。結果寫入 audit/lejiakang_gmaps_check.json。
- 用法：python3 audit/verify_lejiakang_google_maps.py（約 5～10 分鐘；每筆間隔 1 秒，避免頻繁請求）
"""
import json
import math
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pxmart_gcis_match import norm_addr  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent
RAW = BASE_DIR / "lejiakang_stores_raw.json"
MAIN_JSON = BASE_DIR.parent / "data" / "taiwan_home_stores_status.json"
OUT = BASE_DIR / "lejiakang_gmaps_check.json"
CN_DIGITS = str.maketrans("123456789", "一二三四五六七八九")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "zh-TW,zh;q=0.9"}


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def place_by_cid(cid):
    """cid 地點頁 → /maps/preview/place JSON → (名稱, 地址, lat, lng)"""
    html = requests.get(f"https://www.google.com/maps?cid={cid}&hl=zh-TW", headers=UA, timeout=30).text
    m = re.search(r'href="(/maps/preview/place[^"]+)"', html)
    if not m:
        return None
    url = re.sub(r"hl=[^&]+", "hl=zh-TW", m.group(1).replace("&amp;", "&"))  # 取中文店名與地址
    data = requests.get("https://www.google.com" + url, headers=UA, timeout=30).text
    body = json.loads(data.split("\n", 1)[1])
    place = body[6]
    name = place[11]
    addr = place[39] if len(place) > 39 else ""
    lat, lng = place[9][2], place[9][3]
    return {"name": name, "address": addr, "lat": lat, "lng": lng}


def place_by_search(query):
    """Google 地圖搜尋（/search?tbm=map 回傳的 JSON）→ 第一筆地點的 (名稱, 地址, lat, lng)"""
    t = requests.get("https://www.google.com/search", params={"tbm": "map", "q": query, "hl": "zh-TW", "gl": "tw"},
                     headers=UA, timeout=30).text
    body = json.loads(t.split("\n", 1)[1].split('/*""*/')[0])
    found = []

    def walk(x):
        if found or not isinstance(x, list):
            return
        if len(x) > 39 and isinstance(x[11], str) and isinstance(x[9], list) and len(x[9]) > 3:
            found.append({"name": x[11], "address": x[39] or "", "lat": x[9][2], "lng": x[9][3]})
            return
        for y in x:
            walk(y)

    walk(body)
    return found[0] if found else None


def judge(short, address, g):
    """店名比對：數字轉國字（九如1 → 九如一），允許 Google 店名多／少縣市字首（大里中興、桃園南竹）；地址比對門牌"""
    core = short.removesuffix("店").translate(CN_DIGITS)
    gname = g["name"].replace(" ", "").translate(CN_DIGITS)
    gcore = gname.split("超市")[-1].removesuffix("店")
    brand = "樂家康" in gname or "家樂福" in gname
    return {"name_match": brand and bool(gcore) and (core in gname or core[2:] in gname or gcore in core),
            "address_match": norm_addr(re.sub(r"^\d+(台灣)?", "", g["address"])) == norm_addr(address)}


def main():
    raw = {r["name"]: r for r in json.loads(RAW.read_text(encoding="utf-8"))}
    stores = [s for s in json.loads(MAIN_JSON.read_text(encoding="utf-8")) if s.get("brand") == "樂家康"]
    only = set(sys.argv[1:])  # 可指定店名只重查部分門市，結果併回既有檔案
    prev = {x["store"]: x for x in json.loads(OUT.read_text(encoding="utf-8"))} if only and OUT.exists() else {}
    results = []
    for s in stores:
        if only and s["store_name"] not in only:
            results.append(prev[s["store_name"]])
            continue
        short = s["store_name"].replace("樂家康 ", "")
        link = raw.get(short, {}).get("store_link") or ""
        m = re.search(r"cid=(\d+)", link)
        try:
            g, how = (place_by_cid(m.group(1)), "cid") if m else (None, "search")
            # 地點連結以外的門市依序試：店名＋地址 → 地址＋品牌 → 品牌＋店名縮寫（Google 對部分寫法查無結果）
            for q in ([] if m else [f"樂家康超市 {short} {s['address']}", f"{s['address']} 樂家康",
                                     f"樂家康 {short.removesuffix('店')}"]):
                g = place_by_search(q)
                if g and ("樂家康" in g["name"] or "家樂福" in g["name"]):
                    break
                time.sleep(1)
        except Exception as e:  # 單筆失敗不中斷
            g, how = None, f"error: {e}"
        r = {"store": s["store_name"], "address": s["address"], "dashboard": [s["lat"], s["lng"]], "how": how, "google": g}
        if g:
            r["distance_m"] = round(km((s["lat"], s["lng"]), (g["lat"], g["lng"])) * 1000)
            r.update(judge(short, s["address"], g))
        results.append(r)
        print(f'{s["store_name"]}: {how} {r.get("distance_m", "—")} m {g["name"] if g else ""}', flush=True)
        time.sleep(1)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
