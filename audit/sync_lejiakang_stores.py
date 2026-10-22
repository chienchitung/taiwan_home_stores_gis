# -*- coding: utf-8 -*-
"""同步「樂家康（原家樂福超市）」門市；開幕日期有開幕新聞者用新聞日期，其餘用經濟部商工登記分公司核准設立日（儀表板標示「依商工登記」）。

資料來源：
- 門市清單：萬家福官方門市 API（store_type_id=2「超市」），與 sync_mass_retail_stores.py 的萬家福量販同一支 API。
  2026-07-01 起家樂福量販更名萬家福、家樂福超市更名樂家康（中央社 202607010050）。
- 分公司登記：商工登記「統編查分公司資料」API（查無開幕新聞者以核准設立日代表開幕日，並標示依據），營運公司為
  統康生活事業（原惠康百貨／頂好，統編 22662257）與康達盛通生活事業（原家福，統編 22662550）。

比對規則（不做模糊推估）：
1. 門市資料的 tax_id 若是分公司統編，直接對應該分公司。
2. 否則以 full_name 的分公司名稱，在兩家公司「核准設立」的分公司中找同名者。
3. 再找不到則以正規化地址比對同縣市的核准設立分公司（須唯一）。
4. 仍無對應者 opened_date 留空。
開幕日期：分公司核准設立日通常早於開幕數天到數月，因此 opened_date_basis 記為「商工登記」，儀表板標示「依商工登記」，
與全聯相同；有開幕新聞者（NEWS_OPENINGS）以新聞日期為準。
不跨公司合併同址的舊登記：同址舊分公司多為已廢止的不同門市（例如統康三重二分公司 2000 年設立、已廢止，
現址康達盛通三重新北大道 2019 年另行設立），無法證明是同一間店連續營業。

可重複執行：會先移除主資料中的樂家康門市，再以本次結果寫回；既有門市沿用原本的 n。
"""
import csv
import json
import sys
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
from pxmart_gcis_match import norm_addr, norm_city  # noqa: E402
from sync_mass_retail_stores import WANJIAFU_API, WANJIAFU_TOKEN, region_for, maps_url  # noqa: E402

DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
RAW_JSON = BASE_DIR / "lejiakang_stores_raw.json"
MATCH_JSON = BASE_DIR / "lejiakang_gcis_match.json"
GCIS_API = "https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB"
COMPANIES = {"22662257": "統康生活事業", "22662550": "康達盛通生活事業"}
BRAND = "樂家康"

