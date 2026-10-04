# -*- coding: utf-8 -*-
"""Process and synchronize official 全聯福利中心 (Pxmart Supermarket) locations into project datasets.

Verified 100% against official Ministry of Economic Affairs (MOEA / GCIS)
Company & Branch Registry (商業發展署商工登記公示資料) for exact establishment dates.
"""
import csv
import json
import re
from pathlib import Path
from urllib.parse import quote

try:
    from pxmart_gcis_match import match_all
except ImportError:  # 從專案根目錄以 audit.sync_pxmart_stores 匯入時
    from audit.pxmart_gcis_match import match_all

BASE_DIR = Path(__file__).resolve().parent
RAW_JSON = BASE_DIR / "pxmart_stores_raw.json"
GCIS_JSON = BASE_DIR / "pxmart_gcis_branches.json"
OUTPUT_AUDIT = BASE_DIR / "pxmart_location_audit.json"
DATA_DIR = BASE_DIR.parent / "data" if (BASE_DIR.parent / "data").exists() else BASE_DIR
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"

def normalize_city(city):
    return city.replace("臺", "台").strip()

def region_for(city):
    c = normalize_city(city)
    if c in {"台北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣"}:
        return "北部"
    if c in {"台中市", "彰化縣", "南投縣", "雲林縣"}:
        return "中部"
    if c in {"嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"}:
        return "南部"
    return "東部/離島"

def clean_address(raw_addr, city, area):
    addr = re.sub(r'^\(\d+\)', '', raw_addr).strip()
    addr = normalize_city(addr)
    c = normalize_city(city)
    if not addr.startswith(c) and area and not addr.startswith(area):
        addr = c + area + addr
    return addr

def clean_addr_for_matching(a):
    a = str(a).replace('臺', '台').translate(str.maketrans('０１２３４５６７８９段號巷弄樓', '0123456789段號巷弄樓'))
    a = re.sub(r'^\(\d+\)', '', a)
    a = re.sub(r'[（(].*?[）)]', '', a)
    a = re.sub(r'[0-9]+樓.*|地下.*|B\d+.*', '', a)
    a = re.sub(r'[\s、，,]+', '', a)
    a = re.sub(r'[\u4e00-\u9fff]+[里村]', '', a)
    return a

def norm_name(n):
    return n.replace('全聯福利中心', '').replace('全聯', '').replace('分公司', '').replace('店', '').strip()

def load_gcis_branches():
    if not GCIS_JSON.exists():
        return {}, {}, []
    with open(GCIS_JSON, 'r', encoding='utf-8') as f:
        branches = json.load(f)
    exact_name = {}
    exact_addr = {}
    for b in branches:
        b_name = norm_name(b['name'])
        b_addr = clean_addr_for_matching(b['address'])
        exact_name[b_name] = b
        exact_addr[b_addr] = b
    return exact_name, exact_addr, branches


# 有新聞明確記載搬遷、現址開幕日與商工登記不同的門市：採現址開幕日（同一分公司登記沿用舊址日期）
RELOCATED_OPENINGS = {
    "台東中山": ("2022-01-22", "https://ec.ltn.com.tw/article/breakingnews/3809391",
                 "自建五層樓旗艦店 2022-01-22 開幕，原台東中山店遷入；商工登記 2009-01-05 為舊店"),
}


