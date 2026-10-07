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
  if (forcedPin) {
    const inResult = filteredStores.some(s => "s" + s.n === forcedPin.key);
    if (inResult || forcedPin.key !== selectedKey) {
      map.removeLayer(forcedPin.mk);
      forcedPin = null;
    }
  }
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
    pinStores = {}; // 聚合模式不使用延後建立的大頭針清單
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

