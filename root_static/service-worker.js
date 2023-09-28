// Define a cache name
const cacheName = 'image-cache-v1';

// Install event: Setup the cache
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(cacheName) // Open the cache
  );
});

// Fetch event: Intercept network requests
self.addEventListener('fetch', event => {
  // Check if the request is for an image
  if (event.request.destination === 'image') {
    event.respondWith(
      caches.match(event.request) // Check if the image is in the cache
        .then(cachedResponse => {
          if (cachedResponse) {
            console.log('Loading from cache:', event.request.url); // Log message when loading from cache
            return cachedResponse; // If in the cache, return the cached image
          }
          
          // If not in the cache, fetch the image from the network
          return fetch(event.request).then(networkResponse => {
            // Clone the response (Response objects can only be used once)
            const clonedResponse = networkResponse.clone();
            
            // Open the cache
            caches.open(cacheName).then(cache => {
              // Put the fetched image in the cache
              cache.put(event.request, clonedResponse);
              console.log('Saving to cache:', event.request.url); // Log message when saving to cache
            });
            
            // Return the network response
            return networkResponse;
          });
        })
    );
  }
});
