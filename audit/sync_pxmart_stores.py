# -*- coding: utf-8 -*-
"""Process and synchronize official 全聯福利中心 (Pxmart Supermarket) locations into project datasets.

門市清單與座標來自全聯官方門市 API。開幕日期只列新聞、雜誌、官方或社群貼文可查證者
（audit/supermarket_news_openings.json、RELOCATED_OPENINGS），其餘留空。
經濟部商工登記分公司核准設立日不等於開幕日，只用來對應分公司，登記日留在 pxmart_location_audit.json 供參考。
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
NEWS_JSON = BASE_DIR / "supermarket_news_openings.json"
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


def load_news_openings(brand):
    """新聞／社群查得的開幕日期：{店名: 紀錄}"""
    if not NEWS_JSON.exists():
        return {}
    return {x["store_name"]: x for x in json.loads(NEWS_JSON.read_text(encoding="utf-8")) if x["brand"] == brand}


def parse_pxmart_store(item, match, news=None):
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
    
    # 經濟部商工登記分公司比對結果（同縣市、一對一）：只記分公司，登記日不當開幕日
    registry_date = ""
    if match:
        branch, how, first = match
        registry_date = first['opened_date']
        branch_ban = branch.get('branch_ban', '')
        branch_reg_name = branch.get('full_name', '')
    else:
        branch_ban = ""
        branch_reg_name = ""
    if raw_name in RELOCATED_OPENINGS:
        opened_date, src, why = RELOCATED_OPENINGS[raw_name]
        v_status = f"開幕日期依新聞（{why}）"
    elif news:
        opened_date, src = news['opened_date'], news['source_url']
        v_status = f"開幕日期依{news.get('source_title') or '新聞／社群'}"
    else:
        # 查無新聞、官方或社群來源：不推估，日期留空
        opened_date, src = "", ""
        v_status = "官方門市地址與經緯度已核對；查無可查證的開幕日期，未列出"
    opened_year = int(opened_date[:4]) if opened_date else None

    note_parts = []
    if desc:
        note_parts.append(desc)
    if hours_str:
        note_parts.append(f"營業時間: {hours_str}")
    if phone:
        note_parts.append(f"電話: {phone}")
    if srv_list:
        note_parts.append("服務: " + "、".join(srv_list))
    note = " | ".join(note_parts)

    maps_query = quote(f"全聯福利中心 {raw_name} {addr}")

    return registry_date, {
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
        "opened_date_basis": "新聞／官方" if opened_date else "",
        "opened_date_source": src,
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
    news = load_news_openings("全聯福利中心")
    parsed = [parse_pxmart_store(item, matches.get(item['attributes'].get('code')),
                                 news.get(f"全聯福利中心 {item['attributes'].get('name', '').strip()}"))
              for item in raw_items]
    parsed_stores = [p[1] for p in parsed]
    registry_dates = {p[1]['store_name']: p[0] for p in parsed if p[0]}
    print(f"Parsed {len(parsed_stores)} stores from {RAW_JSON}")
    
    matched_exact = sum(1 for s in parsed_stores if s.get('official_branch_ban'))
    print(f"Matched to MOEA / GCIS branches: {matched_exact} / {len(parsed_stores)}")
    print(f"Opening dates listed (news/social): {sum(1 for s in parsed_stores if s['opened_date'])}")

    # Save audit summary
    audit_data = {
        "checked_at": "2026-10-04",
        "source": "https://www.pxmart.com.tw/api/stores",
        "verification_source": "經濟部商業發展署商工登記公示資料 (GCIS)",
        "total_count": len(parsed_stores),
        "exact_verified_count": matched_exact,
        "opened_date_rule": "只列新聞、雜誌、官方或社群可查證的開幕日期；商工登記核准設立日不等於開幕日，僅供參考",
        "registry_estab_dates_reference_only": registry_dates,
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
    
    # 以本次結果取代既有全聯門市，位置與編號 n 沿用（依官方門市代碼），新門市接在最後的編號
    old_n = {s.get('official_store_id'): s.get('n') for s in existing_stores if s.get('brand') == '全聯福利中心'}
    next_n = max([int(s.get('n') or 0) for s in existing_stores] or [0]) + 1
    for s in parsed_stores:
        if old_n.get(s['official_store_id']) is not None:
            s['n'] = old_n[s['official_store_id']]
        else:
            s['n'], next_n = next_n, next_n + 1
    combined_stores, inserted = [], False
    for s in existing_stores:
        if s.get('brand') != '全聯福利中心':
            combined_stores.append(s)
        elif not inserted:
            combined_stores.extend(parsed_stores)
            inserted = True
    if not inserted:
        combined_stores.extend(parsed_stores)

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
