# 🧬 Algoritmo Genético para el Problema de Enrutamiento

En este proyecto, además del clásico y determinista Algoritmo de Dijkstra, se ha implementado un **Algoritmo Genético (AG)** para encontrar rutas entre un departamento de origen y un destino. 

Esta implementación está inspirada en cómo la naturaleza optimiza a las especies y en cómo se resuelve el clásico **Problema del Agente Viajero (TSP por sus siglas en inglés)**.

---

## 🎯 ¿Qué es un Algoritmo Genético?

Los algoritmos genéticos son técnicas de optimización y búsqueda heurística basadas en los postulados de la evolución biológica (selección natural). No garantizan encontrar *la mejor* solución matemática absoluta, pero suelen encontrar una solución "suficientemente buena" (casi óptima) en un tiempo razonable.

## ⚙️ ¿Cómo está implementado en este proyecto?

La lógica se encuentra centralizada en el archivo `genetico.py`. El proceso sigue estos pasos fundamentales:

### 1. Representación del Cromosoma
En nuestro caso, el **cromosoma** (el individuo) es una **ruta** específica. Se representa como una lista ordenada de nodos (departamentos) partiendo del origen y finalizando en el destino.
> Ejemplo: `['Puno', 'Cusco', 'Apurímac', 'Ayacucho', 'Ica', 'Lima']`

### 2. Generación de la Población Inicial
Al iniciar la búsqueda, creamos un conjunto (población) de `N` rutas aleatorias, usando un proceso de caminata aleatoria. 
El algoritmo parte del nodo inicial, busca los nodos vecinos posibles y selecciona uno al azar que aún no haya sido visitado (para evitar ciclos infinitos) hasta llegar al nodo final.
Si el azar nos lleva a un "callejón sin salida", esa ruta es descartada.

### 3. Evaluación (Fitness)
El ambiente natural selecciona a los individuos más "aptos". En nuestro modelo, el **fitness** o aptitud de una ruta está determinado por su distancia total. Cuanto menor sea la distancia del recorrido completo en el grafo (kilómetros acumulados), **más fuerte/apto** será el individuo.

```python
# Un fitness mejor es una distancia menor
poblacion = sorted(poblacion, key=calcular_distancia)
```

### 4. Selección
En cada generación (o ciclo evolutivo), tomamos únicamente a la mejor mitad de la población. Los caminos ineficientes o que dieron mucha vuelta son eliminados, simulando la supervivencia de los más aptos.

### 5. Crossover (Cruce)
Para repoblar el entorno y mantener el mismo tamaño de la población, los individuos sobrevivientes (las mejores rutas) "se aparean" intercambiando información (genes):
- Se toman dos rutas al azar dentro del grupo de las mejores.
- Se busca un nodo (departamento) en común entre ambas (excluyendo el origen y el destino).
- Se genera un "hijo" combinando la primera parte del Camino 1 (hasta el nodo común) con la segunda parte del Camino 2 (desde el nodo común hasta el destino).

Este cruce permite explotar características exitosas de distintas rutas y unirlas para ver si forman un camino aún mejor.

### 6. Mutación
La naturaleza incluye mutaciones genéticas para evitar la homogeneidad y explorar nuevas posibilidades. En los algoritmos genéticos, la mutación previene el "estancamiento" en óptimos locales.
El script incluye la base conceptual de esta mutación introduciendo una pequeña probabilidad de cambio aleatorio en las rutas existentes.

---

## ⚖️ Comparación en el Uso Práctico

| Característica | Dijkstra | Algoritmo Genético |
|---|---|---|
| **Precisión** | 100% (Garantiza el camino más corto). | Heurístico (Puede no encontrar el mejor absoluto). |
| **Naturaleza** | Exacto, Determinista. | Probabilístico, Estocástico. |
| **Uso Ideal** | Grafos con pesos exactos y rutas simples directas. | Problemas NP-Duros muy grandes como el Agente Viajero, donde calcular todo toma demasiado tiempo. |

### Consideraciones sobre el Problema del Agente Viajero (TSP)
Aunque el problema que se resuelve en esta UI es la ruta más corta del punto A al punto B (Pathfinding), las mecánicas utilizadas para mezclar caminos y mutar rutas son directamente extraídas y aplicadas a cómo los Algoritmos Genéticos abordan el TSP (donde el objetivo es visitar todas las ciudades sin repetir).
