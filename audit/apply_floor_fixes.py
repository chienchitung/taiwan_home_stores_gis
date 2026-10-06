# -*- coding: utf-8 -*-
"""依品牌官方門市頁／商場樓層頁修正門市地址中的樓層（2026-10-05 查核）。

Google 地圖在此環境無法連線（google.com 受網路政策限制、Maps API 金鑰只在 Netlify），
因此以官方來源核對；地址其餘部分不變。
"""
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MAIN_JSON = BASE.parent / "data" / "taiwan_home_stores_status.json"
MAIN_CSV = BASE.parent / "data" / "taiwan_home_stores_status.csv"

# 門市 -> (舊樓層字串, 新樓層字串, 來源)
FIXES = {
    "無印良品 花蓮遠東門市": ("581號B1", "581號3F",
        "https://www.feds.com.tw/M/52/MallInfo/FloorStore?FloorId=166&StoreId=4598&tab=floor-3F"),
    "無印良品 板橋大遠百門市": ("28號7F", "28號3F",
        "https://www.feds.com.tw/m/54/MallInfo/FloorStore?FloorId=58&StoreId=4593&tab=floor-3F"),
    "無印良品 中友百貨門市": ("161號A棟7F", "161號B棟3F",
        "https://shop.muji.tw/muji-journal/news/news/170526_1.html"),
    "無印良品 嘉義耐斯門市": ("600號4F", "600號B1F",
        "https://shop.muji.tw/Shop/StoreDetail/41566/37644"),
    "無印良品 CITYLINK南港門市": ("369號C棟2F", "369號C棟3F",
        "https://www.muji.com/tw/news/news/180529.html"),
    "無印良品 微風南京門市": ("337號B1", "337號1F",
        "https://shop.muji.tw/Shop/StoreDetail/41566/37649"),
    "無印良品 文心秀泰門市": ("289號B1", "289號4F",
        "https://shop.muji.tw/Shop/StoreDetail/41566/37666"),
}


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    done = []
    for s in stores:
        fix = FIXES.get(s.get("store_name"))
        if not fix:
            continue
        old, new, src = fix
        for key in ("address", "clean_address"):
            if old in str(s.get(key, "")):
                s[key] = s[key].replace(old, new)
        s["address_floor_source"] = src
        done.append((s["store_name"], s["address"]))
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(stores)
    for d in done:
        print(*d)


if __name__ == "__main__":
    main()
