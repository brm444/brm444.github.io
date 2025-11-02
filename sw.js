/**
 * Service Worker for bankole.org
 * Simple PWA implementation compatible with GitHub Pages
 * No build step required - vanilla JavaScript only
 */

const CACHE_VERSION = 'v1';
const STATIC_CACHE = 'bankole-static-' + CACHE_VERSION;
const RUNTIME_CACHE = 'bankole-runtime-' + CACHE_VERSION;
const OFFLINE_PAGE = '/offline.html';

// Static assets to cache on install
const STATIC_ASSETS = [
  '/',
  '/offline.html',
  '/siteicon.png'
];

/**
 * Install event - cache static assets
 */
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(function(cache) {
        return cache.addAll(STATIC_ASSETS);
      })
      .then(function() {
        return self.skipWaiting();
      })
  );
});

/**
 * Activate event - clean up old caches
 */
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys()
      .then(function(cacheNames) {
        return Promise.all(
          cacheNames.map(function(cacheName) {
            if (cacheName !== STATIC_CACHE && cacheName !== RUNTIME_CACHE) {
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(function() {
        return self.clients.claim();
      })
  );
});

/**
 * Fetch event - implement caching strategies
 * - Cache-first for static assets (CSS, JS, images)
 * - Network-first for HTML pages
 * - Offline fallback for failed navigations
 */
self.addEventListener('fetch', function(event) {
  const request = event.request;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip external requests (analytics, comments, etc.)
  if (url.origin !== location.origin) {
    return;
  }

  // Cache-first strategy for static assets
  if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Network-first strategy for HTML pages
  if (isNavigationRequest(request)) {
    event.respondWith(networkFirst(request));
    return;
  }
});

/**
 * Cache-first strategy
 * Try cache first, fall back to network, then cache the response
 */
function cacheFirst(request) {
  return caches.match(request)
    .then(function(cachedResponse) {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(request)
        .then(function(networkResponse) {
          // Cache successful responses
          if (networkResponse && networkResponse.status === 200) {
            return caches.open(RUNTIME_CACHE)
              .then(function(cache) {
                cache.put(request, networkResponse.clone());
                return networkResponse;
              });
          }
          return networkResponse;
        });
    });
}

/**
 * Network-first strategy
 * Try network first, fall back to cache, then offline page
 */
function networkFirst(request) {
  return fetch(request)
    .then(function(networkResponse) {
      // Cache successful HTML responses
      if (networkResponse && networkResponse.status === 200) {
        return caches.open(RUNTIME_CACHE)
          .then(function(cache) {
            cache.put(request, networkResponse.clone());
            return networkResponse;
          });
      }
      return networkResponse;
    })
    .catch(function() {
      // Try cache first
      return caches.match(request)
        .then(function(cachedResponse) {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Return offline page for navigation requests
          return caches.match(OFFLINE_PAGE);
        });
    });
}

/**
 * Check if the request is for a static asset
 */
function isStaticAsset(pathname) {
  const staticExtensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.woff', '.woff2', '.ttf', '.eot'];
  return staticExtensions.some(function(ext) {
    return pathname.endsWith(ext);
  });
}

/**
 * Check if the request is a navigation request
 */
function isNavigationRequest(request) {
  return request.mode === 'navigate' ||
         (request.method === 'GET' && request.headers.get('accept').includes('text/html'));
}
