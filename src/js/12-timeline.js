/* ════════════════════════════════════════════
   SCHEME A: TIMELINE & EXPANSION PLAYER (歷年展店時序演變)
════════════════════════════════════════════ */
let isTimelineMode = false;
let timelineYear = 2026;
const TIMELINE_LAST_YEAR = Math.max(new Date().getFullYear(), ...ALL_STORES.map(s => s.opened_year || 0));
let timelineMinYear = 1996;
let timelineMaxYear = TIMELINE_LAST_YEAR;

// 時間軸刻度：依目前起訖年份平均取 5～6 個
function renderTimelineTicks() {
  const el = document.querySelector(".tl-ticks");
  if (!el) return;
  const span = timelineMaxYear - timelineMinYear;
  const n = Math.min(5, span);
  const years = [];
  for (let i = 0; i <= n; i++) years.push(Math.round(timelineMinYear + span * i / n));
  el.innerHTML = [...new Set(years)].map(y => `<span>${y}</span>`).join("");
}
let isTimelineCumulative = true;
let timelinePlaying = false;
let timelineTimer = null;
let timelineSpeed = 800;
let savedSidebarBeforeTimeline = false;

function openTimelineMode() {
  if (isTimelineMode) return;
  isTimelineMode = true;
  document.body.classList.add("timeline-mode-active");
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.classList.add("active");
  const panel = document.getElementById("timelinePlayerPanel");
  if (panel) panel.classList.add("active");

  // Auto collapse sidebar for focused immersive map exploration
  savedSidebarBeforeTimeline = !isSidebarCollapsed;
  if (!isSidebarCollapsed) {
    collapseSidebar();
  }

  // Determine min & max years based on current filtered pool
  recalculateTimelineBounds();
  const pool = getTimelineStorePool();
  renderTimelineSparkline(pool);
  updateTimeline(timelineYear, false);
}

function recalculateTimelineBounds() {
  const pool = getTimelineStorePool();
  // 起點＝目前篩選（品牌、縣市等）中最早開店的年份，不同品牌不必都從最早的年份開始
  const prevMin = timelineMinYear;
  let validYears = pool.map(s => s.opened_year).filter(y => y >= 1980 && y <= TIMELINE_LAST_YEAR);
  timelineMinYear = validYears.length ? Math.min(...validYears) : TIMELINE_LAST_YEAR - 10;
  timelineMaxYear = TIMELINE_LAST_YEAR;
  if (timelineMaxYear - timelineMinYear < 2) timelineMinYear = timelineMaxYear - 2;
  // 起點往後移（換成較晚開店的品牌）時，目前年份跟著移到新起點
  if (timelineMinYear > prevMin && timelineYear < timelineMinYear) timelineYear = timelineMinYear;
  renderTimelineTicks();

  const slider = document.getElementById("tlRangeSlider");
  if (slider) {
    slider.min = timelineMinYear;
    slider.max = timelineMaxYear;
    if (timelineYear < timelineMinYear) timelineYear = timelineMinYear;
    if (timelineYear > timelineMaxYear) timelineYear = timelineMaxYear;
    slider.value = timelineYear;
  }
}

function closeTimelineMode() {
  if (!isTimelineMode) return;
  pauseTimeline();
  isTimelineMode = false;
  document.body.classList.remove("timeline-mode-active");
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.classList.remove("active");
  const panel = document.getElementById("timelinePlayerPanel");
  if (panel) panel.classList.remove("active");

  // Restore sidebar state
  if (savedSidebarBeforeTimeline && isSidebarCollapsed) {
    expandSidebar();
  }

  // Restore normal markers and list
  render();
}

function toggleTimelineMode() {
  if (isTimelineMode) {
    closeTimelineMode();
  } else {
    openTimelineMode();
  }
}