# 有開幕新聞的門市以新聞日期為準；其餘用商工登記日並標示依據。
# 抽查的 10 間登記日都早於開幕 4～119 天。
NEWS_OPENINGS = {
    "朴子文明南店": ("2026-04-10", "https://udn.com/news/story/7270/9434742", "經濟日報：家樂福超市朴子文明南店盛大開幕（2026-04-10）"),
    "台南文賢二店": ("2026-03-13", "https://www.ettoday.net/news/20260313/3131620.htm", "ETtoday 2026-03-13：家樂福超市台南文賢店（北區文賢路，400 坪複合店）開幕；登記為文賢二分公司 2026-03-09"),
    "士林華聲店": ("2025-09-19", "https://udn.com/news/story/7270/9015892", "經濟日報：家樂福超市士林華聲店 9/19 開幕（2025）"),
    "潮州光春店": ("2025-06-20", "https://udn.com/news/story/7270/8819906", "聯合報：家樂福超市插旗屏東潮州，2025-06-20 開幕"),
    "新莊民安2店": ("2025-05-23", "https://www.cdns.com.tw/articles/1223078", "中華日報：家樂福超市新莊民安二店歡慶開幕（2025-05-23）"),
    "左營文上店": ("2025-03-28", "https://howlife.cna.com.tw/local/20250328s001.aspx", "中央社好生活 2025-03-28：家樂福左營文上店開幕"),
    "新市民生店": ("2025-02", "https://nvns.net/news_view.php?new_sn=76092&new_csn=1467", "報導：家樂福新市民生店 21 日開幕；社群貼文 2025-02-20 稱今天開幕，日期略有出入，僅記至月份"),
    "新莊新泰店": ("2024-12-20", "https://udn.com/news/story/7270/8438040", "經濟日報：家樂福新莊新泰店 2024-12-20 開幕"),
    "汐止龍安店": ("2024-08-01", "https://www.winnews.com.tw/193378/", "威傳媒：家樂福超市汐止龍安店 2024-08-01 開幕"),
    "花蓮林森店": ("2024-04-30", "https://www.jumpman.tw/carrefour-hualien-market.html", "2024-04-30 開幕（原國聲戲院址，全台第 247 家超市）"),
    "三峽大學店": ("2024-08-30", "https://times.586.com.tw/2024/08/710461/", "報導：家樂福超市三峽大學店（大學路 119 號，北大特區）2024-08-30 開幕；另一篇 2024-09-03 報導稱「日昨」開幕。商工登記的「J三峽大學分公司」2017 年設立，與此店開幕時間不符，不採用"),
    "台北西藏店": ("1995-01", "https://www.winnews.com.tw/167820/", "威傳媒：台北西藏店自 1995 年 1 月開幕至今（原頂好），2023-12 改裝；查無對應商工登記分公司"),
    # 家樂福臉書貼文（本環境無法開啟，2026-10-14 由使用者逐篇開啟確認日期）
    "台中漢口店": ("2015-12-11", "https://www.facebook.com/carrefour.tw/posts/965862830128081/", "家樂福臉書 2015-12-11：又一間便利購在台中開幕，漢口店（漢口路四段295號）；貼文未寫確切開幕日，依使用者指定採貼文日期"),
    "台北濟南店": ("2017-11-20", "https://www.facebook.com/carrefour.tw/posts/1562482737132751/", "家樂福臉書 2017-11-18：11/20 台北濟南店慶開幕（濟南路2段46號B1）"),
    "土城日月光店": ("2018-07-26", "https://www.facebook.com/carrefour.tw/posts/1840152572699098/", "家樂福臉書 2018-07-25：土城日月光店明天（7/26）開幕（學府路二段210號B2）"),
    "北投明德店": ("2018-10-31", "https://www.facebook.com/carrefour.tw/posts/1997394440308243/", "家樂福臉書 2018-10-30：北投明德店明天（10/31）開幕（明德路161號B1）"),
    "三重新北大道店": ("2019-06-28", "https://www.facebook.com/carrefour.tw/posts/2375222992525384/", "家樂福臉書 2019-06-27：三重新北大道店 6/28 開幕（新北大道一段115號B1）"),
    "基隆孝二店": ("2021-07-26", "https://www.facebook.com/carrefour.tw/posts/4310915698956094/", "家樂福臉書貼文（超市開幕、實聯制時期）；開幕日 2021-07-26 由使用者 2026-10-14 查證指定。查無對應商工登記分公司"),
    # 2026-10-14 逐筆開啟來源網頁確認店名與開幕日
    "台中昌平店": ("2015-02-11", "https://www.chinatimes.com/realtimenews/20150211004287-260405", "工商時報 2015-02-11：家樂福便利購台中市昌平店今（11）日開幕，全台第10家便利購"),
    "新竹南大店": ("2017-10-27", "https://www.chinatimes.com/realtimenews/20171027002378-263301", "中時 2017-10-27：便利購大新竹首家店「新竹市南大店」27日開幕"),
    "小港漢民店": ("2019-08", "https://www.ctee.com.tw/news/20190822700655-439803", "工商時報 2019-08-22：接手台糖超市的小港漢民店、台中水湳店、鳳山甲一店於 8/21～8/23 一天一家開幕（未寫明各店對應日期，只記至月份）"),
    "北屯總太店": ("2024-03-23", "https://twpowernews.com/news_pagein.php?iType=1010&n_id=261401", "勁報 2024-03-23：家樂福超市北屯總太店於今（23）日開幕，位於環太東路477號"),
    "太平環中店": ("2015-09-29", "https://www.ctee.com.tw/news/20150930700085-439901", "工商時報 2015-09-30：太平環中店昨（29）日開幕，全台第17家便利購"),
    "大甲蔣公店": ("2017-10-20", "https://n.yam.com/Article/20171021885018", "大成報（蕃新聞 2017-10-21）：20日便利購正式進駐大甲蔣公路商圈，大甲店開幕"),
    "台北錦州店": ("2018-05-25", "https://www.chinatimes.com/realtimenews/20180525004133-260405", "工商時報 2018-05-25：家樂福全台第53家便利購今（25）在中山區錦州街開幕"),
    "林口仁愛店": ("2019-03-08", "https://www.ctee.com.tw/news/20190308700147-430404", "工商時報 2019-03-08：頂好超市今（3月8日）開出林口仁愛店（原頂好，現樂家康）"),
    "大安臨江店": ("2019-09-11", "https://tw.discount.wave-base.com/sale/4LpVM/", "家樂福貼文轉載（SaleEvents，2019-09-10）：便利購大安臨江店明天（9/11）開幕，含臨江街87號"),
    "龜山文青店": ("2021-12-14", "https://www.foodnext.net/news/industry/paper/5470657580", "食力 foodNEXT：2021年12月14日開幕龜山文青店"),
    "太平育賢店": ("2024-06-28", "https://greatnews.com.tw/news_pagein.php?iType=1004&n_id=293461", "大成報 2024-06-30：超市太平育賢店28日開幕，位在育賢路190號"),
    "豐南店": ("2013-07-05", "https://vpnline.pixnet.net/blog/posts/9134949529", "蘋果日報 2013-07-04（痞客邦轉載）：家樂福便利購台中豐南店明日（7/5）正式開幕，位於豐原區"),
    "新莊丹鳳店": ("2015-07", "https://www.chinatimes.com/newspapers/20150722000792-260113", "中國時報 2015-07-22：家樂福便利購進軍新莊開丹鳳店（報導未寫確切開幕日，只記至月份）"),
    "楠梓益群店": ("2016-06-24", "https://tw.news.yahoo.com/家樂福便利購展店搶超市市場-圖-121101290--finance.html", "中央社 2016-06-24 圖片新聞：家樂福便利購超市楠梓益群店24日開幕"),
    "中壢中北店": ("2017-01-13", "https://enews.tw/article/822715", "台灣好新聞（ENews 2017-01-13）：便利購中壢中北店13日上午開幕"),
    "桃園龍安店": ("2017-08-31", "https://news.ltn.com.tw/news/life/breakingnews/2179483", "自由時報 2017-08-31：家樂福便利購超市龍安店今天開幕"),
    "板橋文化店": ("2017-12-19", "https://tw.sale-events.com/sale/家樂福便利購-板橋文化店開幕優惠-_RJMRw", "家樂福貼文轉載（SaleEvents，2017-12-17）：12/19 開幕的家樂福板橋文化店，地點文化路二段313號"),
    "土城中央店": ("2019-09-18", "https://www.ptt.cc/bbs/TuCheng/M.1568773535.A.A85.html", "PTT TuCheng 2019-09-18：家樂福簡訊「便利購土城中央店新開幕！9/18當天…」，地址中央路二段191號B1"),
    "嘉義民族店": ("2023-04-26", "https://www.chiayi.gov.tw/News_Content.aspx?n=455&s=778947", "嘉義市政府新聞 2023-04-26：家樂福於今(26)日宣布第三家分店「民族店」開幕（金財神大樓）"),
    "太保祥和店": ("2024-09-26", "https://www.cna.com.tw/news/ahel/202409260214.aspx", "中央社 2024-09-26：嘉義縣長今天參加家樂福超市太保祥和店開幕"),
    "鳳山甲1店": ("2019-08", "https://www.ctee.com.tw/news/20190822700655-439803", "工商時報 2019-08-22：小港漢民店、台中水湳店、鳳山甲一店於 8/21～8/23 一天一家開幕（只記至月份）"),
}
SOURCE_URL = "https://www.uni-prosperity.com.tw/stores/?hl=zh-TW"


