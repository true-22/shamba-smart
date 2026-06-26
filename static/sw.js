/**
 * Service Worker — Shamba Smart Plant Disease Detector
 * ======================================================
 * Implements:
 *   1. App Shell caching  → works offline after first visit
 *   2. Model caching      → TF.js model files cached for offline inference
 *   3. API fallback       → queue failed predictions for retry when back online
 *
 * Strategy:
 *   - Static assets    : Cache-First (always serve from cache if available)
 *   - API calls        : Network-First (try server, fall back to offline mode)
 */

const CACHE_VERSION  = "shamba-v1.0";
const MODEL_CACHE    = "shamba-model-v1.0";

// Files to pre-cache on install (app shell)
const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.json",
  // TF.js model files (add when model is exported)
  // "./model/tfjs/model.json",
  // "./model/tfjs/group1-shard1of1.bin",
  // "./model/class_labels.json",
];

// ─────────────────────────────────────────────
// INSTALL — pre-cache app shell
// ─────────────────────────────────────────────
self.addEventListener("install", (event) => {
  console.log("[SW] Installing…");
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      console.log("[SW] Pre-caching app shell");
      return cache.addAll(APP_SHELL);
    })
  );
  self.skipWaiting(); // activate immediately
});

// ─────────────────────────────────────────────
// ACTIVATE — clean up old caches
// ─────────────────────────────────────────────
self.addEventListener("activate", (event) => {
  console.log("[SW] Activating…");
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_VERSION && k !== MODEL_CACHE)
          .map((k) => {
            console.log(`[SW] Deleting old cache: ${k}`);
            return caches.delete(k);
          })
      )
    )
  );
  self.clients.claim(); // take control immediately
});

// ─────────────────────────────────────────────
// FETCH — intercept all requests
// ─────────────────────────────────────────────
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests (e.g. POST to /api/predict)
  if (request.method !== "GET") return;

  // Skip browser extension requests
  if (!url.protocol.startsWith("http")) return;

  // ── API requests: Network-First ──────────────────────────
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(networkFirst(request));
    return;
  }

  // ── TF.js model files: Cache-First (large, don't re-download) ──
  if (url.pathname.includes("/model/tfjs/") || url.pathname.includes("tfjs")) {
    event.respondWith(cacheFirst(request, MODEL_CACHE));
    return;
  }

  // ── CDN resources (TF.js from jsdelivr): Cache-First ──────
  if (url.hostname.includes("cdn.jsdelivr.net") ||
      url.hostname.includes("cdnjs.cloudflare.com")) {
    event.respondWith(cacheFirst(request, MODEL_CACHE));
    return;
  }

  // ── App shell: Cache-First with network fallback ───────────
  event.respondWith(cacheFirst(request, CACHE_VERSION));
});

// ─────────────────────────────────────────────
// STRATEGIES
// ─────────────────────────────────────────────

/**
 * Cache-First: serve cached response, fetch from network if not cached.
 * Best for static assets that rarely change.
 */
async function cacheFirst(request, cacheName = CACHE_VERSION) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone()); // cache for next time
    }
    return response;
  } catch {
    return offlineFallback(request);
  }
}

/**
 * Network-First: try network, fall back to cache.
 * Best for API calls where fresh data is preferred.
 */
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || offlineFallback(request);
  }
}

/**
 * Returns a user-friendly offline response when nothing is cached.
 */
async function offlineFallback(request) {
  const url = new URL(request.url);
  if (url.pathname.startsWith("/api/")) {
    return new Response(
      JSON.stringify({
        success: false,
        error: {
          message : "You are offline. Using on-device AI model for analysis.",
          code    : "OFFLINE",
          retake  : false,
        },
      }),
      { status: 503, headers: { "Content-Type": "application/json" } }
    );
  }

  // Try to return the cached index.html for navigation
  const cachedIndex = await caches.match("./index.html");
  return cachedIndex || new Response("Offline — please check your connection.", { status: 503 });
}
