/* ─── DATA INJECTION ─── */
const ALL_STORES = window.ALL_STORES_DATA || [];
let shopeeDataLoaded = false;
let shopeeLoadPromise = null;
let pxmartDataLoaded = false;
let pxmartLoadPromise = null;
let markerClusterLayer = null;

/* ─── BRAND CONFIG ─── */
const BRANDS = {
  "IKEA":              { color: "#0058A3", label: "IKEA 宜家家居",       tableLabel: "IKEA",    abbr: "IK" },
  "無印良品":           { color: "#7F0019", label: "無印良品 (MUJI)",     tableLabel: "無印良品", abbr: "無" },
  "宜得利":             { color: "#00A396", label: "宜得利家居 (NITORI)", tableLabel: "宜得利",   abbr: "宜" },
  "特力屋":             { color: "#EA580C", label: "特力屋 (TLW)",        tableLabel: "特力屋",   abbr: "特" },
  "HOLA":              { color: "#D97706", label: "HOLA 和樂家居",        tableLabel: "HOLA",    abbr: "HO" },
  "hoi! 好好生活":      { color: "#E11D48", label: "hoi! 好好生活",       tableLabel: "hoi!",    abbr: "hi" },
  "MR. LIVING 居家先生":{ color: "#1E293B", label: "MR. LIVING 居家先生", tableLabel: "MR.",     abbr: "MR" },
  "Costco 好市多":      { color: "#E31837", label: "Costco 好市多",       tableLabel: "Costco",  abbr: "CO" },
  "萬家福":             { color: "#0B6E4F", label: "萬家福量販",          tableLabel: "萬家福",   abbr: "萬" },
  "大全聯":             { color: "#E60012", label: "大全聯 MEGA PXMART", tableLabel: "大全聯",   abbr: "大" },
  "全聯福利中心":       { color: "#005BAC", label: "全聯福利中心",        tableLabel: "全聯",     abbr: "全" },
  "蝦皮店到店":         { color: "#EE4D2D", label: "蝦皮店到店",           tableLabel: "蝦皮",     abbr: "蝦" },
};
const BRAND_KEYS = Object.keys(BRANDS);
const DATASET_BRANDS = {
  home: ["IKEA", "無印良品", "宜得利", "特力屋", "HOLA", "hoi! 好好生活", "MR. LIVING 居家先生"],
  mass: ["Costco 好市多", "萬家福", "大全聯"],
  supermarket: ["全聯福利中心"],
  ecommerce: ["蝦皮店到店"]
};

/* ─── SVG ICONS REPOSITORY (Strictly Zero Emojis) ─── */
// 交通方式圖示取自 Google Material Icons（directions_car / directions_transit / directions_walk，Apache-2.0），與 Google 地圖一致
const SVG = {
  store: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m21.9 8.89-1.05-4.37c-.22-.9-1-1.52-1.91-1.52H5.05c-.9 0-1.69.63-1.9 1.52L2.1 8.89c-.24 1.02-.02 2.06.62 2.88.08.11.19.19.28.29V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-6.94c.09-.09.2-.18.28-.28.64-.82.87-1.87.62-2.89zm-2.99-3.9 1.05 4.37c.1.42.01.84-.25 1.17-.14.18-.44.47-.94.47-.61 0-1.14-.49-1.21-1.14L16.98 5l1.93-.01zM13 5h1.96l.54 4.52c.05.39-.07.78-.33 1.07-.22.26-.54.41-.95.41-.67 0-1.22-.59-1.22-1.31V5zM8.49 9.52 9.04 5H11v4.69c0 .72-.55 1.31-1.29 1.31-.34 0-.65-.15-.89-.41a1.42 1.42 0 0 1-.33-1.07zm-4.45-.16L5.05 5h1.97l-.58 4.86c-.08.65-.6 1.14-1.21 1.14-.49 0-.8-.29-.93-.47-.27-.32-.36-.75-.26-1.17zM5 19v-6.03c.08.01.15.03.23.03.87 0 1.66-.36 2.24-.95.6.6 1.4.95 2.31.95.87 0 1.65-.36 2.23-.93.59.57 1.39.93 2.29.93.84 0 1.64-.35 2.24-.95.58.59 1.37.95 2.24.95.08 0 .15-.02.23-.03V19H5z"/></svg>`,
  pin: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zM7 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 2.88-2.88 7.19-5 9.88C9.92 16.21 7 11.85 7 9z"/><circle cx="12" cy="9" r="2.5"/></svg>`,
  external: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>`,
  check: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>`,
  chevron: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6-1.41-1.41z"/></svg>`,
  pause: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 16h2V8H9v8zm3-14C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm1-4h2V8h-2v8z"/></svg>`,
  copy: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>`,
  crosshair: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17 12c0-2.76-2.24-5-5-5s-5 2.24-5 5 2.24 5 5 5 5-2.24 5-5zm-5 3c-1.65 0-3-1.35-3-3s1.35-3 3-3 3 1.35 3 3-1.35 3-3 3zm-7 0H3v4c0 1.1.9 2 2 2h4v-2H5v-4zM5 5h4V3H5c-1.1 0-2 .9-2 2v4h2V5zm14-2h-4v2h4v4h2V5c0-1.1-.9-2-2-2zm0 16h-4v2h4c1.1 0 2-.9 2-2v-4h-2v4z"/></svg>`,
  archive: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m20.54 5.23-1.39-1.68C18.88 3.21 18.47 3 18 3H6c-.47 0-.88.21-1.16.55L3.46 5.23C3.17 5.57 3 6.02 3 6.5V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6.5c0-.48-.17-.93-.46-1.27zM6.24 5h11.52l.81.97H5.44l.8-.97zM5 19V8h14v11H5zm8.45-9h-2.9v3H8l4 4 4-4h-2.55z"/></svg>`,
  gps: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3A8.994 8.994 0 0 0 13 3.06V1h-2v2.06A8.994 8.994 0 0 0 3.06 11H1v2h2.06A8.994 8.994 0 0 0 11 20.94V23h2v-2.06A8.994 8.994 0 0 0 20.94 13H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>`,
  clock: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>`,
  pick: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.71 17.99A5.993 5.993 0 0 1 6 12c0-3.31 2.69-6 6-6 3.22 0 5.84 2.53 5.99 5.71l-2.1-.63a3.999 3.999 0 1 0-4.81 4.81l.63 2.1zM22 12c0 .3-.01.6-.04.9l-1.97-.59c.01-.1.01-.21.01-.31 0-4.42-3.58-8-8-8s-8 3.58-8 8 3.58 8 8 8c.1 0 .21 0 .31-.01l.59 1.97c-.3.03-.6.04-.9.04-5.52 0-10-4.48-10-10S6.48 2 12 2s10 4.48 10 10zm-3.77 4.26L22 15l-10-3 3 10 1.26-3.77 4.27 4.27 1.98-1.98-4.28-4.26z"/></svg>`,
  info: `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>`,
  route: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m22.43 10.59-9.01-9.01c-.75-.75-2.07-.76-2.83 0l-9 9c-.78.78-.78 2.04 0 2.82l9 9c.39.39.9.58 1.41.58.51 0 1.02-.19 1.41-.58l8.99-8.99c.79-.76.8-2.02.03-2.82zm-10.42 10.4-9-9 9-9 9 9-9 9zM8 11v4h2v-3h4v2.5l3.5-3.5L14 7.5V10H9c-.55 0-1 .45-1 1z"/></svg>`,
  car: `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>`,
  transit: `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2c-4.42 0-8 .5-8 4v9.5C4 17.43 5.57 19 7.5 19L6 20.5v.5h12v-.5L16.5 19c1.93 0 3.5-1.57 3.5-3.5V6c0-3.5-3.58-4-8-4zM7.5 17c-.83 0-1.5-.67-1.5-1.5S6.67 14 7.5 14s1.5.67 1.5 1.5S8.33 17 7.5 17zm3.5-6H6V6h5v5zm5.5 6c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm1.5-6h-5V6h5v5z"/></svg>`,
  walk: `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9 7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7"/></svg>`
};

/* ─── HAVERSINE DISTANCE ENGINE ─── */
function haversineDistanceKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function formatDist(km) {
  if (km === undefined || km === null || isNaN(km)) return "";
  return km < 1 ? `${Math.round(km * 1000)} m` : `${km.toFixed(1)} km`;
}

/* ─── PRECOMPUTE CO-LOCATION HUBS (<= 150m) ─── */
ALL_STORES.forEach(s => {
  if (typeof s._isCoLocation === "boolean") return; // 建置時已預先計算
  s._isCoLocation = ALL_STORES.some(o => 
    o.n !== s.n && 
    o.brand !== s.brand && 
    haversineDistanceKm(s.lat, s.lng, o.lat, o.lng) <= 0.15
  );
});

function loadScriptOnce(src, globalCheck) {
  if (globalCheck()) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`無法載入 ${src}`));
    document.head.appendChild(script);
  });
}

function loadStyleOnce(href) {
  if (document.querySelector(`link[href="${href}"]`)) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = href;
  document.head.appendChild(link);
}

function ensureShopeeData() {
  if (shopeeDataLoaded) return Promise.resolve();
  if (shopeeLoadPromise) return shopeeLoadPromise;
  loadStyleOnce("vendor/leaflet.markercluster/MarkerCluster.css");
  loadStyleOnce("vendor/leaflet.markercluster/MarkerCluster.Default.css");
  shopeeLoadPromise = Promise.all([
    loadScriptOnce("shopee_stores_data.js", () => Array.isArray(window.SHOPEE_STORES)),
    loadScriptOnce("vendor/leaflet.markercluster/leaflet.markercluster.js", () => typeof L.markerClusterGroup === "function").catch(() => {})
  ]).then(() => {
    const incoming = window.SHOPEE_STORES || [];
    incoming.forEach(s => { s._isCoLocation = false; });
    ALL_STORES.push(...incoming);
    shopeeDataLoaded = true;
    initDropdowns();
    initBrandPills();
  }).finally(() => { shopeeLoadPromise = null; });
  return shopeeLoadPromise;
}

function ensurePxmartData() {
  if (pxmartDataLoaded) return Promise.resolve();
  if (pxmartLoadPromise) return pxmartLoadPromise;
  loadStyleOnce("vendor/leaflet.markercluster/MarkerCluster.css");
  loadStyleOnce("vendor/leaflet.markercluster/MarkerCluster.Default.css");
  pxmartLoadPromise = Promise.all([
    loadScriptOnce("pxmart_stores_data.js", () => Array.isArray(window.PXMART_STORES)),
    loadScriptOnce("vendor/leaflet.markercluster/leaflet.markercluster.js", () => typeof L.markerClusterGroup === "function").catch(() => {})
  ]).then(() => {
    const incoming = window.PXMART_STORES || [];
    incoming.forEach(s => { s._isCoLocation = false; });
    ALL_STORES.push(...incoming);
    pxmartDataLoaded = true;
    initDropdowns();
    initBrandPills();
  }).finally(() => { pxmartLoadPromise = null; });
  return pxmartLoadPromise;
}

/* ─── BASE MAP TILES CONFIG (Google Maps High-Res Tiles) ─── */
const TILE_LAYERS = {
  mono: L.tileLayer("https://mt{s}.google.com/vt/lyrs=m&hl=zh-TW&x={x}&y={y}&z={z}", {
    className: "tiles-google-mono",
    maxZoom: 20,
    subdomains: ['0', '1', '2', '3'],
    attribution: 'Map data &copy; Google Maps'
  }),
  satellite: L.tileLayer("https://mt{s}.google.com/vt/lyrs=y&hl=zh-TW&x={x}&y={y}&z={z}", {
    className: "tiles-google-satellite",
    maxZoom: 20,
    subdomains: ['0', '1', '2', '3'],
    attribution: 'Imagery &copy; Google Maps'
  }),
  color: L.tileLayer("https://mt{s}.google.com/vt/lyrs=m&hl=zh-TW&x={x}&y={y}&z={z}", {
    className: "tiles-google-color",
    maxZoom: 20,
    subdomains: ['0', '1', '2', '3'],
    attribution: 'Map data &copy; Google Maps'
  })
};

/* ─── SECTION 3: 6 METROPOLITAN REGION SPATIAL BOUNDARIES ─── */
const REGION_DATA = {
  taipei: {
    name: "大台北生活圈",
    cities: ["基隆市", "台北市", "新北市"],
    color: "#0058A3",
    coords: [
      [25.298, 121.538], [25.285, 121.585], [25.207, 121.691], [25.158, 121.765],
      [25.127, 121.921], [25.008, 122.000], [24.960, 121.950], [24.890, 121.780],
      [24.770, 121.520], [24.810, 121.430], [24.950, 121.340], [25.090, 121.330],
      [25.170, 121.410], [25.285, 121.515], [25.298, 121.538]
    ]
  },
  taoyuan_hsinchu: {
    name: "桃竹苗生活圈",
    cities: ["桃園市", "新竹市", "新竹縣", "苗栗縣"],
    color: "#7C3AED",
    coords: [
      [25.130, 121.240], [25.100, 121.400], [24.850, 121.400], [24.720, 121.430],
      [24.460, 121.260], [24.380, 121.230], [24.310, 120.840], [24.380, 120.760],
      [24.440, 120.630], [24.570, 120.700], [24.710, 120.850], [24.850, 120.920],
      [24.990, 121.010], [25.130, 121.240]
    ]
  },
  central: {
    name: "中台灣生活圈",
    cities: ["台中市", "彰化縣", "南投縣", "雲林縣"],
    color: "#C2410C",
    coords: [
      [24.400, 120.570], [24.330, 120.830], [24.280, 121.030], [24.140, 121.270],
      [23.950, 121.250], [23.750, 121.150], [23.470, 120.957], [23.530, 120.800],
      [23.580, 120.680], [23.550, 120.250], [23.680, 120.140], [23.950, 120.320],
      [24.120, 120.400], [24.310, 120.550], [24.400, 120.570]
    ]
  },
  south: {
    name: "南台灣生活圈",
    cities: ["嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"],
    color: "#15803D",
    coords: [
      [23.420, 120.120], [23.600, 120.570], [23.470, 120.950], [23.250, 120.920],
      [22.620, 120.760], [22.250, 120.750], [22.180, 120.880], [21.900, 120.850],
      [21.920, 120.735], [22.080, 120.700], [22.450, 120.450], [22.580, 120.270],
      [22.950, 120.170], [23.150, 120.060], [23.310, 120.110], [23.420, 120.120]
    ]
  },
  east_offshore: {
    name: "東部與離島生活圈",
    cities: ["宜蘭縣", "花蓮縣", "台東縣", "澎湖縣", "金門縣"],
    color: "#BE123C",
    multiCoords: [
      // Eastern Taiwan Corridor
      [
        [24.960, 121.920], [24.580, 121.870], [24.300, 121.750], [24.020, 121.630],
        [23.500, 121.510], [23.130, 121.410], [22.880, 121.230], [22.680, 121.150],
        [22.350, 120.920], [22.350, 120.750], [22.750, 121.000], [23.100, 121.100],
        [23.500, 121.250], [23.850, 121.400], [24.150, 121.250], [24.400, 121.350],
        [24.750, 121.500], [24.920, 121.750], [24.960, 121.920]
      ],
      // Penghu
      [
        [23.720, 119.520], [23.720, 119.680], [23.500, 119.680], [23.500, 119.520], [23.720, 119.520]
      ],
      // Kinmen
      [
        [24.540, 118.230], [24.540, 118.480], [24.400, 118.480], [24.400, 118.230], [24.540, 118.230]
      ]
    ]
  }
};

/* ─── MAP INITIALIZATION ─── */
const map = L.map("map", { zoomControl: false, attributionControl: false });
map.on("zoomend load", () => syncMarkerOverviewMode());
// 手機版初始就用 zoom 7（之後 fitBounds 只微調中心），避免先抓一批 zoom 8 圖磚又整批換掉
map.setView([23.75, 120.95], window.matchMedia("(max-width: 768px)").matches ? 7 : 8);

/* ─── GOOGLE MAPS NAVIGATION CONTROLS (My Location + Zoom In/Out) ─── */
const googleNavControl = L.control({ position: "bottomleft" });
googleNavControl.onAdd = function(map) {
  const container = L.DomUtil.create("div", "google-nav-control-group");
  container.innerHTML = `
    <button class="btn-google-locate" id="btnMapLocate" title="顯示我的位置 (回到所在座標)" role="button" aria-label="顯示我的位置">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3A8.994 8.994 0 0 0 13 3.06V1h-2v2.06A8.994 8.994 0 0 0 3.06 11H1v2h2.06A8.994 8.994 0 0 0 11 20.94V23h2v-2.06A8.994 8.994 0 0 0 20.94 13H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
    </button>
    <div class="google-zoom-box">
      <button class="btn-google-zoom" id="btnMapZoomIn" title="放大地圖" role="button" aria-label="放大地圖">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
      </button>
      <div class="google-zoom-divider"></div>
      <button class="btn-google-zoom" id="btnMapZoomOut" title="縮小地圖" role="button" aria-label="縮小地圖">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 13H5v-2h14v2z"/></svg>
      </button>
    </div>
  `;
  L.DomEvent.disableClickPropagation(container);
  L.DomEvent.disableScrollPropagation(container);
  return container;
};
googleNavControl.addTo(map);

