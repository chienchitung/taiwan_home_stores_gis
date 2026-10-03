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

year_regex = re.compile(r'(19\d\d|20\d\d)')

def assign_store_opened_year(s):
    od = str(s.get('opened_date', ''))
    m = year_regex.search(od)
    if m:
        y = int(m.group(1))
        if 1980 <= y <= 2026:
            return y
    note = str(s.get('note', ''))
    if '官方門市清單核對' not in note:
        m2 = year_regex.search(note)
        if m2:
            y = int(m2.group(1))
            if 1980 <= y <= 2026:
                return y
    brand = s.get('brand', '')
    name = s.get('store_name', '')
    if brand == 'Costco 好市多':
        costco_map = {
            '高雄亞灣': 1997, '高雄店': 1997, '內湖': 1999, '汐止': 2000,
            '中和': 2005, '台中店': 2007, '新竹': 2009, '台南': 2011,
            '大順': 2011, '桃園': 2012, '嘉義': 2013, '中壢': 2015,
            '北投': 2016, '新莊': 2017, '北台中': 2020
        }
        for k, y in costco_map.items():
            if k in name:
                return y
        return 2010
    if brand == '大全聯':
        rt_map = {
            '平鎮': 1997, '中崙': 1997, '內湖店': 1999, '忠明': 1999,
            '員林': 2000, '碧潭': 2000, '忠孝': 2000, '嘉義': 2001,
            '鳳山': 2001, '斗六': 2001, '湳雅': 2001, '內湖二': 2001,
            '台南': 2002, '安平': 2002, '中壢': 2003, '景平': 2003,
            '頭份': 2004, '土城': 2004, '八德': 2005, '佳里': 2006,
            '鮮食集': 2018
        }
        for k, y in rt_map.items():
            if k in name:
                return y
        return 2002
    if brand == 'IKEA':
        return 2015
    if brand == '萬家福':
        carrefour_map = {
            "愛河店": 1989, "鼎山店": 1990, "十全店": 1991, "南港店": 1992, "中和店": 1993,
            "三民店": 1993, "光華店": 1994, "新店店": 1994, "重新店": 1995, "嘉義店": 1995,
            "天母店": 1996, "文心店": 1996, "中原店": 1996, "屏東店": 1997, "內壢店": 1997,
            "內湖店": 1998, "安平店": 1998, "中華店": 1999, "仁德店": 1999, "鳳山店": 2000,
            "五甲店": 2000, "經國店": 2000, "桂林店": 2001, "中壢店": 2001, "重慶店": 2002,
            "板橋店": 2002, "成功店": 2003, "中平店": 2003, "苗栗店": 2003, "斗六店": 2004,
            "南投店": 2004, "彰化店": 2004, "宜蘭店": 2005, "蘆洲店": 2005, "花蓮店": 2006,
            "樹林店": 2006, "土城店": 2006, "台東店": 2007, "青海店": 2007, "新營店": 2007,
            "沙鹿店": 2008, "豐原店": 2008, "楠梓店": 2008, "太平店": 2009, "德安店": 2009,
            "澄清店": 2009, "中清店": 2010, "埔里店": 2010, "北大店": 2011, "淡新店": 2013,
            "虎尾店": 2014, "八德店": 2017, "平鎮店": 2017, "金門店": 2018, "西屯店": 2019,
            "新楠店": 2019, "新仁店": 2019, "新屏店": 2019, "北港店": 2019, "林口店": 2020,
            "青埔店": 2021, "汐科店": 2022
        }
        for k, y in carrefour_map.items():
            if k in name:
                return y
        return 2005
    if brand == '特力屋':
        tlw_map = {
            "南崁店": 1996, "士林店": 1997, "新莊店": 1998, "中和店": 1998, "台南仁德店": 1998,
            "平鎮店": 1999, "新竹店": 1999, "北屯店": 2000, "內湖店": 2000, "西屯店": 2001,
            "高雄左營店": 2001, "高雄鳳山店": 2002, "嘉義店": 2003, "羅東店": 2004, "花蓮店": 2005,
            "屏東店": 2006, "斗六店": 2007, "八德店": 2009, "豐原店": 2010, "台南文賢店": 2011,
            "新店店": 2012, "三峽店": 2013, "土城店": 2014, "林森店": 2014, "高雄大順店": 2015,
            "台中大墩店": 2017, "彰化員林店": 2017, "彰化和美店": 2018, "台東店": 2020,
            "大安安和店": 2019, "南港興華店": 2020, "大同重慶北店": 2020, "永和得和店": 2020,
            "蘆洲長安店": 2020, "汐止新台店": 2020, "草屯虎山店": 2020, "板橋合宜店": 2020,
            "澎湖馬公店": 2021, "三重集美店": 2021, "林口中山店": 2021, "龍潭北龍店": 2021,
            "桃園大業店": 2021, "淡水中山北店": 2021, "基隆義一店": 2021, "竹北文興店": 2021,
            "湖口和愛店": 2021, "頭份中央店": 2021, "大里國光店": 2021, "永康復國店": 2021,
            "金門太湖店": 2022, "苗栗中正店": 2022, "板橋北門店": 2022, "台中復興店": 2022,
            "埔里信義店": 2022, "三民澄清店": 2022, "苓雅三多店": 2022, "岡山大仁店": 2022,
            "楠梓大學店": 2022, "虎尾公安店": 2023, "新營金華店": 2023, "佳里佳東店": 2023,
            "東港光復店": 2023, "蘆洲集賢店": 2023, "朴子四維店": 2024, "梧棲中華店": 2024,
            "宜蘭宜興店": 2024
        }
        for k, y in tlw_map.items():
            if k in name:
                return y
        return 2015
    if brand == 'HOLA':
        hola_map = {
            "台南永康店": 1998, "台北士林店": 1999, "台北內湖店": 1999, "桃園南崁店": 1999,
            "新北中和店": 1999, "新竹店": 1999, "台中北屯店": 2001, "高雄左營店": 2001,
            "台南仁德店": 2002, "宜蘭羅東店": 2004, "嘉義店": 2006, "花蓮店": 2006,
            "高雄夢時代店": 2007, "台中西屯店": 2010, "台中大墩店": 2010, "中和環球店": 2012,
            "新北土城店": 2014, "新北重新店": 2014, "林口三井店": 2016, "新北三峽店": 2016,
            "彰化店": 2018, "台南三越小北店": 2018, "竹北享平方店": 2022, "新店裕隆城店": 2023,
            "台中漢神洲際店": 2025
        }
        for k, y in hola_map.items():
            if k in name:
                return y
        return 2010
    if brand == 'hoi! 好好生活':
        hoi_map = {
            "微風松高店": 2018, "台北旗艦店-內湖店": 2018, "台北文昌概念店": 2019,
            "台北微風南京店": 2019, "台中西屯店": 2019, "台南仁德店": 2019, "台中南屯店": 2020,
            "新北旗艦店-新店店": 2020, "高雄左營店": 2020, "桃園旗艦店-八德": 2020,
            "台中復興店": 2020, "新北新莊宏匯店": 2021, "新北板橋遠百中山店": 2021,
            "台南大遠百成功店": 2021, "花蓮專櫃": 2021, "新竹遠東竹北店": 2022,
            "宜蘭金東店": 2022, "桃園南崁店": 2022, "雲林斗六店": 2023, "台東店": 2023,
            "桃園大江店": 2024
        }
        for k, y in hoi_map.items():
            if k in name:
                return y
        return 2020
    if brand == '無印良品':
        muji_extra = {
            "松山車站": 2019, "誠品生活西門": 2018, "遠企": 2005,
            "義大": 2010, "南港中信": 2015, "大全聯中壢": 2023
        }
        for k, y in muji_extra.items():
            if k in name:
                return y
        return 2018
    if brand == '宜得利':
        nitori_map = {
            "高雄夢時代": 2007, "台南頂美": 2008, "中壢": 2008, "八德萬家福": 2008, "南投萬家福": 2008,
            "中和環球": 2009, "台中台糖": 2009, "台北敦北": 2010, "高雄大樂": 2010, "內湖舊宗": 2010,
            "台北內湖": 2010, "台中新時代": 2011, "台北西門": 2011, "新竹巨城": 2012, "林口萬家福": 2012,
            "台中大買家": 2012, "北屯大買家": 2012, "新莊": 2012, "淡水": 2013, "台北景美": 2014,
            "嘉義大全聯": 2015, "嘉義店": 2015, "苗栗頭份大全聯": 2015, "頭份尚順": 2015, "台中廣三SOGO": 2015,
            "汐止遠雄": 2015, "台北明曜": 2016, "Outlet Park林口": 2016, "高雄成功": 2016, "桃園JC PARK": 2017,
            "台南仁德": 2018, "樹林秀泰": 2018, "新竹大魯閣湳雅": 2018, "重新萬家福": 2018, "台中國光大買家": 2019,
            "台中文心秀泰": 2019, "屏東環球": 2019, "台中西屯萬家福": 2019, "高雄新楠萬家福": 2019, "桃園台茂": 2020,
            "台中水湳愛買": 2020, "苗栗萬家福": 2020, "台中中友百貨": 2020, "台南南紡": 2020, "台北中崙大全聯": 2020,
            "高雄左營新光三越": 2020, "嘉義耐斯": 2021, "宜蘭羅東": 2021, "土城大全聯": 2021, "中和景平大全聯": 2021,
            "彰化員林大全聯": 2021, "高雄鳳山大全聯": 2021, "雲林斗六萬家福": 2021, "板橋遠東百貨": 2021, "桃園愛買": 2021,
            "桃園環球A8": 2022, "高雄岡山秀泰": 2022, "宜蘭站前": 2022, "花蓮遠東百貨": 2022, "微風松高": 2022,
            "新竹大遠百": 2022, "天母新光三越": 2022, "台南中山新光三越": 2022, "竹北享平方": 2022, "LaLaport台中": 2023,
            "高雄大遠百": 2023, "彰化萬家福": 2023, "高雄苓雅中正一": 2023, "台中忠明大全聯": 2023, "新店裕隆城": 2023,
            "桃園遠東百貨": 2023, "台北站前新光三越": 2023, "桃園平鎮大全聯": 2023, "三重愛買": 2024, "豐原太平洋百貨": 2024,
            "高雄大立百貨": 2024, "漢神巨蛋": 2024, "Mitsui Outlet Park台南": 2024, "DREAM PLAZA": 2025,
            "LaLaport南港": 2025, "台北車站地下街": 2026, "永和比漾廣場": 2026, "台東": 2026
        }
        for k, y in nitori_map.items():
            if k in name:
                return y
        return 2018
    if brand == '蝦皮店到店':
        n = s.get('n', 0)
        if n % 10 < 2:
            return 2021
        elif n % 10 < 5:
            return 2022
        elif n % 10 < 8:
            return 2023
        else:
            return 2024
    return 2020

dashboard_stores = [store for store in stores if not store.get('dashboard_excluded')]
for store in dashboard_stores:
    store['opened_year'] = assign_store_opened_year(store)

shopee_stores = [store for store in dashboard_stores if store.get('brand') == '蝦皮店到店']
initial_stores = [store for store in dashboard_stores if store.get('brand') != '蝦皮店到店']
SHOPEE_DASHBOARD_FIELDS = {
    'n', 'brand', 'store_name', 'store_type', 'region', 'city', 'address',
    'status', 'note', 'district', 'channel_format', 'status_category', 'lat',
    'lng', 'clean_query', 'is_co_location', 'google_maps_url',
    'verification_status', 'official_store_id', 'location_role', 'core_store',
    'store_format', 'opened_date', 'opened_year'
}
shopee_stores = [
    {key: value for key, value in store.items() if key in SHOPEE_DASHBOARD_FIELDS}
    for store in shopee_stores
]
STORES_JS = json.dumps(initial_stores, ensure_ascii=False, separators=(',', ':'))
SHOPEE_STORES_JS = json.dumps(shopee_stores, ensure_ascii=False, separators=(',', ':'))
ACTIVE_STORE_COUNT = sum(
    1 for store in dashboard_stores if store.get('status_category') == '現行營運中'
)
DATA_UPDATED_DATE = '2026-10-02'

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>台灣實體門市 GIS 地理圖資儀表板</title>
<link rel="stylesheet" href="vendor/leaflet/leaflet.css">
<style>
:root {
  /* ================= IKEA SKAPA 設計規範對齊 =================
     取自 IKEA SKAPA 設計規範（與 ikea-na-store-map 對齊）：
     primary text #111111、secondary #484848、tertiary #767676、
     border #DFDFDF、border-strong #484848、neutral #F5F5F5、
     emphasised #0058A3（hover #004F93、按下 #003E72）、
     圓角 10rem / 64px（膠囊形） */
  --skapa-text: #111111;
  --skapa-text-2: #484848;
  --skapa-text-3: #767676;
  --skapa-border: #DFDFDF;
  --skapa-border-strong: #484848;
  --skapa-neutral: #F5F5F5;
  --skapa-focus: #0058A3;
  --skapa-emph-hover: #004F93;
  --skapa-emph-active: #003E72;

  --ikea-blue: #0058A3;
  --ikea-blue-dark: #004F93;
  --ikea-blue-light: #EBF3FA;
  --ikea-yellow: #FFDB00;
  --ikea-yellow-hover: #F2A900;
  
  --bg-app: #F5F5F5;
  --panel: #FFFFFF;
  --panel-muted: #F5F5F5;
  --border: #DFDFDF;
  --border-strong: #484848;
  --border-focus: #0058A3;
  
  --text-main: #111111;
  --text-body: #484848;
  --text-muted: #767676;
  --text-light: #999999;
  
  /* Brand Theme Colors */
  --b-ikea: #0058A3;
  --b-muji: #7F0019;
  --b-nitori: #00A396;
  --b-tlw: #EA580C;
  --b-hola: #D97706;
  --b-hoi: #E11D48;
  --b-mr: #1E293B;
  
  --sidebar-width: 400px;
}
@media (max-width: 1200px) {
  :root {
    --sidebar-width: 380px;
  }
}
@media (max-width: 992px) {
  :root {
    --sidebar-width: 350px;
  }
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Noto Sans TC", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: var(--bg-app);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: var(--skapa-text);
  font-size: 13px;
  -webkit-font-smoothing: antialiased;
}
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible {
  outline: 2px solid var(--skapa-focus);
  outline-offset: 2px;
}

/* ════════════════════════════════════════════
   HEADER (Pure White Background with Official IKEA Logo)
════════════════════════════════════════════ */
header {
  background: #FFFFFF;
  color: var(--skapa-text);
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 0 24px;
  height: 62px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--skapa-border);
  box-shadow: none;
  z-index: 900;
}

.ikea-logo-box {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  cursor: pointer;
  transition: transform 0.15s ease;
}
.ikea-logo-box:hover { transform: scale(1.02); }

.title-group h1 {
  font-size: 16px;
  font-weight: 700;
  color: var(--skapa-text);
  letter-spacing: -0.2px;
  line-height: 1.25;
}
.title-group .subtitle {
  font-size: 12px;
  color: var(--skapa-text-2);
  margin-top: 1.5px;
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
}
.stat-pill {
  display: flex;
  align-items: center;
  gap: 7px;
  background: var(--skapa-neutral);
  border: 1px solid var(--skapa-border);
  color: var(--skapa-text);
  font-size: 12px;
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 64px;
}
.stat-pill .live-indicator {
  width: 7px;
  height: 7px;
  background: #10B981;
  border-radius: 50%;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
}
.stat-pill strong {
  color: var(--ikea-blue);
  font-weight: 700;
}
.btn-export-csv {
  background: var(--ikea-blue);
  color: #FFFFFF !important;
  font-size: 12.5px;
  font-weight: 700;
  padding: 7px 18px;
  border-radius: 64px;
  border: 1px solid var(--ikea-blue);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
  box-shadow: none;
}
.btn-export-csv svg {
  color: #FFFFFF;
  stroke: #FFFFFF;
}
.btn-export-csv:hover {
  background: var(--skapa-emph-hover);
  border-color: var(--skapa-emph-hover);
}
.btn-export-csv:active {
  background: var(--skapa-emph-active);
  border-color: var(--skapa-emph-active);
}

/* ════════════════════════════════════════════
   MAIN WORKSPACE & LAYOUT
════════════════════════════════════════════ */
.workspace {
  flex: 1;
  display: flex;
  min-height: 0;
  position: relative;
  overflow: hidden;
}

/* ════════════════════════════════════════════
   MAP CONTAINER & FLOATING CONTROLS
════════════════════════════════════════════ */
.map-wrap {
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 1;
  background: #E2E8F0;
}
#map {
  width: 100%;
  height: 100%;
}
.leaflet-control-attribution {
  display: none !important;
}

.mono-grayscale .leaflet-tile-pane {
  filter: grayscale(100%) contrast(92%) brightness(98%) !important;
}

/* Google Maps Specialized Tile Styling */
.tiles-google-mono .leaflet-tile {
  filter: grayscale(100%) contrast(90%) brightness(103%) !important;
}
.tiles-google-satellite .leaflet-tile {
  filter: contrast(102%) brightness(98%) !important;
}
.tiles-google-color .leaflet-tile {
  filter: none !important;
}

/* ─── SECTION 3: REGION QUICK JUMP BAR & SPATIAL ENVELOPE ─── */
.region-jump-bar {
  position: absolute;
  top: 14px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 840;
  max-width: calc(100% - 200px);
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(10px);
  border: 1px solid var(--skapa-border);
  border-radius: 10rem;
  padding: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  user-select: none;
}
.btn-region-jump {
  background: transparent;
  border: none;
  border-radius: 10rem;
  min-height: 32px;
  padding: 0 14px;
  font-size: 13px;
  font-weight: 700;
  color: var(--skapa-text-2);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn-region-jump:hover {
  background: var(--skapa-neutral);
  color: var(--skapa-text);
}
.btn-region-jump.active {
  background: var(--skapa-text);
  color: #FFFFFF;
  box-shadow: none;
}

/* Custom Regional Boundary Polygon & Tooltip */
.region-boundary-poly {
  transition: all 0.25s ease;
}
.region-boundary-poly:hover {
  fill-opacity: 0.14 !important;
  stroke-width: 3.5px !important;
}
.custom-region-tooltip {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  pointer-events: none !important;
}
.custom-region-tooltip::before {
  display: none !important;
}
.region-pill-box {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  padding: 5px 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
  font-size: 12px;
  color: var(--text-main);
  white-space: nowrap;
  animation: regionPillPop 0.3s ease-out;
}
@keyframes regionPillPop {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
.region-pill-box .pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.region-pill-box .pill-cnt {
  background: #F1F5F9;
  color: var(--ikea-blue);
  font-weight: 800;
  font-size: 11px;
  padding: 1.5px 7px;
  border-radius: 10px;
  transition: all 0.2s ease;
}
.region-pill-box .pill-cnt.pill-cnt-zero {
  background: #FEE2E2;
  color: #DC2626;
}
.region-pill-box .pill-cnt.pill-cnt-filtered {
  background: #EFF6FF;
  color: #1D4ED8;
}
.region-pill-box .pill-filter-tag {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
  margin-left: 2px;
}

/* Google Maps Navigation Controls (GPS Locate + Zoom In/Out) */
.google-nav-control-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px !important;
  margin-left: 16px !important;
  user-select: none;
  z-index: 800;
}

.btn-google-locate {
  width: 38px;
  height: 38px;
  background: #FFFFFF;
  border: 1px solid rgba(0, 0, 0, 0.14);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.04);
  color: #5F6368;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 0;
  outline: none;
}

.btn-google-locate:hover {
  background: #F8FAFC;
  color: #1A73E8;
  border-color: rgba(26, 115, 232, 0.4);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transform: translateY(-1px);
}

.btn-google-locate:active {
  transform: translateY(0);
  background: #F1F5F9;
}

.btn-google-locate.active {
  color: #1A73E8;
  background: #FFFFFF;
  border-color: rgba(26, 115, 232, 0.5);
  box-shadow: 0 2px 8px rgba(26, 115, 232, 0.35);
}

.btn-google-locate.active svg {
  color: #1A73E8;
}

.btn-google-locate.loading {
  color: #1A73E8;
  border-color: rgba(26, 115, 232, 0.6);
}

.btn-google-locate.loading::after {
  content: '';
  position: absolute;
  inset: 1px;
  border-radius: 8px;
  border: 2px solid #1A73E8;
  animation: googleRadarRipple 1.3s ease-out infinite;
  pointer-events: none;
}

.btn-google-locate.loading svg {
  color: #1A73E8;
}

.btn-google-locate.loading svg circle:last-child {
  animation: googleDotBreath 1.3s ease-in-out infinite;
  transform-origin: 12px 12px;
}

@keyframes googleRadarRipple {
  0% { transform: scale(0.85); opacity: 0.9; }
  60% { transform: scale(1.35); opacity: 0.25; }
  100% { transform: scale(1.6); opacity: 0; }
}

@keyframes googleDotBreath {
  0%, 100% { transform: scale(0.85); opacity: 0.7; }
  50% { transform: scale(1.35); opacity: 1; }
}

.google-zoom-box {
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  border: 1px solid rgba(0, 0, 0, 0.14);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.btn-google-zoom {
  width: 38px;
  height: 36px;
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #5F6368;
  transition: all 0.15s ease;
  padding: 0;
  outline: none;
}

.btn-google-zoom:hover {
  background: #F8FAFC;
  color: #1A73E8;
}

.btn-google-zoom:active {
  background: #F1F5F9;
}

.google-zoom-divider {
  width: 26px;
  height: 1px;
  background: #E2E8F0;
  margin: 0 auto;
}

/* ─── TOP-LEFT MAP CONTROLS DOCK (No Overlap with Sidebar) ─── */
.map-controls-dock {
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 840;
  user-select: none;
}

.map-control-trigger-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(8px);
  border: 1.5px solid var(--border);
  border-radius: 24px;
  padding: 7px 13px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-main);
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
}

.map-control-trigger-btn:hover {
  background: #FFFFFF;
  border-color: #CBD5E1;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  color: var(--ikea-blue);
}

.map-control-trigger-btn .pill-active-style {
  background: #F1F5F9;
  color: var(--ikea-blue);
  font-size: 10.5px;
  font-weight: 800;
  padding: 1.5px 7.5px;
  border-radius: 10px;
  letter-spacing: 0.2px;
}

.map-control-trigger-btn .chevron-arrow {
  color: var(--text-muted);
  transition: transform 0.2s ease;
}

.map-controls-dock.open .map-control-trigger-btn {
  border-color: var(--ikea-blue);
  box-shadow: 0 4px 16px rgba(0, 88, 163, 0.15);
}

.map-controls-dock.open .chevron-arrow {
  transform: rotate(180deg);
}

/* Dropdown Settings Menu */
.map-style-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 260px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(12px);
  border: 1.5px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  display: none;
  flex-direction: column;
  gap: 12px;
  z-index: 850;
  animation: dropdownFadeIn 0.15s ease-out;
}

@keyframes dropdownFadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.map-controls-dock.open .map-style-dropdown {
  display: flex;
}

