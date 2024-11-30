document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('map');
    const loadingSpinner = document.querySelector('.loading-spinner');

    try {
        // Safely parse event data
        const eventsDataElement = document.getElementById('events-data');
        const events = JSON.parse(eventsDataElement.textContent || '[]');

        const map = L.map('map').setView([39.9208, 32.8541], 6);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);

        // Add event markers
        events.forEach(event => {
            if (event.latitude && event.longitude) {
                L.marker([event.latitude, event.longitude])
                    .addTo(map)
                    .bindPopup(`
                        <div>
                            <h3>${event.name}</h3>
                            <p><strong>Location:</strong> ${event.location}</p>
                            <p><strong>Date:</strong> ${event.date || 'N/A'}</p>
                            <p><strong>Description:</strong> ${event.description || 'No description provided.'}</p>
                        </div>
                    `);
            }
        });

        // Start and Destination markers
        const startMarker = L.marker([39.9208, 32.8541], { draggable: true }).addTo(map).bindPopup('Start Location');
        const endMarker = L.marker([39.914, 32.850], { draggable: true }).addTo(map).bindPopup('Destination');

        // Handle route finding
        document.getElementById('findRoute').addEventListener('click', () => {
            const start = startMarker.getLatLng();
            const end = endMarker.getLatLng();
            const mode = document.getElementById('mode').value.toLowerCase();

            const routeApiUrl = `https://router.project-osrm.org/route/v1/${mode}/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`;

            loadingSpinner.style.display = 'block';

            fetch(routeApiUrl)
                .then(response => response.json())
                .then(data => {
                    loadingSpinner.style.display = 'none';
                    if (data.routes && data.routes.length > 0) {
                        const route = data.routes[0];
                        const coordinates = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
                        L.polyline(coordinates, { color: 'blue', weight: 5 }).addTo(map);
                    } else {
                        alert('Could not calculate route.');
                    }
                })
                .catch(error => {
                    loadingSpinner.style.display = 'none';
                    alert('An error occurred while calculating the route.');
                });
        });
    } catch (error) {
        loadingSpinner.style.display = 'none';
        alert('Failed to load the map.');
    }
});
