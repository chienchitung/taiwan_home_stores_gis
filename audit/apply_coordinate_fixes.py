# -*- coding: utf-8 -*-
"""修正座標或行政區有誤的門市（2026-10-15 查核）。

以 Google 地圖地點座標為準，並以內政部國土測繪中心「坐標查詢行政區」確認座標所在鄉鎮市區：
- 桃園遠東百貨（中正路 20 號）：原座標在蘆竹區（約差 6 km），改用 Google 地圖上兩店各自的地點座標。
- 台中水湳愛買（中清路二段 1199 號）：原座標落在西屯區；Google 地點座標位於北屯區，與地址一致，改用之。
- 新竹大遠百（西大路 323 號）：座標本來就正確（東區）；宜得利地址誤寫「北區」，改為東區。
可重複執行；需在各 sync／apply 腳本之後執行。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"

SRC = "Google 地圖「{}」地點座標（2026-10-15 查核）"
FIXES = {
    ("宜得利", "宜得利 桃園遠東百貨店"): {
        "lat": 24.9898889, "lng": 121.3139313,
        "coordinate_source": SRC.format("NITORI 宜得利家居 桃園遠東百貨店"),
    },
    ("無印良品", "無印良品 桃園遠東門市"): {
        "lat": 24.9897057, "lng": 121.3137792,
        "coordinate_source": SRC.format("無印良品 桃園門市"),
    },
    ("宜得利", "宜得利 台中水湳愛買店"): {
        "lat": 24.1926758, "lng": 120.6597499,
        "coordinate_source": SRC.format("NITORI 宜得利家居 台中水湳愛買店"),
    },
    ("無印良品", "無印良品 愛買台中門市"): {
        "lat": 24.1926758, "lng": 120.6597499,
        "coordinate_source": SRC.format("無印良品 愛買台中門市"),
    },
    ("宜得利", "宜得利 新竹大遠百店"): {
        "address": "新竹市東區西大路323號5樓",
        "clean_address": "新竹市東區西大路323號",
        "clean_query": "宜得利 新竹大遠百店 新竹市東區西大路323號5樓",
        "district": "東區",
    },
}


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    hit = 0
    for s in stores:
        fix = FIXES.get((s.get("brand"), s.get("store_name")))
        if fix:
            s.update(fix)
            hit += 1
    assert hit == len(FIXES), f"matched {hit}/{len(FIXES)}"
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)
    print(f"coordinate fixes applied: {hit}")


if __name__ == "__main__":
    main()
