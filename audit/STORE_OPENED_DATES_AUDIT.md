# 非全聯品牌開店日期查核（2026-10-04）

## 規則

- 開幕年份只採用有新聞、官方公告或維基百科明確記載的日期；查無來源一律留空，不推估。
- 移除舊版 `build_ikea_gis_dashboard.py` 中的寫死年份表、品牌預設年份（例如大全聯 2002、特力屋 2015）、從備註抓年份（會把熄燈年當開幕年），以及蝦皮店到店依列號產生的假年份。
- 搬遷門市採現址開幕日；同址換品牌（大潤發→大全聯、家樂福→萬家福、特易購→家樂福）採該址量販店原始開幕日；同址歇業後以新店型重新開幕者（大全聯鮮食集）採重新開幕日。
- 年份未知的門市在時間軸上不列入，並顯示「另 N 間開幕年份未知」。
- 查核結果與出處：`audit/store_opened_dates_verified.json`；寫回主資料：`python3 audit/apply_verified_opened_dates.py`（需在各 sync 腳本之後執行）。

## 查核結果

| 品牌 | 門市數 | 有來源 | 未知 |
|---|---|---|---|
| Costco 好市多 | 14 | 14 | 0 |
| IKEA | 11 | 10 | 1 |
| MR. LIVING 居家先生 | 7 | 1 | 6 |
| La-Z-Boy | 1 | 0 | 1 |
| 大全聯 | 22 | 22 | 0 |
| HOLA | 25 | 9 | 16 |
| hoi! 好好生活 | 21 | 7 | 14 |
| 無印良品 | 88 | 14 | 74 |
| 宜得利 | 77 | 25 | 52 |
| 特力屋 | 66 | 16 | 50 |
| 萬家福 | 62 | 50 | 12 |
| 蝦皮店到店 | 3529 | 0 | 3529 |

說明：部分來源為搜尋引擎對維基百科分店列表的摘要（萬家福大多數、大全聯多數），因網路政策無法直接開啟原頁，`evidence` 欄位有註明；屬單一來源，必要時可再抽查。

## 年份被修正的門市（舊儀表板年份 → 查核日期）

