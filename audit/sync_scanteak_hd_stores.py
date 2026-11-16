# -*- coding: utf-8 -*-
"""同步「詩肯」「東稻家居」門市（2026-11-16 查核；資料凍結於 2026-10-31，10/31 後查無異動）。

- 詩肯（詩肯股份有限公司，統編 89403884；旗下詩肯柚木、詩肯居家、詩肯睡眠等品牌，2026-11-16 起品牌統一稱「詩肯」）：詩肯柚木官網門市頁 https://www.scanteak.com.tw/our-stores/ 的 AJAX 清單共 72 間，
  全數列為營業中。原始整理見 audit/scanteak_stores_20261116.json。另依使用者指示「依地點計算」，補入詩肯居家／詩肯睡眠
  官網清單中不在柚木清單的 4 個地點（微風南京、台中文心、彰化金馬、台北民生一），見 audit/scanteak_extra_stores_20261116.json；
  共 76 個地點。公司公布 2026-10 月底全台門市 84 店（鉅亨網 2026-11-12），差額疑為同址居家專櫃另計，未經來源證實。
- 東稻家居（H&D，東稻股份有限公司，統編 27558042）：官網門市資料 https://www.hdlife.com.tw/zSharedFiles/_db_json/store/store.json
  共 8 間；依使用者指示只收營業中的一般門市，睡眠館（台北內湖睡眠館）、快閃店與遷址舊店不計，收 7 間。
  原始整理見 audit/hd_stores_20261116.json（含未收錄的遷址舊店，供日後參考）。
- 座標：逐店在 Google 地圖搜尋品牌地點，查無品牌地點者用門牌地址座標（coordinate_source 註明），並以國土測繪中心確認行政區。
- 開幕日期：只採官方公告、新聞載明或使用者人工查證的正式開幕日（遷址店採現址開幕日）；查無者留空。詩肯 2010 年的商工登記分公司核准日為一次性
  集中登記，不作開幕日；以商場開幕日推論的日期（新店裕隆誠品）也不採用。開幕日期同步寫入 store_opened_dates_verified.json。
- 店型：開在特力屋／HOLA 賣場內者列「店中店／專櫃」，開在萬家福內者列「量販店中店」；所在建物未查證者列「店型待確認」。
可重複執行：先移除主資料中這兩個品牌，再以本清單寫回；既有門市沿用原本的 n。需在各 sync 腳本之後、apply_verified_opened_dates.py 之前執行。
"""
import csv
import json
import re
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
VERIFIED_JSON = BASE_DIR / "store_opened_dates_verified.json"
# 詩肯居家／詩肯睡眠官網門市清單中、不在詩肯柚木清單的地點（依地點計算，同址的居家／睡眠專櫃不另計）
EXTRA_SOURCES = {"詩肯": BASE_DIR / "scanteak_extra_stores_20261116.json"}
LEGACY_BRANDS = {"詩肯柚木": "詩肯"}  # 舊品牌名：重跑時移除並沿用原本的 n
SOURCES = {
    "詩肯": (BASE_DIR / "scanteak_stores_20261116.json", "https://www.scanteak.com.tw/our-stores/"),
    "東稻家居": (BASE_DIR / "hd_stores_20261116.json", "https://www.hdlife.com.tw/Store/"),
}
CHANNEL = {"大型獨棟／街邊門市": "大型獨棟 / 獨立街邊店", "百貨／購物中心門市": "百貨商場 / 購物中心",
           "量販店中店": "量販店中店 / 超市複合", "店中店／專櫃": "店中店 / 專櫃", "店型待確認": "店型待確認"}
USER_CHECKED = "使用者查證（2026-11-16）"
# 開幕日期：只收官方或新聞載明者，以及使用者人工查證者
SCANTEAK_OPENINGS = {
    "台北大舊宗": ("2019-11-13", "https://www.chinatimes.com/realtimenews/20191113002653-260410",
                   "時報資訊 2019-11-13「詩肯台北旗艦店今日正式開幕」；位置「內湖舊宗路與南京東路口」（自由財經），對應本店"),
    "民生": ("1994", "https://www.moneyweekly.com.tw/ArticleData/Info/Article/160672/", "理財周刊：自 1994 年開業（僅年份）"),
    # 官網標 NEW 的門市，開幕日由使用者人工查證（2026-11-16）
    "台中廣三SOGO": ("2026-10-18", USER_CHECKED, "使用者查證"),
    "台中麗寶": ("2026-05-29", USER_CHECKED, "使用者查證"),
    "新店中興(萬家福)": ("2026-05-12", USER_CHECKED, "使用者查證"),
    "北屯松竹": ("2026-01-31", USER_CHECKED, "使用者查證"),
    "新竹大遠百": ("2025-04-25", USER_CHECKED, "使用者查證"),
}

