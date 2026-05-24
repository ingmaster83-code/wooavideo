const CACHE_NAME = 'wooavideo-v1';
const APP_SHELL = [
  '/',
  '/index.html',
  '/video-convert.html',
  '/css/style.css',
  '/js/pwa-install.js',
  '/js/ffmpeg.js',
  '/js/814.ffmpeg.js',
  '/manifest.json',
  '/icons/icon.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