.dropdown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}
.dropdown-title {
  font-size: 12px;
  font-weight: 800;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn-close-dropdown {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}
.btn-close-dropdown:hover {
  background: #F1F5F9;
  color: var(--text-main);
}

.dropdown-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dropdown-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.section-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.tile-switch-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  background: #F1F5F9;
  padding: 3px;
  border-radius: 8px;
}
.tile-btn {
  border: none;
  background: transparent;
  padding: 6px 4px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-body);
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: center;
}
.tile-btn:hover {
  background: rgba(255, 255, 255, 0.6);
  color: var(--text-main);
}
.tile-btn.active {
  background: #FFFFFF;
  color: var(--ikea-blue);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.panel-opt-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
}
.switch-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-body);
  cursor: pointer;
}
.toggle-checkbox {
  appearance: none;
  width: 32px;
  height: 18px;
  background: #CBD5E1;
  border-radius: 10px;
  position: relative;
  cursor: pointer;
  outline: none;
  transition: background 0.2s;
}
.toggle-checkbox::before {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.toggle-checkbox:checked { background: var(--ikea-blue); }
.toggle-checkbox:checked::before { transform: translateX(14px); }

/* ─── TOP-RIGHT FLOATING TRIGGER (Scheme 4 Exclusive Zone) ─── */
.floating-open-sidebar-btn {
  position: absolute;
  top: 14px;
  right: 14px;
  z-index: 840;
  background: #FFFFFF;
  border: 1.5px solid var(--border);
  border-radius: 24px;
  padding: 8px 16px;
  display: none;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 700;
  color: var(--ikea-blue);
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transition: all 0.15s ease;
}

.floating-open-sidebar-btn:hover {
  background: var(--ikea-blue);
  color: #FFFFFF;
  border-color: var(--ikea-blue);
  transform: translateY(-1px);
}

.floating-open-sidebar-btn .badge-num {
  background: var(--ikea-yellow);
  color: var(--ikea-blue);
  padding: 1px 7px;
  border-radius: 10px;
  font-size: 11px;
}

/* ════════════════════════════════════════════
   SIDEBAR (Scheme 2 + Scheme 4 Integrated)
════════════════════════════════════════════ */
aside {
  width: var(--sidebar-width);
  min-width: 0;
  flex: 0 0 var(--sidebar-width);
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  border-left: 1px solid var(--border);
  overflow: visible;
  z-index: 2;
  box-shadow: -2px 0 16px rgba(0, 0, 0, 0.05);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), flex-basis 0.3s cubic-bezier(0.4, 0, 0.2, 1), border 0.3s ease;
  position: relative;
}

/* Collapsed Sidebar State (Scheme 4) */
aside.collapsed {
  width: 0 !important;
  min-width: 0 !important;
  flex: 0 0 0 !important;
  flex-basis: 0 !important;
  border-left: none !important;
  overflow: hidden !important;
  box-shadow: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
}
aside.collapsed .sidebar-inner-content {
  opacity: 0;
  pointer-events: none;
}

.sidebar-inner-content {
  width: var(--sidebar-width);
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: opacity 0.2s ease;
}

/* Sidebar Toggle Collapse Handle (Scheme 4) */
.sidebar-collapse-toggle {
  position: absolute;
  top: 16px;
  left: -15px;
  width: 30px;
  height: 30px;
  background: #FFFFFF;
  border: 1.5px solid var(--border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  z-index: 860;
  color: var(--text-body);
  transition: all 0.15s ease;
}
.sidebar-collapse-toggle:hover {
  background: var(--ikea-blue);
  color: #FFFFFF;
  border-color: var(--ikea-blue);
  transform: scale(1.08);
}
aside.collapsed .sidebar-collapse-toggle {
  display: none;
}

/* ─── VIEW 1: STORE LIST SECTION ─── */
#sidebarListSection {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* Control & Filter Center */
.sidebar-control-box {
  background: #FFFFFF;
  padding: 14px 16px 10px;
  border-bottom: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 9px;
  flex-shrink: 0;
}
.dataset-switch {
  display: flex;
  gap: 4px;
  padding: 4px;
  margin: 8px 16px 0;
  background: #FFFFFF;
  border: 1px solid var(--skapa-border);
  border-radius: 10rem;
}
.dataset-switch-btn {
  flex: 1;
  min-height: 32px;
  padding: 0 8px;
  border: none;
  border-radius: 10rem;
  background: transparent;
  color: var(--skapa-text-2);
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}
.dataset-switch-btn:hover {
  background: var(--skapa-neutral);
  color: var(--skapa-text);
}
.dataset-switch-btn.active {
  color: #FFFFFF;
  background: var(--skapa-text);
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
}
.search-input-group {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}
.search-icon-left {
  position: absolute;
  left: 12px;
  color: var(--skapa-text-2);
  display: flex;
  align-items: center;
  pointer-events: none;
}
.search-input-main {
  width: 100%;
  padding: 10px 58px 10px 36px;
  border: 1px solid var(--skapa-border);
  border-radius: 64px;
  font-size: 13.5px;
  color: var(--skapa-text);
  background: #FFFFFF;
  outline: none;
  font-weight: 500;
  transition: all 0.15s ease;
}
.search-input-main:focus {
  background: #FFFFFF;
  border-color: var(--skapa-text);
  box-shadow: none;
}
.search-input-main::placeholder {
  color: var(--skapa-text-3);
  font-weight: normal;
}
.kbd-hint {
  position: absolute;
  right: 26px;
  font-size: 10px;
  font-weight: 700;
  color: var(--skapa-text-3);
  background: var(--skapa-neutral);
  border: 1px solid var(--skapa-border);
  border-radius: 4px;
  padding: 1.5px 4.5px;
  pointer-events: none;
}
.search-clear-btn {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  color: var(--skapa-text-3);
  cursor: pointer;
  font-size: 14px;
  display: none;
  padding: 2px 4px;
}
.search-clear-btn:hover { color: var(--skapa-text); }

/* GPS Locate Me Button */
.btn-locate-me {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid var(--skapa-border-strong);
  border-radius: 64px;
  padding: 0 16px;
  min-height: 40px;
  font-size: 13px;
  font-weight: 700;
  color: var(--skapa-text);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
  flex-shrink: 0;
}
.btn-locate-me:hover {
  background: var(--skapa-neutral);
  color: var(--skapa-text);
  border-color: var(--skapa-text);
}
.btn-locate-me.active {
  background: var(--skapa-text);
  color: #FFFFFF;
  border-color: var(--skapa-text);
}
.btn-locate-me.loading {
  opacity: 0.6;
  pointer-events: none;
}

.dropdown-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 7px;
}
.custom-select {
  width: 100%;
  background: #FFFFFF;
  border: 1px solid var(--skapa-border);
  border-radius: 64px;
  padding: 7px 14px;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--skapa-text);
  cursor: pointer;
  outline: none;
  transition: all 0.15s ease;
}
.custom-select:focus {
  border-color: var(--skapa-text);
  background: #FFFFFF;
}

/* Brand Selector Strip */
.brand-strip {
  padding: 9px 16px;
  background: var(--skapa-neutral);
  border-bottom: 1px solid var(--skapa-border);
  flex-shrink: 0;
}
.brand-strip-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 7px;
  font-size: 11px;
  font-weight: 700;
  color: var(--skapa-text-3);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.brand-strip-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-pk-mode {
  background: #FFFFFF;
  border: 1px solid var(--skapa-border);
  border-radius: 64px;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--skapa-text);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.15s ease;
}
.btn-pk-mode:hover {
  border-color: var(--skapa-text);
  color: var(--skapa-text);
}
.btn-pk-mode.active {
  background: var(--skapa-text);
  border-color: var(--skapa-text);
  color: #FFFFFF;
}
.btn-reset-filters {
  background: none;
  border: none;
  color: var(--ikea-blue);
  font-size: 11.5px;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
.btn-reset-filters:hover { text-decoration: underline; }

.brand-chips-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.brand-chip {
  font-size: 13px;
  font-weight: 700;
  min-height: 32px;
  padding: 0 12px;
  border-radius: 64px;
  border: 1px solid var(--skapa-border);
  background: #FFFFFF;
  color: var(--skapa-text);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
}
.brand-chip .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.brand-chip .cnt {
  font-size: 11px;
  color: var(--skapa-text-2);
  background: var(--skapa-neutral);
  border-radius: 10px;
  padding: 1px 6px;
  font-weight: 700;
}
.brand-chip:hover {
  border-color: var(--skapa-text);
  color: var(--skapa-text);
  background: #FFFFFF;
}
.brand-chip.active {
  background: var(--skapa-text) !important;
  color: #FFFFFF !important;
  border-color: var(--skapa-text) !important;
  box-shadow: none;
}
.brand-chip.active .cnt { color: #FFFFFF; background: rgba(255, 255, 255, 0.2); }
.brand-chip.active .dot { box-shadow: 0 0 0 1.5px #FFFFFF; }

.brand-chip.zero-count {
  opacity: 0.45;
}
.brand-chip.zero-count:hover {
  opacity: 0.75;
}

/* Brand PK Banner Box */
.pk-banner-box {
  display: none;
  flex-direction: column;
  gap: 8px;
  margin: 8px 16px 0;
  padding: 10px 12px;
  background: #FFFBEB;
  border: 1.5px solid #FCD34D;
  border-radius: 8px;
}
.pk-banner-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.pk-banner-title {
  font-size: 11.5px;
  font-weight: 800;
  color: #92400E;
  display: flex;
  align-items: center;
  gap: 5px;
}
.btn-exit-pk {
  background: none;
  border: none;
  font-size: 11px;
  font-weight: 700;
  color: #B45309;
  cursor: pointer;
}
.btn-exit-pk:hover { text-decoration: underline; }
.pk-compare-bar {
  display: flex;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
  background: #E2E8F0;
}
.pk-segment-a, .pk-segment-b {
  height: 100%;
  transition: width 0.3s ease;
}
.pk-labels-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  font-weight: 800;
}

/* Scheme 2: Map Viewport Sync Toggle Bar */
.viewport-sync-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 16px;
  background: #EEF5FB;
  border-bottom: 1px solid #DCE7F2;
  flex-shrink: 0;
  font-size: 11.5px;
}
.viewport-sync-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  color: var(--ikea-blue);
  cursor: pointer;
  user-select: none;
}
.viewport-sync-indicator {
  font-size: 11px;
  color: var(--text-muted);
}
.viewport-sync-indicator strong {
  color: var(--ikea-blue);
}

.viewport-hint-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: #FEF9C3;
  border-bottom: 1px solid #FEF08A;
  color: #854D0E;
  font-size: 11px;
  line-height: 1.35;
}
.viewport-hint-bar .hint-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #D97706;
  flex-shrink: 0;
}

/* Results & View Switcher Bar */
.results-meta-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: #FFFFFF;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.results-count-text {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
}
.results-count-text strong {
  color: var(--text-main);
  font-weight: 800;
}

.view-switch-btns {
  display: flex;
  background: #F1F5F9;
  padding: 2px;
  border-radius: 6px;
}
.view-btn {
  background: transparent;
  border: none;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.12s ease;
}
.view-btn.active {
  background: #FFFFFF;
  color: var(--ikea-blue);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* Store Cards Container */
.store-cards-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.store-cards-container::-webkit-scrollbar { width: 6px; }
.store-cards-container::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }

/* Brand Category Header in Card View */
.brand-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 12px;
  border-radius: 6px;
  color: #FFFFFF;
  font-weight: 800;
  font-size: 12px;
  cursor: pointer;
  user-select: none;
  margin-top: 4px;
}
.brand-section-header .left-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.brand-section-header .count-tag {
  background: rgba(255, 255, 255, 0.25);
  padding: 1px 7px;
  border-radius: 10px;
  font-size: 10.5px;
}
.brand-section-header .chevron {
  transition: transform 0.2s ease;
}
.brand-section-header.collapsed .chevron {
  transform: rotate(-90deg);
}

/* Store Card Individual */
.store-card {
  background: #FFFFFF;
  border: 1px solid var(--skapa-border);
  border-radius: 8px;
  padding: 14px 16px;
  cursor: pointer;
  transition: border-color 0.15s ease;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  box-shadow: none;
}
.store-card:hover {
  border-color: var(--skapa-border-strong);
  box-shadow: none;
  transform: none;
}
.store-card.selected {
  border: 2px solid var(--ikea-blue);
  background: #FFFFFF;
  padding: 13px 15px;
  box-shadow: none;
}
.store-card.is-archived {
  opacity: 0.72;
  background: #F8FAFC;
  border-style: dashed;
}

.card-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-brand-tag {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  font-weight: 800;
  color: #FFFFFF;
  padding: 2.5px 8.5px;
  border-radius: 10rem;
  text-transform: uppercase;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.card-name-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--skapa-text);
  line-height: 1.35;
  word-break: break-word;
}
.card-meta-line {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--skapa-text-2);
}
.card-channel-pill {
  font-weight: 600;
  color: var(--skapa-text-2);
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
  align-items: center;
}
.tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  padding: 2.5px 8.5px;
  border-radius: 10rem;
  line-height: 1.25;
  white-space: nowrap;
}
.tag-channel {
  background: var(--skapa-neutral);
  color: var(--skapa-text-2);
}
.tag-colocation {
  background: #FEF2F2 !important;
  color: #B91C1C !important;
  border: 1px solid #FECACA !important;
  font-weight: 700 !important;
}

.card-dist-badge {
  display: inline-flex;
  align-items: center;
  gap: 3.5px;
  font-size: 11px;
  font-weight: 700;
  color: var(--skapa-text);
  background: var(--skapa-neutral);
  padding: 2.5px 8.5px;
  border-radius: 10rem;
  border: 1px solid var(--skapa-border);
  white-space: nowrap;
}

.card-address-box {
  display: flex;
  align-items: flex-start;
  gap: 5px;
  font-size: 12px;
  color: var(--skapa-text-2);
  line-height: 1.45;
  margin-top: 2px;
  word-break: break-word;
}
.card-address-box svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--skapa-text-3);
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
  padding: 2.5px 9px;
  border-radius: 10rem;
  white-space: nowrap;
}
.status-active {
  background: #ECFDF5;
  color: #065F46;
  border: 1px solid #A7F3D0;
}
.status-paused {
  background: #FFFBEB;
  color: #92400E;
  border: 1px solid #FDE68A;
}
.status-closed {
  background: var(--skapa-neutral);
  color: var(--skapa-text-2);
  border: 1px solid var(--skapa-border);
}

.card-actions-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--skapa-border);
}
.card-action-btn {
  flex: 1 1 115px;
  min-width: 0;
  min-height: 34px;
  height: 34px;
  padding: 0 12px;
  border-radius: 10rem;
  font-size: 12.5px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  box-sizing: border-box;
  transition: all 0.15s ease;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-action-btn svg {
  flex-shrink: 0;
  width: 13px;
  height: 13px;
}
.card-action-emph {
  background: var(--ikea-blue);
  color: #FFFFFF !important;
  border: 1px solid var(--ikea-blue);
}
.card-action-emph:hover {
  background: var(--skapa-emph-hover);
  border-color: var(--skapa-emph-hover);
}
.card-action-emph:active {
  background: var(--skapa-emph-active);
  border-color: var(--skapa-emph-active);
}
.card-action-secondary {
  background: #FFFFFF;
  color: var(--skapa-text) !important;
  border: 1px solid var(--skapa-border-strong);
}
.card-action-secondary:hover {
  background: var(--skapa-neutral);
  border-color: var(--skapa-text);
  color: var(--skapa-text) !important;
}
.card-action-secondary:active {
  background: #E5E5E5;
}
.btn-card-gmap, .btn-card-view-detail {
  font-size: 11px;
  font-weight: 700;
  color: var(--ikea-blue);
  cursor: pointer;
}

/* ─── VIEW 2: STORE DETAIL DRAWER (Scheme 2) ─── */
#sidebarDetailSection {
  flex: 1;
  display: none;
  flex-direction: column;
  background: #FFFFFF;
  min-height: 0;
  height: 100%;
  overflow: hidden;
}

.detail-nav-top {
  padding: 5px 12px;
  background: #FFFFFF;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  height: 36px;
  box-sizing: border-box;
}
.btn-back-to-list {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #F1F5F9;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3px 9px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-body);
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-back-to-list:hover {
  background: var(--ikea-blue);
  color: #FFFFFF;
  border-color: var(--ikea-blue);
}
.btn-close-detail {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: #FFFFFF;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-close-detail:hover {
  background: #F1F5F9;
  color: var(--text-main);
  border-color: #94A3B8;
}
.detail-brand-tag {
  font-size: 10.5px;
  font-weight: 800;
  color: #FFFFFF;
  padding: 2px 8px;
  border-radius: 4px;
}

/* Pinned Store Identity Bar */
.detail-pinned-header {
  padding: 6px 12px 5px;
  background: #FFFFFF;
  border-bottom: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex-shrink: 0;
}
.detail-pinned-header .detail-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}
.detail-pinned-header .detail-title {
  font-size: 15px;
  font-weight: 900;
  color: var(--text-main);
  line-height: 1.25;
  margin: 0;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.detail-pinned-header .detail-sub-meta {
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
}

/* 3-Tab Skapa Segmented Control */
.detail-tabs-bar {
  display: flex;
  background: #F8FAFC;
  padding: 4px 8px;
  gap: 4px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.detail-tab-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 4px 5px;
  min-height: 26px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-body);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.detail-tab-btn svg {
  width: 12px;
  height: 12px;
}
.detail-tab-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  color: var(--text-main);
}
.detail-tab-btn.active {
  background: #FFFFFF;
  color: var(--ikea-blue);
  border-color: #CBD5E1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.detail-tab-btn .tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #E2E8F0;
  color: var(--text-main);
  font-size: 9.5px;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 10px;
  min-width: 16px;
  height: 14px;
  line-height: 1;
}
.detail-tab-btn.active .tab-badge {
  background: var(--ikea-blue);
  color: #FFFFFF;
}

/* Scrollable Tab Pane Body */
.detail-content-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 8px 10px 14px;
  box-sizing: border-box;
}
.detail-content-body::-webkit-scrollbar { width: 5px; }
.detail-content-body::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }

.detail-tab-pane {
  display: none;
  flex-direction: column;
  gap: 8px;
}
.detail-tab-pane.active {
  display: flex;
}

/* Quick Nav Jump Cards */
.detail-quick-nav-cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 4px;
}
.quick-nav-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: left;
  width: 100%;
}
.quick-nav-card:hover {
  background: #F8FAFC;
  border-color: #94A3B8;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
.quick-nav-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.quick-nav-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.quick-nav-text strong {
  font-size: 12px;
  color: var(--text-main);
}
.quick-nav-text span {
  font-size: 10.5px;
  color: var(--text-muted);
}
.quick-nav-arrow {
  color: #94A3B8;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

/* Detail Info Cards Grid */
.detail-info-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #F8FAFC;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
}
.detail-info-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12.5px;
}
.detail-info-item .icon-col {
  color: var(--ikea-blue);
  flex-shrink: 0;
  margin-top: 2px;
}
.detail-info-item .text-col {
  flex: 1;
  color: var(--text-body);
  line-height: 1.45;
}
.detail-info-item .label {
  font-size: 10.5px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 2px;
}

/* Primary Action Buttons */
.detail-actions-cluster {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.btn-detail-gmap-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  background: var(--ikea-blue);
  color: #FFFFFF !important;
  font-size: 13.5px;
  font-weight: 800;
  padding: 11px 16px;
  border-radius: 8px;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0, 88, 163, 0.25);
  transition: all 0.15s ease;
}
.btn-detail-gmap-primary:hover {
  background: var(--ikea-blue-dark);
  color: #FFFFFF !important;
  transform: translateY(-1px);
}
.btn-detail-gmap-primary * {
  color: #FFFFFF !important;
  stroke: #FFFFFF !important;
}

.detail-secondary-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.btn-sec-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: #FFFFFF;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 7px 10px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-body);
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-sec-action:hover {
  border-color: #CBD5E1;
  background: #F8FAFC;
}
/* ─── P1: CATCHMENT TRADE ZONE & COMPETITOR ANALYSIS ─── */
.catchment-zone-box {
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 14px;
  background: #FFFFFF;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.catchment-zone-box .box-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12.5px;
  font-weight: 800;
  color: var(--text-main);
  gap: 8px;
  flex-wrap: wrap;
}
.catchment-hdr-title {
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn-toggle-circle {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #F1F5F9;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 3px 9px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-body);
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
}
.btn-toggle-circle:hover {
  background: #E2E8F0;
  color: var(--text-main);
}
.btn-toggle-circle.active {
  background: #EBF4FC;
  border-color: rgba(0, 88, 163, 0.4);
  color: var(--ikea-blue);
}
.badge-radius-val {
  background: #EEF2F6;
  color: var(--ikea-blue);
  font-size: 11.5px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 12px;
  border: 1px solid #CBD5E1;
}

.radius-slider-wrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #F8FAFC;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
}
.radius-slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 700;
}
.radius-range-slider {
  width: 100%;
  cursor: pointer;
  accent-color: var(--ikea-blue);
  height: 6px;
}
.radius-presets-row {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}
.btn-radius-preset {
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 3px 9px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-body);
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-radius-preset:hover {
  border-color: var(--ikea-blue);
  color: var(--ikea-blue);
}
.btn-radius-preset.active {
  background: var(--ikea-blue);
  color: #FFFFFF;
  border-color: var(--ikea-blue);
}

/* P2 Route Planning & Travel Time Box (Netlify & Google Maps Ready) */
.route-planning-box {
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 8px 10px;
  background: #FFFFFF;
  display: flex;
  flex-direction: column;
  gap: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  box-sizing: border-box;
}
.route-planning-box .box-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  font-weight: 800;
  color: var(--text-main);
  gap: 6px;
}
.route-hdr-title {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #0F172A;
  font-size: 11px;
}
.badge-route-status {
  background: #EFF6FF;
  color: #1D4ED8;
  font-size: 10px;
  font-weight: 700;
  padding: 1.5px 6px;
  border-radius: 10px;
  border: 1px solid #BFDBFE;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  white-space: nowrap;
}
.badge-route-status.ready {
  background: #ECFDF5;
  color: #065F46;
  border-color: #A7F3D0;
}