function getTimelineStorePool() {
  const allowedBrands = DATASET_BRANDS[activeDatasetMode] || [];
  const statEl = document.getElementById("selStatus");
  const stat = statEl ? statEl.value : "";
  const chanEl = document.getElementById("selChannel");
  const chan = chanEl ? chanEl.value : "";
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const qEl = document.getElementById("q");
  const q = qEl ? qEl.value.trim().toLowerCase() : "";

  return ALL_STORES.filter(s => {
    if (!allowedBrands.includes(s.brand)) return false;
    if (activeBrands.size && !activeBrands.has(s.brand)) return false;
    if (stat && s.status_category !== stat) return false;
    if (chan && (s.store_format || s.channel_format) !== chan) return false;
    if (city && s.city !== city) return false;
    if (dist && s.district !== dist) return false;
    if (q) {
      const match = (s.store_name && s.store_name.toLowerCase().includes(q)) ||
                    (s.brand && s.brand.toLowerCase().includes(q)) ||
                    (s.address && s.address.toLowerCase().includes(q)) ||
                    (s.district && s.district.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });
}

function renderTimelineSparkline(pool) {
  const wrap = document.getElementById("tlSparklineWrap");
  if (!wrap) return;
  wrap.innerHTML = "";

  const countsByYear = {};
  for (let y = timelineMinYear; y <= timelineMaxYear; y++) {
    countsByYear[y] = 0;
  }
  pool.forEach(s => {
    const yr = s.opened_year;
    if (yr && yr >= timelineMinYear && yr <= timelineMaxYear) {
      countsByYear[yr] = (countsByYear[yr] || 0) + 1;
    }
  });

  const maxCnt = Math.max(1, ...Object.values(countsByYear));

  for (let y = timelineMinYear; y <= timelineMaxYear; y++) {
    const cnt = countsByYear[y] || 0;
    const bar = document.createElement("div");
    bar.className = "tl-spark-bar" + (y === timelineYear ? " active" : (y < timelineYear ? " past" : ""));
    bar.dataset.year = y;
    bar.title = `${y} 年: 新增 ${cnt} 間`;
    const heightPct = Math.max(8, Math.round((cnt / maxCnt) * 100));
    bar.style.height = `${heightPct}%`;
    bar.onclick = () => {
      pauseTimeline();
      updateTimeline(y, true);
    };
    wrap.appendChild(bar);
  }
}

function updateTimeline(year, triggerPulse = true) {
  timelineYear = parseInt(year);
  const slider = document.getElementById("tlRangeSlider");
  if (slider && parseInt(slider.value) !== timelineYear) {
    slider.value = timelineYear;
  }
  const curYearLabel = document.getElementById("tlCurrentYear");
  if (curYearLabel) curYearLabel.textContent = timelineYear;

  // Update scope label
  const city = document.getElementById("selCity").value;
  const dist = document.getElementById("selDistrict").value;
  const scopeTextEl = document.getElementById("tlScopeText");
  if (scopeTextEl) {
    scopeTextEl.textContent = dist ? `${city} ${dist}` : (city || "全台門市");
  }

  const pool = getTimelineStorePool();
  // 開幕年份查無可靠來源的門市不放進時間軸（不推估年份）
  const openedSoFar = pool.filter(s => s.opened_year && s.opened_year <= timelineYear);
  const newlyOpenedInYear = pool.filter(s => s.opened_year === timelineYear);
  const unknownCnt = pool.filter(s => !s.opened_year).length;
  const unknownNote = document.getElementById("tlUnknownNote");
  if (unknownNote) {
    unknownNote.hidden = !unknownCnt;
    unknownNote.textContent = `另 ${unknownCnt.toLocaleString()} 間開幕年份未知`;
    unknownNote.title = "查無可靠開幕日期來源的門市不列入時間軸（不推估年份）";
  }

  const cumCntEl = document.getElementById("tlCumulativeCount");
  if (cumCntEl) {
    cumCntEl.textContent = isTimelineCumulative ? openedSoFar.length : newlyOpenedInYear.length;
  }

  const newBadge = document.getElementById("tlNewInYearBadge");
  if (newBadge) {
    newBadge.textContent = `+${newlyOpenedInYear.length} 新增`;
    newBadge.style.display = newlyOpenedInYear.length > 0 ? "inline-block" : "none";
  }

  // Update sparkline visual states
  const bars = document.querySelectorAll(".tl-spark-bar");
  bars.forEach(b => {
    const y = parseInt(b.dataset.year);
    b.classList.toggle("active", y === timelineYear);
    b.classList.toggle("past", y < timelineYear);
  });

  // Filter stores on map
  filteredStores = isTimelineCumulative ? openedSoFar : newlyOpenedInYear;

  // Render markers with pulse for newly opened stores in this year
  renderMarkers(triggerPulse ? timelineYear : null);
  // 手機時光軸模式下清單整個隱藏，播放時每年重建清單只是白做工，停下來再更新
  if (!(timelinePlaying && isMobileLayout())) renderList();
}

function playTimeline() {
  if (timelinePlaying) return;
  if (timelineYear >= timelineMaxYear) {
    timelineYear = timelineMinYear;
  }
  timelinePlaying = true;
  const playIcon = document.getElementById("tlPlayIcon");
  const pauseIcon = document.getElementById("tlPauseIcon");
  if (playIcon) playIcon.style.display = "none";
  if (pauseIcon) pauseIcon.style.display = "block";

  // 從頭播放時先把第一年畫出來，不要讓地圖停在上一輪的最後一年
  updateTimeline(timelineYear, true);
  scheduleTimelineTick();
}

// 每一年畫完、瀏覽器真的把地圖畫到螢幕上（requestAnimationFrame）之後才排下一年。
// 原本用 setInterval：較慢的手機上每年的繪製時間比間隔長時，計時器會一路排隊、
// 瀏覽器來不及把畫面畫出來，看起來就像播放中地圖沒有點，播完才一次出現。
function scheduleTimelineTick() {
  timelineTimer = setTimeout(() => {
    timelineTimer = null;
    if (!timelinePlaying) return;
    if (timelineYear >= timelineMaxYear) {
      pauseTimeline();
      return;
    }
    timelineYear++;
    updateTimeline(timelineYear, true);
    requestAnimationFrame(() => { if (timelinePlaying) scheduleTimelineTick(); });
  }, timelineSpeed);
}

function pauseTimeline() {
  timelinePlaying = false;
  if (timelineTimer) {
    clearTimeout(timelineTimer);
    timelineTimer = null;
  }
  const playIcon = document.getElementById("tlPlayIcon");
  const pauseIcon = document.getElementById("tlPauseIcon");
  if (playIcon) playIcon.style.display = "block";
  if (pauseIcon) pauseIcon.style.display = "none";
  // 手機播放期間略過清單更新，停下來時補上
  if (isTimelineMode && isMobileLayout()) renderList();
}

function toggleTimelinePlay() {
  if (timelinePlaying) pauseTimeline();
  else playTimeline();
}

function initTimelineUI() {
  const triggerBtn = document.getElementById("btnToggleTimeline");
  if (triggerBtn) triggerBtn.onclick = toggleTimelineMode;

  const closeBtn = document.getElementById("btnCloseTimeline");
  if (closeBtn) closeBtn.onclick = closeTimelineMode;

  const playBtn = document.getElementById("tlBtnPlay");
  if (playBtn) playBtn.onclick = toggleTimelinePlay;

  const slider = document.getElementById("tlRangeSlider");
  if (slider) {
    let sliderRaf = null;
    slider.addEventListener("input", (e) => {
      pauseTimeline();
      const targetVal = e.target.value;
      if (sliderRaf) cancelAnimationFrame(sliderRaf);
      sliderRaf = requestAnimationFrame(() => {
        updateTimeline(targetVal, false);
      });
    });
  }

  const cumToggle = document.getElementById("tlCumulativeToggle");
  if (cumToggle) {
    cumToggle.addEventListener("change", (e) => {
      isTimelineCumulative = e.target.checked;
      updateTimeline(timelineYear, false);
    });
  }

  document.querySelectorAll(".tl-speed-btn").forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll(".tl-speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      timelineSpeed = parseInt(btn.dataset.speed);
      if (timelinePlaying) {
        pauseTimeline();
        playTimeline();
      }
    };
  });
}