const mapLocateBtn = document.getElementById("btnMapLocate");
if (mapLocateBtn) {
  mapLocateBtn.onclick = (e) => {
    e.stopPropagation();
    locateUser();
  };
}
const zoomInBtn = document.getElementById("btnMapZoomIn");
if (zoomInBtn) {
  zoomInBtn.onclick = (e) => {
    e.stopPropagation();
    map.zoomIn();
  };
}
const zoomOutBtn = document.getElementById("btnMapZoomOut");
if (zoomOutBtn) {
  zoomOutBtn.onclick = (e) => {
    e.stopPropagation();
    map.zoomOut();
  };
}

let currentTile = TILE_LAYERS.mono;
currentTile.addTo(map);

/* ─── APPLICATION STATE ─── */
let activeBrands = new Set(); // 已選品牌（可複選）；空集合 = 全部
let activeDatasetMode = "home";
let selectedKey = null;
let markers = {};
let filteredStores = [];
let viewMode = "cards";
let highContrastPins = false;
let isSidebarCollapsed = false;
let isViewportSync = false;
let currentDetailStore = null;

// Catchment Buffer Circle State (P1 Feature)
let currentRadiusKm = 3.0;
let bufferCircle = null;
let isBufferCircleEnabled = true;

// GPS Location State (P1 Feature: Google Maps-like re-centering with session cache)
let userLocation = null;
try {
  const cachedLat = sessionStorage.getItem("taiwan_user_lat");
  const cachedLng = sessionStorage.getItem("taiwan_user_lng");
  if (cachedLat && cachedLng) {
    userLocation = { lat: parseFloat(cachedLat), lng: parseFloat(cachedLng) };
  }
} catch (e) {}
let userLocationMarker = null;
let isSortedByDistance = false;

// Regional Boundary Spatial Layer State (Section 3 Feature)
let activeRegionLayer = null;
let currentActiveRegionKey = "all";

// Brand PK Mode State (Section 4)

/* ─── GOOGLE MAPS URL GENERATOR ─── */
function getGmapsSearchUrl(s) {
  const q = s.clean_query || `${s.brand} ${s.store_name} ${s.address}`;
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
}

function getStatusBadge(s) {
  if (s.status_category === "現行營運中") {
    return `<span class="status-pill status-active">${SVG.check} 現行營運</span>`;
  }
  if (s.status_category === "暫停營業") {
    return `<span class="status-pill status-paused">${SVG.pause} 暫停營業</span>`;
  }
  return `<span class="status-pill status-closed">${SVG.archive} 已歇業</span>`;
}

function makeMarkerIcon(s, isNewlyOpened = false) {
  const cfg = BRANDS[s.brand] || { color: "#0058A3", abbr: "?" };
  const contrastClass = highContrastPins ? " high-contrast-pin" : "";
  const pulseClass = isNewlyOpened ? " marker-new-pulse" : "";
  const svgHtml = `<svg width="28" height="36" viewBox="0 0 28 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M14 36 C11 27 1 20.5 1 13.5 A 13 13 0 1 1 27 13.5 C27 20.5 17 27 14 36 Z" fill="${cfg.color}" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <text x="14" y="14" text-anchor="middle" dominant-baseline="central" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="11px" letter-spacing="-0.3px">${cfg.abbr}</text>
  </svg>`;
  return L.divIcon({
    className: "brand-pin-marker" + contrastClass + pulseClass,
    html: svgHtml,
    iconSize: [28, 36],
    iconAnchor: [14, 36],
    popupAnchor: [0, -38]
  });
}

function makePopupHtml(s) {
  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const key = "s" + s.n;

  return `<div class="popup-box">
    <div class="popup-header-row">
      <span class="popup-brand-badge" style="background:${cfg.color}">${s.brand}</span>
      ${getStatusBadge(s)}
    </div>
    <div class="popup-title">${s.store_name}</div>
    <div class="popup-meta">
      <span>${s.city} ${s.district || ""}</span>
    </div>
    <div class="tag-container" style="margin-bottom:8px">
      <span class="tag-badge tag-channel">${SVG.store} ${s.store_format || s.channel_format}</span>
      ${s.opened_year ? `<span class="tag-badge tag-opened-year">${SVG.clock} ${s.opened_year} 開幕</span>` : `<span class="tag-badge tag-opened-unknown" title="查無可靠開幕日期來源，未標示年份">${SVG.clock} 開幕年份未知</span>`}
      ${s._userDist !== undefined && isSortedByDistance ? `<span class="card-dist-badge">${SVG.gps} 距您 ${formatDist(s._userDist)}</span>` : ""}
    </div>
    <div class="popup-addr">
      ${SVG.pin}
      <span>${s.address}</span>
    </div>
    ${(s.status_category !== '現行營運中' && s.note) ? `<div class="popup-note-box">${s.note}</div>` : ''}
    <button class="pop-btn pop-btn-detail" onclick="openStoreDrawerByKey('${key}')" title="查看 ${s.store_name} 詳細資訊">
      ${SVG.info} <span>詳細資訊</span>
    </button>
    <div class="popup-action-row">
      <button class="pop-btn pop-btn-emph" onclick="triggerRoutePlanningByKey('${key}')" title="規劃前往 ${s.store_name} 路線">
        ${SVG.route} <span>規劃路線</span>
      </button>
      <a class="pop-btn pop-btn-secondary" href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener" title="在 Google Maps 開啟完整導航">
        ${SVG.external} <span class="btn-text-full">在 Google Maps 開啟</span><span class="btn-text-compact">Google 地圖</span>
      </a>
    </div>
  </div>`;
}

/* ─── DROPDOWNS INITIALIZATION & TWO-WAY LINKAGE ─── */
// 下拉選單的選項與數字依「目前資料集＋已選品牌＋其他篩選條件」計算（排除自身那一欄，方便改選）
function getScopedStorePoolForDropdowns(exclude = "") {
  const allowedBrands = DATASET_BRANDS[activeDatasetMode] || [];
  const val = id => { const el = document.getElementById(id); return el ? el.value : ""; };
  const city = exclude === "city" ? "" : val("selCity");
  const dist = (exclude === "city" || exclude === "district") ? "" : val("selDistrict");
  const chan = exclude === "channel" ? "" : val("selChannel");
  const stat = exclude === "status" ? "" : val("selStatus");
  return ALL_STORES.filter(s => {
    if (!allowedBrands.includes(s.brand)) return false;
    if (activeBrands.size && !activeBrands.has(s.brand)) return false;
    if (city && s.city !== city) return false;
    if (dist && s.district !== dist) return false;
    if (chan && (s.store_format || s.channel_format) !== chan) return false;
    if (stat && s.status_category !== stat) return false;
    return true;
  });
}

// 固定選項的下拉（門市型態、營運狀態）：標上數字，該條件下沒有門市的選項停用（目前選取的除外）
function updateFixedOptionCounts(selId, keyFn, exclude) {
  const sel = document.getElementById(selId);
  if (!sel) return;
  const counts = {};
  getScopedStorePoolForDropdowns(exclude).forEach(s => {
    const k = keyFn(s);
    if (k) counts[k] = (counts[k] || 0) + 1;
  });
  Array.from(sel.options).forEach(opt => {
    if (!opt.dataset.label) opt.dataset.label = opt.textContent;
    if (!opt.value) return;
    const n = counts[opt.value] || 0;
    opt.textContent = `${opt.dataset.label} (${n})`;
    opt.disabled = n === 0 && sel.value !== opt.value;
  });
}

function initDropdowns() {
  const citySel = document.getElementById("selCity");
  const selectedCity = citySel.value;
  citySel.innerHTML = '<option value="">全部縣市</option>';
  const pool = getScopedStorePoolForDropdowns("city");
  const counts = {};
  pool.forEach(s => {
    if (s.city) counts[s.city] = (counts[s.city] || 0) + 1;
  });
  Object.keys(counts).sort((a, b) => counts[b] - counts[a]).forEach(c => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = `${c} (${counts[c]})`;
    citySel.appendChild(opt);
  });
  if (selectedCity && counts[selectedCity]) {
    citySel.value = selectedCity;
  } else {
    citySel.value = "";
  }
  updateDistrictDropdown(citySel.value);
  updateFixedOptionCounts("selChannel", s => s.store_format || s.channel_format, "channel");
  updateFixedOptionCounts("selStatus", s => s.status_category, "status");
}

function updateDistrictDropdown(selectedCity) {
  const distSel = document.getElementById("selDistrict");
  distSel.disabled = false;
  distSel.title = "";
  const previousVal = distSel.value;

  if (selectedCity) {
    distSel.innerHTML = '<option value="">全部行政區</option>';
    const pool = getScopedStorePoolForDropdowns("district").filter(s => s.city === selectedCity);
    const counts = {};
    pool.forEach(s => {
      if (s.district) counts[s.district] = (counts[s.district] || 0) + 1;
    });
    Object.keys(counts).sort((a, b) => counts[b] - counts[a]).forEach(d => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = `${d} (${counts[d]})`;
      distSel.appendChild(opt);
    });
    if (previousVal && counts[previousVal]) {
      distSel.value = previousVal;
    } else {
      distSel.value = "";
    }
  } else {
    distSel.innerHTML = '<option value="">全部行政區</option>';
    distSel.value = "";
    distSel.disabled = true;
    distSel.title = "請先選擇縣市";
  }
}

/* ─── QUICK BRAND CHIPS INITIALIZATION ─── */
function initBrandPills() {
  const container = document.getElementById("brandPills");
  container.innerHTML = "";

  const allChip = document.createElement("button");
  allChip.className = "brand-chip" + (activeBrands.size === 0 ? " active" : "");
  allChip.dataset.brand = "";
  allChip.innerHTML = `<span class="dot" style="background:#0058A3"></span> 全部 <span class="cnt">${ALL_STORES.length}</span>`;
  allChip.onclick = () => {
    activeBrands.clear();
    render();
  };
  container.appendChild(allChip);

  BRAND_KEYS.forEach(b => {
    const cfg = BRANDS[b];
    const count = ALL_STORES.filter(s => s.brand === b).length;
    const chip = document.createElement("button");
    chip.className = "brand-chip";
    chip.dataset.brand = b;
    chip.innerHTML = `<span class="dot" style="background:${cfg.color}"></span> ${b} <span class="cnt">${count}</span>`;
    chip.onclick = async () => {
      if (b === "全聯福利中心" && !pxmartDataLoaded) {
        await ensurePxmartData();
      }
      // 複選：點一下選取、再點一下取消；點了哪個品牌就顯示哪個（不自動改回「全部」，
      // 否則只有一、兩個品牌的分類會看起來點了沒反應）
      if (activeBrands.has(b)) activeBrands.delete(b); else activeBrands.add(b);
      render();
    };
    container.appendChild(chip);
  });
}

function syncDatasetControls() {
  document.querySelectorAll(".dataset-switch-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.dataset === activeDatasetMode);
  });
  const allowed = DATASET_BRANDS[activeDatasetMode] || [];
  document.querySelectorAll('.brand-chip[data-brand]:not([data-brand=""])').forEach(chip => {
    chip.style.display = allowed.includes(chip.dataset.brand) ? "inline-flex" : "none";
  });
}

/* ─── DYNAMIC FACETED BRAND PILLS COUNT SYNCHRONIZATION ─── */
function updateBrandPillsCounts(nonBrandPool) {
  const allChip = document.querySelector('.brand-chip[data-brand=""]');
  if (allChip) {
    const cntEl = allChip.querySelector(".cnt");
    if (cntEl) cntEl.textContent = nonBrandPool.length;
  }

  const brandCounts = {};
  BRAND_KEYS.forEach(b => { brandCounts[b] = 0; });
  nonBrandPool.forEach(s => {
    if (brandCounts[s.brand] !== undefined) {
      brandCounts[s.brand]++;
    }
  });

  BRAND_KEYS.forEach(b => {
    const chip = document.querySelector(`.brand-chip[data-brand="${b}"]`);
    if (chip) {
      const cntEl = chip.querySelector(".cnt");
      const c = brandCounts[b] || 0;
      if (cntEl) cntEl.textContent = c;
      chip.classList.toggle("zero-count", c === 0);
    }
  });
}

function syncBrandPills() {
  document.querySelectorAll(".brand-chip").forEach(chip => {
    const b = chip.dataset.brand;
    const on = b === "" ? activeBrands.size === 0 : activeBrands.has(b);
    chip.classList.toggle("active", on);
    chip.setAttribute("aria-pressed", String(on));
  });
}

/* ─── BRAND PK MODE (Section 4) ─── */

/* ─── REGION QUICK JUMP BAR & SPATIAL BOUNDARY ENVELOPE (Section 3) ─── */
function updateActiveRegionTooltip() {
  if (!activeRegionLayer || !currentActiveRegionKey || currentActiveRegionKey === "all") return;
  const reg = REGION_DATA[currentActiveRegionKey];
  if (!reg) return;

  const regStores = filteredStores.filter(s => reg.cities.includes(s.city));
  const selectedStatus = document.getElementById("selStatus").value;
  const statusLabel = selectedStatus || "全部狀態";
  const totalStoresInRegion = ALL_STORES.filter(s =>
    reg.cities.includes(s.city) && (!selectedStatus || s.status_category === selectedStatus)
  ).length;
  const isFiltered = regStores.length !== totalStoresInRegion;

  let countPillHtml = "";
  if (regStores.length === 0) {
    countPillHtml = `<span class="pill-cnt pill-cnt-zero">目前篩選：0 間</span><span class="pill-filter-tag">/ 涵蓋縣市・${statusLabel}：${totalStoresInRegion} 間</span>`;
  } else if (isFiltered) {
    countPillHtml = `<span class="pill-cnt pill-cnt-filtered">目前篩選：${regStores.length} 間</span><span class="pill-filter-tag">/ 涵蓋縣市・${statusLabel}：${totalStoresInRegion} 間</span>`;
  } else {
    countPillHtml = `<span class="pill-cnt">涵蓋縣市・${statusLabel}：${totalStoresInRegion} 間</span>`;
  }

  activeRegionLayer.setTooltipContent(`
    <div class="region-pill-box">
      <span class="pill-dot" style="background:${reg.color}"></span>
      <strong>${reg.name}</strong>
      ${countPillHtml}
    </div>
  `);
}

function jumpToRegion(regKey) {
  // Clear any previously displayed regional boundary polygon
  if (activeRegionLayer) {
    map.removeLayer(activeRegionLayer);
    activeRegionLayer = null;
  }
  currentActiveRegionKey = regKey;
  updateLocateButtonsState(userLocation ? "active" : "reset");

  // Update active class on button
  document.querySelectorAll(".btn-region-jump").forEach(b => {
    b.classList.toggle("active", b.dataset.region === regKey);
  });

  if (regKey === "all") {
    map.flyTo([23.85, 120.95], 8, { duration: 0.8 });
    return;
  }

  const reg = REGION_DATA[regKey];
  if (!reg) return;

  // Create regional boundary polygon (Single or MultiPolygon)
  let poly;
  if (reg.multiCoords) {
    poly = L.polygon(reg.multiCoords, {
      color: reg.color,
      weight: 3,
      opacity: 1,
      dashArray: "8, 6",
      fillColor: reg.color,
      fillOpacity: 0.18,
      className: "region-boundary-poly"
    });
  } else {
    poly = L.polygon(reg.coords, {
      color: reg.color,
      weight: 3,
      opacity: 1,
      dashArray: "8, 6",
      fillColor: reg.color,
      fillOpacity: 0.18,
      className: "region-boundary-poly"
    });
  }

  poly.bindTooltip("", {
    permanent: true,
    direction: "center",
    className: "custom-region-tooltip"
  });

  poly.addTo(map);
  activeRegionLayer = poly;

  // Dynamically calculate and render tooltip content based on current active filters
  updateActiveRegionTooltip();

  // Smoothly fit map to the region's spatial bounds with comfortable padding
  map.fitBounds(poly.getBounds(), { padding: [50, 50], maxZoom: 12, duration: 0.8 });
}

function initRegionJumpBar() {
  document.querySelectorAll(".btn-region-jump").forEach(btn => {
    btn.onclick = () => {
      const regKey = btn.dataset.region;
      // If clicking already-active region, toggle back to "all" (toggle off)
      if (btn.classList.contains("active") && regKey !== "all") {
        jumpToRegion("all");
      } else {
        jumpToRegion(regKey);
      }
    };
  });
}

