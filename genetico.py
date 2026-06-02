import random

def calcular_ruta_genetico(grafo, inicio, fin, tamano_poblacion=50, generaciones=100):
    """
    Algoritmo genético para encontrar una ruta entre inicio y fin.
    Para el problema de rutas en un grafo (adaptación del agente viajero).
    """
    def crear_ruta_aleatoria():
        ruta = [inicio]
        actual = inicio
        visitados = {inicio}
        
        while actual != fin:
            vecinos = [n for n in grafo[actual] if n not in visitados]
            if not vecinos:
                return None  # Camino sin salida
            siguiente = random.choice(vecinos)
            ruta.append(siguiente)
            visitados.add(siguiente)
            actual = siguiente
        return ruta

    def calcular_distancia(ruta):
        if not ruta:
            return float('inf')
        dist = 0
        for i in range(len(ruta) - 1):
            if ruta[i+1] not in grafo[ruta[i]]:
                return float('inf')
            dist += grafo[ruta[i]][ruta[i+1]]
        return dist

    # 1. Inicializar población
    poblacion = []
    intentos = 0
    while len(poblacion) < tamano_poblacion and intentos < tamano_poblacion * 10:
        ruta = crear_ruta_aleatoria()
        if ruta:
            poblacion.append(ruta)
        intentos += 1
        
    if not poblacion:
        # Fallback de emergencia por si el grafo es muy restrictivo
        from dijkstra import calcular_ruta_mas_corta
        return calcular_ruta_mas_corta(grafo, inicio, fin)

    # 2. Evolución
    for generacion in range(generaciones):
        # Ordenar por fitness (menor distancia es mejor)
        poblacion = sorted(poblacion, key=calcular_distancia)
        
        # Mantener solo los mejores
        mejores = poblacion[:tamano_poblacion // 2]
        nueva_generacion = list(mejores)
        
        # Crossover
        while len(nueva_generacion) < tamano_poblacion:
            p1 = random.choice(mejores)
            p2 = random.choice(mejores)
            
            # Buscar nodos en común (excluyendo inicio y fin) para hacer crossover
            comunes = set(p1[1:-1]).intersection(set(p2[1:-1]))
            if comunes:
                corte = random.choice(list(comunes))
                idx1 = p1.index(corte)
                idx2 = p2.index(corte)
                hijo = p1[:idx1] + p2[idx2:]
                
                # Verificar si el hijo es válido (sin bucles)
                if len(hijo) == len(set(hijo)):
                    nueva_generacion.append(hijo)
                else:
                    nueva_generacion.append(random.choice(mejores))
            else:
                nueva_generacion.append(random.choice(mejores))
                
        poblacion = nueva_generacion

    mejor_ruta = min(poblacion, key=calcular_distancia)
    distancia_total = calcular_distancia(mejor_ruta)
    
    if distancia_total == float('inf'):
        return None, float('inf')
        
    return mejor_ruta, distancia_total
