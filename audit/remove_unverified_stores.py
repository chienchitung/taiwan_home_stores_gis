# -*- coding: utf-8 -*-
"""移除查無存在證據或與其他品牌重複的門市紀錄。

這些紀錄是早期資料整理時留下的「已結束營業」歷史門市，經 2026-10-06 重新核對：
- 查無無印良品曾在該址設櫃的任何新聞或官方紀錄 → 移除。
- 三重重新、竹北享平方實為 HOLA 門市（資料中已有 HOLA 新北重新店、HOLA 竹北享平方店同址紀錄）→ 移除重複的無印良品紀錄。
同步從 store_opened_dates_verified.json 移除。可重複執行。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"
VERIFIED_JSON = BASE_DIR / "store_opened_dates_verified.json"

REMOVE = {
    ("無印良品", "無印良品 淡水美麗新門市"): "查無無印良品曾在美麗新淡水廣場設櫃的紀錄",
    ("無印良品", "無印良品 天母門市"): "查無新光三越天母店無印良品門市紀錄",
    ("無印良品", "無印良品 京站門市"): "查無京站無印良品門市紀錄",
    ("無印良品", "無印良品 CITYLINK內湖門市"): "查無CITYLINK內湖無印良品門市紀錄",
    ("無印良品", "無印良品 嘉義垂楊新光門市"): "查無新光三越嘉義垂楊無印良品門市紀錄",
    ("無印良品", "無印良品 台南大遠百門市"): "查無遠百台南無印良品門市紀錄",
    ("無印良品", "無印良品 屏東潮州驛站門市"): "查無潮州無印良品門市紀錄",
    ("無印良品", "無印良品 三重重新門市"): "同址為 HOLA 新北重新店，品牌誤植",
    ("無印良品", "無印良品 竹北享平方門市"): "同址為 HOLA 竹北享平方店，品牌誤植",
}


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    kept = [s for s in stores if (s.get("brand"), s.get("store_name")) not in REMOVE]
    print(f"stores: removed {len(stores) - len(kept)}")
    MAIN_JSON.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in kept for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept)

    verified = json.loads(VERIFIED_JSON.read_text(encoding="utf-8"))
    v_kept = [v for v in verified if (v["brand"], v["store_name"]) not in REMOVE]
    print(f"verified: removed {len(verified) - len(v_kept)}")
    VERIFIED_JSON.write_text(json.dumps(v_kept, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
