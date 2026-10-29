// Initialize Leaflet Map centered on Dar es Salaam
const map = L.map('map').setView([-6.7924, 39.2083], 13);

// Add OpenStreetMap Tile Layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Feature Group to store drawn polygons
const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Add Leaflet Draw controls
const drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems
    },
    draw: {
        polygon: true,
        rectangle: true,
        polyline: false,
        circle: false,
        marker: false,
        circlemarker: false
    }
});
map.addControl(drawControl);

let selectedBounds = null;
const btnAnalyze = document.getElementById('btn-analyze');
const resultsContent = document.getElementById('results-content');
const promptSelect = document.getElementById('prompt-select');

// Handle Drawn Layers
map.on(L.Draw.Event.CREATED, function (e) {
    drawnItems.clearLayers();
    const layer = e.layer;
    drawnItems.addLayer(layer);

    selectedBounds = layer.getBounds();
    btnAnalyze.disabled = false;
});

// Send analysis request to FastAPI backend
btnAnalyze.addEventListener('click', async () => {
    if (!selectedBounds) return;

    btnAnalyze.disabled = true;
    btnAnalyze.innerText = "Analyzing...";
    resultsContent.innerHTML = "<p class='placeholder'>Processing spatial data with SAM 3.1 & Muse Spark...</p>";

    const payload = {
        prompt: promptSelect.value,
        coordinates: [
            [selectedBounds.getSouth(), selectedBounds.getWest()],
            [selectedBounds.getNorth(), selectedBounds.getEast()]
        ]
    };

    try {
        const response = await fetch('/api/v1/analyze-spatial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        resultsContent.innerHTML = `<p style="color: #ef4444;">Error: ${error.message}</p>`;
    } finally {
        btnAnalyze.disabled = false;
        btnAnalyze.innerText = "Run AI Analysis";
    }
});

function displayResults(data) {
    resultsContent.innerHTML = `
        <div style="font-size: 0.9rem; display: flex; flex-direction: column; gap: 8px;">
            <p><strong>Status:</strong> ${data.status}</p>
            <p><strong>Prompt:</strong> ${data.prompt}</p>
            <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
            <div style="margin-top: 8px; padding: 8px; background: #111827; border-radius: 4px;">
                <p style="font-size: 0.8rem; color: #10b981;"><strong>Segment Summary:</strong></p>
                <p style="font-size: 0.8rem; color: #d1d5db;">${data.segmentation_summary}</p>
            </div>
        </div>
    `;
}
