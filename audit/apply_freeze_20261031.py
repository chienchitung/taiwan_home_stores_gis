# -*- coding: utf-8 -*-
"""資料凍結於 2026-10-31：補正官方清單同步後需要人工判斷的門市狀態（2026-11-01 查核）。

- 樂家康 內湖東湖店：2026-11-01 萬家福官方門市 API（含量販與超市）已無此店；經濟部商工登記「康達盛通生活事業
  內湖東湖分公司」狀態為廢止（變更核准日 115/10/07）。查無熄燈新聞，結束日期不列。
- 樂家康 台北林森北店：2026-11-01 官方門市 API 已無此店，但商工登記「統康生活事業東光分公司」仍為核准設立，
  也查無熄燈新聞，維持營業中並在備註標示待確認。
sync_lejiakang_stores.py 只保留官方清單上的門市，這裡把兩間補回主資料（沿用原本的 n 與欄位）。
可重複執行；需在 sync_lejiakang_stores.py 之後、apply_verified_opened_dates.py 之前或之後皆可。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
GCIS_API = "https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB"
OFFICIAL = "https://www.uni-prosperity.com.tw/stores/?hl=zh-TW"

LEJIAKANG_COMMON = {
    "brand": "樂家康", "store_type": "社區生鮮超市", "region": "北部", "city": "台北市",
    "channel_format": "社區生鮮超市 / 街邊獨立", "geocode_score": 100, "is_co_location": False,
    "source_url": OFFICIAL, "store_format": "社區超市", "opened_date_basis": "商工登記", "opened_date_source": GCIS_API,
}
RESTORE = [
    {**LEJIAKANG_COMMON,
     "store_name": "樂家康 內湖東湖店", "address": "台北市內湖區東湖路69號B1", "district": "內湖區",
     "opened_date": "2017-08-01", "status": "已結束營業", "status_category": "歷史變動（已熄燈/遷址）", "closed_date": "",
     "note": "原家樂福超市，2026-07-01 起更名樂家康；2026-11-01 官方門市清單已無此店，商工登記內湖東湖分公司 2026-10-07 核准廢止；"
             "查無熄燈新聞，結束日期不列",
     "closed_date_source": GCIS_API,
     "lat": 25.0689469, "lng": 121.6151344,
     "clean_address": "台北市內湖區東湖路69號B1", "clean_name": "樂家康 內湖東湖店",
     "clean_query": "樂家康 內湖東湖店 台北市內湖區東湖路69號B1",
     "coordinate_source": "Google 地圖「樂家康超市 內湖東湖店」地點座標（2026-10-13 逐筆比對）",
     "google_maps_url": "https://www.google.com/maps/search/?api=1&query=%E6%A8%82%E5%AE%B6%E5%BA%B7%20%E5%85%A7%E6%B9%96%E6%9D%B1%E6%B9%96%E5%BA%97%20%E5%8F%B0%E5%8C%97%E5%B8%82%E5%85%A7%E6%B9%96%E5%8D%80%E6%9D%B1%E6%B9%96%E8%B7%AF69%E8%99%9FB1",
     "verification_status": "2026-11-01 官方清單已移除；商工登記分公司已廢止",
     "official_store_id": "119", "official_branch_ban": "51462601", "branch_registry_name": "康達盛通生活事業內湖東湖分公司",
     "n": 5251},
    {**LEJIAKANG_COMMON,
     "store_name": "樂家康 台北林森北店", "address": "台北市中山區林森北路413號B1", "district": "中山區",
     "opened_date": "2000-10-24", "status": "營業中", "status_category": "現行營運中",
     "note": "原家樂福超市，2026-07-01 起更名樂家康；2026-11-01 官方門市清單已無此店，但商工登記東光分公司仍為核准設立、"
             "查無熄燈新聞，營業狀態待確認",
     "lat": 25.0599458, "lng": 121.5257295,
     "clean_address": "台北市中山區林森北路413號B1", "clean_name": "樂家康 台北林森北店",
     "clean_query": "樂家康 台北林森北店 台北市中山區林森北路413號B1",
     "coordinate_source": "Google 地圖「樂家康超市 台北林森北店」地點座標（2026-10-13 逐筆比對）",
     "google_maps_url": "https://www.google.com/maps/search/?api=1&query=%E6%A8%82%E5%AE%B6%E5%BA%B7%20%E5%8F%B0%E5%8C%97%E6%9E%97%E6%A3%AE%E5%8C%97%E5%BA%97%20%E5%8F%B0%E5%8C%97%E5%B8%82%E4%B8%AD%E5%B1%B1%E5%8D%80%E6%9E%97%E6%A3%AE%E5%8C%97%E8%B7%AF413%E8%99%9FB1",
     "verification_status": "2026-11-01 官方清單已移除、商工登記仍核准設立；待確認",
     "official_store_id": "231", "official_branch_ban": "70788494", "branch_registry_name": "統康生活事業東光分公司",
     "n": 5325},
]


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    keys = {(r["brand"], r["store_name"]) for r in RESTORE}
    used_n = {s.get("n") for s in stores if (s["brand"], s["store_name"]) not in keys}
    stores = [s for s in stores if (s["brand"], s["store_name"]) not in keys]
    for row in RESTORE:
        assert row["n"] not in used_n, f"n {row['n']} 已被其他門市使用"
        stores.append(dict(row))
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)
    print(f"freeze 2026-10-31: restored {len(RESTORE)} rows")


if __name__ == "__main__":
    main()
