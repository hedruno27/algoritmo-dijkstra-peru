document.addEventListener('DOMContentLoaded', () => {
    // 1. Inicializar el mapa centrado en Perú
    const map = L.map('map').setView([-9.19, -75.015], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 2. Variables para almacenar marcadores y capas dibujadas
    const markers = {};
    let arrowLayers = []; 

    // Iconos personalizados
    const iconNormal = L.divIcon({
        className: 'custom-icon',
        html: "<div style='background-color:#94a3b8; width:14px; height:14px; border-radius:50%; border:2px solid #fff; box-shadow: 0 0 3px #000;'></div>",
        iconSize: [14, 14], iconAnchor: [7, 7]
    });

    const iconOrigen = L.divIcon({
        className: 'custom-icon',
        html: "<div style='background-color:#22c55e; width:20px; height:20px; border-radius:50%; border:3px solid #fff; box-shadow: 0 0 5px #000; z-index: 1000;'></div>",
        iconSize: [20, 20], iconAnchor: [10, 10]
    });

    const iconDestino = L.divIcon({
        className: 'custom-icon',
        html: "<div style='background-color:#a855f7; width:20px; height:20px; border-radius:50%; border:3px solid #fff; box-shadow: 0 0 5px #000; z-index: 1000;'></div>",
        iconSize: [20, 20], iconAnchor: [10, 10]
    });

    // 3. Renderizar marcadores iniciales
    const DEPARTAMENTOS_DATA = JSON.parse(document.getElementById('departamentos-data').textContent);
    for (const [dep, data] of Object.entries(DEPARTAMENTOS_DATA)) {
        const marker = L.marker([data.lat, data.lng], { icon: iconNormal })
            .addTo(map)
            .bindTooltip(`<b>${dep}</b><br>${data.capital}`, { permanent: false, direction: 'top' });
        markers[dep] = marker;
    }

    // 4. Elementos de la UI
    const selectOrigen = document.getElementById('origen');
    const selectDestino = document.getElementById('destino');
    const btnCalcular = document.getElementById('btn-calcular');
    const divRutasLista = document.getElementById('rutas-lista');
    const spanDistancia = document.getElementById('distancia-text');

    // Función para actualizar colores de marcadores según selección
    function updateMarkers() {
        const origen = selectOrigen.value;
        const destino = selectDestino.value;

        for (const [dep, marker] of Object.entries(markers)) {
            if (dep === origen) {
                marker.setIcon(iconOrigen);
            } else if (dep === destino) {
                marker.setIcon(iconDestino);
            } else {
                marker.setIcon(iconNormal);
            }
        }
    }

    selectOrigen.addEventListener('change', updateMarkers);
    selectDestino.addEventListener('change', updateMarkers);

    // 5. Botón calcular ruta
    btnCalcular.addEventListener('click', async () => {
        const origen = selectOrigen.value;
        const destino = selectDestino.value;

        if (!origen || !destino) {
            alert('Por favor seleccione origen y destino.');
            return;
        }

        if (origen === destino) {
            alert('El origen y destino deben ser diferentes.');
            return;
        }

        btnCalcular.disabled = true;
        btnCalcular.textContent = 'Calculando...';

        try {
            const response = await fetch('/api/calcular_ruta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ origen, destino })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || 'Ocurrió un error al calcular la ruta.');
                return;
            }

            dibujarRuta(data.ruta, data.distancia_total);

        } catch (error) {
            console.error('Error fetching route:', error);
            alert('Error de conexión con el servidor.');
        } finally {
            btnCalcular.disabled = false;
            btnCalcular.textContent = 'Encontrar Camino';
        }
    });

    // 6. Dibujar la ruta y poner lista en panel lateral
    function dibujarRuta(ruta, distancia_total) {
        // Limpiar flechas anteriores
        arrowLayers.forEach(layer => map.removeLayer(layer));
        arrowLayers = [];

        // Extraer coordenadas ordenadas
        const latlngs = ruta.map(n => [n.lat, n.lng]);

        // Dibujar polilínea gruesa base (naranja/roja) como pidió el prototipo
        const polyline = L.polyline(latlngs, {
            color: '#ef4444', 
            weight: 5,
            opacity: 0.8
        }).addTo(map);

        arrowLayers.push(polyline);

        // Añadir flechas usando Leaflet.PolylineDecorator
        const arrowDecorator = L.polylineDecorator(polyline, {
            patterns: [
                {
                    offset: '10%',
                    repeat: '20%',
                    symbol: L.Symbol.arrowHead({
                        pixelSize: 15,
                        polygon: false,
                        pathOptions: { stroke: true, weight: 3, color: '#000' }
                    })
                }
            ]
        }).addTo(map);

        arrowLayers.push(arrowDecorator);

        // Ajustar vista del mapa para que quepa toda la ruta
        map.fitBounds(polyline.getBounds(), { padding: [50, 50] });

        // Actualizar UI Lateral
        divRutasLista.innerHTML = '';
        ruta.forEach((nodo, index) => {
            const div = document.createElement('div');
            div.className = 'ruta-item';

            if (index === 0) {
                div.innerHTML = `
                    <div class="ruta-nodo origen-nodo">
                        <span class="ruta-label">🟢 Inicio</span>
                        <span class="ruta-nombre">${nodo.departamento}</span>
                        <span class="ruta-dist-acum">0 km acumulado</span>
                    </div>`;
            } else {
                const esUltimo = index === ruta.length - 1;
                const icono = esUltimo ? '🟣 Destino' : `↓ Tramo ${index}`;
                div.innerHTML = `
                    <div class="ruta-nodo ${esUltimo ? 'destino-nodo' : ''}">
                        <span class="ruta-label">${icono}</span>
                        <span class="ruta-nombre">${nodo.departamento}</span>
                        <span class="ruta-dist-tramo">+ ${nodo.distancia_tramo} km este tramo</span>
                        <span class="ruta-dist-acum">${nodo.distancia_acumulada} km acumulado</span>
                    </div>`;
            }

            divRutasLista.appendChild(div);
        });

        // Actualizar Distancia
        spanDistancia.innerHTML = `<b>${distancia_total} KM</b>`;
        
        // Asegurarse de que el origen y destino estén bien resaltados
        updateMarkers();
    }
});