/* ─── GPS GEOLOCATION ENGINE (P1 Feature: Google Maps-like Location Re-centering) ─── */
function updateLocateButtonsState(state) {
  const sidebarBtn = document.getElementById("btnLocateMe");
  const mapBtn = document.getElementById("btnMapLocate");

  if (state === "loading") {
    if (sidebarBtn) {
      sidebarBtn.classList.add("loading");
      sidebarBtn.querySelector("span").textContent = "定位中…";
    }
    if (mapBtn) {
      mapBtn.classList.add("loading");
      mapBtn.title = "定位中…";
    }
  } else if (state === "active") {
    if (sidebarBtn) {
      sidebarBtn.classList.remove("loading");
      sidebarBtn.classList.add("active");
      sidebarBtn.querySelector("span").textContent = "我的位置";
      sidebarBtn.title = "點擊立即回到我的目前所在位置（已定位）";
    }
    if (mapBtn) {
      mapBtn.classList.remove("loading");
      mapBtn.classList.add("active");
      mapBtn.title = "已定位（點擊立即回歸我的目前位置）";
    }
  } else if (state === "reset") {
    if (sidebarBtn) {
      sidebarBtn.classList.remove("loading");
      sidebarBtn.classList.remove("active");
      sidebarBtn.querySelector("span").textContent = "離我最近";
      sidebarBtn.title = "以目前位置排序全台門市";
    }
    if (mapBtn) {
      mapBtn.classList.remove("loading");
      mapBtn.classList.remove("active");
      mapBtn.title = "顯示我的位置 (回到所在座標)";
    }
  }
}

function locateUser() {
  // If user location is ALREADY known (in memory or session cache):
  // Immediately re-center to user position like Google Maps without ANY browser permission prompts!
  if (userLocation) {
    if (!userLocationMarker) {
      const userIcon = L.divIcon({
        className: "user-gps-pulse-marker",
        html: `<div class="pulse-ring"></div><div class="user-dot"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      userLocationMarker = L.marker([userLocation.lat, userLocation.lng], { icon: userIcon, zIndexOffset: 4000 })
        .addTo(map)
        .bindPopup(`<div style="font-weight:700;padding:4px">您的目前所在位置</div>`);
      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(userLocation.lat, userLocation.lng, s.lat, s.lng);
      });
    }

    map.flyTo([userLocation.lat, userLocation.lng], 14, { duration: 0.8 });
    setTimeout(() => {
      if (userLocationMarker) userLocationMarker.openPopup();
    }, 850);
    updateLocateButtonsState("active");
    if (!isSortedByDistance) {
      isSortedByDistance = true;
      render();
    }
    return;
  }

  // First-time location acquisition
  if (!navigator.geolocation) {
    alert("您的瀏覽器環境不支援地理定位功能");
    return;
  }

  updateLocateButtonsState("loading");

  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude, longitude } = pos.coords;
      userLocation = { lat: latitude, lng: longitude };

      // Cache to sessionStorage to completely avoid permission prompts across reloads
      try {
        sessionStorage.setItem("taiwan_user_lat", String(latitude));
        sessionStorage.setItem("taiwan_user_lng", String(longitude));
      } catch (e) {}

      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(latitude, longitude, s.lat, s.lng);
      });

      if (userLocationMarker) map.removeLayer(userLocationMarker);
      const userIcon = L.divIcon({
        className: "user-gps-pulse-marker",
        html: `<div class="pulse-ring"></div><div class="user-dot"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      userLocationMarker = L.marker([latitude, longitude], { icon: userIcon, zIndexOffset: 4000 })
        .addTo(map)
        .bindPopup(`<div style="font-weight:700;padding:4px">您的目前所在位置</div>`);

      map.flyTo([latitude, longitude], 14, { duration: 0.8 });
      setTimeout(() => {
        if (userLocationMarker) userLocationMarker.openPopup();
      }, 850);

      updateLocateButtonsState("active");
      isSortedByDistance = true;
      render();
    },
    err => {
      updateLocateButtonsState("reset");
      alert("無法取得您的目前位置資訊（請確認已允許瀏覽器定位權限）");
    },
    { timeout: 10000, enableHighAccuracy: true }
  );
}

document.getElementById("btnLocateMe").onclick = locateUser;

// 路線規劃用：只取得定位（不移動地圖、不重排清單），取得後重新計算路線
function getUserLocation() {
  if (!navigator.geolocation) {
    alert("您的瀏覽器環境不支援地理定位功能");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude, longitude } = pos.coords;
      userLocation = { lat: latitude, lng: longitude };
      try {
        sessionStorage.setItem("taiwan_user_lat", String(latitude));
        sessionStorage.setItem("taiwan_user_lng", String(longitude));
      } catch (e) {}
      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(latitude, longitude, s.lat, s.lng);
      });
      if (currentDetailStore && currentDetailTab === "route" && runRouteFetch) runRouteFetch();
    },
    () => alert("無法取得您的目前位置資訊（請確認已允許瀏覽器定位權限）"),
    { timeout: 10000, enableHighAccuracy: true }
  );
}

/* ─── NON-BRAND FILTER POOL ENGINE (For Dynamic Faceted Counts) ─── */
function getNonBrandFilteredPool() {
  const q = document.getElementById("q").value.trim().toLowerCase();
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const chan = document.getElementById("selChannel").value;
  const stat = document.getElementById("selStatus").value;

  let pool = ALL_STORES.filter(s => {
    if (!(DATASET_BRANDS[activeDatasetMode] || []).includes(s.brand)) return false;
    if (city && s.city !== city) return false;
    if (dist && s.district !== dist) return false;

    if (chan && (s.store_format || s.channel_format) !== chan) {
      return false;
    }

    if (stat && s.status_category !== stat) return false;

    if (q) {
      const haystack = `${s.brand} ${s.store_name} ${s.city} ${s.district || ""} ${s.address} ${s.channel_format} ${s.store_type} ${s.note || ""}`.toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });

  if (isViewportSync && map) {
    const bounds = map.getBounds();
    pool = pool.filter(s => bounds.contains(L.latLng(+s.lat, +s.lng)));
  }

  return pool;
}

/* ─── CORE FILTER & RENDER ─── */
/* ═══════════ MOBILE LAYOUT（≤768px）═══════════
   地圖在上、底部抽屜在下。不複製任何控制項：把現有元素搬進手機容器，
   回到桌機寬度時再搬回原位，所以所有事件與狀態都沿用原本的程式。 */
const MOBILE_MQ = window.matchMedia("(max-width: 768px)");
const MOBILE_MOVES = [
  [".ikea-logo-box", "mLogoSlot"],
  [".search-input-group", "mSearchSlot"],
  ["#btnToggleTimeline", "mMenuPopover"],
  ["#btnExport", "mMenuPopover"],
  [".brand-strip", "mBrandSlot"],
  ["#btnLocateMe", "mRowActions"],
  ["#btnFilterToggle", "mRowActions"],
  [".dataset-switch", "mDatasetSlot"],
  ["#filterPanel", "mFilterSlot"],
  [".results-count-text .viewport-sync-label", "mViewportSlot"],
  ["#regionJumpBar", "mRegionSlot"]
];
const mobileHomes = new Map();   // element -> placeholder comment at its desktop position
let sheetState = "hidden";        // hidden（收成右下角按鈕）| peek | half | full | route
let mobileFlyInProgress = false;
let sheetBeforeRoute = "half";

function isMobileLayout() { return MOBILE_MQ.matches; }

function applyMobileLayout() {
  const mobile = isMobileLayout();
  document.body.classList.toggle("m-layout", mobile);
  MOBILE_MOVES.forEach(([sel, slotId]) => {
    if (mobile) {
      const el = document.querySelector(sel);
      if (!el || mobileHomes.has(el)) return;
      const ph = document.createComment("m-home");
      el.parentNode.insertBefore(ph, el);
      mobileHomes.set(el, ph);
      document.getElementById(slotId).appendChild(el);
    }
  });
  if (!mobile) {
    mobileHomes.forEach((ph, el) => { ph.parentNode.insertBefore(el, ph); ph.remove(); });
    mobileHomes.clear();
    closeMobileFilter();
    document.getElementById("mainSidebar").style.height = "";
    document.body.style.removeProperty("--m-sheet-h");
  } else {
    if (viewMode === "table") document.getElementById("vtCards").click(); // 手機一律卡片
    setSheet(sheetState);
  }
  setTimeout(() => map && map.invalidateSize(), 50);
}

function sheetHeightFor(state) {
  const h = window.innerHeight;
  if (state === "hidden") return 0;
  if (state === "peek") return 132;
  if (state === "preview") return Math.min(330, Math.round(window.innerHeight * 0.4));
  if (state === "route") return Math.min(430, Math.round(h * 0.52));
  if (state === "full") return Math.round(h * 0.9);
  return Math.round(h * 0.5);
}

function setSheet(state) {
  sheetState = state;
  if (!isMobileLayout()) return;
  const px = sheetHeightFor(state);
  const aside = document.getElementById("mainSidebar");
  aside.classList.toggle("m-sheet-hidden", state === "hidden");
  if (state !== "hidden") aside.style.height = px + "px";
  document.getElementById("mFabGroup").hidden = state !== "hidden";
  document.body.style.setProperty("--m-sheet-h", px + "px");
  document.getElementById("btnSheetHandle").setAttribute("aria-label",
    state === "full" ? "收合清單" : "展開清單");
}

// 讓 (lat, lng) 落在「搜尋列下方、抽屜上方」可見區域中央時，地圖中心應該在哪
function visibleCenterFor(lat, lng, zoom, state) {
  const h = map.getSize().y;
  const offsetY = (sheetHeightFor(state) - 112) / 2;
  return map.unproject(map.project([lat, lng], zoom).add([0, Math.max(0, offsetY)]), zoom);
}

// 把地圖上的點移到「抽屜上方可見區域」的中央
function panToVisible(lat, lng) {
  if (!isMobileLayout() || !map || mobileFlyInProgress) return;
  const rect = map.getContainer().getBoundingClientRect();
  const sheetH = sheetHeightFor(sheetState);
  const topUsed = 112; // 搜尋列＋品牌列
  const visibleCenterY = (topUsed + (rect.height - sheetH)) / 2;
  const pt = map.latLngToContainerPoint([lat, lng]);
  map.panBy([pt.x - rect.width / 2, pt.y - visibleCenterY], { animate: true });
}

function openMobileFilter() {
  const page = document.getElementById("mFilterPage");
  page.hidden = false;
  document.getElementById("btnFilterToggle").setAttribute("aria-expanded", "true");
  document.getElementById("btnMobileFilterClose").focus();
}
function closeMobileFilter() {
  const page = document.getElementById("mFilterPage");
  if (page.hidden) return;
  page.hidden = true;
  document.getElementById("btnFilterToggle").setAttribute("aria-expanded", "false");
}

// 已套用條件：在抽屜顯示可移除的標籤
function renderAppliedChips() {
  const box = document.getElementById("mAppliedChips");
  if (!box) return;
  const items = [];
  [["selCity", ""], ["selDistrict", ""], ["selChannel", ""], ["selStatus", "現行營運中"]].forEach(([id, def]) => {
    const sel = document.getElementById(id);
    if (sel.value !== def) {
      const label = sel.options[sel.selectedIndex] ? sel.options[sel.selectedIndex].textContent.replace(/\s*\(\d+\)$/, "") : sel.value;
      items.push(`<button class="m-chip" data-sel="${id}" data-def="${def}" aria-label="移除條件：${label}">${label}<span aria-hidden="true">×</span></button>`);
    }
  });
  box.innerHTML = items.join("");
  box.hidden = items.length === 0;
}
document.getElementById("mAppliedChips").addEventListener("click", e => {
  const chip = e.target.closest(".m-chip");
  if (!chip) return;
  const sel = document.getElementById(chip.dataset.sel);
  sel.value = chip.dataset.def;
  sel.dispatchEvent(new Event("change"));
});

// 防止 iOS Safari 縮放整個網頁。iOS 10 起 Safari 會忽略 viewport 的 maximum-scale，
// 在搜尋列、品牌列、清單上捏合或點兩下就會放大整頁；放大後畫面幾乎都是地圖，
// 雙指手勢全被地圖接走，就縮不回來。地圖本身的雙指縮放走 pointer/touch 事件，不受影響。
(function preventPageZoom() {
  ["gesturestart", "gesturechange", "gestureend"].forEach(type =>
    document.addEventListener(type, e => e.preventDefault(), { passive: false }));
  document.addEventListener("touchmove", e => {
    if (e.touches.length > 1 && !(e.target.closest && e.target.closest("#map"))) e.preventDefault();
  }, { passive: false });
})();

// 記錄時光軸面板高度，讓手機版地圖按鈕停在面板上方
(function trackTimelinePanelHeight() {
  const panel = document.getElementById("timelinePlayerPanel");
  if (!panel || !("ResizeObserver" in window)) return;
  new ResizeObserver(() => {
    // 用面板高度＋底部間距計算（不用目前位置：面板打開時有滑入動畫）
    const h = panel.offsetHeight;
    const bottomGap = parseFloat(getComputedStyle(panel).bottom) || 12;
    if (h) document.body.style.setProperty("--m-timeline-h", Math.round(h + bottomGap + 8) + "px");
  }).observe(panel);
})();

(function initMobileControls() {
  const handle = document.getElementById("btnSheetHandle");
  const order = ["hidden", "peek", "half", "full"];
  const step = dir => {
    if (sheetState === "preview") { setSheet(dir > 0 ? "half" : "peek"); return; }
    const cur = sheetState === "route" ? 2 : order.indexOf(sheetState);
    setSheet(order[Math.max(0, Math.min(order.length - 1, cur + dir))]);
  };
  handle.onclick = () => { if (sheetState === "full") setSheet("half"); else step(1); };
  document.getElementById("btnSheetFab").onclick = () => setSheet("half");
  document.getElementById("btnFabFilter").onclick = openMobileFilter;
  document.getElementById("btnSheetCollapse").onclick = () => setSheet("hidden");
  let startY = null;
  handle.addEventListener("touchstart", e => { startY = e.touches[0].clientY; }, { passive: true });
  handle.addEventListener("touchend", e => {
    if (startY === null) return;
    const dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dy) > 30) { step(dy < 0 ? 1 : -1); e.preventDefault(); }
    startY = null;
  });

  const menuBtn = document.getElementById("btnMobileMenu");
  const menu = document.getElementById("mMenuPopover");
  menuBtn.onclick = (e) => {
    e.stopPropagation();
    menu.hidden = !menu.hidden;
    menuBtn.setAttribute("aria-expanded", String(!menu.hidden));
  };
  document.addEventListener("click", e => {
    if (!menu.hidden && !menu.contains(e.target) && e.target !== menuBtn) {
      menu.hidden = true;
      menuBtn.setAttribute("aria-expanded", "false");
    }
  });
  menu.addEventListener("click", () => { menu.hidden = true; menuBtn.setAttribute("aria-expanded", "false"); });

  document.getElementById("btnMobileFilterClose").onclick = closeMobileFilter;
  document.getElementById("btnMobileFilterApply").onclick = () => { closeMobileFilter(); if (sheetState === "hidden" || sheetState === "peek") setSheet("half"); };
  document.getElementById("btnMobileFilterReset").onclick = () => document.getElementById("btnResetAll").click();
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeMobileFilter(); });

  MOBILE_MQ.addEventListener("change", applyMobileLayout);
  // 手機初始畫面：讓全台落在「搜尋列下方、抽屜上方」的可見區域
  if (isMobileLayout()) {
    setTimeout(() => {
      map.invalidateSize();
      map.fitBounds([[21.85, 119.95], [25.35, 122.05]], {
        paddingTopLeft: [12, 110], paddingBottomRight: [12, sheetHeightFor(sheetState) + 12], animate: false
      });
    }, 0);
  }
  window.addEventListener("resize", () => { if (isMobileLayout()) setSheet(sheetState); });
  applyMobileLayout();
})();

// 篩選面板：顯示已套用的條件數（營運狀態預設為「現行營運中」，不算在內）
function updateFilterCount() {
  const n = ["selCity", "selDistrict", "selChannel"].filter(id => document.getElementById(id).value).length
    + (document.getElementById("selStatus").value !== "現行營運中" ? 1 : 0);
  const badge = document.getElementById("lblFilterCount");
  badge.textContent = n;
  badge.hidden = n === 0;
  const fabBadge = document.getElementById("lblFabFilterCount");
  fabBadge.textContent = n;
  fabBadge.hidden = n === 0;
  document.getElementById("btnFilterToggle").classList.toggle("has-filters", n > 0);
  renderAppliedChips();
}

document.getElementById("btnFilterToggle").onclick = () => {
  if (isMobileLayout()) { openMobileFilter(); return; }
  const panel = document.getElementById("filterPanel");
  panel.hidden = !panel.hidden;
  document.getElementById("btnFilterToggle").setAttribute("aria-expanded", String(!panel.hidden));
};

