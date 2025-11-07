import math
import heapq


# === Versión de Dijkstra de un nodo a otro ===
def dijkstra_simple(graph, start_id, target_id):
    dist = {v: math.inf for v in graph.get_vertices()}
    pred = {v: None for v in graph.get_vertices()}
    dist[start_id] = 0

    no_visitados = set(graph.get_vertices())

    print("=== Iteración inicial ===")
    for v in graph.get_vertices():
        print(f"{v}: ({'∞' if dist[v]==math.inf else dist[v]}, {pred[v]})")
    print()

    while no_visitados:
        # Elegir el vértice no visitado con menor distancia
        u = min(no_visitados, key=lambda v: dist[v])
        if dist[u] == math.inf:
            break

        print(f"Procesando vértice {u} con distancia {dist[u]}")
        no_visitados.remove(u)

        if u == target_id:
            print(f"\nDestino {target_id} alcanzado. Fin de la búsqueda.\n")
            break

        # Relajar aristas
        for v, peso in graph.get_vertex(u).get_connections().items():
            if v in no_visitados:
                nueva_dist = dist[u] + peso
                if nueva_dist < dist[v]:
                    dist[v] = nueva_dist
                    pred[v] = u
                    print(f"  Actualizado {v}: viene de {u}, nuevo costo = {nueva_dist}")

        print("\nEtiquetas actuales:")
        for v in graph.get_vertices():
            costo = "∞" if dist[v] == math.inf else dist[v]
            print(f"{v}: ({costo}, {pred[v]})")
        print()

    # Reconstruir camino más corto
    path = []
    actual = target_id
    while actual is not None:
        path.insert(0, actual)
        actual = pred[actual]

    print(f"Camino más corto de {start_id} a {target_id}: {' → '.join(path)}")
    print(f"Distancia total: {dist[target_id]}")
    return dist, pred, path


def bellman_ford(graph, start):
    dist = {nodo: float('inf') for nodo in graph}
    pred = {nodo: None for nodo in graph}
    dist[start] = 0

    for _ in range(len(graph)-1):
        for u in graph:
            for v, in graph[u].items():
                if dist[u] + graph[u][v] < dist[v]:
                    dist[v] = dist[u] + graph[u][v]
                    pred[v] = u

    # Verificar ciclos negativos
    for u in graph:
        for v, peso in graph[u].items():
            if dist[u] + peso < dist[v]:
                print("El grafo contiene un ciclo de peso negativo")
                return None, None
    return dist, pred

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0

    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso

            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola_prioridad, (distancia, vecino))

    return distancias
