# 七大居家品牌實體據點全面複核

更新日：2026-09-11

## 結論

本次把「品牌官方據點」與「一般完整門市」拆成兩個口徑。七大品牌在儀表板共有 **270 個營運中實體據點**；其中 **263 間為一般／正式門市**，另有 **7 個特殊型態據點**。所有 270 筆都有台灣範圍內的座標，並完成官方地址與 Google Maps 落點的交叉檢查；已知的跨品牌誤列只有 `HOLA La-Z-Boy 微風南京店`，已改列 La-Z-Boy 並排除於七大品牌統計。

| 品牌 | 官方營運中據點 | 一般／正式門市 | 特殊型態 | 本次處理 |
|---|---:|---:|---:|---|
| 宜得利 | 75 | 71 | 4 間 DECO HOME | 保留在宜得利體系，但標記為子品牌門市 |
| 無印良品 | 75 | 74 | 1 間期間限定門市 | 補入愛買台中、麗寶MALL；站前秀泰更名新時代台中 |
| IKEA | 9 | 8 | 1 個訂購取貨中心 | 新竹據點不再視為一般門市 |
| 特力屋 | 65 | 65 | 0 | 另有士林店暫停營業，不列營運中 |
| HOLA | 21 | 21 | 0 | 移除混入官方 API 的 La-Z-Boy 專櫃；另有士林店暫停營業 |
| hoi! 好好生活 | 19 | 18 | 1 個店中店／專櫃 | 花蓮據點標示為設於特力屋內的專櫃 |
| MR. LIVING 居家先生 | 6 | 6 | 0 | 名冊與地址一致 |

## 發現與修正

1. **HOLA／La-Z-Boy 混列**：HOLA 的門市 API 夾帶 La-Z-Boy 微風南京專櫃。Google Maps 的實際 POI 是 La-Z-Boy，並非 HOLA 完整門市；資料已改列 `La-Z-Boy`、排除於七大品牌，更新程式也加入防呆，日後刷新不會再匯回 HOLA。
2. **無印良品漏店**：原資料 73 間，漏了 2025-08-15 開幕的愛買台中門市，以及 2026-07-17 開幕的麗寶MALL門市。官方公告明載麗寶MALL為全台第 75 店，補齊後與官方數量一致。[愛買台中公告](https://shop.muji.tw/muji-journal/news/news/250815.html)、[麗寶MALL公告](https://www.muji.tw/muji-journal/news/news/260717.html)
3. **無印良品名稱更新**：台中市東區南京路 66 號的 `站前秀泰門市` 已依現行官方名稱改為 `新時代台中門市`，地址和座標不變。[官方開幕公告](https://www.muji.tw/muji-journal/news/news/251223.html)
4. **特殊型態標示**：四間 DECO HOME 是宜得利官方子品牌，不是錯誤門市；IKEA 新竹是訂購取貨中心；hoi! 花蓮是店中店專櫃；無印良品新竹大魯閣標為期間限定門市。這些據點保留在地圖，但不再與一般完整門市混為同一型態。

## 數量來源與注意事項

- 宜得利現行門市定位器回傳 75 筆；宜得利企業頁則標示台灣 77 店（截至 2026-08-31）。兩個官方來源目前相差 2 間，因此儀表板採可逐店定位的 75 筆，不虛增無法從定位器核實的門市。[門市定位器](https://www.nitori-net.tw/store)、[企業店舖總數](https://nitori.dokku.nitori-net.tw/)
- IKEA 官方資料可區分 8 間門市與新竹訂購取貨中心。[IKEA 門市資訊](https://www.ikea.com.tw/zh/store/index)
- HOLA、特力屋與 hoi! 以各品牌即時官方門市 API 名冊核對；MR. LIVING 以官方據點頁核對。[HOLA 門市](https://cdn.hola.com.tw/store/locations)、[特力屋門市](https://www.trplus.com.tw/store/locations)、[hoi! 門市](https://www.hoihome.tw/store/locations)、[MR. LIVING 據點](https://www.mrliving.com.tw/about-mrliving-contact)

Google Maps 商家狀態可能晚於品牌公告更新，因此判定順序為：品牌官方名冊確認是否為門市，Google Maps 確認 POI 名稱、地址與落點，最後才以第三方資訊補充。若官方與 Google 不一致，資料會保留並標記待複核，不會直接算成正式門市。

## 檢核結果

- 七大品牌營運中據點：270
- 缺少座標：0
- 座標超出台灣合理範圍：0
- 已排除跨品牌誤列：1（La-Z-Boy 微風南京店）
- 暫停營業：2（特力屋士林、HOLA 士林）

### Sources

- [MUJI 無印良品麗寶MALL門市官方公告](https://www.muji.tw/muji-journal/news/news/260717.html)
- [MUJI 無印良品愛買台中門市官方公告](https://shop.muji.tw/muji-journal/news/news/250815.html)
- [宜得利官方門市定位器](https://www.nitori-net.tw/store)
- [IKEA 台灣門市資訊](https://www.ikea.com.tw/zh/store/index)
- [MR. LIVING 官方門市資訊](https://www.mrliving.com.tw/about-mrliving-contact)