function render() {
  updateFilterCount();
  syncDatasetControls();
  const q = document.getElementById("q").value.trim().toLowerCase();
  document.getElementById("btnClearSearch").style.display = q ? "block" : "none";

  // 1. Get filtered pool based on non-brand criteria (channel, city, district, status, query, viewport)
  const nonBrandPool = getNonBrandFilteredPool();

  // 2. Dynamically update counts on all brand pills in real time!
  updateBrandPillsCounts(nonBrandPool);

  // 3. Update viewport status indicator & guidance hint
  const hintBar = document.getElementById("viewportHintBar");
  const hintText = document.getElementById("viewportHintText");
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;

  if (isViewportSync && map) {
    const curZoom = map.getZoom();
    if (curZoom <= 8) {
      document.getElementById("lblViewportIndicator").innerHTML = `地圖目前涵蓋全台：<strong>${nonBrandPool.length}</strong> 間`;
      if (hintBar) {
        hintBar.style.display = "flex";
        if (hintText) hintText.textContent = "目前地圖視野涵蓋全台。請滾動滑鼠滾輪放大或拖曳地圖，名錄將即時篩選畫面內門市！";
      }
    } else {
      const areaLabel = (city && dist) ? ` (${city} ${dist})` : (city ? ` (${city})` : "");
      document.getElementById("lblViewportIndicator").innerHTML = `目前地圖範圍${areaLabel}：<strong>${nonBrandPool.length}</strong> 間`;
      if (hintBar) hintBar.style.display = "none";
    }
  } else {
    let scopeDesc = "全台";
    if (city && dist) {
      scopeDesc = `${city} ${dist}`;
    } else if (city) {
      scopeDesc = city;
    }
    document.getElementById("lblViewportIndicator").textContent = `清單範圍：${scopeDesc}，共 ${nonBrandPool.length} 間`;
    if (hintBar) hintBar.style.display = "none";
  }

  // 4. Apply Brand Filter or PK Mode
  // 已選品牌在目前條件下沒有門市時自動取消，避免清單變空
  if (activeBrands.size && nonBrandPool.length > 0) {
    [...activeBrands].forEach(b => { if (!nonBrandPool.some(s => s.brand === b)) activeBrands.delete(b); });
  }
  // 縣市／行政區／型態／狀態的選項與數字跟著已選品牌更新
  initDropdowns();

  let pool = nonBrandPool.filter(s => {
    if (activeBrands.size && !activeBrands.has(s.brand)) {
      return false;
    }
    return true;
  });

  // 5. Distance Sorting (P1 Feature: 離我最近)
  if (isSortedByDistance && userLocation) {
    pool.sort((a, b) => (a._userDist || 9999) - (b._userDist || 9999));
  }

  filteredStores = pool;
  if (isTimelineMode) {
    // 時光軸模式也要同步品牌按鈕狀態（原本提前 return，按鈕一直停在「全部」）
    syncBrandPills();
    recalculateTimelineBounds();
    const tlPool = getTimelineStorePool();
    renderTimelineSparkline(tlPool);
    updateTimeline(timelineYear, false);
    return;
  }
  const brandSuffix = activeBrands.size === 0 ? "" : activeBrands.size <= 3 ? `（${[...activeBrands].join("、")}）` : `（${activeBrands.size} 個品牌）`;
  if (isViewportSync && map && map.getZoom() <= 8) {
    document.getElementById("lblCount").textContent = `${filteredStores.length} 間門市（全台視野）${brandSuffix}`;
  } else if (isViewportSync) {
    document.getElementById("lblCount").textContent = `${filteredStores.length} 間門市（地圖畫面內）${brandSuffix}`;
  } else {
    document.getElementById("lblCount").textContent = `${filteredStores.length} 間門市${brandSuffix}`;
  }
  document.getElementById("lblFloatingCount").textContent = filteredStores.length;
  document.getElementById("btnMobileFilterApply").textContent = `顯示 ${filteredStores.length} 間門市`;
  document.getElementById("lblSheetFabCount").textContent = filteredStores.length;
  syncBrandPills();
  renderMarkers();
  renderList();
  updateActiveRegionTooltip();
}

/* ─── MAP MARKERS ─── */
// 縮小到全台／跨縣市視野時，標記改成小圓點並隱藏品牌縮寫，避免文字互相重疊
// （地圖初始化時就會觸發，因此門檻直接寫在函式內，避免 const 尚未初始化）
function syncMarkerOverviewMode() {
  if (!map) return;
  map.getContainer().classList.toggle("map-overview", map.getZoom() <= 9);
}
// 門市標記快取：篩選或移動地圖時只增減差異，不再每次重建全部標記（手機上原本是延遲主因之一）
const CAN_HOVER = window.matchMedia("(hover: hover)").matches;

// 點地圖上的門市：先顯示資訊卡；若已在看某間門市的詳情，則直接切換面板到這一間
function onStoreMarkerClick(s, layer) {
  const key = "s" + s.n;
  const detailOpen = document.getElementById("sidebarDetailSection").style.display === "flex";
  selectStore(key, s, false);
  if (detailOpen && (!isMobileLayout() || sheetState !== "hidden")) {
    map.closePopup();
    openStoreDrawer(s, currentDetailTab === "route" ? "info" : currentDetailTab);
    return;
  }
  layer.openPopup();
}

function popupOptions() {
  const sheetH = isMobileLayout() ? sheetHeightFor(sheetState) : 0;
  return { className: "custom-popup", minWidth: 260, maxWidth: 320, autoPan: true,
           autoPanPaddingTopLeft: [16, isMobileLayout() ? 120 : 24], autoPanPaddingBottomRight: [16, sheetH + 24] };
}

function bindStorePopup(layer, s) {
  layer.bindPopup(() => makePopupHtml(s), popupOptions());
  layer.on("popupopen", () => { layer.closeTooltip(); const pp = layer.getPopup(); if (pp) pp.options = Object.assign(pp.options, popupOptions()); });
  layer.on("click", () => onStoreMarkerClick(s, layer));
}
const markerCache = {};
function getCachedMarker(s, isNew) {
  const key = "s" + s.n;
  const sig = `${highContrastPins ? 1 : 0}|${isNew ? 1 : 0}`;
  let c = markerCache[key];
  if (!c) {
    const mk = L.marker([s.lat, s.lng], { icon: makeMarkerIcon(s, isNew) });
    if (CAN_HOVER) mk.bindTooltip(s.store_name, { direction: "top", offset: [0, -34], className: "store-hover-tip" });
    bindStorePopup(mk, s);
    c = markerCache[key] = { mk, sig };
  } else if (c.sig !== sig) {
    c.mk.setIcon(makeMarkerIcon(s, isNew));
    c.sig = sig;
  }
  return c.mk;
}

// 縮小視野（全台／縣市）改用單一 canvas 畫圓點：數百個帶陰影的 DOM 大頭針在縮放動畫時
// 每一格都要重畫，是手機在全台視野卡頓的主因；放大到街區才換回大頭針。
const DOT_MAX_ZOOM = 10;
// padding 0.5 會讓 canvas 變成視窗的 2×2 倍（高解析手機上數千萬像素），重畫與合成都很慢
const dotRenderer = L.canvas({ padding: 0.15, tolerance: 6 });
const dotCache = {};
let dots = {};
let markerPulseActive = false;
let markerPulseYear = null;
let pinStores = {}; // 目前篩選結果（key → 門市）；大頭針等需要時才建立

function getCachedDot(s) {
  const key = "s" + s.n;
  let d = dotCache[key];
  if (!d) {
    const cfg = BRANDS[s.brand] || { color: "#0058A3" };
    d = L.circleMarker([s.lat, s.lng], {
      renderer: dotRenderer, radius: 5.5, weight: 1.5,
      color: "#FFFFFF", fillColor: cfg.color, fillOpacity: 1
    });
    if (CAN_HOVER) d.bindTooltip(s.store_name, { direction: "top", offset: [0, -6], className: "store-hover-tip" });
    bindStorePopup(d, s);
    dotCache[key] = d;
  }
  d.setStyle({ color: highContrastPins ? "#111111" : "#FFFFFF" });
  return d;
}

function useDotMode() {
  return !markerPulseActive && map.getZoom() <= DOT_MAX_ZOOM;
}

// 依目前縮放，讓「圓點」或「大頭針」其中一組出現在地圖上
function applyMarkerMode() {
  if (markerClusterLayer) return;
  const dotMode = useDotMode();
  // 大頭針延後到真的要顯示才建立（全台視野只畫圓點，初次載入不必建 270 個 marker）
  Object.entries(pinStores).forEach(([k, s]) => {
    if (!markers[k] && (!dotMode || k === selectedKey)) {
      markers[k] = getCachedMarker(s, markerPulseYear && s.opened_year === markerPulseYear);
    }
  });
  Object.entries(markers).forEach(([k, mk]) => {
    const keepPin = !dotMode || k === selectedKey;
    if (keepPin && !map.hasLayer(mk)) mk.addTo(map);
    if (!keepPin && map.hasLayer(mk)) map.removeLayer(mk);
  });
  Object.values(dots).forEach(d => {
    if (dotMode && !map.hasLayer(d)) d.addTo(map);
    if (!dotMode && map.hasLayer(d)) map.removeLayer(d);
  });
}

// 縮放跨過門檻時切換圓點／大頭針（註冊在這裡，確保 filteredStores 等變數已初始化）
map.on("zoomend", applyMarkerMode);

function renderMarkers(pulseYear = null) {
  markerPulseActive = !!pulseYear;
  markerPulseYear = pulseYear;
  const useClusters = (activeDatasetMode === "ecommerce" || (activeDatasetMode === "supermarket" && filteredStores.length > 150)) && typeof L.markerClusterGroup === "function";
  if (useClusters) {
    // 電商據點：聚合圖層只建立一次，之後只增減有變化的據點
    if (!markerClusterLayer) {
      Object.values(markers).forEach(m => map.removeLayer(m));
      Object.values(dots).forEach(d => map.removeLayer(d));
      markers = {};
      dots = {};
      markerClusterLayer = L.markerClusterGroup({
        chunkedLoading: true,
        chunkInterval: 80,
        chunkDelay: 24,
        maxClusterRadius: 52,
        disableClusteringAtZoom: 16,
        removeOutsideVisibleBounds: true
      });
      map.addLayer(markerClusterLayer);
    }
    const next = {};
    const toAdd = [];
    filteredStores.forEach(s => {
      const key = "s" + s.n;
      const mk = getCachedMarker(s, pulseYear && s.opened_year === pulseYear);
      next[key] = mk;
      if (!markers[key]) toAdd.push(mk);
    });
    const toRemove = Object.keys(markers).filter(k => !next[k]).map(k => markers[k]);
    if (toRemove.length) markerClusterLayer.removeLayers(toRemove);
    if (toAdd.length) markerClusterLayer.addLayers(toAdd);
    markers = next;
    return;
  }
  if (markerClusterLayer) {
    map.removeLayer(markerClusterLayer);
    markerClusterLayer.clearLayers();
    markerClusterLayer = null;
    markers = {};
  }

  const next = {}, nextDots = {}, nextStores = {};
  const dotMode = useDotMode();
  filteredStores.forEach(s => {
    const key = "s" + s.n;
    nextStores[key] = s;
    // 已建過的大頭針沿用（更新樣式）；圓點模式下其餘延後到 applyMarkerMode 需要時才建
    if (!dotMode || key === selectedKey || markers[key]) next[key] = getCachedMarker(s, pulseYear && s.opened_year === pulseYear);
    nextDots[key] = getCachedDot(s);
  });
  pinStores = nextStores;
  Object.keys(markers).forEach(k => { if (!next[k] && map.hasLayer(markers[k])) map.removeLayer(markers[k]); });
  Object.keys(dots).forEach(k => { if (!nextDots[k] && map.hasLayer(dots[k])) map.removeLayer(dots[k]); });
  markers = next;
  dots = nextDots;
  applyMarkerMode();
}

/* ─── STORE LIST ─── */
function renderList() {
  const container = document.getElementById("storeList");
  container.innerHTML = "";

  if (filteredStores.length === 0) {
    const ecommerceMessage = activeDatasetMode === "ecommerce" ? `
      <div class="title">電商取貨據點採獨立圖層</div>
      <div class="desc">蝦皮據點屬即時資料，正式同步前請使用官方查詢。</div>
      <a href="https://shopee.tw/m/spxservicepoint" target="_blank" rel="noopener" class="btn-card-gmap" style="margin-top:10px">${SVG.external} 開啟蝦皮官方據點查詢</a>
    ` : `
      <div class="title">找不到符合目前篩選條件的門市</div>
      <div class="desc">${isViewportSync ? "目前地圖視野範圍內無門市，請縮小地圖或關閉視野連動" : "請嘗試清空關鍵字或放寬篩選條件"}</div>
    `;
    container.innerHTML = `
      <div class="empty-state">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 0 0 9.5 3C6.08 3 3.28 5.64 3.03 9h2.02C5.3 6.75 7.18 5 9.5 5 11.99 5 14 7.01 14 9.5S11.99 14 9.5 14c-.17 0-.33-.03-.5-.05v2.02c.17.02.33.03.5.03 1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5z"/><path d="M6.47 10.82 4 13.29l-2.47-2.47-.71.71L3.29 14 .82 16.47l.71.71L4 14.71l2.47 2.47.71-.71L4.71 14l2.47-2.47z"/></svg>
        ${ecommerceMessage}
      </div>`;
    return;
  }

  if (viewMode === "cards") renderCards(container);
  else renderTable(container);
}

// 清單分批建立：先畫第一批，其餘等捲到底部附近才建立（清單收起或在畫面外時完全不建立）。
// 新的 render 會取消舊的批次。卡片與表格列共用。
let listBuildToken = 0;
let listBuildObserver = null;
function buildListLazily(container, jobs, build) {
  const token = ++listBuildToken;
  if (listBuildObserver) { listBuildObserver.disconnect(); listBuildObserver = null; }
  let i = 0;
  const FIRST = 24, CHUNK = 30;
  const sentinel = document.createElement("div");
  sentinel.className = "list-sentinel";
  sentinel.setAttribute("aria-hidden", "true");
  container.appendChild(sentinel);
  const run = (limit) => {
    if (token !== listBuildToken) return;
    const end = Math.min(jobs.length, i + limit);
    for (; i < end; i++) jobs[i].wrap.appendChild(build(jobs[i].s));
    if (i >= jobs.length) {
      sentinel.remove();
      if (listBuildObserver) { listBuildObserver.disconnect(); listBuildObserver = null; }
    }
  };
  sentinel.addEventListener("build-more", () => run(CHUNK));
  run(FIRST);
  if (i < jobs.length) {
    if (!("IntersectionObserver" in window)) { run(jobs.length); return; }
    listBuildObserver = new IntersectionObserver(entries => {
      if (entries.some(e => e.isIntersecting)) run(CHUNK);
    }, { rootMargin: "600px 0px" });
    listBuildObserver.observe(sentinel);
  }
}

// 需要某張卡片存在時（例如點地圖標記要捲到對應卡片），把清單補建到該門市為止
function ensureListBuiltUntil(key) {
  let sentinel;
  while (!document.querySelector(`[data-key="${key}"]`) && (sentinel = document.querySelector(".list-sentinel"))) {
    sentinel.dispatchEvent(new CustomEvent("build-more"));
  }
}

function renderCards(container) {
  const displayStores = activeDatasetMode === "ecommerce" ? filteredStores.slice(0, 200) : filteredStores;
  if (displayStores.length < filteredStores.length) {
    const notice = document.createElement("div");
    notice.className = "viewport-hint-bar";
    notice.style.display = "flex";
    notice.innerHTML = `<span>為維持流暢度，名錄先顯示 200 筆；可用縣市、行政區或關鍵字縮小範圍。地圖仍包含全部 ${filteredStores.length} 間。</span>`;
    container.appendChild(notice);
  }
  if (isSortedByDistance && userLocation) {
    const cardsWrap = document.createElement("div");
    container.appendChild(cardsWrap);
    buildListLazily(container, displayStores.map(s => ({ wrap: cardsWrap, s })), createStoreCardElement);
    return;
  }

  const groups = {};
  BRAND_KEYS.forEach(b => groups[b] = []);
  displayStores.forEach(s => { if (groups[s.brand]) groups[s.brand].push(s); });

  const jobs = [];
  BRAND_KEYS.forEach(brand => {
    const list = groups[brand];
    if (!list.length) return;

    const cfg = BRANDS[brand];
    const hdr = document.createElement("div");
    hdr.className = "brand-section-header";
    hdr.style.background = cfg.color;
    hdr.innerHTML = `
      <div class="left-title">
        <span>${cfg.label}</span>
        <span class="count-tag">${list.length}</span>
      </div>
      <div class="chevron">${SVG.chevron}</div>
    `;

    let collapsed = false;
    hdr.onclick = () => {
      collapsed = !collapsed;
      hdr.classList.toggle("collapsed", collapsed);
      cardsWrap.style.display = collapsed ? "none" : "block";
    };
    container.appendChild(hdr);

    const cardsWrap = document.createElement("div");
    list.forEach(s => jobs.push({ wrap: cardsWrap, s }));
    container.appendChild(cardsWrap);
  });
  buildListLazily(container, jobs, createStoreCardElement);
}