# 座標以 Google 地圖地點為準：verify_lejiakang_google_maps.py 逐筆取得 Google 地圖上同名門市的座標，
# 店名確認相符者採用 Google 座標；查不到的才用官方門市地圖座標。
# （官方座標有 21 間與 Google 相差 100 m 以上，後龍中山店官方座標更誤植為台北長沙店。）
GMAPS_CHECK = BASE_DIR / "lejiakang_gmaps_check.json"


def google_coords():
    if not GMAPS_CHECK.exists():
        return {}
    return {x["store"]: x["google"] for x in json.loads(GMAPS_CHECK.read_text(encoding="utf-8"))
            if x.get("google") and x.get("name_match")}


def roc_to_iso(d):
    d = (d or "").strip()
    if len(d) < 7 or not d.isdigit():
        return ""
    return f"{int(d[:-4]) + 1911}-{d[-4:-2]}-{d[-2:]}"


def fetch_stores():
    resp = requests.get(WANJIAFU_API, params={"page_size": "all", "store_type_id": 2},
                        headers={"Authorization": WANJIAFU_TOKEN, "Origin": "https://www.uni-prosperity.com.tw"},
                        timeout=30)
    resp.raise_for_status()
    rows = resp.json()["data"]["rows"]
    # 存檔前移除聯絡人個資（店長姓名、Email 等）與用不到的大型欄位，只留比對、定位需要的欄位
    drop = {"contact_name", "contact_email", "images", "banners", "news"}
    RAW_JSON.write_text(json.dumps([{k: v for k, v in r.items() if k not in drop} for r in rows],
                                   ensure_ascii=False, indent=1), encoding="utf-8")
    return rows


