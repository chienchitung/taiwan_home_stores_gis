/* ─── GPS GEOLOCATION ENGINE (P1 Feature: Google Maps-like Location Re-centering) ─── */
function updateLocateButtonsState(state) {
  const sidebarBtn = document.getElementById("btnLocateMe");
  const mapBtn = document.getElementById("btnMapLocate");

  if (state === "loading") {
    if (sidebarBtn) {
      sidebarBtn.classList.add("loading");
      sidebarBtn.querySelector("span").textContent = "定位中…";
    }
    if (mapBtn) {
      mapBtn.classList.add("loading");
      mapBtn.title = "定位中…";
    }
  } else if (state === "active") {
    if (sidebarBtn) {
      sidebarBtn.classList.remove("loading");
      sidebarBtn.classList.add("active");
      sidebarBtn.querySelector("span").textContent = "我的位置";
      sidebarBtn.title = "點擊立即回到我的目前所在位置（已定位）";
    }
    if (mapBtn) {
      mapBtn.classList.remove("loading");
      mapBtn.classList.add("active");
      mapBtn.title = "已定位（點擊立即回歸我的目前位置）";
    }
  } else if (state === "reset") {
    if (sidebarBtn) {
      sidebarBtn.classList.remove("loading");
      sidebarBtn.classList.remove("active");
      sidebarBtn.querySelector("span").textContent = "離我最近";
      sidebarBtn.title = "以目前位置排序全台門市";
    }
    if (mapBtn) {
      mapBtn.classList.remove("loading");
      mapBtn.classList.remove("active");
      mapBtn.title = "顯示我的位置 (回到所在座標)";
    }
  }
}

function locateUser() {
  // If user location is ALREADY known (in memory or session cache):
  // Immediately re-center to user position like Google Maps without ANY browser permission prompts!
  if (userLocation) {
    if (!userLocationMarker) {
      const userIcon = L.divIcon({
        className: "user-gps-pulse-marker",
        html: `<div class="pulse-ring"></div><div class="user-dot"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      userLocationMarker = L.marker([userLocation.lat, userLocation.lng], { icon: userIcon, zIndexOffset: 4000 })
        .addTo(map)
        .bindPopup(`<div style="font-weight:700;padding:4px">您的目前所在位置</div>`);
      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(userLocation.lat, userLocation.lng, s.lat, s.lng);
      });
    }

    map.flyTo([userLocation.lat, userLocation.lng], 14, { duration: 0.8 });
    setTimeout(() => {
      if (userLocationMarker) userLocationMarker.openPopup();
    }, 850);
    updateLocateButtonsState("active");
    if (!isSortedByDistance) {
      isSortedByDistance = true;
      render();
    }
    return;
  }

  // First-time location acquisition
  if (!navigator.geolocation) {
    alert("您的瀏覽器環境不支援地理定位功能");
    return;
  }

  updateLocateButtonsState("loading");

  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude, longitude } = pos.coords;
      userLocation = { lat: latitude, lng: longitude };

      // Cache to sessionStorage to completely avoid permission prompts across reloads
      try {
        sessionStorage.setItem("taiwan_user_lat", String(latitude));
        sessionStorage.setItem("taiwan_user_lng", String(longitude));
      } catch (e) {}

      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(latitude, longitude, s.lat, s.lng);
      });

      if (userLocationMarker) map.removeLayer(userLocationMarker);
      const userIcon = L.divIcon({
        className: "user-gps-pulse-marker",
        html: `<div class="pulse-ring"></div><div class="user-dot"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      userLocationMarker = L.marker([latitude, longitude], { icon: userIcon, zIndexOffset: 4000 })
        .addTo(map)
        .bindPopup(`<div style="font-weight:700;padding:4px">您的目前所在位置</div>`);

      map.flyTo([latitude, longitude], 14, { duration: 0.8 });
      setTimeout(() => {
        if (userLocationMarker) userLocationMarker.openPopup();
      }, 850);

      updateLocateButtonsState("active");
      isSortedByDistance = true;
      render();
    },
    err => {
      updateLocateButtonsState("reset");
      alert("無法取得您的目前位置資訊（請確認已允許瀏覽器定位權限）");
    },
    { timeout: 10000, enableHighAccuracy: true }
  );
}

document.getElementById("btnLocateMe").onclick = locateUser;

// 路線規劃用：只取得定位（不移動地圖、不重排清單），取得後重新計算路線
function getUserLocation() {
  if (!navigator.geolocation) {
    alert("您的瀏覽器環境不支援地理定位功能");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude, longitude } = pos.coords;
      userLocation = { lat: latitude, lng: longitude };
      try {
        sessionStorage.setItem("taiwan_user_lat", String(latitude));
        sessionStorage.setItem("taiwan_user_lng", String(longitude));
      } catch (e) {}
      ALL_STORES.forEach(s => {
        s._userDist = haversineDistanceKm(latitude, longitude, s.lat, s.lng);
      });
      if (currentDetailStore && currentDetailTab === "route" && runRouteFetch) runRouteFetch();
    },
    () => alert("無法取得您的目前位置資訊（請確認已允許瀏覽器定位權限）"),
    { timeout: 10000, enableHighAccuracy: true }
  );
}