function createStoreCardElement(s) {
  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const key = "s" + s.n;

  const card = document.createElement("div");
  const isArchived = s.status_category.includes("歷史");
  card.className = "store-card" + (isArchived ? " is-archived" : "");
  card.dataset.key = key;
  if (selectedKey === key) card.classList.add("selected");

  card.innerHTML = `
    <div class="card-top-bar">
      <span class="card-brand-tag" style="background:${cfg.color}">${s.brand}</span>
      <div style="display:flex;align-items:center;gap:4px">
        ${s._userDist !== undefined && isSortedByDistance ? `<span class="card-dist-badge">${SVG.gps} 距您 ${formatDist(s._userDist)}</span>` : ""}
        ${getStatusBadge(s)}
      </div>
    </div>
    <div class="card-name-title">${s.store_name}</div>
    <div class="card-meta-line">
      <span class="card-channel-pill">${s.region ? s.region + "地區" : ""}</span>
      <span>${s.city} ${s.district || ""}</span>
    </div>
    <div class="tag-container">
      <span class="tag-badge tag-channel">${SVG.store} ${s.store_format || s.channel_format}</span>
    </div>
    <div class="card-address-box">
      ${SVG.pin}
      <span>${s.address}</span>
    </div>
    <div class="card-actions-row">
      <button class="card-action-btn card-action-emph" onclick="event.stopPropagation(); triggerRoutePlanning(ALL_STORES.find(item => item.n === ${s.n}))" title="規劃前往 ${s.store_name} 路線">
        ${SVG.route} <span>規劃路線</span>
      </button>
      <a class="card-action-btn card-action-secondary" href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener" onclick="event.stopPropagation();" title="在 Google Maps 開啟完整導航">
        ${SVG.external} <span class="btn-text-full">在 Google Maps 開啟</span><span class="btn-text-compact">Google 地圖</span>
      </a>
    </div>
  `;

  card.onclick = (e) => {
    if (e.target.closest("a") || e.target.closest(".card-action-btn") || e.target.closest(".btn-card-view-detail")) return;
    selectStore(key, s, true);
    openStoreDrawer(s, "info");
  };

  return card;
}

function renderTable(container) {
  const wrap = document.createElement("div");
  wrap.style.overflowX = "auto";
  const tbl = document.createElement("table");
  tbl.style.cssText = "width:100%;border-collapse:collapse;font-size:12px;background:#fff;border-radius:8px;overflow:hidden";
  tbl.innerHTML = `
    <thead style="position:sticky;top:0;background:#0058A3;color:#fff;z-index:2">
      <tr>
        <th style="padding:8px 10px;text-align:left;white-space:nowrap">品牌 / 門市</th>
        <th style="padding:8px 10px;white-space:nowrap">地區</th>
        <th class="col-wide" style="padding:8px 10px;white-space:nowrap">門市型態</th>
        <th class="col-wide" style="padding:8px 10px;white-space:nowrap">地址與導航</th>
        ${isSortedByDistance ? `<th style="padding:8px 10px;white-space:nowrap">距離</th>` : ""}
        <th class="col-wide" style="padding:8px 10px;white-space:nowrap">營運狀態</th>
      </tr>
    </thead>
    <tbody id="tblBody"></tbody>`;
  wrap.appendChild(tbl);
  container.appendChild(wrap);
  const tbody = tbl.querySelector("#tblBody");

  const displayStores = activeDatasetMode === "ecommerce" ? filteredStores.slice(0, 200) : filteredStores;
  if (displayStores.length < filteredStores.length) {
    const notice = document.createElement("div");
    notice.className = "viewport-hint-bar";
    notice.style.display = "flex";
    notice.textContent = `為維持流暢度，表格先顯示 200 筆；地圖仍包含全部 ${filteredStores.length} 間。`;
    container.appendChild(notice);
  }
  const buildRow = (s) => {
    const key = "s" + s.n;
    const cfg = BRANDS[s.brand] || { color: "#0058A3" };
    const tableBrand = cfg.tableLabel || s.brand;
    const tableStoreName = s.store_name.startsWith(s.brand + " ")
      ? s.store_name.slice(s.brand.length + 1)
      : s.store_name;
    const tr = document.createElement("tr");
    tr.style.cssText = "cursor:pointer;border-bottom:1px solid #E2E8F0;transition:background 0.1s";
    tr.dataset.key = key;
    if (selectedKey === key) tr.style.background = "#EBF4FC";

    tr.innerHTML = `
      <td style="padding:8px 10px;min-width:128px">
        <span title="${s.brand}" style="display:inline-flex;white-space:nowrap;background:${cfg.color};color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:4px">${tableBrand}</span>
<br>
        <strong title="${tableStoreName}" style="font-size:12.5px;color:#111;margin-top:4px;display:block;white-space:nowrap;max-width:150px;overflow:hidden;text-overflow:ellipsis">${tableStoreName}</strong>
        <span class="col-narrow-meta">${s.store_format || s.channel_format}${s.status_category !== "現行營運中" ? ` · ${s.status_category === "暫停營業" ? "暫停營業" : "已歇業"}` : ""}</span>
      </td>
      <td style="padding:8px 10px;white-space:nowrap">${s.city}<br><span style="color:#64748B;font-size:11px">${s.district||""}</span></td>
      <td class="col-wide" style="padding:8px 10px;white-space:nowrap;font-size:11px;color:#475569">${s.store_format || s.channel_format}</td>
      <td class="col-wide" style="padding:8px 10px">
        <a href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener" style="color:#0058A3;font-weight:700;font-size:11.5px;text-decoration:none;display:inline-flex;align-items:center;gap:4px" onclick="event.stopPropagation()">
          ${SVG.external} ${s.address}
        </a>
      </td>
      ${isSortedByDistance ? `
        <td style="padding:8px 10px;white-space:nowrap">
          <span class="card-dist-badge">${formatDist(s._userDist)}</span>
        </td>
      ` : ""}
      <td class="col-wide" style="padding:8px 10px;white-space:nowrap">
        ${getStatusBadge(s)}
      </td>`;
    tr.onmouseenter = () => { if (selectedKey !== key) tr.style.background = "#F1F5F9"; };
    tr.onmouseleave = () => { if (selectedKey !== key) tr.style.background = ""; };
    tr.onclick = (e) => {
      if (e.target.tagName === "A") return;
      selectStore(key, s, true);
      openStoreDrawer(s, "info");
    };
    return tr;
  };
  buildListLazily(wrap, displayStores.map(s => ({ wrap: tbody, s })), buildRow);
}

/* ─── P1: CATCHMENT BUFFER CIRCLE & DRAWER CONTROLLER ─── */
let currentDetailTab = "info";

document.getElementById("detailTabsBar").addEventListener("keydown", (e) => {
  if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
  const tabs = [...document.querySelectorAll(".detail-tab-btn")];
  const i = tabs.findIndex(b => b.classList.contains("active"));
  const next = tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
  switchDetailTab(next.dataset.tab);
  next.focus();
  e.preventDefault();
});

function switchDetailTab(tabName) {
  currentDetailTab = tabName;
  const tabs = document.querySelectorAll(".detail-tab-btn");
  tabs.forEach(btn => {
    const on = btn.dataset.tab === tabName;
    btn.classList.toggle("active", on);
    btn.setAttribute("aria-selected", on ? "true" : "false");
    btn.tabIndex = on ? 0 : -1;
  });

  const panes = document.querySelectorAll(".detail-tab-pane");
  const targetPaneId = "paneDetail" + tabName.charAt(0).toUpperCase() + tabName.slice(1);
  panes.forEach(pane => {
    pane.classList.toggle("active", pane.id === targetPaneId);
  });

  if (isMobileLayout()) {
    if (tabName === "route" && sheetState !== "route") { sheetBeforeRoute = sheetState; setSheet("route"); }
    else if (tabName !== "route" && sheetState === "route") setSheet(sheetBeforeRoute === "route" ? "half" : sheetBeforeRoute);
  }
  if (tabName === "route" && currentDetailStore && runRouteFetch) {
    runRouteFetch();
  }
}

function openStoreDrawerByKey(key) {
  const s = ALL_STORES.find(item => "s" + item.n === key);
  if (s) { selectStore(key, s, false); openStoreDrawer(s, "info", { fromMap: true }); }
}

function triggerRoutePlanningByKey(key) {
  const s = ALL_STORES.find(item => "s" + item.n === key);
  if (s) triggerRoutePlanning(s);
}

function triggerRoutePlanning(s) {
  if (!s) return;
  if (map) map.closePopup();
  const key = "s" + s.n;
  selectStore(key, s, true);
  openStoreDrawer(s, "route");
}

// 門市詳情的瀏覽紀錄：從「周邊」點進另一間門市時，返回鍵回到前一間
let detailHistory = [];
let listScrollBeforeDetail = 0;

// opts.pushHistory：保留目前門市以便返回；opts.fromMap：從地圖點擊開啟（手機先顯示預覽高度）
function openStoreDrawer(s, preferredTab = null, opts = {}) {
  const listSection = document.getElementById("sidebarListSection");
  if (listSection.style.display !== "none") {
    listScrollBeforeDetail = isMobileLayout() ? listSection.scrollTop : document.getElementById("storeList").scrollTop;
  }
  if (opts.pushHistory && currentDetailStore && currentDetailStore !== s) {
    detailHistory.push({ s: currentDetailStore, tab: currentDetailTab });
  } else if (!opts.keepHistory) {
    detailHistory = [];
  }
  currentDetailStore = s;

  if (map) map.closePopup();

  if (isTimelineMode && timelinePlaying) {
    pauseTimeline();
  }

  if (isSidebarCollapsed) {
    expandSidebar();
  }

  document.getElementById("sidebarListSection").style.display = "none";
  const detailSection = document.getElementById("sidebarDetailSection");
  detailSection.style.display = "flex";

  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const topBadge = document.getElementById("detailTopBrandBadge");
  topBadge.textContent = s.brand;
  topBadge.style.background = cfg.color;

  updateBufferCircleOnMap(s);

  // Render Pinned Identity Header
  const pinnedHdr = document.getElementById("detailPinnedHeader");
  if (pinnedHdr) {
    const distText = (s._userDist !== undefined && s._userDist !== null) ? ` · 距你 ${formatDist(s._userDist)}` : "";
    const prev = detailHistory[detailHistory.length - 1];
    const backLabel = prev ? `返回 ${prev.s.store_name}` : "返回門市清單";
    pinnedHdr.innerHTML = `
      <div class="sk-hdr-row">
        <button class="sk-hdr-btn" onclick="goBackInDrawer()" title="${backLabel}" aria-label="${backLabel}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z"/></svg>
        </button>
        <div class="sk-hdr-text">
          <h2 class="detail-title" title="${s.store_name}">${s.store_name}</h2>
          <div class="detail-sub-meta">
            <span class="brand-dot" style="background:${cfg.color}"></span>
            <span>${s.city} ${s.district || ""}${distText}</span>
          </div>
        </div>
        <button class="sk-hdr-btn" onclick="dismissStoreDrawer()" title="關閉並回到地圖" aria-label="關閉門市面板，回到地圖">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/></svg>
        </button>
      </div>
      ${s.status_category !== "現行營運中" ? `<div class="sk-hdr-status">${getStatusBadge(s)}</div>` : ""}
    `;
  }

  // Render 3 Distinct Tab Panes inside Body
  const detailBody = document.getElementById("detailContentBody");
  detailBody.innerHTML = `
    <!-- 資訊 -->
    <div class="detail-tab-pane" id="paneDetailInfo" role="tabpanel" aria-labelledby="tabDetailInfo">
      <dl class="sk-facts">
        <div><dt>品牌</dt><dd>${s.brand}</dd></div>
        <div><dt>型態</dt><dd>${s.store_format || s.channel_format}</dd></div>
        <div><dt>開幕</dt>${s.opened_year
          ? `<dd>${s.opened_year} 年${s.opened_basis === "商工登記" ? `<span class="sk-basis" title="經濟部商工登記分公司核准設立日，通常比實際開幕早 1～4 個月">依商工登記</span>` : ""}</dd>`
          : `<dd class="sk-unknown" title="查無新聞、官方或商工登記等可靠來源，不推估年份">未知<span class="sk-basis">查無可靠來源</span></dd>`}</div>
      </dl>
      <div class="sk-section">
        <div class="sk-label">地址</div>
        <div class="sk-address-row">
          <span>${s.address}</span>
          <button class="sk-icon-btn" onclick="copyStoreAddress('${s.address}')" title="複製地址" aria-label="複製地址">${SVG.copy}</button>
        </div>
      </div>
      ${(s.status_category !== '現行營運中' && s.note) ? `
        <div class="sk-notice">
          <strong>營運狀態</strong>
          <div>${s.note}</div>
        </div>` : ''}
      <button class="sk-link-row" onclick="switchDetailTab('catchment')">
        <span id="lblInfoNearby">查看周邊門市</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6-6-6z"/></svg>
      </button>
      <div class="sk-actions">
        <a class="sk-btn sk-btn-primary" href="${getGmapsSearchUrl(s)}" target="_blank" rel="noopener">${SVG.external} 在 Google Maps 開啟</a>
        <div class="sk-btn-row">
          <button class="sk-btn sk-btn-secondary" onclick="switchDetailTab('route')">${SVG.route} 規劃路線</button>
          <button class="sk-btn sk-btn-secondary" onclick="focusCurrentDrawerStore()">${SVG.crosshair} 地圖定位</button>
        </div>
      </div>
    </div>

    <!-- 路線 -->
    <div class="detail-tab-pane" id="paneDetailRoute" role="tabpanel" aria-labelledby="tabDetailRoute">
      <div id="routePlanningBox">
        <div class="route-mode-switcher" id="routeModeSwitcher" role="group" aria-label="交通方式">
          <button class="btn-route-mode ${currentRouteMode === 'driving' ? 'active' : ''}" data-mode="driving">${SVG.car} <span>開車</span></button>
          <button class="btn-route-mode ${currentRouteMode === 'transit' ? 'active' : ''}" data-mode="transit">${SVG.transit} <span>大眾運輸</span></button>
          <button class="btn-route-mode ${currentRouteMode === 'walking' ? 'active' : ''}" data-mode="walking">${SVG.walk} <span>步行</span></button>
        </div>

        <div class="sk-route-result" id="routeResult" aria-live="polite">
          <div class="sk-route-duration" id="lblRouteDuration">--</div>
          <div class="sk-route-meta" id="lblRouteMeta"></div>
        </div>

        <div class="sk-notice sk-notice-sm" id="routeGpsHint" hidden>
          尚未取得你的位置，目前從台北車站計算。<button class="sk-inline-link" id="btnHintLocate">開啟定位</button>
        </div>

        <details class="sk-origin-details" id="routeOriginDetails">
          <summary>
            <span>從 <strong id="lblOriginSummary">我的位置</strong>${currentRouteMode === 'transit' ? ` · <span id="lblDepartureSummary">${routeDeparture === 'tomorrow9' ? '明早 9:00' : '現在'}</span>` : ''}</span>
            <span class="sk-change">更改</span>
          </summary>
          <div class="sk-origin-stack">
            <div class="sk-section" id="routeDepartureRow" ${currentRouteMode === 'transit' ? '' : 'hidden'}>
              <label class="sk-label" for="selRouteDeparture">出發時間</label>
              <select id="selRouteDeparture" class="sel-route-origin">
                <option value="now" ${routeDeparture === 'now' ? 'selected' : ''}>現在出發</option>
                <option value="tomorrow9" ${routeDeparture === 'tomorrow9' ? 'selected' : ''}>明天早上 9:00 出發</option>
              </select>
            </div>
            <label class="sk-label" for="selRouteOrigin">出發地</label>
            <select id="selRouteOrigin" class="sel-route-origin">
              <option value="gps">我的位置</option>
              <option value="tpe_main">台北車站</option>
              <option value="banqiao">板橋車站</option>
              <option value="hsinchu">新竹車站</option>
              <option value="taichung">台中車站</option>
              <option value="tainan">台南車站</option>
              <option value="zuoying">左營高鐵站</option>
              <option value="custom" disabled>地圖選點</option>
            </select>
            <div class="sk-btn-row">
              <button class="sk-btn sk-btn-secondary sk-btn-sm" id="btnRelocateGps">${SVG.gps} 用我目前的位置</button>
              <button class="sk-btn sk-btn-secondary sk-btn-sm" id="btnPickOriginOnMap">${SVG.pick} <span id="lblPickOrigin">在地圖上點選</span></button>
            </div>
          </div>
        </details>

        <div class="sk-actions">
          <a class="sk-btn sk-btn-primary" id="btnGmapsTurnByTurn" href="#" target="_blank" rel="noopener">${SVG.external} 在 Google Maps 導航</a>
          <button class="sk-link-btn" id="btnClearRoute">清除地圖上的路線</button>
        </div>
      </div>
    </div>

    <!-- 周邊 -->
    <div class="detail-tab-pane" id="paneDetailCatchment" role="tabpanel" aria-labelledby="tabDetailCatchment">
      <div class="sk-section">
        <div class="sk-catch-head">
          <span>半徑 <strong id="lblRadiusVal">${currentRadiusKm.toFixed(1)} km</strong></span>
          <label class="sk-switch">
            <input type="checkbox" id="chkToggleCircle" ${isBufferCircleEnabled ? 'checked' : ''}>
            <span>在地圖顯示範圍</span>
          </label>
        </div>
        <input type="range" id="rngRadius" class="radius-range-slider" min="1.0" max="30.0" step="0.5" value="${currentRadiusKm}" aria-label="服務半徑">
        <div class="radius-presets-row">
          ${[1, 3, 5, 10, 20].map(km => `<button class="btn-radius-preset" data-km="${km}">${km} km</button>`).join("")}
        </div>
      </div>
      <div id="catchmentResultsBox"></div>
    </div>
  `;

  clearActiveRoute();
  if (isMobileLayout()) {
    const target = opts.fromMap ? "preview" : "half";
    if (sheetState !== target && !(opts.fromMap && sheetState === "half")) setSheet(target);
    setTimeout(() => panToVisible(s.lat, s.lng), 300);
  }
  initCatchmentControls(s);
  updateCatchmentList(s);
  initRouteControls(s);
  switchDetailTab(preferredTab || "info");
}