def fetch_branches():
    branches = []
    for ban, company in COMPANIES.items():
        resp = requests.get(GCIS_API, params={"$format": "json", "$filter": f"Business_Accounting_NO eq {ban}",
                                              "$skip": 0, "$top": 1000}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        (BASE_DIR / "gcis" / f"{ban}_{company}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        for x in data:
            branches.append({
                "company": company,
                "ban": x["Branch_Office_Business_Accounting_NO"],
                "name": x["Branch_Office_Name"],
                "address": norm_city(x["Branch_Office_Location"]),
                "status": x["Branch_Office_Status_Desc"],
                "opened_date": roc_to_iso(x["BR_ESTAB_DATE"]),
            })
    return branches


def full_address(row):
    city, area = row["city_name"], row.get("area_name") or ""
    street = norm_city(row["street"].strip())
    return street if street.startswith(norm_city(city)) else norm_city(city) + area + street


def branch_label(full_name):
    name = full_name.split("股份有限公司")[-1]
    for suffix in ("分公司", "門市"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def norm_branch(name):
    """分公司名稱比對用：去掉「分公司／門市」、開頭的英文代碼（如 J三峽大學）、阿拉伯數字轉國字（民安2 → 民安二）"""
    import re
    name = re.sub(r"(分公司|門市)$", "", name)
    name = re.sub(r"^[A-Za-z]+", "", name)
    return name.translate(str.maketrans("123456789", "一二三四五六七八九"))


def match(row, address, branches, by_ban):
    b = by_ban.get(str(row.get("tax_id") or ""))
    if b:
        return b, "分公司統編"
    active = [x for x in branches if x["status"] == "核准設立"]
    label = norm_branch(branch_label(row.get("full_name") or ""))
    cands = [x for x in active if norm_branch(x["name"]) == label]
    if len(cands) == 1:
        return cands[0], "分公司名稱"
    key = norm_addr(address)
    cands = [x for x in active if norm_addr(x["address"]) == key]
    if len(cands) == 1:
        return cands[0], "地址"
    return None, ""


def main():
    rows = fetch_stores()
    branches = fetch_branches()
    by_ban = {b["ban"]: b for b in branches}
    gmaps = google_coords()

    stores, audit = [], []
    for row in rows:
        address = full_address(row)
        city = norm_city(row["city_name"])
        b, how = match(row, address, branches, by_ban)
        name = f"{BRAND} {row['name']}"
        news = NEWS_OPENINGS.get(row["name"])
        g = gmaps.get(name)
        if news:
            opened, basis, src = news[0], "新聞／官方", news[1]
        elif b:
            opened, basis, src = b["opened_date"], "商工登記", GCIS_API
        else:
            opened, basis, src = "", "", ""
        store = {
            "brand": BRAND,
            "store_name": name,
            "store_type": "社區生鮮超市",
            "region": region_for(city),
            "city": city,
            "address": address,
            "opened_date": opened,
            "status": "營業中",
            "note": "原家樂福超市，2026-07-01 起更名樂家康",
            "district": row.get("area_name") or "",
            "channel_format": "社區生鮮超市 / 街邊獨立",
            "status_category": "現行營運中",
            "lat": round(g["lat"], 7) if g else float(row["latitude"]),
            "lng": round(g["lng"], 7) if g else float(row["longitude"]),
            "geocode_score": 100,
            "clean_address": address,
            "clean_name": name,
            "clean_query": f"{name} {address}",
            "is_co_location": False,
            "source_url": SOURCE_URL,
            "coordinate_source": f"Google 地圖「{g['name']}」地點座標（2026-10-13 逐筆比對）" if g else "萬家福／樂家康官方門市地圖座標",
            "google_maps_url": maps_url(BRAND, row["name"], address),
            "verification_status": ("官方門市；開幕日期依開幕新聞" if news else
                                    "官方門市；開幕日期採經濟部商工登記分公司核准設立日" if b else
                                    "官方門市；查無開幕新聞與商工登記，開幕日期未知"),
            "official_store_id": str(row["id"]),
            "store_format": "社區超市",
            "official_branch_ban": b["ban"] if b else "",
            "branch_registry_name": f"{b['company']}{b['name']}" if b else "",
            "opened_date_basis": basis,
            "opened_date_source": src,
        }
        stores.append(store)
        audit.append({
            "store": name, "api_full_name": row.get("full_name"), "api_tax_id": row.get("tax_id"),
            "match_by": how, "branch": b, "current_address": address,
            "opened_date": opened, "opened_date_basis": basis, "news": news[2] if news else "",
            "registry_estab_date": b["opened_date"] if b else "",
            "registry_address_differs": bool(b) and norm_addr(b["address"]) != norm_addr(address),
        })

    main_rows = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    old_n = {r.get("official_store_id"): r["n"] for r in main_rows if r.get("brand") == BRAND}
    kept = [r for r in main_rows if r.get("brand") != BRAND]
    # 新門市編號接在所有既有資料（含本次替換的品牌）之後，避免和沿用舊編號的門市重複
    next_n = max(int(r.get("n") or 0) for r in main_rows) + 1
    for s in stores:
        n = old_n.get(s["official_store_id"])
        if n is None:
            n, next_n = next_n, next_n + 1
        s["n"] = n
    all_rows = kept + stores
    MAIN_JSON.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for r in all_rows for k in r))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)
    MATCH_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=1), encoding="utf-8")

    matched = sum(1 for a in audit if a["branch"])
    print(f"樂家康 {len(stores)} 間；對應商工登記 {matched} 間"
          f"（統編 {sum(a['match_by'] == '分公司統編' for a in audit)}、名稱 {sum(a['match_by'] == '分公司名稱' for a in audit)}、"
          f"地址 {sum(a['match_by'] == '地址' for a in audit)}）；未對應 {len(stores) - matched} 間")
    print(f"新聞日期 {sum(1 for a in audit if a['news'])} 間；商工登記日 {sum(1 for a in audit if a['opened_date_basis'] == '商工登記')} 間；"
          f"未知 {sum(1 for a in audit if not a['opened_date'])} 間")
    print(f"登記地址與現址不同：{sum(a['registry_address_differs'] for a in audit)} 間")


if __name__ == "__main__":
    main()
