# -*- coding: utf-8 -*-
"""把 store_opened_dates_verified.json 的查核結果寫回主資料的 opened_date。

- 全聯福利中心：日期來自商工登記（sync_pxmart_stores.py），這裡不動。
- 蝦皮店到店：沒有公開的開店日期來源，維持空白。
- 其他品牌：只有 confidence == "confirmed"（有新聞／官方來源明確寫出日期或年份）才寫入；
  查無來源的一律清空，不推估。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
VERIFIED_JSON = BASE_DIR / "store_opened_dates_verified.json"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
SKIP_BRANDS = {"全聯福利中心"}


def main():
    verified = json.loads(VERIFIED_JSON.read_text(encoding="utf-8"))
    by_key = {(v["brand"], v["store_name"]): v for v in verified}
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))

    confirmed = cleared = missing = 0
    for s in stores:
        if s.get("brand") in SKIP_BRANDS:
            continue
        v = by_key.get((s.get("brand"), s.get("store_name")))
        if v and v.get("confidence") == "confirmed" and v.get("year"):
            s["opened_date"] = v.get("date") or str(v["year"])
            s["opened_date_source"] = (v.get("sources") or [""])[0]
            confirmed += 1
        else:
            if s.get("brand") != "蝦皮店到店" and not v:
                missing += 1
            s["opened_date"] = ""
            s["opened_date_source"] = ""
            cleared += 1

    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)
    print(f"confirmed {confirmed}, cleared {cleared}, not in verified file {missing}")


if __name__ == "__main__":
    main()