| 品牌 | 門市 | 舊 | 查核 | 來源 |
|---|---|---|---|---|
| Costco 好市多 | Costco 好市多 北台中店 | 2007 | 2020-11-20 | https://www.ettoday.net/news/20201019/1834847.htm |
| Costco 好市多 | Costco 好市多 高雄亞灣店 | 1997 | 2026-07-03 | https://www.ctee.com.tw/news/20260703700941-431401 |
| IKEA | IKEA 新竹訂購取貨中心 | 2015 | 2016-09-08 | https://www.chinatimes.com/realtimenews/20160908005922-260405 |
| 大全聯 | 大全聯 內湖店 | 1999 | 2002 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC_(%E5%8F%B0%E7%81%A3) |
| 大全聯 | 大全聯 中和店 | 2002 | 1998 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 土城店 | 2004 | 1998-09 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 碧潭店 | 2000 | 2001 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 景平店 | 2003 | 2001 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 中崙店 | 2026 | 2004-12 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 湳雅店 | 2001 | 1997 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 忠孝店 | 2000 | 1998-09 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 中壢店 | 2003 | 2001 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 頭份店 | 2004 | 2010-11 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 八德店 | 2005 | 2003-12 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC_(%E5%8F%B0%E7%81%A3) |
| 大全聯 | 大全聯 忠明店 | 1999 | 1998 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 斗南店 | 2002 | 1999-08 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 嘉義店 | 2001 | 2008-10-09 | https://www.epochtimes.com/b5/8/10/9/n2291394.htm |
| 大全聯 | 大全聯 台南店 | 2002 | 2000 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 佳里店 | 2006 | 2002 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 鳳山店 | 2001 | 2010-05-05 | https://blog.xuite.net/yjkk0623/blog/33792497 |
| 大全聯 | 大全聯 台東店 | 2002 | 1999-08 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC%E5%8F%B0%E7%81%A3 |
| 大全聯 | 大全聯 鮮食集 | 2018 | 2021-04-28 | https://zh.wikipedia.org/zh-tw/%E5%A4%A7%E6%BD%A4%E7%99%BC_(%E5%8F%B0%E7%81%A3) |
| 大全聯 | 大全聯 青埔店 | 2002 | 2025-12-16 | https://www.storm.mg/article/11087368 |
| HOLA | HOLA 林口三井店 | 2016 | 2024-11 | https://udn.com/news/story/7270/8364539 |
| HOLA | HOLA 新北三峽店 | 2016 | 2013-01-12 | https://tw.news.yahoo.com/%E7%89%B9%E5%8A%9B%E5%B1%8B-hola-12%E6%97%A5%E9%80%B2%E9%A7%90%E5%8C%97%E5%A4%A7%E5%95%86%E5%9C%88-213000155.html |
| HOLA | HOLA 宜蘭羅東店 | 2004 | 2020-10-01 | https://ec.ltn.com.tw/article/breakingnews/3306955 |
| HOLA | HOLA 竹北享平方店 | 2022 | 2024-11-22 | https://www.ettoday.net/news/20241210/2867933.htm |
| HOLA | HOLA 台中西屯店 | 2010 | 2018-05-12 | https://www.ctee.com.tw/news/20180509700020-439803 |
| HOLA | HOLA 台中大墩店 | 2010 | 2019-03-29 | https://www.ctee.com.tw/news/20190328700446-431401 |
| HOLA | HOLA 台中漢神洲際店 | 2025 | 2026-04-10 | https://www.chinatimes.com/realtimenews/20260409002659-260421 |
| hoi! 好好生活 | hoi! 台北微風南京店 | 2019 | 2020-06-05 | https://www.niusnews.com/=P0h80fw0 |
| hoi! 好好生活 | hoi! 新北旗艦店-新店店(8/21試營運!) | 2020 | 2026-08-21 | https://n.yam.com/Article/20260821816569 |
| hoi! 好好生活 | hoi! 台南大遠百成功店 | 2021 | 2024-03-22 | https://www.feds.com.tw/tw/Event/Detail/24736 |
| hoi! 好好生活 | hoi! 桃園旗艦店-八德 | 2020 | 2025-08-08 | https://udn.com/news/story/7270/8906247 |
| 無印良品 | 無印良品 桃園台茂門市 | 2010 | 2016-09-08 | https://www.muji.com/tw/news/news/160909.html |
| 無印良品 | 無印良品 環球A19門市 | 2021 | 2026-06-26 | https://shop.muji.tw/muji-journal/news/news/260626.html |
| 無印良品 | 無印良品 環球A8門市 | 2015 | 2016-03-25 | https://www.chinatimes.com/realtimenews/20160324004892-260410 |
| 無印良品 | 無印良品 愛買桃園門市 | 2022 | 2024-03-28 | https://500times.udn.com/wtimes/story/12671/7862011 |
| 無印良品 | 無印良品 新竹大魯閣門市 | 2022 | 2025-03-27 | https://www.muji.com/tw/news/news/250327.html |
| 無印良品 | 無印良品 頭份尚順門市 | 2015 | 2022-12-07 | https://www.muji.com/tw/news/news/221207.html |
| 無印良品 | 無印良品 台中港三井Outlet門市 | 2018 | 2026-01-13 | https://shop.muji.tw/muji-journal/news/news/260113.html |
| 宜得利 | 宜得利 台北內湖舊宗店 | 2010 | 2014-06 | https://www.nitori.com.tw/about/history |
| 宜得利 | 宜得利 台北中崙大全聯店 | 2026 | 2020-12 | https://www.ettoday.net/news/20201230/1884464.htm |
| 特力屋 | 特力屋 南港興華店(社區店) | 2020 | 2022-09-25 | https://www.findcoupon.tw/store-53329.htm |
| 特力屋 | 特力屋 大安安和店(社區店) | 2019 | 2020-05-30 | https://www.ettoday.net/news/20200531/1726828.htm |
| 特力屋 | 特力屋 中和店 | 1998 | 2003-12 | https://zh.wikipedia.org/zh-tw/%E7%89%B9%E5%8A%9B%E5%B1%8B |
| 特力屋 | 特力屋 羅東店 | 2004 | 2020-10-01 | https://ec.ltn.com.tw/article/breakingnews/3306955 |
| 特力屋 | 特力屋 林森店 | 2014 | 2026-03-13 | https://www.chinatimes.com/realtimenews/20260316000909-260410 |
| 特力屋 | 特力屋 西屯店 | 2001 | 2016-01-22 | https://mercury0314.pixnet.net/blog/posts/9442497899-%E7%94%9F%E6%B4%BB%E3%80%82%E5%8F%B0%E4%B8%AD%E8%A5%BF%E5%B1%AF%E3%80%90%E7%89%B9%E5%8A%9B%E5%B1%8B-%E8%A5%BF%E5%B1%AF%E5%BA%97%E3%80%91 |
| 特力屋 | 特力屋 台中大墩店 | 2017 | 2019-01-11 | https://n.yam.com/Article/20190112881056 |
| 特力屋 | 特力屋 彰化和美店 | 2018 | 2001-03-29 | https://zh.wikipedia.org/zh-tw/%E7%89%B9%E5%8A%9B%E5%B1%8B |
| 特力屋 | 特力屋 台東店 | 2020 | 2024-01-24 | https://estate.ltn.com.tw/article/19488 |
| 特力屋 | 特力屋 高雄大順店 | 2015 | 1998 | https://howlife.cna.com.tw/life/20220311s024.aspx |
| 萬家福 | 萬家福 南港店 | 1992 | 2021-08-18 | https://www.ettoday.net/news/20210819/2059994.htm |
| 萬家福 | 萬家福 北港店 | 2019 | 2002-12 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 西屯店 | 2019 | 2007-04-21 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 北大店 | 2011 | 2009-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 林口店 | 2020 | 2008-03 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 新店店 | 1994 | 2004-11 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 樹林店 | 2006 | 2003-12 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 土城店 | 2006 | 2002-02 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中和店 | 1993 | 2003-12 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 板橋店 | 2002 | 1992-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中平店 | 2003 | 2009-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 蘆洲店 | 2005 | 2008-11 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 重新店 | 1995 | 2007-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 汐科店 | 2022 | 2015-05-08 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 安平店 | 1998 | 2001-09 | https://taikoinfotw.fandom.com/zh-tw/wiki/%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%AE%89%E5%B9%B3%E5%BA%97 |
| 萬家福 | 萬家福 中華店 | 1999 | 1993-11 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 斗六店 | 2004 | 2008-11-28 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 虎尾店 | 2014 | 2015-04-30 | https://www.chinatimes.com/realtimenews/20150505002105-260511 |
| 萬家福 | 萬家福 嘉義店 | 1995 | 1997-09 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 愛河店 | 1989 | 1996 | https://news.tvbs.com.tw/life/3165188 |
| 萬家福 | 萬家福 苗栗店 | 2003 | 2006-08 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中原店 | 1996 | 2002-11-30 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 經國店 | 2000 | 2006-08 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 內壢店 | 1997 | 2002-12 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中壢店 | 2001 | 1998-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 台東店 | 2007 | 2008-09-26 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 宜蘭店 | 2005 | 2008-11 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 花蓮店 | 2006 | 1998-12 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 三民店 | 1993 | 2003-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 內湖店 | 1998 | 2005-07-22 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 太平店 | 2009 | 2008-07-25 | https://www.cosme.net.tw/channel_details/6400 |
| 萬家福 | 萬家福 文心店 | 1996 | 2006-09 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 青海店 | 2007 | 2004-12-09 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 德安店 | 2009 | 2004-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 南投店 | 2004 | 2000-07 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 彰化店 | 2004 | 2000-01 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 中清店 | 2010 | 1999-03 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 埔里店 | 2010 | 2013-12-20 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 平鎮店 | 2017 | 2016-09-03 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 桂林店 | 2001 | 2006-11 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 重慶店 | 2002 | 2006-12 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |
| 萬家福 | 萬家福 天母店 | 1996 | 1991-10 | https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%AE%B6%E6%A8%82%E7%A6%8F%E5%88%86%E5%BA%97%E5%88%97%E8%A1%A8 |

