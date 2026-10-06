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

