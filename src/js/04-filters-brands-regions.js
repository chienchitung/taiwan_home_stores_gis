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

