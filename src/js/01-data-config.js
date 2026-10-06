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