/* Dual Metric Cards: 公里數 & 預估時間 看板 */
.route-metric-cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
.route-metric-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 6px 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.15s ease;
}
.route-metric-card:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
}
.metric-card-top {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 700;
  color: #64748B;
}
.metric-card-icon {
  display: inline-flex;
  align-items: center;
  color: #1D4ED8;
}
.metric-card-icon svg {
  width: 12px;
  height: 12px;
}
.metric-card-main {
  display: flex;
  align-items: baseline;
  gap: 2px;
  margin: 2px 0 1px 0;
}
.metric-card-val {
  font-size: 19px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.1;
  letter-spacing: -0.5px;
  font-variant-numeric: tabular-nums;
}
.metric-card-unit {
  font-size: 11px;
  font-weight: 700;
  color: #475569;
}
.metric-card-sub {
  font-size: 9px;
  color: #64748B;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Mode Switcher */
.route-mode-switcher {
  display: flex;
  gap: 3px;
  background: #F1F5F9;
  border: 1px solid var(--skapa-border);
  padding: 3px;
  border-radius: 10rem;
}
.btn-route-mode {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 28px;
  padding: 0 4px;
  border: none;
  background: transparent;
  color: var(--skapa-text-2);
  font-size: 11.5px;
  font-weight: 700;
  border-radius: 10rem;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn-route-mode svg {
  flex-shrink: 0;
  width: 13px;
  height: 13px;
}
.btn-route-mode:hover {
  background: var(--skapa-neutral);
  color: var(--skapa-text);
}
.btn-route-mode.active {
  background: var(--skapa-text);
  color: #FFFFFF;
  box-shadow: none;
}
.btn-route-mode.active svg {
  color: #FFFFFF;
}
.mode-badge-preview {
  display: none;
}

/* Origin Selector Panel */
.route-origin-panel {
  background: #F8FAFC;
  border: 1px solid var(--skapa-border);
  border-radius: 8px;
  padding: 5px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.route-origin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10.5px;
  color: var(--skapa-text-2);
  font-weight: 700;
}
.route-origin-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}
.sel-route-origin {
  flex: 1;
  min-width: 0;
  background: #FFFFFF;
  border: 1px solid var(--skapa-border);
  border-radius: 64px;
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 600;
  color: var(--skapa-text);
  outline: none;
  cursor: pointer;
  height: 28px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.sel-route-origin:focus {
  border-color: var(--skapa-text);
}
.btn-origin-locate, .btn-origin-map-pick {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 3px 8px;
  height: 28px;
  background: #FFFFFF;
  border: 1px solid var(--skapa-border-strong);
  border-radius: 64px;
  font-size: 10.5px;
  font-weight: 700;
  color: var(--skapa-text);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
  flex-shrink: 0;
}
.btn-origin-locate svg, .btn-origin-map-pick svg {
  width: 12px;
  height: 12px;
}
.btn-origin-locate:hover, .btn-origin-map-pick:hover {
  background: var(--skapa-neutral);
  color: var(--skapa-text);
  border-color: var(--skapa-text);
}
.btn-origin-map-pick.picking {
  background: var(--skapa-text);
  color: #FFFFFF;
  border-color: var(--skapa-text);
}

/* Route Action Buttons */
.route-actions-row {
  display: flex;
  gap: 6px;
}
.btn-calc-route {
  flex: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: var(--ikea-blue);
  color: #FFFFFF;
  border: 1px solid var(--ikea-blue);
  border-radius: 10rem;
  min-height: 32px;
  padding: 0 10px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn-calc-route svg {
  width: 13px;
  height: 13px;
}
.btn-calc-route:hover {
  background: var(--skapa-emph-hover);
  border-color: var(--skapa-emph-hover);
}
.btn-calc-route:active {
  background: var(--skapa-emph-active);
}
.btn-calc-route.loading {
  opacity: 0.7;
  cursor: wait;
}
.btn-clear-route {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  background: #FFFFFF;
  color: var(--skapa-text);
  border: 1px solid var(--skapa-border-strong);
  border-radius: 10rem;
  min-height: 32px;
  padding: 0 8px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn-clear-route:hover {
  background: var(--skapa-neutral);
  border-color: var(--skapa-text);
}

/* External Turn-by-Turn Nav Button */
.btn-ext-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  min-height: 30px;
  width: 100%;
  box-sizing: border-box;
  padding: 0 10px;
  border-radius: 10rem;
  font-size: 11.5px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.15s ease;
  white-space: nowrap;
  background: #FFFFFF;
  color: var(--skapa-text);
  border: 1px solid var(--skapa-border-strong);
}
.btn-ext-nav svg {
  width: 12px;
  height: 12px;
}
.btn-ext-nav:hover {
  background: var(--skapa-neutral);
  color: var(--skapa-text);
  border-color: var(--skapa-text);
}

/* Route Summary & Engine Bar */
.route-results-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  border-radius: 6px;
  padding: 7px 10px;
  font-size: 11px;
  color: #166534;
  gap: 8px;
}
.route-engine-tag {
  background: rgba(0, 0, 0, 0.05);
  font-size: 9.5px;
  padding: 2px 6px;
  border-radius: 4px;
  color: #475569;
  font-weight: 700;
  white-space: nowrap;
}

.catchment-meta-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11.5px;
  color: var(--text-muted);
  font-weight: 600;
  padding: 0 2px;
}
.catchment-meta-summary strong {
  color: var(--ikea-blue);
  font-weight: 800;
}

.badge-dist {
  font-size: 10.5px;
  font-weight: 800;
  color: #0F766E;
  background: #CCFBF1;
  border: 1px solid #99F6E4;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.exclusive-zone-box {
  background: #F0FDF4;
  border: 1.5px dashed #22C55E;
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  gap: 10px;
  align-items: flex-start;
  color: #166534;
  font-size: 12px;
  line-height: 1.45;
}
.exclusive-zone-box .icon-col {
  color: #16A34A;
  flex-shrink: 0;
  margin-top: 1px;
}

.competitor-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.competitor-mini-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: 6px;
  background: #F8FAFC;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.15s ease;
}
.competitor-mini-item:hover {
  background: #F0F6FA;
  border-color: var(--ikea-blue);
  transform: translateX(2px);
}
.competitor-mini-item .brand-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.competitor-mini-item .c-name {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-main);
}
.competitor-mini-item .c-chan {
  font-size: 10.5px;
  color: var(--text-muted);
}

/* Toast Copy Feedback */
.toast-msg {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(100px);
  background: #111827;
  color: #FFFFFF;
  padding: 9px 18px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  z-index: 9999;
  opacity: 0;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}
.toast-msg.show {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

/* ════════════════════════════════════════════
   LEAFLET PIN & POPUP STYLING
════════════════════════════════════════════ */
.brand-pin-marker {
  position: relative;
  cursor: pointer;
  filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.4));
  transform-origin: 14px 36px !important;
  transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.brand-pin-marker:hover {
  transform: scale(1.18);
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.55));
  z-index: 1000 !important;
}

.brand-pin-marker svg {
  display: block;
  overflow: visible;
}

.high-contrast-pin svg path {
  stroke: #000000 !important;
  stroke-width: 2.5 !important;
}

/* GPS User Pulsing Marker */
.user-gps-pulse-marker {
  position: relative;
  width: 24px;
  height: 24px;
}
.user-gps-pulse-marker .pulse-ring {
  position: absolute;
  top: -6px;
  left: -6px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 88, 163, 0.35);
  animation: gpsPulse 2s infinite ease-out;
}
.user-gps-pulse-marker .user-dot {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #0058A3;
  border: 3px solid #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 88, 163, 0.5);
}
@keyframes gpsPulse {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(1.6); opacity: 0; }
}

.custom-popup .leaflet-popup-content-wrapper {
  border-radius: 12px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18);
  border: 1px solid var(--skapa-border);
}
.custom-popup .leaflet-popup-content {
  margin: 0;
  padding: 0;
  width: auto !important;
  line-height: inherit;
}
.custom-popup .leaflet-popup-tip-container { display: none; }

.popup-box {
  padding: 16px;
  width: 320px;
  max-width: min(340px, calc(100vw - 36px));
  min-width: 260px;
  box-sizing: border-box;
  color: var(--skapa-text);
  font-family: inherit;
  font-size: 13px;
  line-height: 1.5;
}
.popup-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 6px;
  padding-right: 18px;
}
.popup-brand-badge {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  font-weight: 800;
  color: #FFFFFF;
  padding: 2.5px 9px;
  border-radius: 10rem;
  letter-spacing: 0.2px;
  white-space: nowrap;
}
.popup-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--skapa-text);
  margin-bottom: 3px;
  line-height: 1.35;
  word-break: break-word;
}
.popup-meta {
  font-size: 12.5px;
  color: var(--skapa-text-2);
  margin-bottom: 8px;
  display: flex;
  gap: 6px;
}
.popup-addr {
  font-size: 12px;
  color: var(--skapa-text-2);
  margin-bottom: 10px;
  line-height: 1.45;
  display: flex;
  gap: 6px;
  word-break: break-word;
}
.popup-addr svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--skapa-text-2);
}
.popup-note-box {
  background: #FEF3C7;
  color: #92400E;
  font-size: 11px;
  padding: 6px 8px;
  border-radius: 6px;
  margin-bottom: 10px;
  line-height: 1.35;
  border-left: 3px solid #D97706;
}
.popup-action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--skapa-border);
}
.popup-action-row .pop-btn {
  flex: 1 1 115px;
  min-width: 0;
  height: 36px;
  min-height: 36px;
  padding: 0 12px;
  margin: 0;
  box-sizing: border-box;
  line-height: 1;
  font-size: 13px;
  font-weight: 700;
  border-radius: 10rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  font-family: inherit;
  transition: all 0.15s ease;
  overflow: hidden;
  text-overflow: ellipsis;
}
.popup-action-row .pop-btn svg {
  flex-shrink: 0;
  width: 14px;
  height: 14px;
}
.pop-btn-emph {
  background: var(--ikea-blue);
  color: #FFFFFF !important;
  border: 1px solid var(--ikea-blue);
}
.pop-btn-emph:hover {
  background: var(--skapa-emph-hover);
  border-color: var(--skapa-emph-hover);
}
.pop-btn-emph:active {
  background: var(--skapa-emph-active);
  border-color: var(--skapa-emph-active);
}
.pop-btn-secondary {
  background: #FFFFFF;
  color: var(--skapa-text) !important;
  border: 1px solid var(--skapa-border-strong);
}
.pop-btn-secondary:hover {
  background: var(--skapa-neutral);
  border-color: var(--skapa-text);
  color: var(--skapa-text) !important;
}
.pop-btn-secondary:active {
  background: #E5E5E5;
}
.popup-gmap-btn, .popup-drawer-btn {
  display: none;
}

/* Responsive Button Label adaptation across widths */
.btn-text-full {
  display: none;
}
.btn-text-compact {
  display: inline;
}
@media (min-width: 520px) {
  .store-card .btn-text-full {
    display: inline;
  }
  .store-card .btn-text-compact {
    display: none;
  }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
}
.empty-state svg {
  color: var(--text-light);
  margin-bottom: 12px;
}
.empty-state .title {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-body);
  margin-bottom: 4px;
}
.empty-state .desc {
  font-size: 12px;
}

.footer-info {
  padding: 10px 16px;
  font-size: 10.5px;
  color: var(--text-light);
  border-top: 1px solid var(--border);
  background: #FFFFFF;
  text-align: center;
  flex-shrink: 0;
}

/* Mobile Responsive Optimization (Section 4) */
@media (max-width: 768px) {
  header {
    height: auto;
    padding: 10px 14px;
    flex-wrap: wrap;
    gap: 8px;
  }
  .title-group h1 { font-size: 14px; }
  .title-group .subtitle { display: none; }
  .header-actions { width: 100%; margin-left: 0; justify-content: space-between; }
  .stat-pill { padding: 5px 9px; }
  .btn-export-csv { min-height: 40px; padding: 7px 12px; }
  .workspace {
    flex-direction: column-reverse;
  }
  aside {
    width: 100% !important;
    max-height: 48vh;
    border-left: none;
    border-top: 2px solid var(--border);
  }
  .sidebar-inner-content {
    width: 100% !important;
  }
  .sidebar-collapse-toggle { display: none; }
  .region-jump-bar {
    top: auto;
    bottom: 12px;
    max-width: 95%;
    overflow-x: auto;
  }
  .btn-region-jump { min-height: 40px; flex: 0 0 auto; }
  .btn-card-view-detail, .btn-card-gmap, .btn-sec-action { min-height: 40px; }
  .google-nav-control-group {
    margin-bottom: 56px !important;
    margin-left: 10px !important;
  }
  .map-controls-dock {
    top: 10px;
    left: 10px;
  }
  .map-style-dropdown { width: 230px; }
  .timeline-mode-active #regionJumpBar {
    display: none !important;
  }
  .timeline-player-panel {
    width: 95% !important;
    bottom: 12px !important;
    padding: 10px 12px !important;
  }
}

/* ════════════════════════════════════════════
   SCHEME A: TIMELINE & EXPANSION PLAYER (歷年展店時序演變)
════════════════════════════════════════════ */
.btn-header-timeline,
.btn-timeline-trigger {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 700;
  color: #1E293B;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap;
}
.btn-header-timeline:hover,
.btn-timeline-trigger:hover {
  background: #F8FAFC;
  border-color: var(--ikea-blue);
  color: var(--ikea-blue);
  box-shadow: 0 3px 10px rgba(0, 88, 163, 0.16);
  transform: translateY(-1px);
}
.btn-header-timeline.active,
.btn-timeline-trigger.active {
  background: var(--ikea-blue);
  border-color: var(--ikea-blue);
  color: #FFFFFF !important;
  box-shadow: 0 3px 12px rgba(0, 88, 163, 0.35);
}
.btn-header-timeline.active svg,
.btn-timeline-trigger.active svg {
  stroke: #FFFFFF;
}
.pill-timeline-tag {
  background: #EFF6FF;
  color: #1D4ED8;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 10px;
  letter-spacing: 0.3px;
  transition: all 0.15s ease;
}
.btn-header-timeline.active .pill-timeline-tag,
.btn-timeline-trigger.active .pill-timeline-tag {
  background: rgba(255, 255, 255, 0.22);
  color: #FFFFFF;
}

/* Timeline Player Floating Panel */
.timeline-player-panel {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(40px);
  width: 90%;
  max-width: 660px;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1.5px solid #CBD5E1;
  border-radius: 18px;
  padding: 12px 18px 10px 18px;
  box-shadow: 0 12px 36px rgba(15, 23, 42, 0.18), 0 2px 8px rgba(15, 23, 42, 0.06);
  z-index: 860;
  opacity: 0;
  pointer-events: none;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
}
.timeline-player-panel.active {
  opacity: 1;
  pointer-events: auto;
  visibility: visible;
  transform: translateX(-50%) translateY(0);
}

.timeline-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.timeline-title-area {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.timeline-scope-pill {
  background: #0058A3;
  color: #FFFFFF;
  font-size: 11.5px;
  font-weight: 700;
  padding: 2.5px 9px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.timeline-stat-text {
  font-size: 12.5px;
  color: #334155;
  font-weight: 600;
}
.timeline-stat-text strong {
  color: #0F172A;
  font-size: 14.5px;
  font-weight: 800;
}
.tl-highlight-num {
  color: #0058A3 !important;
}
.tl-counter-sep {
  color: #CBD5E1;
  margin: 0 3px;
}
.tl-new-badge {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
  font-size: 10.5px;
  font-weight: 800;
  padding: 1px 6px;
  border-radius: 10px;
  margin-left: 4px;
}

.timeline-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.tl-toggle-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
  color: #475569;
}
.tl-toggle-wrap input[type="checkbox"] {
  accent-color: #0058A3;
  width: 13px;
  height: 13px;
  cursor: pointer;
}
.btn-close-timeline {
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #64748B;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-close-timeline:hover {
  background: #E2E8F0;
  color: #0F172A;
  transform: scale(1.08);
}

/* Sparkline bar chart */
.timeline-sparkline-wrap {
  display: flex;
  align-items: flex-end;
  height: 26px;
  gap: 2px;
  margin-bottom: 6px;
  padding: 0 4px;
  background: rgba(241, 245, 249, 0.7);
  border-radius: 6px;
}
.tl-spark-bar {
  flex: 1;
  background: #CBD5E1;
  border-radius: 2px 2px 0 0;
  min-height: 2px;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
}
.tl-spark-bar:hover {
  background: #93C5FD;
}
.tl-spark-bar.active {
  background: #0058A3;
}
.tl-spark-bar.past {
  background: #94A3B8;
}

/* Scrubber row */
.timeline-scrubber-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.tl-btn-play {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #0058A3;
  color: #FFFFFF;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 3px 8px rgba(0, 88, 163, 0.28);
  transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
}
.tl-btn-play:hover {
  background: #004580;
  transform: scale(1.06);
}
.tl-slider-track-wrap {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.tl-range-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  background: #E2E8F0;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  transition: background 0.15s ease;
}
.tl-range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #0058A3;
  border: 3px solid #FFFFFF;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
  cursor: pointer;
  transition: transform 0.1s ease;
}
.tl-range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}
.tl-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: #94A3B8;
  font-weight: 700;
  padding: 0 2px;
}
.tl-speed-selector {
  display: flex;
  align-items: center;
  background: #F1F5F9;
  border-radius: 14px;
  padding: 2px;
  gap: 2px;
  flex-shrink: 0;
}
.tl-speed-btn {
  background: transparent;
  border: none;
  font-size: 10.5px;
  font-weight: 700;
  color: #64748B;
  padding: 2.5px 7px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.tl-speed-btn.active {
  background: #FFFFFF;
  color: #0F172A;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tag-opened-year {
  background: #FEF3C7 !important;
  color: #B45309 !important;
}

/* Timeline Mode Active overrides */
.timeline-mode-active #regionJumpBar {
  opacity: 0.15 !important;
  pointer-events: none !important;
  transform: translateX(-50%) translateY(-12px) !important;
  transition: all 0.3s ease !important;
}
.timeline-mode-active #regionJumpBar:hover {
  opacity: 0.95 !important;
  pointer-events: auto !important;
  transform: translateX(-50%) translateY(0) !important;
}
.timeline-mode-active #pkCompareBar {
  display: none !important;
}

/* Pulse animation for newly opened store pins */
@keyframes tlMarkerPulse {
  0% {
    transform: scale(0.6);
    filter: drop-shadow(0 0 0 rgba(0, 88, 163, 0.8));
  }
  50% {
    transform: scale(1.35);
    filter: drop-shadow(0 0 10px rgba(0, 88, 163, 0.9));
  }
  100% {
    transform: scale(1);
    filter: drop-shadow(0 0 0 rgba(0, 88, 163, 0));
  }
}
.brand-pin-marker.marker-new-pulse {
  animation: tlMarkerPulse 0.9s cubic-bezier(0.16, 1, 0.3, 1) !important;
  z-index: 6000 !important;
}

