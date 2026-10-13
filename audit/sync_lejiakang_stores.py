# -*- coding: utf-8 -*-
"""同步「樂家康（原家樂福超市）」門市；開幕日期只列有開幕新聞可查證者，其餘留空（不以商工登記日代替）。

資料來源：
- 門市清單：萬家福官方門市 API（store_type_id=2「超市」），與 sync_mass_retail_stores.py 的萬家福量販同一支 API。
  2026-07-01 起家樂福量販更名萬家福、家樂福超市更名樂家康（中央社 202607010050）。
- 分公司登記：商工登記「統編查分公司資料」API（只作比對參考，不當開幕日期），營運公司為
  統康生活事業（原惠康百貨／頂好，統編 22662257）與康達盛通生活事業（原家福，統編 22662550）。

比對規則（不做模糊推估）：
1. 門市資料的 tax_id 若是分公司統編，直接對應該分公司。
2. 否則以 full_name 的分公司名稱，在兩家公司「核准設立」的分公司中找同名者。
3. 再找不到則以正規化地址比對同縣市的核准設立分公司（須唯一）。
4. 仍無對應者不記分公司。
開幕日期：分公司核准設立日不等於開幕日（可能早於開幕數天到數月，或是公司重組時的重新登記），
所以只採用 NEWS_OPENINGS 的開幕新聞日期，其餘門市 opened_date 留空；登記日僅保留在 lejiakang_gcis_match.json 供參考。
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
NEWS_JSON = BASE_DIR / "supermarket_news_openings.json"
GCIS_API = "https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB"
COMPANIES = {"22662257": "統康生活事業", "22662550": "康達盛通生活事業"}
BRAND = "樂家康"

# 有開幕新聞可查證的門市才列開幕日期；其餘留空。
# 抽查的 10 間登記日都早於開幕 4～119 天，登記日不能當作開幕日。
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
    # 逐店查新聞、雜誌、社群貼文所得的開幕日期（supermarket_news_openings.json）
    extra_news = {x["store_name"]: (x["opened_date"], x["source_url"], x.get("evidence", ""))
                  for x in json.loads(NEWS_JSON.read_text(encoding="utf-8")) if x["brand"] == BRAND} if NEWS_JSON.exists() else {}

    stores, audit = [], []
    for row in rows:
        address = full_address(row)
        city = norm_city(row["city_name"])
        b, how = match(row, address, branches, by_ban)
        name = f"{BRAND} {row['name']}"
        news = NEWS_OPENINGS.get(row["name"]) or extra_news.get(name)
        g = gmaps.get(name)
        if news:
            opened, basis, src = news[0], "新聞／官方", news[1]
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
            "verification_status": "官方門市；開幕日期依新聞／社群" if news else "官方門市；查無可查證的開幕日期，未列出",
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
            "registry_estab_date_reference_only": b["opened_date"] if b else "",
            "registry_address_differs": bool(b) and norm_addr(b["address"]) != norm_addr(address),
        })

    main_rows = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    old_n = {r.get("official_store_id"): r["n"] for r in main_rows if r.get("brand") == BRAND}
    kept = [r for r in main_rows if r.get("brand") != BRAND]
    next_n = max(int(r.get("n") or 0) for r in kept) + 1
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
    print(f"列出開幕日期（新聞）{sum(1 for a in audit if a['news'])} 間；未列出 {sum(1 for a in audit if not a['opened_date'])} 間")
    print(f"登記地址與現址不同：{sum(a['registry_address_differs'] for a in audit)} 間")


if __name__ == "__main__":
    main()