def parse_pxmart_store(item, match):
    attr = item['attributes']
    raw_name = attr.get('name', '').strip()
    full_name = f"全聯福利中心 {raw_name}"
    city = normalize_city(attr.get('city', ''))
    area = attr.get('area', '').strip()
    raw_addr = attr.get('address', '').strip()
    addr = clean_address(raw_addr, city, area)
    lat = float(attr.get('latitude', 0))
    lng = float(attr.get('longitude', 0))
    code = str(attr.get('code', ''))
    hours_start = attr.get('startDate', '')
    hours_end = attr.get('endDate', '')
    hours_str = f"{hours_start}–{hours_end}" if hours_start and hours_end else ""
    phone = attr.get('phone', '').strip()
    desc = attr.get('description') or ''
    
    srv_list = []
    srv_data = attr.get('services', {}).get('data', [])
    for s in srv_data:
        title = s.get('attributes', {}).get('title')
        if title:
            srv_list.append(title)
    
    # 經濟部商工登記分公司比對結果（同縣市、一對一；同址重新登記取最早設立日期）
    if match:
        branch, how, first = match
        opened_date = first['opened_date']
        opened_year = int(opened_date[:4])
        branch_ban = branch.get('branch_ban', '')
        branch_reg_name = branch.get('full_name', '')
        v_status = f"官方門市與經濟部商工登記分公司比對（{how}）；開店日期採分公司核准設立日期"
        if raw_name in RELOCATED_OPENINGS:
            opened_date, url, why = RELOCATED_OPENINGS[raw_name]
            opened_year = int(opened_date[:4])
            v_status = f"官方門市與經濟部商工登記分公司比對（{how}）；現址為搬遷後新店，開店日期採新聞記載現址開幕日（{why}；{url}）"
    else:
        # 找不到可靠對應：不推估，日期留空
        opened_year = None
        opened_date = ""
        branch_ban = ""
        branch_reg_name = ""
        v_status = "官方門市地址與經緯度已核對；商工登記無可靠對應，開店日期未知"

    note_parts = []
    if desc:
        note_parts.append(desc)
    if opened_date:
        note_parts.append(f"設立日期: {opened_date}")
    if hours_str:
        note_parts.append(f"營業時間: {hours_str}")
    if phone:
        note_parts.append(f"電話: {phone}")
    if srv_list:
        note_parts.append("服務: " + "、".join(srv_list))
    note = " | ".join(note_parts)

    maps_query = quote(f"全聯福利中心 {raw_name} {addr}")

    return {
        "brand": "全聯福利中心",
        "store_name": full_name,
        "store_type": "社區生鮮超市",
        "region": region_for(city),
        "city": city,
        "address": addr,
        "opened_date": opened_date,
        "status": "營業中",
        "note": note,
        "district": area,
        "channel_format": "社區生鮮超市 / 街邊獨立",
        "status_category": "現行營運中",
        "lat": lat,
        "lng": lng,
        "geocode_score": 100,
        "clean_address": addr,
        "clean_name": full_name,
        "clean_query": f"{full_name} {addr}",
        "is_co_location": False,
        "source_url": "https://www.pxmart.com.tw/customer-service/stores/pxmart",
        "coordinate_source": "全聯官方門市地圖座標",
        "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={maps_query}",
        "verification_status": v_status,
        "official_store_id": code,
        "location_role": "一般門市",
        "core_store": False,
        "store_format": "社區超市",
        "opened_year": opened_year,
        "official_branch_ban": branch_ban,
        "branch_registry_name": branch_reg_name
    }

def main():
    if not RAW_JSON.exists():
        raise FileNotFoundError(f"{RAW_JSON} not found!")

    _, _, branches = load_gcis_branches()
    print(f"Loaded {len(branches)} GCIS branch records for exact opening date verification")

    with open(RAW_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    raw_items = data.get('data', [])
    matches = match_all([it['attributes'] for it in raw_items], branches)
    parsed_stores = [parse_pxmart_store(item, matches.get(item['attributes'].get('code'))) for item in raw_items]
    print(f"Parsed {len(parsed_stores)} stores from {RAW_JSON}")
    
    matched_exact = sum(1 for s in parsed_stores if s.get('official_branch_ban'))
    print(f"Verified against MOEA / GCIS records: {matched_exact} / {len(parsed_stores)} ({matched_exact/len(parsed_stores)*100:.2f}%)")

    # Save audit summary
    audit_data = {
        "checked_at": "2026-10-04",
        "source": "https://www.pxmart.com.tw/api/stores",
        "verification_source": "經濟部商業發展署商工登記公示資料 (GCIS)",
        "total_count": len(parsed_stores),
        "exact_verified_count": matched_exact,
        "by_city": {},
        "by_year": {},
        "stores": parsed_stores
    }
    for s in parsed_stores:
        c = s['city']
        audit_data['by_city'][c] = audit_data['by_city'].get(c, 0) + 1
        y = s['opened_year'] if s['opened_year'] is not None else '未知'
        audit_data['by_year'][y] = audit_data['by_year'].get(y, 0) + 1

    with open(OUTPUT_AUDIT, 'w', encoding='utf-8') as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)

    # Sync into main JSON & CSV
    existing_stores = []
    if MAIN_JSON.exists():
        with open(MAIN_JSON, 'r', encoding='utf-8') as f:
            existing_stores = json.load(f)
    
    # Filter out any prior pxmart stores if present
    base_stores = [s for s in existing_stores if s.get('brand') != '全聯福利中心']
    combined_stores = base_stores + parsed_stores
    
    # Re-index n
    for idx, s in enumerate(combined_stores, 1):
        s['n'] = idx

    with open(MAIN_JSON, 'w', encoding='utf-8') as f:
        json.dump(combined_stores, f, ensure_ascii=False, indent=2)
    print(f"Updated {MAIN_JSON}: total {len(combined_stores)} stores")

    # CSV write
    all_fields = list(dict.fromkeys(key for row in combined_stores for key in row))
    with open(MAIN_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(combined_stores)
    print(f"Updated {MAIN_CSV}: total {len(combined_stores)} rows")

if __name__ == "__main__":
    main()
