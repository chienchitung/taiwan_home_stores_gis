# -*- coding: utf-8 -*-
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_candidates = [
    os.path.join(BASE_DIR, 'data', 'taiwan_home_stores_status.json'),
    os.path.join(BASE_DIR, 'taiwan_home_stores_status.json'),
    '/Users/jackietung/taiwan_home_stores_gis/taiwan_home_stores_status.json',
    '/Users/jackietung/.gemini/antigravity/scratch/taiwan_home_stores_status.json'
]
json_path = next((p for p in json_candidates if os.path.exists(p)), json_candidates[0])
with open(json_path, 'r', encoding='utf-8') as f:
    stores = json.load(f)

import re

date_year_regex = re.compile(r'^(19\d\d|20\d\d)(?:-\d\d){0,2}$')

def assign_store_opened_year(s):
    """開幕年份只取有出處的 opened_date（YYYY / YYYY-MM / YYYY-MM-DD）。

    - 全聯福利中心：經濟部商工登記分公司核准設立日期（audit/sync_pxmart_stores.py）
    - 其他品牌：audit/store_opened_dates_verified.json 中有新聞／官方來源的日期
      （audit/apply_verified_opened_dates.py 寫入）
    查無可靠來源就回傳 None（前端顯示為未知、不列入時間軸），不推估、不從備註抓年份。
    """
    m = date_year_regex.match(str(s.get('opened_date') or '').strip())
    return int(m.group(1)) if m else None

dashboard_stores = [store for store in stores if not store.get('dashboard_excluded')]
for store in dashboard_stores:
    store['opened_year'] = assign_store_opened_year(store)
    # 開幕日期依據：全聯一律為商工登記；其他品牌由 apply_verified_opened_dates.py 寫入
    if store['opened_year']:
        store['opened_basis'] = '商工登記' if store.get('brand') == '全聯福利中心' else (store.get('opened_date_basis') or '新聞／官方')
    else:
        store['opened_basis'] = ''
    # 部分資料的座標是字串（例如 "25.010977"）；Leaflet 的 bounds.contains() 會把字串陣列
    # 誤判成範圍而無限遞迴，導致「只看地圖範圍內」當掉，因此統一轉成數字
    for key in ('lat', 'lng'):
        if isinstance(store.get(key), str):
            store[key] = float(store[key])

shopee_stores = [store for store in dashboard_stores if store.get('brand') == '蝦皮店到店']
pxmart_stores = [store for store in dashboard_stores if store.get('brand') == '全聯福利中心']
initial_stores = [store for store in dashboard_stores if store.get('brand') not in ('蝦皮店到店', '全聯福利中心')]
SHOPEE_DASHBOARD_FIELDS = {
    'n', 'brand', 'store_name', 'store_type', 'region', 'city', 'address',
    'status', 'note', 'district', 'channel_format', 'status_category', 'lat',
    'lng', 'clean_query', 'is_co_location', 'google_maps_url',
    'verification_status', 'official_store_id', 'location_role', 'core_store',
    'store_format', 'opened_date', 'opened_year', 'opened_basis'
}
shopee_stores = [
    {key: value for key, value in store.items() if key in SHOPEE_DASHBOARD_FIELDS}
    for store in shopee_stores
]
# 網頁沒有用到的欄位不打包，減少下載與解析量
UNUSED_FIELDS = {'google_maps_url', 'source_url', 'clean_name', 'coordinate_source',
                 'verification_status', 'geocode_score', 'location_role', 'core_store',
                 'is_co_location', 'opened_date', 'opened_date_basis', 'opened_date_source',
                 'address_floor_source'}
initial_stores = [{k: v for k, v in s.items() if k not in UNUSED_FIELDS} for s in initial_stores]
pxmart_stores = [{k: v for k, v in s.items() if k not in UNUSED_FIELDS} for s in pxmart_stores]
for s in pxmart_stores:
    s['_isCoLocation'] = False

# 150 公尺內是否有其他品牌：原本在每位使用者的瀏覽器裡兩兩比對，改成建置時算好
def _haversine_km(a_lat, a_lng, b_lat, b_lng):
    from math import radians, sin, cos, atan2, sqrt
    d_lat, d_lng = radians(b_lat - a_lat), radians(b_lng - a_lng)
    h = sin(d_lat / 2) ** 2 + cos(radians(a_lat)) * cos(radians(b_lat)) * sin(d_lng / 2) ** 2
    return 6371 * 2 * atan2(sqrt(h), sqrt(1 - h))
