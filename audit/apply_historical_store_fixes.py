# -*- coding: utf-8 -*-
"""修正歷史門市（已歇業／遷址／暫停營業）的地址與備註。

2026-10-06 逐筆查證非全聯品牌的歷史門市：每家都確實存在過，但部分備註的熄燈原因、日期
或地址與新聞／官方公告不符，或寫了查不到出處的細節。這裡改成有出處的內容，查不到的就寫明「未查得」。
出處列在 STORE_OPENED_DATES_AUDIT.md「歷史門市查證」一節。可重複執行。
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MAIN_JSON = DATA_DIR / "taiwan_home_stores_status.json"
MAIN_CSV = DATA_DIR / "taiwan_home_stores_status.csv"

FIXES = {
    ("HOLA", "HOLA 花蓮店"): {
        # 原址「吉安鄉國安一街21號2F」查無出處；實際位於家樂福（現萬家福）花蓮店 B1
        "address": "花蓮縣新城鄉嘉里路15號B1（家樂福花蓮店）",
        "clean_address": "花蓮縣新城鄉嘉里路15號",
        "clean_query": "HOLA 花蓮店 花蓮縣新城鄉嘉里路15號",
        "district": "新城鄉",
        "lat": 24.0154743,
        "lng": 121.610611,
        "channel_format": "量販店中店 / 超市複合",
        "store_format": "量販店中店",
        "note": "位於家樂福花蓮店B1，2024年12月1日結束營業；官方說明為經營策略調整（擬改進駐百貨未及覓得據點）",
    },
    ("HOLA", "HOLA 台南永康店"): {
        "note": "HOLA品牌全台第1號店（1998年9月開幕），營運23年後因租約到期、地主收回，於2021年12月12日熄燈",
    },
    ("hoi! 好好生活", "hoi! 微風松高店（初代首店）"): {
        "note": "2018年與淘寶合作開出的首家智慧門店（Taobao × hoi! 淘寶精選店）；已不在2026-09官方門市清單，熄燈日期與原因未查得",
    },
    ("hoi! 好好生活", "hoi! 台北文昌概念店"): {
        "note": "2019年10月進駐台北文昌家具街；已不在2026-09官方門市清單，熄燈日期與原因未查得",
    },
    ("MR. LIVING 居家先生", "MR. LIVING 台中文心門市（初代首店）"): {
        "note": "居家先生第1家實體門市（2018年），文心路經營約四年後，2022年遷至南屯黎明路旗艦店（遷移月份未查得）",
    },
    ("特力屋", "特力屋 士林店"): {
        "note": "2026年5月11日起配合所在商場整體改裝暫停營業，官方表示非結束營業；截至2026-10未見重新開幕消息",
    },
    ("HOLA", "HOLA 台北士林店"): {
        "note": "2026年5月11日起配合所在商場整體改裝暫停營業，官方預估約半年；截至2026-10未見重新開幕消息",
    },
    ("無印良品", "無印良品 廣三SOGO門市"): {
        "note": "2020年10月4日最後營業日，門市移至對面金典綠園道（金典門市）",
    },
    ("無印良品", "無印良品 漢神本館門市"): {
        "note": "高雄首家無印良品，2024年2月29日因租約到期停止營業（同期漢神本館B2改裝）",
    },
}


def main():
    stores = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    hit = 0
    for s in stores:
        fix = FIXES.get((s.get("brand"), s.get("store_name")))
        if fix:
            s.update(fix)
            hit += 1
    assert hit == len(FIXES), f"matched {hit}/{len(FIXES)}"
    MAIN_JSON.write_text(json.dumps(stores, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(dict.fromkeys(k for row in stores for k in row))
    with open(MAIN_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(stores)
    print(f"historical fixes applied: {hit}")


if __name__ == "__main__":
    main()
