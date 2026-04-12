from flask import Flask, jsonify, render_template, request
from datos_peru import DEPARTAMENTOS, obtener_grafo
from dijkstra import calcular_ruta_mas_corta

app = Flask(__name__)

# Precalcular el grafo una sola vez al iniciar el servidor
GRAFO = obtener_grafo()

@app.route('/')
def index():
    # Enviar al frontend la lista de departamentos y sus coordenadas
    return render_template('index.html', departamentos=DEPARTAMENTOS)

@app.route('/api/calcular_ruta', methods=['POST'])
def api_calcular_ruta():
    data = request.json
    origen = data.get('origen')
    destino = data.get('destino')
    
    if not origen or not destino:
        return jsonify({"error": "Origen y destino son requeridos"}), 400
        
    if origen not in GRAFO or destino not in GRAFO:
        return jsonify({"error": "Departamento no válido"}), 400
        
    ruta, distancia_total = calcular_ruta_mas_corta(GRAFO, origen, destino)
    
    if not ruta:
        return jsonify({"error": "No se encontró una ruta"}), 404
        
    # Agrupar información de coordenadas + distancias parciales
    ruta_coordenadas = []
    distancia_acumulada = 0.0
    for i, parada in enumerate(ruta):
        distancia_tramo = 0.0
        if i > 0:
            anterior = ruta[i - 1]
            distancia_tramo = GRAFO[anterior][parada]
            distancia_acumulada += distancia_tramo

        ruta_coordenadas.append({
            "departamento": parada,
            "lat": DEPARTAMENTOS[parada]["lat"],
            "lng": DEPARTAMENTOS[parada]["lng"],
            "distancia_tramo": round(distancia_tramo, 2),
            "distancia_acumulada": round(distancia_acumulada, 2)
        })

    return jsonify({
        "ruta": ruta_coordenadas,
        "distancia_total": round(distancia_total, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
