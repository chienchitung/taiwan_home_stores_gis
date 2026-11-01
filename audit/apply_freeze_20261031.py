# -*- coding: utf-8 -*-
"""資料凍結於 2026-10-31：補正官方清單同步後需要人工判斷的門市狀態（2026-11-01 查核）。

- 樂家康 內湖東湖店：2026-11-01 萬家福官方門市 API（含量販與超市）已無此店；經濟部商工登記「康達盛通生活事業
  內湖東湖分公司」狀態為廢止（變更核准日 115/10/07）。查無熄燈新聞，結束日期不列。
- 樂家康 台北林森北店：2026-11-01 官方門市 API 已無此店，使用者查證確已結束營業（商工登記東光分公司仍核准設立），
  結束日期未查得。
sync_lejiakang_stores.py 只保留官方清單上的門市，這裡把兩間補回主資料（沿用原本的 n 與欄位）。

居家品牌（2026-11-01 比對官方門市清單／API 與官方新聞）：
- 新光三越台南中山店 2026-10-31 熄燈：店內的無印良品中山門市（官方公告 2026-11-01 停止營業，最後營業日 10/31）、
  宜得利台南中山新光三越店（隨百貨熄燈，宜得利未另發公告）改列已結束營業，結束日 2026-10-31。
- 無印良品 國泰小檜溪門市：2026-10-29 開幕（官方新聞 261029），新增。
- 無印良品 南西門市：2026-05-22 由南西三館（南京西路15號B1）移至南西一館（南京西路12號6F），依遷址規則改採現址開幕日。
- 無印良品 台中港三井Outlet門市：門牌依官方新聞為臺灣大道十段166號（原誤植168號）。
- 宜得利 淡水店：官方門市清單現名「淡水萬家福店」（同址）。
- 宜得利 ISS萬家福桂林店（2025-05）、ISS萬家福重慶店（2025-12）：官網沿革有開幕紀錄、門市查詢頁未列，官網店數 76 含此兩店，
  使用者查證確有營業，補入；座標用所在萬家福門市。
- 無印良品：地址與 Google 地圖不一致者一律以 Google 地圖為準（使用者指示），更正 10 間樓層／門牌，員林門市改名大全聯員林門市。
可重複執行；需在各 sync 腳本之後、apply_verified_opened_dates.py 之前執行（本腳本同步更新 store_opened_dates_verified.json）。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
VERIFIED_JSON = BASE_DIR / "store_opened_dates_verified.json"
GCIS_API = "https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB"
OFFICIAL = "https://www.uni-prosperity.com.tw/stores/?hl=zh-TW"

LEJIAKANG_COMMON = {
    "brand": "樂家康", "store_type": "社區生鮮超市", "region": "北部", "city": "台北市",
    "channel_format": "社區生鮮超市 / 街邊獨立", "geocode_score": 100, "is_co_location": False,
    "source_url": OFFICIAL, "store_format": "社區超市", "opened_date_basis": "商工登記", "opened_date_source": GCIS_API,
}
RESTORE = [
    {**LEJIAKANG_COMMON,
     "store_name": "樂家康 內湖東湖店", "address": "台北市內湖區東湖路69號B1", "district": "內湖區",
     "opened_date": "2017-08-01", "status": "已結束營業", "status_category": "歷史變動（已熄燈/遷址）", "closed_date": "",
     "note": "原家樂福超市，2026-07-01 起更名樂家康；2026-11-01 官方門市清單已無此店，商工登記內湖東湖分公司 2026-10-07 核准廢止；"
             "查無熄燈新聞，結束日期不列",
     "closed_date_source": GCIS_API,
     "lat": 25.0689469, "lng": 121.6151344,
     "clean_address": "台北市內湖區東湖路69號B1", "clean_name": "樂家康 內湖東湖店",
     "clean_query": "樂家康 內湖東湖店 台北市內湖區東湖路69號B1",
     "coordinate_source": "Google 地圖「樂家康超市 內湖東湖店」地點座標（2026-10-13 逐筆比對）",
     "google_maps_url": "https://www.google.com/maps/search/?api=1&query=%E6%A8%82%E5%AE%B6%E5%BA%B7%20%E5%85%A7%E6%B9%96%E6%9D%B1%E6%B9%96%E5%BA%97%20%E5%8F%B0%E5%8C%97%E5%B8%82%E5%85%A7%E6%B9%96%E5%8D%80%E6%9D%B1%E6%B9%96%E8%B7%AF69%E8%99%9FB1",
     "verification_status": "2026-11-01 官方清單已移除；商工登記分公司已廢止",
     "official_store_id": "119", "official_branch_ban": "51462601", "branch_registry_name": "康達盛通生活事業內湖東湖分公司",
     "n": 5251},
    {**LEJIAKANG_COMMON,
     "store_name": "樂家康 台北林森北店", "address": "台北市中山區林森北路413號B1", "district": "中山區",
     "opened_date": "2000-10-24", "status": "已結束營業", "status_category": "歷史變動（已熄燈/遷址）", "closed_date": "",
     "note": "原家樂福超市，2026-07-01 起更名樂家康；2026-11-01 官方門市清單已無此店，使用者查證確已結束營業；"
             "商工登記東光分公司仍為核准設立，結束日期未查得",
     "lat": 25.0599458, "lng": 121.5257295,
     "clean_address": "台北市中山區林森北路413號B1", "clean_name": "樂家康 台北林森北店",
     "clean_query": "樂家康 台北林森北店 台北市中山區林森北路413號B1",
     "coordinate_source": "Google 地圖「樂家康超市 台北林森北店」地點座標（2026-10-13 逐筆比對）",
     "google_maps_url": "https://www.google.com/maps/search/?api=1&query=%E6%A8%82%E5%AE%B6%E5%BA%B7%20%E5%8F%B0%E5%8C%97%E6%9E%97%E6%A3%AE%E5%8C%97%E5%BA%97%20%E5%8F%B0%E5%8C%97%E5%B8%82%E4%B8%AD%E5%B1%B1%E5%8D%80%E6%9E%97%E6%A3%AE%E5%8C%97%E8%B7%AF413%E8%99%9FB1",
     "verification_status": "2026-11-01 官方清單已移除；使用者查證已結束營業",
     "official_store_id": "231", "official_branch_ban": "70788494", "branch_registry_name": "統康生活事業東光分公司",
     "n": 5325},
]

MUJI_NEWS = "https://www.muji.tw/muji-journal/news/news/"
CLOSE_TAINAN = {"status": "已結束營業", "status_category": "歷史變動（已熄燈/遷址）", "closed_date": "2026-10-31"}
# (品牌, 店名): 要更新的欄位；"_rename" 改店名、"_note" 附加在備註後
FIXES = {
    ("無印良品", "無印良品 新光三越台南中山門市"): {
        **CLOSE_TAINAN, "closed_date_source": MUJI_NEWS + "261002.html",
        "_note": "官方公告中山門市 2026-11-01 停止營業（最後營業日 10/31），隨新光三越台南中山店熄燈"},
    ("宜得利", "宜得利 台南中山新光三越店"): {
        **CLOSE_TAINAN, "closed_date_source": "https://www.nownews.com/news/6888059",
        "_note": "新光三越台南中山店 2026-10-31 熄燈，店內門市隨之結束；宜得利未另發閉店公告（2026-11-01 官方門市清單仍列此店）"},
    ("無印良品", "無印良品 新光三越台北南西門市"): {
        "address": "台北市中山區南京西路12號6F（新光三越台北南西店一館）", "clean_address": "台北市中山區南京西路12號",
        "clean_query": "無印良品 新光三越台北南西門市 台北市中山區南京西路12號", "lat": 25.0523038, "lng": 121.5211048,
        "opened_date": "2026-05-22", "opened_date_source": MUJI_NEWS + "260522.html", "opened_date_basis": "新聞／官方",
        "_note": "2026-05-22 由南西三館 B1 移至南西一館 6F（145→210 坪），依遷址規則採現址開幕日；原 2018-08-02 為三館 B1 開幕日"},
    ("無印良品", "無印良品 台中港三井Outlet門市"): {
        "address": "台中市梧棲區臺灣大道十段166號1F（MITSUI OUTLET PARK 台中港）", "clean_address": "台中市梧棲區臺灣大道十段166號",
        "clean_query": "無印良品 台中港三井Outlet門市 台中市梧棲區臺灣大道十段166號"},
    ("無印良品", "無印良品 板橋車站門市"): {"address": "新北市板橋區縣民大道二段7號2F（Global Mall 板橋車站）", "clean_address": "新北市板橋區縣民大道二段7號", "clean_query": "無印良品 板橋車站門市 新北市板橋區縣民大道二段7號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 中和環球門市"): {"address": "新北市中和區中山路三段122號2F（Global Mall 新北中和）", "clean_address": "新北市中和區中山路三段122號", "clean_query": "無印良品 中和環球門市 新北市中和區中山路三段122號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 永和比漾門市"): {"address": "新北市永和區中山路一段238號2F（比漾廣場）", "clean_address": "新北市永和區中山路一段238號", "clean_query": "無印良品 永和比漾門市 新北市永和區中山路一段238號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 林口三井門市"): {"address": "新北市林口區文化二路一段123號1F（MITSUI OUTLET PARK 林口）", "clean_address": "新北市林口區文化二路一段123號", "clean_query": "無印良品 林口三井門市 新北市林口區文化二路一段123號", "lat": 25.0690895, "lng": 121.3653541, "coordinate_source": "Google 地圖地點座標（2026-11-01）", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 樹林秀泰門市"): {"address": "新北市樹林區樹新路40-6號1F（秀泰生活樹林店）", "clean_address": "新北市樹林區樹新路40-6號", "clean_query": "無印良品 樹林秀泰門市 新北市樹林區樹新路40-6號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 新竹大遠百門市"): {"address": "新竹市東區西大路323號7F（新竹大遠百）", "clean_address": "新竹市東區西大路323號", "clean_query": "無印良品 新竹大遠百門市 新竹市東區西大路323號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 豐原太平洋門市"): {"address": "台中市豐原區復興路2號B1F（太平洋百貨豐原店）", "clean_address": "台中市豐原區復興路2號", "clean_query": "無印良品 豐原太平洋門市 台中市豐原區復興路2號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 台南南紡門市"): {"address": "台南市東區中華東路一段358號2F（南紡購物中心 2館）", "clean_address": "台南市東區中華東路一段358號", "clean_query": "無印良品 台南南紡門市 台南市東區中華東路一段358號", "lat": 22.9923209, "lng": 120.2334389, "coordinate_source": "Google 地圖地點座標（2026-11-01）", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 高雄夢時代門市"): {"address": "高雄市前鎮區中華五路789號2F（統一夢時代購物中心）", "clean_address": "高雄市前鎮區中華五路789號", "clean_query": "無印良品 高雄夢時代門市 高雄市前鎮區中華五路789號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 屏東太平洋門市"): {"address": "屏東縣屏東市中正路72號2F（太平洋百貨屏東店）", "clean_address": "屏東縣屏東市中正路72號", "clean_query": "無印良品 屏東太平洋門市 屏東縣屏東市中正路72號", "_note": "地址依 Google 地圖更正（2026-11-01）"},
    ("無印良品", "無印良品 員林大潤發門市"): {"_rename": "無印良品 大全聯員林門市", "address": "彰化縣埔心鄉中山路319號1F（大全聯員林店 / 原大潤發員林店）", "clean_name": "無印良品 大全聯員林門市", "clean_query": "無印良品 大全聯員林門市 彰化縣埔心鄉中山路319號", "_note": "店名與樓層依 Google 地圖更正（2026-11-01）"},
    ("宜得利", "宜得利 淡水店"): {"_rename": "宜得利 淡水萬家福店", "clean_name": "宜得利 淡水萬家福店",
                                  "clean_query": "宜得利 淡水萬家福店 新北市淡水區中山北路二段383號"},
}
ADD = [{
    "brand": "無印良品", "store_name": "無印良品 國泰小檜溪門市", "store_type": "購物中心門市", "region": "北部", "city": "桃園市",
    "address": "桃園市桃園區春日路515號1F（國泰置地生活廣場 小檜溪）", "opened_date": "2026-10-29", "status": "營業中",
    "note": "官方新聞：2026-10-29 開幕，320 坪以上，全台第 76 店", "district": "桃園區",
    "channel_format": "百貨商場 / 購物中心", "status_category": "現行營運中", "lat": 25.0038871, "lng": 121.312874,
    "geocode_score": 100, "clean_address": "桃園市桃園區春日路515號", "clean_name": "無印良品 國泰小檜溪門市",
    "clean_query": "無印良品 國泰小檜溪門市 桃園市桃園區春日路515號", "is_co_location": True,
    "store_format": "百貨／購物中心門市", "opened_date_source": MUJI_NEWS + "261029.html", "opened_date_basis": "新聞／官方",
    "coordinate_source": "Google 地圖地點座標（國土測繪中心確認桃園區）",
}]

for _name, _addr, _dist, _lat, _lng, _ym, _host in (
        ("宜得利 ISS萬家福桂林店", "台北市萬華區桂林路1號（萬家福桂林店內）", "萬華區", 25.0378418, 121.506172, "2025-05", "萬家福 桂林店"),
        ("宜得利 ISS萬家福重慶店", "台北市大同區重慶北路二段171號（萬家福重慶店內）", "大同區", 25.0590902, 121.5117216, "2025-12", "萬家福 重慶店")):
    ADD.append({
        "brand": "宜得利", "store_name": _name, "store_type": "量販店中店", "region": "北部", "city": "台北市",
        "address": _addr, "opened_date": _ym, "status": "營業中",
        "note": "ISS 店中店；宜得利官網沿革記載開幕年月，門市查詢頁未列；官網店數 76 含此店（使用者查證確有此店）",
        "district": _dist, "channel_format": "量販店中店 / 超市複合", "status_category": "現行營運中",
        "lat": _lat, "lng": _lng, "geocode_score": 100, "clean_address": _addr.split("（")[0], "clean_name": _name,
        "clean_query": f"{_name} {_addr.split('（')[0]}", "is_co_location": True, "store_format": "量販店中店",
        "opened_date_source": "https://www.nitori.com.tw/about/history", "opened_date_basis": "新聞／官方",
        "coordinate_source": f"同址「{_host}」座標（店中店無獨立 Google 地點）",
    })


def update_verified(renames):
    raw = VERIFIED_JSON.read_text(encoding="utf-8")
    verified = json.loads(raw)
    for v in verified:
        key = (v["brand"], v["store_name"])
        if key in renames:
            v["store_name"] = renames[key]
        if v["store_name"] == "無印良品 新光三越台北南西門市" and v["date"] != "2026-05-22":
            v.update(date="2026-05-22", year=2026, sources=[MUJI_NEWS + "260410.html", MUJI_NEWS + "260522.html"],
                     evidence="官方新聞：南西門市 2026-05-22 移至南西一館 6F 重新開幕（原 2018-08-02 三館 B1），依遷址規則採現址開幕日")
    have = {(v["brand"], v["store_name"]) for v in verified}
    for a in ADD:
        if (a["brand"], a["store_name"]) not in have:
            verified.append({"brand": a["brand"], "store_name": a["store_name"], "date": a["opened_date"],
                             "year": int(a["opened_date"][:4]), "confidence": "confirmed",
                             "sources": [a["opened_date_source"]], "evidence": a["note"]})
    VERIFIED_JSON.write_text(json.dumps(verified, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""),
                             encoding="utf-8")


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    keys = {(r["brand"], r["store_name"]) for r in RESTORE}
    used_n = {s.get("n") for s in stores if (s["brand"], s["store_name"]) not in keys}
    stores = [s for s in stores if (s["brand"], s["store_name"]) not in keys]
    for row in RESTORE:
        assert row["n"] not in used_n, f"n {row['n']} 已被其他門市使用"
        stores.append(dict(row))
    renames = {}
    for st in stores:
        fix = FIXES.get((st["brand"], st["store_name"]))
        if not fix:
            continue
        fix = dict(fix)
        note = fix.pop("_note", "")
        new_name = fix.pop("_rename", None)
        if note and note not in (st.get("note") or ""):
            st["note"] = (st["note"] + "；" if st.get("note") else "") + note
        if new_name:
            renames[(st["brand"], st["store_name"])] = new_name
            st["store_name"] = new_name
        st.update(fix)
    have = {(st["brand"], st["store_name"]) for st in stores}
    next_n = max(int(st.get("n") or 0) for st in stores) + 1
    for a in ADD:
        if (a["brand"], a["store_name"]) not in have:
            stores.append({**a, "n": next_n})
            next_n += 1
    update_verified(renames)
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)
    print(f"freeze 2026-10-31: restored {len(RESTORE)} rows")


if __name__ == "__main__":
    main()
