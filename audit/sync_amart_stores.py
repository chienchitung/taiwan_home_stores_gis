# -*- coding: utf-8 -*-
"""同步「愛買」量販門市（2026-10-22 查核）。

- 門市清單：中文維基百科〈愛買〉「分店資訊」（截至 2025-10 共 13 間；2026-03 中央社／工商時報報導仍為 13 間，
  忠孝店 2025-09-30 熄燈後未再展店）。愛買官網（www.amart.com.tw）在本環境無法連線。
- 座標：逐店在 Google 地圖搜尋「愛買 ＋ 店名 ＋ 地址」，13 間皆找到同名地點，並以國土測繪中心
  「坐標查詢行政區」確認所在行政區與地址相符（水湳店地址門牌在北屯區，維基寫西屯區，依座標採北屯區）。
- 開幕日期：維基百科〈愛買〉歷史章節逐店記載的開業日（各條附新聞出處）。有試營運者採正式開業日，並在備註寫明試營運日。
  同址換品牌但同一集團持續營運者（吉安量販台中復興店 2000 年併入愛買吉安）採原始開幕日，與萬家福、大全聯的規則一致。
  開幕日期同步寫入 store_opened_dates_verified.json（apply_verified_opened_dates.py 會依該檔覆寫）。
可重複執行：會先移除主資料中的愛買門市，再以本清單寫回；既有門市沿用原本的 n。需在 sync_mass_retail_stores.py 之後執行。
"""
import csv
import json
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
VERIFIED_JSON = BASE_DIR / "store_opened_dates_verified.json"
BRAND = "愛買"
WIKI = "https://zh.wikipedia.org/wiki/愛買"

# (店名, 縣市, 行政區, 地址, Google lat, Google lng, 開幕日, 備註)
STORES = [
    ("基隆店", "基隆市", "信義區", "基隆市信義區深溪路53號B1", 25.1330542, 121.7822013, "2010-01-15", "原址為萬家福量販基隆店"),
    ("景美店", "台北市", "文山區", "台北市文山區景中街30巷12號", 24.9922341, 121.5422939, "1990-09", "愛買第1間分店"),
    ("永和店", "新北市", "永和區", "新北市永和區民生路46巷56號", 24.9965568, 121.5211151, "1996-07", ""),
    ("三重店", "新北市", "三重區", "新北市三重區中正北路193巷45號", 25.0714136, 121.4761974, "2008-10-31", "原址為萬家福量販三重店"),
    ("南雅店", "新北市", "板橋區", "新北市板橋區貴興路101號", 25.001956, 121.4564732, "2015-04-29", "2015-01-31 試營運，4/29 正式開業"),
    ("桃園店", "桃園市", "桃園區", "桃園市桃園區中山路939號", 24.9848928, 121.2859269, "1999-12", "原址為中南紡織廠"),
    ("楊梅店", "桃園市", "楊梅區", "桃園市楊梅區中山北路二段23巷6號", 24.907779, 121.167413, "2000-05", ""),
    ("巨城店", "新竹市", "東區", "新竹市東區中央路229號B3", 24.809691, 120.975657, "2012-04-28", "位於 Big City 遠東巨城購物中心；2012-04-23 試營運"),
    ("豐原店", "台中市", "豐原區", "台中市豐原區水源路420號", 24.2567184, 120.7349868, "2011-01-12", "原址為亞洲購量販"),
    ("復興店", "台中市", "南區", "台中市南區復興路一段359號", 24.1154479, 120.6540222, "1998-12-17", "原為吉安量販台中復興店（1998-12-17 開幕），2000-07 更名愛買吉安"),
    ("水湳店", "台中市", "北屯區", "台中市北屯區中清路二段1199號", 24.1926564, 120.6597145, "2020-09-23", "購物中心型量販店；2020-08-18 試營運"),
    ("台南店", "台南市", "永康區", "台南市永康區中正南路533號", 23.0345864, 120.2288699, "2000-07", "原址為遠東鴻利多量販（1995-01 開業、2000-07 結束），由愛買吉安接手開設"),
    ("花蓮店", "花蓮縣", "花蓮市", "花蓮縣花蓮市和平路581號B1", 23.9781721, 121.5996227, "2009-10-28", "與遠東百貨花蓮店共構"),
]


def region_for(city):
    if city in {"台北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣"}:
        return "北部"
    if city in {"台中市", "彰化縣", "南投縣", "雲林縣"}:
        return "中部"
    if city in {"嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"}:
        return "南部"
    return "東部/離島"


def main():
    rows = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    old_n = {r["store_name"]: r["n"] for r in rows if r.get("brand") == BRAND}
    kept = [r for r in rows if r.get("brand") != BRAND]
    next_n = max(int(r.get("n") or 0) for r in kept) + 1
    stores = []
    for name, city, district, address, lat, lng, opened, note in STORES:
        full = f"{BRAND} {name}"
        n = old_n.get(full)
        if n is None:
            n, next_n = next_n, next_n + 1
        stores.append({
            "brand": BRAND, "store_name": full, "store_type": "量販店 / 倉儲賣場",
            "region": region_for(city), "city": city, "address": address,
            "opened_date": opened, "status": "營業中", "note": note, "district": district,
            "channel_format": "大型獨棟 / 獨立街邊店", "status_category": "現行營運中",
            "lat": lat, "lng": lng, "geocode_score": 100,
            "clean_address": address, "clean_name": full, "clean_query": f"{full} {address}",
            "is_co_location": False, "source_url": WIKI,
            "coordinate_source": f"Google 地圖「愛買 {name}」地點座標（2026-10-22 查核）",
            "google_maps_url": "https://www.google.com/maps/search/?api=1&query=" + quote(f"{full} {address}"),
            "verification_status": "維基百科分店清單；Google 地圖地點與國土測繪中心行政區已交叉核對",
            "n": n, "opened_date_source": WIKI, "opened_date_basis": "新聞／官方",
        })
    all_rows = kept + stores
    MAIN_JSON.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for r in all_rows for k in r))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    raw = VERIFIED_JSON.read_text(encoding="utf-8")
    verified = [v for v in json.loads(raw) if v["brand"] != BRAND]
    for name, _, _, _, _, _, opened, note in STORES:
        verified.append({
            "brand": BRAND, "store_name": f"{BRAND} {name}", "date": opened, "year": int(opened[:4]),
            "confidence": "confirmed", "sources": [WIKI],
            "evidence": f"維基百科〈愛買〉歷史章節開業日：{opened}" + (f"；{note}" if note else ""),
        })
    VERIFIED_JSON.write_text(json.dumps(verified, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""),
                             encoding="utf-8")
    print(f"愛買 {len(stores)} 間")


if __name__ == "__main__":
    main()