/* ─── Store drawer: simplified Skapa-style content ─── */
.sk-section { display:flex; flex-direction:column; gap:8px; margin-bottom:16px; }
.sk-label { font-size:12px; font-weight:700; color:#484848; }
.sk-address-row { display:flex; align-items:flex-start; gap:8px; font-size:14px; line-height:1.5; color:#111; }
.sk-address-row span { flex:1; }
.sk-icon-btn { flex-shrink:0; width:36px; height:36px; display:inline-flex; align-items:center; justify-content:center; border-radius:50%; border:1px solid #DFDFDF; background:#fff; color:#111; cursor:pointer; }
.sk-icon-btn:hover { border-color:#111; }
.sk-icon-btn.picking { background:var(--ikea-blue); border-color:var(--ikea-blue); color:#fff; }
.sk-icon-btn svg { width:16px; height:16px; }
.sk-notice { background:#FFF7E0; border-left:4px solid #F2A900; padding:10px 12px; border-radius:4px; font-size:13px; line-height:1.5; color:#111; margin-bottom:16px; }
.sk-actions { display:flex; flex-direction:column; gap:8px; }
.sk-btn-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
.sk-btn { display:inline-flex; align-items:center; justify-content:center; gap:6px; min-height:44px; padding:0 16px; border-radius:999px; font-size:14px; font-weight:700; text-decoration:none; cursor:pointer; font-family:inherit; white-space:nowrap; }
.sk-btn svg { width:14px; height:14px; }
.sk-btn-primary { background:var(--ikea-blue); color:#fff; border:none; }
.sk-btn-primary:hover { background:var(--ikea-blue-dark); }
.sk-btn-secondary { background:#fff; color:#111; border:1px solid #929292; }
.sk-btn-secondary:hover { border-color:#111; }
.sk-link-btn { background:none; border:none; color:#484848; font-size:13px; text-decoration:underline; cursor:pointer; padding:6px; font-family:inherit; }
.sk-origin-stack { display:flex; flex-direction:column; gap:8px; }
/* 自訂下拉箭頭，避免原生箭頭貼到膠囊圓角外 */
#paneDetailRoute .sel-route-origin {
  -webkit-appearance:none; appearance:none; width:100%; height:44px; flex:none;
  padding:0 40px 0 16px; font-size:14px; border-radius:999px;
  background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23111' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E") no-repeat right 16px center;
}
.sk-btn-sm { min-height:40px; font-size:13px; padding:0 12px; }
.sk-btn-secondary.picking { background:var(--ikea-blue); border-color:var(--ikea-blue); color:#fff; }
/* .sk-section 是 flex，需明確讓 hidden 生效（非大眾運輸時隱藏出發時間） */
.sk-section[hidden] { display:none; }
.sk-route-result { padding:14px 0; margin-bottom:12px; border-top:1px solid #DFDFDF; border-bottom:1px solid #DFDFDF; }
.sk-route-duration { font-size:24px; font-weight:700; color:#111; line-height:1.2; }
.sk-route-meta { font-size:13px; color:#484848; margin-top:4px; }
.sk-route-result.is-error .sk-route-duration { font-size:16px; color:#CC0008; }
#paneDetailRoute .route-mode-switcher { margin-bottom:16px; }
.sk-catch-head { display:flex; align-items:center; justify-content:space-between; gap:8px; font-size:14px; }
.sk-switch { display:inline-flex; align-items:center; gap:6px; font-size:12px; color:#484848; cursor:pointer; }
.sk-switch input { accent-color:var(--ikea-blue); width:16px; height:16px; }
.sk-empty { font-size:13px; color:#484848; padding:12px 0; }

/* Zoomed-out overview markers */
.map-overview .brand-pin-marker svg { transform: scale(0.5); transform-origin: 50% 100%; }
.map-overview .brand-pin-marker svg text { display: none; }
/* Nearby list brand filter */
.sk-brand-chips { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; }
.sk-brand-chip { display:inline-flex; align-items:center; gap:5px; min-height:32px; padding:0 10px; border-radius:999px; border:1px solid #DFDFDF; background:#fff; font-size:12px; font-weight:700; color:#111; cursor:pointer; font-family:inherit; }
.sk-brand-chip.active { border-color:#111; background:#111; color:#fff; }
.sk-brand-chip .brand-dot { width:8px; height:8px; border-radius:50%; }
.badge-same-building { font-size:11px; font-weight:700; color:#111; background:#FFDB00; border-radius:4px; padding:1px 6px; }
/* Mobile: store detail gets more room, tighter spacing */
@media (max-width: 768px) {
  aside:has(#sidebarDetailSection[style*="flex"]) { max-height: 64vh; }
  .sk-section { margin-bottom: 10px; }
  #paneDetailRoute .route-mode-switcher { margin-bottom: 10px; }
  .sk-route-result { padding: 10px 0; margin-bottom: 10px; }
  .sk-route-duration { font-size: 20px; }
  .sk-btn { min-height: 44px; }
  body:has(#sidebarDetailSection[style*="flex"]) .map-controls-dock,
  body:has(#sidebarDetailSection[style*="flex"]) .region-jump-bar { display: none; }
}
</style>
</head>
<body>

<!-- ═══════════════════════ HEADER ═══════════════════════ -->
<header>
  <div class="ikea-logo-box" title="台灣實體門市 GIS 地理圖資儀表板">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40" width="86" height="34.4" style="display:block;" aria-label="IKEA">
      <g fill="none" fill-rule="evenodd">
        <path fill="#0058A3" d="M100 40H0V0h100v40z"/>
        <path fill="#FFDB00" d="M2 20c0 9.8325 20.1163 18 48.0072 18C77.898 38 98 29.8325 98 20S77.8837 2 50.0072 2C22.1306 2 2 10.1675 2 20z"/>
        <path fill="#0058A3" fill-rule="nonzero" d="M46.448 26.0047c.3153.4477.6593.8674 1.0606 1.2452H36.6874c0-.4198-.4156-1.2732-.8743-1.9447-.4586-.6716-2.9382-4.351-2.9382-4.351v5.0505c0 .4197 0 .8254.215 1.2452h-9.0152c.215-.4198.215-.8255.215-1.2452V14.0008c0-.4197 0-.8254-.215-1.2451h9.0152c-.215.4197-.215.8254-.215 1.2451v5.2465s2.8809-3.6655 3.5402-4.519c.5016-.6435 1.118-1.553 1.118-1.9726h9.4022c-.645.4197-1.3616 1.1752-1.9493 1.8747-.516.6156-3.4398 4.0992-3.4398 4.0992s4.3284 6.4497 4.9017 7.2751zm2.8378-12.0039v12.0039c0 .4197 0 .8254-.215 1.2452h17.3999v-4.0293c-.43.2098-.8457.2098-1.2756.2098h-7.324v-1.9027h7.0373v-3.05h-7.0373v-1.9166h7.324c.43 0 .8456 0 1.2756.1959v-4.0153H49.0708c.215.4337.215.8394.215 1.2591zm41.2924 12.0039c.1433.4617.387.8814.7023 1.2452h-9.4309c.043-.4198-.1146-.8255-.2866-1.2452 0 0-.1434-.3358-.344-.8254l-.086-.2099h-5.4321l-.086.2238s-.1577.4058-.301.8255c-.1433.4197-.301.8254-.2436 1.2451h-7.4387a3.6406 3.6406 0 0 0 .6737-1.2451l4.4574-12.0039c.1577-.4197.3153-.8254.258-1.2451h12.5697c-.1146.4197.1147.8254.2724 1.2451.3726.9094 4.4 11.1784 4.7154 11.9899zm-10.6348-4.0992-1.3186-3.3578c-.1147-.3077-.215-.6295-.2867-.9513a5.5011 5.5011 0 0 1-.258.9513c-.043.14-.602 1.609-1.247 3.3578h3.1103zm-60.1399-9.1498H10c.215.4197.215.8254.215 1.2451v12.0039c0 .4197 0 .8254-.215 1.2452h9.8035c-.215-.4198-.215-.8255-.215-1.2452V14.0008c0-.4197 0-.8254.215-1.2451zm67.7648 1.1472c-.043-1.0213.774-1.8747 1.8203-1.9027h.129c1.0606-.014 1.9349.7974 1.9492 1.8327v.07c.0287 1.0493-.817 1.9307-1.9062 1.9587-1.075.028-1.978-.7975-2.0066-1.8608.0143-.028.0143-.07.0143-.098zm.387 0c0 .8394.7023 1.525 1.5623 1.525s1.5622-.6856 1.5622-1.525c0-.8394-.7023-1.525-1.5622-1.525-.8313-.028-1.5336.6016-1.5623 1.413v.112zm1.1753 1.1332h-.344v-2.2944h.8743c.4157.014.731.3357.731.7415 0 .2798-.1577.5316-.4157.6715l.5017.8814h-.387l-.4587-.8114h-.5016v.8114zm0-1.1332h.473c.2293.014.43-.154.43-.3778 0-.2238-.1577-.4197-.387-.4197h-.516v.7975z"/>
      </g>
    </svg>
  </div>
  <div class="title-group">
    <h1>台灣實體門市 GIS 地理圖資儀表板</h1>
  </div>
  <div class="header-actions">
    <button class="btn-header-timeline" id="btnToggleTimeline" title="切換歷年展店時序演變模式（動態播放商圈拓點軌跡）">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
      <span>歷年展店時序</span>
      <span class="pill-timeline-tag">時光軸</span>
    </button>
    <button class="btn-export-csv" id="btnExport" title="匯出當前篩選名錄至 CSV">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
      <span>匯出篩選 CSV</span>
    </button>
  </div>
</header>

<!-- ═══════════════════════ MAIN WORKSPACE ═══════════════════════ -->
<div class="workspace">

  <!-- Map Wrap -->
  <div class="map-wrap">
    <div id="map"></div>

    <!-- SECTION 3: Region Quick Jump Bar with Interactive Boundary Envelopes -->
    <div class="region-jump-bar" id="regionJumpBar">
      <button class="btn-region-jump active" data-region="all" title="將地圖移回全台範圍">全台</button>
      <button class="btn-region-jump" data-region="taipei" title="快速移動到大台北；開啟「門市清單跟隨目前地圖範圍」後才會同步縮小清單">大台北</button>
      <button class="btn-region-jump" data-region="taoyuan_hsinchu" title="快速移動到桃竹苗；開啟「門市清單跟隨目前地圖範圍」後才會同步縮小清單">桃竹苗</button>
      <button class="btn-region-jump" data-region="central" title="快速移動到中台灣；開啟「門市清單跟隨目前地圖範圍」後才會同步縮小清單">中台灣</button>
      <button class="btn-region-jump" data-region="south" title="快速移動到南台灣；開啟「門市清單跟隨目前地圖範圍」後才會同步縮小清單">南台灣</button>
      <button class="btn-region-jump" data-region="east_offshore" title="快速移動到東部與離島；開啟「門市清單跟隨目前地圖範圍」後才會同步縮小清單">東部與離島</button>
    </div>

    <!-- TOP-LEFT: Floating Map View & Layer Style Dock (No Overlap with Sidebar) -->
    <div class="map-controls-dock" id="mapControlsDock">
      <button class="map-control-trigger-btn" id="btnToggleMapControls" title="切換底圖風格與視覺降噪設定">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
        <span>底圖風格</span>
        <span class="pill-active-style" id="lblPillActiveStyle">Google 淺灰</span>
        <svg class="chevron-arrow" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </button>

      <!-- Dropdown Card Menu -->
      <div class="map-style-dropdown" id="mapStyleDropdown">
        <div class="dropdown-header">
          <div class="dropdown-title">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            底圖與圖層顯示
          </div>
          <button class="btn-close-dropdown" id="btnCloseMapStyle" title="關閉選單">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>

        <div class="dropdown-body">
          <div class="dropdown-section">
            <div class="section-label">Google 地圖模式</div>
            <div class="tile-switch-group">
              <button class="tile-btn active" id="btnTileMono" title="Google Maps 簡約淺灰高對比底圖（保留極簡調色）">Google 淺灰</button>
              <button class="tile-btn" id="btnTileSatellite" title="Google Maps 混合衛星空拍圖（含繁中道路與地標覆蓋）">Google 衛星</button>
              <button class="tile-btn" id="btnTileColor" title="Google Maps 官方原生繁中彩色街道圖">Google 彩色</button>
            </div>
          </div>

          <div class="dropdown-section">
            <div class="section-label">視覺降噪與對比</div>
            <div class="panel-opt-row">
              <label class="switch-label" for="chkGrayscale">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a10 10 0 0 1 0 20z"></path></svg>
                單色灰階降噪濾鏡
              </label>
              <input type="checkbox" id="chkGrayscale" class="toggle-checkbox" title="開啟後全圖去飽和純色化">
            </div>

            <div class="panel-opt-row">
              <label class="switch-label" for="chkContrast">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                門市標記高對比邊框
              </label>
              <input type="checkbox" id="chkContrast" class="toggle-checkbox" title="增強門市標記黑邊，在淺底圖上更加醒目">
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TOP-RIGHT: Floating Trigger when Sidebar is collapsed (Scheme 4 Exclusive Zone) -->
    <button class="floating-open-sidebar-btn" id="btnOpenSidebar" title="展開側邊門市面板">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      <span>門市名錄面板</span>
      <span class="badge-num" id="lblFloatingCount">ACTIVE_STORE_COUNT_PLACEHOLDER</span>
    </button>

    <!-- BOTTOM-CENTER: Timeline Player Panel -->
    <div class="timeline-player-panel" id="timelinePlayerPanel">
      <div class="timeline-header-row">
        <div class="timeline-title-area">
          <span class="timeline-scope-pill" id="tlScopeLabel">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
            <span id="tlScopeText">全台門市</span>
          </span>
          <span class="timeline-stat-text">
            <strong id="tlCurrentYear">2026</strong> 年
            <span class="tl-counter-sep">|</span>
            累計 <strong id="tlCumulativeCount" class="tl-highlight-num">0</strong> 間
            <span id="tlNewInYearBadge" class="tl-new-badge">+0 新增</span>
          </span>
        </div>
        <div class="timeline-header-actions">
          <label class="tl-toggle-wrap" title="開關：僅看當年度新開門市 vs 歷年累計已開門市">
            <input type="checkbox" id="tlCumulativeToggle" checked>
            <span>累積模式</span>
          </label>
          <button class="btn-close-timeline" id="btnCloseTimeline" title="退出演變模式 (恢復原本完整儀表板)">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Sparkline bar chart (Yearly store opening velocity) -->
      <div class="timeline-sparkline-wrap" id="tlSparklineWrap" title="各年份新開店數分布 (點擊柱條可直接跳轉)"></div>

      <!-- Scrubber bar & controls -->
      <div class="timeline-scrubber-row">
        <button class="tl-btn-play" id="tlBtnPlay" title="播放 / 暫停時序演變">
          <svg id="tlPlayIcon" width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
          </svg>
          <svg id="tlPauseIcon" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="display:none">
            <rect x="6" y="4" width="4" height="16"></rect>
            <rect x="14" y="4" width="4" height="16"></rect>
          </svg>
        </button>

        <div class="tl-slider-track-wrap">
          <input type="range" id="tlRangeSlider" class="tl-range-slider" min="1996" max="2026" step="1" value="2026">
          <div class="tl-ticks">
            <span>1996</span>
            <span>2004</span>
            <span>2010</span>
            <span>2016</span>
            <span>2021</span>
            <span>2026</span>
          </div>
        </div>

        <div class="tl-speed-selector">
          <button class="tl-speed-btn active" data-speed="800">1x</button>
          <button class="tl-speed-btn" data-speed="400">2x</button>
          <button class="tl-speed-btn" data-speed="200">4x</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══════════════════════ INTEGRATED SIDEBAR ═══════════════════════ -->
  <aside id="mainSidebar">

    <!-- Scheme 4: Collapse Toggle Handle -->
    <button class="sidebar-collapse-toggle" id="btnCollapseSidebar" title="收起側邊面板 (釋放全螢幕地圖)">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>

    <div class="sidebar-inner-content">

      <!-- ─── SUBVIEW 1: STORE LIST & FILTERS ─── -->
      <div id="sidebarListSection">

        <div class="dataset-switch" aria-label="資料類型切換">
          <button class="dataset-switch-btn active" data-dataset="home">居家品牌</button>
          <button class="dataset-switch-btn" data-dataset="mass">量販通路</button>
          <button class="dataset-switch-btn" data-dataset="ecommerce">電商取貨</button>
        </div>

        <!-- Control Center -->
        <div class="sidebar-control-box">
          <div class="search-wrapper">
            <div class="search-input-group">
              <span class="search-icon-left">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </span>
              <input id="q" class="search-input-main" type="text" placeholder="搜尋門市、商圈（快速鍵 Cmd+K）…">
              <span class="kbd-hint">Cmd+K</span>
              <button class="search-clear-btn" id="btnClearSearch" title="清除搜尋">&times;</button>
            </div>
            <button class="btn-locate-me" id="btnLocateMe" title="GPS 定位我的位置，依距離遠近排序">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"></circle><path d="M12 2v3M12 19v3M2 12h3M19 12h3"></path><circle cx="12" cy="12" r="7"></circle></svg>
              <span>離我最近</span>
            </button>
          </div>

          <div class="dropdown-grid">
            <select class="custom-select" id="selCity">
              <option value="">全部縣市</option>
            </select>
            <select class="custom-select" id="selDistrict">
              <option value="">全部行政區</option>
            </select>
          </div>
          <div class="dropdown-grid">
            <select class="custom-select" id="selChannel">
              <option value="">全部門市型態</option>
              <option value="大型獨棟／街邊門市">大型獨棟／街邊門市</option>
              <option value="百貨／購物中心門市">百貨／購物中心門市</option>
              <option value="都會／社區門市">都會／社區門市</option>
              <option value="量販店中店">量販店中店</option>
              <option value="店中店／專櫃">店中店／專櫃</option>
              <option value="子品牌門市">子品牌門市</option>
              <option value="訂購取貨中心">訂購取貨中心</option>
              <option value="期間限定門市">期間限定門市</option>
            </select>
            <select class="custom-select" id="selStatus">
              <option value="">全部營運狀態</option>
              <option value="現行營運中" selected>現行營運中</option>
              <option value="暫停營業">暫停營業</option>
              <option value="歷史變動（已熄燈/遷址）">歷史紀錄（已熄燈/遷址）</option>
            </select>
          </div>
        </div>

        <!-- Quick Brand Strip -->
        <div class="brand-strip">
          <div class="brand-strip-hdr">
            <span>品牌快速篩選</span>
            <div class="brand-strip-actions">
              <button class="btn-pk-mode" id="btnPkMode" title="開啟雙品牌門市戰略對比">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                <span>品牌比較</span>
              </button>
              <button class="btn-reset-filters" id="btnResetAll" title="清空全部關鍵字與條件">重設篩選</button>
            </div>
          </div>
          <div class="brand-chips-wrap" id="brandPills"></div>
        </div>

        <!-- Brand PK Mode Banner -->
        <div class="pk-banner-box" id="pkBannerBox">
          <div class="pk-banner-top">
            <span class="pk-banner-title">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
              雙品牌比較模式
            </span>
            <button class="btn-exit-pk" id="btnExitPk">結束比較 &times;</button>
          </div>
          <div class="pk-compare-bar">
            <div class="pk-segment-a" id="pkSegA" style="width:50%;background:#0058A3"></div>
            <div class="pk-segment-b" id="pkSegB" style="width:50%;background:#00A396"></div>
          </div>
          <div class="pk-labels-row">
            <span id="pkLabelA" style="color:#0058A3">IKEA 11 間</span>
            <span id="pkLabelB" style="color:#00A396">宜得利 77 間</span>
          </div>
        </div>

        <!-- Scheme 2: Map Viewport Sync Toggle Bar -->
        <div class="viewport-sync-bar">
          <label class="viewport-sync-label" for="chkViewportSync" title="開啟後僅列出目前地圖畫面所看見的門市">
            <input type="checkbox" id="chkViewportSync" style="cursor:pointer">
            <span>門市清單跟隨目前地圖範圍</span>
          </label>
          <span class="viewport-sync-indicator" id="lblViewportIndicator">清單範圍：全台</span>
        </div>
        <div class="viewport-hint-bar" id="viewportHintBar" style="display:none;">
          <span class="hint-dot"></span>
          <span id="viewportHintText">目前地圖視野涵蓋全台。請滾動滑鼠滾輪放大地圖或拖曳，名錄將即時篩選畫面內門市！</span>
        </div>

        <!-- Results & View Switcher Bar -->
        <div class="results-meta-bar">
          <div class="results-count-text">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
            目前顯示：<strong id="lblCount">ACTIVE_STORE_COUNT_PLACEHOLDER 間門市</strong>
          </div>
          <div class="view-switch-btns">
            <button class="view-btn active" id="vtCards">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
              卡片
            </button>
            <button class="view-btn" id="vtTable">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
              表格
            </button>
          </div>
        </div>

        <!-- Store List Area -->
        <div class="store-cards-container" id="storeList"></div>

        <!-- Footer Meta -->
        <div class="footer-info">
          門市座標已依官方資訊與 Google Maps 核對 ｜ 資料更新：DATA_UPDATED_DATE_PLACEHOLDER
        </div>
      </div>

      <!-- ─── SUBVIEW 2: STORE DETAIL DRAWER (Scheme 2) ─── -->
      <div id="sidebarDetailSection">
        <div class="detail-nav-top">
          <button class="btn-back-to-list" id="btnBackToList">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            <span>返回門市清單</span>
          </button>
          <div style="display:flex;align-items:center;gap:8px">
            <span id="detailTopBrandBadge" class="detail-brand-tag">IKEA</span>
            <button class="btn-close-detail" id="btnCloseDetailDrawer" title="關閉門市面板" aria-label="關閉門市面板">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>
        </div>

        <!-- Pinned Store Identity Bar -->
        <div class="detail-pinned-header" id="detailPinnedHeader"></div>

        <!-- Pinned 3-Tab Skapa Segmented Navigation -->
        <div class="detail-tabs-bar" id="detailTabsBar" role="tablist" aria-label="門市資訊分頁">
          <button class="detail-tab-btn active" data-tab="info" role="tab" id="tabDetailInfo" aria-controls="paneDetailInfo" aria-selected="true" tabindex="0" onclick="switchDetailTab('info')">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <span>資訊</span>
          </button>
          <button class="detail-tab-btn" data-tab="route" role="tab" id="tabDetailRoute" aria-controls="paneDetailRoute" aria-selected="false" tabindex="-1" onclick="switchDetailTab('route')">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"></circle><path d="M9 19h8.5a4.5 4.5 0 0 0 0-9H7a3 3 0 0 1 0-6h11"></path><polyline points="15 7 18 4 21 7"></polyline></svg>
            <span>路線</span>
          </button>
          <button class="detail-tab-btn" data-tab="catchment" role="tab" id="tabDetailCatchment" aria-controls="paneDetailCatchment" aria-selected="false" tabindex="-1" onclick="switchDetailTab('catchment')">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
            <span>周邊門市</span>
            <span class="tab-badge" id="tabCatchmentCount">0</span>
          </button>
        </div>

        <div class="detail-content-body" id="detailContentBody">
          <!-- Dynamic Content Panes Injected Here -->
        </div>
      </div>

    </div>
  </aside>

</div>

<!-- Copy Feedback Toast -->
<div class="toast-msg" id="toastMsg">已複製門市地址至剪貼簿！</div>

<!-- ═══════════════════════ JAVASCRIPT ═══════════════════════ -->
<script src="vendor/leaflet/leaflet.js"></script>
<script>
/* ─── DATA INJECTION ─── */
const ALL_STORES = STORES_DATA_PLACEHOLDER;
let shopeeDataLoaded = false;
let shopeeLoadPromise = null;
let markerClusterLayer = null;

/* ─── BRAND CONFIG ─── */
const BRANDS = {
  "IKEA":              { color: "#0058A3", label: "IKEA 宜家家居",       tableLabel: "IKEA",    abbr: "IK" },
  "無印良品":           { color: "#7F0019", label: "無印良品 (MUJI)",     tableLabel: "無印良品", abbr: "無" },
  "宜得利":             { color: "#00A396", label: "宜得利家居 (NITORI)", tableLabel: "宜得利",   abbr: "宜" },
  "特力屋":             { color: "#EA580C", label: "特力屋 (TLW)",        tableLabel: "特力屋",   abbr: "特" },
  "HOLA":              { color: "#D97706", label: "HOLA 和樂家居",        tableLabel: "HOLA",    abbr: "HO" },
  "hoi! 好好生活":      { color: "#E11D48", label: "hoi! 好好生活",       tableLabel: "hoi!",    abbr: "hi" },
  "MR. LIVING 居家先生":{ color: "#1E293B", label: "MR. LIVING 居家先生", tableLabel: "MR.",     abbr: "MR" },
  "Costco 好市多":      { color: "#E31837", label: "Costco 好市多",       tableLabel: "Costco",  abbr: "CO" },
  "萬家福":             { color: "#0B6E4F", label: "萬家福量販",          tableLabel: "萬家福",   abbr: "萬" },
  "大全聯":             { color: "#E60012", label: "大全聯 MEGA PXMART", tableLabel: "大全聯",   abbr: "大" },
  "蝦皮店到店":         { color: "#EE4D2D", label: "蝦皮店到店",           tableLabel: "蝦皮",     abbr: "蝦" },
};
const BRAND_KEYS = Object.keys(BRANDS);
const DATASET_BRANDS = {
  home: ["IKEA", "無印良品", "宜得利", "特力屋", "HOLA", "hoi! 好好生活", "MR. LIVING 居家先生"],
  mass: ["Costco 好市多", "萬家福", "大全聯"],
  ecommerce: ["蝦皮店到店"]
};

/* ─── SVG ICONS REPOSITORY (Strictly Zero Emojis) ─── */
const SVG = {
  store: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>`,
  pin: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>`,
  external: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`,
  check: `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
  chevron: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>`,
  pause: `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`,
  copy: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`,
  crosshair: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="22" y1="12" x2="18" y2="12"></line><line x1="6" y1="12" x2="2" y2="12"></line><line x1="12" y1="6" x2="12" y2="2"></line><line x1="12" y1="22" x2="12" y2="18"></line></svg>`,
  archive: `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg>`,
  gps: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"></circle><path d="M12 2v3M12 19v3M2 12h3M19 12h3"></path><circle cx="12" cy="12" r="7"></circle></svg>`,
  battle: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`,
  target: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path></svg>`,
  fileSearch: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><circle cx="10.5" cy="14.5" r="2.5"></circle><line x1="12.3" y1="16.3" x2="14.5" y2="18.5"></line></svg>`,
  star: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`,
  clock: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
  route: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"></circle><path d="M9 19h8.5a4.5 4.5 0 0 0 0-9H7a3 3 0 0 1 0-6h12"></path><circle cx="18" cy="5" r="3"></circle></svg>`,
  car: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12l2-5a2 2 0 0 1 1.9-1.3h8.2A2 2 0 0 1 18 7l2 5v5a1 1 0 0 1-1 1h-1a2 2 0 0 1-4 0H10a2 2 0 0 1-4 0H5a1 1 0 0 1-1-1v-5z"></path><circle cx="8" cy="17" r="1.5"></circle><circle cx="16" cy="17" r="1.5"></circle><path d="M5 12h14"></path></svg>`,
  transit: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h12a3 3 0 0 1 3 3v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a3 3 0 0 1 3-3z"></path><path d="M3 10h18"></path><path d="M12 3v7"></path><circle cx="7.5" cy="15" r="1.2" fill="currentColor"></circle><circle cx="16.5" cy="15" r="1.2" fill="currentColor"></circle><path d="M8 18l-3 3"></path><path d="M16 18l3 3"></path></svg>`,
  walk: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="14" cy="4" r="2"></circle><path d="M7 21l3.5-7 2.5 3.5V21"></path><path d="M18 10l-4-2.5-3.5 2-2.5-1.5"></path><path d="M11 14l2-4.5"></path></svg>`,
  navigation: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>`
};

/* ─── HAVERSINE DISTANCE ENGINE ─── */
function haversineDistanceKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function formatDist(km) {
  if (km === undefined || km === null || isNaN(km)) return "";
  return km < 1 ? `${Math.round(km * 1000)} m` : `${km.toFixed(1)} km`;
}

/* ─── PRECOMPUTE CO-LOCATION HUBS (<= 150m) ─── */
ALL_STORES.forEach(s => {
  s._isCoLocation = ALL_STORES.some(o => 
    o.n !== s.n && 
    o.brand !== s.brand && 
    haversineDistanceKm(s.lat, s.lng, o.lat, o.lng) <= 0.15
  );
});

function loadScriptOnce(src, globalCheck) {
  if (globalCheck()) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`無法載入 ${src}`));
    document.head.appendChild(script);
  });
}

function loadStyleOnce(href) {
  if (document.querySelector(`link[href="${href}"]`)) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = href;
  document.head.appendChild(link);
}

function ensureShopeeData() {
  if (shopeeDataLoaded) return Promise.resolve();
  if (shopeeLoadPromise) return shopeeLoadPromise;
  loadStyleOnce("vendor/leaflet.markercluster/MarkerCluster.css");
  loadStyleOnce("vendor/leaflet.markercluster/MarkerCluster.Default.css");
  shopeeLoadPromise = Promise.all([
    loadScriptOnce("shopee_stores_data.js", () => Array.isArray(window.SHOPEE_STORES)),
    loadScriptOnce("vendor/leaflet.markercluster/leaflet.markercluster.js", () => typeof L.markerClusterGroup === "function").catch(() => {})
  ]).then(() => {
    const incoming = window.SHOPEE_STORES || [];
    incoming.forEach(s => { s._isCoLocation = false; });
    ALL_STORES.push(...incoming);
    shopeeDataLoaded = true;
    initDropdowns();
    initBrandPills();
  }).finally(() => { shopeeLoadPromise = null; });
  return shopeeLoadPromise;
}

/* ─── BASE MAP TILES CONFIG (Google Maps High-Res Tiles) ─── */
const TILE_LAYERS = {
  mono: L.tileLayer("https://mt{s}.google.com/vt/lyrs=m&hl=zh-TW&x={x}&y={y}&z={z}", {
    className: "tiles-google-mono",
    maxZoom: 20,
    subdomains: ['0', '1', '2', '3'],
    attribution: 'Map data &copy; Google Maps'
  }),
  satellite: L.tileLayer("https://mt{s}.google.com/vt/lyrs=y&hl=zh-TW&x={x}&y={y}&z={z}", {
    className: "tiles-google-satellite",
    maxZoom: 20,
    subdomains: ['0', '1', '2', '3'],
    attribution: 'Imagery &copy; Google Maps'
  }),
  color: L.tileLayer("https://mt{s}.google.com/vt/lyrs=m&hl=zh-TW&x={x}&y={y}&z={z}", {
    className: "tiles-google-color",
    maxZoom: 20,
    subdomains: ['0', '1', '2', '3'],
    attribution: 'Map data &copy; Google Maps'
  })
};

/* ─── SECTION 3: 6 METROPOLITAN REGION SPATIAL BOUNDARIES ─── */
const REGION_DATA = {
  taipei: {
    name: "大台北生活圈",
    cities: ["基隆市", "台北市", "新北市"],
    color: "#0058A3",
    coords: [
      [25.298, 121.538], [25.285, 121.585], [25.207, 121.691], [25.158, 121.765],
      [25.127, 121.921], [25.008, 122.000], [24.960, 121.950], [24.890, 121.780],
      [24.770, 121.520], [24.810, 121.430], [24.950, 121.340], [25.090, 121.330],
      [25.170, 121.410], [25.285, 121.515], [25.298, 121.538]
    ]
  },
  taoyuan_hsinchu: {
    name: "桃竹苗生活圈",
    cities: ["桃園市", "新竹市", "新竹縣", "苗栗縣"],
    color: "#7C3AED",
    coords: [
      [25.130, 121.240], [25.100, 121.400], [24.850, 121.400], [24.720, 121.430],
      [24.460, 121.260], [24.380, 121.230], [24.310, 120.840], [24.380, 120.760],
      [24.440, 120.630], [24.570, 120.700], [24.710, 120.850], [24.850, 120.920],
      [24.990, 121.010], [25.130, 121.240]
    ]
  },
  central: {
    name: "中台灣生活圈",
    cities: ["台中市", "彰化縣", "南投縣", "雲林縣"],
    color: "#C2410C",
    coords: [
      [24.400, 120.570], [24.330, 120.830], [24.280, 121.030], [24.140, 121.270],
      [23.950, 121.250], [23.750, 121.150], [23.470, 120.957], [23.530, 120.800],
      [23.580, 120.680], [23.550, 120.250], [23.680, 120.140], [23.950, 120.320],
      [24.120, 120.400], [24.310, 120.550], [24.400, 120.570]
    ]
  },
  south: {
    name: "南台灣生活圈",
    cities: ["嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"],
    color: "#15803D",
    coords: [
      [23.420, 120.120], [23.600, 120.570], [23.470, 120.950], [23.250, 120.920],
      [22.620, 120.760], [22.250, 120.750], [22.180, 120.880], [21.900, 120.850],
      [21.920, 120.735], [22.080, 120.700], [22.450, 120.450], [22.580, 120.270],
      [22.950, 120.170], [23.150, 120.060], [23.310, 120.110], [23.420, 120.120]
    ]
  },
  east_offshore: {
    name: "東部與離島生活圈",
    cities: ["宜蘭縣", "花蓮縣", "台東縣", "澎湖縣", "金門縣"],
    color: "#BE123C",
    multiCoords: [
      // Eastern Taiwan Corridor
      [
        [24.960, 121.920], [24.580, 121.870], [24.300, 121.750], [24.020, 121.630],
        [23.500, 121.510], [23.130, 121.410], [22.880, 121.230], [22.680, 121.150],
        [22.350, 120.920], [22.350, 120.750], [22.750, 121.000], [23.100, 121.100],
        [23.500, 121.250], [23.850, 121.400], [24.150, 121.250], [24.400, 121.350],
        [24.750, 121.500], [24.920, 121.750], [24.960, 121.920]
      ],
      // Penghu
      [
        [23.720, 119.520], [23.720, 119.680], [23.500, 119.680], [23.500, 119.520], [23.720, 119.520]
      ],
      // Kinmen
      [
        [24.540, 118.230], [24.540, 118.480], [24.400, 118.480], [24.400, 118.230], [24.540, 118.230]
      ]
    ]
  }
};

/* ─── MAP INITIALIZATION ─── */
const map = L.map("map", { zoomControl: false, attributionControl: false });
map.on("zoomend load", () => syncMarkerOverviewMode());
map.setView([23.75, 120.95], 8);

/* ─── GOOGLE MAPS NAVIGATION CONTROLS (My Location + Zoom In/Out) ─── */
const googleNavControl = L.control({ position: "bottomleft" });
googleNavControl.onAdd = function(map) {
  const container = L.DomUtil.create("div", "google-nav-control-group");
  container.innerHTML = `
    <button class="btn-google-locate" id="btnMapLocate" title="顯示我的位置 (回到所在座標)" role="button" aria-label="顯示我的位置">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="7"></circle>
        <line x1="12" y1="2" x2="12" y2="5"></line>
        <line x1="12" y1="19" x2="12" y2="22"></line>
        <line x1="2" y1="12" x2="5" y2="12"></line>
        <line x1="20" y1="12" x2="23" y2="12"></line>
        <circle cx="12" cy="12" r="2.5" fill="currentColor"></circle>
      </svg>
    </button>
    <div class="google-zoom-box">
      <button class="btn-google-zoom" id="btnMapZoomIn" title="放大地圖" role="button" aria-label="放大地圖">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
      <div class="google-zoom-divider"></div>
      <button class="btn-google-zoom" id="btnMapZoomOut" title="縮小地圖" role="button" aria-label="縮小地圖">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
    </div>
  `;
  L.DomEvent.disableClickPropagation(container);
  L.DomEvent.disableScrollPropagation(container);
  return container;
};
googleNavControl.addTo(map);

const mapLocateBtn = document.getElementById("btnMapLocate");
if (mapLocateBtn) {
  mapLocateBtn.onclick = (e) => {
    e.stopPropagation();
    locateUser();
  };
}
const zoomInBtn = document.getElementById("btnMapZoomIn");
if (zoomInBtn) {
  zoomInBtn.onclick = (e) => {
    e.stopPropagation();
    map.zoomIn();
  };
}
const zoomOutBtn = document.getElementById("btnMapZoomOut");
if (zoomOutBtn) {
  zoomOutBtn.onclick = (e) => {
    e.stopPropagation();
    map.zoomOut();
  };
}

let currentTile = TILE_LAYERS.mono;
currentTile.addTo(map);

/* ─── APPLICATION STATE ─── */
let activeBrand = "";
let activeDatasetMode = "home";
let selectedKey = null;
let markers = {};
let filteredStores = [];
let viewMode = "cards";
let highContrastPins = false;
let isSidebarCollapsed = false;
let isViewportSync = false;
let currentDetailStore = null;

// Catchment Buffer Circle State (P1 Feature)
let currentRadiusKm = 3.0;
let bufferCircle = null;
let isBufferCircleEnabled = true;

// GPS Location State (P1 Feature: Google Maps-like re-centering with session cache)
let userLocation = null;
try {
  const cachedLat = sessionStorage.getItem("taiwan_user_lat");
  const cachedLng = sessionStorage.getItem("taiwan_user_lng");
  if (cachedLat && cachedLng) {
    userLocation = { lat: parseFloat(cachedLat), lng: parseFloat(cachedLng) };
  }
} catch (e) {}
let userLocationMarker = null;
let isSortedByDistance = false;

// Regional Boundary Spatial Layer State (Section 3 Feature)
let activeRegionLayer = null;
let currentActiveRegionKey = "all";

// Brand PK Mode State (Section 4)
let isPkMode = false;
let pkBrands = ["IKEA", "宜得利"];

/* ─── GOOGLE MAPS URL GENERATOR ─── */
function getGmapsSearchUrl(s) {
  const q = s.clean_query || `${s.brand} ${s.store_name} ${s.address}`;
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
}

function getStatusBadge(s) {
  if (s.status_category === "現行營運中") {
    return `<span class="status-pill status-active">${SVG.check} 現行營運</span>`;
  }
  if (s.status_category === "暫停營業") {
    return `<span class="status-pill status-paused">${SVG.pause} 暫停營業</span>`;
  }
  return `<span class="status-pill status-closed">${SVG.archive} 已歇業</span>`;
}

function makeMarkerIcon(s, isNewlyOpened = false) {
  const cfg = BRANDS[s.brand] || { color: "#0058A3", abbr: "?" };
  const contrastClass = highContrastPins ? " high-contrast-pin" : "";
  const pulseClass = isNewlyOpened ? " marker-new-pulse" : "";
  const svgHtml = `<svg width="28" height="36" viewBox="0 0 28 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M14 36 C11 27 1 20.5 1 13.5 A 13 13 0 1 1 27 13.5 C27 20.5 17 27 14 36 Z" fill="${cfg.color}" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <text x="14" y="14" text-anchor="middle" dominant-baseline="central" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="11px" letter-spacing="-0.3px">${cfg.abbr}</text>
  </svg>`;
  return L.divIcon({
    className: "brand-pin-marker" + contrastClass + pulseClass,
    html: svgHtml,
    iconSize: [28, 36],
    iconAnchor: [14, 36],
    popupAnchor: [0, -38]
  });
}

function makePopupHtml(s) {
  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const key = "s" + s.n;

  return `<div class="popup-box">
    <div class="popup-header-row">
      <span class="popup-brand-badge" style="background:${cfg.color}">${s.brand}</span>
      ${getStatusBadge(s)}
    </div>
    <div class="popup-title">${s.store_name}</div>
    <div class="popup-meta">
      <span>${s.city} ${s.district || ""}</span>
    </div>
    <div class="tag-container" style="margin-bottom:8px">
      <span class="tag-badge tag-channel">${SVG.store} ${s.store_format || s.channel_format}</span>
      ${s.opened_year ? `<span class="tag-badge tag-opened-year">${SVG.clock} ${s.opened_year} 開幕</span>` : ""}
      ${s._isCoLocation ? `<span class="tag-badge tag-colocation">${SVG.battle} 附近有其他品牌</span>` : ""}
      ${s._userDist !== undefined && isSortedByDistance ? `<span class="card-dist-badge">${SVG.gps} 距您 ${formatDist(s._userDist)}</span>` : ""}
    </div>
    <div class="popup-addr">
      ${SVG.pin}
      <span>${s.address}</span>
    </div>
    ${(s.status_category !== '現行營運中' && s.note) ? `<div class="popup-note-box">${s.note}</div>` : ''}
    <div class="popup-action-row">
      <button class="pop-btn pop-btn-emph" onclick="triggerRoutePlanningByKey('${key}')" title="規劃前往 ${s.store_name} 路線">
        ${SVG.route} <span>規劃路線</span>
      </button>
      <a class="pop-btn pop-btn-secondary" href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener" title="在 Google Maps 開啟完整導航">
        ${SVG.external} <span class="btn-text-full">在 Google Maps 開啟</span><span class="btn-text-compact">Google 地圖</span>
      </a>
    </div>
  </div>`;
}

/* ─── DROPDOWNS INITIALIZATION & TWO-WAY LINKAGE ─── */
function getScopedStorePoolForDropdowns() {
  const allowedBrands = DATASET_BRANDS[activeDatasetMode] || [];
  const statEl = document.getElementById("selStatus");
  const stat = statEl ? statEl.value : "";
  const chanEl = document.getElementById("selChannel");
  const chan = chanEl ? chanEl.value : "";
  return ALL_STORES.filter(s => {
    if (!allowedBrands.includes(s.brand)) return false;
    if (stat && s.status_category !== stat) return false;
    if (chan && (s.store_format || s.channel_format) !== chan) return false;
    return true;
  });
}

function initDropdowns() {
  const citySel = document.getElementById("selCity");
  const selectedCity = citySel.value;
  citySel.innerHTML = '<option value="">全部縣市</option>';
  const pool = getScopedStorePoolForDropdowns();
  const counts = {};
  pool.forEach(s => {
    if (s.city) counts[s.city] = (counts[s.city] || 0) + 1;
  });
  Object.keys(counts).sort((a, b) => counts[b] - counts[a]).forEach(c => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = `${c} (${counts[c]})`;
    citySel.appendChild(opt);
  });
  if (selectedCity && counts[selectedCity]) {
    citySel.value = selectedCity;
  } else {
    citySel.value = "";
  }
  updateDistrictDropdown(citySel.value);
}

function updateDistrictDropdown(selectedCity) {
  const distSel = document.getElementById("selDistrict");
  const previousVal = distSel.value;

  if (selectedCity) {
    distSel.innerHTML = '<option value="">全部行政區</option>';
    const pool = getScopedStorePoolForDropdowns().filter(s => s.city === selectedCity);
    const counts = {};
    pool.forEach(s => {
      if (s.district) counts[s.district] = (counts[s.district] || 0) + 1;
    });
    Object.keys(counts).sort((a, b) => counts[b] - counts[a]).forEach(d => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = `${d} (${counts[d]})`;
      distSel.appendChild(opt);
    });
    if (previousVal && counts[previousVal]) {
      distSel.value = previousVal;
    } else {
      distSel.value = "";
    }
  } else {
    distSel.innerHTML = '<option value="">全部行政區（請先選縣市）</option>';
    distSel.value = "";
  }
}

/* ─── QUICK BRAND CHIPS INITIALIZATION ─── */
function initBrandPills() {
  const container = document.getElementById("brandPills");
  container.innerHTML = "";

  const allChip = document.createElement("button");
  allChip.className = "brand-chip" + (!activeBrand && !isPkMode ? " active" : "");
  allChip.dataset.brand = "";
  allChip.innerHTML = `<span class="dot" style="background:#0058A3"></span> 全部 <span class="cnt">${ALL_STORES.length}</span>`;
  allChip.onclick = () => {
    if (isPkMode) return;
    activeBrand = "";
    render();
  };
  container.appendChild(allChip);

  BRAND_KEYS.forEach(b => {
    const cfg = BRANDS[b];
    const count = ALL_STORES.filter(s => s.brand === b).length;
    const chip = document.createElement("button");
    chip.className = "brand-chip";
    chip.dataset.brand = b;
    chip.dataset.dataset = Object.keys(DATASET_BRANDS).find(key => DATASET_BRANDS[key].includes(b)) || "home";
    chip.innerHTML = `<span class="dot" style="background:${cfg.color}"></span> ${b} <span class="cnt">${count}</span>`;
    chip.onclick = () => {
      if (isPkMode) {
        if (pkBrands.includes(b)) {
          if (pkBrands.length > 1) {
            pkBrands = pkBrands.filter(item => item !== b);
          }
        } else {
          if (pkBrands.length >= 2) {
            pkBrands[1] = b;
          } else {
            pkBrands.push(b);
          }
        }
        updatePkBanner();
        render();
        return;
      }
      activeBrand = (activeBrand === b) ? "" : b;
      render();
    };
    container.appendChild(chip);
  });
}

function syncDatasetControls() {
  document.querySelectorAll(".dataset-switch-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.dataset === activeDatasetMode);
  });
  document.querySelectorAll('.brand-chip[data-brand]:not([data-brand=""])').forEach(chip => {
    chip.style.display = chip.dataset.dataset === activeDatasetMode ? "inline-flex" : "none";
  });
  const compareButton = document.getElementById("btnPkMode");
  if (compareButton) {
    const canCompareBrands = activeDatasetMode === "home";
    compareButton.style.display = canCompareBrands ? "inline-flex" : "none";
    compareButton.disabled = !canCompareBrands;
    compareButton.setAttribute("aria-hidden", canCompareBrands ? "false" : "true");
  }
}

/* ─── DYNAMIC FACETED BRAND PILLS COUNT SYNCHRONIZATION ─── */
function updateBrandPillsCounts(nonBrandPool) {
  const allChip = document.querySelector('.brand-chip[data-brand=""]');
  if (allChip) {
    const cntEl = allChip.querySelector(".cnt");
    if (cntEl) cntEl.textContent = nonBrandPool.length;
  }

  const brandCounts = {};
  BRAND_KEYS.forEach(b => { brandCounts[b] = 0; });
  nonBrandPool.forEach(s => {
    if (brandCounts[s.brand] !== undefined) {
      brandCounts[s.brand]++;
    }
  });

  BRAND_KEYS.forEach(b => {
    const chip = document.querySelector(`.brand-chip[data-brand="${b}"]`);
    if (chip) {
      const cntEl = chip.querySelector(".cnt");
      const c = brandCounts[b] || 0;
      if (cntEl) cntEl.textContent = c;
      chip.classList.toggle("zero-count", c === 0);
    }
  });
}

function syncBrandPills() {
  document.querySelectorAll(".brand-chip").forEach(chip => {
    const b = chip.dataset.brand;
    if (isPkMode) {
      chip.classList.toggle("active", pkBrands.includes(b));
    } else {
      if (b === "") {
        chip.classList.toggle("active", activeBrand === "");
      } else {
        chip.classList.toggle("active", activeBrand === b);
      }
    }
  });
}

/* ─── BRAND PK MODE (Section 4) ─── */
function togglePkMode() {
  if (activeDatasetMode !== "home" && !isPkMode) return;
  isPkMode = !isPkMode;
  document.getElementById("btnPkMode").classList.toggle("active", isPkMode);
  const banner = document.getElementById("pkBannerBox");
  banner.style.display = isPkMode ? "flex" : "none";
  if (isPkMode) {
    activeBrand = "";
    if (pkBrands.length < 2) pkBrands = ["IKEA", "宜得利"];
  }
  render();
}

function updatePkBanner(poolToUse) {
  if (!isPkMode) return;
  const b1 = pkBrands[0] || "IKEA";
  const b2 = pkBrands[1] || "宜得利";
  const c1 = BRANDS[b1] ? BRANDS[b1].color : "#0058A3";
  const c2 = BRANDS[b2] ? BRANDS[b2].color : "#00A396";
  const targetPool = poolToUse || getNonBrandFilteredPool();
  const count1 = targetPool.filter(s => s.brand === b1).length;
  const count2 = targetPool.filter(s => s.brand === b2).length;
  const total = count1 + count2 || 1;
  const pct1 = Math.round((count1 / total) * 100);
  const pct2 = 100 - pct1;

  document.getElementById("pkSegA").style.width = `${pct1}%`;
  document.getElementById("pkSegA").style.background = c1;
  document.getElementById("pkSegB").style.width = `${pct2}%`;
  document.getElementById("pkSegB").style.background = c2;

  document.getElementById("pkLabelA").style.color = c1;
  document.getElementById("pkLabelA").textContent = `${b1} ${count1} 間 (${pct1}%)`;
  document.getElementById("pkLabelB").style.color = c2;
  document.getElementById("pkLabelB").textContent = `${b2} ${count2} 間 (${pct2}%)`;
}

document.getElementById("btnPkMode").onclick = togglePkMode;
document.getElementById("btnExitPk").onclick = togglePkMode;

/* ─── REGION QUICK JUMP BAR & SPATIAL BOUNDARY ENVELOPE (Section 3) ─── */
function updateActiveRegionTooltip() {
  if (!activeRegionLayer || !currentActiveRegionKey || currentActiveRegionKey === "all") return;
  const reg = REGION_DATA[currentActiveRegionKey];
  if (!reg) return;

  const regStores = filteredStores.filter(s => reg.cities.includes(s.city));
  const selectedStatus = document.getElementById("selStatus").value;
  const statusLabel = selectedStatus || "全部狀態";
  const totalStoresInRegion = ALL_STORES.filter(s =>
    reg.cities.includes(s.city) && (!selectedStatus || s.status_category === selectedStatus)
  ).length;
  const isFiltered = regStores.length !== totalStoresInRegion;

  let countPillHtml = "";
  if (regStores.length === 0) {
    countPillHtml = `<span class="pill-cnt pill-cnt-zero">目前篩選：0 間</span><span class="pill-filter-tag">/ 涵蓋縣市・${statusLabel}：${totalStoresInRegion} 間</span>`;
  } else if (isFiltered) {
    countPillHtml = `<span class="pill-cnt pill-cnt-filtered">目前篩選：${regStores.length} 間</span><span class="pill-filter-tag">/ 涵蓋縣市・${statusLabel}：${totalStoresInRegion} 間</span>`;
  } else {
    countPillHtml = `<span class="pill-cnt">涵蓋縣市・${statusLabel}：${totalStoresInRegion} 間</span>`;
  }

  activeRegionLayer.setTooltipContent(`
    <div class="region-pill-box">
      <span class="pill-dot" style="background:${reg.color}"></span>
      <strong>${reg.name}</strong>
      ${countPillHtml}
    </div>
  `);
}

function jumpToRegion(regKey) {
  // Clear any previously displayed regional boundary polygon
  if (activeRegionLayer) {
    map.removeLayer(activeRegionLayer);
    activeRegionLayer = null;
  }
  currentActiveRegionKey = regKey;
  updateLocateButtonsState(userLocation ? "active" : "reset");

  // Update active class on button
  document.querySelectorAll(".btn-region-jump").forEach(b => {
    b.classList.toggle("active", b.dataset.region === regKey);
  });

  if (regKey === "all") {
    map.flyTo([23.85, 120.95], 8, { duration: 0.8 });
    return;
  }

  const reg = REGION_DATA[regKey];
  if (!reg) return;

  // Create regional boundary polygon (Single or MultiPolygon)
  let poly;
  if (reg.multiCoords) {
    poly = L.polygon(reg.multiCoords, {
      color: reg.color,
      weight: 3,
      opacity: 1,
      dashArray: "8, 6",
      fillColor: reg.color,
      fillOpacity: 0.18,
      className: "region-boundary-poly"
    });
  } else {
    poly = L.polygon(reg.coords, {
      color: reg.color,
      weight: 3,
      opacity: 1,
      dashArray: "8, 6",
      fillColor: reg.color,
      fillOpacity: 0.18,
      className: "region-boundary-poly"
    });
  }

  poly.bindTooltip("", {
    permanent: true,
    direction: "center",
    className: "custom-region-tooltip"
  });

  poly.addTo(map);
  activeRegionLayer = poly;

  // Dynamically calculate and render tooltip content based on current active filters
  updateActiveRegionTooltip();

  // Smoothly fit map to the region's spatial bounds with comfortable padding
  map.fitBounds(poly.getBounds(), { padding: [50, 50], maxZoom: 12, duration: 0.8 });
}

function initRegionJumpBar() {
  document.querySelectorAll(".btn-region-jump").forEach(btn => {
    btn.onclick = () => {
      const regKey = btn.dataset.region;
      // If clicking already-active region, toggle back to "all" (toggle off)
      if (btn.classList.contains("active") && regKey !== "all") {
        jumpToRegion("all");
      } else {
        jumpToRegion(regKey);
      }
    };
  });
}

/* ─── GPS GEOLOCATION ENGINE (P1 Feature: Google Maps-like Location Re-centering) ─── */
function updateLocateButtonsState(state) {
  const sidebarBtn = document.getElementById("btnLocateMe");
  const mapBtn = document.getElementById("btnMapLocate");

  if (state === "loading") {
    if (sidebarBtn) {
      sidebarBtn.classList.add("loading");
      sidebarBtn.querySelector("span").textContent = "定位中…";
    }
    if (mapBtn) {
      mapBtn.classList.add("loading");
      mapBtn.title = "定位中…";
    }
  } else if (state === "active") {
    if (sidebarBtn) {
      sidebarBtn.classList.remove("loading");
      sidebarBtn.classList.add("active");
      sidebarBtn.querySelector("span").textContent = "我的位置";
      sidebarBtn.title = "點擊立即回到我的目前所在位置（已定位）";
    }
    if (mapBtn) {
      mapBtn.classList.remove("loading");
      mapBtn.classList.add("active");
      mapBtn.title = "已定位（點擊立即回歸我的目前位置）";
    }
  } else if (state === "reset") {
    if (sidebarBtn) {
      sidebarBtn.classList.remove("loading");
      sidebarBtn.classList.remove("active");
      sidebarBtn.querySelector("span").textContent = "離我最近";
      sidebarBtn.title = "以目前位置排序全台門市";
    }
    if (mapBtn) {
      mapBtn.classList.remove("loading");
      mapBtn.classList.remove("active");
      mapBtn.title = "顯示我的位置 (回到所在座標)";
    }
  }
}

function locateUser() {
  // If user location is ALREADY known (in memory or session cache):
  // Immediately re-center to user position like Google Maps without ANY browser permission prompts!
  if (userLocation) {
    if (!userLocationMarker) {
      const userIcon = L.divIcon({
        className: "user-gps-pulse-marker",
        html: `<div class="pulse-ring"></div><div class="user-dot"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      userLocationMarker = L.marker([userLocation.lat, userLocation.lng], { icon: userIcon, zIndexOffset: 4000 })
        .addTo(map)
        .bindPopup(`<div style="font-weight:700;padding:4px">您的目前所在位置</div>`);
      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(userLocation.lat, userLocation.lng, s.lat, s.lng);
      });
    }

    map.flyTo([userLocation.lat, userLocation.lng], 14, { duration: 0.8 });
    setTimeout(() => {
      if (userLocationMarker) userLocationMarker.openPopup();
    }, 850);
    updateLocateButtonsState("active");
    if (!isSortedByDistance) {
      isSortedByDistance = true;
      render();
    }
    return;
  }

  // First-time location acquisition
  if (!navigator.geolocation) {
    alert("您的瀏覽器環境不支援地理定位功能");
    return;
  }

  updateLocateButtonsState("loading");

  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude, longitude } = pos.coords;
      userLocation = { lat: latitude, lng: longitude };

      // Cache to sessionStorage to completely avoid permission prompts across reloads
      try {
        sessionStorage.setItem("taiwan_user_lat", String(latitude));
        sessionStorage.setItem("taiwan_user_lng", String(longitude));
      } catch (e) {}

      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(latitude, longitude, s.lat, s.lng);
      });

      if (userLocationMarker) map.removeLayer(userLocationMarker);
      const userIcon = L.divIcon({
        className: "user-gps-pulse-marker",
        html: `<div class="pulse-ring"></div><div class="user-dot"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      userLocationMarker = L.marker([latitude, longitude], { icon: userIcon, zIndexOffset: 4000 })
        .addTo(map)
        .bindPopup(`<div style="font-weight:700;padding:4px">您的目前所在位置</div>`);

      map.flyTo([latitude, longitude], 14, { duration: 0.8 });
      setTimeout(() => {
        if (userLocationMarker) userLocationMarker.openPopup();
      }, 850);

      updateLocateButtonsState("active");
      isSortedByDistance = true;
      render();
    },
    err => {
      updateLocateButtonsState("reset");
      alert("無法取得您的目前位置資訊（請確認已允許瀏覽器定位權限）");
    },
    { timeout: 10000, enableHighAccuracy: true }
  );
}

document.getElementById("btnLocateMe").onclick = locateUser;

/* ─── NON-BRAND FILTER POOL ENGINE (For Dynamic Faceted Counts) ─── */
function getNonBrandFilteredPool() {
  const q = document.getElementById("q").value.trim().toLowerCase();
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const chan = document.getElementById("selChannel").value;
  const stat = document.getElementById("selStatus").value;

  let pool = ALL_STORES.filter(s => {
    if (!(DATASET_BRANDS[activeDatasetMode] || []).includes(s.brand)) return false;
    if (city && s.city !== city) return false;
    if (dist && s.district !== dist) return false;

    if (chan && (s.store_format || s.channel_format) !== chan) {
      return false;
    }

    if (stat && s.status_category !== stat) return false;

    if (q) {
      const haystack = `${s.brand} ${s.store_name} ${s.city} ${s.district || ""} ${s.address} ${s.channel_format} ${s.store_type} ${s.note || ""}`.toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });

  if (isViewportSync && map) {
    const bounds = map.getBounds();
    pool = pool.filter(s => bounds.contains([s.lat, s.lng]));
  }

  return pool;
}

/* ─── CORE FILTER & RENDER ─── */
function render() {
  syncDatasetControls();
  const q = document.getElementById("q").value.trim().toLowerCase();
  document.getElementById("btnClearSearch").style.display = q ? "block" : "none";

  // 1. Get filtered pool based on non-brand criteria (channel, city, district, status, query, viewport)
  const nonBrandPool = getNonBrandFilteredPool();

  // 2. Dynamically update counts on all brand pills in real time!
  updateBrandPillsCounts(nonBrandPool);

  // 3. Update viewport status indicator & guidance hint
  const hintBar = document.getElementById("viewportHintBar");
  const hintText = document.getElementById("viewportHintText");
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;

  if (isViewportSync && map) {
    const curZoom = map.getZoom();
    if (curZoom <= 8) {
      document.getElementById("lblViewportIndicator").innerHTML = `地圖目前涵蓋全台：<strong>${nonBrandPool.length}</strong> 間`;
      if (hintBar) {
        hintBar.style.display = "flex";
        if (hintText) hintText.textContent = "目前地圖視野涵蓋全台。請滾動滑鼠滾輪放大或拖曳地圖，名錄將即時篩選畫面內門市！";
      }
    } else {
      const areaLabel = (city && dist) ? ` (${city} ${dist})` : (city ? ` (${city})` : "");
      document.getElementById("lblViewportIndicator").innerHTML = `目前地圖範圍${areaLabel}：<strong>${nonBrandPool.length}</strong> 間`;
      if (hintBar) hintBar.style.display = "none";
    }
  } else {
    let scopeDesc = "全台";
    if (city && dist) {
      scopeDesc = `${city} ${dist}`;
    } else if (city) {
      scopeDesc = city;
    }
    document.getElementById("lblViewportIndicator").textContent = `清單範圍：${scopeDesc}，共 ${nonBrandPool.length} 間`;
    if (hintBar) hintBar.style.display = "none";
  }

  // 4. Apply Brand Filter or PK Mode
  if (activeBrand && !isPkMode) {
    const brandHasStores = nonBrandPool.some(s => s.brand === activeBrand);
    if (!brandHasStores && nonBrandPool.length > 0) {
      activeBrand = "";
    }
  }

  let pool = nonBrandPool.filter(s => {
    if (isPkMode) {
      return pkBrands.includes(s.brand);
    }
    if (activeBrand && s.brand !== activeBrand) {
      return false;
    }
    return true;
  });

  // 5. Distance Sorting (P1 Feature: 離我最近)
  if (isSortedByDistance && userLocation) {
    pool.sort((a, b) => (a._userDist || 9999) - (b._userDist || 9999));
  }

  filteredStores = pool;
  if (isTimelineMode) {
    const tlPool = getTimelineStorePool();
    renderTimelineSparkline(tlPool);
    updateTimeline(timelineYear, false);
    return;
  }
  const brandSuffix = (activeBrand && !isPkMode) ? `（${activeBrand}）` : "";
  if (isViewportSync && map && map.getZoom() <= 8) {
    document.getElementById("lblCount").textContent = `${filteredStores.length} 間門市（全台視野）${brandSuffix}`;
  } else if (isViewportSync) {
    document.getElementById("lblCount").textContent = `${filteredStores.length} 間門市（地圖畫面內）${brandSuffix}`;
  } else {
    document.getElementById("lblCount").textContent = `${filteredStores.length} 間門市${brandSuffix}`;
  }
  document.getElementById("lblFloatingCount").textContent = filteredStores.length;
  syncBrandPills();
  if (isPkMode) updatePkBanner(nonBrandPool);
  renderMarkers();
  renderList();
  updateActiveRegionTooltip();
}

/* ─── MAP MARKERS ─── */
// 縮小到全台／跨縣市視野時，標記改成小圓點並隱藏品牌縮寫，避免文字互相重疊
// （地圖初始化時就會觸發，因此門檻直接寫在函式內，避免 const 尚未初始化）
function syncMarkerOverviewMode() {
  if (!map) return;
  map.getContainer().classList.toggle("map-overview", map.getZoom() <= 9);
}
function renderMarkers(pulseYear = null) {
  Object.values(markers).forEach(m => map.removeLayer(m));
  if (markerClusterLayer) {
    map.removeLayer(markerClusterLayer);
    markerClusterLayer.clearLayers();
    markerClusterLayer = null;
  }
  markers = {};

  const useClusters = activeDatasetMode === "ecommerce" && typeof L.markerClusterGroup === "function";
  if (useClusters) {
    markerClusterLayer = L.markerClusterGroup({
      chunkedLoading: true,
      chunkInterval: 80,
      chunkDelay: 24,
      maxClusterRadius: 52,
      disableClusteringAtZoom: 16,
      removeOutsideVisibleBounds: true
    });
  }
  const clusterMarkers = [];

  filteredStores.forEach(s => {
    const key = "s" + s.n;
    const isNewInYear = pulseYear && (s.opened_year === pulseYear);
    const mk = L.marker([s.lat, s.lng], { icon: makeMarkerIcon(s, isNewInYear) })
      .bindPopup(makePopupHtml(s), { className: "custom-popup", minWidth: 260, maxWidth: 320, autoPan: true, autoPanPadding: [24, 24] });

    if (markerClusterLayer) clusterMarkers.push(mk);
    else mk.addTo(map);

    mk.on("click", () => { selectStore(key, s, false); openStoreDrawer(s, "info"); });
    markers[key] = mk;
  });
  if (markerClusterLayer) {
    markerClusterLayer.addLayers(clusterMarkers);
    map.addLayer(markerClusterLayer);
  }
}

/* ─── STORE LIST ─── */
function renderList() {
  const container = document.getElementById("storeList");
  container.innerHTML = "";

  if (filteredStores.length === 0) {
    const ecommerceMessage = activeDatasetMode === "ecommerce" ? `
      <div class="title">電商取貨據點採獨立圖層</div>
      <div class="desc">蝦皮據點屬即時資料，正式同步前請使用官方查詢。</div>
      <a href="https://shopee.tw/m/spxservicepoint" target="_blank" rel="noopener" class="btn-card-gmap" style="margin-top:10px">${SVG.external} 開啟蝦皮官方據點查詢</a>
    ` : `
      <div class="title">找不到符合目前篩選條件的門市</div>
      <div class="desc">${isViewportSync ? "目前地圖視野範圍內無門市，請縮小地圖或關閉視野連動" : "請嘗試清空關鍵字或放寬篩選條件"}</div>
    `;
    container.innerHTML = `
      <div class="empty-state">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
        ${ecommerceMessage}
      </div>`;
    return;
  }

  if (viewMode === "cards") renderCards(container);
  else renderTable(container);
}

function renderCards(container) {
  const displayStores = activeDatasetMode === "ecommerce" ? filteredStores.slice(0, 200) : filteredStores;
  if (displayStores.length < filteredStores.length) {
    const notice = document.createElement("div");
    notice.className = "viewport-hint-bar";
    notice.style.display = "flex";
    notice.innerHTML = `<span>為維持流暢度，名錄先顯示 200 筆；可用縣市、行政區或關鍵字縮小範圍。地圖仍包含全部 ${filteredStores.length} 間。</span>`;
    container.appendChild(notice);
  }
  if (isSortedByDistance && userLocation) {
    const cardsWrap = document.createElement("div");
    displayStores.forEach(s => {
      cardsWrap.appendChild(createStoreCardElement(s));
    });
    container.appendChild(cardsWrap);
    return;
  }

  const groups = {};
  BRAND_KEYS.forEach(b => groups[b] = []);
  displayStores.forEach(s => { if (groups[s.brand]) groups[s.brand].push(s); });

  BRAND_KEYS.forEach(brand => {
    const list = groups[brand];
    if (!list.length) return;

    const cfg = BRANDS[brand];
    const hdr = document.createElement("div");
    hdr.className = "brand-section-header";
    hdr.style.background = cfg.color;
    hdr.innerHTML = `
      <div class="left-title">
        <span>${cfg.label}</span>
        <span class="count-tag">${list.length}</span>
      </div>
      <div class="chevron">${SVG.chevron}</div>
    `;

    let collapsed = false;
    hdr.onclick = () => {
      collapsed = !collapsed;
      hdr.classList.toggle("collapsed", collapsed);
      cardsWrap.style.display = collapsed ? "none" : "block";
    };
    container.appendChild(hdr);

    const cardsWrap = document.createElement("div");
    list.forEach(s => {
      cardsWrap.appendChild(createStoreCardElement(s));
    });
    container.appendChild(cardsWrap);
  });
}

function createStoreCardElement(s) {
  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const key = "s" + s.n;

  const card = document.createElement("div");
  const isArchived = s.status_category.includes("歷史");
  card.className = "store-card" + (isArchived ? " is-archived" : "");
  card.dataset.key = key;
  if (selectedKey === key) card.classList.add("selected");

  card.innerHTML = `
    <div class="card-top-bar">
      <span class="card-brand-tag" style="background:${cfg.color}">${s.brand}</span>
      <div style="display:flex;align-items:center;gap:4px">
        ${s._userDist !== undefined && isSortedByDistance ? `<span class="card-dist-badge">${SVG.gps} 距您 ${formatDist(s._userDist)}</span>` : ""}
        ${getStatusBadge(s)}
      </div>
    </div>
    <div class="card-name-title">${s.store_name}</div>
    <div class="card-meta-line">
      <span class="card-channel-pill">${s.region ? s.region + "地區" : ""}</span>
      <span>${s.city} ${s.district || ""}</span>
    </div>
    <div class="tag-container">
      <span class="tag-badge tag-channel">${SVG.store} ${s.store_format || s.channel_format}</span>
      ${s._isCoLocation ? `<span class="tag-badge tag-colocation">${SVG.battle} 附近有其他品牌</span>` : ""}
    </div>
    <div class="card-address-box">
      ${SVG.pin}
      <span>${s.address}</span>
    </div>
    <div class="card-actions-row">
      <button class="card-action-btn card-action-emph" onclick="event.stopPropagation(); triggerRoutePlanning(ALL_STORES.find(item => item.n === ${s.n}))" title="規劃前往 ${s.store_name} 路線">
        ${SVG.route} <span>規劃路線</span>
      </button>
      <a class="card-action-btn card-action-secondary" href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener" onclick="event.stopPropagation();" title="在 Google Maps 開啟完整導航">
        ${SVG.external} <span class="btn-text-full">在 Google Maps 開啟</span><span class="btn-text-compact">Google 地圖</span>
      </a>
    </div>
  `;

  card.onclick = (e) => {
    if (e.target.closest("a") || e.target.closest(".card-action-btn") || e.target.closest(".btn-card-view-detail")) return;
    selectStore(key, s, true);
    openStoreDrawer(s, "info");
  };

  return card;
}

function renderTable(container) {
  const wrap = document.createElement("div");
  wrap.style.overflowX = "auto";
  const tbl = document.createElement("table");
  tbl.style.cssText = "width:100%;border-collapse:collapse;font-size:12px;background:#fff;border-radius:8px;overflow:hidden";
  tbl.innerHTML = `
    <thead style="position:sticky;top:0;background:#0058A3;color:#fff;z-index:2">
      <tr>
        <th style="padding:8px 10px;text-align:left;white-space:nowrap">品牌 / 門市</th>
        <th style="padding:8px 10px;white-space:nowrap">地區</th>
        <th style="padding:8px 10px;white-space:nowrap">門市型態</th>
        <th style="padding:8px 10px;white-space:nowrap">地址與導航</th>
        ${isSortedByDistance ? `<th style="padding:8px 10px;white-space:nowrap">距離</th>` : ""}
        <th style="padding:8px 10px;white-space:nowrap">營運狀態</th>
      </tr>
    </thead>
    <tbody id="tblBody"></tbody>`;
  wrap.appendChild(tbl);
  container.appendChild(wrap);
  const tbody = tbl.querySelector("#tblBody");

  const displayStores = activeDatasetMode === "ecommerce" ? filteredStores.slice(0, 200) : filteredStores;
  if (displayStores.length < filteredStores.length) {
    const notice = document.createElement("div");
    notice.className = "viewport-hint-bar";
    notice.style.display = "flex";
    notice.textContent = `為維持流暢度，表格先顯示 200 筆；地圖仍包含全部 ${filteredStores.length} 間。`;
    container.appendChild(notice);
  }
  displayStores.forEach(s => {
    const key = "s" + s.n;
    const cfg = BRANDS[s.brand] || { color: "#0058A3" };
    const tableBrand = cfg.tableLabel || s.brand;
    const tableStoreName = s.store_name.startsWith(s.brand + " ")
      ? s.store_name.slice(s.brand.length + 1)
      : s.store_name;
    const tr = document.createElement("tr");
    tr.style.cssText = "cursor:pointer;border-bottom:1px solid #E2E8F0;transition:background 0.1s";
    tr.dataset.key = key;
    if (selectedKey === key) tr.style.background = "#EBF4FC";

    tr.innerHTML = `
      <td style="padding:8px 10px;min-width:128px">
        <span title="${s.brand}" style="display:inline-flex;white-space:nowrap;background:${cfg.color};color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:4px">${tableBrand}</span>
        ${s._isCoLocation ? `<span class="tag-badge tag-colocation" title="150 公尺內有其他品牌門市" style="font-size:9.5px;padding:1px 4px;white-space:nowrap">${SVG.battle} 鄰近品牌</span>` : ""}<br>
        <strong title="${tableStoreName}" style="font-size:12.5px;color:#111;margin-top:4px;display:block;white-space:nowrap;max-width:150px;overflow:hidden;text-overflow:ellipsis">${tableStoreName}</strong>
      </td>
      <td style="padding:8px 10px;white-space:nowrap">${s.city}<br><span style="color:#64748B;font-size:11px">${s.district||""}</span></td>
      <td style="padding:8px 10px;white-space:nowrap;font-size:11px;color:#475569">${s.store_format || s.channel_format}</td>
      <td style="padding:8px 10px">
        <a href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener" style="color:#0058A3;font-weight:700;font-size:11.5px;text-decoration:none;display:inline-flex;align-items:center;gap:4px" onclick="event.stopPropagation()">
          ${SVG.external} ${s.address}
        </a>
      </td>
      ${isSortedByDistance ? `
        <td style="padding:8px 10px;white-space:nowrap">
          <span class="card-dist-badge">${formatDist(s._userDist)}</span>
        </td>
      ` : ""}
      <td style="padding:8px 10px;white-space:nowrap">
        ${getStatusBadge(s)}
      </td>`;
    tr.onmouseenter = () => { if (selectedKey !== key) tr.style.background = "#F1F5F9"; };
    tr.onmouseleave = () => { if (selectedKey !== key) tr.style.background = ""; };
    tr.onclick = (e) => {
      if (e.target.tagName === "A") return;
      selectStore(key, s, true);
      openStoreDrawer(s, "info");
    };
    tbody.appendChild(tr);
  });
}

/* ─── P1: CATCHMENT BUFFER CIRCLE & DRAWER CONTROLLER ─── */
let currentDetailTab = "info";

document.getElementById("detailTabsBar").addEventListener("keydown", (e) => {
  if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
  const tabs = [...document.querySelectorAll(".detail-tab-btn")];
  const i = tabs.findIndex(b => b.classList.contains("active"));
  const next = tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
  switchDetailTab(next.dataset.tab);
  next.focus();
  e.preventDefault();
});

function switchDetailTab(tabName) {
  currentDetailTab = tabName;
  const tabs = document.querySelectorAll(".detail-tab-btn");
  tabs.forEach(btn => {
    const on = btn.dataset.tab === tabName;
    btn.classList.toggle("active", on);
    btn.setAttribute("aria-selected", on ? "true" : "false");
    btn.tabIndex = on ? 0 : -1;
  });

  const panes = document.querySelectorAll(".detail-tab-pane");
  const targetPaneId = "paneDetail" + tabName.charAt(0).toUpperCase() + tabName.slice(1);
  panes.forEach(pane => {
    pane.classList.toggle("active", pane.id === targetPaneId);
  });

  if (tabName === "route" && currentDetailStore && runRouteFetch) {
    runRouteFetch();
  }
}

function openStoreDrawerByKey(key) {
  const s = ALL_STORES.find(item => "s" + item.n === key);
  if (s) openStoreDrawer(s, "info");
}

function triggerRoutePlanningByKey(key) {
  const s = ALL_STORES.find(item => "s" + item.n === key);
  if (s) triggerRoutePlanning(s);
}

function triggerRoutePlanning(s) {
  if (!s) return;
  if (map) map.closePopup();
  const key = "s" + s.n;
  selectStore(key, s, true);
  openStoreDrawer(s, "route");
}

function openStoreDrawer(s, preferredTab = null) {
  currentDetailStore = s;

  if (map) map.closePopup();

  if (isTimelineMode && timelinePlaying) {
    pauseTimeline();
  }

  if (isSidebarCollapsed) {
    expandSidebar();
  }

  document.getElementById("sidebarListSection").style.display = "none";
  const detailSection = document.getElementById("sidebarDetailSection");
  detailSection.style.display = "flex";

  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const topBadge = document.getElementById("detailTopBrandBadge");
  topBadge.textContent = s.brand;
  topBadge.style.background = cfg.color;

  updateBufferCircleOnMap(s);

  // Render Pinned Identity Header
  const pinnedHdr = document.getElementById("detailPinnedHeader");
  if (pinnedHdr) {
    pinnedHdr.innerHTML = `
      <div class="detail-meta-row">
        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">
          ${getStatusBadge(s)}
          ${s._isCoLocation ? `<span class="tag-badge tag-colocation">${SVG.battle} 附近有其他品牌</span>` : ""}
        </div>
        ${(s._userDist !== undefined && s._userDist !== null) ? `<span class="card-dist-badge">${formatDist(s._userDist)}</span>` : ""}
      </div>
      <h2 class="detail-title" title="${s.store_name}">${s.store_name}</h2>
      <div class="detail-sub-meta">
        <span>${s.brand}</span>
        <span>·</span>
        <span>${s.store_format || s.channel_format}</span>
        <span>·</span>
        <span>${s.city} ${s.district || ""}</span>
      </div>
    `;
  }

  // Render 3 Distinct Tab Panes inside Body
  const detailBody = document.getElementById("detailContentBody");
  detailBody.innerHTML = `
    <!-- 資訊 -->
    <div class="detail-tab-pane" id="paneDetailInfo" role="tabpanel" aria-labelledby="tabDetailInfo">
      <div class="sk-section">
        <div class="sk-label">地址</div>
        <div class="sk-address-row">
          <span>${s.address}</span>
          <button class="sk-icon-btn" onclick="copyStoreAddress('${s.address}')" title="複製地址" aria-label="複製地址">${SVG.copy}</button>
        </div>
      </div>
      ${(s.status_category !== '現行營運中' && s.note) ? `
        <div class="sk-notice">
          <strong>營運狀態</strong>
          <div>${s.note}</div>
        </div>` : ''}
      <div class="sk-actions">
        <a class="sk-btn sk-btn-primary" href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener">${SVG.external} 在 Google Maps 開啟</a>
        <div class="sk-btn-row">
          <button class="sk-btn sk-btn-secondary" onclick="switchDetailTab('route')">${SVG.route} 規劃路線</button>
          <button class="sk-btn sk-btn-secondary" onclick="focusCurrentDrawerStore()">${SVG.crosshair} 地圖定位</button>
        </div>
      </div>
    </div>

    <!-- 路線 -->
    <div class="detail-tab-pane" id="paneDetailRoute" role="tabpanel" aria-labelledby="tabDetailRoute">
      <div id="routePlanningBox">
        <div class="route-mode-switcher" id="routeModeSwitcher" role="group" aria-label="交通方式">
          <button class="btn-route-mode ${currentRouteMode === 'driving' ? 'active' : ''}" data-mode="driving">${SVG.car} <span>開車</span></button>
          <button class="btn-route-mode ${currentRouteMode === 'transit' ? 'active' : ''}" data-mode="transit">${SVG.transit} <span>大眾運輸</span></button>
          <button class="btn-route-mode ${currentRouteMode === 'walking' ? 'active' : ''}" data-mode="walking">${SVG.walk} <span>步行</span></button>
        </div>

        <div class="sk-section" id="routeDepartureRow" ${currentRouteMode === 'transit' ? '' : 'hidden'}>
          <label class="sk-label" for="selRouteDeparture">出發時間</label>
          <select id="selRouteDeparture" class="sel-route-origin">
            <option value="now" ${routeDeparture === 'now' ? 'selected' : ''}>現在出發</option>
            <option value="tomorrow9" ${routeDeparture === 'tomorrow9' ? 'selected' : ''}>明天早上 9:00 出發</option>
          </select>
        </div>

        <div class="sk-section">
          <label class="sk-label" for="selRouteOrigin">出發地</label>
          <div class="sk-origin-stack">
            <select id="selRouteOrigin" class="sel-route-origin">
              <option value="gps">我的位置</option>
              <option value="tpe_main">台北車站</option>
              <option value="banqiao">板橋車站</option>
              <option value="hsinchu">新竹車站</option>
              <option value="taichung">台中車站</option>
              <option value="tainan">台南車站</option>
              <option value="zuoying">左營高鐵站</option>
              <option value="custom" disabled>地圖選點</option>
            </select>
            <div class="sk-btn-row">
              <button class="sk-btn sk-btn-secondary sk-btn-sm" id="btnRelocateGps">${SVG.gps} 用我目前的位置</button>
              <button class="sk-btn sk-btn-secondary sk-btn-sm" id="btnPickOriginOnMap">${SVG.crosshair} <span id="lblPickOrigin">在地圖上點選</span></button>
            </div>

          </div>
        </div>

        <div class="sk-route-result" id="routeResult" aria-live="polite">
          <div class="sk-route-duration" id="lblRouteDuration">--</div>
          <div class="sk-route-meta" id="lblRouteMeta"></div>
        </div>

        <div class="sk-actions">
          <a class="sk-btn sk-btn-primary" id="btnGmapsTurnByTurn" href="#" target="_blank" rel="noopener">${SVG.external} 在 Google Maps 導航</a>
          <button class="sk-link-btn" id="btnClearRoute">清除地圖上的路線</button>
        </div>
      </div>
    </div>

    <!-- 周邊 -->
    <div class="detail-tab-pane" id="paneDetailCatchment" role="tabpanel" aria-labelledby="tabDetailCatchment">
      <div class="sk-section">
        <div class="sk-catch-head">
          <span>半徑 <strong id="lblRadiusVal">${currentRadiusKm.toFixed(1)} km</strong></span>
          <label class="sk-switch">
            <input type="checkbox" id="chkToggleCircle" ${isBufferCircleEnabled ? 'checked' : ''}>
            <span>在地圖顯示範圍</span>
          </label>
        </div>
        <input type="range" id="rngRadius" class="radius-range-slider" min="1.0" max="30.0" step="0.5" value="${currentRadiusKm}" aria-label="服務半徑">
        <div class="radius-presets-row">
          ${[1, 3, 5, 10, 20].map(km => `<button class="btn-radius-preset" data-km="${km}">${km} km</button>`).join("")}
        </div>
      </div>
      <div id="catchmentResultsBox"></div>
    </div>
  `;

  clearActiveRoute();
  initCatchmentControls(s);
  updateCatchmentList(s);
  initRouteControls(s);
  switchDetailTab(preferredTab || "info");
}

function updateBufferCircleOnMap(s) {
  if (!isBufferCircleEnabled) {
    if (bufferCircle) {
      map.removeLayer(bufferCircle);
      bufferCircle = null;
    }
    return;
  }

  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const radiusMeters = currentRadiusKm * 1000;

  if (!bufferCircle) {
    bufferCircle = L.circle([s.lat, s.lng], {
      radius: radiusMeters,
      color: cfg.color,
      fillColor: cfg.color,
      fillOpacity: 0.12,
      weight: 1.8,
      dashArray: "6, 6"
    }).addTo(map);
  } else {
    bufferCircle.setLatLng([s.lat, s.lng]);
    bufferCircle.setRadius(radiusMeters);
    bufferCircle.setStyle({ color: cfg.color, fillColor: cfg.color });
  }
}

function initCatchmentControls(s) {
  const slider = document.getElementById("rngRadius");
  const presets = document.querySelectorAll(".btn-radius-preset");

  function setRadius(newR) {
    currentRadiusKm = parseFloat(newR);
    if (slider) slider.value = currentRadiusKm;
    const lbl = document.getElementById("lblRadiusVal");
    if (lbl) lbl.textContent = `${currentRadiusKm.toFixed(1)} km`;

    presets.forEach(p => {
      const km = parseFloat(p.dataset.km);
      p.classList.toggle("active", Math.abs(km - currentRadiusKm) < 0.1);
    });

    if (bufferCircle) {
      bufferCircle.setRadius(currentRadiusKm * 1000);
    }

    updateCatchmentList(s);
  }

  if (slider) {
    slider.oninput = (e) => setRadius(e.target.value);
  }

  presets.forEach(btn => {
    btn.onclick = () => setRadius(btn.dataset.km);
  });

  presets.forEach(p => {
    const km = parseFloat(p.dataset.km);
    p.classList.toggle("active", Math.abs(km - currentRadiusKm) < 0.1);
  });

  const chkToggleCircle = document.getElementById("chkToggleCircle");
  if (chkToggleCircle) {
    chkToggleCircle.onchange = () => {
      isBufferCircleEnabled = chkToggleCircle.checked;
      updateBufferCircleOnMap(s);
    };
  }
}

// 周邊門市品牌篩選（換門市時重設）
let catchmentBrandFilter = { storeN: null, brand: null };
const SAME_BUILDING_KM = 0.05;

function setCatchmentBrandFilter(brand) {
  catchmentBrandFilter.brand = catchmentBrandFilter.brand === brand ? null : brand;
  if (currentDetailStore) updateCatchmentList(currentDetailStore);
}

function updateCatchmentList(s) {
  const resBox = document.getElementById("catchmentResultsBox");
  if (!resBox) return;
  if (catchmentBrandFilter.storeN !== s.n) catchmentBrandFilter = { storeN: s.n, brand: null };

  const nearby = [];
  ALL_STORES.forEach(c => {
    if (c.n === s.n) return;
    const d = haversineDistanceKm(s.lat, s.lng, c.lat, c.lng);
    if (d <= currentRadiusKm) {
      nearby.push({ store: c, dist: d });
    }
  });

  nearby.sort((a, b) => a.dist - b.dist);

  const tabBadge = document.getElementById("tabCatchmentCount");
  if (tabBadge) tabBadge.textContent = nearby.length;

  if (nearby.length === 0) {
    resBox.innerHTML = `
      <div class="sk-empty">此範圍內沒有其他居家品牌門市</div>
    `;
    return;
  }

  // 依品牌統計，數量多的排前面
  const brandCounts = {};
  nearby.forEach(item => { brandCounts[item.store.brand] = (brandCounts[item.store.brand] || 0) + 1; });
  const brands = Object.keys(brandCounts).sort((a, b) => brandCounts[b] - brandCounts[a]);
  if (catchmentBrandFilter.brand && !brandCounts[catchmentBrandFilter.brand]) catchmentBrandFilter.brand = null;
  const activeBrand = catchmentBrandFilter.brand;
  const shown = activeBrand ? nearby.filter(item => item.store.brand === activeBrand) : nearby;

  resBox.innerHTML = `
    <div class="sk-label">範圍內 ${nearby.length} 間門市・${brands.length} 個品牌</div>
    <div class="sk-brand-chips" role="group" aria-label="依品牌篩選">
      <button class="sk-brand-chip ${activeBrand ? "" : "active"}" aria-pressed="${!activeBrand}" onclick="setCatchmentBrandFilter(null)">全部 ${nearby.length}</button>
      ${brands.map(b => {
        const color = (BRANDS[b] || { color: "#0058A3" }).color;
        const on = activeBrand === b;
        return `<button class="sk-brand-chip ${on ? "active" : ""}" aria-pressed="${on}" data-brand="${b}" onclick="setCatchmentBrandFilter(this.dataset.brand)"><span class="brand-dot" style="background:${color}"></span>${b} ${brandCounts[b]}</button>`;
      }).join("")}
    </div>
    <div class="competitor-list">
      ${shown.map(item => {
        const c = item.store;
        const cCfg = BRANDS[c.brand] || { color: "#0058A3" };
        const isSameBrand = (c.brand === s.brand);
        const sameBuilding = item.dist < SAME_BUILDING_KM;
        return `
          <div class="competitor-mini-item" onclick="navigateToCompetitor(${c.n})">
            <div style="display:flex;align-items:center;gap:8px;min-width:0">
              <span class="brand-dot" style="background:${cCfg.color}"></span>
              <div style="overflow:hidden;text-overflow:ellipsis">
                <div class="c-name">${c.store_name}</div>
                <div class="c-chan">${c.brand}${isSameBrand ? " · 同品牌" : ""}</div>
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:6px;flex-shrink:0">
              ${sameBuilding ? `<span class="badge-same-building">同棟</span>` : `<span class="badge-dist">${formatDist(item.dist)}</span>`}
            </div>
          </div>
        `;
      }).join("")}
    </div>
  `;
}

/* ─── P2: ROUTE PLANNING & TRAVEL TIME ENGINE (Netlify Serverless & Google Routes API) ─── */
let activeRouteLayer = null;
let activeRouteOriginMarker = null;
let currentRouteMode = "driving";
let selectedOriginPresetId = "gps";
let customRouteOrigin = null;
let isMapPickingOrigin = false;

const ROUTE_ORIGIN_PRESETS = {
  gps: { id: "gps", name: "我的位置", lat: null, lng: null },
  tpe_main: { id: "tpe_main", name: "台北車站", lat: 25.0478, lng: 121.5170 },
  banqiao: { id: "banqiao", name: "板橋車站", lat: 25.0142, lng: 121.4637 },
  hsinchu: { id: "hsinchu", name: "新竹車站", lat: 24.8018, lng: 120.9716 },
  taichung: { id: "taichung", name: "台中車站", lat: 24.1368, lng: 120.6850 },
  tainan: { id: "tainan", name: "台南車站", lat: 22.9972, lng: 120.2127 },
  zuoying: { id: "zuoying", name: "左營高鐵站", lat: 22.6874, lng: 120.3082 }
};

function getEffectiveOrigin() {
  if (customRouteOrigin) {
    return customRouteOrigin;
  }
  if (selectedOriginPresetId === "gps" && userLocation) {
    return { id: "gps", name: "我的位置", lat: userLocation.lat, lng: userLocation.lng };
  }
  if (ROUTE_ORIGIN_PRESETS[selectedOriginPresetId] && ROUTE_ORIGIN_PRESETS[selectedOriginPresetId].lat !== null) {
    return ROUTE_ORIGIN_PRESETS[selectedOriginPresetId];
  }
  return { id: "tpe_main", name: "台北車站（尚未取得你的位置）", lat: 25.0478, lng: 121.5170 };
}

function formatDurationDisplay(minutes) {
  if (minutes < 60) {
    return { val: String(minutes), unit: "分鐘" };
  }
  const hours = Math.floor(minutes / 60);
  const rem = minutes % 60;
  if (rem === 0) {
    return { val: String(hours), unit: "小時" };
  }
  return { val: `${hours} 小時 ${rem}`, unit: "分" };
}

function formatDistanceDisplay(km) {
  if (km < 1) {
    return { val: String(Math.round(km * 1000)), unit: "公尺" };
  }
  return { val: km.toFixed(1), unit: "公里" };
}

function clearActiveRoute() {
  if (activeRouteLayer && map) {
    map.removeLayer(activeRouteLayer);
    activeRouteLayer = null;
  }
  if (activeRouteOriginMarker && map) {
    map.removeLayer(activeRouteOriginMarker);
    activeRouteOriginMarker = null;
  }
  const resBar = document.getElementById("routeResultsBar");
  if (resBar) resBar.style.display = "none";
}

function decodePolyline(encoded) {
  if (!encoded) return [];
  let points = [];
  let index = 0, len = encoded.length;
  let lat = 0, lng = 0;
  while (index < len) {
    let b, shift = 0, result = 0;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    let dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lat += dlat;
    shift = 0;
    result = 0;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    let dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lng += dlng;
    points.push([lat / 1e5, lng / 1e5]);
  }
  return points;
}

// 前端快取：同一起訖點與交通方式不重複呼叫 API（後端記憶體快取在冷啟動後會清空）
const routeResultCache = new Map();
let routeDeparture = "now"; // "now" | "tomorrow9"（僅大眾運輸）

function getDepartureIso() {
  if (currentRouteMode !== "transit" || routeDeparture !== "tomorrow9") return null;
  const d = new Date();
  d.setDate(d.getDate() + 1);
  d.setHours(9, 0, 0, 0);
  return d.toISOString();
}

async function requestRoutePlan(originLat, originLng, destLat, destLng, mode) {
  const departure = getDepartureIso();
  const cacheKey = [originLat.toFixed(4), originLng.toFixed(4), destLat.toFixed(4), destLng.toFixed(4), mode, departure ? departure.slice(0, 10) : "now"].join("|");
  if (routeResultCache.has(cacheKey)) return routeResultCache.get(cacheKey);
  try {
    let netlifyUrl = `/api/directions?originLat=${originLat}&originLng=${originLng}&destLat=${destLat}&destLng=${destLng}&mode=${mode}`;
    if (departure) netlifyUrl += `&departureTime=${encodeURIComponent(departure)}`;
    const res = await fetch(netlifyUrl, { signal: AbortSignal.timeout(10000) });
    const data = await res.json().catch(() => null);
    if (res.ok && data && data.success) {
      if (routeResultCache.size > 100) routeResultCache.delete(routeResultCache.keys().next().value);
      routeResultCache.set(cacheKey, data);
      return data;
    }
    const errMsg = (data && data.error) ? data.error : `HTTP ${res.status}: ${res.statusText || 'Google Routes API 連線失敗'}`;
    return {
      success: false,
      engine: "google",
      mode: mode,
      error: errMsg
    };
  } catch (e) {
    return {
      success: false,
      engine: "google",
      mode: mode,
      error: e.name === "TimeoutError" ? "Google Routes API 請求超時" : (e.message || "Google Routes API 連線異常")
    };
  }
}

function drawPolylineOnMap(result, orig) {
  clearActiveRoute();
  if (!result || !result.polyline) return;

  const BLUE = "#0058A3";
  const layers = [];
  // Google 地圖式畫法：白色外框 + 色線；步行段用圓點虛線
  const addLine = (pts, color, walking) => {
    if (walking) {
      layers.push(L.polyline(pts, { color, weight: 6, opacity: 0.9, dashArray: "0 10", lineCap: "round", interactive: false }));
    } else {
      layers.push(L.polyline(pts, { color: "#FFFFFF", weight: 9, opacity: 1, lineCap: "round", lineJoin: "round", interactive: false }));
      layers.push(L.polyline(pts, { color, weight: 5, opacity: 1, lineCap: "round", lineJoin: "round", interactive: false }));
    }
  };

  let all = [];
  if (currentRouteMode === "transit" && Array.isArray(result.steps) && result.steps.length) {
    // 大眾運輸逐段繪製：搭乘段用路線官方顏色，轉乘步行段用灰色圓點
    result.steps.forEach(st => {
      const pts = decodePolyline(st.polyline);
      if (!pts.length) return;
      all = all.concat(pts);
      addLine(pts, st.mode === "WALK" ? "#767676" : (st.color || BLUE), st.mode === "WALK");
    });
  }
  if (!all.length) {
    all = decodePolyline(result.polyline);
    if (!all.length) return;
    addLine(all, BLUE, currentRouteMode === "walking");
  }
  activeRouteLayer = L.layerGroup(layers).addTo(map);

  const originIcon = L.divIcon({
    className: "route-origin-pin",
    html: `<div style="background:#FFFFFF;width:14px;height:14px;border-radius:50%;border:4px solid #111;box-sizing:border-box;box-shadow:0 1px 4px rgba(0,0,0,0.35)"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
  activeRouteOriginMarker = L.marker([orig.lat, orig.lng], { icon: originIcon, zIndexOffset: 3000 })
    .bindTooltip(`出發地：${orig.name}`, { direction: "top" })
    .addTo(map);

  map.fitBounds(L.latLngBounds(all), { padding: [60, 60] });
}

function updateRouteDisplay(s, explicitResult = null) {
  const box = document.getElementById("routePlanningBox");
  if (!box) return;

  const orig = getEffectiveOrigin();
  const elDur = document.getElementById("lblRouteDuration");
  const elMeta = document.getElementById("lblRouteMeta");
  const result = document.getElementById("routeResult");

  if (!explicitResult) {
    result.classList.remove("is-error");
    elDur.textContent = "計算中…";
    elMeta.textContent = `從 ${orig.name}`;
  } else if (!explicitResult.success) {
    result.classList.add("is-error");
    elDur.textContent = "暫時無法取得路線";
    elMeta.textContent = (currentRouteMode === "transit" && routeDeparture === "now")
      ? "目前可能已無班次，可改選「明天早上 9:00 出發」，或在 Google Maps 開啟導航"
      : "請稍後再試，或直接在 Google Maps 開啟導航";
    if (explicitResult.error) console.warn("[Routes API]", explicitResult.error);
  } else {
    result.classList.remove("is-error");
    const d = formatDurationDisplay(explicitResult.duration_min);
    elDur.textContent = `${d.val} ${d.unit}`;
    elMeta.textContent = `${explicitResult.distance_text} · 從 ${orig.name}`;
  }

  const gMode = currentRouteMode === "transit" ? "transit" : (currentRouteMode === "walking" ? "walking" : "driving");
  const gmapNavBtn = document.getElementById("btnGmapsTurnByTurn");
  if (gmapNavBtn) {
    gmapNavBtn.href = `https://www.google.com/maps/dir/?api=1&origin=${orig.lat},${orig.lng}&destination=${s.lat},${s.lng}&travelmode=${gMode}`;
  }
}

let runRouteFetch = null;
let routeRequestSeq = 0;

function initRouteControls(s) {
  const box = document.getElementById("routePlanningBox");
  if (!box) return;

  const clearBtn = document.getElementById("btnClearRoute");
  clearBtn.onclick = clearActiveRoute;

  async function fetchAndApplyRoute() {
    const orig = getEffectiveOrigin();
    const seq = ++routeRequestSeq;
    updateRouteDisplay(s);
    try {
      const result = await requestRoutePlan(orig.lat, orig.lng, s.lat, s.lng, currentRouteMode);
      if (seq !== routeRequestSeq || currentDetailStore !== s) return; // 已切換門市／模式，丟棄過期結果
      updateRouteDisplay(s, result);
      if (result && result.success && result.polyline) drawPolylineOnMap(result, orig);
      else clearActiveRoute();
    } catch (err) {
      if (seq !== routeRequestSeq) return;
      updateRouteDisplay(s, { success: false, error: err.message });
      clearActiveRoute();
    }
  }
  // Initialize dropdown selection state
  const selOrigin = document.getElementById("selRouteOrigin");
  if (selOrigin) {
    if (customRouteOrigin) {
      let optCustom = selOrigin.querySelector('option[value="custom"]');
      if (optCustom) {
        optCustom.disabled = false;
        optCustom.textContent = customRouteOrigin.name;
      }
      selOrigin.value = "custom";
    } else {
      selOrigin.value = selectedOriginPresetId;
    }

    selOrigin.onchange = () => {
      const val = selOrigin.value;
      if (val === "gps") {
        customRouteOrigin = null;
        selectedOriginPresetId = "gps";
        if (!userLocation) {
          getUserLocation();
        }
      } else if (ROUTE_ORIGIN_PRESETS[val]) {
        customRouteOrigin = null;
        selectedOriginPresetId = val;
      }
      updateRouteDisplay(s);
      fetchAndApplyRoute();
    };
  }

  // GPS Locate Button
  const btnRelocate = document.getElementById("btnRelocateGps");
  if (btnRelocate) {
    btnRelocate.onclick = () => {
      customRouteOrigin = null;
      selectedOriginPresetId = "gps";
      if (selOrigin) selOrigin.value = "gps";
      if (!userLocation) {
        getUserLocation();
      }
      updateRouteDisplay(s);
      fetchAndApplyRoute();
    };
  }

  // Map Pick Button
  const btnPick = document.getElementById("btnPickOriginOnMap");
  if (btnPick) {
    btnPick.onclick = () => {
      if (isMapPickingOrigin) {
        isMapPickingOrigin = false;
        btnPick.classList.remove("picking");
        document.getElementById("lblPickOrigin").textContent = "在地圖上點選";
        map.getContainer().style.cursor = "";
        return;
      }
      isMapPickingOrigin = true;
      btnPick.classList.add("picking");
      document.getElementById("lblPickOrigin").textContent = "請點地圖（再按取消）";
      map.getContainer().style.cursor = "crosshair";

      map.once("click", (e) => {
        isMapPickingOrigin = false;
        btnPick.classList.remove("picking");
        const lblPick = document.getElementById("lblPickOrigin");
        if (lblPick) lblPick.textContent = "在地圖上點選";
        map.getContainer().style.cursor = "";

        customRouteOrigin = {
          id: "custom",
          name: "地圖選點",
          lat: e.latlng.lat,
          lng: e.latlng.lng
        };

        if (selOrigin) {
          let optCustom = selOrigin.querySelector('option[value="custom"]');
          if (optCustom) {
            optCustom.disabled = false;
            optCustom.textContent = customRouteOrigin.name;
          }
          selOrigin.value = "custom";
        }

        updateRouteDisplay(s);
        fetchAndApplyRoute();
      });
    };
  }

  // Mode Switcher Buttons
  box.querySelectorAll(".btn-route-mode").forEach(btn => {
    btn.onclick = () => {
      box.querySelectorAll(".btn-route-mode").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentRouteMode = btn.dataset.mode;
      const depRow = document.getElementById("routeDepartureRow");
      if (depRow) depRow.hidden = currentRouteMode !== "transit";
      updateRouteDisplay(s);
      fetchAndApplyRoute();
    };
  });

  const selDeparture = document.getElementById("selRouteDeparture");
  if (selDeparture) {
    selDeparture.onchange = () => {
      routeDeparture = selDeparture.value;
      fetchAndApplyRoute();
    };
  }

  // 只在「路線」分頁開啟時才呼叫 API（避免每次點門市都計費）
  runRouteFetch = () => fetchAndApplyRoute();
  updateRouteDisplay(s);
}

function closeStoreDrawer() {
  document.getElementById("sidebarDetailSection").style.display = "none";
  document.getElementById("sidebarListSection").style.display = "flex";
  currentDetailStore = null;

  if (bufferCircle) {
    map.removeLayer(bufferCircle);
    bufferCircle = null;
  }

  clearActiveRoute();

  // If in timeline mode, re-collapse sidebar to keep full map canvas unobstructed
  if (isTimelineMode && !isSidebarCollapsed) {
    collapseSidebar();
  }
}

document.getElementById("btnBackToList").onclick = closeStoreDrawer;
const btnCloseDetail = document.getElementById("btnCloseDetailDrawer");
if (btnCloseDetail) btnCloseDetail.onclick = closeStoreDrawer;

function copyStoreAddress(addr) {
  navigator.clipboard.writeText(addr).then(() => {
    const toast = document.getElementById("toastMsg");
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2000);
  });
}

/* ─── SCHEME 4: SIDEBAR COLLAPSE / EXPAND ─── */
function collapseSidebar() {
  isSidebarCollapsed = true;
  const aside = document.getElementById("mainSidebar");
  aside.classList.add("collapsed");
  document.getElementById("btnOpenSidebar").style.display = "inline-flex";
  setTimeout(() => { map.invalidateSize(); }, 320);
}

function expandSidebar() {
  isSidebarCollapsed = false;
  const aside = document.getElementById("mainSidebar");
  aside.classList.remove("collapsed");
  document.getElementById("btnOpenSidebar").style.display = "none";
  setTimeout(() => { map.invalidateSize(); }, 320);
}

document.getElementById("btnCollapseSidebar").onclick = collapseSidebar;
document.getElementById("btnOpenSidebar").onclick = expandSidebar;

/* ─── SCHEME 2: MAP VIEWPORT SYNC ─── */
function onMapViewportChange() {
  if (isViewportSync) {
    render();
  }
}

document.getElementById("chkViewportSync").addEventListener("change", e => {
  isViewportSync = e.target.checked;
  if (isViewportSync) {
    map.on("moveend", onMapViewportChange);
    map.on("zoomend", onMapViewportChange);
  } else {
    map.off("moveend", onMapViewportChange);
    map.off("zoomend", onMapViewportChange);
  }
  render();
});

/* ─── STORE MAP FOCUS & COMPETITOR NAVIGATION ─── */
function ensureStoreMarkerOnMap(s) {
  const key = "s" + s.n;
  if (!markers[key]) {
    const mk = L.marker([s.lat, s.lng], { icon: makeMarkerIcon(s) })
      .addTo(map)
      .bindPopup(makePopupHtml(s), { className: "custom-popup", minWidth: 260, maxWidth: 320, autoPan: true, autoPanPadding: [24, 24] });
    mk.on("click", () => { selectStore(key, s, false); openStoreDrawer(s, "info"); });
    markers[key] = mk;
  }
  return markers[key];
}

function focusCurrentDrawerStore() {
  if (!currentDetailStore) return;
  const s = currentDetailStore;
  const key = "s" + s.n;
  
  const mk = ensureStoreMarkerOnMap(s);
  Object.values(markers).forEach(m => m.setZIndexOffset(0));
  if (mk) mk.setZIndexOffset(3500);

  map.flyTo([s.lat, s.lng], Math.max(map.getZoom(), 16), { duration: 0.8 });
  setTimeout(() => {
    if (markers[key]) {
      markers[key].setZIndexOffset(3500);
      markers[key].openPopup();
    }
  }, 850);
}

function navigateToCompetitor(n) {
  const target = ALL_STORES.find(i => i.n === n);
  if (!target) return;

  let filterChanged = false;
  if (!isPkMode && activeBrand && activeBrand !== target.brand) {
    activeBrand = "";
    filterChanged = true;
  }
  const qInput = document.getElementById("q");
  if (qInput && qInput.value.trim()) {
    const q = qInput.value.trim().toLowerCase();
    const haystack = `${target.brand} ${target.store_name} ${target.city} ${target.district || ""} ${target.address}`.toLowerCase();
    if (!haystack.includes(q)) {
      qInput.value = "";
      filterChanged = true;
    }
  }

  if (filterChanged) {
    render();
  }

  const key = "s" + target.n;
  const mk = ensureStoreMarkerOnMap(target);
  Object.values(markers).forEach(m => m.setZIndexOffset(0));
  if (mk) mk.setZIndexOffset(3500);

  selectedKey = key;
  map.flyTo([target.lat, target.lng], Math.max(map.getZoom(), 16), { duration: 0.8 });

  openStoreDrawer(target, "info");
}

/* ─── SELECT STORE ─── */
function selectStore(key, s, flyTo) {
  selectedKey = key;
  if (isSidebarCollapsed) expandSidebar();

  document.querySelectorAll(".store-card").forEach(c =>
    c.classList.toggle("selected", c.dataset.key === key));
  document.querySelectorAll("#tblBody tr").forEach(r => {
    r.style.background = (r.dataset.key === key) ? "#EBF4FC" : "";
  });

  const cardEl = document.querySelector(`[data-key="${key}"]`);
  if (cardEl) cardEl.scrollIntoView({ block: "nearest", behavior: "smooth" });

  if (flyTo) {
    const mk = ensureStoreMarkerOnMap(s);
    Object.values(markers).forEach(m => m.setZIndexOffset(0));
    if (mk) mk.setZIndexOffset(3500);

    map.flyTo([s.lat, s.lng], Math.max(map.getZoom(), 16), { duration: 0.8 });
    setTimeout(() => {
      if (markers[key]) {
        markers[key].setZIndexOffset(3500);
        const detailSection = document.getElementById("sidebarDetailSection");
        const isDrawerOpen = detailSection && detailSection.style.display === "flex";
        if (!isDrawerOpen) {
          markers[key].openPopup();
        }
      }
    }, 850);
  }
}

/* ─── BASE MAP SWITCHING & DOCK INTERACTIONS ─── */
const styleLabels = {
  mono: "Google 淺灰",
  satellite: "Google 衛星",
  color: "Google 彩色"
};

function setBaseTile(type) {
  map.removeLayer(currentTile);
  currentTile = TILE_LAYERS[type];
  currentTile.addTo(map);

  document.getElementById("btnTileMono").classList.toggle("active", type === "mono");
  document.getElementById("btnTileSatellite").classList.toggle("active", type === "satellite");
  document.getElementById("btnTileColor").classList.toggle("active", type === "color");

  const lbl = document.getElementById("lblPillActiveStyle");
  if (lbl) lbl.textContent = styleLabels[type] || "底圖風格";
}

document.getElementById("btnTileMono").onclick = () => setBaseTile("mono");
document.getElementById("btnTileSatellite").onclick = () => setBaseTile("satellite");
document.getElementById("btnTileColor").onclick = () => setBaseTile("color");

const mapControlsDock = document.getElementById("mapControlsDock");
const btnToggleMapControls = document.getElementById("btnToggleMapControls");
const btnCloseMapStyle = document.getElementById("btnCloseMapStyle");

if (btnToggleMapControls && mapControlsDock) {
  btnToggleMapControls.onclick = (e) => {
    e.stopPropagation();
    mapControlsDock.classList.toggle("open");
  };
}

if (btnCloseMapStyle && mapControlsDock) {
  btnCloseMapStyle.onclick = (e) => {
    e.stopPropagation();
    mapControlsDock.classList.remove("open");
  };
}

document.addEventListener("click", (e) => {
  if (mapControlsDock && !mapControlsDock.contains(e.target)) {
    mapControlsDock.classList.remove("open");
  }
});

document.getElementById("chkGrayscale").onchange = (e) => {
  document.getElementById("map").classList.toggle("mono-grayscale", e.target.checked);
};

document.getElementById("chkContrast").onchange = (e) => {
  highContrastPins = e.target.checked;
  renderMarkers();
};

/* ─── KEYBOARD NAVIGATION (Section 4) ─── */
window.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    const q = document.getElementById("q");
    q.focus();
    q.select();
  } else if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "SELECT") {
    e.preventDefault();
    const q = document.getElementById("q");
    q.focus();
    q.select();
  } else if (e.key === "Escape") {
    if (currentDetailStore) {
      closeStoreDrawer();
    } else {
      const q = document.getElementById("q");
      if (q && q.value) {
        q.value = "";
        render();
      }
    }
  }
});

/* ─── RESET ALL FILTERS ─── */
document.querySelectorAll(".dataset-switch-btn").forEach(btn => {
  btn.onclick = async () => {
    activeDatasetMode = btn.dataset.dataset;
    activeBrand = "";
    if (isPkMode) togglePkMode();
    if (activeDatasetMode === "ecommerce" && !shopeeDataLoaded) {
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = "載入中…";
      try {
        await ensureShopeeData();
      } catch (error) {
        activeDatasetMode = "home";
        alert("蝦皮門市資料載入失敗，請確認 shopee_stores_data.js 與儀表板放在同一資料夾後再試一次。");
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    }
    initDropdowns();
    if (isTimelineMode) {
      recalculateTimelineBounds();
    }
    render();
  };
});

document.getElementById("btnResetAll").onclick = () => {
  document.getElementById("q").value = "";
  document.getElementById("selCity").value = "";
  document.getElementById("selDistrict").value = "";
  document.getElementById("selChannel").value = "";
  document.getElementById("selStatus").value = "現行營運中";
  activeBrand = "";
  if (isPkMode) togglePkMode();
  isSortedByDistance = false;
  if (activeRegionLayer) {
    map.removeLayer(activeRegionLayer);
    activeRegionLayer = null;
  }
  currentActiveRegionKey = "all";
  map.flyTo([23.75, 120.95], 8, { duration: 0.8 });
  document.querySelectorAll(".btn-region-jump").forEach(b => b.classList.remove("active"));
  document.querySelector('.btn-region-jump[data-region="all"]').classList.add("active");
  const btnLocate = document.getElementById("btnLocateMe");
  if (userLocation) {
    btnLocate.querySelector("span").textContent = "我的位置";
    btnLocate.title = "點擊立即回到我的目前所在位置（已定位）";
  } else {
    btnLocate.classList.remove("active");
    btnLocate.querySelector("span").textContent = "離我最近";
    btnLocate.title = "GPS 定位我的位置，依距離遠近排序";
  }
  initDropdowns();
  if (isTimelineMode) {
    recalculateTimelineBounds();
  }
  render();
};

/* ─── EXPORT CSV ─── */
document.getElementById("btnExport").onclick = () => {
  if (!filteredStores.length) { alert("目前篩選結果為空"); return; }
  const headers = ["品牌","門市名稱","門市型態","區域","縣市","行政區","原始地址","精確定位地址","緯度","經度","150公尺內有其他品牌","距離所在位置","狀態分類","重大說明"];
  const rows = filteredStores.map(s => [
    `"${s.brand}"`,`"${s.store_name}"`,`"${s.store_format || s.channel_format}"`,
    `"${s.region}"`,`"${s.city}"`,`"${s.district||""}"`,`"${s.address}"`,
    `"${s.clean_address||s.address}"`,s.lat,s.lng,
    s._isCoLocation ? '"是"' : '"否"',
    s._userDist !== undefined ? `"${formatDist(s._userDist)}"` : '""',
    `"${s.status_category}"`,`"${(s.note||"").replace(/"/g,'""')}"`
  ]);
  const csv = "\uFEFF" + [headers.join(","), ...rows.map(r=>r.join(","))].join("\r\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `taiwan_home_stores_${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
};

/* ─── EVENT HANDLERS ─── */
document.getElementById("q").addEventListener("input", render);
document.getElementById("btnClearSearch").onclick = () => {
  document.getElementById("q").value = "";
  render();
};

document.getElementById("selCity").addEventListener("change", e => {
  const city = e.target.value;
  updateDistrictDropdown(city);
  if (city) {
    const scopedStores = getScopedStorePoolForDropdowns().filter(s => s.city === city);
    const fitList = scopedStores.length > 0 ? scopedStores : ALL_STORES.filter(s => s.city === city);
    if (fitList.length > 0) {
      const b = L.latLngBounds(fitList.map(s => [s.lat, s.lng]));
      map.fitBounds(b, { padding: [50, 50], maxZoom: 13, duration: 0.8 });
    }
  } else {
    map.flyTo([23.75, 120.95], 8, { duration: 0.8 });
  }
  render();
});

document.getElementById("selDistrict").addEventListener("change", e => {
  const dist = e.target.value;
  const city = document.getElementById("selCity").value;
  if (dist && city) {
    const scopedStores = getScopedStorePoolForDropdowns().filter(s => s.city === city && s.district === dist);
    const fitList = scopedStores.length > 0 ? scopedStores : ALL_STORES.filter(s => s.city === city && s.district === dist);
    if (fitList.length > 0) {
      if (fitList.length === 1) {
        map.flyTo([fitList[0].lat, fitList[0].lng], 15, { duration: 0.8 });
      } else {
        const b = L.latLngBounds(fitList.map(s => [s.lat, s.lng]));
        map.fitBounds(b, { padding: [50, 50], maxZoom: 15, duration: 0.8 });
      }
    }
  } else if (!dist && city) {
    const scopedStores = getScopedStorePoolForDropdowns().filter(s => s.city === city);
    const fitList = scopedStores.length > 0 ? scopedStores : ALL_STORES.filter(s => s.city === city);
    if (fitList.length > 0) {
      const b = L.latLngBounds(fitList.map(s => [s.lat, s.lng]));
      map.fitBounds(b, { padding: [50, 50], maxZoom: 13, duration: 0.8 });
    }
  }
  render();
});

document.getElementById("selChannel").addEventListener("change", () => {
  initDropdowns();
  render();
});
document.getElementById("selStatus").addEventListener("change", () => {
  initDropdowns();
  render();
});

document.getElementById("vtCards").onclick = () => {
  viewMode = "cards";
  document.getElementById("vtCards").classList.add("active");
  document.getElementById("vtTable").classList.remove("active");
  renderList();
};
document.getElementById("vtTable").onclick = () => {
  viewMode = "table";
  document.getElementById("vtTable").classList.add("active");
  document.getElementById("vtCards").classList.remove("active");
  renderList();
};

/* ════════════════════════════════════════════
   SCHEME A: TIMELINE & EXPANSION PLAYER (歷年展店時序演變)
════════════════════════════════════════════ */
let isTimelineMode = false;
let timelineYear = 2026;
let timelineMinYear = 1996;
let timelineMaxYear = 2026;
let isTimelineCumulative = true;
let timelinePlaying = false;
let timelineTimer = null;
let timelineSpeed = 800;
let savedSidebarBeforeTimeline = false;

function openTimelineMode() {
  if (isTimelineMode) return;
  isTimelineMode = true;
  document.body.classList.add("timeline-mode-active");
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.classList.add("active");
  const panel = document.getElementById("timelinePlayerPanel");
  if (panel) panel.classList.add("active");

  // Auto collapse sidebar for focused immersive map exploration
  savedSidebarBeforeTimeline = !isSidebarCollapsed;
  if (!isSidebarCollapsed) {
    collapseSidebar();
  }

  // Determine min & max years based on current filtered pool
  recalculateTimelineBounds();
  const pool = getTimelineStorePool();
  renderTimelineSparkline(pool);
  updateTimeline(timelineYear, false);
}

function recalculateTimelineBounds() {
  const pool = getTimelineStorePool();
  let validYears = pool.map(s => s.opened_year || 2020).filter(y => y >= 1980 && y <= 2026);
  if (validYears.length > 0) {
    timelineMinYear = Math.max(1996, Math.min(...validYears));
  } else {
    timelineMinYear = 1996;
  }
  timelineMaxYear = 2026;

  const slider = document.getElementById("tlRangeSlider");
  if (slider) {
    slider.min = timelineMinYear;
    slider.max = timelineMaxYear;
    if (timelineYear < timelineMinYear) timelineYear = timelineMinYear;
    if (timelineYear > timelineMaxYear) timelineYear = timelineMaxYear;
    slider.value = timelineYear;
  }
}

function closeTimelineMode() {
  if (!isTimelineMode) return;
  pauseTimeline();
  isTimelineMode = false;
  document.body.classList.remove("timeline-mode-active");
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.classList.remove("active");
  const panel = document.getElementById("timelinePlayerPanel");
  if (panel) panel.classList.remove("active");

  // Restore sidebar state
  if (savedSidebarBeforeTimeline && isSidebarCollapsed) {
    expandSidebar();
  }

  // Restore normal markers and list
  render();
}

function toggleTimelineMode() {
  if (isTimelineMode) {
    closeTimelineMode();
  } else {
    openTimelineMode();
  }
}

function getTimelineStorePool() {
  const allowedBrands = DATASET_BRANDS[activeDatasetMode] || [];
  const statEl = document.getElementById("selStatus");
  const stat = statEl ? statEl.value : "";
  const chanEl = document.getElementById("selChannel");
  const chan = chanEl ? chanEl.value : "";
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const qEl = document.getElementById("q");
  const q = qEl ? qEl.value.trim().toLowerCase() : "";

  return ALL_STORES.filter(s => {
    if (!allowedBrands.includes(s.brand)) return false;
    if (isPkMode) {
      if (!pkBrands.includes(s.brand)) return false;
    } else if (activeBrand && s.brand !== activeBrand) {
      return false;
    }
    if (stat && s.status_category !== stat) return false;
    if (chan && (s.store_format || s.channel_format) !== chan) return false;
    if (city && s.city !== city) return false;
    if (dist && s.district !== dist) return false;
    if (q) {
      const match = (s.store_name && s.store_name.toLowerCase().includes(q)) ||
                    (s.brand && s.brand.toLowerCase().includes(q)) ||
                    (s.address && s.address.toLowerCase().includes(q)) ||
                    (s.district && s.district.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });
}

function renderTimelineSparkline(pool) {
  const wrap = document.getElementById("tlSparklineWrap");
  if (!wrap) return;
  wrap.innerHTML = "";

  const countsByYear = {};
  for (let y = timelineMinYear; y <= timelineMaxYear; y++) {
    countsByYear[y] = 0;
  }
  pool.forEach(s => {
    const yr = s.opened_year || 2020;
    if (yr >= timelineMinYear && yr <= timelineMaxYear) {
      countsByYear[yr] = (countsByYear[yr] || 0) + 1;
    }
  });

  const maxCnt = Math.max(1, ...Object.values(countsByYear));

  for (let y = timelineMinYear; y <= timelineMaxYear; y++) {
    const cnt = countsByYear[y] || 0;
    const bar = document.createElement("div");
    bar.className = "tl-spark-bar" + (y === timelineYear ? " active" : (y < timelineYear ? " past" : ""));
    bar.dataset.year = y;
    bar.title = `${y} 年: 新增 ${cnt} 間`;
    const heightPct = Math.max(8, Math.round((cnt / maxCnt) * 100));
    bar.style.height = `${heightPct}%`;
    bar.onclick = () => {
      pauseTimeline();
      updateTimeline(y, true);
    };
    wrap.appendChild(bar);
  }
}

function updateTimeline(year, triggerPulse = true) {
  timelineYear = parseInt(year);
  const slider = document.getElementById("tlRangeSlider");
  if (slider && parseInt(slider.value) !== timelineYear) {
    slider.value = timelineYear;
  }
  const curYearLabel = document.getElementById("tlCurrentYear");
  if (curYearLabel) curYearLabel.textContent = timelineYear;

  // Update scope label
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const scopeTextEl = document.getElementById("tlScopeText");
  if (scopeTextEl) {
    scopeTextEl.textContent = dist ? `${city} ${dist}` : (city || "全台門市");
  }

  const pool = getTimelineStorePool();
  const openedSoFar = pool.filter(s => (s.opened_year || 2020) <= timelineYear);
  const newlyOpenedInYear = pool.filter(s => (s.opened_year || 2020) === timelineYear);

  const cumCntEl = document.getElementById("tlCumulativeCount");
  if (cumCntEl) {
    cumCntEl.textContent = isTimelineCumulative ? openedSoFar.length : newlyOpenedInYear.length;
  }

  const newBadge = document.getElementById("tlNewInYearBadge");
  if (newBadge) {
    newBadge.textContent = `+${newlyOpenedInYear.length} 新增`;
    newBadge.style.display = newlyOpenedInYear.length > 0 ? "inline-block" : "none";
  }

  // Update sparkline visual states
  const bars = document.querySelectorAll(".tl-spark-bar");
  bars.forEach(b => {
    const y = parseInt(b.dataset.year);
    b.classList.toggle("active", y === timelineYear);
    b.classList.toggle("past", y < timelineYear);
  });

  // Filter stores on map
  filteredStores = isTimelineCumulative ? openedSoFar : newlyOpenedInYear;

  // Render markers with pulse for newly opened stores in this year
  renderMarkers(triggerPulse ? timelineYear : null);
  renderList();
}

function playTimeline() {
  if (timelinePlaying) return;
  if (timelineYear >= timelineMaxYear) {
    timelineYear = timelineMinYear;
  }
  timelinePlaying = true;
  const playIcon = document.getElementById("tlPlayIcon");
  const pauseIcon = document.getElementById("tlPauseIcon");
  if (playIcon) playIcon.style.display = "none";
  if (pauseIcon) pauseIcon.style.display = "block";

  timelineTimer = setInterval(() => {
    if (timelineYear >= timelineMaxYear) {
      pauseTimeline();
      return;
    }
    timelineYear++;
    updateTimeline(timelineYear, true);
  }, timelineSpeed);
}

function pauseTimeline() {
  timelinePlaying = false;
  if (timelineTimer) {
    clearInterval(timelineTimer);
    timelineTimer = null;
  }
  const playIcon = document.getElementById("tlPlayIcon");
  const pauseIcon = document.getElementById("tlPauseIcon");
  if (playIcon) playIcon.style.display = "block";
  if (pauseIcon) pauseIcon.style.display = "none";
}

function toggleTimelinePlay() {
  if (timelinePlaying) pauseTimeline();
  else playTimeline();
}

function initTimelineUI() {
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.onclick = toggleTimelineMode;

  const closeBtn = document.getElementById("btnCloseTimeline");
  if (closeBtn) closeBtn.onclick = closeTimelineMode;

  const playBtn = document.getElementById("tlBtnPlay");
  if (playBtn) playBtn.onclick = toggleTimelinePlay;

  const slider = document.getElementById("tlRangeSlider");
  if (slider) {
    let sliderRaf = null;
    slider.addEventListener("input", (e) => {
      pauseTimeline();
      const targetVal = e.target.value;
      if (sliderRaf) cancelAnimationFrame(sliderRaf);
      sliderRaf = requestAnimationFrame(() => {
        updateTimeline(targetVal, false);
      });
    });
  }

  const cumToggle = document.getElementById("tlCumulativeToggle");
  if (cumToggle) {
    cumToggle.addEventListener("change", (e) => {
      isTimelineCumulative = e.target.checked;
      updateTimeline(timelineYear, false);
    });
  }

  document.querySelectorAll(".tl-speed-btn").forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll(".tl-speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      timelineSpeed = parseInt(btn.dataset.speed);
      if (timelinePlaying) {
        pauseTimeline();
        playTimeline();
      }
    };
  });
}

/* ─── INITIAL BOOT ─── */
initDropdowns();
initBrandPills();
initRegionJumpBar();
initTimelineUI();
render();
</script>
</body>
</html>"""

HTML = (HTML_TEMPLATE
        .replace("STORES_DATA_PLACEHOLDER", STORES_JS)
        .replace("ACTIVE_STORE_COUNT_PLACEHOLDER", str(ACTIVE_STORE_COUNT))
        .replace("DATA_UPDATED_DATE_PLACEHOLDER", DATA_UPDATED_DATE))

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
