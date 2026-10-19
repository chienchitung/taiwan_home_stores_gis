# -*- coding: utf-8 -*-
"""補入官方門市清單已有、但主資料尚未收錄的門市，並修正店型（2026-10-19 查核）。

以特力屋官方門市 API（https://cdn.trplus.com.tw/rest/v2/trplus/pos/search）比對主資料：
- 特力屋 新莊幸福店(社區店)：2026-10-04 開幕（特力屋貼文「新莊幸福店，10/4盛大開幕」）。
- 特力屋 豐原大社店(社區店)：2026-10-08 試營運（特力屋貼文「豐原大社店 10/8試營運」），位於 Mini G Mall B1。
座標為 Google 地圖上同名地點，並以國土測繪中心「坐標查詢行政區」確認所在行政區。
開幕日期同步寫入 store_opened_dates_verified.json（apply_verified_opened_dates.py 會依該檔覆寫）。

另修正：特力屋 彰化和美店 為大型店（官方名稱無「社區店」，且官方大型店 28 間的口徑須含此店），
店型由「都會／社區門市」改為「大型獨棟／街邊門市」。
可重複執行；需在各 sync／apply 腳本之後執行。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
VERIFIED_JSON = BASE_DIR / "store_opened_dates_verified.json"
SALE_EVENTS = "https://tw.sale-events.com/sale/%E7%89%B9%E5%8A%9B%E5%B1%8B/"

NEW_STORES = [
    {
        "brand": "特力屋", "store_name": "特力屋 新莊幸福店(社區店)", "region": "北部", "city": "新北市",
        "district": "新莊區", "address": "新北市新莊區幸福路763號B1（J-MART 佳瑪新莊店）",
        "clean_address": "新北市新莊區幸福路763號",
        "lat": 25.0488719, "lng": 121.4478707,
        "coordinate_source": "Google 地圖「特力屋新莊幸福店(社區店)」地點座標（2026-10-19 查核）",
        "opened_date": "2026-10-04",
        "evidence": "特力屋貼文（SaleEvents 轉載 2026-09-29）：「歡慶特力屋 新莊幸福店，10/4盛大開幕！」；2026-10-04 貼文「正式開幕囉」",
    },
    {
        "brand": "特力屋", "store_name": "特力屋 豐原大社店(社區店)", "region": "中部", "city": "台中市",
        "district": "豐原區", "address": "台中市豐原區大社街8號B1之1（Mini G Mall）",
        "clean_address": "台中市豐原區大社街8號",
        "lat": 24.2500711, "lng": 120.7013912,
        "coordinate_source": "Google 地圖「特力屋豐原大社店(社區店)」地點座標（2026-10-19 查核）",
        "opened_date": "2026-10-08",
        "evidence": "特力屋貼文（SaleEvents 轉載 2026-10-07）：「歡慶特力屋 豐原大社店 10/8試營運！」；以試營運首日為開幕日",
    },
]
FORMAT_FIXES = {("特力屋", "特力屋 彰化和美店"): {"store_format": "大型獨棟／街邊門市"}}


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    existing = {(s["brand"], s["store_name"]) for s in stores}
    next_n = max(int(s.get("n") or 0) for s in stores) + 1
    added = 0
    for item in NEW_STORES:
        if (item["brand"], item["store_name"]) in existing:
            continue
        row = {k: v for k, v in item.items() if k != "evidence"}
        row.update({
            "store_type": "", "channel_format": "", "store_format": "都會／社區門市",
            "status": "營業中", "status_category": "現行營運中", "note": "2026-10-19 官方門市清單核對",
            "geocode_score": 100, "clean_name": item["store_name"],
            "clean_query": f"{item['store_name']} {item['clean_address']}",
            "is_co_location": True, "n": next_n,
            "opened_date_source": SALE_EVENTS, "opened_date_basis": "新聞／官方",
        })
        stores.append(row)
        next_n += 1
        added += 1
    for s in stores:
        fix = FORMAT_FIXES.get((s["brand"], s["store_name"]))
        if fix:
            s.update(fix)
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)

    raw = VERIFIED_JSON.read_text(encoding="utf-8")
    verified = json.loads(raw)
    have = {(v["brand"], v["store_name"]) for v in verified}
    for item in NEW_STORES:
        if (item["brand"], item["store_name"]) not in have:
            verified.append({
                "brand": item["brand"], "store_name": item["store_name"], "date": item["opened_date"],
                "year": int(item["opened_date"][:4]), "confidence": "confirmed",
                "sources": [SALE_EVENTS], "evidence": item["evidence"],
            })
    VERIFIED_JSON.write_text(json.dumps(verified, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""),
                             encoding="utf-8")
    print(f"stores added: {added}; format fixes: {len(FORMAT_FIXES)}")


if __name__ == "__main__":
    main()
