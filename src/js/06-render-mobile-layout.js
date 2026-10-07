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
  [".app-logo", "mLogoSlot"],
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