## 尚無可靠來源（年份留空，待補）

- **IKEA**（1）：桃園舊店（中山路店）
- **MR. LIVING 居家先生**（6）：MR. LIVING 台中文心門市（初代首店）、MR. LIVING 新北新莊旗艦店、MR. LIVING 台北內湖門市、MR. LIVING 新竹竹北門市、MR. LIVING 台南崇善門市、MR. LIVING 高雄巨蛋門市
- **La-Z-Boy**（1）：微風南京店
- **HOLA**（16）：新北中和店、台北內湖店、台北士林店、新店裕隆城店、新北重新店、中和環球店、新北土城店、桃園南崁店、新竹店、台中北屯店、彰化店、嘉義店、台南三越小北店、台南仁德店、高雄左營店、高雄夢時代店
- **hoi! 好好生活**（14）：hoi! 台北文昌概念店、hoi! 新北板橋遠百中山店、hoi! 台中西屯店、hoi! 台中南屯店、hoi! 雲林斗六店、hoi! 宜蘭金東店、hoi! 台東店、hoi! 花蓮專櫃(特力屋花蓮店內)、hoi! 高雄左營店、hoi! 台南仁德店、hoi! 新北新莊宏匯店、hoi! 台中復興店、hoi! 桃園大江店、hoi! 桃園南崁店
- **無印良品**（74）：微風門市（初代首店）、信義A11門市、淡水美麗新門市、微風松高旗艦店、統一時代門市、美麗華旗艦店、微風台北車站門市、新光三越台北南西門市、遠東SOGO復興館門市、微風南京門市、館前門市、天母門市、大葉高島屋門市、京站門市、CITYLINK南港門市、CITYLINK內湖門市、景美瀚星門市、板橋車站門市、板橋大遠百門市、遠東百貨板橋門市、新店裕隆城門市、中和環球門市、永和比漾門市、新莊宏匯門市、三重重新門市、林口三井門市、汐止遠雄門市、樹林秀泰門市、徐匯廣場門市、基隆皇冠門市、桃園遠東門市、中壢SOGO門市、中壢大江門市、新竹大遠百門市、新竹巨城門市、竹北享平方門市、新光三越台中中港門市、台中大遠百門市、廣三SOGO門市、中友百貨門市、豐原太平洋門市、員林大潤發門市、雲林斗六門市、嘉義耐斯門市、嘉義垂楊新光門市、新光三越台南新天地門市、新光三越台南中山門市、台南南紡門市、台南三井Outlet門市、台南大遠百門市、高雄大立旗艦店、高雄岡山門市、漢神巨蛋門市、漢神本館門市、高雄夢時代門市、新光三越高雄左營門市、三多門市、SKM Park高雄草衙門市、義大門市、屏東太平洋門市、屏東潮州驛站門市、宜蘭新月門市、花蓮遠東門市、台東門市、愛買台中門市、麗寶MALL門市、遠企門市、松山車站門市、大全聯內湖門市、誠品生活西門門市、南港中信門市、LaLaport南港門市、新店碧潭門市、愛買台南門市
- **宜得利**（52）：台中台糖店、板橋遠東百貨店、汐止遠雄店、永和比漾廣場店、中和景平大全聯店、Mitsui Outlet Park林口店、中和環球店、土城大全聯店、樹林秀泰店、重新萬家福店、新莊店、林口萬家福店、淡水店、新竹大魯閣湳雅店、新竹巨城店、竹北享平方店、中壢店、桃園平鎮大全聯店、桃園愛買店、桃園環球A8店、桃園八德萬家福店、苗栗萬家福店、苗栗頭份大全聯店、DECO HOME LaLaport台中店、LaLaport台中店、台中廣三SOGO店、台中中友百貨店、新店裕隆城店、台中水湳愛買店、北屯大買家店、台中西屯萬家福店、台中文心秀泰店、台中國光大買家、彰化員林大全聯店、南投萬家福店、嘉義耐斯店、嘉義大全聯店、雲林斗六萬家福店、台南中山新光三越店、台南頂美店、DECO HOME Mitsui Outlet Park台南店、台南仁德店、高雄苓雅中正一店、高雄大遠百店、高雄夢時代店、高雄大樂店、高雄新楠萬家福店、高雄左營新光三越店、高雄岡山秀泰店、高雄鳳山大全聯店、屏東環球店、台東店
- **特力屋**（50）：大同重慶北店(社區店)、士林店、汐止新台店(社區店)、三重集美店(社區店)、蘆洲集賢店(社區店)、新店店、蘆洲長安店(社區店)、板橋北門店(社區店)、土城店、板橋合宜店(社區店)、新莊店、淡水中山北店(社區店)、林口中山店(社區店)、基隆義一店(社區店)、桃園大業店(社區店)、八德店、平鎮店、宜蘭宜興店(社區店)、龍潭北龍店(社區店)、湖口和愛店(社區店)、竹北文興店(社區店)、新竹店、頭份中央店(社區店)、苗栗中正店(社區店)、花蓮店、豐原店、北屯店、埔里信義店(社區店)、梧棲中華店(社區店)、大里國光店(社區店)、台中復興店(社區店)、草屯虎山店(社區店)、彰化員林店、斗六店、虎尾公安店(社區店)、嘉義店、朴子四維店(社區店)、新營金華店(社區店)、佳里佳東店(社區店)、永康復國店(社區店)、台南文賢店、台南仁德店、岡山大仁店(社區店)、屏東店、楠梓大學店(社區店)、高雄左營店、三民澄清店(社區店)、高雄鳳山店、苓雅三多店(社區店)、東港光復店(社區店)
- **萬家福**（12）：仁德店、中正店、新營店、楠梓店、光華店、澄清店、成功店、鳳山店、五甲店、鼎山店、豐原店、沙鹿店
