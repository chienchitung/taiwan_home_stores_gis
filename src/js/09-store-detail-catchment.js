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