for s in initial_stores:
    s['_isCoLocation'] = any(
        o['n'] != s['n'] and o['brand'] != s['brand']
        and _haversine_km(s['lat'], s['lng'], o['lat'], o['lng']) <= 0.15
        for o in initial_stores
    )

STORES_JS = json.dumps(initial_stores, ensure_ascii=False, separators=(',', ':'))
SHOPEE_STORES_JS = json.dumps(shopee_stores, ensure_ascii=False, separators=(',', ':'))
PXMART_STORES_JS = json.dumps(pxmart_stores, ensure_ascii=False, separators=(',', ':'))
ACTIVE_STORE_COUNT = sum(
    1 for store in dashboard_stores if store.get('status_category') == '現行營運中'
)
DATA_UPDATED_DATE = '2026-10-04'


# ─── 前端程式 ───
# 畫面（src/index.html）、樣式（src/css/*.css）、互動（src/js/*.js）各自維護，
# 這裡只負責：依檔名順序合併成 assets/app.css、assets/app.js，並把內容雜湊當版本號寫進 index.html，
# 程式沒改時瀏覽器可直接用快取。src/js 依序合併成單一 script，執行順序與作用域和原本單檔相同。
import glob
import hashlib

SRC_DIR = os.path.join(BASE_DIR, "src")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def bundle(pattern):
    parts = []
    for path in sorted(glob.glob(os.path.join(SRC_DIR, pattern))):
        with open(path, encoding="utf-8") as f:
            parts.append(f.read())
    if not parts:
        raise SystemExit(f"找不到前端原始檔：src/{pattern}")
    return "".join(parts)


def write_asset(name, content):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    path = os.path.join(ASSETS_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated successfully: {path} ({len(content.encode('utf-8')):,} bytes)")
    return hashlib.sha1(content.encode("utf-8")).hexdigest()[:10]


APP_CSS_VERSION = write_asset("app.css", bundle("css/*.css"))
APP_JS_VERSION = write_asset("app.js", bundle("js/*.js"))
with open(os.path.join(SRC_DIR, "index.html"), encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()

# 門市資料獨立成檔案：瀏覽器可分開快取；內容雜湊當版本號，資料更新時網址會變、不會讀到舊快取
STORES_DATA_FILE = "window.ALL_STORES_DATA=" + STORES_JS + ";\n"
STORES_DATA_VERSION = hashlib.sha1(STORES_DATA_FILE.encode("utf-8")).hexdigest()[:10]
with open(os.path.join(BASE_DIR, "stores_data.js"), "w", encoding="utf-8") as f:
    f.write(STORES_DATA_FILE)
print(f"Generated successfully: {os.path.join(BASE_DIR, 'stores_data.js')} ({len(STORES_DATA_FILE.encode('utf-8')):,} bytes)")

HTML = (HTML_TEMPLATE
        .replace("APP_CSS_VERSION_PLACEHOLDER", APP_CSS_VERSION)
        .replace("APP_JS_VERSION_PLACEHOLDER", APP_JS_VERSION)
        .replace("STORES_DATA_VERSION_PLACEHOLDER", STORES_DATA_VERSION)
        .replace("ACTIVE_STORE_COUNT_PLACEHOLDER", str(ACTIVE_STORE_COUNT))
        .replace("DATA_UPDATED_DATE_PLACEHOLDER", DATA_UPDATED_DATE))
assert "PLACEHOLDER" not in HTML, "index.html 還有未替換的佔位字"

out_paths = [
    os.path.join(BASE_DIR, "index.html"),
]

for path in out_paths:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(HTML)
        print(f"Generated successfully: {path} ({len(HTML):,} bytes)")
    except Exception as e:
        print(f"Notice: skipped {path}: {e}")

data_paths = [
    os.path.join(BASE_DIR, "shopee_stores_data.js"),
]
SHOPEE_DATA_FILE = "window.SHOPEE_STORES=" + SHOPEE_STORES_JS + ";\n"
for path in data_paths:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(SHOPEE_DATA_FILE)
        print(f"Generated successfully: {path} ({len(SHOPEE_DATA_FILE):,} bytes)")
    except Exception as e:
        print(f"Notice: skipped {path}: {e}")

pxmart_data_paths = [
    os.path.join(BASE_DIR, "pxmart_stores_data.js"),
]
PXMART_DATA_FILE = "window.PXMART_STORES=" + PXMART_STORES_JS + ";\n"
for path in pxmart_data_paths:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(PXMART_DATA_FILE)
        print(f"Generated successfully: {path} ({len(PXMART_DATA_FILE):,} bytes)")
    except Exception as e:
        print(f"Notice: skipped {path}: {e}")
