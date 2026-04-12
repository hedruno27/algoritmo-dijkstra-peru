import heapq

def calcular_ruta_mas_corta(grafo, inicio, fin):
    """
    Implementa el algoritmo de Dijkstra para encontrar la ruta más corta entre dos nodos.
    :param grafo: Diccionario de diccionarios representando el grafo con distancias.
    :param inicio: Nodo de origen.
    :param fin: Nodo de destino.
    :return: Una tupla (ruta_lista, distancia_total)
    """
    # Inicialización
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    camino_previo = {}
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Optimización: si llegamos al fin, terminamos el bucle
        if nodo_actual == fin:
            break
            
        # Ignorar si encontramos un camino más largo al procesar
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        # Analizar vecinos
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
            
            # Solo considerar este camino si es mejor
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                camino_previo[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia, vecino))
                
    # Reconstruir el camino
    camino_final = []
    nodo = fin
    
    # Si el nodo final no está en el camino y no es el origen, no hay ruta
    if nodo not in camino_previo and nodo != inicio:
        return None, float('inf')
        
    while nodo != inicio:
        camino_final.insert(0, nodo)
        nodo = camino_previo[nodo]
    camino_final.insert(0, inicio)
    
    return camino_final, distancias[fin]
