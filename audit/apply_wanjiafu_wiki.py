# -*- coding: utf-8 -*-
"""以維基百科「萬家福分店列表」營運中分店表的「開業日」更新萬家福門市。

audit/wanjiafu_wiki_stores.json 為該表解析結果（2026-10-05 擷取，表內各列附新聞出處）。
規則：
- 同一門市有多個日期（例：原特易購／台糖量販／愛買，後由家樂福接手）時，採「家樂福」開業日，
  因儀表板顯示的是本品牌於該址的開幕；原經營者日期保留在 evidence。
- 搬遷門市（南港店第二代）採現址開業日。
- 既有日期若同月且更精確（到日），保留到日的日期。
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
VERIFIED = BASE / "store_opened_dates_verified.json"
SRC = "https://zh.wikipedia.org/wiki/萬家福分店列表"
ALIAS = {"内湖店": "內湖店", "内壢店": "內壢店", "臺東店": "台東店"}


def to_date(s):
    m = re.search(r"(\d{4})年(?:(\d{1,2})月)?(?:(\d{1,2})日)?", s)
    y, mo, d = m.groups()
    return y + (f"-{int(mo):02d}" if mo else "") + (f"-{int(d):02d}" if d else "")


def main():
    rows = json.loads((BASE / "wanjiafu_wiki_stores.json").read_text(encoding="utf-8"))
    verified = json.loads(VERIFIED.read_text(encoding="utf-8"))
    by = {o["store_name"]: o for o in verified if o["brand"] == "萬家福"}
    changed = []
    for r in rows:
        name = "萬家福 " + ALIAS.get(r["name"], r["name"])
        o = by.get(name)
        if not o:
            print("not in data:", name)
            continue
        parts = [p.strip() for p in r["opened"].split(" / ")]
        pick = next((p for p in parts if "家樂福" in p), None) or next((p for p in parts if "第二代" in p), None) or parts[-1]
        date = to_date(pick)
        old = o.get("date") or ""
        if old.startswith(date) and len(old) > len(date):
            date = old
        if o["confidence"] != "confirmed" or old != date:
            changed.append((name, f'{o["confidence"]} {old}', date))
        o.update(date=date, year=int(date[:4]), confidence="confirmed", sources=[SRC],
                 evidence="維基百科萬家福分店列表「開業日」：" + r["opened"]
                          + ("；採家樂福於此址開業日" if len(parts) > 1 else ""))
    VERIFIED.write_text(json.dumps(verified, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in changed:
        print("  ", *c)
    print("changed", len(changed))


if __name__ == "__main__":
    main()