# 官網標「NEW」但開幕日查無者，已查得確定早於凍結日的佐證（2026-11-16）
SCANTEAK_NOTES = {
    "嘉義新北港": "官網標 NEW，但 2021-09-28 嘉義市長已到店參觀（官網 store_event/210928、中時 2021-10-02「全台最大旗艦店設北港路」），開幕早於 2026-10-31；確切開幕日查無",
    "泰山店(原 大新莊店)": "官網標 NEW；同址 2014 年官方門市清單即為大新莊店，屬更名，開幕早於 2026-10-31；確切開幕日查無",
}


def region_for(city):
    if city in {"台北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣"}:
        return "北部"
    if city in {"台中市", "彰化縣", "南投縣", "雲林縣"}:
        return "中部"
    if city in {"嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"}:
        return "南部"
    return "東部/離島"

# 2026-11-16 逐間以 Google 地圖與同址門市核對店型（官網原名 → (店型, 依據)）
FORMAT_OVERRIDES = {
    "南崁": ("店中店／專櫃", "與特力屋南崁店（B1）、HOLA 桃園南崁店（1F）同為蘆竹區中正路1號"),
    "內湖新湖": ("店中店／專櫃", "與特力屋內湖店（B1）、HOLA 台北內湖店（1F）、hoi! 內湖店（2F）同為新湖三路23號，官網地址為 2 樓 E 櫃"),
    "汐止新五": ("百貨／購物中心門市", "Google 地圖 iFG 遠雄廣場地址為新台五路一段93-99號，門市位於 97 號 3 樓"),
}


def store_format(brand, item):
    if item["name"] in FORMAT_OVERRIDES:
        return FORMAT_OVERRIDES[item["name"]][0]
    fmt, basis = item["store_format"], item.get("format_basis") or ""
    if "未判定" in fmt or "查無" in fmt:
        return "店型待確認"
    if fmt == "量販店中店" and ("特力" in item["name"] or "HOLA" in item["name"] or "特力屋" in basis):
        return "店中店／專櫃"
    return fmt


def clean_address(address):
    a = re.sub(r"^\d{3,6}", "", address.replace("臺", "台"))
    a = re.sub(r"[（(].*?[）)]", "", a)
    m = re.match(r"(.+?號)", a)
    return m.group(1) if m else a


