import math

# Coordenadas aproximadas de las capitales de cada departamento
DEPARTAMENTOS = {
    "Amazonas": {"lat": -6.2294, "lng": -77.8726, "capital": "Chachapoyas"},
    "Ancash": {"lat": -9.5278, "lng": -77.5278, "capital": "Huaraz"},
    "Apurímac": {"lat": -13.6339, "lng": -72.8814, "capital": "Abancay"},
    "Arequipa": {"lat": -16.4090, "lng": -71.5375, "capital": "Arequipa"},
    "Ayacucho": {"lat": -13.1588, "lng": -74.2239, "capital": "Ayacucho"},
    "Cajamarca": {"lat": -7.1638, "lng": -78.5003, "capital": "Cajamarca"},
    "Callao": {"lat": -12.0566, "lng": -77.1181, "capital": "Callao"},
    "Cusco": {"lat": -13.5226, "lng": -71.9673, "capital": "Cusco"},
    "Huancavelica": {"lat": -12.7826, "lng": -74.9727, "capital": "Huancavelica"},
    "Huánuco": {"lat": -9.9306, "lng": -76.2422, "capital": "Huánuco"},
    "Ica": {"lat": -14.0678, "lng": -75.7286, "capital": "Ica"},
    "Junín": {"lat": -12.0651, "lng": -75.2049, "capital": "Huancayo"},
    "La Libertad": {"lat": -8.1091, "lng": -79.0215, "capital": "Trujillo"},
    "Lambayeque": {"lat": -6.7714, "lng": -79.8409, "capital": "Chiclayo"},
    "Lima": {"lat": -12.0464, "lng": -77.0428, "capital": "Lima"},
    "Loreto": {"lat": -3.7491, "lng": -73.2243, "capital": "Iquitos"},
    "Madre de Dios": {"lat": -12.5933, "lng": -69.1836, "capital": "Puerto Maldonado"},
    "Moquegua": {"lat": -17.1983, "lng": -70.9357, "capital": "Moquegua"},
    "Pasco": {"lat": -10.6675, "lng": -76.2567, "capital": "Cerro de Pasco"},
    "Piura": {"lat": -5.1945, "lng": -80.6328, "capital": "Piura"},
    "Puno": {"lat": -15.8402, "lng": -70.0219, "capital": "Puno"},
    "San Martín": {"lat": -6.0342, "lng": -76.9723, "capital": "Moyobamba"},
    "Tacna": {"lat": -18.0066, "lng": -70.2463, "capital": "Tacna"},
    "Tumbes": {"lat": -3.5669, "lng": -80.4515, "capital": "Tumbes"},
    "Ucayali": {"lat": -8.3791, "lng": -74.5539, "capital": "Pucallpa"}
}

# Mapa de adyacencia (quién conecta con quién)
CONEXIONES = [
    ("Tumbes", "Piura"),
    ("Piura", "Lambayeque"), ("Piura", "Cajamarca"),
    ("Lambayeque", "Cajamarca"), ("Lambayeque", "La Libertad"),
    ("La Libertad", "Cajamarca"), ("La Libertad", "Amazonas"), ("La Libertad", "San Martín"), ("La Libertad", "Huánuco"), ("La Libertad", "Ancash"),
    ("Ancash", "Huánuco"), ("Ancash", "Lima"),
    ("Lima", "Callao"), ("Lima", "Huánuco"), ("Lima", "Pasco"), ("Lima", "Junín"), ("Lima", "Huancavelica"), ("Lima", "Ica"),
    ("Ica", "Huancavelica"), ("Ica", "Ayacucho"), ("Ica", "Arequipa"),
    ("Arequipa", "Ayacucho"), ("Arequipa", "Apurímac"), ("Arequipa", "Cusco"), ("Arequipa", "Puno"), ("Arequipa", "Moquegua"),
    ("Moquegua", "Puno"), ("Moquegua", "Tacna"),
    ("Tacna", "Puno"),
    ("Cajamarca", "Amazonas"),
    ("Amazonas", "San Martín"), ("Amazonas", "Loreto"),
    ("San Martín", "Huánuco"), ("San Martín", "Loreto"), ("San Martín", "Ucayali"),
    ("Huánuco", "Pasco"), ("Huánuco", "Ucayali"),
    ("Pasco", "Junín"), ("Pasco", "Ucayali"),
    ("Junín", "Huancavelica"), ("Junín", "Ayacucho"), ("Junín", "Cusco"), ("Junín", "Ucayali"),
    ("Huancavelica", "Ayacucho"),
    ("Ayacucho", "Apurímac"), ("Ayacucho", "Cusco"),
    ("Apurímac", "Cusco"),
    ("Cusco", "Puno"), ("Cusco", "Madre de Dios"), ("Cusco", "Ucayali"),
    ("Puno", "Madre de Dios"),
    ("Madre de Dios", "Ucayali"),
    ("Ucayali", "Loreto")
]

def haversine_dist(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radio de la Tierra en kilómetros
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def obtener_grafo():
    grafo = {dep: {} for dep in DEPARTAMENTOS}
    for origen, destino in CONEXIONES:
        lat1, lon1 = DEPARTAMENTOS[origen]["lat"], DEPARTAMENTOS[origen]["lng"]
        lat2, lon2 = DEPARTAMENTOS[destino]["lat"], DEPARTAMENTOS[destino]["lng"]
        
        distancia = round(haversine_dist(lat1, lon1, lat2, lon2), 2)
        
        grafo[origen][destino] = distancia
        grafo[destino][origen] = distancia # El grafo es bidireccional
    
    return grafo
