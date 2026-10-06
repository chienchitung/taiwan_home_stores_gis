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