function updateBufferCircleOnMap(s) {
  if (!isBufferCircleEnabled) {
    if (bufferCircle) {
      map.removeLayer(bufferCircle);
      bufferCircle = null;
    }
    return;
  }

  const cfg = BRANDS[s.brand] || { color: "#0058A3" };
  const radiusMeters = currentRadiusKm * 1000;

  if (!bufferCircle) {
    bufferCircle = L.circle([s.lat, s.lng], {
      radius: radiusMeters,
      color: cfg.color,
      fillColor: cfg.color,
      fillOpacity: 0.12,
      weight: 1.8,
      dashArray: "6, 6"
    }).addTo(map);
  } else {
    bufferCircle.setLatLng([s.lat, s.lng]);
    bufferCircle.setRadius(radiusMeters);
    bufferCircle.setStyle({ color: cfg.color, fillColor: cfg.color });
  }
}

function initCatchmentControls(s) {
  const slider = document.getElementById("rngRadius");
  const presets = document.querySelectorAll(".btn-radius-preset");

  function setRadius(newR) {
    currentRadiusKm = parseFloat(newR);
    if (slider) slider.value = currentRadiusKm;
    const lbl = document.getElementById("lblRadiusVal");
    if (lbl) lbl.textContent = `${currentRadiusKm.toFixed(1)} km`;

    presets.forEach(p => {
      const km = parseFloat(p.dataset.km);
      p.classList.toggle("active", Math.abs(km - currentRadiusKm) < 0.1);
    });

    if (bufferCircle) {
      bufferCircle.setRadius(currentRadiusKm * 1000);
    }

    updateCatchmentList(s);
  }

  if (slider) {
    slider.oninput = (e) => setRadius(e.target.value);
  }

  presets.forEach(btn => {
    btn.onclick = () => setRadius(btn.dataset.km);
  });

  presets.forEach(p => {
    const km = parseFloat(p.dataset.km);
    p.classList.toggle("active", Math.abs(km - currentRadiusKm) < 0.1);
  });

  const chkToggleCircle = document.getElementById("chkToggleCircle");
  if (chkToggleCircle) {
    chkToggleCircle.onchange = () => {
      isBufferCircleEnabled = chkToggleCircle.checked;
      updateBufferCircleOnMap(s);
    };
  }
}

// 周邊門市品牌篩選（換門市時重設）
let catchmentBrandFilter = { storeN: null, brand: null };
const SAME_BUILDING_KM = 0.05;

// 八方位（以目前門市為中心）
function compassDirection(from, to) {
  const y = Math.sin((to.lng - from.lng) * Math.PI / 180) * Math.cos(to.lat * Math.PI / 180);
  const x = Math.cos(from.lat * Math.PI / 180) * Math.sin(to.lat * Math.PI / 180) -
            Math.sin(from.lat * Math.PI / 180) * Math.cos(to.lat * Math.PI / 180) * Math.cos((to.lng - from.lng) * Math.PI / 180);
  const deg = (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
  return ["北", "東北", "東", "東南", "南", "西南", "西", "西北"][Math.round(deg / 45) % 8] + "方";
}

function setCatchmentBrandFilter(brand) {
  catchmentBrandFilter.brand = catchmentBrandFilter.brand === brand ? null : brand;
  if (currentDetailStore) updateCatchmentList(currentDetailStore);
}

function updateCatchmentList(s) {
  const resBox = document.getElementById("catchmentResultsBox");
  if (!resBox) return;
  if (catchmentBrandFilter.storeN !== s.n) catchmentBrandFilter = { storeN: s.n, brand: null };

  const nearby = [];
  ALL_STORES.forEach(c => {
    if (c.n === s.n) return;
    const d = haversineDistanceKm(s.lat, s.lng, c.lat, c.lng);
    if (d <= currentRadiusKm) {
      nearby.push({ store: c, dist: d });
    }
  });

  nearby.sort((a, b) => a.dist - b.dist);

  const tabRadius = document.getElementById("lblTabRadius");
  if (tabRadius) tabRadius.textContent = String(+currentRadiusKm.toFixed(1));
  const infoNearby = document.getElementById("lblInfoNearby");
  if (infoNearby) infoNearby.textContent = nearby.length
    ? `附近 ${+currentRadiusKm.toFixed(1)} km 內有 ${nearby.length} 間門市`
    : `附近 ${+currentRadiusKm.toFixed(1)} km 內沒有其他門市`;

  if (nearby.length === 0) {
    resBox.innerHTML = `
      <div class="sk-empty">此範圍內沒有其他居家品牌門市</div>
    `;
    return;
  }

  // 依品牌統計，數量多的排前面
  const brandCounts = {};
  nearby.forEach(item => { brandCounts[item.store.brand] = (brandCounts[item.store.brand] || 0) + 1; });
  const brands = Object.keys(brandCounts).sort((a, b) => brandCounts[b] - brandCounts[a]);
  if (catchmentBrandFilter.brand && !brandCounts[catchmentBrandFilter.brand]) catchmentBrandFilter.brand = null;
  const activeBrand = catchmentBrandFilter.brand;
  const shown = activeBrand ? nearby.filter(item => item.store.brand === activeBrand) : nearby;

  resBox.innerHTML = `
    <div class="sk-label">範圍內 ${nearby.length} 間門市・${brands.length} 個品牌</div>
    <div class="sk-brand-chips" role="group" aria-label="依品牌篩選">
      <button class="sk-brand-chip ${activeBrand ? "" : "active"}" aria-pressed="${!activeBrand}" onclick="setCatchmentBrandFilter(null)">全部 ${nearby.length}</button>
      ${brands.map(b => {
        const color = (BRANDS[b] || { color: "#0058A3" }).color;
        const on = activeBrand === b;
        return `<button class="sk-brand-chip ${on ? "active" : ""}" aria-pressed="${on}" data-brand="${b}" onclick="setCatchmentBrandFilter(this.dataset.brand)"><span class="brand-dot" style="background:${color}"></span>${b} ${brandCounts[b]}</button>`;
      }).join("")}
    </div>
    <div class="competitor-list">
      ${shown.map(item => {
        const c = item.store;
        const cCfg = BRANDS[c.brand] || { color: "#0058A3" };
        const isSameBrand = (c.brand === s.brand);
        const sameBuilding = item.dist < SAME_BUILDING_KM;
        return `
          <div class="competitor-mini-item" onclick="navigateToCompetitor(${c.n})">
            <div style="display:flex;align-items:center;gap:8px;min-width:0">
              <span class="brand-dot" style="background:${cCfg.color}"></span>
              <div style="overflow:hidden;text-overflow:ellipsis">
                <div class="c-name">${c.store_name}</div>
                <div class="c-chan">${sameBuilding ? "同一棟建築" : `往${compassDirection(s, c)}`}${isSameBrand ? " · 同品牌" : ""}</div>
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:6px;flex-shrink:0">
              ${sameBuilding ? `<span class="badge-same-building">同棟</span>` : `<span class="badge-dist">${formatDist(item.dist)}</span>`}
            </div>
          </div>
        `;
      }).join("")}
    </div>
  `;
}

/* ─── P2: ROUTE PLANNING & TRAVEL TIME ENGINE (Netlify Serverless & Google Routes API) ─── */
let activeRouteLayer = null;
let activeRouteOriginMarker = null;
let currentRouteMode = "driving";
let selectedOriginPresetId = "gps";
let customRouteOrigin = null;
let isMapPickingOrigin = false;

const ROUTE_ORIGIN_PRESETS = {
  gps: { id: "gps", name: "我的位置", lat: null, lng: null },
  tpe_main: { id: "tpe_main", name: "台北車站", lat: 25.0478, lng: 121.5170 },
  banqiao: { id: "banqiao", name: "板橋車站", lat: 25.0142, lng: 121.4637 },
  hsinchu: { id: "hsinchu", name: "新竹車站", lat: 24.8018, lng: 120.9716 },
  taichung: { id: "taichung", name: "台中車站", lat: 24.1368, lng: 120.6850 },
  tainan: { id: "tainan", name: "台南車站", lat: 22.9972, lng: 120.2127 },
  zuoying: { id: "zuoying", name: "左營高鐵站", lat: 22.6874, lng: 120.3082 }
};

function getEffectiveOrigin() {
  if (customRouteOrigin) {
    return customRouteOrigin;
  }
  if (selectedOriginPresetId === "gps" && userLocation) {
    return { id: "gps", name: "我的位置", lat: userLocation.lat, lng: userLocation.lng };
  }
  if (ROUTE_ORIGIN_PRESETS[selectedOriginPresetId] && ROUTE_ORIGIN_PRESETS[selectedOriginPresetId].lat !== null) {
    return ROUTE_ORIGIN_PRESETS[selectedOriginPresetId];
  }
  return { id: "tpe_main", name: "台北車站", lat: 25.0478, lng: 121.5170 };
}

function formatDurationDisplay(minutes) {
  if (minutes < 60) {
    return { val: String(minutes), unit: "分鐘" };
  }
  const hours = Math.floor(minutes / 60);
  const rem = minutes % 60;
  if (rem === 0) {
    return { val: String(hours), unit: "小時" };
  }
  return { val: `${hours} 小時 ${rem}`, unit: "分" };
}

function formatDistanceDisplay(km) {
  if (km < 1) {
    return { val: String(Math.round(km * 1000)), unit: "公尺" };
  }
  return { val: km.toFixed(1), unit: "公里" };
}

function clearActiveRoute() {
  if (activeRouteLayer && map) {
    map.removeLayer(activeRouteLayer);
    activeRouteLayer = null;
  }
  if (activeRouteOriginMarker && map) {
    map.removeLayer(activeRouteOriginMarker);
    activeRouteOriginMarker = null;
  }
  const resBar = document.getElementById("routeResultsBar");
  if (resBar) resBar.style.display = "none";
}

function decodePolyline(encoded) {
  if (!encoded) return [];
  let points = [];
  let index = 0, len = encoded.length;
  let lat = 0, lng = 0;
  while (index < len) {
    let b, shift = 0, result = 0;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    let dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lat += dlat;
    shift = 0;
    result = 0;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    let dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lng += dlng;
    points.push([lat / 1e5, lng / 1e5]);
  }
  return points;
}

// 前端快取：同一起訖點與交通方式不重複呼叫 API（後端記憶體快取在冷啟動後會清空）
const routeResultCache = new Map();
let routeDeparture = "now"; // "now" | "tomorrow9"（僅大眾運輸）

function getDepartureIso() {
  if (currentRouteMode !== "transit" || routeDeparture !== "tomorrow9") return null;
  const d = new Date();
  d.setDate(d.getDate() + 1);
  d.setHours(9, 0, 0, 0);
  return d.toISOString();
}

async function requestRoutePlan(originLat, originLng, destLat, destLng, mode) {
  const departure = getDepartureIso();
  const cacheKey = [originLat.toFixed(4), originLng.toFixed(4), destLat.toFixed(4), destLng.toFixed(4), mode, departure ? departure.slice(0, 10) : "now"].join("|");
  if (routeResultCache.has(cacheKey)) return routeResultCache.get(cacheKey);
  try {
    let netlifyUrl = `/api/directions?originLat=${originLat}&originLng=${originLng}&destLat=${destLat}&destLng=${destLng}&mode=${mode}`;
    if (departure) netlifyUrl += `&departureTime=${encodeURIComponent(departure)}`;
    const res = await fetch(netlifyUrl, { signal: AbortSignal.timeout(10000) });
    const data = await res.json().catch(() => null);
    if (res.ok && data && data.success) {
      if (routeResultCache.size > 100) routeResultCache.delete(routeResultCache.keys().next().value);
      routeResultCache.set(cacheKey, data);
      return data;
    }
    const errMsg = (data && data.error) ? data.error : `HTTP ${res.status}: ${res.statusText || 'Google Routes API 連線失敗'}`;
    return {
      success: false,
      engine: "google",
      mode: mode,
      error: errMsg
    };
  } catch (e) {
    return {
      success: false,
      engine: "google",
      mode: mode,
      error: e.name === "TimeoutError" ? "Google Routes API 請求超時" : (e.message || "Google Routes API 連線異常")
    };
  }
}

function drawPolylineOnMap(result, orig) {
  clearActiveRoute();
  if (!result || !result.polyline) return;

  const BLUE = "#0058A3";
  const layers = [];
  // Google 地圖式畫法：白色外框 + 色線；步行段用圓點虛線
  const addLine = (pts, color, walking) => {
    if (walking) {
      layers.push(L.polyline(pts, { color, weight: 6, opacity: 0.9, dashArray: "0 10", lineCap: "round", interactive: false }));
    } else {
      layers.push(L.polyline(pts, { color: "#FFFFFF", weight: 9, opacity: 1, lineCap: "round", lineJoin: "round", interactive: false }));
      layers.push(L.polyline(pts, { color, weight: 5, opacity: 1, lineCap: "round", lineJoin: "round", interactive: false }));
    }
  };

  let all = [];
  if (currentRouteMode === "transit" && Array.isArray(result.steps) && result.steps.length) {
    // 大眾運輸逐段繪製：搭乘段用路線官方顏色，轉乘步行段用灰色圓點
    result.steps.forEach(st => {
      const pts = decodePolyline(st.polyline);
      if (!pts.length) return;
      all = all.concat(pts);
      addLine(pts, st.mode === "WALK" ? "#767676" : (st.color || BLUE), st.mode === "WALK");
    });
  }
  if (!all.length) {
    all = decodePolyline(result.polyline);
    if (!all.length) return;
    addLine(all, BLUE, currentRouteMode === "walking");
  }
  activeRouteLayer = L.layerGroup(layers).addTo(map);

  const originIcon = L.divIcon({
    className: "route-origin-pin",
    html: `<div style="background:#FFFFFF;width:14px;height:14px;border-radius:50%;border:4px solid #111;box-sizing:border-box;box-shadow:0 1px 4px rgba(0,0,0,0.35)"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
  activeRouteOriginMarker = L.marker([orig.lat, orig.lng], { icon: originIcon, zIndexOffset: 3000 })
    .bindTooltip(`出發地：${orig.name}`, { direction: "top" })
    .addTo(map);

  const sheetPad = isMobileLayout() ? sheetHeightFor(sheetState) : 0;
  map.fitBounds(L.latLngBounds(all), isMobileLayout()
    ? { paddingTopLeft: [40, 130], paddingBottomRight: [40, sheetPad + 30] }
    : { padding: [60, 60] });
}

function updateRouteDisplay(s, explicitResult = null) {
  const box = document.getElementById("routePlanningBox");
  if (!box) return;

  const orig = getEffectiveOrigin();
  const elDur = document.getElementById("lblRouteDuration");
  const elMeta = document.getElementById("lblRouteMeta");
  const result = document.getElementById("routeResult");

  const noGps = selectedOriginPresetId === "gps" && !customRouteOrigin && !userLocation;
  const summary = document.getElementById("lblOriginSummary");
  if (summary) summary.textContent = orig.name;
  const depSummary = document.getElementById("lblDepartureSummary");
  if (depSummary) depSummary.textContent = routeDeparture === "tomorrow9" ? "明早 9:00" : "現在";
  const gpsHint = document.getElementById("routeGpsHint");
  if (gpsHint) gpsHint.hidden = !noGps;
  const gpsOpt = document.querySelector('#selRouteOrigin option[value="gps"]');
  if (gpsOpt) gpsOpt.textContent = noGps ? "我的位置（尚未取得定位）" : "我的位置";

  if (!explicitResult) {
    result.classList.remove("is-error");
    elDur.textContent = "計算中…";
    elMeta.textContent = "";
  } else if (!explicitResult.success) {
    result.classList.add("is-error");
    elDur.textContent = "暫時無法取得路線";
    elMeta.textContent = (currentRouteMode === "transit" && routeDeparture === "now")
      ? "目前可能已無班次，可改選「明天早上 9:00 出發」，或在 Google Maps 開啟導航"
      : "請稍後再試，或直接在 Google Maps 開啟導航";
    if (explicitResult.error) console.warn("[Routes API]", explicitResult.error);
  } else {
    result.classList.remove("is-error");
    const d = formatDurationDisplay(explicitResult.duration_min);
    elDur.textContent = `${d.val} ${d.unit}`;
    elMeta.textContent = explicitResult.distance_text;
  }

  const gMode = currentRouteMode === "transit" ? "transit" : (currentRouteMode === "walking" ? "walking" : "driving");
  const gmapNavBtn = document.getElementById("btnGmapsTurnByTurn");
  if (gmapNavBtn) {
    gmapNavBtn.href = `https://www.google.com/maps/dir/?api=1&origin=${orig.lat},${orig.lng}&destination=${s.lat},${s.lng}&travelmode=${gMode}`;
  }
}

let runRouteFetch = null;
let routeRequestSeq = 0;

function initRouteControls(s) {
  const box = document.getElementById("routePlanningBox");
  if (!box) return;

  const clearBtn = document.getElementById("btnClearRoute");
  clearBtn.onclick = clearActiveRoute;

  async function fetchAndApplyRoute() {
    const orig = getEffectiveOrigin();
    const seq = ++routeRequestSeq;
    updateRouteDisplay(s);
    try {
      const result = await requestRoutePlan(orig.lat, orig.lng, s.lat, s.lng, currentRouteMode);
      if (seq !== routeRequestSeq || currentDetailStore !== s) return; // 已切換門市／模式，丟棄過期結果
      updateRouteDisplay(s, result);
      if (result && result.success && result.polyline) drawPolylineOnMap(result, orig);
      else clearActiveRoute();
    } catch (err) {
      if (seq !== routeRequestSeq) return;
      updateRouteDisplay(s, { success: false, error: err.message });
      clearActiveRoute();
    }
  }
  // Initialize dropdown selection state
  const selOrigin = document.getElementById("selRouteOrigin");
  if (selOrigin) {
    if (customRouteOrigin) {
      let optCustom = selOrigin.querySelector('option[value="custom"]');
      if (optCustom) {
        optCustom.disabled = false;
        optCustom.textContent = customRouteOrigin.name;
      }
      selOrigin.value = "custom";
    } else {
      selOrigin.value = selectedOriginPresetId;
    }

    selOrigin.onchange = () => {
      const val = selOrigin.value;
      if (val === "gps") {
        customRouteOrigin = null;
        selectedOriginPresetId = "gps";
        if (!userLocation) {
          getUserLocation();
        }
      } else if (ROUTE_ORIGIN_PRESETS[val]) {
        customRouteOrigin = null;
        selectedOriginPresetId = val;
      }
      updateRouteDisplay(s);
      fetchAndApplyRoute();
    };
  }

  // GPS Locate Button
  const btnRelocate = document.getElementById("btnRelocateGps");
  const btnHintLocate = document.getElementById("btnHintLocate");
  if (btnHintLocate && btnRelocate) btnHintLocate.onclick = () => btnRelocate.onclick();
  if (btnRelocate) {
    btnRelocate.onclick = () => {
      customRouteOrigin = null;
      selectedOriginPresetId = "gps";
      if (selOrigin) selOrigin.value = "gps";
      if (!userLocation) {
        getUserLocation();
      }
      updateRouteDisplay(s);
      fetchAndApplyRoute();
    };
  }

  // Map Pick Button
  const btnPick = document.getElementById("btnPickOriginOnMap");
  if (btnPick) {
    btnPick.onclick = () => {
      if (isMapPickingOrigin) {
        isMapPickingOrigin = false;
        btnPick.classList.remove("picking");
        document.getElementById("lblPickOrigin").textContent = "在地圖上點選";
        map.getContainer().style.cursor = "";
        return;
      }
      isMapPickingOrigin = true;
      btnPick.classList.add("picking");
      document.getElementById("lblPickOrigin").textContent = "請點地圖（再按取消）";
      map.getContainer().style.cursor = "crosshair";

      map.once("click", (e) => {
        isMapPickingOrigin = false;
        btnPick.classList.remove("picking");
        const lblPick = document.getElementById("lblPickOrigin");
        if (lblPick) lblPick.textContent = "在地圖上點選";
        map.getContainer().style.cursor = "";

        customRouteOrigin = {
          id: "custom",
          name: "地圖選點",
          lat: e.latlng.lat,
          lng: e.latlng.lng
        };

        if (selOrigin) {
          let optCustom = selOrigin.querySelector('option[value="custom"]');
          if (optCustom) {
            optCustom.disabled = false;
            optCustom.textContent = customRouteOrigin.name;
          }
          selOrigin.value = "custom";
        }

        updateRouteDisplay(s);
        fetchAndApplyRoute();
      });
    };
  }

  // Mode Switcher Buttons
  box.querySelectorAll(".btn-route-mode").forEach(btn => {
    btn.onclick = () => {
      box.querySelectorAll(".btn-route-mode").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentRouteMode = btn.dataset.mode;
      const depRow = document.getElementById("routeDepartureRow");
      if (depRow) depRow.hidden = currentRouteMode !== "transit";
      updateRouteDisplay(s);
      fetchAndApplyRoute();
    };
  });

  const selDeparture = document.getElementById("selRouteDeparture");
  if (selDeparture) {
    selDeparture.onchange = () => {
      routeDeparture = selDeparture.value;
      fetchAndApplyRoute();
    };
  }

  // 只在「路線」分頁開啟時才呼叫 API（避免每次點門市都計費）
  runRouteFetch = () => fetchAndApplyRoute();
  updateRouteDisplay(s);
}

// 結束門市詳情、回到清單（不收起面板）
function closeStoreDrawer() {
  if (isMobileLayout() && (sheetState === "route" || sheetState === "preview")) setSheet("half");
  document.getElementById("sidebarDetailSection").style.display = "none";
  const listSection = document.getElementById("sidebarListSection");
  listSection.style.display = "flex";
  currentDetailStore = null;
  detailHistory = [];

  if (bufferCircle) {
    map.removeLayer(bufferCircle);
    bufferCircle = null;
  }
  clearActiveRoute();

  // 回到剛才的清單捲動位置，並讓選取的門市保持反白
  requestAnimationFrame(() => {
    if (isMobileLayout()) listSection.scrollTop = listScrollBeforeDetail;
    else document.getElementById("storeList").scrollTop = listScrollBeforeDetail;
  });
}

// ‹ 返回：有上一間門市就回到它（原本的分頁），否則回到門市清單；面板保持開啟
function goBackInDrawer() {
  const prev = detailHistory.pop();
  if (prev) {
    selectStore("s" + prev.s.n, prev.s, false);
    map.panTo([prev.s.lat, prev.s.lng]);
    openStoreDrawer(prev.s, prev.tab, { keepHistory: true });
    return;
  }
  if (isSidebarCollapsed) expandSidebar();
  closeStoreDrawer();
}

// × 關閉：結束查看並收起面板回到地圖（桌機收起側欄、手機收成右下角按鈕）
function dismissStoreDrawer() {
  closeStoreDrawer();
  selectedKey = null;
  document.querySelectorAll(".store-card.selected").forEach(c => c.classList.remove("selected"));
  applyMarkerMode();
  if (isMobileLayout()) setSheet("hidden");
  else if (!isSidebarCollapsed) collapseSidebar();
}

document.getElementById("btnBackToList").onclick = goBackInDrawer;
const btnCloseDetail = document.getElementById("btnCloseDetailDrawer");
if (btnCloseDetail) btnCloseDetail.onclick = dismissStoreDrawer;

function copyStoreAddress(addr) {
  const toast = document.getElementById("toastMsg");
  const showToast = (text) => {
    if (text) toast.textContent = text;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2000);
  };
  // 非 HTTPS、內嵌頁面或使用者拒絕權限時 Clipboard API 會失敗，改用選取文字的舊方法
  const fallback = () => {
    const ta = document.createElement("textarea");
    ta.value = addr;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;opacity:0;top:0;left:0";
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand("copy"); } catch (e) {}
    ta.remove();
    showToast(ok ? "已複製地址" : "無法自動複製，請長按地址手動複製");
  };
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(addr).then(() => showToast("已複製地址"), fallback);
  } else {
    fallback();
  }
}

