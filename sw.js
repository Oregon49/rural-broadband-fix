// Rural Broadband Fix service worker — cache the app shell
var CACHE = 'rbf-v1';
var SHELL = ['/', '/index.html', '/manifest.json', '/assets/icon-192.png', '/assets/icon-512.png'];
self.addEventListener('install', function(e) {
  e.waitUntil(caches.open(CACHE).then(function(c) { return c.addAll(SHELL); }).then(function() { return self.skipWaiting(); }));
});
self.addEventListener('activate', function(e) {
  e.waitUntil(self.clients.claim());
});
self.addEventListener('fetch', function(e) {
  e.respondWith(fetch(e.request).catch(function() { return caches.match(e.request).then(function(r) { return r || caches.match('/index.html'); }); }));
});
