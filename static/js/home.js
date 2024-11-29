// Detayları Gör butonlarına animasyon ekleyin
document.querySelectorAll('.details-button').forEach(button => {
    button.addEventListener('click', () => {
        button.innerText = "Loading...";
        setTimeout(() => {
            button.innerText = "Detayları Gör";
        }, 1000); // 1 saniyelik gecikme simülasyonu
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Etkinliğe Katıl
    document.querySelectorAll('.join-button').forEach(button => {
        button.addEventListener('click', () => {
            const eventItem = button.closest('li');
            const eventId = button.dataset.eventId;

            fetch(`/event_management/${eventId}/join/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'joined') {
                        // Sağ tarafa kaydırma animasyonu
                        eventItem.classList.add('slide-right');

                        setTimeout(() => {
                            // "Your Events" kısmına taşı
                            const userEventsList = document.querySelector('#user-events-list');
                            eventItem.classList.remove('slide-right');
                            eventItem.innerHTML = `
                                <strong>${data.event_name}</strong> - ${data.event_date}
                                <br>Location: ${data.event_location}
                                <a href="/event_management/${data.event_id}/" class="details-button">Detayları Gör</a>
                                <button class="leave-button" data-event-id="${data.event_id}">Çık</button>
                            `;
                            userEventsList.appendChild(eventItem);
                        }, 500); // Animasyonun süresiyle senkronize
                    }
                });
        });
    });

    // Etkinlikten Çık
    document.querySelectorAll('.leave-button').forEach(button => {
        button.addEventListener('click', () => {
            const eventItem = button.closest('li');
            const eventId = button.dataset.eventId;

            fetch(`/event_management/${eventId}/leave/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'left') {
                        // Sol tarafa kaydırma animasyonu
                        eventItem.classList.add('slide-left');

                        setTimeout(() => {
                            // "General Events" kısmına taşı
                            const generalEventsList = document.querySelector('#general-events-list');
                            eventItem.classList.remove('slide-left');
                            eventItem.innerHTML = `
                                <strong>${data.event_name}</strong> - ${data.event_date}
                                <br>Location: ${data.event_location}
                                <a href="/event_management/${data.event_id}/" class="details-button">Detayları Gör</a>
                                <button class="join-button" data-event-id="${data.event_id}">Katıl</button>
                            `;
                            generalEventsList.appendChild(eventItem);
                        }, 500); // Animasyonun süresiyle senkronize
                    }
                });
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([39.9208, 32.8541], 6); // Default location: Ankara

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    // Example events
    const events = [
        { name: 'Rock Concert', latitude: 39.9208, longitude: 32.8541, location: 'Ankara', description: 'A great concert' },
        { name: 'Art Exhibition', latitude: 41.0082, longitude: 28.9784, location: 'Istanbul', description: 'A wonderful exhibition' },
    ];

    // Add markers for events
    events.forEach(event => {
        const marker = L.marker([event.latitude, event.longitude]).addTo(map).bindPopup(`
            <div>
                <h3>${event.name}</h3>
                <p><strong>Location:</strong> ${event.location}</p>
                <p><strong>Description:</strong> ${event.description}</p>
            </div>
        `);
    });

    // Route Planning
    const startMarker = L.marker([39.9208, 32.8541], { draggable: true }).addTo(map).bindPopup('Start');
    const endMarker = L.marker([41.0082, 28.9784], { draggable: true }).addTo(map).bindPopup('End');

    document.getElementById('findRoute').addEventListener('click', () => {
        const start = startMarker.getLatLng();
        const end = endMarker.getLatLng();
        const mode = document.getElementById('mode').value;

        const apiUrl = `https://router.project-osrm.org/route/v1/${mode.toLowerCase()}/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data.routes && data.routes.length > 0) {
                    const coordinates = data.routes[0].geometry.coordinates.map(coord => [coord[1], coord[0]]);
                    L.polyline(coordinates, { color: 'blue' }).addTo(map);
                } else {
                    alert('Route calculation failed.');
                }
            });
    });
});

