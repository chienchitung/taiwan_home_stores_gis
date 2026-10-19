/* ─── MAP INITIALIZATION ─── */
const map = L.map("map", { zoomControl: false, attributionControl: false });
map.on("zoomend load", () => syncMarkerOverviewMode());
// 手機版初始就用 zoom 7（之後 fitBounds 只微調中心），避免先抓一批 zoom 8 圖磚又整批換掉
map.setView([23.75, 120.95], window.matchMedia("(max-width: 768px)").matches ? 7 : 8);

/* ─── GOOGLE MAPS NAVIGATION CONTROLS (My Location + Zoom In/Out) ─── */
const googleNavControl = L.control({ position: "bottomleft" });
googleNavControl.onAdd = function(map) {
  const container = L.DomUtil.create("div", "google-nav-control-group");
  container.innerHTML = `
    <button class="btn-google-locate" id="btnMapRecenter" title="置中：縮放到目前篩選的門市（未篩選時回到全台）" role="button" aria-label="地圖置中">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 15H3v4c0 1.1.9 2 2 2h4v-2H5v-4zM5 5h4V3H5c-1.1 0-2 .9-2 2v4h2V5zm14-2h-4v2h4v4h2V5c0-1.1-.9-2-2-2zm0 16h-4v2h4c1.1 0 2-.9 2-2v-4h-2v4zM12 9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
    </button>
    <button class="btn-google-locate" id="btnMapLocate" title="顯示我的位置 (回到所在座標)" role="button" aria-label="顯示我的位置">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3A8.994 8.994 0 0 0 13 3.06V1h-2v2.06A8.994 8.994 0 0 0 3.06 11H1v2h2.06A8.994 8.994 0 0 0 11 20.94V23h2v-2.06A8.994 8.994 0 0 0 20.94 13H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
    </button>
    <div class="google-zoom-box">
      <button class="btn-google-zoom" id="btnMapZoomIn" title="放大地圖" role="button" aria-label="放大地圖">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
      </button>
      <div class="google-zoom-divider"></div>
      <button class="btn-google-zoom" id="btnMapZoomOut" title="縮小地圖" role="button" aria-label="縮小地圖">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 13H5v-2h14v2z"/></svg>
      </button>
    </div>
    <button class="btn-google-locate" id="btnScreenshotMode" title="截圖模式：隱藏所有按鈕與面板，只留地圖（按 Esc 結束）" role="button" aria-label="截圖模式">
      <svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 2 7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8.2A3.2 3.2 0 1 0 12 15.2 3.2 3.2 0 1 0 12 8.8z"/></svg>
    </button>
  `;
  L.DomEvent.disableClickPropagation(container);
  L.DomEvent.disableScrollPropagation(container);
  return container;
};
googleNavControl.addTo(map);

const mapLocateBtn = document.getElementById("btnMapLocate");
if (mapLocateBtn) {
  mapLocateBtn.onclick = (e) => {
    e.stopPropagation();
    locateUser();
  };
}
const recenterBtn = document.getElementById("btnMapRecenter");
if (recenterBtn) {
  recenterBtn.onclick = (e) => {
    e.stopPropagation();
    recenterMap();
  };
}
const zoomInBtn = document.getElementById("btnMapZoomIn");
if (zoomInBtn) {
  zoomInBtn.onclick = (e) => {
    e.stopPropagation();
    map.zoomIn();
  };
}
const zoomOutBtn = document.getElementById("btnMapZoomOut");
if (zoomOutBtn) {
  zoomOutBtn.onclick = (e) => {
    e.stopPropagation();
    map.zoomOut();
  };
}

let currentTile = TILE_LAYERS.mono;
currentTile.addTo(map);

