import math


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