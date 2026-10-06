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

