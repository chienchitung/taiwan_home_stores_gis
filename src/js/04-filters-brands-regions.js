/* ─── MULTI-SELECT FACET FILTERS（縣市／行政區／門市型態／營運狀態）─── */
// 同一類內是「或」（台北市或新北市），不同類之間是「且」（且為百貨型門市）。
// 每個選項的數字＝套用「其他類」條件後的門市數；0 間的選項停用（已勾選的除外，方便取消）。
const FACET_DEFAULT_STATUS = "現行營運中";
const filterState = {
  city: new Set(),
  district: new Set(),   // 值為「縣市|行政區」，避免不同縣市的同名行政區（如東區、中正區）混在一起
  channel: new Set(),
  status: new Set([FACET_DEFAULT_STATUS])
};
const FACET_CITY_GROUPS = [
  ["北部", ["台北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "宜蘭縣"]],
  ["中部", ["苗栗縣", "台中市", "彰化縣", "南投縣", "雲林縣"]],
  ["南部", ["嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣"]],
  ["東部", ["花蓮縣", "台東縣"]],
  ["離島", ["澎湖縣", "金門縣", "連江縣"]]
];
const FACET_CHANNEL_OPTIONS = ["大型獨棟／街邊門市", "百貨／購物中心門市", "都會／社區門市", "量販店中店",
  "店中店／專櫃", "子品牌門市", "訂購取貨中心", "期間限定門市"];
const FACET_STATUS_OPTIONS = [["現行營運中", "現行營運中"], ["暫停營業", "暫停營業"], ["歷史變動（已熄燈/遷址）", "已歇業／遷址"]];
const FACET_DISTRICT_MAX_CITIES = 3;   // 選太多縣市時行政區選項會上百個，只在 1～3 個縣市時提供
const FACET_DISTRICT_PREVIEW = 8;      // 每個縣市先列 8 個行政區，其餘收在「顯示更多」
const facetOpen = { status: true, city: true, district: true, channel: false };
const facetDistrictExpanded = new Set();

const storeFormatOf = s => s.store_format || s.channel_format;
const districtKeyOf = s => `${s.city}|${s.district || ""}`;

function isFacetStatusDefault() {
  return filterState.status.size === 1 && filterState.status.has(FACET_DEFAULT_STATUS);
}

// 門市是否符合縣市／行政區／型態／狀態條件；exclude 指定略過哪一類（算該類選項數字用）
function storeMatchesFacets(s, exclude = "") {
  if (exclude !== "city" && filterState.city.size && !filterState.city.has(s.city)) return false;
  if (exclude !== "city" && exclude !== "district" && filterState.district.size) {
    // 只有勾了行政區的縣市才限縮行政區；同時勾選的其他縣市維持全縣市
    const cityHasDistrict = [...filterState.district].some(k => k.startsWith(s.city + "|"));
    if (cityHasDistrict && !filterState.district.has(districtKeyOf(s))) return false;
  }
  if (exclude !== "channel" && filterState.channel.size && !filterState.channel.has(storeFormatOf(s))) return false;
  if (exclude !== "status" && filterState.status.size && !filterState.status.has(s.status_category)) return false;
  return true;
}

// 目前資料集＋已選品牌＋縣市等條件（排除 exclude 那一類）
function getFacetPool(exclude = "") {
  const allowedBrands = DATASET_BRANDS[activeDatasetMode] || [];
  return ALL_STORES.filter(s =>
    allowedBrands.includes(s.brand) &&
    (!activeBrands.size || activeBrands.has(s.brand)) &&
    storeMatchesFacets(s, exclude));
}

// 已套用條件數（營運狀態維持預設「現行營運中」時不算）
function activeFacetCount() {
  return filterState.city.size + filterState.district.size + filterState.channel.size +
    (isFacetStatusDefault() ? 0 : 1);
}

// 清單／時光軸上「範圍」的文字描述
function describeFacetScope(fallback) {
  const cities = [...filterState.city];
  if (!cities.length) return fallback;
  if (cities.length === 1) {
    const dists = [...filterState.district].filter(k => k.startsWith(cities[0] + "|")).map(k => k.split("|")[1]);
    return dists.length ? `${cities[0]} ${dists.slice(0, 3).join("、")}${dists.length > 3 ? ` 等 ${dists.length} 區` : ""}` : cities[0];
  }
  return cities.length <= 3 ? cities.join("、") : `${cities.length} 個縣市`;
}

function resetFacetFilters() {
  filterState.city.clear();
  filterState.district.clear();
  filterState.channel.clear();
  filterState.status = new Set([FACET_DEFAULT_STATUS]);
  facetDistrictExpanded.clear();
}

function countBy(pool, keyFn) {
  const c = {};
  pool.forEach(s => { const k = keyFn(s); if (k) c[k] = (c[k] || 0) + 1; });
  return c;
}

const escAttr = v => String(v).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

function facetOptionHtml(facet, value, label, count, checked) {
  const disabled = !count && !checked;
  return `<label class="facet-opt${disabled ? " is-disabled" : ""}${checked ? " is-checked" : ""}">
    <input type="checkbox" data-facet="${facet}" value="${escAttr(value)}"${checked ? " checked" : ""}${disabled ? " disabled" : ""}>
    <span class="facet-label">${label}</span><span class="facet-cnt">${count || 0}</span>
  </label>`;
}

function facetSectionHtml(facet, title, selCount, body) {
  return `<details class="facet-section" data-facet="${facet}"${facetOpen[facet] ? " open" : ""}>
    <summary><span class="facet-title">${title}${selCount ? `<span class="facet-sel-count">${selCount}</span>` : ""}</span>
      <svg class="facet-chevron" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6-1.41-1.41z"/></svg></summary>
    <div class="facet-body">${body}</div>
  </details>`;
}

function renderFacetPanel() {
  const panel = document.getElementById("facetPanel");
  if (!panel) return;
  // 重畫前記住焦點與捲動位置，勾選後不會跳掉
  const active = document.activeElement;
  const focusKey = active && panel.contains(active) && active.dataset
    ? (active.dataset.facet ? `${active.dataset.facet}::${active.value}` : (active.dataset.action ? `${active.dataset.action}::${active.dataset.arg || ""}` : ""))
    : "";
  const scrollTop = panel.scrollTop;

  // 營運狀態
  const statusCounts = countBy(getFacetPool("status"), s => s.status_category);
  const statusBody = FACET_STATUS_OPTIONS.map(([v, label]) =>
    facetOptionHtml("status", v, label, statusCounts[v], filterState.status.has(v))).join("") +
    (filterState.status.size ? "" : `<div class="facet-hint">未勾選＝顯示全部營運狀態</div>`);

  // 縣市（依地區分組，每組可一次全選）
  const cityCounts = countBy(getFacetPool("city"), s => s.city);
  const knownCities = new Set(FACET_CITY_GROUPS.flatMap(g => g[1]));
  const otherCities = Object.keys(cityCounts).filter(c => !knownCities.has(c));
  const groups = otherCities.length ? [...FACET_CITY_GROUPS, ["其他", otherCities]] : FACET_CITY_GROUPS;
  const cityBody = groups.map(([gName, cities]) => {
    const shown = cities.filter(c => cityCounts[c] || filterState.city.has(c));
    if (!shown.length) return "";
    const selectable = shown.filter(c => cityCounts[c]);
    const allOn = selectable.length && selectable.every(c => filterState.city.has(c));
    return `<div class="facet-group">
      <div class="facet-group-head"><span>${gName}</span>
        <button type="button" class="facet-link" data-action="city-group" data-arg="${gName}">${allOn ? "取消全選" : "全選"}</button></div>
      <div class="facet-grid">${shown.map(c => facetOptionHtml("city", c, c, cityCounts[c], filterState.city.has(c))).join("")}</div>
    </div>`;
  }).join("");

  // 行政區（依已選縣市分組）
  let districtBody;
  const selCities = [...filterState.city];
  if (!selCities.length) {
    districtBody = `<div class="facet-hint">先勾選縣市（最多 ${FACET_DISTRICT_MAX_CITIES} 個）即可選擇行政區</div>`;
  } else if (selCities.length > FACET_DISTRICT_MAX_CITIES) {
    districtBody = `<div class="facet-hint">已選 ${selCities.length} 個縣市；勾選 ${FACET_DISTRICT_MAX_CITIES} 個以內的縣市才能再細分行政區</div>`;
  } else {
    const distCounts = countBy(getFacetPool("district"), s => s.district ? districtKeyOf(s) : "");
    districtBody = selCities.map(city => {
      const keys = Object.keys(distCounts).filter(k => k.startsWith(city + "|"));
      filterState.district.forEach(k => { if (k.startsWith(city + "|") && !keys.includes(k)) keys.push(k); });
      keys.sort((a, b) => (distCounts[b] || 0) - (distCounts[a] || 0));
      if (!keys.length) return "";
      const expanded = facetDistrictExpanded.has(city);
      const visible = expanded ? keys : keys.filter((k, i) => i < FACET_DISTRICT_PREVIEW || filterState.district.has(k));
      const more = keys.length - visible.length;
      return `<div class="facet-group">
        <div class="facet-group-head"><span>${city}</span></div>
        <div class="facet-grid">${visible.map(k => facetOptionHtml("district", k, k.split("|")[1], distCounts[k], filterState.district.has(k))).join("")}</div>
        ${more > 0 ? `<button type="button" class="facet-link facet-more" data-action="district-more" data-arg="${escAttr(city)}">顯示更多（${more}）</button>`
          : (expanded && keys.length > FACET_DISTRICT_PREVIEW ? `<button type="button" class="facet-link facet-more" data-action="district-less" data-arg="${escAttr(city)}">收合</button>` : "")}
      </div>`;
    }).join("");
  }

  // 門市型態
  const chanCounts = countBy(getFacetPool("channel"), storeFormatOf);
  const chanBody = FACET_CHANNEL_OPTIONS
    .filter(v => chanCounts[v] || filterState.channel.has(v))
    .map(v => facetOptionHtml("channel", v, v, chanCounts[v], filterState.channel.has(v))).join("") ||
    `<div class="facet-hint">目前條件下沒有門市</div>`;

  panel.innerHTML =
    facetSectionHtml("status", "營運狀態", isFacetStatusDefault() ? 0 : filterState.status.size, statusBody) +
    facetSectionHtml("city", "縣市", filterState.city.size, cityBody) +
    facetSectionHtml("district", "行政區", filterState.district.size, districtBody) +
    facetSectionHtml("channel", "門市型態", filterState.channel.size, chanBody);

  panel.scrollTop = scrollTop;
  if (focusKey) {
    const [a, b] = focusKey.split("::");
    const el = [...panel.querySelectorAll("input[data-facet], button[data-action]")]
      .find(x => (x.dataset.facet === a && x.value === b) || (x.dataset.action === a && (x.dataset.arg || "") === b));
    if (el) el.focus({ preventScroll: true });
  }
}

// 舊名稱沿用：資料集、品牌、重設等處都會呼叫
function initDropdowns() {
  renderFacetPanel();
}

// 勾選縣市／行政區後，地圖縮放到符合條件的門市
function fitMapToFacetSelection() {
  if (!filterState.city.size) {
    map.flyTo([23.75, 120.95], 8, { duration: 0.8 });
    return;
  }
  let fitList = getFacetPool();
  if (!fitList.length) fitList = ALL_STORES.filter(s => filterState.city.has(s.city));
  if (!fitList.length) return;
  if (fitList.length === 1) {
    map.flyTo([fitList[0].lat, fitList[0].lng], 15, { duration: 0.8 });
    return;
  }
  map.fitBounds(L.latLngBounds(fitList.map(s => [s.lat, s.lng])),
    { padding: [50, 50], maxZoom: filterState.district.size ? 15 : 13, duration: 0.8 });
}

function initFacetPanel() {
  const panel = document.getElementById("facetPanel");
  panel.addEventListener("toggle", e => {
    const sec = e.target.closest && e.target.closest(".facet-section");
    if (sec) facetOpen[sec.dataset.facet] = sec.open;
  }, true);
  panel.addEventListener("change", e => {
    const input = e.target;
    if (!input.dataset || !input.dataset.facet) return;
    const facet = input.dataset.facet;
    const set = filterState[facet];
    if (input.checked) set.add(input.value); else set.delete(input.value);
    if (facet === "city" && !input.checked) {
      // 取消縣市時一併取消該縣市的行政區
      [...filterState.district].forEach(k => { if (k.startsWith(input.value + "|")) filterState.district.delete(k); });
      facetDistrictExpanded.delete(input.value);
    }
    if (facet === "city" || facet === "district") fitMapToFacetSelection();
    render();
  });
  panel.addEventListener("click", e => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;
    e.preventDefault();
    const arg = btn.dataset.arg;
    if (btn.dataset.action === "city-group") {
      const group = FACET_CITY_GROUPS.find(g => g[0] === arg);
      const cityCounts = countBy(getFacetPool("city"), s => s.city);
      const cities = (group ? group[1] : Object.keys(cityCounts)).filter(c => cityCounts[c]);
      const allOn = cities.length && cities.every(c => filterState.city.has(c));
      cities.forEach(c => {
        if (allOn) {
          filterState.city.delete(c);
          [...filterState.district].forEach(k => { if (k.startsWith(c + "|")) filterState.district.delete(k); });
        } else {
          filterState.city.add(c);
        }
      });
      fitMapToFacetSelection();
      render();
    } else if (btn.dataset.action === "district-more") {
      facetDistrictExpanded.add(arg);
      renderFacetPanel();
    } else if (btn.dataset.action === "district-less") {
      facetDistrictExpanded.delete(arg);
      renderFacetPanel();
    }
  });
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
  const statusSet = filterState.status;
  const statusLabel = statusSet.size
    ? FACET_STATUS_OPTIONS.filter(([v]) => statusSet.has(v)).map(o => o[1]).join("、")
    : "全部狀態";
  const totalStoresInRegion = ALL_STORES.filter(s =>
    reg.cities.includes(s.city) && (!statusSet.size || statusSet.has(s.status_category))
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

