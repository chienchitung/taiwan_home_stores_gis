# -*- coding: utf-8 -*-
"""新增經查證的歷史門市紀錄（已不在任何官方門市清單中，sync 腳本不會產生）。
可重複執行：已存在的紀錄會以這裡的欄位更新（保留原 n）。"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"

NEW_STORES = [
    {
        "brand": "IKEA",
        "store_name": "IKEA 台北敦南店（台灣首店）",
        "store_type": "台灣首店",
        "region": "北部",
        "city": "台北市",
        "address": "台北市大安區敦化南路一段246號B1（原永琦百貨，現遠東SOGO敦化館）",
        "status": "已結束營業",
        "note": "IKEA台灣首店，位於永琦百貨地下室，約1,200坪；1994/12/14試賣、12/17正式開幕，2001年9月2日熄燈",
        "district": "大安區",
        "channel_format": "百貨商場 / 購物中心",
        "status_category": "歷史變動（已熄燈/遷址）",
        # 座標為人工定位於遠東SOGO敦化館（忠孝敦化路口西南側）
        "lat": 25.0412,
        "lng": 121.5489,
        "geocode_score": 70,
        "clean_address": "台北市大安區敦化南路一段246號",
        "clean_name": "IKEA 台北敦南店",
        "clean_query": "IKEA 台北敦南店 台北市大安區敦化南路一段246號",
        "is_co_location": False,
        "store_format": "百貨／購物中心門市",
    },
]


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    existing = {(s.get("brand"), s.get("store_name")) for s in stores}
    next_n = max(int(s.get("n") or 0) for s in stores) + 1
    added = 0
    for new in NEW_STORES:
        if (new["brand"], new["store_name"]) in existing:
            for s in stores:
                if (s.get("brand"), s.get("store_name")) == (new["brand"], new["store_name"]):
                    s.update(new)
            continue
        stores.append({**new, "n": next_n})
        next_n += 1
        added += 1
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)
    print(f"historical stores added: {added}")


if __name__ == "__main__":
    main()
