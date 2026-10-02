# -*- coding: utf-8 -*-
"""Synchronize Shopee buyer-pickup service points from the official SPX map.

The official locator caps each search at the nearest 100 points.  We therefore
sample Taiwan on a geographic grid, add denser samples in metropolitan areas,
and de-duplicate with the official service-point id.
"""
import asyncio
import csv
import json
import random
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

import aiohttp


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "taiwan_home_stores_status.json"
CSV_PATH = BASE_DIR / "taiwan_home_stores_status.csv"
AUDIT_PATH = BASE_DIR / "shopee_location_audit.json"
API_URL = "https://spx.tw/api/service-point/point/around/list"
SOURCE_URL = "https://spx.tw/service-point"
BRAND = "蝦皮店到店"


def region_for(city):
    city = city.replace("臺", "台")
    if city in {"台北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣"}:
        return "北部"
    if city in {"台中市", "彰化縣", "南投縣", "雲林縣"}:
        return "中部"
    if city in {"嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"}:
        return "南部"
    return "東部/離島"


def grid(lat_min, lat_max, lng_min, lng_max, step):
    points = []
    lat = lat_min
    while lat <= lat_max + 1e-9:
        lng = lng_min
        while lng <= lng_max + 1e-9:
            points.append((round(lat, 6), round(lng, 6)))
            lng += step
        lat += step
    return points


def query_points():
    # Broad coverage for the main island plus dedicated offshore-island grids.
    mainland = grid(21.90, 25.35, 120.00, 122.00, 0.10)
    points = [
        (lat, lng) for lat, lng in mainland
        if (
            (lat < 22.5 and 120.55 <= lng <= 121.05)
            or (22.5 <= lat < 23.0 and 120.15 <= lng <= 121.45)
            or (23.0 <= lat < 24.0 and 120.00 <= lng <= 121.70)
            or (24.0 <= lat < 24.7 and 120.25 <= lng <= 121.85)
            or (lat >= 24.7 and 120.55 <= lng <= 122.00)
        )
    ]
    points += grid(23.15, 23.85, 119.25, 119.75, 0.10)  # Penghu
    points += grid(24.35, 24.55, 118.15, 118.50, 0.07)  # Kinmen
    points += grid(25.90, 26.40, 119.85, 120.55, 0.10)  # Matsu
    points += [(22.055, 121.55), (22.675, 121.49)]       # Orchid/Green islands

    # The API returns at most 100 records. Dense grids prevent hidden points in
    # Taipei–Taoyuan, Taichung, Tainan and Kaohsiung metropolitan areas.
    points += grid(24.75, 25.35, 120.85, 122.00, 0.045)
    points += grid(24.45, 24.85, 120.75, 121.25, 0.05)
    points += grid(23.85, 24.45, 120.30, 121.05, 0.05)
    points += grid(22.35, 23.45, 120.05, 120.65, 0.05)
    return sorted(set(points))


async def fetch_one(session, semaphore, lat, lng):
    params = {
        "radius": 400000000,
        "longitude": lng,
        "latitude": lat,
        "selected_radius": 4000,
        "support_buyer_collection": 1,
    }
    for attempt in range(8):
        try:
            async with semaphore:
                async with session.get(API_URL, params=params) as response:
                    response.raise_for_status()
                    payload = await response.json(content_type=None)
            return payload.get("data", {}).get("list", [])
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == 7:
                raise
            await asyncio.sleep(min(30, 1.5 * (2 ** attempt)) + random.random())


async def fetch_all():
    points = query_points()
    timeout = aiohttp.ClientTimeout(total=40)
    connector = aiohttp.TCPConnector(limit=8)
    headers = {"Referer": SOURCE_URL, "Accept": "application/json"}
    semaphore = asyncio.Semaphore(6)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector, headers=headers) as session:
        tasks = [fetch_one(session, semaphore, lat, lng) for lat, lng in points]
        responses = await asyncio.gather(*tasks)
    unique = {}
    capped_queries = 0
    for rows in responses:
        capped_queries += len(rows) >= 100
        for row in rows:
            functions = row.get("ext", {}).get("function_data", {})
            if functions.get("support_buyer_collection") == 1 and row.get("is_display", True):
                unique[int(row["id"])] = row
    return unique, len(points), capped_queries


