const https = require("https");

// In-memory cache to avoid duplicate API calls and save quota (TTL: 10 mins)
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

function httpPost(urlStr, headers, bodyObj) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const postData = JSON.stringify(bodyObj);
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: "POST",
      headers: {
        ...headers,
        "Content-Length": Buffer.byteLength(postData)
      },
      timeout: 8000
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => { data += chunk; });
      res.on("end", () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ ok: res.statusCode >= 200 && res.statusCode < 300, status: res.statusCode, json: parsed, raw: data });
        } catch (e) {
          resolve({ ok: false, status: res.statusCode, json: null, raw: data });
        }
      });
    });

    req.on("error", (err) => { reject(err); });
    req.on("timeout", () => {
      req.destroy();
      reject(new Error("Google Routes API 請求超時 (Timeout)"));
    });
    req.write(postData);
    req.end();
  });
}

/**
 * Exclusively calls Google Routes API (computeRoutes)
 * Documentation: https://developers.google.com/maps/documentation/routes
 */
async function fetchGoogleRoutesApi(originLat, originLng, destLat, destLng, mode, apiKey) {
  const travelModeMap = {
    driving: "DRIVE",
    transit: "TRANSIT",
    walking: "WALK"
  };
  const travelMode = travelModeMap[mode] || "DRIVE";

  const requestBody = {
    origin: {
      location: {
        latLng: {
          latitude: originLat,
          longitude: originLng
        }
      }
    },
    destination: {
      location: {
        latLng: {
          latitude: destLat,
          longitude: destLng
        }
      }
    },
    travelMode: travelMode,
    languageCode: "zh-TW",
    computeAlternativeRoutes: false
  };

  if (travelMode === "DRIVE") {
    requestBody.routingPreference = "TRAFFIC_UNAWARE";
  }

  const res = await httpPost(
    "https://routes.googleapis.com/directions/v2:computeRoutes",
    {
      "Content-Type": "application/json",
      "X-Goog-Api-Key": apiKey,
      "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.description"
    },
    requestBody
  );

  if (!res.ok || !res.json || res.json.error) {
    const err = res.json?.error || {};
    const errMsg = [err.status, err.message].filter(Boolean).join(" - ") || res.raw?.slice(0, 200) || `Status ${res.status}`;
    throw new Error(`Google Routes API [${err.status || res.status}]: ${errMsg}`);
  }

  if (!res.json.routes || res.json.routes.length === 0) {
    throw new Error("Google Routes API: 查無可行路線 (NO_ROUTES)");
  }

  const route = res.json.routes[0];
  const durationSec = parseInt(route.duration, 10) || 0;
  const durationMin = Math.round(durationSec / 60);
  const durationText = durationMin < 60
    ? `${durationMin} 分鐘`
    : `${Math.floor(durationMin / 60)} 小時 ${durationMin % 60} 分鐘`;

  const distanceMeters = route.distanceMeters || 0;
  const distanceKm = Math.round((distanceMeters / 1000) * 10) / 10;
  const distanceText = distanceKm < 1 ? `${distanceMeters} 公尺` : `${distanceKm} 公里`;

  return {
    success: true,
    engine: "google",
    mode: mode,
    duration_text: durationText,
    duration_sec: durationSec,
    duration_min: durationMin,
    distance_text: distanceText,
    distance_km: distanceKm,
    polyline: route.polyline ? route.polyline.encodedPolyline : "",
    summary: route.description || (mode === "transit" ? "大眾運輸推薦班次" : (mode === "walking" ? "步行推薦路線" : "開車推薦路徑"))
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
        body: JSON.stringify({ success: false, error: "Missing or invalid coordinate parameters (originLat, originLng, destLat, destLng)" })
      };
    }

    const apiKey = (process.env.GOOGLE_MAPS_API_KEY || "").trim();
    if (!apiKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          success: false,
          error: "未在 Netlify 讀取到 GOOGLE_MAPS_API_KEY 環境變數 (請在 Netlify Site configuration -> Environment variables 設定並觸發 Clear cache and deploy site)"
        })
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

    const result = await fetchGoogleRoutesApi(originLat, originLng, destLat, destLng, mode, apiKey);
    setCache(cacheKey, result);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(result)
    };
  } catch (err) {
    return {
      statusCode: 502,
      headers,
      body: JSON.stringify({
        success: false,
        error: err.message
      })
    };
  }
};
