# 台灣實體門市 GIS 地理圖資儀表板
### Taiwan Home & Retail Stores GIS Intelligence Dashboard

[![Deploy: Netlify](https://img.shields.io/badge/Deploy-Netlify-00C7B7?logo=netlify&logoColor=white)](https://www.netlify.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一個現代化、全功能的一站式台灣實體零售與居家生活門市地理資訊系統（GIS）與商圈競爭情報儀表板。整合 Leaflet 地圖、歷年展店時序軌跡、服務半徑商圈分析，以及多模式路徑導航估算。

---

## 核心功能特色

### 1. 互動式空間地圖與商圈聚類
* **全台品牌門市視覺化**：收錄 IKEA、無印良品、宜得利、特力屋、HOLA、hoi! 好好生活、MR. LIVING、Costco 好市多、萬家福/家樂福、大全聯、全聯福利中心，以及數千間蝦皮店到店門市。
* **高密度標記聚類（Marker Cluster）**：支援數千個節點的高流暢平移縮放，依視角自動分群。
* **共構商圈樞紐辨識**：自動計算並標記 150 公尺內存在同業競爭對手的高密度「商圈共構節點」。

### 2. 路徑規劃與抵達時間雙指標看板
* **雙指標重點看板**：
  * **預估耗時**：大字號呈現開車、大眾運輸、步行的通勤時間（分鐘／小時）。
  * **路徑里程**：精確標註道路實測行車里程（公里數）與直線地理距離。
* **三種交通模式專屬樣式**：
  * **開車**：高對比科技深藍雙層實線（`#2563EB`）。
  * **大眾運輸**：專屬捷運紫段落虛線（`#8B5CF6`）。
  * **步行**：翡翠綠行人步道點狀虛線（`#10B981`）。
* **多元出發起點設定**：
  * 支援瀏覽器 GPS 定位一鍵取得目前位置。
  * 內建全台主要交通樞紐選單（台北車站、板橋車站、新竹巨城、台中車站、台南車站、左營高鐵站）。
  * 地圖自由選點功能：點擊地圖任意位置即可自訂出發點。
* **Google Routes API 官方圖資**：全面整合 Google Maps Platform 最新世代 Routes API（computeRoutes），精準計算開車、大眾運輸與步行等多元模式之即時路況、道路里程與公車捷運轉乘。

### 3. 商圈半徑緩衝區分析（Catchment Buffer Zone）
* **服務半徑調節**：支援 1.0 ~ 30.0 km 自由拖曳半徑或使用預設值（1km 步行鄰近、3km 生活圈、5km 核心商圈、10km 跨區驅車、20km 全都會區）。
* **重疊競品分析**：即時計算半徑內競爭對手門市與同品牌分店，依距離排序。
* **獨立封閉商圈獨佔優勢辨識**：若周邊指定半徑無同業進駐，系統自動識別並提示客群獨佔排他紅利。

### 4. 歷史展店時序軌跡回放（1989 ~ 2026）
* **動態時間軸播放器**：支援播放、暫停與自由拖曳年份，動態觀看全台居家與量販版圖的演進與消長。
* **100% 地毯式歷史審核**：校正歷史展店時序資料，修復異常單一年份高峰，完整重現各品牌在台灣的拓點歷程。

---

## 專案目錄結構

```text
taiwan_home_stores_gis/
├── index.html                           # 產出檔：儀表板首頁（由建置腳本產生，請勿直接修改）
├── assets/                              # 產出檔：app.css、app.js（由 src/ 合併而成，請勿直接修改）
├── src/                                 # 前端原始碼（要改畫面請改這裡）
│   ├── index.html                       # 頁面結構樣板（PLACEHOLDER 由建置腳本替換）
│   ├── css/                             # 樣式，依檔名順序合併：基礎、地圖、清單、詳情、大頭針、時光軸、手機版
│   └── js/                              # 互動程式，依檔名順序合併：資料設定、地圖、狀態、篩選、定位、
│                                        #   清單渲染與手機版面、大頭針、清單、詳情與商圈、路線、互動事件、時光軸、啟動
├── favicon.svg / favicon.ico / favicon-32.png / apple-touch-icon.png  # 網站圖示（中性地圖定位針）
├── stores_data.js                       # 產出檔：居家／量販門市資料
├── vendor/                              # 內建 Leaflet 與 MarkerCluster（不依賴外部 CDN）
├── pxmart_stores_data.js                # 隨選動態載入之全聯福利中心門市資料集
├── shopee_stores_data.js                # 隨選動態載入之全台電商門市資料集
├── build_ikea_gis_dashboard.py          # 建置腳本：整理門市資料、合併 src/ 產出 index.html 與 assets/
├── netlify.toml                         # Netlify 雲端部署規則與 API 反向代理配置
├── netlify/
│   └── functions/
│       └── directions.js                # Serverless 路徑規劃代理（Google Routes API 專用）
├── data/                                # 核心乾淨門市資料庫
│   ├── taiwan_home_stores_status.json   # 5,191 間實體門市完整生命週期資料庫 (JSON)
│   └── taiwan_home_stores_status.csv    # 5,191 間實體門市歷史狀態對帳表 (CSV)
└── audit/                               # 歷史門市地毯式查核紀錄與同步腳本
    ├── HOME_BRAND_STORE_AUDIT.md        # 居家品牌查核總報告
    ├── PXMART_STORE_LOCATION_AUDIT.md   # 全聯門市 Google 地圖地理位置核對報告
    ├── STORE_AUDIT_REPORT.md            # 門市歷史軌跡核對紀錄
    ├── audit_store_data.py              # 門市資料檢驗腳本
    ├── finalize_store_audit.py          # 查核彙整產出腳本
    ├── sync_mass_retail_stores.py       # 量販門市同步腳本
    ├── sync_pxmart_stores.py            # 全聯福利中心門市同步腳本
    ├── sync_shopee_stores.py            # 蝦皮店到店同步腳本
    ├── mass_retail_location_audit.json  # 量販查核資料庫
    ├── pxmart_location_audit.json       # 全聯門市位置查核紀錄
    ├── shopee_location_audit.json       # 蝦皮位置查核紀錄
    ├── store_audit_queries.json         # 門市查詢對帳紀錄
    ├── store_count_audit.csv            # 各品牌店數對帳統計
    └── store_location_audit.csv         # 門市逐店校對結果明細
```

---

## 快速開始與本地執行

### 1. 直接開啟
無需安裝任何後端依賴，直接使用現代瀏覽器開啟專案中的 `index.html` 即可瀏覽完整 GIS 地圖圖資。

### 2. 本地 HTTP 伺服器（推薦）
若要測試完整的定位與本機連線，可在專案目錄啟動簡易伺服器：
```bash
# Python 3
python3 -m http.server 8080
```
開啟瀏覽器訪問 `http://localhost:8080`。

### 3. 重新編譯儀表板
更新了 `data/taiwan_home_stores_status.json` 中的門市資料，或修改了 `src/` 底下的畫面、樣式、程式後，執行建置腳本重新產生靜態檔案：
```bash
python3 build_ikea_gis_dashboard.py
```

建置腳本會：
- 依檔名順序把 `src/css/*.css` 合併成 `assets/app.css`、`src/js/*.js` 合併成 `assets/app.js`（合併成單一檔案，執行順序與作用域和分檔前完全相同）。
- 以檔案內容雜湊當版本號寫進 `index.html`（`?v=...`），只有內容改變時瀏覽器才會重新下載；資料更新不會讓 CSS／JS 快取失效。

> `index.html`、`assets/`、`stores_data.js` 等都是產出檔，直接修改會在下次建置時被覆蓋，請改 `src/` 或 `data/`。

新增 JS 檔時以兩位數字開頭命名（例如 `src/js/14-new-feature.js`）決定合併順序；在 JS 檔最上層直接呼叫其他檔案定義的函式時，該檔需排在定義檔之後（函式內呼叫則不受影響）。

---

## Netlify 雲端部署與 API 設定

本專案已完全相容 Netlify 的零配置部署：

1. 登入 [Netlify](https://www.netlify.com/)，點選 **Add new site** → **Import an existing project**。
2. 連結您的 GitHub 儲存庫 `chienchitung/taiwan_home_stores_gis`。
3. 部署設定會自動讀取 `netlify.toml`，無需額外填寫建置指令。
4. **設定 Google Routes API Key**：
   * 前往 Netlify 控制台：**Site configuration** → **Environment variables**。
   * 新增變數：
     * **Key**：`GOOGLE_MAPS_API_KEY`
     * **Value**：您的 Google Cloud API 金鑰。
   * **Google Cloud Console 設定注意事項**：
     * 需啟用 **Routes API**（Google 新版專案由現代 Routes API 提供路徑計算）。
     * API 金鑰的「應用程式限制」請選 **無 (None)**（因由 Netlify 後端 Serverless Node.js 呼叫，不能設 HTTP 參照網址限制）。
     * API 金鑰的「API 限制」請勾選 **Routes API**（避免產生未授權費用）。
   * 設定後，雲端 Serverless 函數即由 Google Routes API 提供即時多模式路網與精準公車捷運轉乘班次計算。

---

## 資料來源與審核說明

專案所收錄之實體門市資料歷經嚴謹比對，核對來源包含：
1. **經濟部商業發展署商工登記資料（GCIS）**
2. **台灣連鎖暨加盟協會（TCFA）連鎖店年鑑**
3. **各大企業官方網站歷史門市公告、新聞稿與股東會年報**
4. **Google Maps Platform 官方地標審核**

詳細歷程與對帳資料請參閱 [`audit/HOME_BRAND_STORE_AUDIT.md`](audit/HOME_BRAND_STORE_AUDIT.md)。

---

## 授權條款

本專案採 [MIT License](LICENSE) 授權開放。
