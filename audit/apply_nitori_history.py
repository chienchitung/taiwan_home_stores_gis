# -*- coding: utf-8 -*-
"""以宜得利官網「沿革」（https://www.nitori.com.tw/about/history）的開幕年月更新宜得利門市。

audit/nitori_history_events.json 為該頁解析結果：[年月, 店名, open/close, 原文]（2026-10-05 擷取）。
官方年月優先於新聞與商工登記；若既有日期為同月且更精確（到日），保留到日的日期。
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
VERIFIED = BASE / "store_opened_dates_verified.json"
SRC = "https://www.nitori.com.tw/about/history"
ALIAS = {
    "台北內湖店": "台北内湖店", "新莊店": "新荘店", "淡水店": "淡水萬家福店",
    "北屯大買家店": "台中大買家店", "LaLaport台中店": "LALAPORT台中店",
    "新店裕隆城店": "台北新店裕隆城店", "永和比漾廣場店": "永和比漾店",
    "台北天母新光三越店": "天母新光三越店", "高雄夢時代店（初代首店）": "高雄夢時代店",
}
# 同名店曾閉店後重開：現行門市取最後一次開幕，初代門市取第一次
PICK_FIRST = {"高雄夢時代店（初代首店）"}


def main():
    opens = {}
    for ym, name, kind, _ in json.loads((BASE / "nitori_history_events.json").read_text(encoding="utf-8")):
        if kind == "open":
            opens.setdefault(name, []).append(ym)
    verified = json.loads(VERIFIED.read_text(encoding="utf-8"))
    changed, missing = [], []
    for o in verified:
        if o["brand"] != "宜得利":
            continue
        n = o["store_name"].replace("宜得利 ", "", 1)
        key = ALIAS.get(n, n)
        hits = opens.get(key) or opens.get(key + "店")
        if not hits:
            missing.append(n)
            continue
        ym = hits[0] if n in PICK_FIRST else hits[-1]
        old = o.get("date") or ""
        date = old if old.startswith(ym) and len(old) > 7 else ym
        if o.get("confidence") != "confirmed" or old != date:
            changed.append((n, f"{o.get('confidence')} {old}", date))
        o.update(date=date, year=int(ym[:4]), confidence="confirmed", sources=[SRC],
                 evidence=f"宜得利官網沿革：「{key}」{ym[:4]}年{int(ym[5:])}月開幕"
                          + ("（同名店 2010 年閉店後於 2016-12 重新開幕，此為現行門市）" if len(hits) > 1 and n not in PICK_FIRST else ""))
    VERIFIED.write_text(json.dumps(verified, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in changed:
        print("  ", *c)
    print(f"changed {len(changed)}; not in history: {missing}")


if __name__ == "__main__":
    main()
