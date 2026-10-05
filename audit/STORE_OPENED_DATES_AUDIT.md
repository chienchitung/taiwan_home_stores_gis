# 非全聯品牌開店日期查核（2026-10-04）

## 規則

- 開幕年份只採用有新聞、官方公告或維基百科明確記載的日期；查無來源一律留空，不推估。
- 移除舊版 `build_ikea_gis_dashboard.py` 中的寫死年份表、品牌預設年份（例如大全聯 2002、特力屋 2015）、從備註抓年份（會把熄燈年當開幕年），以及蝦皮店到店依列號產生的假年份。
- 搬遷門市採現址開幕日；同址換品牌（大潤發→大全聯、家樂福→萬家福、特易購→家樂福）採該址量販店原始開幕日；同址歇業後以新店型重新開幕者（大全聯鮮食集）採重新開幕日。
- 年份未知的門市在時間軸上不列入，並顯示「另 N 間開幕年份未知」。
- 查無新聞的門市，改用經濟部商工登記「分公司核准設立日」（`audit/apply_gcis_branch_dates.py`，原始資料在 `audit/gcis/`），與全聯同一標準；儀表板資料以 `opened_date_basis` 標示「新聞／官方」或「商工登記」。
- 宜得利以官網沿革（https://www.nitori.com.tw/about/history，2026-10-05 擷取，`audit/nitori_history_events.json`）為準，`audit/apply_nitori_history.py` 套用；此頁也更正了先前依搜尋摘要記錄的 3 筆（台北內湖舊宗店 2014-06→2025-12、微風松高 2022-07→2022-08、台中忠明大全聯 2023-09→2023-08）。
- 查核結果與出處：`audit/store_opened_dates_verified.json`；寫回主資料：`python3 audit/apply_verified_opened_dates.py`（需在各 sync 腳本之後執行）。

## 查核結果

| 品牌 | 門市數 | 新聞／官方 | 商工登記 | 未知 |
|---|---|---|---|---|
| Costco 好市多 | 14 | 14 | 0 | 0 |
| IKEA | 11 | 10 | 1 | 0 |
| MR. LIVING 居家先生 | 7 | 1 | 6 | 0 |
| La-Z-Boy | 1 | 0 | 0 | 1 |
| 大全聯 | 22 | 22 | 0 | 0 |
| HOLA | 25 | 9 | 12 | 4 |
| hoi! 好好生活 | 21 | 8 | 0 | 13 |
| 無印良品 | 88 | 51 | 0 | 37 |
| 宜得利 | 77 | 25 | 2 | 50 |
| 特力屋 | 66 | 20 | 46 | 0 |
| 萬家福 | 62 | 50 | 0 | 12 |
| 蝦皮店到店 | 3529 | 0 | 0 | 3529 |

商工登記日的可靠度：以已有新聞日期的門市比對，2010 年後新設門市的登記日約早於開幕 0.5～3 個月（如特力屋新竹林森登記 2025-11-12／開幕 2026-03-13、台東 2024-01-08／2024-01-24、IKEA 台中 2013-07-16／2013-09-05）；早期門市若曾重新登記會晚於實際開幕（特力屋南崁 1996 開幕／2010 登記、IKEA 高雄 2006／2009），此類已有新聞者一律以新聞為準。萬家福、台灣無印良品、好好生活（hoi!）公司名下無對應的門市分公司登記，宜得利只有 3 家分公司，無法以此補齊。

說明：部分新聞來源為搜尋引擎對維基百科分店列表的摘要（萬家福大多數、大全聯多數），因網路政策無法直接開啟原頁，`evidence` 欄位有註明；無印良品多數取自 MUJI 官方新聞（網址末段為公告日期 YYMMDD）。

## 年份被修正的門市（舊儀表板年份 → 查核日期，共 177 間）