def build(brand, item, source_url):
    city = item["city"].replace("臺", "台")
    name = item["name"]
    if brand == "東稻家居":
        name = "新莊三和路門市" if "三和路" in name else re.sub(r"\s*[（(].*?[）)]\s*$", "", name)
    elif not re.search(r"店\)?$|店（", name):  # 詩肯官網店名不含「店」，補上以便辨識，如「北屯松竹」→「北屯松竹店」
        m = re.match(r"(.+?)([（(].*[）)])$", name)
        name = f"{m.group(1)}店{m.group(2)}" if m else name + "店"
    full = f"{brand} {name}"
    address = item["address"].replace("臺", "台")
    fmt = store_format(brand, item)
    opened, osrc, basis = "", "", ""
    if brand == "詩肯" and item["name"] in SCANTEAK_OPENINGS:
        opened, osrc, _ = SCANTEAK_OPENINGS[item["name"]]
        basis = "使用者查證" if osrc == USER_CHECKED else "新聞／官方"
    elif brand == "東稻家居" and re.match(r"\d{4}", item.get("opened_date") or ""):
        opened = item["opened_date"]
        osrc = (re.findall(r"https?://[^\s）)，；]+", item.get("opened_source") or "") or [source_url])[0]
        basis = "新聞／官方"
    status = item["status"]
    closed = item.get("closed_date") or ""
    m = re.match(r"(\d{4}-\d{2}(?:-\d{2})?)", closed)
    note_parts = [p for p in (item.get("note") or "",) if p and p != "None"]
    if item["name"] == "新店裕隆誠品":  # 店名比對用官網原名
        note_parts.append("商場誠品生活新店 2023-09-28 開幕時已列進駐品牌，但品牌本身開幕日查無，不以商場開幕日代替")
    if item["name"] in SCANTEAK_NOTES:
        note_parts.append(SCANTEAK_NOTES[item["name"]])
    if item["name"] in FORMAT_OVERRIDES:
        note_parts.append("店型依據：" + FORMAT_OVERRIDES[item["name"]][1])
    if fmt == "店型待確認":
        note_parts.append("所在建物未查證，店型待確認")
    row = {
        "brand": brand, "store_name": full, "store_type": fmt, "region": region_for(city), "city": city,
        "address": address, "opened_date": opened, "status": "營業中" if status == "營業中" else "已遷址",
        "note": "；".join(note_parts), "district": item["district"],
        "channel_format": CHANNEL[fmt],
        "status_category": "現行營運中" if status == "營業中" else "歷史變動（已熄燈/遷址）",
        "lat": item["lat"], "lng": item["lng"], "geocode_score": 100,
        "clean_address": clean_address(address), "clean_name": full,
        "clean_query": f"{full} {clean_address(address)}", "is_co_location": fmt != "大型獨棟／街邊門市",
        "source_url": source_url, "coordinate_source": item.get("coord_basis") or "",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=" + quote(f"{full} {clean_address(address)}"),
        "verification_status": "官方門市清單；Google 地圖地點與國土測繪中心行政區已交叉核對（2026-11-16）",
        "store_format": fmt, "opened_date_source": osrc, "opened_date_basis": basis,
    }
    if status != "營業中":
        row["closed_date"] = m.group(1) if m else ""
        row["closed_date_source"] = (re.findall(r"https?://[^\s）)，；]+", item.get("closed_source") or "") or [""])[0]
    return row


def keep_hd(item):
    """東稻家居依使用者指示只收營業中的一般門市：睡眠館、快閃店與已遷址舊店不計"""
    return item["status"] == "營業中" and "睡眠館" not in item["name"] and "快閃" not in item["name"]


def main():
    rows = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    old_n = {}
    for r in rows:
        if r.get("brand") in LEGACY_BRANDS:
            new_brand = LEGACY_BRANDS[r["brand"]]
            old_n[(new_brand, r["store_name"].replace(r["brand"], new_brand, 1))] = r["n"]
        elif r.get("brand") in SOURCES:
            old_n[(r["brand"], r["store_name"])] = r["n"]
    kept = [r for r in rows if r.get("brand") not in SOURCES and r.get("brand") not in LEGACY_BRANDS]
    next_n = max(int(r.get("n") or 0) for r in rows) + 1
    new = []
    for brand, (path, url) in SOURCES.items():
        items = json.loads(path.read_text(encoding="utf-8"))
        if brand in EXTRA_SOURCES:
            items += json.loads(EXTRA_SOURCES[brand].read_text(encoding="utf-8"))
        for item in items:
            if brand == "東稻家居" and not keep_hd(item):
                continue
            row = build(brand, item, item.get("source_url") or url)
            n = old_n.get((brand, row["store_name"]))
            if n is None:
                n, next_n = next_n, next_n + 1
            row["n"] = n
            new.append(row)
    all_rows = kept + new
    MAIN_JSON.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for r in all_rows for k in r))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    raw = VERIFIED_JSON.read_text(encoding="utf-8")
    verified = [v for v in json.loads(raw) if v["brand"] not in SOURCES and v["brand"] not in LEGACY_BRANDS]
    for r in new:
        if r["opened_date"]:
            verified.append({"brand": r["brand"], "store_name": r["store_name"], "date": r["opened_date"],
                             "year": int(r["opened_date"][:4]), "confidence": "confirmed",
                             "sources": [r["opened_date_source"]],
                             "evidence": f"開幕日 {r['opened_date']}（" + ("使用者人工查證" if r["opened_date_source"] == USER_CHECKED else "官方公告或新聞") + "）"})
    VERIFIED_JSON.write_text(json.dumps(verified, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""),
                             encoding="utf-8")
    count = {b: sum(1 for r in new if r["brand"] == b and r["status"] == "營業中") for b in SOURCES}
    print(f"詩肯／東稻家居：{len(new)} 筆；營業中 {count}")


if __name__ == "__main__":
    main()