def normalize_store(row):
    address_data = json.loads(row.get("address_data") or "{}")
    city = (address_data.get("city") or "").replace("臺", "台")
    district = (address_data.get("district") or "").replace("臺", "台")
    address = (row.get("address") or "").replace("臺", "台").strip()
    # A few official address_data records retain an old/wrong district id even
    # though the human-readable address and Google pin are correct. Prefer the
    # address prefix when it carries a complete city + district.
    address_parts = re.match(
        r"^(?P<city>[^縣市]{1,4}[縣市])(?P<district>.{1,5}?[區鄉鎮市])(?![區鄉鎮市])",
        address,
    )
    if address_parts:
        city = address_parts.group("city")
        district = address_parts.group("district")
    lat = float(row["latitude"])
    lng = float(row["longitude"])
    alias = (row.get("alias") or row.get("point_nick_name") or f"門市 {row['id']}").strip()
    point_type = "智取門市" if row.get("ext", {}).get("support_locker") else "直營／合作服務點"
    coordinate_ok = 21.7 <= lat <= 26.5 and 117.9 <= lng <= 122.2
    address_ok = bool(district and district in address and (city[:2] in address or not address.startswith(("台", "新", "高", "基", "桃", "嘉"))))
    status = "暫停營運" if row.get("point_status") == 3 else "營業中"
    maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote(f"{lat:.6f},{lng:.6f}")
    verification = "官方 Google Maps 圖層座標已逐筆載入；地址行政區一致"
    if not coordinate_ok or not address_ok:
        verification = "需人工複核：官方地址行政區與座標欄位不一致"
    return {
        "brand": BRAND,
        "store_name": f"{BRAND} {alias}",
        "store_type": point_type,
        "region": region_for(city),
        "city": city,
        "address": address,
        "opened_date": "",
        "status": status,
        "note": "",
        "district": district,
        "channel_format": "電商取貨據點",
        "status_category": "現行營運中" if status == "營業中" else "暫停營運",
        "lat": lat,
        "lng": lng,
        "geocode_score": 100 if coordinate_ok and address_ok else 60,
        "clean_address": address,
        "clean_name": alias,
        "clean_query": f"蝦皮店到店 {alias} {address}",
        "is_co_location": False,
        "source_url": SOURCE_URL,
        "coordinate_source": "蝦皮官方服務據點資料，於官方 Google Maps 圖層顯示",
        "google_maps_url": maps_url,
        "verification_status": verification,
        "official_store_id": int(row["id"]),
        "official_station_id": row.get("station_id"),
        "official_point_status": row.get("point_status"),
    }


def write_csv(rows):
    fieldnames = list(dict.fromkeys(key for row in rows for key in row))
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    raw, query_count, capped_queries = asyncio.run(fetch_all())
    stores = sorted((normalize_store(row) for row in raw.values()), key=lambda x: (x["city"], x["district"], x["store_name"]))
    current = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    current = [row for row in current if row.get("brand") != BRAND]
    all_rows = current + stores
    for index, row in enumerate(all_rows, 1):
        row["n"] = index
    DATA_PATH.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(all_rows)

    needs_review = [row for row in stores if row["geocode_score"] < 100]
    audit = {
        "checked_at": date.today().isoformat(),
        "source": SOURCE_URL,
        "scope": "蝦皮官方查詢頁中支援買家取件且顯示中的服務點",
        "method": "分區網格查詢官方 API、以官方門市 ID 去重；每筆官方座標均為官方頁面 Google Maps 圖釘座標",
        "query_points": query_count,
        "queries_reaching_api_cap": capped_queries,
        "unique_store_count": len(stores),
        "active_count": sum(row["status_category"] == "現行營運中" for row in stores),
        "temporary_closed_count": sum(row["status_category"] == "暫停營運" for row in stores),
        "needs_manual_review_count": len(needs_review),
        "needs_manual_review": needs_review,
        "stores": stores,
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: audit[key] for key in ("query_points", "unique_store_count", "active_count", "temporary_closed_count", "needs_manual_review_count")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
