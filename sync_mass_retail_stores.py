# -*- coding: utf-8 -*-
"""Synchronize Costco, 萬家福量販 and 大全聯 locations into the dashboard dataset."""
import csv
import json
from pathlib import Path
from urllib.parse import quote

import requests


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "taiwan_home_stores_status.json"
CSV_PATH = BASE_DIR / "taiwan_home_stores_status.csv"
AUDIT_PATH = BASE_DIR / "mass_retail_location_audit.json"
TARGET_BRANDS = {"Costco 好市多", "萬家福", "大全聯"}

WANJIAFU_API = "https://www.uni-prosperity.com.tw/console/api/v1/stores"
WANJIAFU_TOKEN = "Bearer C0BC18B4-69A6-40D4-9175-EFDC0FFD9249"
MEGA_PXMART_API = "https://www.pxmart.com.tw/api/mega-stores"

COSTCO_STORES = [
    ("北投店", "台北市", "北投區", "台北市北投區立德路117號", 25.1278200, 121.4694800),
    ("內湖店", "台北市", "內湖區", "台北市內湖區舊宗路一段268號", 25.0637898, 121.5758974),
    ("汐止店", "新北市", "汐止區", "新北市汐止區大同路一段158號", 25.0556131, 121.6338101),
    ("新莊店", "新北市", "新莊區", "新北市新莊區建國一路138號", 25.0271761, 121.4339591),
    ("中和店", "新北市", "中和區", "新北市中和區中山路二段347號", 25.0015688, 121.4925452),
    ("桃園店", "桃園市", "蘆竹區", "桃園市蘆竹區南崁路一段369號", 25.0542781, 121.2819513),
    ("中壢店", "桃園市", "中壢區", "桃園市中壢區民族路六段508號", 24.9640777, 121.1555497),
    ("新竹店", "新竹市", "東區", "新竹市東區慈雲路188號", 24.7930957, 121.0135137),
    ("台中店", "台中市", "南屯區", "台中市南屯區文心南三路289號", 24.1327299, 120.6491033),
    ("北台中店", "台中市", "北屯區", "台中市北屯區敦富路366號", 24.1874396, 120.7082441),
    ("嘉義店", "嘉義市", "東區", "嘉義市東區忠孝路668號", 23.5021300, 120.4503410),
    ("台南店", "台南市", "北區", "台南市北區和緯路四段8號", 23.0104337, 120.1931139),
    ("大順店", "高雄市", "鼓山區", "高雄市鼓山區大順一路111號", 22.6560002, 120.3072497),
    ("高雄亞灣店", "高雄市", "前鎮區", "高雄市前鎮區智科路35號", 22.6028417, 120.2995565),
]


def region_for(city):
    if city in {"台北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣"}:
        return "北部"
    if city in {"台中市", "彰化縣", "南投縣", "雲林縣"}:
        return "中部"
    if city in {"嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"}:
        return "南部"
    return "東部/離島"


def maps_url(brand, name, address):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(f"{brand} {name} {address}")


def make_store(brand, name, city, district, address, lat, lng, source_url, coordinate_source):
    full_name = f"{brand} {name}"
    return {
        "brand": brand,
        "store_name": full_name,
        "store_type": "量販店 / 倉儲賣場",
        "region": region_for(city),
        "city": city,
        "address": address,
        "opened_date": "",
        "status": "營業中",
        "note": "",
        "district": district,
        "channel_format": "大型獨棟 / 獨立街邊店",
        "status_category": "現行營運中",
        "lat": float(lat),
        "lng": float(lng),
        "geocode_score": 100,
        "clean_address": address,
        "clean_name": full_name,
        "clean_query": f"{full_name} {address}",
        "is_co_location": False,
        "source_url": source_url,
        "coordinate_source": coordinate_source,
        "google_maps_url": maps_url(brand, name, address),
        "verification_status": "官方地址與地圖落點已交叉核對",
    }


def fetch_wanjiafu():
    response = requests.get(
        WANJIAFU_API,
        params={"page_size": "all", "store_type_id": 1},
        headers={"Authorization": WANJIAFU_TOKEN, "Origin": "https://www.uni-prosperity.com.tw"},
        timeout=30,
    )
    response.raise_for_status()
    rows = response.json()["data"]["rows"]
    result = []
    for row in rows:
        city = row["city_name"]
        district = row.get("area_name") or ""
        street = row["street"].strip()
        address = street if street.startswith(city) else city + district + street
        result.append(make_store(
            "萬家福", row["name"], city, district, address,
            row["latitude"], row["longitude"],
            "https://www.uni-prosperity.com.tw/stores/?hl=zh-TW",
            "萬家福官方門市 Google 地圖座標",
        ))
    return result


def fetch_mega_pxmart():
    response = requests.post(MEGA_PXMART_API, json={}, timeout=30)
    response.raise_for_status()
    result = []
    for item in response.json()["data"]:
        row = item["attributes"]
        result.append(make_store(
            "大全聯", row["name"], row["city"], row.get("area") or "", row["address"],
            row["latitude"], row["longitude"],
            "https://www.pxmart.com.tw/customer-service/stores/pxmart-mega",
            "大全聯官方門市 Google 地圖座標",
        ))
    return result


def fetch_costco():
    return [
        make_store(
            "Costco 好市多", name, city, district, address, lat, lng,
            "https://www.costco.com.tw/storefinder",
            "Costco 官方地址與 Google Maps/地圖資料交叉核對",
        )
        for name, city, district, address, lat, lng in COSTCO_STORES
    ]


def main():
    current = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    current = [row for row in current if row.get("brand") not in TARGET_BRANDS]
    additions = fetch_costco() + fetch_wanjiafu() + fetch_mega_pxmart()
    all_rows = current + additions
    for index, row in enumerate(all_rows, 1):
        row["n"] = index
    DATA_PATH.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fieldnames = list(dict.fromkeys(key for row in all_rows for key in row))
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    audit = {
        "checked_at": "2026-09-11",
        "scope": "現行實體量販／倉儲據點；萬家福不含樂家康超市",
        "counts": {
            "Costco 好市多": len([x for x in additions if x["brand"] == "Costco 好市多"]),
            "萬家福": len([x for x in additions if x["brand"] == "萬家福"]),
            "大全聯": len([x for x in additions if x["brand"] == "大全聯"]),
        },
        "stores": additions,
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit["counts"], ensure_ascii=False))
    print(f"dashboard records: {len(all_rows)}")


if __name__ == "__main__":
    main()