/* ─── SCHEME 4: SIDEBAR COLLAPSE / EXPAND ─── */
function collapseSidebar() {
  isSidebarCollapsed = true;
  const aside = document.getElementById("mainSidebar");
  aside.classList.add("collapsed");
  document.getElementById("btnOpenSidebar").style.display = "inline-flex";
  setTimeout(() => { map.invalidateSize({ pan: false }); }, 320);
}

function expandSidebar() {
  isSidebarCollapsed = false;
  const aside = document.getElementById("mainSidebar");
  aside.classList.remove("collapsed");
  document.getElementById("btnOpenSidebar").style.display = "none";
  // 不重新置中（原本 invalidateSize 會把整張地圖往左推，造成點門市時的跳動）；
  // 只有選取的門市被展開的側欄蓋住時，才平移最小距離
  setTimeout(() => {
    map.invalidateSize({ pan: false });
    if (currentDetailStore) {
      const pt = map.latLngToContainerPoint([currentDetailStore.lat, currentDetailStore.lng]);
      const w = map.getSize().x;
      if (pt.x > w - 40) map.panBy([pt.x - (w - 80), 0]);
    }
  }, 320);
}

document.getElementById("btnCollapseSidebar").onclick = collapseSidebar;
document.getElementById("btnOpenSidebar").onclick = expandSidebar;

/* ─── SCHEME 2: MAP VIEWPORT SYNC ─── */
function onMapViewportChange() {
  if (isViewportSync) {
    render();
  }
}

document.getElementById("chkViewportSync").addEventListener("change", e => {
  isViewportSync = e.target.checked;
  if (isViewportSync) {
    map.on("moveend", onMapViewportChange);
    map.on("zoomend", onMapViewportChange);
  } else {
    map.off("moveend", onMapViewportChange);
    map.off("zoomend", onMapViewportChange);
  }
  render();
});

/* ─── STORE MAP FOCUS & COMPETITOR NAVIGATION ─── */
function ensureStoreMarkerOnMap(s) {
  const key = "s" + s.n;
  // 大頭針是延後建立的：一律從快取取，避免同一間店出現兩個 marker
  if (!markers[key]) markers[key] = getCachedMarker(s, false);
  const mk = markers[key];
  if (!map.hasLayer(mk) && !(markerClusterLayer && markerClusterLayer.hasLayer(mk))) mk.addTo(map);
  return markers[key];
}

// 地圖定位：把地圖移到這間門市並放大（不再彈出地圖卡片）；手機把抽屜降到預覽高度露出地圖
function focusCurrentDrawerStore() {
  if (!currentDetailStore) return;
  const s = currentDetailStore;
  const key = "s" + s.n;
  const mk = ensureStoreMarkerOnMap(s);
  Object.values(markers).forEach(m => m.setZIndexOffset(0));
  if (mk) mk.setZIndexOffset(3500);
  const z = Math.max(map.getZoom(), 16);
  if (isMobileLayout()) {
    setSheet("preview");
    mobileFlyInProgress = true;
    map.once("moveend", () => { mobileFlyInProgress = false; });
    map.flyTo(visibleCenterFor(s.lat, s.lng, z, "preview"), z, { duration: 0.8 });
  } else {
    map.flyTo([s.lat, s.lng], z, { duration: 0.8 });
  }
  setTimeout(() => { if (markers[key]) markers[key].setZIndexOffset(3500); }, 850);
}

function navigateToCompetitor(n) {
  const target = ALL_STORES.find(i => i.n === n);
  if (!target) return;

  let filterChanged = false;
  if (activeBrands.size && !activeBrands.has(target.brand)) {
    activeBrands.clear();
    filterChanged = true;
  }
  const qInput = document.getElementById("q");
  if (qInput && qInput.value.trim()) {
    const q = qInput.value.trim().toLowerCase();
    const haystack = `${target.brand} ${target.store_name} ${target.city} ${target.district || ""} ${target.address}`.toLowerCase();
    if (!haystack.includes(q)) {
      qInput.value = "";
      filterChanged = true;
    }
  }

  if (filterChanged) {
    render();
  }

  const key = "s" + target.n;
  const mk = ensureStoreMarkerOnMap(target);
  Object.values(markers).forEach(m => m.setZIndexOffset(0));
  if (mk) mk.setZIndexOffset(3500);

  selectedKey = key;
  applyMarkerMode();
  map.flyTo([target.lat, target.lng], Math.max(map.getZoom(), 16), { duration: 0.8 });

  openStoreDrawer(target, "info", { pushHistory: true });
}

/* ─── SELECT STORE ─── */
function selectStore(key, s, flyTo) {
  const prevKey = selectedKey;
  selectedKey = key;
  if (prevKey !== key) applyMarkerMode();

  document.querySelectorAll(".store-card").forEach(c =>
    c.classList.toggle("selected", c.dataset.key === key));
  document.querySelectorAll("#tblBody tr").forEach(r => {
    r.style.background = (r.dataset.key === key) ? "#EBF4FC" : "";
  });

  ensureListBuiltUntil(key);
  const cardEl = document.querySelector(`[data-key="${key}"]`);
  if (cardEl) cardEl.scrollIntoView({ block: "nearest", behavior: "smooth" });

  if (flyTo) {
    const mk = ensureStoreMarkerOnMap(s);
    Object.values(markers).forEach(m => m.setZIndexOffset(0));
    if (mk) mk.setZIndexOffset(3500);

    if (isMobileLayout()) {
      const z = Math.max(map.getZoom(), 15);
      mobileFlyInProgress = true;
      map.once("moveend", () => { mobileFlyInProgress = false; });
      map.flyTo(visibleCenterFor(s.lat, s.lng, z, "half"), z, { duration: 0.8 });
    } else {
      map.flyTo([s.lat, s.lng], Math.max(map.getZoom(), 16), { duration: 0.8 });
    }
    setTimeout(() => { if (markers[key]) markers[key].setZIndexOffset(3500); }, 850);
  }
}

/* ─── BASE MAP SWITCHING & DOCK INTERACTIONS ─── */
const styleLabels = {
  mono: "Google 淺灰",
  satellite: "Google 衛星",
  color: "Google 彩色"
};

function setBaseTile(type) {
  map.removeLayer(currentTile);
  currentTile = TILE_LAYERS[type];
  currentTile.addTo(map);

  document.getElementById("btnTileMono").classList.toggle("active", type === "mono");
  document.getElementById("btnTileSatellite").classList.toggle("active", type === "satellite");
  document.getElementById("btnTileColor").classList.toggle("active", type === "color");

  const lbl = document.getElementById("lblPillActiveStyle");
  if (lbl) lbl.textContent = styleLabels[type] || "底圖風格";
}

document.getElementById("btnTileMono").onclick = () => setBaseTile("mono");
document.getElementById("btnTileSatellite").onclick = () => setBaseTile("satellite");
document.getElementById("btnTileColor").onclick = () => setBaseTile("color");

const mapControlsDock = document.getElementById("mapControlsDock");
const btnToggleMapControls = document.getElementById("btnToggleMapControls");
const btnCloseMapStyle = document.getElementById("btnCloseMapStyle");

if (btnToggleMapControls && mapControlsDock) {
  btnToggleMapControls.onclick = (e) => {
    e.stopPropagation();
    mapControlsDock.classList.toggle("open");
  };
}

if (btnCloseMapStyle && mapControlsDock) {
  btnCloseMapStyle.onclick = (e) => {
    e.stopPropagation();
    mapControlsDock.classList.remove("open");
  };
}

document.addEventListener("click", (e) => {
  if (mapControlsDock && !mapControlsDock.contains(e.target)) {
    mapControlsDock.classList.remove("open");
  }
});

document.getElementById("chkGrayscale").onchange = (e) => {
  document.getElementById("map").classList.toggle("mono-grayscale", e.target.checked);
};

document.getElementById("chkContrast").onchange = (e) => {
  highContrastPins = e.target.checked;
  renderMarkers();
};

/* ─── KEYBOARD NAVIGATION (Section 4) ─── */
window.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    const q = document.getElementById("q");
    q.focus();
    q.select();
  } else if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "SELECT") {
    e.preventDefault();
    const q = document.getElementById("q");
    q.focus();
    q.select();
  } else if (e.key === "Escape") {
    if (currentDetailStore) {
      goBackInDrawer();
    } else {
      const q = document.getElementById("q");
      if (q && q.value) {
        q.value = "";
        render();
      }
    }
  }
});

