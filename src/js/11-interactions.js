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

