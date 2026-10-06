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