/* ─── RESET ALL FILTERS ─── */
document.querySelectorAll(".dataset-switch-btn").forEach(btn => {
  btn.onclick = async () => {
    activeDatasetMode = btn.dataset.dataset;
    activeBrands.clear();
    if (activeDatasetMode === "supermarket" && !pxmartDataLoaded) {
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = "載入中…";
      try {
        await ensurePxmartData();
      } catch (error) {
        activeDatasetMode = "home";
        alert("全聯門市資料載入失敗，請確認 pxmart_stores_data.js 與儀表板放在同一資料夾後再試一次。");
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    } else if (activeDatasetMode === "ecommerce" && !shopeeDataLoaded) {
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = "載入中…";
      try {
        await ensureShopeeData();
      } catch (error) {
        activeDatasetMode = "home";
        alert("蝦皮門市資料載入失敗，請確認 shopee_stores_data.js 與儀表板放在同一資料夾後再試一次。");
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    }
    initDropdowns();
    if (isTimelineMode) {
      recalculateTimelineBounds();
    }
    render();
  };
});

document.getElementById("btnResetAll").onclick = () => {
  document.getElementById("q").value = "";
  document.getElementById("selCity").value = "";
  document.getElementById("selDistrict").value = "";
  document.getElementById("selChannel").value = "";
  document.getElementById("selStatus").value = "現行營運中";
  activeBrands.clear();
  isSortedByDistance = false;
  if (activeRegionLayer) {
    map.removeLayer(activeRegionLayer);
    activeRegionLayer = null;
  }
  currentActiveRegionKey = "all";
  map.flyTo([23.75, 120.95], 8, { duration: 0.8 });
  document.querySelectorAll(".btn-region-jump").forEach(b => b.classList.remove("active"));
  document.querySelector('.btn-region-jump[data-region="all"]').classList.add("active");
  const btnLocate = document.getElementById("btnLocateMe");
  if (userLocation) {
    btnLocate.querySelector("span").textContent = "我的位置";
    btnLocate.title = "點擊立即回到我的目前所在位置（已定位）";
  } else {
    btnLocate.classList.remove("active");
    btnLocate.querySelector("span").textContent = "離我最近";
    btnLocate.title = "GPS 定位我的位置，依距離遠近排序";
  }
  initDropdowns();
  if (isTimelineMode) {
    recalculateTimelineBounds();
  }
  render();
};

/* ─── EXPORT CSV ─── */
document.getElementById("btnExport").onclick = () => {
  if (!filteredStores.length) { alert("目前篩選結果為空"); return; }
  const headers = ["品牌","門市名稱","門市型態","區域","縣市","行政區","原始地址","精確定位地址","緯度","經度","150公尺內有其他品牌","距離所在位置","狀態分類","重大說明"];
  const rows = filteredStores.map(s => [
    `"${s.brand}"`,`"${s.store_name}"`,`"${s.store_format || s.channel_format}"`,
    `"${s.region}"`,`"${s.city}"`,`"${s.district||""}"`,`"${s.address}"`,
    `"${s.clean_address||s.address}"`,s.lat,s.lng,
    s._isCoLocation ? '"是"' : '"否"',
    s._userDist !== undefined ? `"${formatDist(s._userDist)}"` : '""',
    `"${s.status_category}"`,`"${(s.note||"").replace(/"/g,'""')}"`
  ]);
  const csv = "\uFEFF" + [headers.join(","), ...rows.map(r=>r.join(","))].join("\r\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `taiwan_home_stores_${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
};

/* ─── EVENT HANDLERS ─── */
document.getElementById("q").addEventListener("input", render);
document.getElementById("btnClearSearch").onclick = () => {
  document.getElementById("q").value = "";
  render();
};

document.getElementById("selCity").addEventListener("change", e => {
  const city = e.target.value;
  updateDistrictDropdown(city);
  if (city) {
    const scopedStores = getScopedStorePoolForDropdowns().filter(s => s.city === city);
    const fitList = scopedStores.length > 0 ? scopedStores : ALL_STORES.filter(s => s.city === city);
    if (fitList.length > 0) {
      const b = L.latLngBounds(fitList.map(s => [s.lat, s.lng]));
      map.fitBounds(b, { padding: [50, 50], maxZoom: 13, duration: 0.8 });
    }
  } else {
    map.flyTo([23.75, 120.95], 8, { duration: 0.8 });
  }
  render();
});

document.getElementById("selDistrict").addEventListener("change", e => {
  const dist = e.target.value;
  const city = document.getElementById("selCity").value;
  if (dist && city) {
    const scopedStores = getScopedStorePoolForDropdowns().filter(s => s.city === city && s.district === dist);
    const fitList = scopedStores.length > 0 ? scopedStores : ALL_STORES.filter(s => s.city === city && s.district === dist);
    if (fitList.length > 0) {
      if (fitList.length === 1) {
        map.flyTo([fitList[0].lat, fitList[0].lng], 15, { duration: 0.8 });
      } else {
        const b = L.latLngBounds(fitList.map(s => [s.lat, s.lng]));
        map.fitBounds(b, { padding: [50, 50], maxZoom: 15, duration: 0.8 });
      }
    }
  } else if (!dist && city) {
    const scopedStores = getScopedStorePoolForDropdowns().filter(s => s.city === city);
    const fitList = scopedStores.length > 0 ? scopedStores : ALL_STORES.filter(s => s.city === city);
    if (fitList.length > 0) {
      const b = L.latLngBounds(fitList.map(s => [s.lat, s.lng]));
      map.fitBounds(b, { padding: [50, 50], maxZoom: 13, duration: 0.8 });
    }
  }
  render();
});

document.getElementById("selChannel").addEventListener("change", () => {
  initDropdowns();
  render();
});
document.getElementById("selStatus").addEventListener("change", () => {
  initDropdowns();
  render();
});

document.getElementById("vtCards").onclick = () => {
  viewMode = "cards";
  document.getElementById("vtCards").classList.add("active");
  document.getElementById("vtTable").classList.remove("active");
  renderList();
};
document.getElementById("vtTable").onclick = () => {
  viewMode = "table";
  document.getElementById("vtTable").classList.add("active");
  document.getElementById("vtCards").classList.remove("active");
  renderList();
};

/* ════════════════════════════════════════════
   SCHEME A: TIMELINE & EXPANSION PLAYER (歷年展店時序演變)
════════════════════════════════════════════ */
let isTimelineMode = false;
let timelineYear = 2026;
const TIMELINE_LAST_YEAR = Math.max(new Date().getFullYear(), ...ALL_STORES.map(s => s.opened_year || 0));
let timelineMinYear = 1996;
let timelineMaxYear = TIMELINE_LAST_YEAR;

// 時間軸刻度：依目前起訖年份平均取 5～6 個
function renderTimelineTicks() {
  const el = document.querySelector(".tl-ticks");
  if (!el) return;
  const span = timelineMaxYear - timelineMinYear;
  const n = Math.min(5, span);
  const years = [];
  for (let i = 0; i <= n; i++) years.push(Math.round(timelineMinYear + span * i / n));
  el.innerHTML = [...new Set(years)].map(y => `<span>${y}</span>`).join("");
}
let isTimelineCumulative = true;
let timelinePlaying = false;
let timelineTimer = null;
let timelineSpeed = 800;
let savedSidebarBeforeTimeline = false;

function openTimelineMode() {
  if (isTimelineMode) return;
  isTimelineMode = true;
  document.body.classList.add("timeline-mode-active");
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.classList.add("active");
  const panel = document.getElementById("timelinePlayerPanel");
  if (panel) panel.classList.add("active");

  // Auto collapse sidebar for focused immersive map exploration
  savedSidebarBeforeTimeline = !isSidebarCollapsed;
  if (!isSidebarCollapsed) {
    collapseSidebar();
  }

  // Determine min & max years based on current filtered pool
  recalculateTimelineBounds();
  const pool = getTimelineStorePool();
  renderTimelineSparkline(pool);
  updateTimeline(timelineYear, false);
}

function recalculateTimelineBounds() {
  const pool = getTimelineStorePool();
  // 起點＝目前篩選（品牌、縣市等）中最早開店的年份，不同品牌不必都從最早的年份開始
  const prevMin = timelineMinYear;
  let validYears = pool.map(s => s.opened_year).filter(y => y >= 1980 && y <= TIMELINE_LAST_YEAR);
  timelineMinYear = validYears.length ? Math.min(...validYears) : TIMELINE_LAST_YEAR - 10;
  timelineMaxYear = TIMELINE_LAST_YEAR;
  if (timelineMaxYear - timelineMinYear < 2) timelineMinYear = timelineMaxYear - 2;
  // 起點往後移（換成較晚開店的品牌）時，目前年份跟著移到新起點
  if (timelineMinYear > prevMin && timelineYear < timelineMinYear) timelineYear = timelineMinYear;
  renderTimelineTicks();

  const slider = document.getElementById("tlRangeSlider");
  if (slider) {
    slider.min = timelineMinYear;
    slider.max = timelineMaxYear;
    if (timelineYear < timelineMinYear) timelineYear = timelineMinYear;
    if (timelineYear > timelineMaxYear) timelineYear = timelineMaxYear;
    slider.value = timelineYear;
  }
}

function closeTimelineMode() {
  if (!isTimelineMode) return;
  pauseTimeline();
  isTimelineMode = false;
  document.body.classList.remove("timeline-mode-active");
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.classList.remove("active");
  const panel = document.getElementById("timelinePlayerPanel");
  if (panel) panel.classList.remove("active");

  // Restore sidebar state
  if (savedSidebarBeforeTimeline && isSidebarCollapsed) {
    expandSidebar();
  }

  // Restore normal markers and list
  render();
}

function toggleTimelineMode() {
  if (isTimelineMode) {
    closeTimelineMode();
  } else {
    openTimelineMode();
  }
}

function getTimelineStorePool() {
  const allowedBrands = DATASET_BRANDS[activeDatasetMode] || [];
  const statEl = document.getElementById("selStatus");
  const stat = statEl ? statEl.value : "";
  const chanEl = document.getElementById("selChannel");
  const chan = chanEl ? chanEl.value : "";
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const qEl = document.getElementById("q");
  const q = qEl ? qEl.value.trim().toLowerCase() : "";

  return ALL_STORES.filter(s => {
    if (!allowedBrands.includes(s.brand)) return false;
    if (activeBrands.size && !activeBrands.has(s.brand)) return false;
    if (stat && s.status_category !== stat) return false;
    if (chan && (s.store_format || s.channel_format) !== chan) return false;
    if (city && s.city !== city) return false;
    if (dist && s.district !== dist) return false;
    if (q) {
      const match = (s.store_name && s.store_name.toLowerCase().includes(q)) ||
                    (s.brand && s.brand.toLowerCase().includes(q)) ||
                    (s.address && s.address.toLowerCase().includes(q)) ||
                    (s.district && s.district.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });
}

function renderTimelineSparkline(pool) {
  const wrap = document.getElementById("tlSparklineWrap");
  if (!wrap) return;
  wrap.innerHTML = "";

  const countsByYear = {};
  for (let y = timelineMinYear; y <= timelineMaxYear; y++) {
    countsByYear[y] = 0;
  }
  pool.forEach(s => {
    const yr = s.opened_year;
    if (yr && yr >= timelineMinYear && yr <= timelineMaxYear) {
      countsByYear[yr] = (countsByYear[yr] || 0) + 1;
    }
  });

  const maxCnt = Math.max(1, ...Object.values(countsByYear));

  for (let y = timelineMinYear; y <= timelineMaxYear; y++) {
    const cnt = countsByYear[y] || 0;
    const bar = document.createElement("div");
    bar.className = "tl-spark-bar" + (y === timelineYear ? " active" : (y < timelineYear ? " past" : ""));
    bar.dataset.year = y;
    bar.title = `${y} 年: 新增 ${cnt} 間`;
    const heightPct = Math.max(8, Math.round((cnt / maxCnt) * 100));
    bar.style.height = `${heightPct}%`;
    bar.onclick = () => {
      pauseTimeline();
      updateTimeline(y, true);
    };
    wrap.appendChild(bar);
  }
}

function updateTimeline(year, triggerPulse = true) {
  timelineYear = parseInt(year);
  const slider = document.getElementById("tlRangeSlider");
  if (slider && parseInt(slider.value) !== timelineYear) {
    slider.value = timelineYear;
  }
  const curYearLabel = document.getElementById("tlCurrentYear");
  if (curYearLabel) curYearLabel.textContent = timelineYear;

  // Update scope label
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const scopeTextEl = document.getElementById("tlScopeText");
  if (scopeTextEl) {
    scopeTextEl.textContent = dist ? `${city} ${dist}` : (city || "全台門市");
  }

  const pool = getTimelineStorePool();
  // 開幕年份查無可靠來源的門市不放進時間軸（不推估年份）
  const openedSoFar = pool.filter(s => s.opened_year && s.opened_year <= timelineYear);
  const newlyOpenedInYear = pool.filter(s => s.opened_year === timelineYear);
  const unknownCnt = pool.filter(s => !s.opened_year).length;
  const unknownNote = document.getElementById("tlUnknownNote");
  if (unknownNote) {
    unknownNote.hidden = !unknownCnt;
    unknownNote.textContent = `另 ${unknownCnt.toLocaleString()} 間開幕年份未知`;
    unknownNote.title = "查無可靠開幕日期來源的門市不列入時間軸（不推估年份）";
  }

  const cumCntEl = document.getElementById("tlCumulativeCount");
  if (cumCntEl) {
    cumCntEl.textContent = isTimelineCumulative ? openedSoFar.length : newlyOpenedInYear.length;
  }

  const newBadge = document.getElementById("tlNewInYearBadge");
  if (newBadge) {
    newBadge.textContent = `+${newlyOpenedInYear.length} 新增`;
    newBadge.style.display = newlyOpenedInYear.length > 0 ? "inline-block" : "none";
  }

  // Update sparkline visual states
  const bars = document.querySelectorAll(".tl-spark-bar");
  bars.forEach(b => {
    const y = parseInt(b.dataset.year);
    b.classList.toggle("active", y === timelineYear);
    b.classList.toggle("past", y < timelineYear);
  });

  // Filter stores on map
  filteredStores = isTimelineCumulative ? openedSoFar : newlyOpenedInYear;

  // Render markers with pulse for newly opened stores in this year
  renderMarkers(triggerPulse ? timelineYear : null);
  renderList();
}

function playTimeline() {
  if (timelinePlaying) return;
  if (timelineYear >= timelineMaxYear) {
    timelineYear = timelineMinYear;
  }
  timelinePlaying = true;
  const playIcon = document.getElementById("tlPlayIcon");
  const pauseIcon = document.getElementById("tlPauseIcon");
  if (playIcon) playIcon.style.display = "none";
  if (pauseIcon) pauseIcon.style.display = "block";

  timelineTimer = setInterval(() => {
    if (timelineYear >= timelineMaxYear) {
      pauseTimeline();
      return;
    }
    timelineYear++;
    updateTimeline(timelineYear, true);
  }, timelineSpeed);
}

function pauseTimeline() {
  timelinePlaying = false;
  if (timelineTimer) {
    clearInterval(timelineTimer);
    timelineTimer = null;
  }
  const playIcon = document.getElementById("tlPlayIcon");
  const pauseIcon = document.getElementById("tlPauseIcon");
  if (playIcon) playIcon.style.display = "block";
  if (pauseIcon) pauseIcon.style.display = "none";
}

function toggleTimelinePlay() {
  if (timelinePlaying) pauseTimeline();
  else playTimeline();
}

function initTimelineUI() {
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.onclick = toggleTimelineMode;

  const closeBtn = document.getElementById("btnCloseTimeline");
  if (closeBtn) closeBtn.onclick = closeTimelineMode;

  const playBtn = document.getElementById("tlBtnPlay");
  if (playBtn) playBtn.onclick = toggleTimelinePlay;

  const slider = document.getElementById("tlRangeSlider");
  if (slider) {
    let sliderRaf = null;
    slider.addEventListener("input", (e) => {
      pauseTimeline();
      const targetVal = e.target.value;
      if (sliderRaf) cancelAnimationFrame(sliderRaf);
      sliderRaf = requestAnimationFrame(() => {
        updateTimeline(targetVal, false);
      });
    });
  }

  const cumToggle = document.getElementById("tlCumulativeToggle");
  if (cumToggle) {
    cumToggle.addEventListener("change", (e) => {
      isTimelineCumulative = e.target.checked;
      updateTimeline(timelineYear, false);
    });
  }

  document.querySelectorAll(".tl-speed-btn").forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll(".tl-speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      timelineSpeed = parseInt(btn.dataset.speed);
      if (timelinePlaying) {
        pauseTimeline();
        playTimeline();
      }
    };
  });
}

/* ─── INITIAL BOOT ─── */
initDropdowns();
initBrandPills();
initRegionJumpBar();
initTimelineUI();
render();
