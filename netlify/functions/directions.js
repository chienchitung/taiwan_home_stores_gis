const https = require("https");

// Simple in-memory cache to avoid duplicate API calls and save quota (TTL: 10 mins)
const cache = new Map();
const CACHE_TTL_MS = 10 * 60 * 1000;

function getCache(key) {
  const item = cache.get(key);
  if (!item) return null;
  if (Date.now() - item.time > CACHE_TTL_MS) {
    cache.delete(key);
    return null;
  }
  return item.data;
}

function setCache(key, data) {
  if (cache.size > 200) {
    const oldestKey = cache.keys().next().value;
    cache.delete(oldestKey);
  }
  cache.set(key, { time: Date.now(), data });
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = "";
      res.on("data", (chunk) => { data += chunk; });
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error("Failed to parse JSON response: " + e.message));
        }
      });
    }).on("error", (err) => {
      reject(err);
    });
  });
}

async function fetchGoogleDirections(originLat, originLng, destLat, destLng, mode, apiKey) {
  const modeMap = {
    driving: "driving",
    transit: "transit",
    walking: "walking"
  };
  const gMode = modeMap[mode] || "driving";
  const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${originLat},${originLng}&destination=${destLat},${destLng}&mode=${gMode}&language=zh-TW&key=${apiKey}`;

  const json = await httpGet(url);
  if (json.status !== "OK" || !json.routes || json.routes.length === 0) {
    throw new Error(`Google API returned status: ${json.status || "NO_ROUTES"}`);
  }

  const route = json.routes[0];
  const leg = route.legs[0];

  return {
    success: true,
    engine: "google",
    mode: gMode,
    duration_text: leg.duration.text,
    duration_sec: leg.duration.value,
    duration_min: Math.round(leg.duration.value / 60),
    distance_text: leg.distance.text,
    distance_km: Math.round((leg.distance.value / 1000) * 10) / 10,
    polyline: route.overview_polyline ? route.overview_polyline.points : "",
    summary: route.summary || leg.start_address + " -> " + leg.end_address
  };
}

async function fetchOsrmRoute(originLat, originLng, destLat, destLng, mode = "driving") {
  const url = `https://router.project-osrm.org/route/v1/driving/${originLng},${originLat};${destLng},${destLat}?overview=full&geometries=polyline`;

  const json = await httpGet(url);
  if (json.code !== "Ok" || !json.routes || json.routes.length === 0) {
    throw new Error(`OSRM returned code: ${json.code || "NO_ROUTES"}`);
  }

  const route = json.routes[0];
  const distanceKm = Math.round((route.distance / 1000) * 10) / 10;
  
  let durationMin = Math.round(route.duration / 60);
  let summaryText = "開車規劃路徑 (OSRM 備援引擎)";

  if (mode === "walking") {
    durationMin = Math.max(1, Math.round((distanceKm / 4.5) * 60));
    summaryText = "步行路徑估算 (OSRM 備援引擎)";
  } else if (mode === "transit") {
    durationMin = Math.max(5, Math.round((distanceKm / 24) * 60) + 8);
    summaryText = "大眾運輸通勤估算 (OSRM 備援引擎)";
  }

  const durationSec = durationMin * 60;
  const durationText = durationMin < 60 ? `${durationMin} 分鐘` : `${Math.floor(durationMin / 60)} 小時 ${durationMin % 60} 分鐘`;

  return {
    success: true,
    engine: "osrm",
    mode: mode,
    duration_text: durationText,
    duration_sec: durationSec,
    duration_min: durationMin,
    distance_text: `${distanceKm} 公里`,
    distance_km: distanceKm,
    polyline: route.geometry,
    summary: summaryText
  };
}

exports.handler = async function (event, context) {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Content-Type": "application/json; charset=utf-8"
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  try {
    const params = event.queryStringParameters || {};
    const originLat = parseFloat(params.originLat);
    const originLng = parseFloat(params.originLng);
    const destLat = parseFloat(params.destLat);
    const destLng = parseFloat(params.destLng);
    const mode = params.mode || "driving";

    if (isNaN(originLat) || isNaN(originLng) || isNaN(destLat) || isNaN(destLng)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: "Missing or invalid coordinate parameters (originLat, originLng, destLat, destLng)" })
      };
    }

    const cacheKey = `${originLat.toFixed(4)},${originLng.toFixed(4)}_${destLat.toFixed(4)},${destLng.toFixed(4)}_${mode}`;
    const cachedResult = getCache(cacheKey);
    if (cachedResult) {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ ...cachedResult, cached: true })
      };
    }

    const apiKey = process.env.GOOGLE_MAPS_API_KEY;

    if (apiKey) {
      try {
        const googleResult = await fetchGoogleDirections(originLat, originLng, destLat, destLng, mode, apiKey);
        setCache(cacheKey, googleResult);
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify(googleResult)
        };
      } catch (err) {
        console.warn("Google API call failed, falling back to OSRM:", err.message);
      }
    }

    // Free Open Source Routing Machine Fallback
    const osrmResult = await fetchOsrmRoute(originLat, originLng, destLat, destLng, mode);
    setCache(cacheKey, osrmResult);
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(osrmResult)
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: err.message })
    };
  }
};