| 品牌 | 門市 | 舊 | 查核 | 依據 | 來源 |
|---|---|---|---|---|---|
| Costco 好市多 | Costco 好市多 北台中店 | 2007 | 2020-11-20 | 新聞／官方 | https://www.ettoday.net/news/20201019/1834847.htm |
| Costco 好市多 | Costco 好市多 高雄亞灣店 | 1997 | 2026-07-03 | 新聞／官方 | https://www.ctee.com.tw/news/20260703700941-431401 |
| IKEA | IKEA 新竹訂購取貨中心 | 2015 | 2016-09-08 | 新聞／官方 | https://www.chinatimes.com/realtimenews/20160908005922-260405 |
| MR. LIVING 居家先生 | MR. LIVING 新北新莊旗艦店 | 2023 | 2024-09-19 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 65905937 |
| MR. LIVING 居家先生 | MR. LIVING 新竹竹北門市 | 2021 | 2020-03-19 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 65905937 |
| MR. LIVING 居家先生 | MR. LIVING 台南崇善門市 | 2021 | 2023-07-31 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 65905937 |
| MR. LIVING 居家先生 | MR. LIVING 高雄巨蛋門市 | 2020 | 2018-10-05 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 65905937 |
| 大全聯 | 大全聯 內湖店 | 1999 | 2002 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC_(%E5%8F%B0%E7%81%A3) |
| 大全聯 | 大全聯 中和店 | 2002 | 1998 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 土城店 | 2004 | 1998-09 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 碧潭店 | 2000 | 2001 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 景平店 | 2003 | 2001 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 中崙店 | 2026 | 2004-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 湳雅店 | 2001 | 1997 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 忠孝店 | 2000 | 1998-09 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 中壢店 | 2003 | 2001 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 頭份店 | 2004 | 2010-11 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 八德店 | 2005 | 2003-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC_(%E5%8F%B0%E7%81%A3) |
| 大全聯 | 大全聯 忠明店 | 1999 | 1998 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 斗南店 | 2002 | 1999-08 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 嘉義店 | 2001 | 2008-10-09 | 新聞／官方 | https://www.epochtimes.com/b5/8/10/9/n2291394.htm |
| 大全聯 | 大全聯 台南店 | 2002 | 2000 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 佳里店 | 2006 | 2002 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 鳳山店 | 2001 | 2010-05-05 | 新聞／官方 | https://blog.xuite.net/yjkk0623/blog/33792497 |
| 大全聯 | 大全聯 台東店 | 2002 | 1999-08 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 鮮食集 | 2018 | 2021-04-28 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC_(%E5%8F%B0%E7%81%A3) |
| 大全聯 | 大全聯 青埔店 | 2002 | 2025-12-16 | 新聞／官方 | https://www.storm.mg/article/11087368 |
| HOLA | HOLA 新北中和店 | 2000 | 2003-10-21 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 台北內湖店 | 1999 | 2000-01-25 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 台北士林店 | 1999 | 2001-01-15 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 新北重新店 | 2014 | 2021-11-24 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 新北土城店 | 2014 | 2006-02-22 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 林口三井店 | 2016 | 2024-11 | 新聞／官方 | https://udn.com/news/story/7270/8364539 |
| HOLA | HOLA 新北三峽店 | 2016 | 2013-01-12 | 新聞／官方 | https://tw.news.yahoo.com/%E7%89%B9%E5%8A%9B%E5%B1%8B-hola-12%E6%97%A5%E9%80%B2%E9%A7%90%E5%8C%97%E5%A4%A7%E5%95%86%E5%9C%88-213000155.html |
| HOLA | HOLA 宜蘭羅東店 | 2004 | 2020-10-01 | 新聞／官方 | https://ec.ltn.com.tw/article/breakingnews/3306955 |
| HOLA | HOLA 竹北享平方店 | 2022 | 2024-11-22 | 新聞／官方 | https://www.ettoday.net/news/20241210/2867933.htm |
| HOLA | HOLA 新竹店 | 1999 | 2010-04-12 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 台中北屯店 | 2001 | 2004-07-27 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 台中西屯店 | 2010 | 2018-05-12 | 新聞／官方 | https://www.ctee.com.tw/news/20180509700020-439803 |
| HOLA | HOLA 台中大墩店 | 2010 | 2019-03-29 | 新聞／官方 | https://www.ctee.com.tw/news/20190328700446-431401 |
| HOLA | HOLA 彰化店 | 2018 | 2010-12-14 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 嘉義店 | 2006 | 2013-01-10 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 台中漢神洲際店 | 2025 | 2026-04-10 | 新聞／官方 | https://www.chinatimes.com/realtimenews/20260409002659-260421 |
| HOLA | HOLA 台南仁德店 | 2002 | 2005-11-07 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 高雄左營店 | 2001 | 2005-02-17 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| HOLA | HOLA 高雄夢時代店 | 2007 | 2011-06-08 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| hoi! 好好生活 | hoi! 台北微風南京店 | 2019 | 2020-06-05 | 新聞／官方 | https://www.niusnews.com/=P0h80fw0 |
| hoi! 好好生活 | hoi! 新北旗艦店-新店店(8/21試營運!) | 2020 | 2026-08-21 | 新聞／官方 | https://n.yam.com/Article/20260821816569 |
| hoi! 好好生活 | hoi! 台南大遠百成功店 | 2021 | 2024-03-22 | 新聞／官方 | https://www.feds.com.tw/tw/Event/Detail/24736 |
| hoi! 好好生活 | hoi! 桃園旗艦店-八德 | 2020 | 2025-08-08 | 新聞／官方 | https://udn.com/news/story/7270/8906247 |
| 無印良品 | 無印良品 信義A11門市 | 2005 | 2016-07-20 | 新聞／官方 | https://www.muji.com/tw/news/news/160720.html |
| 無印良品 | 無印良品 微風台北車站門市 | 2007 | 2018-04-03 | 新聞／官方 | https://www.muji.com/tw/news/news/18040301.html |
| 無印良品 | 無印良品 新光三越台北南西門市 | 2008 | 2018-08-02 | 新聞／官方 | https://www.muji.tw/tw/news/news/180802.html |
| 無印良品 | 無印良品 CITYLINK南港門市 | 2014 | 2018-06-04 | 新聞／官方 | https://www.muji.com/tw/news/news/180529.html |
| 無印良品 | 無印良品 景美瀚星門市 | 2015 | 2019-08-23 | 新聞／官方 | https://www.muji.com/tw/news/news/190823.html |
| 無印良品 | 無印良品 板橋車站門市 | 2010 | 2024-12-12 | 新聞／官方 | https://www.muji.com/tw/news/news/241212.html |
| 無印良品 | 無印良品 林口三井門市 | 2016 | 2024-11-14 | 新聞／官方 | https://500times.udn.com/wtimes/story/12671/8360514 |
| 無印良品 | 無印良品 汐止遠雄門市 | 2015 | 2016-04-27 | 新聞／官方 | https://www.muji.com/tw/news/news/160428.html |
| 無印良品 | 無印良品 徐匯廣場門市 | 2012 | 2017-11-17 | 新聞／官方 | https://www.muji.com/tw/news/news/171117.html |
| 無印良品 | 無印良品 桃園台茂門市 | 2010 | 2016-09-08 | 新聞／官方 | https://www.muji.com/tw/news/news/160909.html |
| 無印良品 | 無印良品 環球A19門市 | 2021 | 2026-06-26 | 新聞／官方 | https://shop.muji.tw/muji-journal/news/news/260626.html |
| 無印良品 | 無印良品 環球A8門市 | 2015 | 2016-03-25 | 新聞／官方 | https://www.chinatimes.com/realtimenews/20160324004892-260410 |
| 無印良品 | 無印良品 愛買桃園門市 | 2022 | 2024-03-28 | 新聞／官方 | https://500times.udn.com/wtimes/story/12671/7862011 |
| 無印良品 | 無印良品 新竹大魯閣門市 | 2022 | 2025-03-27 | 新聞／官方 | https://www.muji.com/tw/news/news/250327.html |
| 無印良品 | 無印良品 頭份尚順門市 | 2015 | 2022-12-07 | 新聞／官方 | https://www.muji.com/tw/news/news/221207.html |
| 無印良品 | 無印良品 台中港三井Outlet門市 | 2018 | 2026-01-13 | 新聞／官方 | https://shop.muji.tw/muji-journal/news/news/260113.html |
| 無印良品 | 無印良品 員林大潤發門市 | 2022 | 2024-09-12 | 新聞／官方 | https://www.muji.com/tw/news/news/240912.html |
| 無印良品 | 無印良品 雲林斗六門市 | 2024 | 2025-11-21 | 新聞／官方 | https://www.muji.tw/tw/news/news/251121.html |
| 無印良品 | 無印良品 台南南紡門市 | 2014 | 2020-12-25 | 新聞／官方 | https://storeinfo.muji.tw/nf/ |
| 無印良品 | 無印良品 台南三井Outlet門市 | 2022 | 2026-03-20 | 新聞／官方 | https://shop.muji.tw/muji-journal/news/news/260317.html |
| 無印良品 | 無印良品 SKM Park高雄草衙門市 | 2016 | 2020-03-27 | 新聞／官方 | https://www.muji.com/tw/zh_tw/shop/detail/200311?error=login_required |
| 無印良品 | 無印良品 義大門市 | 2010 | 2015-07-25 | 新聞／官方 | https://shop.muji.tw/Shop/StoreDetail/41566/37654 |
| 無印良品 | 無印良品 屏東太平洋門市 | 2013 | 2017-09-22 | 新聞／官方 | https://www.muji.tw/muji-journal/news/news/170922.html |
| 無印良品 | 無印良品 宜蘭新月門市 | 2008 | 2016-05-21 | 新聞／官方 | https://www.muji.tw/tw/news/news/160523.html |
| 無印良品 | 無印良品 松山車站門市 | 2019 | 2020-01-09 | 新聞／官方 | https://www.muji.com/tw/news/news/200109.html |
| 無印良品 | 無印良品 誠品生活西門門市 | 2018 | 2017-06-22 | 新聞／官方 | https://www.muji.tw/tw/news/news/170622.html |
| 宜得利 | 宜得利 台北內湖舊宗店 | 2010 | 2014-06 | 新聞／官方 | https://www.nitori.com.tw/about/history |
| 宜得利 | 宜得利 台北中崙大全聯店 | 2026 | 2020-12 | 新聞／官方 | https://www.ettoday.net/news/20201230/1884464.htm |
| 特力屋 | 特力屋 南港興華店(社區店) | 2020 | 2021-09-25 | 新聞／官方 | https://www.findcoupon.tw/store-53329.htm |
| 特力屋 | 特力屋 大安安和店(社區店) | 2019 | 2020-05-30 | 新聞／官方 | https://www.ettoday.net/news/20200531/1726828.htm |
| 特力屋 | 特力屋 大同重慶北店(社區店) | 2020 | 2023-04-27 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 士林店 | 1997 | 2000-12-29 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 汐止新台店(社區店) | 2020 | 2024-05-08 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 三重集美店(社區店) | 2021 | 2020-12-28 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 蘆洲集賢店(社區店) | 2023 | 2019-11-11 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 新店店 | 2012 | 2004-10-05 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 中和店 | 1998 | 2003-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E7%89%B9%E5%8A%9B%E5%B1%8B |
| 特力屋 | 特力屋 蘆洲長安店(社區店) | 2020 | 2021-03-15 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 板橋北門店(社區店) | 2022 | 2025-10-30 | 新聞／官方 | https://www.threads.com/@trplus_summer_sunny/post/DQb7kPNEtBh |
| 特力屋 | 特力屋 土城店 | 2014 | 2001-10-24 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 板橋合宜店(社區店) | 2020 | 2026-05-08 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 新莊店 | 1998 | 1997-11-22 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 淡水中山北店(社區店) | 2021 | 2025-11-06 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 林口中山店(社區店) | 2021 | 2019-06-27 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 基隆義一店(社區店) | 2021 | 2020-10-20 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 桃園大業店(社區店) | 2021 | 2019-07-24 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 八德店 | 2009 | 2010-12-09 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 平鎮店 | 1999 | 2000-01-29 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 宜蘭宜興店(社區店) | 2024 | 2022-07-15 | 新聞／官方 | https://howlife.cna.com.tw/life/20220719s004.aspx |
| 特力屋 | 特力屋 龍潭北龍店(社區店) | 2021 | 2020-12-24 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 羅東店 | 2004 | 2020-10-01 | 新聞／官方 | https://ec.ltn.com.tw/article/breakingnews/3306955 |
| 特力屋 | 特力屋 湖口和愛店(社區店) | 2021 | 2022-10-21 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 竹北文興店(社區店) | 2021 | 2019-10-18 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 新竹店 | 1999 | 2003-08-06 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 林森店 | 2014 | 2026-03-13 | 新聞／官方 | https://www.chinatimes.com/realtimenews/20260316000909-260410 |
| 特力屋 | 特力屋 頭份中央店(社區店) | 2021 | 2020-06-15 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 花蓮店 | 2005 | 2007-10-17 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 豐原店 | 2010 | 2013-08-02 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 北屯店 | 2000 | 2001-10-12 | 新聞／官方 | https://travel.taichung.gov.tw/zh-tw/shop/consume/4782 |
| 特力屋 | 特力屋 埔里信義店(社區店) | 2022 | 2021-12-21 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 梧棲中華店(社區店) | 2024 | 2022-01-17 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 西屯店 | 2001 | 2016-01-22 | 新聞／官方 | https://mercury0314.pixnet.net/blog/posts/9442497899-%E7%94%9F%E6%B4%BB%E3%80%82%E5%8F%B0%E4%B8%AD%E8%A5%BF%E5%B1%AF%E3%80%90%E7%89%B9%E5%8A%9B%E5%B1%8B-%E8%A5%BF%E5%B1%AF%E5%BA%97%E3%80%91 |
| 特力屋 | 特力屋 台中大墩店 | 2017 | 2019-01-11 | 新聞／官方 | https://n.yam.com/Article/20190112881056 |
| 特力屋 | 特力屋 台中復興店(社區店) | 2022 | 2020-12-10 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 草屯虎山店(社區店) | 2020 | 2012-07-06 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 彰化和美店 | 2018 | 2001-03-29 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E7%89%B9%E5%8A%9B%E5%B1%8B |
| 特力屋 | 特力屋 彰化員林店 | 2017 | 2001-09-27 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 斗六店 | 2007 | 2022-06-24 | 新聞／官方 | https://howlife.cna.com.tw/life/20220624s006.aspx |
| 特力屋 | 特力屋 虎尾公安店(社區店) | 2023 | 2025-08-08 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 嘉義店 | 2003 | 1999-08-10 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 朴子四維店(社區店) | 2024 | 2022-07-20 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 新營金華店(社區店) | 2023 | 2020-03-10 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 佳里佳東店(社區店) | 2023 | 2021-04-27 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 台東店 | 2020 | 2024-01-24 | 新聞／官方 | https://estate.ltn.com.tw/article/19488 |
| 特力屋 | 特力屋 永康復國店(社區店) | 2021 | 2020-03-18 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 台南文賢店 | 2011 | 1999-08-10 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 台南仁德店 | 1998 | 2003-04-28 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 岡山大仁店(社區店) | 2022 | 2020-12-10 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 屏東店 | 2006 | 2004-10-11 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 楠梓大學店(社區店) | 2022 | 2023-04-27 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 高雄左營店 | 2001 | 2005-01-26 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 三民澄清店(社區店) | 2022 | 2020-08-18 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 高雄大順店 | 2015 | 1998 | 新聞／官方 | https://howlife.cna.com.tw/life/20220311s024.aspx |
| 特力屋 | 特力屋 苓雅三多店(社區店) | 2022 | 2021-10-07 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 特力屋 | 特力屋 東港光復店(社區店) | 2023 | 2021-12-01 | 商工登記 | https://data.gcis.nat.gov.tw/od/data/api/FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB?$format=json&$filter=Business_Accounting_NO eq 89390488 |
| 萬家福 | 萬家福 南港店 | 1992 | 2021-08-18 | 新聞／官方 | https://www.ettoday.net/news/20210819/2059994.htm |
| 萬家福 | 萬家福 北港店 | 2019 | 2002-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 西屯店 | 2019 | 2007-04-21 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 北大店 | 2011 | 2009-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 林口店 | 2020 | 2008-03 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 新店店 | 1994 | 2004-11 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 樹林店 | 2006 | 2003-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 土城店 | 2006 | 2002-02 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中和店 | 1993 | 2003-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 板橋店 | 2002 | 1992-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中平店 | 2003 | 2009-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 蘆洲店 | 2005 | 2008-11 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 重新店 | 1995 | 2007-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 汐科店 | 2022 | 2015-05-08 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 安平店 | 1998 | 2001-09 | 新聞／官方 | https://taikoinfotw.fandom.com/zh-tw/wiki/%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%AE%89%E5%B9%B3%E5%BA%97 |
| 萬家福 | 萬家福 中華店 | 1999 | 1993-11 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 斗六店 | 2004 | 2008-11-28 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 虎尾店 | 2014 | 2015-04-30 | 新聞／官方 | https://www.chinatimes.com/realtimenews/20150505002105-260511 |
| 萬家福 | 萬家福 嘉義店 | 1995 | 1997-09 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 愛河店 | 1989 | 1996 | 新聞／官方 | https://news.tvbs.com.tw/life/3165188 |
| 萬家福 | 萬家福 苗栗店 | 2003 | 2006-08 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中原店 | 1996 | 2002-11-30 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 經國店 | 2000 | 2006-08 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 內壢店 | 1997 | 2002-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中壢店 | 2001 | 1998-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 台東店 | 2007 | 2008-09-26 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 宜蘭店 | 2005 | 2008-11 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 花蓮店 | 2006 | 1998-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 三民店 | 1993 | 2003-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 內湖店 | 1998 | 2005-07-22 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 太平店 | 2009 | 2008-07-25 | 新聞／官方 | https://www.cosme.net.tw/channel_details/6400 |
| 萬家福 | 萬家福 文心店 | 1996 | 2006-09 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 青海店 | 2007 | 2004-12-09 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 德安店 | 2009 | 2004-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 南投店 | 2004 | 2000-07 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 彰化店 | 2004 | 2000-01 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中清店 | 2010 | 1999-03 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 埔里店 | 2010 | 2013-12-20 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 平鎮店 | 2017 | 2016-09-03 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 桂林店 | 2001 | 2006-11 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 重慶店 | 2002 | 2006-12 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 天母店 | 1996 | 1991-10 | 新聞／官方 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |

## 尚無可靠來源（年份留空，待補）

多為百貨／量販內專櫃，查無公開開幕報導，品牌也未為各櫃登記分公司。

- **La-Z-Boy**（1）：微風南京店
- **HOLA**（4）：新店裕隆城店、中和環球店、桃園南崁店、台南三越小北店
- **hoi! 好好生活**（13）：hoi! 新北板橋遠百中山店、hoi! 台中西屯店、hoi! 台中南屯店、hoi! 雲林斗六店、hoi! 宜蘭金東店、hoi! 台東店、hoi! 花蓮專櫃(特力屋花蓮店內)、hoi! 高雄左營店、hoi! 台南仁德店、hoi! 新北新莊宏匯店、hoi! 台中復興店、hoi! 桃園大江店、hoi! 桃園南崁店
- **無印良品**（37）：淡水美麗新門市、遠東SOGO復興館門市、微風南京門市、館前門市、天母門市、大葉高島屋門市、京站門市、CITYLINK內湖門市、板橋大遠百門市、遠東百貨板橋門市、中和環球門市、永和比漾門市、三重重新門市、基隆皇冠門市、桃園遠東門市、中壢SOGO門市、中壢大江門市、新竹大遠百門市、新竹巨城門市、竹北享平方門市、新光三越台中中港門市、台中大遠百門市、廣三SOGO門市、中友百貨門市、豐原太平洋門市、嘉義耐斯門市、嘉義垂楊新光門市、新光三越台南新天地門市、新光三越台南中山門市、台南大遠百門市、漢神本館門市、新光三越高雄左營門市、三多門市、屏東潮州驛站門市、花蓮遠東門市、遠企門市、南港中信門市
- **宜得利**（50）：台中台糖店、板橋遠東百貨店、汐止遠雄店、永和比漾廣場店、中和景平大全聯店、Mitsui Outlet Park林口店、中和環球店、土城大全聯店、樹林秀泰店、重新萬家福店、新莊店、林口萬家福店、淡水店、新竹大魯閣湳雅店、新竹巨城店、竹北享平方店、桃園平鎮大全聯店、桃園愛買店、桃園環球A8店、桃園八德萬家福店、苗栗萬家福店、苗栗頭份大全聯店、DECO HOME LaLaport台中店、LaLaport台中店、台中廣三SOGO店、台中中友百貨店、新店裕隆城店、台中水湳愛買店、北屯大買家店、台中西屯萬家福店、台中文心秀泰店、台中國光大買家、彰化員林大全聯店、南投萬家福店、嘉義耐斯店、嘉義大全聯店、雲林斗六萬家福店、台南中山新光三越店、DECO HOME Mitsui Outlet Park台南店、台南仁德店、高雄苓雅中正一店、高雄大遠百店、高雄夢時代店、高雄大樂店、高雄新楠萬家福店、高雄左營新光三越店、高雄岡山秀泰店、高雄鳳山大全聯店、屏東環球店、台東店
- **萬家福**（12）：仁德店、中正店、新營店、楠梓店、光華店、澄清店、成功店、鳳山店、五甲店、鼎山店、豐原店、沙鹿店
